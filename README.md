# ParcelMachine

### :movie_camera:__VIDEO__<br>
[![ParcelMachine](https://i.ytimg.com/vi/cD_2b2yRt_Y/hqdefault.jpg?sqp=-oaymwEZCPYBEIoBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLB4_ggUqt0dGjsf5-QOu2b7tYki0Q)](https://youtu.be/cD_2b2yRt_Y)
<br>
![ParcelMachine1](https://github.com/YunByungKwan/video/blob/master/ParcelMachine/ParcelMachine1.gif)
<br>
![ParcelMachine1](https://github.com/YunByungKwan/video/blob/master/ParcelMachine/ParcelMachine2.gif)
<br>
![ParcelMachine1](https://github.com/YunByungKwan/video/blob/master/ParcelMachine/ParcelMachine3.gif)
<br>
![ParcelMachine1](https://github.com/YunByungKwan/video/blob/master/ParcelMachine/ParcelMachine4.gif)
<br>
![ParcelMachine1](https://github.com/YunByungKwan/video/blob/master/ParcelMachine/ParcelMachine5.gif)
<br>
:pushpin:__소개__<br>
물류 현장에서 지게차는 필수적이다. 하지만 인명사고가 날 경우, 최소 중상 이상의 피해를 입을 정도로 굉장히 심각한 상황이다. 이를 해결하기 위해 스마트 무인 지게차를 설계하였다.<br><br>

:pushpin:__개발배경 및 필요성__<br>
현재 물류 작업 현장에서 지게차에 의한 사고가 가장 높은 비율로 나타나고 있다. 지게차에 의한 충돌 사고 뿐만 아니라 지게차를 운전하는 운전자의 사고비율이 매우 높은 상황이다. 지게차 운전자의 사고 위험성 때문에 수요가 감소하고 있으며, 이로 인해 작업의 효율 또한 감소하고 있다. 이를 해결하지 않는다면 지게차 없이 작업을 진행할 수 없는 물류 현장에서 사상자는 매년 발생할 것이다. 따라서 이를 해결하기위해 스마트 무인 지게차를 설계해 보았다.<br><br>

:pushpin:__특장점__<br>
- 기존 CNN 알고리즘 모델의 Layer 개선과 OpenCV의 Canny Edge Detector 알고리즘의 결합을 통해서 유효한 사진에 대하여 88.83%였던 객체에 대한 인식률이 99.48%로 올라감. 또한 유효하지 않은 객체의 사진을 90% 이상의 유효한 객체로 인식<br> 
- 라인 트레이서 센서로 바닥의 라인을 인식하여, 운전자 없이 지게차 스스로주행이 가능<br>
- OpenCV를 활용한 영상처리를 통해, 적재된 화물의 수를 스스로 파악함<br> 
- 카메라 모듈을 통해 QR코드를 인식하여, 지게차 스스로 화물을 지역별로 분류하는 빠른 판단이 가능<br>
- 평지뿐만 아니라 내리막의 경우, 표지판을 인식하여 180도 회전 후 이동하여 안전사고를 방지<br>
- 모바일 어플리케이션과 라즈베리파이 간에 블루투스 통신을 통해 돌발 상황 발생시 수동으로 조작할 수 있는 컨트롤러를 제작<br><br>

:pushpin:__기능__<br>

- 딥러닝(Deep Learning) 학습을 통해 사람, 사물 등 객체를 인식
- 카메라로 QR코드를 인식하여, 분기점 인식 및 지역별로 화물을 빠르게 분류
- 카메라로 객체의 색을 인식하여, 적재된 화물의 수를 한눈에 파악
- 평지뿐만 아니라 지게차가 가기 힘든 내리막 등에서도 작동이 가능
- 돌발 상황 발생 시, 컨트롤러를 통해 사람이 직접 수동으로 지게차를 제어
<br>
