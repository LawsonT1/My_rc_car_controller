import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import can
import struct

class CanMess(Node):
    def __init__(self):
        super().__init__("can_mess")
        self.declare_parameter("can_interface", "can0")
        can_interface = self.get_parameter("can_interface").value

        self.subscription = self.create_subscription(
            Twist,
            '/cmd_drive',
            self.cmd_drive_callback,
            10
        )

        self.bus = None
        try:
            self.bus = can.interface.Bus(interface='socketcan', channel=can_interface, bitrate=1000000)
            self.get_logger().info(f"Connected to CAN bus '{can_interface}'")
        except Exception as e:
            self.get_logger().error(f"Cannot access SocketCAN device {can_interface}: {e}")
            self.get_logger().warn("CAN messages will be skipped until interface is available")

    def cmd_drive_callback(self, msg):
        velocity = msg.linear.x
        steering = msg.angular.z

        # Sending the drive motor CAN message (0x11)
        self.send_can_message(0x11, velocity)

        # Sending the steering motor CAN message (0x12)
        self.send_can_message(0x12, steering)

    def send_can_message(self, motor_id, value):
        # Pack the value as a 4 byte float
        data = struct.pack('>f', value)

        # Construct arbitration ID the same way the rover does
        priority = 0x0
        command_id = 0x03
        sender_node_id = 0x01
        arbitration_id = priority << 24 | command_id << 16 | motor_id << 8 | sender_node_id

        message = can.Message(
            arbitration_id=arbitration_id,
            data=data,
            is_extended_id=True
        )

        if self.bus is None:
            self.get_logger().warning('CAN bus unavailable, skipping CAN message send')
            return

        self.bus.send(message)
        self.get_logger().info(f'Sent CAN message to motor {hex(motor_id)}, value: {value}')

def main(args=None):
    rclpy.init(args=args)
    node = CanMess()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()