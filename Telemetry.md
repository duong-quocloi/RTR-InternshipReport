# Ứng dụng của telemetry trên drone

	Bằng cách sử dụng Telemetry, người dùng có thể nhận được thông số và trạng thái của drone trong thời gian thực (vd dung lượng pin, nhiệt độ, độ cao,..) , từ đó phi công có thể phản ứng kịp thời trước các tình huống. Trong Ground Control Station còn cho phép người dùng điều khiển drone mà không đến tay cầm hay port USB (thay đổi các thông số trong ardupilot, thay đổi flight plan,...). 

Ngoài ra, ardupilot còn hỗ trợ telemetry log cho máy tính. Tính năng này cho phép người dùng mô phỏng lại mission (mission playback), chắt lọc những thông số và waypoint cần thiết, vẽ lại đồ thị,... giúp người dùng phân tích chuyến bay. Một số flight controller không có thẻ nhớ để lưu trữ log nên tính năng này đặc biệt quan trọng. 


# Các lựa chọn Telemetry tầm gần cho drone

Ardupilot có đề cập một số lựa chọn để ứng dụng telemetry. Lưu ý rằng một số tay cầm RC đã tích hợp sẵn tính năng này mà không cần những module hỗ trợ. Nhưng không thể kết nối với GCS qua cách này. 


<table>
  <tr>
   <td>Type
   </td>
   <td>Module
   </td>
   <td>Range
   </td>
   <td>Baud rate
   </td>
   <td>Protocol
   </td>
   <td>Note
   </td>
  </tr>
  <tr>
   <td>Bluetooth
   </td>
   <td><a href="https://ardupilot.org/copter/docs/common-mission-planner-bluetooth-connectivity.html">Bluetooth telemetry modem p</a>
<p>
<em>(Y-MCU Bluetooth Board Module)</em>
   </td>
   <td>50 m
   </td>
   <td>57600
   </td>
   <td>Bluetooth
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td rowspan="5" >Wifi
   </td>
   <td rowspan="2" ><a href="https://ardupilot.org/copter/docs/common-cuav-pwlink.html">CUAV PW-Link</a>
   </td>
   <td>200 m
   </td>
   <td rowspan="2" >57600
   </td>
   <td rowspan="2" >MAVLink2
   </td>
   <td rowspan="4" >* Có thể lắp thêm antena để tăng khoảng cách truyền
   </td>
  </tr>
  <tr>
   <td>450 m (external antenna)
   </td>
  </tr>
  <tr>
   <td><a href="https://ardupilot.org/copter/docs/common-esp8266-telemetry.html">ESP8266</a>
   </td>
   <td>~100 m <a href="https://discuss.ardupilot.org/t/esp8266-wifi-on-pixhawk/14681/17">[1]</a>
   </td>
   <td>921600
   </td>
   <td>MAVLink
   </td>
  </tr>
  <tr>
   <td rowspan="2" ><a href="https://ardupilot.org/copter/docs/common-esp32-telemetry.html">ESP32</a>
   </td>
   <td rowspan="2" >~50 m - 200 m
   </td>
   <td rowspan="2" >115200
   </td>
   <td rowspan="2" >MAVLink
   </td>
  </tr>
  <tr>
   <td>* Có thể flash firmware của DroneBridge để sử dụng ứng dụng DroneBridge trên Android.
   </td>
  </tr>
  <tr>
   <td rowspan="5" >Radio
   </td>
   <td rowspan="2" ><a href="https://ardupilot.org/copter/docs/common-frsky-telemetry.html">FrSky RX (SPort or FPort)</a>
   </td>
   <td rowspan="2" >-
   </td>
   <td rowspan="2" >300 <a href="https://community.emlid.com/t/telemetry-to-frsky-receiver/186/4">[2]</a>
   </td>
   <td rowspan="2" >FrSky SPort Passthrough (OpenTX)
   </td>
   <td>* Có thể thay đổi thông số bằng Yaapu LUAGCS script với OpenTX
   </td>
  </tr>
  <tr>
   <td rowspan="3" >* OSD
<p>
* Ưu điểm:
<p>
- Dùng để bay khi không có GCS mà vẫn có thể giám sát được các thông số
<p>
- Phương án dự phòng khi GCS không hoạt động (kết nối MAVlink bị ngắt)
<p>
- Khi đã có 1 người khác giám sát GCS
<p>
- Phù hợp cho các phi công cần phản ứng nhanh
   </td>
  </tr>
  <tr>
   <td><a href="https://ardupilot.org/copter/docs/common-hott-telemetry.html">HOTT Telemetry</a>
   </td>
   <td>-
   </td>
   <td>19200
   </td>
   <td>HottTelem
   </td>
  </tr>
  <tr>
   <td><a href="https://ardupilot.org/copter/docs/common-msp-overview.html">Multiwii Serial Protocol</a>
   </td>
   <td>-
   </td>
   <td>115200
   </td>
   <td>MSP
   </td>
  </tr>
  <tr>
   <td><a href="https://ardupilot.org/copter/docs/common-3dr-radio-v1.html">SiK Radio</a>
   </td>
   <td>> 300 m
   </td>
   <td>57600
   </td>
   <td>MAVLink2
   </td>
   <td>
   </td>
  </tr>
