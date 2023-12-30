from launch_ros.actions import Node, SetParameters

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression

def generate_launch_description():
    turtlesim_ns = LaunchConfiguration('turtlesim_ns')
    use_provided_red = LaunchConfiguration('use_provided_red')
    new_background_r = LaunchConfiguration('new_background_r')

    turtlesim_ns_launch_arg = DeclareLaunchArgument(
        'turtlesim_ns',
        default_value='turtlesim1'
    )
    use_provided_red_launch_arg = DeclareLaunchArgument(
        'use_provided_red',
        default_value='True'
    )
    new_background_r_launch_arg = DeclareLaunchArgument(
        'new_background_r',
        default_value='200'
    )

    turtlesim_node = Node(
        package='turtlesim',
        namespace=turtlesim_ns,
        executable='turtlesim_node',
        name='sim'
    )
    spawn_turtle = Node(
        package='turtlesim',
        namespace=turtlesim_ns,
        executable='spawn',
        output='screen',
        arguments=['2', '2', '0.2'],
        remappings=[('/turtlesim1/cmd_vel', '/%s/cmd_vel' % turtlesim_ns)]
    )
    
    change_background_r = Node(
        package='ros2_turtlesim',
        executable='set_background',
        namespace=turtlesim_ns,
        output='screen',
        arguments=[new_background_r],
        condition=IfCondition(PythonExpression(
            [new_background_r, ' != 200 or not ', use_provided_red]
        ))
    )

    return LaunchDescription([
        turtlesim_ns_launch_arg,
        use_provided_red_launch_arg,
        new_background_r_launch_arg,
        turtlesim_node,
        spawn_turtle,
        SetParameters(
            [
                {'background_r': int(new_background_r)},
            ],
            namespace=turtlesim_ns
        ),
        TimerAction(
            period=2.0,
            actions=[change_background_r],
        )
    ])
