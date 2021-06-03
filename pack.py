import os
import cv2
from pyzbar import pyzbar
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import time
import datetime
import numpy as np

def decode(image):
    num = 0
    type = 0
    x, y, w, h = 0, 0, 0, 0
    decoded_objects = pyzbar.decode(image)
    for obj in decoded_objects:
        image, x, y, w, h = draw_box(obj, image)
        num = obj.data
        type = obj.type
    return image, num, type, x, y, w, h

def draw_box(decoded, image):
    x = decoded.rect.left
    y = decoded.rect.top
    w = decoded.rect.width
    h = decoded.rect.height
    image = cv2.rectangle(image, (x, y),
                            (x+w, y+h),
                            color=(0, 255, 0),
                            thickness=5)
    return image, x, y, w, h

def cutvdo(mydata):
    os.chdir(vdo)
    data = cv2.VideoCapture('{}bc.mp4'.format(mydata))
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = int(data.get(cv2.CAP_PROP_FPS))

    end = int(frames / fps)
    if end >= 180:
        start = end-180
    else:
        start = 0
    ffmpeg_extract_subclip('{}bc.mp4'.format(mydata), start, end, targetname='{}.mp4'.format(mydata))

def scanQR():
    cap = cv2.VideoCapture(0)
    frame_w = int(cap.get(3))
    frame_h = int(cap.get(4))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    i = 0
    record = 0
    array = []
    while True:
        _, frame = cap.read()
        if frame is None:
            continue
        frame_detect, data, type, x, y, w, h = decode(frame)
        roi = frame_detect[y:y+h, x:x+w]
        if type == 'QRCODE' and record == 0:
            if data not in array and data != 0:
                mydata = data.decode('utf-8')
                if i == 0:
                    num1 = mydata
                    i += 1
                    time.sleep(1)
                elif i == 1:
                    num2 = mydata
                    i += 1
                    time.sleep(1)
                elif i == 2:
                    num3 = mydata
                    i = 0
                    if num1 == num2 == num3:
                        array.append(data)
                        os.chdir(qrcode)
                        word = str(mydata)+".jpg"
                        cv2.imwrite(word, roi)
                        record = 1
        elif record == 1:
            os.chdir(vdo)
            file = str(mydata)+"bc.mp4"
            rec = cv2.VideoWriter(file, cv2.VideoWriter_fourcc(*'MP4V'),21, (frame_w, frame_h))
            record = 2
        elif record == 2:
            roi = frame_detect[-size-10:-10, -size-10:-10]
            roi[np.where(mask)] = 0
            roi += img
            cv2.putText(frame_detect, "ID: {}".format(str(mydata)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame_detect, datetime.datetime.now().strftime("%D %T"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)
            rec.write(frame_detect)
        cv2.imshow("test", frame_detect)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    try:
        return mydata
    except:
        pass

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    qrcode = os.path.join(base_dir,"qrcode")
    vdo = os.path.join(base_dir,"vdo")
    logo = os.path.join(base_dir,"logo")
    try:
        os.mkdir(vdo)
        os.mkdir(qrcode)
        os.mkdir(logo)
    except:
        os.chdir(logo)
        img = cv2.imread('logo.png')
        size = 50
        img = cv2.resize(img, (size, size))
        imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(imggray, 1, 255, cv2.THRESH_BINARY)
        while True:
            check = input("0 for cam, 1 for break: ")
            if check == "0":
                nameid = scanQR()
                try:
                    cutvdo(nameid)
                    os.remove('{}bc.mp4'.format(nameid))
                except:
                    pass
            elif check == "1":
                break