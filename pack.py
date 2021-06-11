import os
import cv2
from pyzbar import pyzbar
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import time
import datetime
import numpy as np
import requests
import imutils
import base64

# decode QR code
def decode(image):
    num = 0
    type = 0
    x, y, w, h = 0, 0, 0, 0
    decoded_objects = pyzbar.decode(image)
    for obj in decoded_objects:
        image, x, y, w, h = draw_box(obj, image)
        num = obj.data
        type = obj.type
    return num, type, x, y, w, h

# bounding box QR code
def draw_box(decoded, image):
    x = decoded.rect.left
    y = decoded.rect.top
    w = decoded.rect.width
    h = decoded.rect.height
    image = cv2.rectangle(image, (x, y),(x+w, y+h),color=(0, 255, 0),thickness=5)
    return image, x, y, w, h

# edit video
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

# post by requests to url
def post_requests(mydata,url):
    os.chdir(vdo)
    file_name = "{}.mp4".format(mydata)
    name, extension = os.path.splitext(file_name)
    with open(file_name, "rb") as file:
        text = base64.b64encode(file.read()).decode('utf-8')
        data = {"data": text, "file_name": name, "file_type": extension}
        response = requests.post(url, json=data)

        if response.ok:
            print("Upload completed successfully!")
            # print(response.json())
        else:
            print("Something went wrong!")

# save background image
def getback():
    cap = cv2.VideoCapture(1)
    while True:
        _, frame = cap.read()
        cv2.imwrite("image/background.jpg", frame)
        break
    cap.release()
    cv2.destroyAllWindows()

# load logo image
def checklogo(frame):
    os.chdir(logo)
    img = cv2.imread('logo.png')
    size = 50
    img = cv2.resize(img, (size, size))
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(imggray, 1, 255, cv2.THRESH_BINARY)
    roilogo = frame[-size - 10:-10, -size - 10:-10]
    roilogo[np.where(mask)] = 0
    roilogo += img

# check motion to auto video ending
def checkback(frame,check,fh,fw):
    frame = cv2.resize(frame, (fh, fw))
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    img2 = cv2.imread("background.jpg")
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img2 = cv2.resize(img2, (fh, fw))
    frameDelta = cv2.absdiff(img2, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        if cv2.contourArea(c) < 30000:
            # print("break")
            continue
        else:
            print(cv2.contourArea(c))
            check = 1
    cv2.imshow("delta", frameDelta)
    cv2.imshow("thresh", thresh)
    return check

def scanQR():
    cap = cv2.VideoCapture(1)
    frame_w = int(cap.get(4))
    frame_h = int(cap.get(3))
    record = 0
    array = []
    st = 0
    while True:
        check = 0
        _, frame = cap.read()
        if frame is None:
            continue

        # decode qr
        data, type, x, y, w, h = decode(frame)
        roi = frame[y:y + h, x:x + w]
        if record == 0:
            if type == 'QRCODE':
                st = 0
                mydata = data.decode('utf-8')
                # check that qr code in 3 sec is same
                if len(array) < 3:
                    array.append(mydata)
                    time.sleep(1)
                    continue
                # save qr image
                if len(set(array)) == 1:
                    os.chdir(qrcode)
                    word = str(mydata) + ".jpg"
                    cv2.imwrite(word, roi)
                    record = 1
                array = []
            else:
                # in 30 sec, if not find any qr code it will break
                if st == 0:
                    st = time.time()
                else:
                    et = time.time()
                    if et-st > 30:
                        break
        # create video file
        if record == 1:
            os.chdir(vdo)
            file = str(mydata)+"bc.mp4"
            rec = cv2.VideoWriter(file, cv2.VideoWriter_fourcc(*'MP4V'),21, (frame_h, frame_w))
            record = 2

        # video recording
        if record == 2:
            checklogo(frame)
            cv2.putText(frame, "ID: {}".format(str(mydata)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255), 2)
            cv2.putText(frame, datetime.datetime.now().strftime("%D %T"), (10, frame.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)
            rec.write(frame)

            # check motion to auto video ending. if user leave frame that is a video ending
            check = checkback(frame,check,frame_h,frame_w)
        cv2.imshow("test", frame)
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
    # create path dir
    base_dir = os.path.dirname(os.path.abspath(__file__))
    qrcode = os.path.join(base_dir,"qrcode")
    vdo = os.path.join(base_dir,"vdo")
    logo = os.path.join(base_dir,"image")
    try:
        os.mkdir(vdo)
        os.mkdir(qrcode)
        os.mkdir(logo)
    except:
        pass
    # get background image
    getback()
    while True:
        # wait input to turn on camera
        wait_input = input("0 for cam, 1 for break: ")
        if wait_input == "0":
            nameid = scanQR()
            try:
                # create new and remove old
                cutvdo(nameid)
                os.remove('{}bc.mp4'.format(nameid))
                url = "https://globalapi.advice.co.th/api/upfile_json"
                # post_requests(nameid, url)
            except:
                pass
        elif wait_input == "1":
            break