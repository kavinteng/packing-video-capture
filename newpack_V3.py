import os
import cv2
from pyzbar import pyzbar
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import time
import datetime
import numpy as np
import requests
# from object_detector import *
# from tk2_V3 import confirm
import urllib.request
from getmac import getmac
import jwt
import mariadb
import sys
from tkinter import messagebox
from tkinter import *
import urllib.request
import shutil

date_dir = datetime.date.today()
def backuppost(size,forget_end,date, a, record,nameid,customid,orderid,tel):
    try:
        connection = mariadb.connect(host="localhost", user="root", passwd="123456", database="advicev3")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    cursor = connection.cursor()
    try:
        TableSql = """CREATE TABLE backuppost(ID INT(20) PRIMARY KEY AUTO_INCREMENT,nameid CHAR(20),customid CHAR(20),orderid CHAR(20),tel CHAR(20),size CHAR(20),date CHAR(20),time CHAR(20),detail CHAR(50))"""
        cursor.execute(TableSql)
    except:
        pass

    if record==2:
        cursor.execute("insert into backuppost(nameid,customid,orderid,tel,size,date,time) values (?,?,?,?,?,?,?)", (nameid,customid,orderid,tel,size,date,a,))
        if forget_end == 1:
            cursor.execute("update backuppost set detail = 'forget end' where orderid = ? and time = ?", (orderid,a))
        elif forget_end == 0:
            cursor.execute("update backuppost set detail = 'processing' where orderid = ? and time = ?", (orderid, a))
        elif forget_end == 'limit timeout':
            cursor.execute("update backuppost set detail = 'Limit Timeout 5 min' where orderid = ? and time = ?", (orderid, a))
        elif forget_end == 'no box':
            cursor.execute("update backuppost set detail = 'No box 1 min' where orderid = ? and time = ?", (orderid, a))
    elif forget_end == 'no internet':
        cursor.execute("update backuppost set detail = 'No internet connection' where orderid = ? and time = ?",
                       (orderid, a))
    elif record==0 and forget_end == None:
        cursor.execute("delete from backuppost where orderid = ? and time = ?", (orderid,a))
    else:
        cursor.execute("update backuppost set detail = ? where orderid = ? and time = ?", (forget_end,orderid, a))
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
def cutvdo(mydata,vdo,a,no_box_1min):
    os.chdir(vdo)
    # data = cv2.VideoCapture('{}bc.mp4'.format(mydata))
    data = cv2.VideoCapture('{}bc{}.mp4'.format(mydata,a))
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = int(data.get(cv2.CAP_PROP_FPS))
    total = int(frames / fps)
    if no_box_1min == 1:
        if total >= 120:
            start = total - 120
        else:
            start = 0
        end = total-60
        ffmpeg_extract_subclip('{}bc{}.mp4'.format(mydata, a), start, end, targetname='{}{}.mp4'.format(mydata, a))
    else:
        if total >= 60:
            start = total - 60
        else:
            start = 0
        end = total-1
        # ffmpeg_extract_subclip('{}bc.mp4'.format(mydata), start, end, targetname='{}.mp4'.format(mydata))
        ffmpeg_extract_subclip('{}bc{}.mp4'.format(mydata,a), start, end, targetname='{}{}.mp4'.format(mydata,a))

# post by requests to url
def post_requests(size,forget_end,a, vdo,record,nameid,customid, order, tel, url):
    os.chdir(vdo)
    # file_name = "{}.mp4".format(order)
    file_name = "{}{}.mp4".format(order,a)
    name, extension = os.path.splitext(file_name)
    mac = getmac.get_mac_address()
    encoded = jwt.encode({'mac address': mac}, 'secret', algorithm='HS256')
    try:
        with open(file_name, "rb") as file:
            data = {"data": file}
            text = {"Username": nameid, "Customer ID": customid, "Order ID": order, "Tel": tel, "Box size": size, "file_type": extension, "token": encoded}
            response = requests.post(url, files=data ,data=text)
            print('------posting------')
            if response.ok:
                check_post = 1
                print("Upload completed successfully!")
                backuppost(size,forget_end,date_dir, a, record, nameid, customid, order, tel)

            else:
                response.raise_for_status()
                # print("Something went wrong!")
                # backuppost(check_post, date_dir, a, record, nameid, customid, order, tel)
    except Exception as e:
        e = str(e)
        detail1, detail2 = e.split(':', 1)
        # check_post = 2
        backuppost(size,detail1, date_dir, a, record, nameid, customid, order, tel)

    # return check_post

