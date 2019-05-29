#__VERSION__ 18.08.27
#Fixes : Add infrared sensor

import cv2 
import numpy as np 
import time 
import pyzbar.pyzbar as pyzbar 
import RPi.GPIO as IO
from picamera.array import PiRGBArray
from picamera import PiCamera
from fork import loadfork,upfork
from fork import extractfork
from Object_detect import Person_detect,auto_canny
from ColorDetect import GreenDetect,RedDetect2
from Hill import r_main,Downhill

Q1=None
Q2=None
bpoint=False
Str=None


IO.setwarnings(False)
IO.setmode(IO.BCM)

#set line sensor
IO.setup(2,IO.IN) #left
IO.setup(3,IO.IN) #right

IO.setup(10, IO.OUT) # sound sensor

#set motor
IO.setup(12,IO.OUT)
IO.setup(13,IO.OUT)
IO.setup(18,IO.OUT)
IO.setup(19,IO.OUT)

IO.setup(20,IO.IN) # ack
IO.setup(21,IO.OUT) # triger

IO.setup(22,IO.OUT) #down
IO.setup(23,IO.OUT) #up
pwm12=IO.PWM(12,100)
pwm13=IO.PWM(13,100)
pwm18=IO.PWM(18,100)
pwm19=IO.PWM(19,100)

pwm12.start(0)
pwm13.start(0)
pwm18.start(0)
pwm19.start(0)

font = cv2.FONT_HERSHEY_SIMPLEX
dis_tmp = False

def decode(im) : #image decording
	decodedObjects = pyzbar.decode(im)
	for obj in decodedObjects:
		print('Type : ', obj.type)
		print('Data : ', obj.data,'\n')
	return decodedObjects

def Cam(): #QR Code recognition
	camera = PiCamera()
	camera.resolution = (640, 480)
	camera.framerate = 32
	rawCapture = PiRGBArray(camera, size=(640, 480))
	time.sleep(0.1)
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		image = frame.array
		img=image.copy()
		im=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
		decodedObjects=decode(im)
		reg=None

		for decodedObject in decodedObjects: 
			points = decodedObject.polygon
			if len(points) > 4 : 
				hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
				hull = list(map(tuple, np.squeeze(hull)))
			else : 
				hull = points;

			n = len(hull)
			for j in range(0,n):
				cv2.line(image, hull[j], hull[ (j+1) % n], (255,0,0), 3)

			x = decodedObject.rect.left
			y = decodedObject.rect.top
			reg=str(decodedObject.data)
			barCode = str(decodedObject.data)
			cv2.putText(image, barCode, (x, y), font, 1, (0,255,255), 2, cv2.LINE_AA)

		cv2.imshow("Frame", image)
		key = cv2.waitKey(1) & 0xFF
		rawCapture.truncate(0)
                
		if reg != None:
			cv2.destroyAllWindows()
			break
	camera.close()
	return reg

