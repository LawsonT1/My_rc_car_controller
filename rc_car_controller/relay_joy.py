import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

class MyNode(Node):
    def __init__(self):
        super().__init__("relay_joy")
        self.subscription = self.create_subscription(
            Joy, '/joy', self.joy_callback, 10
        )
        self.publisher = self.create_publisher(Twist, '/cmd_drive', 10)
        self.max_linear_speed = 1.0
        self.max_steering_angle = 1.0

    def joy_callback(self, msg):
        twist = Twist()
        twist.linear.x = msg.axes[1] * self.max_linear_speed
        twist.angular.z = msg.axes[0] * self.max_steering_angle
        self.publisher.publish(twist)

        self.get_logger().info('Received joy message')
        # I may add choose to show user the values of twist.linear.x
        # or twist.angular.z in this same message.
        

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()