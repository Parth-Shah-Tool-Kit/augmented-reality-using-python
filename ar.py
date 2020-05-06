#Made by Parth Shah, Tool Kit
# For detailed explaination of this code, visit : https://youtu.be/DviB93RC0_A

import cv2
import numpy as np
import sys

video = cv2.VideoCapture(0)
bgvideo = cv2.VideoCapture('vid.mp4')

sucess, ref_img = video.read()
flag = 0

while True:
    
    sucess, img = video.read()
    if img is not None:
        img = cv2.resize(img , (1500, 850), interpolation= cv2.INTER_AREA)
        ref_img = cv2.resize(ref_img , (1500, 850), interpolation= cv2.INTER_AREA)
        
        img = cv2.flip(img, 1)

        sucess, bg = bgvideo.read()
        bg = cv2.resize(bg , (1500, 850), interpolation= cv2.INTER_AREA)
        
        if flag == 0:
            ref_img = img
        
        diff1 = cv2.subtract(img,ref_img)
        diff2 = cv2.subtract(ref_img,img)
        
        diff = diff1 + diff2

        diff[abs(diff) < 25] = 0

        gray = cv2.cvtColor(diff.astype(np.uint8), cv2.COLOR_BGR2GRAY)
        gray[np.abs(gray) <10] = 0

        fgmask = gray.astype(np.uint8)

        fgmask[fgmask > 0 ] = 255

        fgmask_inv = cv2.bitwise_not(fgmask)

        fgimg = cv2.bitwise_and(img, img, mask= fgmask)
        bgimg = cv2.bitwise_and(bg, bg, mask= fgmask_inv)

        dst = cv2.add(bgimg, fgimg)
        cv2.imshow('Background removal', dst)

        key = cv2.waitKey(5) & 0xFF

        if ord('q') == key:
            break
        elif ord('d') == key:
            flag = 1
            print("background captured")
        elif ord('r') == key:
            flag = 0
            print("ready to capture a new background")

cv2.destroyAllWindows()
video.release()
