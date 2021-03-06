import os
from pyzbar import pyzbar
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import time
import datetime
import numpy as np
import requests
from object_detector import *
from tk2 import confirm
import urllib.request
from getmac import getmac
import jwt
import mariadb
import sys

date_dir = datetime.date.today()
def backuppost(date, a, record,nameid,customid,orderid,tel):
    try:
        connection = mariadb.connect(host="localhost", user="root", passwd="123456", database="advice")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    cursor = connection.cursor()
    try:
        TableSql = """CREATE TABLE backuppost(ID INT(20) PRIMARY KEY AUTO_INCREMENT,nameid CHAR(20),customid CHAR(20),orderid CHAR(20),tel CHAR(20),date CHAR(20),time CHAR(20))"""
        cursor.execute(TableSql)
    except:
        pass

    if record==2:
        cursor.execute("insert into backuppost(nameid,customid,orderid,tel,date,time) values (?,?,?,?,?,?)", (nameid,customid,orderid,tel,date,a,))
    elif record==0:
        cursor.execute("delete from backuppost where orderid = ? and time = ?", (orderid,a))
    connection.commit()
    connection.close()

def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

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
    image = cv2.rectangle(image, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=5)
    return image, x, y, w, h


# edit video
def cutvdo(mydata,vdo,a):
    os.chdir(vdo)
    # data = cv2.VideoCapture('{}bc.mp4'.format(mydata))
    data = cv2.VideoCapture('{}bc{}.mp4'.format(mydata,a))
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = int(data.get(cv2.CAP_PROP_FPS))
    total = int(frames / fps)
    if total >= 60:
        start = total - 60
    else:
        start = 0
    end = total-1
    # ffmpeg_extract_subclip('{}bc.mp4'.format(mydata), start, end, targetname='{}.mp4'.format(mydata))
    ffmpeg_extract_subclip('{}bc{}.mp4'.format(mydata,a), start, end, targetname='{}{}.mp4'.format(mydata,a))

# post by requests to url
def post_requests(a, vdo,record,nameid,customid, order, tel, url):
    os.chdir(vdo)
    # file_name = "{}.mp4".format(order)
    file_name = "{}{}.mp4".format(order,a)
    name, extension = os.path.splitext(file_name)
    mac = getmac.get_mac_address()
    encoded = jwt.encode({'mac address': mac}, 'secret', algorithm='HS256')

    with open(file_name, "rb") as file:
        data = {"data": file}
        text = {"Username": nameid, "Customer ID": customid, "Order ID": order, "Tel": tel, "file_type": extension, "token": encoded}
        response = requests.post(url, files=data ,data=text)
        if response.ok:
            check_post = 1
            print("Upload completed successfully!")
            backuppost(date_dir, a, record, nameid, customid, order, tel)

        else:
            check_post = 0
            response.raise_for_status()
            print("Something went wrong!")
    return check_post

# load logo image
def checklogo(frame,logo):
    os.chdir(logo)
    img = cv2.imread('a++F--20_.png',cv2.IMREAD_UNCHANGED)
    img = cv2.resize(img, (0, 0), None, 0.16, 0.16)
    *_, mask = cv2.split(img)
    maskBGRA = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGRA)
    maskBGR = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    imgRGBA = cv2.bitwise_and(img, maskBGRA)
    imgRGB = cv2.cvtColor(imgRGBA, cv2.COLOR_BGRA2BGR)
    hf, wf, cf = img.shape
    hb, wb, cb = frame.shape

    pos = [wb - wf, hb - hf]
    imgMaskFull = np.zeros((hb, wb, cb), np.uint8)
    imgMaskFull[pos[1]:hf + pos[1], pos[0]:wf + pos[0], :] = imgRGB
    imgMaskFull2 = np.ones((hb, wb, cb), np.uint8) * 255
    maskBGRInv = cv2.bitwise_not(maskBGR)
    imgMaskFull2[pos[1]:hf + pos[1], pos[0]:wf + pos[0], :] = maskBGRInv

    imgback2 = cv2.bitwise_and(frame, imgMaskFull2)
    vdoframe = cv2.bitwise_or(imgback2, imgMaskFull)

    return vdoframe

    # size = 50
    # img = cv2.resize(img, (size+90, size+10))
    # imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # ret, mask = cv2.threshold(imggray, 1, 255, cv2.THRESH_BINARY)
    # roilogo = frame[-size - 11:-1, -size - 100:-10]
    # roilogo = frame[-48:-10, -127:-1]
    # roilogo[np.where(mask)] = 0
    # roilogo += img


