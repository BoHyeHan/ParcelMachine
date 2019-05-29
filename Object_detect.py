#__version__  18-08-23
#__version__  18-08-26

import time
import cv2
import numpy as np
from matplotlib import pyplot as plt
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as IO

IO.setwarnings(False)
IO.setmode(IO.BCM)

IO.setup(10, IO.OUT)

#Path is your model's route
MODEL_PATH="./BFP3.model"
PERSON=False

print("[INFO] loading model..")
model=load_model(MODEL_PATH)

#Frame width & Height
w=640
h=480


font = cv2.FONT_HERSHEY_SIMPLEX

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)	
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))									
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
	
    # return the edged	
    return edged

def Person_detect():   #model,font
    cnt=0
    bcnt=0
    check=0
    #Pcount=0
    Ocount=0
    Pcount=0
    Fcount=0
    Bcount=0
    flag=False
    camera = PiCamera()

    camera.resolution = (640, 480)

    camera.framerate = 32

    rawCapture = PiRGBArray(camera, size=(640, 480))

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        img = frame.array
        Frame=img.copy()
	gray = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray,(3,3),0)
	clahe=cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
	blurred=clahe.apply(blur)
		
	#Detecting Edges
	edges = auto_canny(blurred)
        kernel=np.ones((3,3),np.uint8)
        #th=cv2.adaptiveThreshold(edges,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
        MorphC=cv2.morphologyEx(edges,cv2.MORPH_CLOSE,kernel)
        #cntr_frame, contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	#cv2.imshow("MorphC",MorphC)


        cntr_frame, contours, hierarchy = cv2.findContours(MorphC,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 
        for cnt in contours:
	    hull=cv2.convexHull(cnt)
	    area = cv2.contourArea(hull)
	    x,y,w,h=cv2.boundingRect(cnt)
	    aspect_ratio=float(w)/h
            print(area)
	    if area > 15000  and area <20000:#7000 #15000
		#print(area)
                trim_img=Frame[y:y+h,x:x+w]
		image=cv2.resize(trim_img,(28,28))
		image=image.astype("float")/255.0
		image=img_to_array(image)
		image=np.expand_dims(image,axis=0)

		(box,parcel,person)=model.predict(image)[0]

		Label=""
		proba = 0
		
                if max(box,parcel,person) == box:
                    Label="Box"
                    proba=box
                    Bcount+=1

		elif max(box,parcel,person) == parcel:
		    Label="Forklift"
		    proba=parcel
                    Fcount+=1
                else:
                    Label="Person"
                    proba=person
                    Pcount+=1
				
                label="{}:{:.2f}%".format(Label,proba*100)
			    
		if proba<0.80:
		    continue

                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
		img=cv2.putText(img,label,(x,y),font,0.7,(0,255,0),2)
                
        cv2.imshow("Frame", img)
        k=cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        #if k ==ord('q'):
        #    break

         
        if Pcount == 20 or Fcount == 3 or Bcount == 3:
            flag = True
            cv2.destroyAllWindows()
            camera.close()
            print("The program will be fired after 10 second...")
            return Label
        
#Run Main
if __name__ == "__main__" :
    sec=time.time()
    while(True):
        l=Person_detect()
        if(l=="Person"):
            p=IO.PWM(10,600)
            p.start(100)
            p.ChangeDutyCycle(90)
            time.sleep(4)
            p.stop()
            break
    #if(label == "Person")
    '''
    while True:
        end=time.time()
        flag=Person_detect()
        e=(float(end-sec)%60)
        if e>10:
            cv2.destroyAllWindows()
            break
   '''     

