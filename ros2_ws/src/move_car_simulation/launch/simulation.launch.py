import os

from ament_index_python.packages import get_package_share_directory #获取包的共享目录
from launch import LaunchDescription #启动描述
from launch.actions import DeclareLaunchArgument, ExecuteProcess, SetEnvironmentVariable #声明启动参数，执行进程，设置环境变量
from launch.conditions import IfCondition #条件
from launch.substitutions import LaunchConfiguration #启动配置
from launch_ros.actions import Node #启动ROS节点


def generate_launch_description(): #生成启动描述
    description_share = get_package_share_directory('move_car_description') #获取描述包的共享目录
    urdf_path = os.path.join(description_share, 'urdf', 'move_car.urdf') #获取URDF文件路径
    world_path = os.path.join(description_share, 'world', 'room.world') #获取世界文件路径
    gui = LaunchConfiguration('gui')
    # 本机 GAZEBO_MODEL_PATH 只有 TurtleBot3，官方 gzserver 启动脚本因此找不到sun 和 ground_plane，会一直等网络下载。这里直接使用系统模型。
    gazebo_env = { #设置Gazebo环境变量
        'GAZEBO_MODEL_PATH': '/usr/share/gazebo-11/models', #Gazebo模型路径
        'GAZEBO_RESOURCE_PATH': '/usr/share/gazebo-11', #Gazebo资源路径
        'ROS_DOMAIN_ID': '42', #ROS域ID
    }

    with open(urdf_path, 'r', encoding='utf-8') as urdf_file: #读取URDF文件
        robot_description = urdf_file.read() #读取URDF文件内容 

    return LaunchDescription([
        DeclareLaunchArgument('gui', default_value='true'), #声明启动参数，默认值为true
        # 实车节点在域 0，仿真固定用 42，避免两个 /odom 互相覆盖。
        SetEnvironmentVariable('ROS_DOMAIN_ID', '42'),
        ExecuteProcess(
            cmd=[
                'gzserver', world_path,
                '-s', 'libgazebo_ros_init.so',
                '-s', 'libgazebo_ros_factory.so',
            ],
            additional_env=gazebo_env,
            output='screen',
        ),
        ExecuteProcess(
            cmd=['gzclient'], #启动Gazebo客户端
            additional_env=gazebo_env,
            output='screen',
            condition=IfCondition(gui),
        ),
        Node(
            package='robot_state_publisher', #机器人状态发布器
            executable='robot_state_publisher',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'robot_description': robot_description,
            }],
        ),
        Node(
            package='gazebo_ros', #Gazebo ROS节点
            executable='spawn_entity.py',
            output='screen',
            arguments=[
                '-entity', 'move_car',
                '-file', urdf_path,
                '-x', '0.7',
                '-y', '0.0',
                '-z', '0.0',
                '-Y', '0.0',
            ],
        ),
        Node(
            package='nav2_collision_monitor', #碰撞监视器
            executable='collision_monitor',
            name='collision_monitor',
            output='screen',
            parameters=[os.path.join(
                get_package_share_directory('move_car_navigation'),
                'config',
                'collision_monitor.yaml',
            )],
        ),
        Node(
            package='nav2_lifecycle_manager', #生命周期管理器
            executable='lifecycle_manager',
            name='lifecycle_manager_safety',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'autostart': True,
                'node_names': ['collision_monitor'],
            }],
        ),
    ])