# measure object
# def measure_object(img_aruco, aruco_dict, parameters, detector, img):
#     corners, _, _ = cv2.aruco.detectMarkers(img_aruco, aruco_dict, parameters=parameters)
#     if corners:
#
#         # Draw polygon around the marker
#         # int_corners = np.int0(corners)
#         # cv2.polylines(img, int_corners, True, (0, 255, 0), 5)
#
#         # Aruco Perimeter
#         aruco_perimeter = cv2.arcLength(corners[0], True)
#
#         # Pixel to cm ratio
#         pixel_cm_ratio = aruco_perimeter / 20
#
#         contours = detector.detect_objects(img)
#
#         # Draw objects boundaries
#         for cnt in contours:
#             # Get rect
#             rect = cv2.minAreaRect(cnt)
#             (x, y), (w, h), angle = rect
#
#             # Get Width and Height of the Objects by applying the Ratio pixel to cm
#             object_width = w / pixel_cm_ratio
#             object_height = h / pixel_cm_ratio
#
#             # Display rectangle
#             box = cv2.boxPoints(rect)
#             box = np.int0(box)
#
#             cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
#             cv2.polylines(img, [box], True, (255, 0, 0), 2)
#             cv2.putText(img, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)),
#                         cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
#             cv2.putText(img, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)),
#                         cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)


def main(ip,port,vdo,logo,camID,positionx,positiony,record, font, nameid, login, array, img_aruco):
    # Load Aruco detector
    # parameters = cv2.aruco.DetectorParameters_create()
    # aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)

    # Load Object Detector
    detector = HomogeneousBgDetector()

    cap = cv2.VideoCapture(camID)
    # cap.set(3, 640)
    # cap.set(4, 480)
    # frame_w = int(cap.get(4))
    # frame_h = int(cap.get(3))
    # print(frame_w,frame_h)
    orderid = "-"
    st = 0
    array2 = []
    out = 0
    in_st = 0
    forget_end = 0

    while True:
        _, frame = cap.read()
        if frame is None:
            continue

        # frame = cv2.resize(frame, (320, 240))

        # ?????????????????? 3 ??????????????? (1600*900)
        frame = cv2.resize(frame, (530, 380))

        # frame = cv2.resize(frame, (1280, 720))
        vdoframe = frame.copy()
        vdoframe = cv2.resize(vdoframe, (640, 360))

        # decode qr
        data, type, x, y, w, h = decode(frame)

        if type == 'QRCODE' and out != 1 and in_st != 1:
            st = 0
            mydata = data.decode('utf-8')

            if mydata.isnumeric() == False:
                if login == False:
                    nameid = "Please Login !!!"
                    continue
                elif login == True and record != 2:
                    in_st = 1
                    orderid = mydata
                elif record == 2:
                    end = mydata
                    if end == orderid:
                        array.append(end)
                        if out == 0:
                            cv2.putText(frame, f"check:{str(len(array))}", (100, 70), font, 0.5, (0, 255, 0), 2)
                        # config frame to check stop
                        if len(array) > 1:
                            out = 1
                    # ??????????????????????????????????????????????????? ??????????????????????????????????????? ?????????????????????????????????????????????????????????
                    elif end != orderid:
                        forget_end = 1
                        backuppost(date_dir, a, record, nameid, customid, order, tel)
                        record = 0
                        order_old = order
                        a_old = a

            elif mydata.isnumeric() == True and record == 0:
                if mydata == "":
                    nameid = "username cannot empty"
                    continue
                elif len(mydata)==6 and nameid!=mydata:
                    nameid = mydata
                    if ip is not None:
                        confirm(ip,port)
                    login = True
                    continue

        if type == 0 and out == 0:
            array2.append(type)
            if len(array2) > 20:
                array = []
                array2 = []

        # config delay stop time
        if out == 1:
            cv2.putText(frame, "STOP", (10, 90), font, 1, (0, 0, 255), 4)
            if st == 0:
                st = time.time()
            else:
                et = time.time()
                if et - st > 1:
                    rec.release()
                    backuppost(date_dir, a, record, nameid, customid, order, tel)
                    record = 0
                    if ip is not None:
                        confirm(ip, port)
                    break

        if login == False:
            nameid = "-"

        # config delay start time
        if login:
            rec_color = (0,255,0)
            cv2.putText(frame, f"Order ID : {str(orderid)}", (10, 50), font, 0.5, (0, 0, 255), 2)
            if orderid != "-" and record == 0:
                cv2.putText(frame, "RECORDING", (10, 70), font, 0.5, (0, 0, 255), 2)
                if st == 0:
                    st = time.time()
                else:
                    et = time.time()
                    if et - st > 3:
                        record = 1
                        # time.sleep(1)
                    elif et - st <1:
                        if ip is not None:
                            confirm(ip,port)

            # config time to logout
            # elif orderid == "-":
            #     # measure_object(frame, aruco_dict, parameters, detector, frame)
            #     if st == 0:
            #         st = time.time()
            #     else:
            #         et = time.time()
            #         if et - st > 1800:
            #             login = False

        # create video file
        if record == 1:
            os.chdir(vdo)
            try:
                test1, test2 = orderid.split('C')
                customid, test4 = test2.split('O')
                order, tel = test4.split('T')
            except Exception as e:
                print(e)
                orderid = "-"
                record = 0
                continue


            # ????????????????????????????????????????????????
            a = datetime.datetime.now().strftime("%T")
            a = a.replace(':','-')
            a = str(a)

            # backuppost(a, record, nameid, customid, order, tel)
            file = str(order) + "bc{}.mp4".format(a)

            # file = str(order) + "bc.mp4"
            # video_size = (1280, 720)
            video_size = (640, 360)
            fourcc = cv2.VideoWriter_fourcc(*'H264')
            rec = cv2.VideoWriter(file, fourcc, 50, video_size)

            # ?????????????????????????????????????????????????????????????????????????????????
            if forget_end == 1:
                cutvdo(order_old, vdo, a_old)

            record = 2

        # video recording
        if record == 2:
            in_st = 0
            if out != 1:
                rec_color = (255, 0, 0)
                cv2.putText(frame, "RECORDING", (10, 70), font, 0.5, (0, 0, 255), 2)
            elif out == 1:
                rec_color = (0, 0, 255)
            vdoframe = checklogo(vdoframe,logo)
            # cv2.putText(vdoframe, "Order ID: {}".format(str(order)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
            #             (0, 0, 255), 2)
            # cv2.putText(vdoframe, datetime.datetime.now().strftime("%d/%m/%Y %T"), (10, vdoframe.shape[0] - 10),
            #             font, 0.4, (0, 0, 255), 1)

            # config over 300 mb
            cv2.putText(vdoframe, "Order ID: {}".format(str(order)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255), 1)
            cv2.putText(vdoframe, datetime.datetime.now().strftime("%d/%m/%Y %T"), (10, vdoframe.shape[0] - 10),
                        font, 0.4, (255, 255, 0), 1)
            rec.write(vdoframe)
        cv2.putText(frame, f"Log in as : {str(nameid)}", (10, 25), font, 0.7, (255, 0, 0), 2)
        if login == True:
            cv2.rectangle(frame, (0, 0), (530, 380), rec_color, 15)
        cv2.imshow("{}".format(camID), frame)
