# iot_project
### smart car display

1. Topic - 자동차 디스플레이의 한부분을 배운 것을 활용하여 구현 해보고 싶어서 이 주제를 선택   
2. Content   
    + 전원을 켜면 시스템 가동됨
    + 현재 날짜와 실시간이 표시됨   
    + 움직임에 따라 속도가 변하고, 변화된 속도가 표시됨   
    + 블랙박스에 1분마다 영상이 저장되고, 저장된 영상을 확인할 수 있음   
    + 음악을 켜고 끌 수 있음      
    
3.Mechanism   

Basic 화면


![image](https://github.com/aubepluieh3/iot_project/blob/main/basic.png)   
현재 날짜와 실시간 표시

REC 표시

블랙박스 확인 버튼

기본 이미지

속도 표시

음악 버튼

---

Power On
  
![image](https://github.com/aubepluieh3/iot_project/blob/main/Power%20ON.png)
Joystick Button을 누르면 Power On

LED가 켜지고 기본 속도인 50이 표시됨

블랙박스가 가동되어 동영상 녹화가 시작됨

---
Speed Down

![image](https://github.com/aubepluieh3/iot_project/blob/main/speed%20down.png)
Joystick을 아래 방향으로 움직이면 속도가 3씩 줄어듦

Joystick을 움직임 없이 놔두면 속도가 유지됨

---
Speed Up

![image](https://github.com/aubepluieh3/iot_project/blob/main/speed%20up.png)
Joystick을 위쪽 방향으로 움직이면 속도가 3씩 늘어남

속도가 75 초과면 빨간색으로 경고함

---
Open File

![image](https://github.com/aubepluieh3/iot_project/blob/main/mp4%20files.png)

Check BlackBox를 누르면 파일을 열 수 있음

Raspberry Pi는 동영상이 .h264로 저장되기 때문에 .MP4로 변환해줌

새로운 파일이 MP4로 저장됨을 확인할 수 있음

약 1분 단위로 파일이 저장됨을 확인할 수 있음

파일 이름은 파일 녹화 시작 시간을 반영함

파일이 .MP4인 경우면 열 수 있게 설정함

---
Play Video

![image](https://github.com/aubepluieh3/iot_project/blob/main/video_.png)

기본 이미지가 있던 자리에 영상이 재생됨

재생, 정지 가능

---
Play Music

![image](https://github.com/aubepluieh3/iot_project/blob/main/music.png)

음악 재생, 정지 가능

다른 기능들과 별개로 작동 가능