# load logo image
def checklogo(frame,logo,order,customid):
    os.chdir(logo)
    font = cv2.FONT_HERSHEY_SIMPLEX
    img = cv2.imread('Banner03.jpg')
    img = cv2.resize(img, (640, 85))
    img_height, img_width, _ = img.shape
    x, y = 0, 0
    frame[y:y + img_height, x:x + img_width] = img
    cv2.putText(frame, 'order No: {}'.format(str(order)), (20, 45), font, 0.4, (0, 0, 0), 1)
    cv2.putText(frame, 'Customer No: {}'.format(customid), (20, 65), font, 0.4, (0, 0, 0), 1)
    cv2.putText(frame, 'Record Time: {}'.format(datetime.datetime.now().strftime("%d/%m/%Y")), (210, 45), font, 0.4, (0, 0, 0), 1)
    cv2.putText(frame, '{}'.format(datetime.datetime.now().strftime("%T")), (310, 65), font, 0.4,(0, 0, 0), 1)

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


def box_detect(img):
    img = img[50:360,0:640]
    lower1 = np.array([105, 127, 152])
    upper1 = np.array([121, 151, 166])
    mask1 = cv2.inRange(img, lower1, upper1)
    # gray_thresh = cv2.adaptiveThreshold(mask1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                                     cv2.THRESH_BINARY_INV, 11, 1)
    kernel = np.ones((1, 1), np.uint8)
    closing = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, kernel, iterations=2)
    contours, hierachy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        thresh = 0
        if area > thresh:
            # ellipse = cv2.fitEllipse(cnt)
            # cv2.ellipse(img,ellipse,(0,255,0),2)
            return 1
    return 2

