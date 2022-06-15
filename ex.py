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
g=392
a=440
b=493

# 4옥타브 도~시 , 5옥타브 도의 주파수 
Frq1 = [c,d,e]
Frq2 = [a,e ]

speed1 = 0.5 # 음과 음 사이 연주시간 설정 (0.5초)
speed2 = 0.8 # 음과 음 사이 연주시간 설정 (0.8초)

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
# 0 ~ 7 까지 8개의 채널에서 SPI 데이터를 읽어옵니다.
def readadc(adcnum):
  if adcnum > 7 or adcnum < 0:
    return -1
  r = spi.xfer2([1, 8 + adcnum << 4, 0])
  data = ((r[1] & 3) << 8) + r[2]
  return data

speed=0

def speed_start():
    global speed
     # X, Y 축 포지션
    vrx_pos = readadc(vrx_channel)
    vry_pos = readadc(vry_channel)
    # 스위치 입력
    sw_val = readadc(sw_channel)
    if(vrx_pos == 0 and sw_val == 1023): # SPEED UP
        speed = speed+3     
        print(speed) 
        time.sleep(1)   # 1초동안 대기상태

    elif(vrx_pos == 518 and vry_pos == 504 and sw_val == 1023): #MAINTAIN
        print(speed)
        time.sleep(1)   # 1초동안 대기상태

    elif(vrx_pos == 1023 and sw_val == 1023): #SPEED DOWN 
        speed = speed-3
        print(speed)      
        time.sleep(1)   # 1초동안 대기상태

while True:
    speed_start()
    
