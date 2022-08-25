# Kiến trúc thượng tầng



<p id="gdcalert1" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image1.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert2">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image1.png "image_tooltip")



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



<p id="gdcalert2" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image2.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert3">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image2.png "image_tooltip")



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

	Trong ví dụ này, ta sẽ dùng pyMAVlink để điều khiển độ cao drone theo giá trị của throttle stick (1000-2000 ↔1m - 11m)