#         cv2.imshow("vdo", vdoframe)
        cv2.moveWindow("{}".format(camID), positionx, positiony)
#         cv2.moveWindow("vdo", 0, 0)
        k = cv2.waitKey(1)
        if k == ord('q'):
            exit()
    try:
        # return record, font, st, nameid, customid, order, tel, login
        return a, record, font, st, nameid, customid, order, tel, login
    except:
        pass


# if __name__ == '__main__':
    # # create path dir
    # base_dir = os.path.dirname(os.path.abspath(__file__))
    # qrcode = os.path.join(base_dir, "qrcode")
    # vdo = os.path.join(base_dir, "vdo")
    # logo = os.path.join(base_dir, "image")
    # try:
    #     os.mkdir(vdo)
    #     os.mkdir(qrcode)
    #     os.mkdir(logo)
    # except:
    #     pass
    #
    # record = 0
    # array = []
    # font = cv2.FONT_HERSHEY_SIMPLEX
    # st = 0
    # nameid = "-"
    # orderid = "-"
    # login = False
    # img_aruco = cv2.imread("phone_aruco_marker.jpg")
    #
    # while True:
    #     if connect() == False:
    #         print('No Internet connection!')
    #         continue
    #     else:
    #         print('Internet connected')
    #     # wait input to turn on camera
    #     # if login == False:
    #     #     wait_input = input("0 for cam, 1 for break: ")
    #     # if wait_input == "0":
    #
    #     # create new and remove old
    #     try:
    #         record, font, st, nameid, customid, order, tel, login = main(record, font, nameid, login, array, img_aruco)
    #         cutvdo(order)
    #         os.remove('{}bc.mp4'.format(order))
    #         # post to url
    #         url = "https://globalapi.advice.co.th/api/upfile_json"
    #         # post_requests(nameid,customid, order, tel, url)
    #     except Exception as e:
    #         print(e)
    # # elif wait_input == "1":
    # #     break