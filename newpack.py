import os
import cv2
from pyzbar import pyzbar
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import time
import datetime
import numpy as np
import requests
import base64
from object_detector import *

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
    img = cv2.imread('logo4.png')
    size = 100
    img = cv2.resize(img, (size, size))
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(imggray, 1, 255, cv2.THRESH_BINARY)
    roilogo = frame[-size - 1:-1, -size - 10:-10]
    roilogo[np.where(mask)] = 0
    roilogo += img

# measure object
def measure_object(img_aruco,aruco_dict,parameters,detector,img):
    corners, _, _ = cv2.aruco.detectMarkers(img_aruco, aruco_dict, parameters=parameters)
    if corners:

        # Draw polygon around the marker
        # int_corners = np.int0(corners)
        # cv2.polylines(img, int_corners, True, (0, 255, 0), 5)

        # Aruco Perimeter
        aruco_perimeter = cv2.arcLength(corners[0], True)

        # Pixel to cm ratio
        pixel_cm_ratio = aruco_perimeter / 20

        contours = detector.detect_objects(img)

        # Draw objects boundaries
        for cnt in contours:
            # Get rect
            rect = cv2.minAreaRect(cnt)
            (x, y), (w, h), angle = rect

            # Get Width and Height of the Objects by applying the Ratio pixel to cm
            object_width = w / pixel_cm_ratio
            object_height = h / pixel_cm_ratio

            # Display rectangle
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
            cv2.polylines(img, [box], True, (255, 0, 0), 2)
            cv2.putText(img, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)),
                        cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
            cv2.putText(img, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)),
                        cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)

def main(record,font,nameid,login,array,img_aruco):
    # Load Aruco detector
    parameters = cv2.aruco.DetectorParameters_create()
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)

    # Load Object Detector
    detector = HomogeneousBgDetector()

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    frame_w = int(cap.get(4))
    frame_h = int(cap.get(3))
    print(frame_w,frame_h)
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

            if mydata.isnumeric() == False:
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
                        # config frame to check stop
                        if len(array) > 30:
                            out = 1

            elif mydata.isnumeric() == True and record == 0:
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

        # config delay stop time
        if out == 1:
            cv2.putText(frame, "STOP", (400, 50), font, 2, (0, 0, 255), 4)
            if st == 0:
                st = time.time()
            else:
                et = time.time()
                if et-st >3:
                    record = 0
                    break

        if login == False:
            nameid = "-"

        # config delay start time
        if login:
            cv2.putText(frame, f"Order ID : {str(orderid)}", (10, 50), font, 0.7, (0, 0, 255), 2)
            if orderid != "-" and record != 2:
                cv2.putText(frame, "RECORDING", (400, 50), font, 1, (0, 0, 255), 2)
                if st == 0:
                    st = time.time()
                else:
                    et = time.time()
                    if et-st > 3:
                        record = 1
            # config time to logout
            elif orderid == "-":
                measure_object(img_aruco,aruco_dict,parameters,detector,frame)
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
            cv2.putText(vdoframe, "Order ID: {}".format(str(orderid)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0, 0, 255), 2)
            cv2.putText(vdoframe, datetime.datetime.now().strftime("%d/%m/%Y %T"), (10, frame.shape[0] - 10),
                        font, 0.4, (0, 0, 255), 1)
            rec.write(vdoframe)
        cv2.putText(frame, f"Log in as : {str(nameid)}", (10, 20), font, 0.7, (255, 0, 0), 2)
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
    img_aruco = cv2.imread("phone_aruco_marker.jpg")

    while True:
        # wait input to turn on camera
        # if login == False:
        #     wait_input = input("0 for cam, 1 for break: ")
        # if wait_input == "0":
            record, font, st, nameid, orderid, login = main(record, font, nameid, login,array,img_aruco)
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