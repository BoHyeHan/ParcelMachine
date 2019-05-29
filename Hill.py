import time  
import RPi.GPIO as IO
from ColorDetect import RedDetect2

IO.setwarnings(False)
IO.setmode(IO.BCM)
	
#set line sensor(head)
IO.setup(2,IO.IN) #left
IO.setup(3,IO.IN) #right

#set line sensor(tail)
IO.setup(17,IO.IN)  #right
IO.setup(27,IO.IN)  #left


#set motor
IO.setup(12,IO.OUT)
IO.setup(13,IO.OUT)
IO.setup(18,IO.OUT)
IO.setup(19,IO.OUT)

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

#terminated = 0
#terminated_flag = 0

def Downhill():
        sec=time.time()
	while True:
		pwm12.ChangeDutyCycle(80)
		IO.output(13,False)
		pwm18.ChangeDutyCycle(80)
		IO.output(19,False)
		end=time.time()
		e=float((end-sec)%60)
		print(e)
		if e >=0.2:  #0.9 #1.0	#0.72
			
			pwm12.ChangeDutyCycle(0)
			pwm13.ChangeDutyCycle(0)
			pwm18.ChangeDutyCycle(0)
			pwm19.ChangeDutyCycle(0)
			break

	time.sleep(1)
		
	#turn 180 
	sec=time.time()
	while True:
		pwm12.ChangeDutyCycle(100)
		IO.output(13,False)
		pwm19.ChangeDutyCycle(100)
		IO.output(18,False)
		end=time.time()
		e=float((end-sec)%60)
		print(e)
		if e >=0.85:  #0.9 #1.0	#0.72 #0.9
			
			pwm12.ChangeDutyCycle(0)
			pwm13.ChangeDutyCycle(0)
			pwm18.ChangeDutyCycle(0)
			pwm19.ChangeDutyCycle(0)
			break

	time.sleep(2)
	#go little
	

	while True:
		if (IO.input(27)==False  and IO.input(17) is None)or (IO.input(27)==False and IO.input(17)==True):
			print('left')
			IO.output(12, False)
			pwm13.ChangeDutyCycle(40) #40 #38  #60 #70 #70 
			pwm18.ChangeDutyCycle(60)  #60 #35 #40 #50 #65
			IO.output(19,False)

		elif(IO.input(27) is None and IO.input(17)==False)or (IO.input(27)==True and IO.input(17)==False):
			print('right')
			pwm12.ChangeDutyCycle(60)
			IO.output(13, False)
			IO.output(18, False)
			pwm19.ChangeDutyCycle(40)

		elif IO.input(17)==True and IO.input(27)==True:
			print('go')
			pwm13.ChangeDutyCycle(100)   #53 #58  #70 75 
			IO.output(12,False) 
			pwm19.ChangeDutyCycle(100)  #53  #58 #70 75
			IO.output(18,False)
	
		elif IO.input(17)==False and IO.input(27)==False:
			print('Detect Down hill')
			IO.output(12,False)
			IO.output(13,False)
			IO.output(18,False)
			IO.output(19,False)
			pwm12.ChangeDutyCycle(0)
			pwm13.ChangeDutyCycle(0)
			pwm18.ChangeDutyCycle(0)
			pwm19.ChangeDutyCycle(0)
			time.sleep(2)
			#turn 180 
			sec=time.time()
			while True:
				pwm12.ChangeDutyCycle(100)
				IO.output(13,False)
				pwm19.ChangeDutyCycle(100)
				IO.output(18,False)
				end=time.time()
				e=float((end-sec)%60)
			
				if e >=0.9:  #0.9 #1.0	 #0.72 #1.5
					pwm12.ChangeDutyCycle(0)
					pwm13.ChangeDutyCycle(0)
					pwm18.ChangeDutyCycle(0)
					pwm19.ChangeDutyCycle(0)
					break
			time.sleep(2)

		
			return

	
	

def r_main(terminated, terminated_flag, uphill_detect):
	cnt=0
	#uphill_detect=RedDetect2()
	if uphill_detect == 1:
		#fork up
		sec=time.time()
		while True:
			IO.output(22,False)
			IO.output(23,True)
			end=time.time()
			e=float((end-sec)%60)
			if e >=1.5:     #2
				IO.output(22,False)
				IO.output(23,False)
				break
		time.sleep(2)
	
	
		
		while True:
			if terminated == 1:
				terminated_flag += 1
				if terminated_flag > 10000:
					break

			if (IO.input(2)==False  and IO.input(3) is None)or (IO.input(2)==False and IO.input(3)==True):
				print('left')
				IO.output(12, False)
				pwm13.ChangeDutyCycle(40) #40 #38  #60 #70 #70 
				pwm18.ChangeDutyCycle(60)  #60 #35 #40 #50 #65
				IO.output(19,False)
	
			elif(IO.input(2) is None and IO.input(3)==False)or (IO.input(2)==True and IO.input(3)==False):
				print('right')
				pwm12.ChangeDutyCycle(60)
				IO.output(13, False)
				IO.output(18, False)
				pwm19.ChangeDutyCycle(40)
	
			elif IO.input(2)==True and IO.input(3)==True:
				print('go')
				pwm12.ChangeDutyCycle(58)   #53 #58  #70 75 
				IO.output(13,False) 
				pwm18.ChangeDutyCycle(58)  #53  #58 #70 75
				IO.output(19,False)
		
			elif IO.input(2)==False and IO.input(3)==False:
				print('Detect Down hill')
				cnt=cnt+1
				if cnt >=20: 
					IO.output(12,False)
					IO.output(13,False)
					IO.output(18,False)
					IO.output(19,False)
					pwm12.ChangeDutyCycle(0)
					pwm13.ChangeDutyCycle(0)
					pwm18.ChangeDutyCycle(0)
					pwm19.ChangeDutyCycle(0)
					time.sleep(2)
					tmp = RedDetect2()
					if tmp == 1:
						Downhill()	
						#cnt=0
						sec=time.time()
						while True:
							IO.output(23,False)
							IO.output(22,True)
							end=time.time()
							e=float((end-sec)%60)
							if e >=1.0:     #2
								IO.output(22,False)
								IO.output(23,False)
								break
						time.sleep(2)	
					
					terminated = 1
					break

	#else:
if __name__ == '__main__':
	terminated = 0
	terminated_flag = 0
	r_main(terminated, terminated_flag)

