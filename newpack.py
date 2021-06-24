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

# load logo image
def checklogo(frame):
    os.chdir(logo)
    img = cv2.imread('logo2.png')
    size = 100
    img = cv2.resize(img, (size, size))
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(imggray, 1, 255, cv2.THRESH_BINARY)
    roilogo = frame[-size - 10:-10, -size - 10:-10]
    roilogo[np.where(mask)] = 0
    roilogo += img

def scanQR(record,font,nameid,login,array):
    cap = cv2.VideoCapture(0)
    frame_w = int(cap.get(4))
    frame_h = int(cap.get(3))
    orderid = "-"
    st = 0
    array2 = []
    out = 0

    while True:
        _, frame = cap.read()
        if frame is None:
            continue

        frame = cv2.resize(frame, (640, 480))
        vdoframe = frame.copy()

        # decode qr
        data, type, x, y, w, h = decode(frame)

        if type == 'QRCODE':
            st = 0
            mydata = data.decode('utf-8')

            if mydata.isnumeric() == True:
                if login == False:
                    nameid = "Please Login !!!"
                    continue
                elif login == True and record != 2:
                    orderid = mydata
                elif record == 2:
                    end = mydata
                    if end == orderid:
                        array.append(end)
                        if out == 0:
                            cv2.putText(frame, f"check:{str(len(array))}", (500, 100), font, 0.5, (0, 255, 0), 2)
                        if len(array) > 30:
                            out = 1

            elif mydata.isnumeric() == False and record == 0:
                if mydata == "":
                    nameid = "username cannot empty"
                    continue
                nameid = mydata
                login = True

        if type == 0 and out == 0:
            array2.append(type)
            if len(array2) > 20:
                array = []
                array2 = []

        if out == 1:
            cv2.putText(frame, "break", (400, 50), font, 2, (0, 0, 255), 4)
            if st == 0:
                st = time.time()
            else:
                et = time.time()
                if et-st >3:
                    record = 0
                    break

        if login == False:
            nameid = "-"

        if login:
            cv2.putText(frame, f"Order ID : {str(orderid)}", (10, 50), font, 0.5, (0, 0, 255), 2)
            if orderid != "-" and record != 2:
                cv2.putText(frame, "RECORDING", (400, 50), font, 1, (0, 0, 255), 2)
                if st == 0:
                    st = time.time()
                else:
                    et = time.time()
                    if et-st > 3:
                        record = 1
            elif orderid == "-":
                if st == 0:
                    st = time.time()
                else:
                    et = time.time()
                    if et - st > 1800:
                        login = False

        # create video file
        if record == 1:
            os.chdir(vdo)
            file = str(orderid)+"bc.mp4"
            rec = cv2.VideoWriter(file, cv2.VideoWriter_fourcc(*'MP4V'),21, (frame_h, frame_w))
            record = 2

        # video recording
        if record == 2:
            if out != 1:
                cv2.putText(frame, "RECORDING", (400, 50), font, 1, (0, 0, 255), 2)
            checklogo(vdoframe)
            cv2.putText(vdoframe, "Order ID: {}".format(str(orderid)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255), 2)
            cv2.putText(vdoframe, datetime.datetime.now().strftime("%D %T"), (10, frame.shape[0] - 10),
                        font, 0.4, (0, 0, 255), 2)
            rec.write(vdoframe)
        cv2.putText(frame, f"Log in as : {str(nameid)}", (10, 20), font, 0.5, (255, 0, 0), 2)
        cv2.imshow("test", frame)
        cv2.imshow("vdo", vdoframe)
        cv2.moveWindow("test", 640, 0)
        cv2.moveWindow("vdo", 0, 0)
        k = cv2.waitKey(1)
        if k == ord('q'):
            record = 0
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
    qrcode = os.path.join(base_dir, "qrcode")
    vdo = os.path.join(base_dir, "vdo")
    logo = os.path.join(base_dir, "image")
    try:
        os.mkdir(vdo)
        os.mkdir(qrcode)
        os.mkdir(logo)
    except:
        pass

    record = 0
    array = []
    font = cv2.FONT_HERSHEY_SIMPLEX
    st = 0
    nameid = "-"
    orderid = "-"
    login = False

    while True:
        # wait input to turn on camera
        # if login == False:
        #     wait_input = input("0 for cam, 1 for break: ")
        # if wait_input == "0":
            record, font, st, nameid, orderid, login = scanQR(record, font, nameid, login,array)
            try:
                # create new and remove old
                cutvdo(orderid)
                os.remove('{}bc.mp4'.format(orderid))
                # post to url
                url = "https://globalapi.advice.co.th/api/upfile_json"
                # post_requests(nameid,orderid, url)
            except:
                pass
        # elif wait_input == "1":
        #     break