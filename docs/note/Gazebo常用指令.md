## 启动 / 关闭

```bash
gazebo
```

打开 Gazebo（空世界 + 窗口）。

```bash
gazebo /usr/share/gazebo-11/worlds/empty.world
```

打开指定世界文件。

```bash
gazebo --verbose
```

多打日志，出问题好查。

本项目带小车启动（推荐平时用这个）：

```bash
ros2 launch move_car_simulation simulation.launch.py
```

关掉：在跑 Gazebo 的终端按 `Ctrl+C`。窗口关不干净时：

```bash
killall gzserver gzclient
```

---

## 两个进程分别是啥


| 命令         | 作用           |
| ---------- | ------------ |
| `gzserver` | 仿真计算（没窗口也能跑） |
| `gzclient` | 图形窗口         |
| `gazebo`   | 两个一起开        |


只要后端、不要窗口：

```bash
gzserver /usr/share/gazebo-11/worlds/empty.world
```

---

## 和本项目相关的

```bash
gazebo --version
```

看版本（你应是 11.x）。

```bash
export GAZEBO_MODEL_PATH=/usr/share/gazebo-11/models
```

让 Gazebo 找到地面、太阳等模型（本项目 launch 里已经设过）。

仿真时记得：

```bash
export ROS_DOMAIN_ID=42
```

---



## 窗口里常用操作（不是终端命令）

- 滚轮：缩放  
- 中键拖：平移视角  
- 左键点物体：选中  
- 右键：旋转视角（视设置而定）

