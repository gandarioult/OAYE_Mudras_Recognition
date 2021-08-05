def capture(key, frame, roi_dict):
    import cv2
    import os
    import time

    directory = 'oaye_data/train/'
    s_is_pressed = True
    cv2.imshow("Frame", frame)
    time.sleep(1)
    kp = cv2.waitKey(1)


    while kp == -1 :        ###LOOP    
        kp = cv2.waitKey(1) ##checking for break loop key
        cv2.imwrite(directory+key+'/'+str(len(os.listdir(directory+key)))+'.jpg', roi_dict['Object'])   ##saving frame as img in respective folder

        cap = cv2.VideoCapture(0)
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)

        cv2.rectangle(frame, roi_dict['Coords']['vertices'][0], roi_dict['Coords']['vertices'][1], (255,0,255) ,1)  ##extracting the ROI
        roi_dict['Object'] = frame[roi_dict['Coords']['y1']:roi_dict['Coords']['y2'], roi_dict['Coords']['x1']:roi_dict['Coords']['x2']]
        roi_dict['Object'] = cv2.resize(roi_dict['Object'], (150, 150)) ##ROI is 150px by 150px for model

        cv2.putText(frame, 'Capturing {0} : {1}.  Press any key to stop'.format(key, len(os.listdir(directory+key))), (10, 10), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0))
        cv2.imshow("Frame", frame)

        roi_dict['Object'] = cv2.cvtColor(roi_dict['Object'], cv2.COLOR_BGR2GRAY)
        _, roi_dict['Object'] = cv2.threshold(roi_dict['Object'], 155, 255, cv2.THRESH_BINARY)
        cv2.imshow(f"{key}_{roi_dict}", roi_dict['Object'])

    return None