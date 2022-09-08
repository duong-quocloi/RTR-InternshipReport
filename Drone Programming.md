# Kiến trúc thượng tầng

![alt_text](https://user-images.githubusercontent.com/67494883/186568698-328ace6e-ce33-4f7c-9964-6a2b4bf6aef8.png)




# Programming library

Programming library là phương thức gửi lệnh MAVlink từ máy tính nhúng (hoặc GCS) đến flight controller bằng cách lập trình. 

Ví dụ về một số thư viện: MAVROS, Pymavlink, Dronekit, MAVSDK.


# MAVlink

MAVlink là một message protocol gọn nhẹ dùng để giao tiếp với drone (và giữa những phần tử trên drone)

Điểm nổi bật[[1]](https://mavlink.io/en/):

- Hiệu suất cao: MAVlink 1 chỉ có 8 bytes overhead, MAVlink 2 chỉ có 14 bytes overhead (vì lý do bảo mật và để mở rộng). 

- Đáng tin cậy: MAVlink được sử dụng từ 2009 cho nhiều loại phương tiện, trạm kiểm soát... kể cả trong những trường hợp môi trường giao tiếp gặp nhiều khó khăn (độ trễ cao/ nhiễu), vì MAVlink hỗ trợ phương pháp xác định packet drop, tín hiệu lỗi, xác thực packet.

- Hỗ trợ nhiều ngôn ngữ lập trình, chạy được trên vi điều khiển và nhiều hệ điều hành. 

- Cho phép 255 hệ thống hoạt động cùng lúc trên network

- Cho phép giao tiếp onboard và offboard.


## Cấu trúc:



![alt_text](https://user-images.githubusercontent.com/67494883/186568827-eb8cfab1-c4fa-4ee9-ac75-bf5fc83f49ed.png)




<table>
  <tr>
   <td>Vị trí bit
   </td>
   <td>Nội dung
   </td>
   <td>Giá trị
   </td>
   <td>Giải thích
   </td>
  </tr>
  <tr>
   <td>0
   </td>
   <td>Bit khởi đầu của thông điệp 
   </td>
   <td>0xFD
   </td>
   <td>Đánh dấu điểm đầu của của packet được gửi
   </td>
  </tr>
  <tr>
   <td>1
   </td>
   <td>Độ dài của Payload
   </td>
   <td>0-255
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>2
   </td>
   <td>Flag không tương thích
   </td>
   <td>
   </td>
   <td>Đánh dấu feature mà thư viện MAVlink phải hỗ trợ để có thể xử lý được package
   </td>
  </tr>
  <tr>
   <td>3
   </td>
   <td>Flag tương thích
   </td>
   <td>
   </td>
   <td>Đánh dấu feature mà thư viện MAVlink, dù không có hỗ trợ, vẫn có thể xử lý được package
   </td>
  </tr>
  <tr>
   <td>4
   </td>
   <td>Số thứ tự của packet
   </td>
   <td>0-255
   </td>
   <td>Dùng để xác định packet loss. Số sẽ được tăng lên sau mỗi thông điệp được gửi đi
   </td>
  </tr>
  <tr>
   <td>5
   </td>
   <td>System ID (sender)
   </td>
   <td>1-255
   </td>
   <td>ID của hệ thống gửi thông điệp đi, dùng để phân biệt các hệ thống trên network
   </td>
  </tr>
  <tr>
   <td>6
   </td>
   <td>Component ID (sender)
   </td>
   <td>1-255
   </td>
   <td>ID của phần tử (trên hệ thống) gửi đi, dùng để phân biệt các phần tử trên cùng 1 hệ thống.
   </td>
  </tr>
  <tr>
   <td>7-9
   </td>
   <td>Message ID
   </td>
   <td>0 - 16777215
   </td>
   <td>ID của loại thông điệp trong payload
   </td>
  </tr>
  <tr>
   <td>9+n
   </td>
   <td>Payload
   </td>
   <td>
   </td>
   <td>Nội dung của thông điệp 
   </td>
  </tr>
  <tr>
   <td>n+10 - n+11
   </td>
   <td>Checksum
   </td>
   <td>
   </td>
   <td>CRC-16/MCRF4XX cho message (trừ magic byte). Bao gồm CRC_EXTRA byte.
   </td>
  </tr>
  <tr>
   <td>n+12 - n+25
   </td>
   <td>Signature
   </td>
   <td>
   </td>
   <td>(Optional) Để đảm bảo tính bảo mật của liên kết
   </td>
  </tr>
</table>



## MAVlink message

Mỗi thông điệp sẽ có định nghĩa riêng. Để tra cứu, danh sách các thông điệp MAVlink có thể tìm được ở [đây](https://mavlink.io/en/messages/common.html#SYS_STATUS).

Để minh hoạ, chúng ta sẽ xét COMMAND_LONG ( #76 ). Đây là thông điệp dùng để thực thi lệnh MAVlink. Chúng ta có thể điều khiển drone gián tiếp thông qua thông điệp này.

Thông điệp được định nghĩa theo bảng sau:


<table>
  <tr>
   <td><strong>Field Name</strong>
   </td>
   <td><strong>Type</strong>
   </td>
   <td><strong>Values</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td>target_system
   </td>
   <td>uint8_t
   </td>
   <td>
   </td>
   <td>System which should execute the command
   </td>
  </tr>
  <tr>
   <td>target_component
   </td>
   <td>uint8_t
   </td>
   <td>
   </td>
   <td>Component which should execute the command, 0 for all components
   </td>
  </tr>
  <tr>
   <td>command
   </td>
   <td>uint16_t
   </td>
   <td><a href="https://mavlink.io/en/messages/common.html#MAV_CMD">MAV_CMD</a>
   </td>
   <td>Command ID (of command to send).
   </td>
  </tr>
  <tr>
   <td>confirmation
   </td>
   <td>uint8_t
   </td>
   <td>
   </td>
   <td>0: First transmission of this command. 1-255: Confirmation transmissions (e.g. for kill command)
   </td>
  </tr>
  <tr>
   <td>param1
   </td>
   <td>float
   </td>
   <td>
   </td>
   <td>Parameter 1 (for the specific command).
   </td>
  </tr>
  <tr>
   <td>param2
   </td>
   <td>float
   </td>
   <td>
   </td>
   <td>Parameter 2 (for the specific command).
   </td>
  </tr>
  <tr>
   <td>param3
   </td>
   <td>float
   </td>
   <td>
   </td>
   <td>Parameter 3 (for the specific command).
   </td>
  </tr>
  <tr>
   <td>param4
   </td>
   <td>float
   </td>
   <td>
   </td>
   <td>Parameter 4 (for the specific command).
   </td>
  </tr>
  <tr>
   <td>param5
   </td>
   <td>float
   </td>
   <td>
   </td>
   <td>Parameter 5 (for the specific command).
   </td>
  </tr>
  <tr>
   <td>param6
   </td>
   <td>float
   </td>
   <td>
   </td>
   <td>Parameter 6 (for the specific command).
   </td>
  </tr>
  <tr>
   <td>param7
   </td>
   <td>float
   </td>
   <td>
   </td>
   <td>Parameter 7 (for the specific command).
   </td>
  </tr>
</table>


Lệnh MAVlink MAV_CMD_NAV_TAKEOFF #22 được định nghĩa như sau:


<table>
  <tr>
   <td><strong>Param (:Label)</strong>
   </td>
   <td><strong>Description</strong>
   </td>
   <td><strong>Units</strong>
   </td>
  </tr>
  <tr>
   <td>1: Pitch
   </td>
   <td>Minimum pitch (if airspeed sensor present), desired pitch without sensor
   </td>
   <td>deg
   </td>
  </tr>
  <tr>
   <td>2
   </td>
   <td>Empty
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>3
   </td>
   <td>Empty
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>4: Yaw
   </td>
   <td>Yaw angle (if magnetometer present), ignored without magnetometer. NaN to use the current system yaw heading mode (e.g. yaw towards next waypoint, yaw to home, etc.).
   </td>
   <td>deg
   </td>
  </tr>
  <tr>
   <td>5: Latitude
   </td>
   <td>Latitude
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>6: Longitude
   </td>
   <td>Longitude
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>7: Altitude
   </td>
   <td>Altitude
   </td>
   <td>m
   </td>
  </tr>
</table>


Giả sử ta muốn dùng thông điệp để drone cất cánh (MAV_CMD_NAV_TAKEOFF) với pitch bằng 15 độ, và yaw bằng 10 độ, với độ cao 5 m. Khi đó, thông điệp sẽ có dạng


<table>
  <tr>
   <td>target_system
   </td>
   <td>target_component
   </td>
   <td>command
   </td>
   <td>confirmation
   </td>
   <td>param1
   </td>
   <td>param2
   </td>
   <td>param3
   </td>
   <td>param4
   </td>
   <td>param5
   </td>
   <td>param6
   </td>
   <td>param7
   </td>
  </tr>
  <tr>
   <td>target_system
   </td>
   <td>target_component
   </td>
   <td>22
   </td>
   <td>0
   </td>
   <td>15
   </td>
   <td>0
   </td>
   <td>0
   </td>
   <td>10
   </td>
   <td>0
   </td>
   <td>0
   </td>
   <td>5
   </td>
  </tr>
</table>



# Pymavlink

PyMAVlink có thể được xem là một phiên bản áp dụng giao thức MAVlink bằng python. Thư viện này cũng bao gồm các hàm để gửi thông điệp MAVlink qua UDP/TCP hoặc Serial-Radio. Điểm mạnh của nó là rất dễ cài đặt và đa dụng vì chạy bằng python, phù hợp cho các ứng dụng drone tự động <span style="text-decoration:underline;">đơn giản</span>, hoặc các ứng dụng giám sát drone từ xa.


## Ví dụ sử dụng PyMAVlink trong lập trình drone

Trong ví dụ này, ta sẽ dùng pyMAVlink để điều khiển độ cao drone theo giá trị của throttle stick (1000-2000 ↔ 1m - 11m)
*Note*: Thay vì đọc giá trị row/pitch rồi set theo x,y. Chúng ta có thể dùng mavutil.mavlink_connection.mav.rc_channels_override_send
```python
#import một số thư viện cần dùng. module mavutil có nhiều hàm để hỗ trợ cho việc kết nối và gửi thông điệp
from pymavlink import mavutil
from time import sleep

# Tạo kết nối qua cổng UDP. 14550 14551 là 2 cổng mặc định của mavlink connection stream. Ta sẽ sử dụng port 14550 cho GCS
the_connection = mavutil.mavlink_connection('udpin:localhost:14551')

# Chờ xác nhận kết nối -> Lấy được system ID, component ID của liên kết
the_connection.wait_heartbeat() 
print("Heartbeat from system (system %u component %u)" %
      (the_connection.target_system, the_connection.target_component))

#Arm the quad
the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)

#Take off
the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 1)
msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)
sleep(5)

#Tạo biến toạ độ tương đối x,y,z và vận tốc v
x_rev = 0
y_rev = 0
z_rev = 0
v = 5

while 1:
    #Đọc tín hiệu gửi về, và lọc ra, chỉ đọc của RC_CHANNELS
    msg = the_connection.recv_match(type='RC_CHANNELS', blocking=True)

    #print('{} {} {} {}'.format(msg.chan1_raw,msg.chan2_raw,msg.chan3_raw,msg.chan4_raw))
    rollI = (msg.chan1_raw-1515)/100
    pitchI = (msg.chan2_raw-1500)/100
    yawI = (msg.chan4_raw-1517)/100
    throttleI = -((msg.chan3_raw-1000)/100 +1)

    x_rev += pitchI
    y_rev += rollI
    z_rev = throttleI

    #print("{} {} {}".format(x_rev,y_rev,z_rev))
    the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, the_connection.target_system,
                        the_connection.target_component, mavutil.mavlink.MAV_FRAME_LOCAL_NED, int(0b110111000000), x_rev, y_rev, z_rev, v, v, 0, 0, 0, 0, 0, 0))
```
### Video demo
[![Throttle value to height](https://res.cloudinary.com/marcomontalbano/image/upload/v1661399342/video_to_markdown/images/youtube--XIMLoLxmTDw-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://youtu.be/icSMvVgDrow "Throttle value to height")

# MAVROS

MAVROS là một lựa chọn dành cho những ai sử dụng ROS. ROS đặc biệt hữu dụng cho việc kết hợp các hệ thống khác nhau trên cùng 1 thiết bị nhờ vào khả năng truyền dữ liệu giữa các hệ thống với nhau.

![Graphic design is my passion(1)](https://user-images.githubusercontent.com/67494883/187829555-4cdf11c2-b55d-4a5a-8283-17eaf7b75750.png)

_Ảnh trên minh hoạ kiến trúc chung của Companion Computer chạy trên ROS._

Ví dụ ở một kiến trúc thường gặp trên Companion Computer sử dụng ROS. Giả sử ta có một node được thiết kế với nhiệm vụ đọc tín hiệu camera và xử lý ảnh, sau đó dữ liệu được chuyển qua một Node chuyển đổi để tính toạ độ theo hệ quy chiếu chung (cho thuật toán tìm đường chẳng hạn). Thuật toán sẽ gửi các lệnh tìm đường đến Node MAVROS để chuyển qua MAVlink cho flight controller. 


## Ví dụ sử dụng MAVROS trong lập trình drone


### Nhiệm vụ:

Drone sẽ đọc hình ảnh từ camera và di chuyển đến mép đường bay.


### Mô tả:

Hệ thống sẽ gồm 3 Node: 



* 1 Node dùng để hiện luồng ảnh từ topic `/webcame/image_raw` thông qua `cv_bridge`
* 1 Node để xử lý ảnh: Đọc ảnh topic `/webcame/image_raw` thông qua `cv_bridge`, đếm số pixel của mặt đường. Nếu số pixel của đường > 15% tổng số pixel thì vẫn xem là drone ở trong đường bay. Trả về topic `img_signal`
* 1 Node để điều khiển drone: Đọc tín hiệu từ topic `img_signal`, nếu tín hiệu là true, sẽ cho drone bay sang phải 0.5 đơn vị.

![Screenshot from 2022-09-01 09-25-30](https://user-images.githubusercontent.com/67494883/187829613-9208555c-55a9-464f-a4f9-2035e8d9e4d3.png)

_Rqt graph_

### Video Demo:

[![Throttle value to height](https://res.cloudinary.com/marcomontalbano/image/upload/v1661399342/video_to_markdown/images/youtube--XIMLoLxmTDw-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://youtu.be/VqjRB8BPLlg "ROSPY Vision")

---

# Tham khảo



1. [MAVLink Introduction | Middleware for Open Source Drones](https://www.youtube.com/watch?v=iZ-usX1VXRI)
2. [MAVLink Messages | Dissecting the Protocol](https://www.youtube.com/watch?v=Ha66uKC-od0)
3. [Packet Serialization](https://mavlink.io/en/guide/serialization.html)
4. [Using Pymavlink Libraries (mavgen)](https://mavlink.io/en/mavgen_python/)
5. [https://github.com/ArduPilot/pymavlink](https://github.com/ArduPilot/pymavlink)
6. [Drone Programming Libraries 2021](https://www.youtube.com/watch?v=XpkEi7tFZGc&t=434s)
7. [ROS Tutorials Python - Beginner](https://youtu.be/C6BlNbeU3fQ?list=PLAjUtIp46jDcQb-MgFLpGqskm9iB5xfoP)
8. [iq_gnc package](https://github.com/Intelligent-Quads/iq_gnc)
9. [ROS Developers LIVE Class #86: How to use OpenCV with ROS](https://www.youtube.com/watch?v=0C0gOsLoP9k)
