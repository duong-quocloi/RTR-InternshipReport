# Note:

Yêu cầu trước khi setup:



1. [Installing Ardupilot and MAVProxy [20.04]](https://github.com/Intelligent-Quads/iq_tutorials/blob/master/docs/Installing_Ardupilot_20_04.md)
2. [Installing Gazebo and ArduPilot Plugin [18.04-20.04]](https://github.com/Intelligent-Quads/iq_tutorials/blob/master/docs/installing_gazebo_arduplugin.md)
3. [Installing ROS and MAVROS [20.04]](https://github.com/Intelligent-Quads/iq_tutorials/blob/master/docs/installing_ros_20_04.md)


# Set up package:

Ở thư mục catkin_ws, tạo package mới `control_uav` với các build dependency package `rospy`, `mavlink`, `mavros`, `sensor_msgs`, `std_msgs` như sau:
```
catkin_create_pkg control_uav rospy mavlink mavros sensor_msgs std_msgs
```

# Thêm script vào package:

Tạo một folder mới mang tên `scripts` trong thư mục `control_uav` và thêm các file python vào. Cây thư mục nhìn tổng quan như sau:
```
catkin_ws/
└── src/
    └── control_uav/
        ├── scripts/
        │   ├── control_node.py
        │   ├── img_node.py
        │   ├── show_img_node.py
        │   └── PrintColours.py
        ├── src/
        ├── CMakeLists.txt
        └── package.xml
```
# Cập nhật file CMakeLists:
Trong file `CMakeLists.txt`, ở dưới `catkin_package()`, thêm đoạn code sau:
```
catkin_install_python(PROGRAMS scripts/control_node.py scripts/img_node.py scripts/PrintColours.py scripts/show_img_node.py
DESTINATION $(CATKIN_PACKAGE_BIN_DESTINATION)
)
```
![carbon](https://user-images.githubusercontent.com/67494883/187826758-1a591d2d-c9ec-4f24-b799-ee6cb95090e2.png)

# Build lại workspace:
Tại thư mục `catkin_ws`, chạy lệnh sau:
```
catkin_make
source devel/setup.bash
```
# Chạy code:

```
rosrun <tên_pkg> <file python>
```
Note: nếu dùng `rosrun`, file python phải bắt đầu bằng `#!/usr/bin/env python`
