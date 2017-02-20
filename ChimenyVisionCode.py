import numpy as np
import cv2
# To see messages from networktables, you must setup logging
import logging
logging.basicConfig(level=logging.DEBUG)
from ChimenyCodePipeline import GripPipeline
pipe = GripPipeline()
from networktables import NetworkTables
NetworkTables.initialize(server='10.35.74.2')
table = NetworkTables.getTable('SmartDashboard')

nt = NetworkTables.getTable('/SmartDashboard/vision')
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    pipe.process(frame)
    #img, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)




    contours = pipe.filter_contours_output
    cv2.drawContours(frame, contours, -1, (255, 255, 0), 3)

    cX = []
    cY = []
    #n = 0
    for c in contours:

        M = cv2.moments(c)
        if M["m00"] == 0:
            cX = 0
            cY = 0
        else:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

        # draw the contour and center of the shape on the image
        cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
        cv2.circle(frame, (cX, cY), 2, (255, 255, 255), -1)
        cv2.putText(frame, str(cY), (cX - 20, cY - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

        print(cX)
        print(cY)
        table.putNumber('cX', cX)
        table.putNumber('cY', cY)

        #n += 1




    # Display the resulting frame
    #cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
