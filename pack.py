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
import HandTrackingModule as htm

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
def post_requests(nameid,orderid,url):
    os.chdir(vdo)
    file_name = "{}.mp4".format(orderid)
    name, extension = os.path.splitext(file_name)
    with open(file_name, "rb") as file:
        text = base64.b64encode(file.read()).decode('utf-8')
        data = {"data": text, "Username": nameid, "Order ID": name, "file_type": extension}
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
    frame = cv2.flip(frame, 1)
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

def scanQR(record,font,st,nameid,orderid,login):
    cap = cv2.VideoCapture(1)
    frame_w = int(cap.get(4))
    frame_h = int(cap.get(3))
    orderid = "-"
    st = 0

    detector = htm.handDetector(detectionCon=0.65, maxHands=1)
    color = (0, 0, 255)

    while True:
        check = 0
        _, frame = cap.read()
        if frame is None:
            continue

        frame = cv2.resize(frame, (640, 480))
        frame = cv2.flip(frame, 1)
        vdoframe = frame.copy()
        frame = detector.findHands(frame)
        lmList = detector.findPosition(frame, draw=False)

        # decode qr
        data, type, x, y, w, h = decode(frame)
        roi = frame[y:y + h, x:x + w]
        if record == 0:
            if type == 'QRCODE':
                st = 0
                mydata = data.decode('utf-8')
                # # check that qr code in 3 sec is same
                # if len(array) < 3:
                #     array.append(mydata)
                #     time.sleep(1)
                #     continue
                # # save qr image
                # if len(set(array)) == 1:
                #     os.chdir(qrcode)
                #     word = str(mydata) + ".jpg"
                #     cv2.imwrite(word, roi)
                #     record = 1
                # array = []
                if mydata.isnumeric() == True:
                    if login == False:
                        nameid = "Please Login !!!"
                        continue
                    elif login == True:
                        orderid = mydata
                elif mydata.isnumeric() == False and login == False:
                    if mydata == "":
                        nameid = "username cannot empty"
                        continue
                    nameid = mydata
                    login = True
                    array = []
            if login == False:
                # in 30 sec, if not find any qr code it will break
                if st == 0:
                    st = time.time()
                else:
                    et = time.time()
                    if et-st > 30:
                        break
        if login:
            if record == 0:
                cv2.rectangle(frame, (300, 0), (380, 40), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, "Log out", (310, 25), font, 0.5, (255, 255, 255), 2)
            if orderid != "-" and record != 2:
                cv2.rectangle(frame, (400, 0), (480, 40), (255, 0, 255), cv2.FILLED)
                cv2.putText(frame, "Record", (410, 25), font, 0.5, (255, 255, 255), 2)
            if record == 2:
                cv2.rectangle(frame, (500, 0), (580, 40), (0, 0, 255), 2)
                cv2.putText(frame, "STOP", (520, 25), font, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, f"Order ID : {str(orderid)}", (10, 50), font, 0.5, (0, 0, 255), 2)
            if len(lmList) != 0:
                # print(lmList)
                x1, y1 = lmList[8][1:]
                x2, y2 = lmList[12][1:]
                cv2.circle(frame, (x1, y1), 15, color, cv2.FILLED)
                fingers = detector.fingersUp()
                if fingers[1] and fingers[2]:
                    if y1 < 40:
                        if 300 < x1 < 380 and record != 2 :
                            color = (0, 255, 0)
                            cv2.circle(frame, (x2, y2), 15, color, cv2.FILLED)
                            login = False
                            nameid = "-"
                            orderid = "-"
                        if 400 < x1 < 480 and orderid != "-" and record != 2:
                            color = (0, 255, 0)
                            cv2.circle(frame, (x2, y2), 15, color, cv2.FILLED)
                            record = 1
                        if 500 < x1 < 580 and record == 2:
                            color = (0, 255, 0)
                            cv2.circle(frame, (x2, y2), 15, color, cv2.FILLED)
                            record = 3
                else:
                    color = (0, 0, 255)
        # create video file
        if record == 1:
            os.chdir(vdo)
            file = str(orderid)+"bc.mp4"
            rec = cv2.VideoWriter(file, cv2.VideoWriter_fourcc(*'MP4V'),21, (frame_h, frame_w))
            record = 2

        # video recording
        if record == 2:
            checklogo(vdoframe)
            cv2.putText(vdoframe, "Order ID: {}".format(str(orderid)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255), 2)
            cv2.putText(vdoframe, datetime.datetime.now().strftime("%D %T"), (10, frame.shape[0] - 10),
                        font, 0.4, (0, 0, 255), 2)
            rec.write(vdoframe)

            # check motion to auto video ending. if user leave frame that is the end
            check = checkback(frame,check,frame_h,frame_w)
        cv2.putText(frame, f"Log in as : {str(nameid)}", (10, 20), font, 0.5, (255, 0, 0), 2)
        cv2.imshow("test", frame)
        cv2.imshow("vdo", vdoframe)
        k = cv2.waitKey(1)
        if check != 1 and record == 2:
            record = 0
            break
        if record == 3:
            record = 0
            break
        if k == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    try:
        return record,font,st,nameid,orderid,login
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

    record = 0
    array = []
    font = cv2.FONT_HERSHEY_SIMPLEX
    st = 0
    nameid = "-"
    orderid = "-"
    login = False

    while True:
        # wait input to turn on camera
        if login == False:
            wait_input = input("0 for cam, 1 for break: ")
        if wait_input == "0":
            record,font,st,nameid,orderid,login = scanQR(record,font,st,nameid,orderid,login)
            try:
                    # create new and remove old
                cutvdo(orderid)
                os.remove('{}bc.mp4'.format(orderid))
                    # post to url
                url = "https://globalapi.advice.co.th/api/upfile_json"
                # post_requests(nameid,orderid, url)
            except:
                pass
        elif wait_input == "1":
            break