def main(cap,order_dummy, ip,port,vdo,logo,camID,positionx,positiony,record, font, nameid, login, array):
    # Load Aruco detector
    # parameters = cv2.aruco.DetectorParameters_create()
    # aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)

    # Load Object Detector
    # detector = HomogeneousBgDetector()

    # cap = cv2.VideoCapture(camID)
    # cap.set(3, 640)
    # cap.set(4, 480)
    # frame_w = int(cap.get(4))
    # frame_h = int(cap.get(3))
    # print(frame_w,frame_h)

    QR_dict = {
        "bcDwYT": "000A",
        "bcWPu4": "000B",
        "bcWPuJ": "000C",
        "bcWPuU": "000D",
        "000E": "000E"
    }

    orderid = "-"
    st = 0
    array2 = []
    out = 0
    in_st = 0
    forget_end = 0
    st_scan_in = time.time()
    qrsize = 0
    check_box = 0
    et_no_box,st_no_box = 0,0

    while True:
        _, frame = cap.read()
        if frame is None:
            continue

        # frame = cv2.resize(frame, (320, 240))

        # สำหรับ 3 กล้อง (1600*900)
        # frame = cv2.resize(frame, (530, 380))

        frame = cv2.resize(frame, (640, 360))
        vdoframe = frame.copy()
        vdoframe = cv2.resize(vdoframe, (640, 360))


        # decode qr
        data, type, x, y, w, h = decode(frame)
        # check_box = box_detect(frame)

        if type == 'QRCODE' and out != 1 and in_st != 1:
            st = 0
            mydata = data.decode('utf-8')
            check_c,check_o,check_t = 'C','O','T'
            if (check_c in mydata) and (check_o in mydata) and (check_t in mydata) and len(mydata) == 29:
                check_order = True
            else:
                check_order = False

            if mydata.isnumeric() == False:
                if login == False:
                    nameid = "Please Login !!!"
                    continue
                elif login == True and record != 2 and check_order == True:
                    et_scan_in = time.time()
                    if et_scan_in - st_scan_in > 1:
                        # if len(mydata) == 4:
                        #     qrsize = 1
                        #     box_size = mydata
                        #     in_st = 1
                        # else:
                        orderid = mydata
                elif record == 2 :
                    et_scan = time.time()
                    if et_scan - st_scan > 5:
                        no_scan = 0

                    if no_scan == 0:
                        if mydata == '000E':
                            getdict = ['0','0','0','000E']
                        else:
                            getdict = mydata.split('/')

                        if len(getdict) == 4:
                            box_size = QR_dict["{}".format(getdict[3])]
                            array.append(box_size)
                            if out == 0:
                                cv2.putText(frame, f"check:{str(len(array))}", (100, 70), font, 0.5, (0, 255, 0), 2)
                            # config frame to check stop
                            if len(array) > 1:
                                out = 1
                        # เพิ่มอัดวิดิโอต่อ แล้วจบของเก่า ตอนที่ลืมสแกนจบคลิป
                        elif len(mydata) == 29 and mydata != orderid:
                            forget_end = 1
                            box_size = '-'
                            backuppost(box_size,forget_end,date_dir, a, record, nameid, customid, order, tel)
                            record = 0
                            order_old = order
                            a_old = a

            elif mydata.isnumeric() == True and record == 0:
                if mydata == "":
                    nameid = "username cannot empty"
                    continue
                elif len(mydata)==6 and nameid!=mydata:
                    nameid = mydata
                    # if ip is not None:
                    #     confirm(ip,port)
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
                if et - st > 0.2:
                    rec.release()
                    backuppost(box_size,forget_end,date_dir, a, record, nameid, customid, order, tel)
                    record = 0
                    # if ip is not None:
                    #     confirm(ip, port)
                    break

        if out == 2:
            cv2.putText(frame, "limit timeout", (10, 90), font, 1, (0, 0, 255), 4)
            forget_end = 'limit timeout'
            box_size = '-'
            backuppost(box_size, forget_end, date_dir, a, record, nameid, customid, order, tel)
            record = 0
            rec.release()
            break

        if out == 3:
            forget_end = 'no box'
            box_size = '--'
            backuppost(box_size, forget_end, date_dir, a, record, nameid, customid, order, tel)
            record = 0
            rec.release()
            break

        if login == False:
            nameid = "-"

        # config delay start time
        if login:
            rec_color = (0,255,0)
            cv2.putText(frame, f"Order ID : {str(orderid)}", (10, 50), font, 0.5, (0, 0, 255), 2)
            if orderid != "-" and record == 0:
                # if qrsize == 0:
                #     cv2.putText(frame, "SCAN BOX SIZE", (10, 120), font, 2, (0, 0, 255), 3)
                # if qrsize == 1:
                cv2.putText(frame, "RECORDING", (10, 70), font, 0.5, (0, 0, 255), 2)
                if st == 0:
                    st = time.time()
                else:
                    et = time.time()
                    rec_color = (0, 255, 255)
                    if et - st > 1:
                        no_scan = 1
                        st_scan = time.time()
                        record = 1
                        # time.sleep(1)
                    # elif et - st <1:
                    #     if ip is not None:
                    #         confirm(ip,port)
            if record == 2:
                check_box = box_detect(frame)
                et_limit = time.time()
                if et_limit - st_scan > 300:
                    out = 2
                if check_box == 1:
                    st_no_box = time.time()
                if check_box == 2:
                    et_no_box = time.time()
                if et_no_box-st_no_box > 60:
                    out = 3

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
                failqr = Tk()
                failqr.withdraw()
                messagebox.showerror("Error QRCODE", 'Wrong QRCODE Format')
                orderid = "-"
                record = 0
                in_st = 0
                continue


            # เพิ่มเวลาทุกคลิป
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

            # ตัดคลิปเก่าของกรณีลืมจบคลิป
            if forget_end == 1:
                cutvdo(order_old, vdo, a_old)
                forget_end = 0

            record = 2

        # video recording
        if record == 2:
            in_st = 0
            if out != 1:
                rec_color = (255, 0, 0)
                cv2.putText(frame, "RECORDING", (10, 70), font, 0.5, (0, 0, 255), 2)
            elif out == 1:
                rec_color = (0, 0, 255)
            checklogo(vdoframe,logo,order,customid)
            # cv2.putText(vdoframe, "Order ID: {}".format(str(order)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
            #             (0, 0, 255), 2)
            # cv2.putText(vdoframe, datetime.datetime.now().strftime("%d/%m/%Y %T"), (10, vdoframe.shape[0] - 10),
            #             font, 0.4, (0, 0, 255), 1)

            # config over 300 mb
            # cv2.putText(vdoframe, "Order ID: {}".format(str(order)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
            #             (0, 0, 255), 1)
            # cv2.putText(vdoframe, datetime.datetime.now().strftime("%d/%m/%Y %T"), (10, vdoframe.shape[0] - 10),
            #             font, 0.4, (255, 0, 0), 1)
            rec.write(vdoframe)

        cv2.rectangle(frame, (0, 0), (240, 35), (255, 255, 255), cv2.FILLED)
        cv2.putText(frame, f"Log in as : {str(nameid)}", (10, 25), font, 0.7, (0, 0, 0), 2)
        if check_box == 2:
            cv2.putText(frame, 'No box', (500, 25), font, 0.7, (0, 0, 255), 2)

        if login == True:
            cv2.rectangle(frame, (0, 0), (640, 360), rec_color, 15)
        # print("{}".format(camID), cv2.getWindowImageRect("{}".format(camID)))
        cv2.imshow("{}".format(camID), frame)
#         cv2.imshow("vdo", vdoframe)

        # cv2.moveWindow("{}".format(camID), positionx, positiony)
#         cv2.moveWindow("vdo", 0, 0)
        k = cv2.waitKey(1)
        if k == ord('q'):
            exit()
    try:
        # return record, font, st, nameid, customid, order, tel, login
        return box_size, a, record, font, st, nameid, customid, order, tel, login
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