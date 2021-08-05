import cv2
import numpy as np
import os
import time

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


## handedness preset for ROI position
left_handed = False
right_handed = False
center = False

while True:
    one_handed = ord(input('Collecting data from webcam. For one-handed mudras, Right-handed [r] or Left-Handed [l] ?\n'))
    if one_handed == ord('r') or one_handed == ord('l'):
        if one_handed == ord('r'):
            right_handed = True
        else:
            left_handed = True
        break
    else:
        print('incorrect input')

while True:
    two_handed = ord(input('Collecting data from webcam. For two-handed mudras, unchanged[spacebar] or center [c] ?\n'))
    if two_handed == ord(' ') or two_handed == ord('c'):
        if two_handed == ord('c'):
            center = True
        break
    else:
        print('incorrect input')



## Preset for key combinaison for 2hand mudras automation 
k = last_key = -1
s_is_pressed = False


while True:
    
    if not cap.isOpened():
        raise ModuleNotFoundError('Camera not Found. Try manually turning it on')


    _, frame = cap.read()

    #getting frame size
    frameheight = frame.shape[0]
    framewidth = frame.shape[1]
    framecenter = (int(0.5*frameheight), int(0.5*framewidth))
    textplaceholder1 = (10, framecenter[0]+30)

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
    cv2.putText(frame, "PRESS s TO ACTIVATE 2HAND AUTOCAPTURE", (10, 240), cv2.FONT_HERSHEY_PLAIN, 1, (10,150,255), 1)
    
    #------------

            # Coordinates of the ROI
            # x1 = int(0.5*frame.shape[1])
            # y1 = 10
            # x2 = frame.shape[1]-10
            # y2 = int(0.5*frame.shape[1])

    #------------

    ##Coordinates of the ROI given the handedness
    #1handed ROI
    if left_handed == True:
        x1_one = 10
        y1_one = int(frameheight / 6)
        x2_one = int(framewidth / 4)
        y2_one = int(2*frameheight / 3)
        rect_coords1 = ((x1_one-1, y1_one-1), (x2_one+1, y2_one+1))
        cv2.rectangle(frame, rect_coords1[0], rect_coords1[1], (255,0,0) ,1)
        #cv2.rectangle(frame, (10,470), (160,10), (255,0,0))

    elif right_handed == True:
        x1_one = int(3*framewidth / 4)
        y1_one = int(frameheight / 6)
        x2_one = int(framewidth - 10)
        y2_one = int(2*frameheight / 3)
        rect_coords1 = ((x1_one-1, y1_one-1), (x2_one+1, y2_one+1))
        cv2.rectangle(frame, rect_coords1[0], rect_coords1[1], (255,0,0) ,1)
    else:
        raise LookupError('Cant find ROI for 1handed ROI')

    
    #2handed ROI
    if center == True:
        x1_two = int(framewidth / 4)
        y1_two = int(2*frameheight / 4)
        x2_two = int(3*framewidth / 4)
        y2_two = int(frameheight - 10)
        rect_coords2 = ((x1_two-1, y1_two-1), (x2_two+1, y2_two+1))
        cv2.rectangle(frame, rect_coords2[0], rect_coords2[1], (255,0,255) ,1)
        #cv2.rectangle(frame, (10,400), (630,450), (255,255,0))
    else:
        pass
    
        


    # Drawing the ROI
    # The increment/decrement by 1 is to compensate for the bounding box
    
    # Extracting the ROI
    roi1 = frame[y1_one:y2_one,x1_one:x2_one]
    roi2 = frame[y1_two:y2_two,x1_two:x2_two]
    roi1 = cv2.resize(roi1, (150, 150)) 
    roi2 = cv2.resize(roi2, (150, 150)) 
    
    cv2.imshow("Frame", frame)
    
    #_, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
    #kernel = np.ones((1, 1), np.uint8)
    #img = cv2.dilate(mask, kernel, iterations=1)
    #img = cv2.erode(mask, kernel, iterations=1)
    # do the processing after capturing the image!
    roi1 = cv2.cvtColor(roi1, cv2.COLOR_BGR2GRAY)
    _, roi1 = cv2.threshold(roi1, 155, 255, cv2.THRESH_BINARY)
    cv2.imshow("ROI1", roi1)

    roi2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2GRAY)
    _, roi2 = cv2.threshold(roi2, 155, 255, cv2.THRESH_BINARY)
    cv2.imshow("ROI2", roi2)

    #Automation of captures for the 2hands mudras (Anjali&Dhyana).
    #0.25sec intervals between captures and 's' key as primary key to
    #activate and deactivate the automation 
    #  
    
    last_key = k
    k = cv2.waitKey(100)
    
    if k == -1:
        s_is_pressed = False
    

    ##AUTOCAP OF ANJALI
    if k == ord('0') and last_key == ord('s') and center is True: 
        s_is_pressed = True
        cv2.imshow("Frame", frame)
        time.sleep(1)
        kp = cv2.waitKey(1)


        while kp == -1 :        ###LOOP    
            kp = cv2.waitKey(1) ##checking for break loop key
            cv2.imwrite(directory+'Anjali/'+str(count['Anjali'])+'.jpg', roi2)   ##saving frame as img in respective folder
            count['Anjali'] += 1
            time.sleep(0.2)

            _, frame = cap.read()
            frame = cv2.flip(frame, 1)

            cv2.rectangle(frame, rect_coords2[0], rect_coords2[1], (255,0,255) ,1)  ##extracting the ROI
            roi2 = frame[y1_two:y2_two,x1_two:x2_two]
            roi2 = cv2.resize(roi2, (150, 150)) ##ROI is 150px by 150px for model

            cv2.putText(frame, 'Capturing Anjali : {}.  Press any key to stop'.format(count['Anjali']), (10, 10), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0))
            cv2.imshow("Frame", frame)

            roi2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2GRAY)
            _, roi2 = cv2.threshold(roi2, 155, 255, cv2.THRESH_BINARY)
            cv2.imshow("ROI2", roi2)


    ##AUTOCAP OF DHYANA
    elif k == ord('1') and last_key == ord('s') and center is True: 
        s_is_pressed = True
        cv2.imshow("Frame", frame)
        time.sleep(1)
        kp = cv2.waitKey(1)


        while kp == -1 :        ###LOOP    
            kp = cv2.waitKey(1) ##checking for break loop key
            cv2.imwrite(directory+'Dhyana/'+str(count['Dhyana'])+'.jpg', roi2)   ##saving frame as img in respective folder
            count['Dhyana'] += 1
            time.sleep(0.2)

            _, frame = cap.read()
            frame = cv2.flip(frame, 1)

            cv2.rectangle(frame, rect_coords2[0], rect_coords2[1], (255,0,255) ,1)  ##extracting the ROI
            roi2 = frame[y1_two:y2_two,x1_two:x2_two]
            roi2 = cv2.resize(roi2, (150, 150)) ##ROI is 150px by 150px for model

            cv2.putText(frame, 'Capturing Dhyana : {}.  Press any key to stop'.format(count['Dhyana']), (10, 10), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0))
            cv2.imshow("Frame", frame)

            roi2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2GRAY)
            _, roi2 = cv2.threshold(roi2, 155, 255, cv2.THRESH_BINARY)
            cv2.imshow("ROI2", roi2)


    elif k & 0xFF == ord('2'):
        cv2.imwrite(directory+'Gyan/'+str(count['Gyan'])+'.jpg', roi1)
    elif k & 0xFF == ord('3'):
        cv2.imwrite(directory+'Mushti/'+str(count['Mushti'])+'.jpg', roi1)
    elif k & 0xFF == ord('4'):
        cv2.imwrite(directory+'Vayu/'+str(count['Vayu'])+'.jpg', roi1)
    elif k & 0xFF == ord('5'):
        cv2.imwrite(directory+'Misc/'+str(count['Misc'])+'.jpg', roi1)
    else:
        cv2.putText(frame, "no key combination pressed", (25, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
        cv2.imshow("Frame", frame)
        time.sleep(0.05)
    
    #cv2.imshow("Frame", frame)

    if k == 27:
        break

    
cap.release()
cv2.destroyAllWindows()


# Spliting between train and test folder following a set ratio (70/30 here)

choice = input('If first time capturing data on storage, do you want me to split between train and test? yes[y]\tno[n]')
if choice == 'y':
    import shutil

    source = 'oaye_data/train/'
    destination = 'oaye_data/test/'
    test_split = 0.3    ##here set test split

    # if any(os.scandir(destination))
    for folder in os.listdir(source):
        for file, idx in zip(os.listdir(source+folder), range(0,int(test_split*count[folder]))):
            shutil.move(source+folder+'/'+file, destination+folder+'/')






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
