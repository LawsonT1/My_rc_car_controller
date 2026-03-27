
import launch
from launch_ros.actions import Node

def generate_launch_description():

    joy_node = Node(
          package="joy",
          executable="joy_node",
          name="joy_node",
          output="screen"
    )
    relay_joy_node = Node(
        package="rc_car_controller",
        executable="relay_joy",
        name="relay_joy",
        output="screen",
    )

    can_mess_node = Node(
        package="rc_car_controller",
        executable="can_mess",
        name="can_mess",
        output="screen"
    )

    return launch.LaunchDescription([
        relay_joy_node,
        can_mess_node,
        joy_node,
    ])


if __name__ == '__main__':
        generate_launch_description()
