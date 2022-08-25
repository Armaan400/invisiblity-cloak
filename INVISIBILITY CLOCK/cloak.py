from os import access
import cv2
import time
import numpy as np


#to save output in file - output.avi
four_cc=cv2.VideoWriter_fourcc(*'XVID')
output_file=cv2.VideoWriter('output.avi',four_cc,20.0,(640,480))

#Startin webcam
cap=cv2.VideoCapture(0)

#Allowing webacm to strt ny makin the code sleep for 2sec

time.sleep(2)
bg=0

#capturin bg for 60frames

for i in range(60):
    ret,bg=cap.read()
#flippin the bg
bg=np.flip(bg,axis=1)

#readin the cap frame until the cam is open 

while(cap.isOpened()):
    ret,img=cap.read()
    if not ret :
        break
    #filpin the img for consistancy
    img=np.flip(img,axis=1)



    #convertin color from rgb to hsv

    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #generatin mask to detect red color

    lower_red=np.array([0,120,50])
    upper_red=np.array([10,255,255])

    mask1=cv2.inRange(hsv,lower_red,upper_red)

    lower_red=np.array([170,120,70])
    upper_red=np.array([180,255,255])

    mask2=cv2.inRange(hsv,lower_red,upper_red)

    mask1=mask1+mask2

    #open and expand the image where there is mask1

    mask1=cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    mask1=cv2.morphologyEx(mask1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))

    #selectin onlt the part that doesnot have mask1 and savin it in mask2

    mask2=cv2.bitwise_not(mask1)

    #savin only part of img withot red color

    result1=cv2.bitwise_and(img,img,mask=mask2)

    #savin only part of img with red color

    result2=cv2.bitwise_and(bg,bg,mask=mask1)

    #generatin the final output by merging result 1 amd 2

    final_output=cv2.addWeighted(result1,1,result2,1,0)
    output_file.write(final_output)

    #displayin output to user

    cv2.imshow("magic",final_output)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()