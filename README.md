# omnibot
## Environment setup

### Install ROS 2 Jazzy

Install instructions can be found [here](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html). Make sure to select the full desktop install (`ros-jazzy-desktop`) to ensure that we have access to GUI tools, such as RViz. Also install the dev tools (`ros-dev-tools`) so we can use `rosdep` and `colcon`. After installation, you can run this command to automatically source your ROS 2 install with every new terminal session (if you are using Bash).

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
```

### Clone the repo
```bash
mkdir ~/ros2_ws && cd ~/ros2_ws
git clone https://github.com/AxelD7/omnibot.git src
```

### Install ROS 2 dependencies

`rosdep` is a utility for installing and satisfying dependencies for ROS 2 packages. Read more about it [here](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Rosdep.html). 

```bash
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
```

### Build and source the workspace

`colcon` is a utility for compiling and building the workspace. 

```bash
# Build the workspace
colcon build --symlink-install --cmake-args=-DCMAKE_BUILD_TYPE=Release
# Source the workspace
. install/setup.bash
```

### Run (or launch) something!

For example, you can bring up the robot simulation with the main launch file:

```bash
ros2 launch omnibot_launch launch_sim.launch.py use_sim_time:=true
```

If you want to take her for a spin in the simulation, Open another terminal (source your workspace!):

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/omni_wheel_drive_controller/cmd_vel -p stamped:=true -p frame_id:=base_footprint
```