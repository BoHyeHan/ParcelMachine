import time
import RPi.GPIO as IO
#from ColorDetect import GreenDetect

IO.setwarnings(False)
IO.setmode(IO.BCM)

IO.setup(22,IO.OUT) #down
IO.setup(23,IO.OUT) #up

IO.setup(12,IO.OUT)
IO.setup(13,IO.OUT)
IO.setup(18,IO.OUT)
IO.setup(19,IO.OUT)

pwm12=IO.PWM(12,100)
pwm13=IO.PWM(13,100)
pwm18=IO.PWM(18,100)
pwm19=IO.PWM(19,100)

pwm12.start(0)
pwm13.start(0)
pwm18.start(0)
pwm19.start(0)

def upfork(cnt):
	if cnt==0:
		sec=time.time()
		while True:
			pwm12.ChangeDutyCycle(60)
			IO.output(13,False)
			pwm18.ChangeDutyCycle(60)
			IO.output(19,False)
			end=time.time()
			e=float((end-sec)%60)
			if e >=0.5: # 0.3
				pwm12.ChangeDutyCycle(0)
				pwm13.ChangeDutyCycle(0)
				pwm18.ChangeDutyCycle(0)
				pwm19.ChangeDutyCycle(0)
				break
		time.sleep(1)

		return
	elif cnt==1:
		sec=time.time()
		while True:
			IO.output(22,False)
			IO.output(23,True)
			end=time.time()
			e=float((end-sec)%60)
			if e >=5: # 5 #5.6
				IO.output(22,False)
				IO.output(23,False)
				break
	elif cnt==2:
		sec=time.time()
		while True:
			IO.output(22,False)
			IO.output(23,True)
			end=time.time()
			e=float((end-sec)%60)
			if e >=11.2:   #10.5   
				IO.output(22,False)
				IO.output(23,False)
				break
	
	sec=time.time()
	while True:
		pwm12.ChangeDutyCycle(60)
		IO.output(13,False)
		pwm18.ChangeDutyCycle(60)
		IO.output(19,False)
		end=time.time()
		e=float((end-sec)%60)
		if e >=0.5:
			pwm12.ChangeDutyCycle(0)
			pwm13.ChangeDutyCycle(0)
			pwm18.ChangeDutyCycle(0)
			pwm19.ChangeDutyCycle(0)
			break


def loadfork(cnt):
		


	if cnt==0:

		sec=time.time()
		while True:
			IO.output(22,True)
			IO.output(23,False)
			end=time.time()
			e=float((end-sec)%60)
			if e >=1.8:  #0.6     
				IO.output(22,False)
				IO.output(23,False)
				break
		time.sleep(1)
		#go back	
		sec=time.time()
		while True:
			pwm13.ChangeDutyCycle(80) #60
			IO.output(12,False)
			pwm19.ChangeDutyCycle(80)
			IO.output(18,False)
			end=time.time()
			e=float((end-sec)%60)
			if e >=0.7:  #1.5 #1.3 #1.1 #1.0 #0.9
				pwm12.ChangeDutyCycle(0)
				pwm13.ChangeDutyCycle(0)
				pwm18.ChangeDutyCycle(0)
				pwm19.ChangeDutyCycle(0)
				break
		

	elif cnt ==1:
		
		#down
		sec=time.time()
		while True:
			IO.output(22,True)
			IO.output(23,False)
			end=time.time()
			e=float((end-sec)%60)
			if e >=1.1: #1.4 #1.3 #1.1
				IO.output(22,False)
				IO.output(23,False)
				break
		time.sleep(1)
		#go back	
		sec=time.time()
		while True:
			pwm13.ChangeDutyCycle(80)
			IO.output(12,False)
			pwm19.ChangeDutyCycle(80)
			IO.output(18,False)
			end=time.time()
			e=float((end-sec)%60)
			if e >=0.8:  #1
				pwm12.ChangeDutyCycle(0)
				pwm13.ChangeDutyCycle(0)
				pwm18.ChangeDutyCycle(0)
				pwm19.ChangeDutyCycle(0)
				break
		time.sleep(1)
		#down
		sec=time.time()
		while True:
			IO.output(22,True)
			IO.output(23,False)
			end=time.time()
			e=float((end-sec)%60)
			if e >=5.8: #5.1     
				IO.output(22,False)
				IO.output(23,False)
				break

	elif cnt ==2:
		#down
		sec=time.time()
		while True:
			IO.output(22,True)
			IO.output(23,False)
			end=time.time()
			e=float((end-sec)%60)
			if e >=1.25:  #1.2   
				IO.output(22,False)
				IO.output(23,False)
				break
		time.sleep(1)

		#go back	
		sec=time.time()
		while True:
			pwm13.ChangeDutyCycle(80) #60
			IO.output(12,False)
			pwm19.ChangeDutyCycle(80)
			IO.output(18,False)
			end=time.time()
			e=float((end-sec)%60)
			if e >=0.8 :# 1
				pwm12.ChangeDutyCycle(0)
				pwm13.ChangeDutyCycle(0)
				pwm18.ChangeDutyCycle(0)
				pwm19.ChangeDutyCycle(0)
				break
		time.sleep(1)
		sec=time.time()
		while True:
			IO.output(22,True)
			IO.output(23,False)
			end=time.time()
			e=float((end-sec)%60)
			if e >=10.8:  #9.9 # 10.8 
				IO.output(22,False)
				IO.output(23,False)
				break

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
		if e >=0.8:   #0.8
			pwm12.ChangeDutyCycle(0)
			pwm13.ChangeDutyCycle(0)
			pwm18.ChangeDutyCycle(0)
			pwm19.ChangeDutyCycle(0)
			break
	time.sleep(1)
	
def extractfork():

	#frist detect QRcode 
	
	
	
	#fork up
	sec=time.time()
	while True:
		IO.output(22,False)
		IO.output(23,True)
		end=time.time()
		e=float((end-sec)%60)
		if e >=2.5:     #2
			IO.output(22,False)
			IO.output(23,False)
			break
	time.sleep(2)
	


	#trun 180
	sec=time.time()
	while True:
		pwm12.ChangeDutyCycle(100)
		IO.output(13,False)
		pwm19.ChangeDutyCycle(100)
		IO.output(18,False)
		end=time.time()
		e=float((end-sec)%60)
		print(e)
		if e >=0.9:  #0.9 #1.0	#0.9 #1.1
			
			pwm12.ChangeDutyCycle(0)
			pwm13.ChangeDutyCycle(0)
			pwm18.ChangeDutyCycle(0)
			pwm19.ChangeDutyCycle(0)
			break

def main():
	print("start")
	cnt=0
	upfork(1)
	#extractfork()
	#time.sleep(2)	
	#while True:
		#cnt=GreenDetect()
		#if cnt>=0:
		#	break
	time.sleep(2)
	loadfork(1)
	
	#extractfork()
	print('end')
if __name__ == '__main__':
	main()