</table>



# Set up bằng ESP8266

	Trong bài viết này, người viết sử dụng ESP8266 để làm telemetry cho drone, với lý do như sau:



1. Kết nối wifi ổn định và có tốc độ cao hơn Bluetooth rất nhiều
2. ESP8266 có giá thành tương đối rẻ


## Tải firmware



* [firmware-esp01_1m.bin](https://firmware.ardupilot.org/Tools/MAVESP8266/latest/firmware-esp01_1m.bin) cho các board có 1MB flash (thông dụng nhất)
* [firmware-esp01.bin](https://firmware.ardupilot.org/Tools/MAVESP8266/latest/firmware-esp01.bin) cho các board có 512KB flash (các board cũ)
* [firmware-esp12e.bin](https://firmware.ardupilot.org/Tools/MAVESP8266/latest/firmware-esp12e.bin) cho các board có 1MB flash


## Flash firmware trên máy tính

*Lưu ý*: Với loại board Adafruit HUZZAH ESP8266, cần phải bật bootloader mode để flash. Sau khi kết nối với máy tính qua dây FTDI, nhấn giữ đồng thời nút Reset và GPIO0, sau đó lần lượt thả nút Reset và GPIO0 ra. Đèn LED sẽ sáng màu đỏ.


### MAC & LINUX



1. Tải [esptool](https://github.com/espressif/esptool) về máy.
2. Chạy dòng lệnh sau[[3]](https://aiqianji.com/openoker/PX4-user_guide/raw/d4a9e67aceb249ce869ece14da97788ac3c042e6/zh/telemetry/esp8266_wifi_module.md):

python3 esptool.py --baud 921600 --port /dev/your_serial_port write_flash 0x00000 firmware_xxxxx.bin


### Window



1. Tải NodeMCU flasher ([64bit](https://github.com/nodemcu/nodemcu-flasher/blob/master/Win64/Release/ESP8266Flasher.exe) or[ 32bit](https://github.com/nodemcu/nodemcu-flasher/blob/master/Win32/Release/ESP8266Flasher.exe))
2. Ở tab Advance, chỉnh Flash size = 4MB
3. Ở tab Config, nhấn biểu tượng bánh răng và chọn firmware vừa tải về
4. Ở tab Operation, chọn cổng COM phù hợp và nhấn Flash


## Thay đổi SSID và mật khẩu

Kết nối đến điểm wifi bằng máy tính (SSID = Ardupilot, mật khẩu = Ardupilot)

Vào trình duyệt và truy cập địa chỉ 192.168.4.1

Nhấn "Set up"

Chỉnh lại ô "AP SSID" and "AP Password", nhấn Save và khởi động lại ESP


## Chỉnh lại tham số trên ardupilot



1. Kết nối ESP với Flight controller thông qua cổng Telem1/2
2. Thay đổi các hệ số sau (thay x bằng ID serial của tổng Telem. Tham khảo Pinout của Flight controller để biết thêm chi tiết ) :
* [SERIALx_PROTOCOL](https://ardupilot.org/copter/docs/parameters.html#serial1-protocol) = 2 (MAVLink2) or 1 (MAVLink1)
* [SERIALx_BAUD](https://ardupilot.org/copter/docs/parameters.html#serial1-baud) = 921 (921600 baud)


## Kết quả



![image](https://user-images.githubusercontent.com/67494883/189047356-e5f4d03c-fe85-4a21-8b0a-9cafa51b9b96.png)



_Kết nối với Network_


![image](https://user-images.githubusercontent.com/67494883/189047607-51ae6692-d558-43e8-a660-0c1a0c61cb7a.png)


_Trên Missionplanner, chọn UDP với baudrate 921600 và kết nối_

![image](https://user-images.githubusercontent.com/67494883/189047657-ac41a524-300f-4298-8976-a3de6ec50e47.png)



_Chọn port_

![image](https://user-images.githubusercontent.com/67494883/189047561-cc8aaacd-d46e-491f-be93-f9d0e7c91cbc.png)



_Kết nối thành công_


# Tham khảo



1. [Telemetry (landing page) (ardupilot.org)](https://ardupilot.org/copter/docs/common-telemetry-landingpage.html)
2. [ESP8266 wifi telemetry (ardupilot.org)](https://ardupilot.org/copter/docs/common-esp8266-telemetry.html)
3. Drone Community Discord server
