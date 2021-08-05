## Quick function to calculate fps of webcam for following bakground estimator
def cvgetfps(_cap=None, num_frames=120):
    import time
    import cv2

    if _cap is None:
        _cap = cv2.VideoCapture(0)
        print('Computing webcam fps. Please wait.')
    else:
        if not _cap.isOpened():
            raise ModuleNotFoundError('Calculating fps. Camera not found. Try manually turning it on')
        else:
            print('Computing webcam fps. Please wait.')
    
    
    start = time.time()

    for i in range(0, num_frames):
        ret, frame = _cap.read()
        current = time.time()
        esc_key = cv2.waitKey(30) & 0xFF

        if current >= start + 30:
            RuntimeWarning('This is taking too long. Press ESC to abort')
        
        if esc_key == 27:
            break
    
    end = time.time()

    secs = end - start
    fps = num_frames // secs
    fps = int(fps)

    print(f'Webcam FPS : {fps}')

    _cap.release()
    cv2.destroyAllWindows()

    return fps

### -----------------------------

##Compute average background of webcam feed for substraction
def avg_background(fps):
    import cv2
    import numpy as np

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise ModuleNotFoundError('Calculating average background. Camera not found. Try manually turning it on')
    else:
        print('Computing average background. Please stand still and do not move your camera')

    fgbg = cv2.createBackgroundSubtractorMOG2()
    counter = 0

    for counter in range(0, fps*5):
        # capturing 5sec at fps to get an average of background to substract
        # must warn user of the 'preset delay' needed in order to get good average
        ret, frame = cap.read()
        fgmask = fgbg.apply(frame)

        flat_fgmask = np.atleast_2d(fgmask.flatten())

        if counter == 0:
            storage = flat_fgmask.copy()
        else:
            storage = np.append(storage, flat_fgmask, axis = 0)
            
        counter += 1
            

    avg_vec = np.mean(storage, axis=0)   
    avg_arr = avg_vec.reshape(int(cap.get(4)), int(cap.get(3)))
    print(f'shape of frame : {avg_arr.shape}') 

    # cap.release()
    # cv2.destroyAllWindows()

    return avg_arr, cap







#!/usr/bin/env python

import cv2
import os
import numpy as np

if __name__ == '__main__':

    #cap = cv2.VideoCapture(0)
    #fgbg = cv2.createBackgroundSubtractorMOG2()

    # counter = 0
    # avg_arr = np.empty(tuple(map(int,(cap.get(3), cap.get(4))))).T


    fps = cvgetfps()
    avg_bgrnd, cap = avg_background(fps)


    ##Capturing Loop
    while True:
        ret, frame = cap.read()

        if not cap.isOpened():
            raise ModuleNotFoundError('Camera not found. Try manually turning it on')

        cv2.imshow('normal frame', frame)
        cv2.imshow('background sub frame', avg_bgrnd)
        #cv2.imshow('background sub frame', frame-avg_bgrnd)

        k = cv2.waitKey(20) & 0xFF

        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
