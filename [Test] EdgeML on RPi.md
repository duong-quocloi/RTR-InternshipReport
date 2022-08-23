
<p style="color: red; font-weight: bold">>>>>>  gd2md-html alert:  ERRORs: 0; WARNINGs: 1; ALERTS: 0.</p>
<ul style="color: red; font-weight: bold"><li>See top comment block for details on ERRORs and WARNINGs. <li>In the converted Markdown or HTML, search for inline alerts that start with >>>>>  gd2md-html alert:  for specific instances that need correction.</ul>

<p style="color: red; font-weight: bold">Links to alert messages:</p>
<p style="color: red; font-weight: bold">>>>>> PLEASE check and correct alert issues and delete this message and the inline alerts.<hr></p>


[Test] Sử dụng edge ML cho raspberry pi


# A. Edge ML


## 1. Định nghĩa

Edge ML là kỹ thuật sử dụng thiết bị thông minh để xử lý data cục bộ (ở sever địa phương hoặc hay trong thiết bị) bằng các thuật toán ML/DL nhằm giảm đi sự phụ thuộc vào các hệ thống đám mây. [[1]](https://www.fierceelectronics.com/electronics/what-edge-machine-learning)


## 2. Ưu điểm

- Không phụ thuộc vào đường truyền internet

- Chạy các ứng dụng ở thời gian thực

- Đáp ứng về vấn đề bảo mật

- Giá thành rẻ


## 3. Nhược điểm

- Model không được cập nhật liên tục 

- Không thể áp dụng Reinforcement learning

- Bị giới hạn ở một số loại model nhất định


# B. edge ML cho raspberry pi


## 1. Yêu cầu

Soft goal: 10 FPS, 300ms - 500ms latency

Goal: 20 FPS, 100 ms latency


## 2. Phần cứng

Raspberry Pi 4 Model B 8GB RAM


## 3. Frame work

- Framework sử dụng:

+ Pytorch: tiny-yolov5

+ Tensor flow: yolov5

+ Tensorflow lite: tiny-yolov3, efficient net, mobile net

- Một số framework khác (có tìm hiểu nhưng không sử dụng):

+ OpenVINO: Là một toolkit để tối ưu các model ML dành cho thiết bị của Intel. Có hỗ trợ RPi, nhưng document cũ (1 số thư viện cài đặt không còn được hỗ trợ) + quá trình cài đặt phức tạp.

+ TensorFlow Lite for Microcontrollers: Hướng đến việc ứng dụng trên vi điều khiển. Cài thử trên linux và quá trình cài đặt hơi phức tạp (C++ API cấp thấp)

+ Edge impulse: Một trong số rất nhiều development platform cho Edge ML hiện nay. Có hỗ trợ Model FOMO. Trong quá trình cài đặt gặp [bug](https://forum.edgeimpulse.com/t/cannot-detect-camera-when-using-raspberry-pi-4/4202/5) với RPi. Còn khá mới nên chưa được hỗ trợ nhiều.


## 4. Kết quả


<table>
  <tr>
   <td>Framework
   </td>
   <td>Model
   </td>
   <td>Inference time
   </td>
   <td>Note
   </td>
  </tr>
  <tr>
   <td rowspan="3" >Pytorch
   </td>
   <td rowspan="2" >Mobile net
   </td>
   <td>0.03 ms
   </td>
   <td rowspan="2" >- <a href="https://pytorch.org/tutorials/intermediate/realtime_rpi.html">Ví dụ</a> trang web chính thức của pytorch. 
<p>
- Nếu thêm bước lọc class theo xác suất thì FPS giảm xuống đáng kể
<p>
- Không có bounding box
   </td>
  </tr>
  <tr>
   <td>143 ms
   </td>
  </tr>
  <tr>
   <td>tiny-yolov5
   </td>
   <td>18.86 s 
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Tensorflow
   </td>
   <td>yolov5
   </td>
   <td>833 ms
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td rowspan="3" >Tensorflow lite
   </td>
   <td>tiny-yolov3 
   </td>
   <td>500 ms
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>mobile net
   </td>
   <td>130 ms
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Efficient net 0*
   </td>
   <td>110 ms (2s latency)
   </td>
   <td>Model efficient net của tflite có bao gồm một node mang tên "TFLite_Detection_PostProcess". Node này có tác dụng chia ra 4 output: Vị trí của boundingbox, tên class, score của box và số box detect được. 
<p>
Tất cả các model trên không có bước này, và muốn lọc ra được kết quả theo ý muốn phải thêm một thuật toán trung gian (vd Non max suppression).
<p>
Nếu có thể ứng dụng node này cho các model khác thì hiệu quả mang lại sẽ rất lớn
   </td>
  </tr>
</table>



## 5. Kết luận

Nhìn chung các model không thích hợp cho việc chạy real time.


## 6. Một số lưu ý

- Phiên bản hệ điều hành của RPi sẽ ảnh hưởng đến chất lượng của opencv(?). Có thể do xung đột thư viện hoặc vì 1 lý do chưa biết, nếu chạy code chỉ sử dụng camera, FPS ~ 3.

- 64bit của hệ OS không hỗ trợ thư viện camera.

- Việc cài đặt tensorflow rất kén phiên bản hệ điều hành của RPi (build bằng file whl sẽ fail). Người viết cài đặt thành công trên link [này](https://github.com/PINTO0309/Tensorflow-bin) với RasOS 64 bit/aarch64/glibc2.33 or glibc2.31

- Không khuyến khích cài Pytorch trên virtual environment vì thời gian build thư viện rất lâu.
