



# Kiến trúc thượng tầng



<p id="gdcalert5" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image5.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert6">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image5.png "image_tooltip")



# Programming library

Programming library là phương thức gửi lệnh MAVlink từ máy tính nhúng (hoặc GCS) đến flight controller bằng cách lập trình. 

Ví dụ về một số thư viện: MAVROS, Pymavlink, Dronekit, MAVSDK.


# MAVlink

MAVlink là một message protocol gọn nhẹ dùng để giao tiếp với drone (và giữa những phần tử trên drone)

Điểm nổi bật[[.]](https://mavlink.io/en/):

- Hiệu suất cao: MAVlink 1 chỉ có 8 bytes overhead, MAVlink 2 chỉ có 14 bytes overhead (vì lý do bảo mật và để mở rộng). 

- Đáng tin cậy: MAVlink được sử dụng từ 2009 cho nhiều loại phương tiện, trạm kiểm soát... kể cả trong những trường hợp môi trường giao tiếp gặp nhiều khó khăn (độ trễ cao/ nhiễu), vì MAVlink hỗ trợ phương pháp xác định packet drop, tín hiệu lỗi, xác thực packet.

- Hỗ trợ nhiều ngôn ngữ lập trình, chạy được trên vi điều khiển và nhiều hệ điều hành. 

- Cho phép 255 hệ thống hoạt động cùng lúc trên network

- Cho phép giao tiếp onboard và offboard.


## Cấu trúc:



<p id="gdcalert6" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image6.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert7">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image6.png "image_tooltip")



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
   <td>0-2
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
   </td>
   <td>
   </td>
   <td>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>
   </td>
   <td>
   </td>
   <td>
   </td>
   <td>
   </td>
  </tr>
</table>
