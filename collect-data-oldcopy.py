import cv2
import numpy as np
import os

# Create the directory structure
if not os.path.exists("oaye_data"):
    os.makedirs("oaye_data")
    os.makedirs("oaye_data/train")
    os.makedirs("oaye_data/test")
    os.makedirs("oaye_data/train/Anjali")
    os.makedirs("oaye_data/train/Dhyana")
    os.makedirs("oaye_data/train/Gyan")
    os.makedirs("oaye_data/train/Mushti")
    os.makedirs("oaye_data/train/Vayu")
    os.makedirs("oaye_data/train/Misc")
    os.makedirs("oaye_data/test/Anjali")
    os.makedirs("oaye_data/test/Dhyana")
    os.makedirs("oaye_data/test/Gyan")
    os.makedirs("oaye_data/test/Mushti")
    os.makedirs("oaye_data/test/Vayu")
    os.makedirs("oaye_data/test/Misc")
    

# Train or test 
mode = 'train'
directory = 'oaye_data/'+mode+'/'

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    # Simulating mirror image
    frame = cv2.flip(frame, 1)
    
    # Getting count of existing images
    count = {'Anjali': len(os.listdir(directory+"Anjali")),
             'Dhyana': len(os.listdir(directory+"Dhyana")),
             'Gyan': len(os.listdir(directory+"Gyan")),
             'Mushti': len(os.listdir(directory+"Mushti")),
             'Vayu': len(os.listdir(directory+"Vayu")),
             'Misc': len(os.listdir(directory+"Misc"))}
    
    # Printing the count in each set to the screen
    cv2.putText(frame, "MODE : "+mode, (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255), 1)
    cv2.putText(frame, "IMAGE COUNT", (10, 100), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255), 1)
    cv2.putText(frame, "ANJALI : "+str(count['Anjali']), (10, 120), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255), 1)
    cv2.putText(frame, "DHYANA : "+str(count['Dhyana']), (10, 140), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255), 1)
    cv2.putText(frame, "GYAN : "+str(count['Gyan']), (10, 160), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255), 1)
    cv2.putText(frame, "MUSHTI : "+str(count['Mushti']), (10, 180), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255), 1)
    cv2.putText(frame, "VAYU : "+str(count['Vayu']), (10, 200), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255), 1)
    cv2.putText(frame, "MISC : "+str(count['Misc']), (10, 220), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255), 1)
    
    # Coordinates of the ROI
    x1 = int(0.5*frame.shape[1])
    y1 = 10
    x2 = frame.shape[1]-10
    y2 = int(0.5*frame.shape[1])
    # Drawing the ROI
    # The increment/decrement by 1 is to compensate for the bounding box
    cv2.rectangle(frame, (x1-1, y1-1), (x2+1, y2+1), (255,0,0) ,1)
    # Extracting the ROI
    roi = frame[y1:y2, x1:x2]
    roi = cv2.resize(roi, (150, 150), interpolation=cv2.INTER_AREA) 
 
    cv2.imshow("Frame", frame)
    
    #_, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
    #kernel = np.ones((1, 1), np.uint8)
    #img = cv2.dilate(mask, kernel, iterations=1)
    #img = cv2.erode(mask, kernel, iterations=1)
    # do the processing after capturing the image!
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, roi = cv2.threshold(roi, 120, 255, cv2.THRESH_BINARY)
    cv2.imshow("ROI", roi)
    
    interrupt = cv2.waitKey(10)
    if interrupt & 0xFF == 27: # esc key
        break
    if interrupt & 0xFF == ord
    if interrupt & 0xFF == ord('0'):
        cv2.imwrite(directory+'Anjali/'+str(count['Anjali'])+'.jpg', roi)
    if interrupt & 0xFF == ord('1'):
        cv2.imwrite(directory+'Dhyana/'+str(count['Dhyana'])+'.jpg', roi)
    if interrupt & 0xFF == ord('2'):
        cv2.imwrite(directory+'Gyan/'+str(count['Gyan'])+'.jpg', roi)
    if interrupt & 0xFF == ord('3'):
        cv2.imwrite(directory+'Mushti/'+str(count['Mushti'])+'.jpg', roi)
    if interrupt & 0xFF == ord('4'):
        cv2.imwrite(directory+'Vayu/'+str(count['Vayu'])+'.jpg', roi)
    if interrupt & 0xFF == ord('5'):
        cv2.imwrite(directory+'Misc/'+str(count['Misc'])+'.jpg', roi)
    
cap.release()
cv2.destroyAllWindows()
"""
d = "old-data/test/0"
newd = "data/test/0"
for walk in os.walk(d):
    for file in walk[2]:
        roi = cv2.imread(d+"/"+file)
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(roi, 120, 255, cv2.THRESH_BINARY)
        cv2.imwrite(newd+"/"+file, mask)     
"""
