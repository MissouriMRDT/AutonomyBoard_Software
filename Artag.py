import numpy as np
import cv2, PIL
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import time

# define an empty custom dictionary with 
aruco_dict = aruco.custom_dictionary(2, 5, 1)
# add empty bytesList array to fill with 3 markers later
aruco_dict.bytesList = np.empty(shape = (2, 4, 4), dtype = np.uint8)

# add new marker(s)
mybits = np.array([[1,1,0,1,1],[1,1,0,1,1],[1,0,1,0,1],[1,1,1,1,1],[1,1,1,1,1,]], dtype = np.uint8)
aruco_dict.bytesList[0] = aruco.Dictionary_getByteListFromBits(mybits)

mybits_1 = np.array([[1,1,0,1,1],[1,1,0,1,1],[1,0,1,0,1],[0,0,1,1,0],[1,1,1,0,1,]], dtype = np.uint8)
aruco_dict.bytesList[1] = aruco.Dictionary_getByteListFromBits(mybits_1)

# open video capture from (first) webcam
# can also be used with video files
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
        #apply some effects to make image easy to process
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        parameters =  aruco.DetectorParameters_create()
        parameters.markerBorderBits = 2
        corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
        frame = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

        # resize frame to show even on smaller screens
        frame = cv2.resize(frame, None, fx = 0.6, fy = 0.6)
        # Display the resulting frame
        cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()