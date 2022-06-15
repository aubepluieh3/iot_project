#상하좌우 xysw
#상 0 505 1023
#하 1023 505 1023
#좌 518 0 1023  
#우 518 1023 1023

import spidev
import time
import RPi.GPIO as GPIO 
import picamera
import datetime
import threading


# 불필요한 warning 제거
GPIO.setwarnings(False) 
# GPIO핀의 번호 모드 설정
GPIO.setmode(GPIO.BCM) 
# GPIO 18번 핀을 출력으로 설정 
GPIO.setup(18, GPIO.OUT)

# PWM 인스턴스 p를 만들고  GPIO 18번을 PWM 핀으로 설정, 주파수  = 100Hz
p = GPIO.PWM(18, 100)  
c=262 #도
d=294 #레
e=330 #미
f=349
fs=370
g=392
a=440
b=493
c2=554
d2=587
e2=659

# 4옥타브 도~시 , 5옥타브 도의 주파수 
Frq1 = [c,d,e] #전원 부팅음
Frq2 = [a,e ] #전원 꺼지는 소리
Frq3 = [c,c,g,g,a,a,g]
Frq4 = [f,f,e,e,d,d,c]
Frq5 = [g,g,f,f,e,e,d]

speed= 50 #기본 속도 50으로 설정
speed1 = 0.5 # 음과 음 사이 연주시간 설정 (0.5초)
speed2 = 0.8 # 음과 음 사이 연주시간 설정 (0.8초)
speed3 = 1 # 음과 음 사이 연주시간 설정 (1초)
#led 핀 번호
red_pin = 4
# LED 핀의 OUT설정
GPIO.setup(red_pin, GPIO.OUT,initial=GPIO.LOW)

# MCP3008 채널설정
sw_channel = 0
vrx_channel = 1
vry_channel = 2

# SPI 인스턴스 spi 생성
spi = spidev.SpiDev()

# SPI 통신 시작하기
spi.open(0, 0)

# SPI 통신 속도 설정
spi.max_speed_hz = 100000

#전원 led
power_led = False
#음악
music = False

# 0 ~ 7 까지 8개의 채널에서 SPI 데이터를 읽어옵니다.
def readadc(adcnum):
  if adcnum > 7 or adcnum < 0:
    return -1
  r = spi.xfer2([1, 8 + adcnum << 4, 0])
  data = ((r[1] & 3) << 8) + r[2]
  return data

def blackbox_start():
    while power_led ==True:
        with picamera.PiCamera() as camera:
            camera.resolution = (640,480)
            camera.start_preview()
            now= datetime.datetime.now()
            filename=now.strftime('%Y-%m-%d %H:%M:%S')
            camera.start_recording(output=filename+'.h264')
            camera.wait_recording(60)
            camera.stop_recording()
            camera.stop_preview()

def speed_start():
    while power_led ==True:
        vrx_pos = readadc(vrx_channel)
        vry_pos = readadc(vry_channel)
        sw_val = readadc(sw_channel)
        global speed
        if(vrx_pos == 0 and sw_val == 1023 and speed<100): # SPEED UP , 최대속도 100으로 설정
            speed = speed+3     
            print(speed) 
            time.sleep(1)   # 1초동안 대기상태
        elif(vrx_pos == 518 and vry_pos == 504 and sw_val == 1023): #MAINTAIN
            print(speed)
            time.sleep(1)   # 1초동안 대기상태

        elif(vrx_pos == 1023 and sw_val == 1023 and speed>0): #SPEED DOWN 
            speed = speed-3
            print(speed)      
            time.sleep(1)   # 1초동안 대기상태

def sound():
        p.start(10)  # PWM 시작 , 듀티사이클 10 (충분)
        for fr in Frq3:
            p.ChangeFrequency(fr)    #주파수를 fr로 변경
            time.sleep(speed1)       #speed 초만큼 딜레이 (0.5s) 
        time.sleep(speed2) 

        for fr in Frq4:
            p.ChangeFrequency(fr)    #주파수를 fr로 변경
            time.sleep(speed1)       #speed 초만큼 딜레이 (0.5s)
        time.sleep(speed2)

        for fr in Frq5:
            p.ChangeFrequency(fr)    #주파수를 fr로 변경
            time.sleep(speed1)
        time.sleep(speed2)           #speed 초만큼 딜레이 (0.8s) 

        for fr in Frq5:
            p.ChangeFrequency(fr)    #주파수를 fr로 변경
            time.sleep(speed1)       #speed 초만큼 딜레이         
        time.sleep(speed2)     
             # GPIO 설정 초기화 

        for fr in Frq3:
            p.ChangeFrequency(fr)    #주파수를 fr로 변경
            time.sleep(speed1)       #speed 초만큼 딜레이 (0.5s) 
        time.sleep(speed2) 

        for fr in Frq4:
            p.ChangeFrequency(fr)    #주파수를 fr로 변경
            time.sleep(speed1)       #speed 초만큼 딜레이 (0.5s)
        time.sleep(speed2)
        
def music():
    if(music == False):
        t4 = threading.Thread(target=sound)   # Thread t2 생성
        t4.start()     
        music = True
    else:
        p.stop() 
        music = False

        


def button():
    global power_led
    if(power_led == False): #LED가 안 들어와 있다면
        GPIO.output(red_pin,1) #전원 불 켜기

        p.start(10)  # PWM 시작 , 전원 부팅 소리
        for fr in Frq1:
            p.ChangeFrequency(fr)    #주파수를 fr로 변경
            time.sleep(speed1)       #speed 초만큼 딜레이 (0.5s) 
        time.sleep(speed2) 
        p.stop()      # GPIO 설정 초기화 
        power_led = True
        #블랙박스 작동
        t2 = threading.Thread(target=blackbox_start)   # Thread t1 생성
        #speed 작동
        t3 = threading.Thread(target=speed_start) # Thread t2 생성
        t2.start()
        t3.start()

    else:
        GPIO.output(red_pin,0)
        p.start(10)  # PWM 시작 , 듀티사이클 10 (충분)
        for fr in Frq2:
            p.ChangeFrequency(fr)    #주파수를 fr로 변경
            time.sleep(speed1)       #speed 초만큼 딜레이 (0.5s) 
        time.sleep(speed2) 
        p.stop()      # GPIO 설정 초기화 
        power_led= False
        exit()
                                 



def joystick():
    while True:
        # 스위치 입력
        sw_val = readadc(sw_channel)
        if(sw_val==0): #버튼을 눌렀을 때 (전원 on/off )
            button()

t1 = threading.Thread(target=joystick)   # Thread t1 생성
t1.start()