def main():
	dis=0
	switch=0    #default value =0
	Q1=None
	Q2=None
	flag=0   
	detect_flag=True
	count=0  #sw 2 count
	detect=False
	label=None

	while True:
		print("count : ",count)
		print("switch : ",switch)
		if switch == 0:
			IO.output(21,False) #초음파센서
       			IO.output(21,True)
        		time.sleep(0.0001)
        		IO.output(21,False)
        		cnt1=0
        		cnt2=0
        		error_flag=False
			distance = 100
        		while IO.input(20)==False:
        		        pulse_start=time.time()
        		        cnt1+=1
        		        if cnt1 >=100:
        		                error_flag=True
        		                break
	
	        	while IO.input(20)== True and error_flag == False:
	        	        pulse_end=time.time()
	        	        cnt2+=1
	        	        if cnt2>100:
                                    error_flag=True
		
		        if error_flag == False:
		                pulse_duration=pulse_end-pulse_start
		                distance =pulse_duration*17000
		                distance=round(distance,2)
				print "Distance : ",distance,"cm"
				
				if distance >20  and distance < 30: #거리 20 - 30에 객체가 감지되었을 경우
					IO.output(12,False) #정지
					IO.output(13,False)
					IO.output(18,False)
					IO.output(19,False)
					pwm12.ChangeDutyCycle(0)
					pwm13.ChangeDutyCycle(0)
					pwm18.ChangeDutyCycle(0)
					pwm19.ChangeDutyCycle(0)
				
					detect,label=Person_detect() # 객체 인식 실행
					print("BBoo!!")
					print(label)
					dis=0
					if label is "Person": # 사람을 인식하였을 경우
						p=IO.PWM(10,600) #피에조 부저 4초간 울린다
						p.start(100)
						p.ChangeDutyCycle(90)
						time.sleep(4)
						p.stop()
						print("Human is detected!")
					continue
                
		if (IO.input(2)==False  and IO.input(3) is None)or (IO.input(2)==False and IO.input(3)==True): # 좌회전
			print('left')           
			IO.output(12, False)
			pwm13.ChangeDutyCycle(40)
			pwm18.ChangeDutyCycle(60)
			IO.output(19,False)
            	
		elif(IO.input(2) is None and IO.input(3)==False)or (IO.input(2)==True and IO.input(3)==False): # 우회전
			print('right')
			pwm12.ChangeDutyCycle(60)
			IO.output(13, False)
			IO.output(18, False)
			pwm19.ChangeDutyCycle(40)
		
		elif IO.input(2)==True and IO.input(3)==True: #전진
			print('go')
			pwm12.ChangeDutyCycle(58)  #왼쪽바퀴 정방향
			IO.output(13,False) 
			pwm18.ChangeDutyCycle(58)  #오른쪽바퀴 정방향
			IO.output(19,False)

		elif IO.input(2)==False and IO.input(3)==False: # 멈춤
			print('two line')
                        
			IO.output(12,False) #정지
			IO.output(13,False)
			IO.output(18,False)
			IO.output(19,False)
			pwm12.ChangeDutyCycle(0)
			pwm13.ChangeDutyCycle(0)
			pwm18.ChangeDutyCycle(0)
			pwm19.ChangeDutyCycle(0) 
			region=None

			if switch == 0:
				terminated = 0
				terminated_flag = 0
				detect_flag=0
				detect_flag=RedDetect2() #경사면 판별
				if detect_flag >=1:
					r_main(terminated, terminated_flag,detect_flag) #경사면 인식
				else:
					Q1=Cam() # QR Code 인식
					if Q1 =='Exit': #test
						break
					print('go Source!')
					sec=time.time()
					while True: #0.5초간 전진
						pwm12.ChangeDutyCycle(58)
						IO.output(13, False)
						pwm18.ChangeDutyCycle(58)
						IO.output(19, False)
						end=time.time()
						e=float((end-sec)%60)
						if e >=0.5:
						    break
					switch = 3
                       
			elif switch == 1:   #Exit     #little foward and turn left
				detect_flag=True
				print("switch=1, turn left")
				sec=time.time()
				while True: #0.19초간 전진
					pwm12.ChangeDutyCycle(60)
					IO.output(13, False)
					pwm18.ChangeDutyCycle(60)
					IO.output(19, False)
					end=time.time()
					e3=float((end-sec)%60)
					if e3>=0.19: 
						break


				sec3=time.time()
				while True: #좌회전
					IO.output(12, False)
					pwm13.ChangeDutyCycle(40) 
					pwm18.ChangeDutyCycle(60) 
					IO.output(19, False)
					end3=time.time()
					e3=float((end3-sec3)%60)
					if e3>=0.6:
						break
			
				if count == 3:
					switch=0
					count=0
				else:
					switch=2
            
			elif switch ==2:            #find destination
				Q2=Cam()
				if Q2 == 'Exit':  #test
					break
				print(Q2)
				if Q1==Q2: #little foward and turn left
					count=count+1 # increase
					sec2=time.time()
					while True:  #0.5초간 전진
						pwm12.ChangeDutyCycle(60)
						IO.output(13, False)
						pwm18.ChangeDutyCycle(60)
						IO.output(19, False)
						end2=time.time()
						e2=float((end2-sec2)%60)
						if e2>=0.5:
							break
                    			
					sec3=time.time()
					while True: #좌회전
						IO.output(12, False)
						pwm13.ChangeDutyCycle(40) 
						pwm18.ChangeDutyCycle(60)	
						IO.output(19, False)
						end3=time.time()
						e3=float((end3-sec3)%60)
						if e3>=0.7: 
							break
						
					detect_flag=False
					switch=4  #switch 4 destination mechanism 
               
				else:               #if Q1 != Q2 go foward
					count=count+1
					sec=time.time()
					while True: #0.5초간 전진
						pwm12.ChangeDutyCycle(60)
						IO.output(13, False)
						pwm18.ChangeDutyCycle(60)
						IO.output(19, False)
						end=time.time()
						e=float((end-sec)%60)
						if e >=0.5:  #0.8
							break
				if count ==3:
					switch=0
					count=0
            
			elif switch == 3:    #source extract machanism
				print('extrack!!')
				time.sleep(1)
				extractfork() #택배 상자 싣기
				time.sleep(2)
				switch = 1
	
			elif switch==4:       #destination load mechanism
				print('load')
				if flag==0:
					time.sleep(1)
					cnt=GreenDetect() #적재장소에 적재된 택배 상자의 수 파악
					print("clolor cnt :", cnt)
					upfork(cnt)
					flag=1
					time.sleep(1)
				elif flag==1:
					time.sleep(1)
					loadfork(cnt) #포크 내리기
					flag=0
					switch=5
                                        count+=1
			elif switch == 5:   #Exit     #little foward and turn left
				detect_flag=True
				print("switch=5, turn left")
				sec=time.time()
				while True: #0.15초간 전진
					pwm12.ChangeDutyCycle(60)
					IO.output(13, False)
					pwm18.ChangeDutyCycle(60)
					IO.output(19, False)
					end=time.time()
					e3=float((end-sec)%60)
					if e3>=0.15:
						break


				sec3=time.time()
				while True: #좌회전
					IO.output(12, False)
					pwm13.ChangeDutyCycle(40) #20
					pwm18.ChangeDutyCycle(60) #40
					IO.output(19, False)
					end3=time.time()
					e3=float((end3-sec3)%60)
					if e3>=0.6:
						break
			
			#if count is 2, it meets all destination branch. so,reset 	
				if count == 3:
					switch=0
					count=0
				else:
					switch=2
            
			else:
				print('exception')
				break  #test


if __name__ ==  "__main__":
	main()

