import os
import cv2
from pyzbar import pyzbar
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import time
import datetime
import numpy as np
import requests
import imutils

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
    image = cv2.rectangle(image, (x, y),(x+w, y+h),color=(0, 255, 0),thickness=5)
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

def post_requests(mydata,url):
    os.chdir(vdo)
    with open("{}.mp4".format(mydata), "rb") as a_file:
        file_dict = {"file": a_file}
        response = requests.post(url, files=file_dict)

        if response.ok:
            print("Upload completed successfully!")
            # print(response.text)
        else:
            print("Something went wrong!")

def getback():
    cap = cv2.VideoCapture(1)
    while True:
        _, frame = cap.read()
        cv2.imwrite("background.jpg", frame)
        break
    cap.release()
    cv2.destroyAllWindows()

def checkback(gray):
    os.chdir(logo)
    img2 = cv2.imread("background.jpg")
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img2 = cv2.resize(img2, (640, 480))
    frameDelta = cv2.absdiff(img2, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        if cv2.contourArea(c) < 10000:
            continue
        check = 1
    return check

def scanQR():
    cap = cv2.VideoCapture(1)
    frame_w = int(cap.get(3))
    frame_h = int(cap.get(4))
    record = 0
    array = []

    while True:
        check = 0
        _, frame = cap.read()
        if frame is None:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        frame_detect, data, type, x, y, w, h = decode(frame)
        roi = frame_detect[y:y + h, x:x + w]
        if type == 'QRCODE' and record == 0:
            mydata = data.decode('utf-8')
            if len(array) < 3:
                array.append(mydata)
                time.sleep(1)
                continue
            if len(set(array)) == 1:
                os.chdir(qrcode)
                word = str(mydata) + ".jpg"
                cv2.imwrite(word, roi)
                record = 1
            array = []
        if record == 1:
            os.chdir(vdo)
            file = str(mydata)+"bc.mp4"
            rec = cv2.VideoWriter(file, cv2.VideoWriter_fourcc(*'MP4V'),21, (frame_w, frame_h))
            record = 2
        if record == 2:
            check = checkback(gray)
            roi = frame_detect[-size-10:-10, -size-10:-10]
            roi[np.where(mask)] = 0
            roi += img
            cv2.putText(frame_detect, "ID: {}".format(str(mydata)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame_detect, datetime.datetime.now().strftime("%D %T"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)
            rec.write(frame_detect)
            cv2.imshow("Thresh", thresh)
            cv2.imshow("Frame Delta", frameDelta)
        cv2.imshow("test", frame_detect)
        k = cv2.waitKey(1)
        if check != 1 and record == 2:
            break
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
        pass
    os.chdir(logo)
    img = cv2.imread('logo.png')
    size = 50
    img = cv2.resize(img, (size, size))
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(imggray, 1, 255, cv2.THRESH_BINARY)
    getback()
    while True:
        check = input("0 for cam, 1 for break: ")
        if check == "0":
            nameid = scanQR()
            try:
                cutvdo(nameid)
                os.remove('{}bc.mp4'.format(nameid))
                url = "http://httpbin.org/post"
                post_requests(nameid, url)
            except:
                pass
        elif check == "1":
            break