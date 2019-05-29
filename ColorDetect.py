import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
font=cv2.FONT_HERSHEY_SIMPLEX
#camera = PiCamera()

#camera.resolution = (640, 480)

#camera.framerate = 32

#rawCapture = PiRGBArray(camera, size=(640, 480))



time.sleep(0.1)


def RedDetect():
	cnt=0
	bcnt=0
	check=0
	camera = PiCamera()

	camera.resolution = (640, 480)

	camera.framerate = 32

	rawCapture = PiRGBArray(camera, size=(640, 480))

	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		image = frame.array
		hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    	#idefine the ramge of red color
		red_lower=np.array([136, 87, 11],np.uint8) # 136 87 11
		red_upper=np.array([180, 255, 255],np.uint8) # 180 255 255
	
		#finding the ramge pf red cp;pr in the image
		red=cv2.inRange(hsv,red_lower,red_upper)
	
		#morphological transformation
	
		kernal=np.ones((5,5),"uint8")
	
		red=cv2.dilate(red,kernal)
		res=cv2.bitwise_and(image,image,mask=red)
	
		#Tracking the Red Color
		(_,contours,hierarchy)=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
		for pic, contour in enumerate(contours):
			area=cv2.contourArea(contour)
			if(area>=2000):
				cnt=cnt+1
				x,y,w,h=cv2.boundingRect(contour)
				image=cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
				cv2.putText(image,"RED color",(x,y),font,0.7,(0,0,255))
		temp=bcnt
		bcnt=cnt
		cnt=temp
		if cnt==bcnt:
 			check=check+1
		else:
			check=0

		cv2.imshow("Frame", image)
		key = cv2.waitKey(1) & 0xFF
		rawCapture.truncate(0)
		if key == ord('q'):
			cv2.destroyAllWindows()
			break	
		#if check==6:
		#	cv2.destroyAllWindows()
		#	break	
	camera.close()
	return cnt

def GreenDetect():
	cnt=0
	bcnt=0
	check=0
	camera = PiCamera()

	camera.resolution = (640, 480)

	camera.framerate = 32

	rawCapture = PiRGBArray(camera, size=(640, 480))
	
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		image = frame.array
		cnt=0
		hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    	#idefine the ramge of red color
		green_lower=np.array([30,80,80],np.uint8)
		green_upper=np.array([90,255,255],np.uint8)
	
		#finding the ramge pf red cp;pr in the image
		green=cv2.inRange(hsv,green_lower,green_upper)
	
		#morphological transformation
	
		kernal=np.ones((5,5),"uint8")
	
		green=cv2.dilate(green,kernal)
		res=cv2.bitwise_and(image,image,mask=green)
	
		#Tracking the Green Color
		(_,contours,hierarchy)=cv2.findContours(green,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
		for pic, contour in enumerate(contours):
			area=cv2.contourArea(contour)
			if(area>=7000):
				cnt=cnt+1
				x,y,w,h=cv2.boundingRect(contour)
				image=cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
				cv2.putText(image,"Green color",(x,y),font,0.7,(0,0,255))
		temp=cnt
		cnt=bcnt
		bcnt=temp
		if cnt==bcnt:
 			check=check+1
		else:
			check=0
	
		cv2.imshow("ColorDetect", image)
		key = cv2.waitKey(1) & 0xFF
		rawCapture.truncate(0)
		if key == ord('q'):
			break
		if check==7:
			cv2.destroyAllWindows()
			break
	camera.close()
	return cnt

def RedDetect2():
	cnt=0
	bcnt=0
	check=0
	camera = PiCamera()

	camera.resolution = (640, 480)

	camera.framerate = 32

	rawCapture = PiRGBArray(camera, size=(640, 480))
	
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		image = frame.array
		cnt=0
		hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    	#idefine the ramge of red color
		red_lower=np.array([136,87,11],np.uint8) #136 87 11
		red_upper=np.array([180,255,255],np.uint8) #180 255 255
	
		#finding the ramge pf red cp;pr in the image
		red=cv2.inRange(hsv,red_lower,red_upper)
	
		#morphological transformation
	
		kernal=np.ones((5,5),"uint8")
	
		red=cv2.dilate(red,kernal)
		res=cv2.bitwise_and(image,image,mask=red)
	
		#Tracking the Red Color
		(_,contours,hierarchy)=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
		for pic, contour in enumerate(contours):
			area=cv2.contourArea(contour)
			if(area>=10000):
				cnt=cnt+1
				x,y,w,h=cv2.boundingRect(contour)
				image=cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
				cv2.putText(image,"Red color",(x,y),font,0.7,(0,0,255))
		temp=cnt
		cnt=bcnt
		bcnt=temp
		if cnt==bcnt:
 			check=check+1
		else:
			check=0
	
		cv2.imshow("ColorDetect", image)
		key = cv2.waitKey(1) & 0xFF
		rawCapture.truncate(0)
		if key == ord('q'):
			break
		if check==7:
			cv2.destroyAllWindows()
			break
	camera.close()
	return cnt

def main():
	print('main')
	while True:
		#cnt=GreenDetect()
		cnt=RedDetect2()
		print("Object Detect : "+str(cnt)+"!!")
		#if cnt == 3:
		break
		'''
		cv2.imshow("Frame", image)
		key = cv2.waitKey(1) & 0xFF
		rawCapture.truncate(0)
		if key == ord('q'):
			break
		'''
if __name__ == '__main__':
	main()
