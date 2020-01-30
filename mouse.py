#developed by gautam patil

#importing numpy to handle cv2 operations
import numpy as np
#importing pynput to controller the mouse 
from pynput.mouse import Button,Controller
#importing the computer vision library 
import cv2
#importing imutils to perform image operations
import imutils
import math
import pyautogui as py


#creating a controller object
mouse=Controller()

width,height=py.size()

#filtering red pixels from the video stream using a lower and upper bound
red_UpperBond=np.array([40,255,255])
red_LowerBond=np.array([22,100,100])

x=320;
y=220;
#to person morphological operations opening and closing cernels to filter the unfiltered pixels
curnel_open=np.ones((5,5))
curnel_close=np.ones((15,15))



cap=cv2.VideoCapture(0)
while(True):
    ret,frames=cap.read()
    imutils.resize(frames,x,y)
    hsv_img=cv2.cvtColor(frames,cv2.COLOR_BGR2HSV)

    #creating a mask to filter the red pixels
    mask=cv2.inRange(hsv_img,red_LowerBond,red_UpperBond)
    mask_open=cv2.morphologyEx(mask,cv2.MORPH_OPEN,curnel_open)
    mask_close=cv2.morphologyEx(mask_open,cv2.MORPH_CLOSE,curnel_close)
    mask_final=mask_close
    
    #finding the boundries of the object
    contour= cv2.findContours(mask_final.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    print(len(contour))
    
    if len(contour)==1:
        
        x1,y1,w1,h1=cv2.boundingRect(contour[0])

        x_c=x1+w1/2

        y_c=y1+h1/2

        cv2.rectangle(frames,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)

        cv2.circle(frames,(x,y),10,(0,0,255),-1)

        #mouse_loc=(width-(x_c*width/x),y_c*height/y)
        mouse.position=(x_c,y_c)
        
    
    elif len(contour)==2:
                
         x1,y1,w1,h1=cv2.boundingRect(contour[0])

         x2,y2,w2,h2=cv2.boundingRect(contour[1])
         
         circle1x=x1+w1/2

         circle1y=y1+h1/2
         
         circle2x=x2+w2/2
         
         circle2y=y2+h2/2
         
         cv2.rectangle(frames,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
         cv2.rectangle(frames,(x2,y2),(x2+w2,y2+h2),(255,0,0),2)
         cv2.circle(frames,(circle1x,circle1y),10,(0,0,255),-1)
         cv2.circle(frames,(circle2x,circle2y),10,(0,0,255),-1)
         cv2.line(frames,(circle1x,circle1y),(circle2x,circle2y),(255,255,250),2)
         midpt_x=(circle1x+circle2x)/2
         midpt_y=(circle1y+circle2y)/2
         
         cv2.circle(frames,(midpt_x,midpt_y),5,(0,0,255),-1)
         
         x2_x1=circle1x-circle2x;
         y2_y1=circle1y-circle2y;
         distance=math.sqrt(pow(x2_x1,2) + pow(y2_y1,2))
         print(distance)
         #mouse.position=(midpt_x,midpt_y)
         
         
         if(distance<50):
             
             mouse.position=(midpt_x,midpt_y)
             mouse.click(Button.left,2)
             mouse.release(Button.left)
         else:
             #mouse.position=(midpt_x,midpt_y)
             mouse.release(Button.left)

         
         #cv2.putText(frames,str(2), (x1, h1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),3) 
         #mouse.move(x2,y2)
         #.rectangle(frames,(x1,y1),(x1+w1,y1+h1),(255,0,0),3)
         #cv2.rectangle(frames,(x2,y2),(x2+w2,y2+h2),(255,0,0),3)

    elif len(contour)>2:
         print("too many background objects are red ")
         
    
    #.rectangle(frames,(),(),(255,255,255),2)
    
    cv2.imshow('mouse3',mask_close)
    
    cv2.imshow('final',frames)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
