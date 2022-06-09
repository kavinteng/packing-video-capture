import os
import cv2
from pyzbar import pyzbar
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import time
import datetime
import numpy as np
import requests
import urllib.request
from tkinter import *
import urllib.request
from tkinter.ttk import Combobox
from datetime import date
import sqlite3
import jwt
from getmac import getmac
from tkinter import messagebox
import shutil
import tkinter.simpledialog

date_dir = datetime.date.today()
base_dir = os.path.dirname(os.path.abspath(__file__))
sqlite_dir = base_dir + '/video_packing_log.db'

#----- main -----
def backuppost(size,forget_end,date, a, record,nameid,customid,orderid,tel):
    connection = sqlite3.connect(sqlite_dir)
    cursor = connection.cursor()

    TableSql = "CREATE TABLE IF NOT EXISTS backuppost(ID integer PRIMARY KEY AUTOINCREMENT,nameid CHAR(20),customid CHAR(20),orderid CHAR(20),tel CHAR(20),size CHAR(20),date CHAR(20),time CHAR(20),detail CHAR(50))"
    cursor.execute(TableSql)

    if record==2:
        cursor.execute("insert into backuppost(nameid,customid,orderid,tel,size,date,time) values (?,?,?,?,?,?,?)", (nameid,customid,orderid,tel,size,date,a,))
        cursor.execute("select * from backuppost")
        print(cursor.fetchall())
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
    elif forget_end == 'post limit timeout':
        cursor.execute("update backuppost set detail = 'post to store(time limit)' where orderid = ? and time = ?",
                       (orderid, a))
    elif forget_end == 'post forget end':
        cursor.execute("update backuppost set detail = 'post to store(forget end)' where orderid = ? and time = ?",
                       (orderid, a))
    elif record==0 and forget_end == None:
        cursor.execute("delete from backuppost where orderid = ? and time = ?", (orderid,a))
    else:
        cursor.execute("update backuppost set detail = ? where orderid = ? and time = ?", (forget_end,orderid, a))
    connection.commit()
    connection.close()

def main(cap,vdo,logo,camID,positionx,positiony,record, font, nameid, login, array):
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

        # frame = cv2.resize(frame, (640, 360))
        frame = cv2.resize(frame,(1080,650))
        vdoframe = frame.copy()
        vdoframe = cv2.resize(vdoframe, (640, 360))


        # decode qr
        data, type, x, y, w, h = decode(frame)

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
                            tel_old = tel
                            customid_old = customid
                            nameid_old = nameid

            elif mydata.isnumeric() == True and record == 0:
                if mydata == "":
                    nameid = "username cannot empty"
                    continue
                elif len(mydata)==6 and nameid!=mydata:
                    nameid = mydata
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

            if record == 2:
                check_box = box_detect(frame)
                et_limit = time.time()
                if et_limit - st_scan > 180:
                    out = 2
                if check_box == 1:
                    st_no_box = time.time()
                if check_box == 2:
                    et_no_box = time.time()
                # if et_no_box-st_no_box > 60:
                #     out = 3

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
                # messagebox.showerror("Error QRCODE", 'Wrong QRCODE Format')
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

            video_size = (640, 360)
            fourcc = cv2.VideoWriter_fourcc(*'H264')
            rec = cv2.VideoWriter(file, fourcc, 15, video_size)

            # ตัดคลิปเก่าของกรณีลืมจบคลิป
            if forget_end == 1:
                no_box_1min = 0
                check_success = 'fall'
                url = "https://globalapi2.advice.co.th/api/upfile_json"
                cutvdo(order_old, vdo, a_old,no_box_1min)
                forget_end = 'post forget end'
                post_requests(box_size, forget_end, a_old, vdo, record, nameid_old, customid_old, order_old, tel_old, url, check_success)
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
            rec.write(vdoframe)

        cv2.rectangle(frame, (0, 0), (240, 35), (255, 255, 255), cv2.FILLED)
        cv2.putText(frame, f"Log in as : {str(nameid)}", (10, 25), font, 0.7, (0, 0, 0), 2)
        if check_box == 2:
            cv2.putText(frame, 'No box', (500, 25), font, 0.7, (0, 0, 255), 2)

        if login == True:
            cv2.rectangle(frame, (0, 0), (1080, 650), rec_color, 15)
        cv2.imshow("{}".format(camID), frame)

        cv2.moveWindow("{}".format(camID), positionx, positiony)
        k = cv2.waitKey(1)
    try:
        return box_size, a, record, font, st, nameid, customid, order, tel, login
    except:
        pass
#----- main -----

#----- tkinter -----
def repost():
    global root2, i, form_edit
    connection = sqlite3.connect(sqlite_dir)
    cursor = connection.cursor()

    TableSql = "CREATE TABLE IF NOT EXISTS backuppost(ID integer PRIMARY KEY AUTOINCREMENT,nameid CHAR(20),customid CHAR(20),orderid CHAR(20),tel CHAR(20),size CHAR(20),date CHAR(20),time CHAR(20),detail CHAR(50))"
    cursor.execute(TableSql)

    connection.commit()
    connection.close()

    form_edit = ''
    root2 = Tk()
    root2.title('repost')

    e = Label(root2, width=11, text='ID', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
    e.grid(row=0, column=0)
    e = Label(root2, width=11, text='USER ID', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
    e.grid(row=0, column=1)
    e = Label(root2, width=11, text='CUSTOMER ID', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
    e.grid(row=0, column=2)
    e = Label(root2, width=11, text='ORDER ID', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
    e.grid(row=0, column=3)
    e = Label(root2, width=11, text='TEL', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
    e.grid(row=0, column=4)
    e = Label(root2, width=11, text='BOX SIZE', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
    e.grid(row=0, column=5)
    e = Label(root2, width=11, text='DATE', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
    e.grid(row=0, column=6)
    e = Label(root2, width=11, text='TIME', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
    e.grid(row=0, column=7)
    e = Label(root2, width=30, text='Error detail', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
    e.grid(row=0, column=8)

    i = list_realtime()

    edit_box = Button(root2, text="Edit box size", command=editbox)
    edit_box.grid(row=i + 1, column=0, sticky='W', padx=5, pady=2)
    root2.mainloop()

def list_realtime():
    connection = sqlite3.connect(sqlite_dir)
    cursor = connection.cursor()
    cursor.execute("select * from backuppost limit 0,20")
    lists = cursor.fetchall()
    i = 1
    for list in lists:
        for j in range(len(list)):
            if j % 8 == 0 and j != 0:
                e = Label(root2, width=30, text=list[j],
                          borderwidth=2, relief='ridge', anchor="w")
                e.grid(row=i, column=j)
            else:
                e = Label(root2, width=11, text=list[j],
                          borderwidth=2, relief='ridge', anchor="w")
                e.grid(row=i, column=j)

        e = Button(root2, text='Check vdo', bg='#32CD32', fg='white'
                   , command=lambda order=list[3], date=list[6], time=list[7]: check_vdo(order, date, time))
        e.grid(row=i, column=9)
        i = i + 1
    return i

def choices_id_list():
    connection = sqlite3.connect(sqlite_dir)
    cursor = connection.cursor()
    cursor.execute("select * from backuppost limit 0,20")
    lists_nosize = cursor.fetchall()
    choices_id = []
    for list_nosize in lists_nosize:
        if list_nosize[5] == '-':
            choices_id.append(list_nosize[0])

    connection.commit()
    connection.close()
    try:
        return choices_id
    except:
        choices_id = ['']
        return choices_id

def check_vdo(order,date,time):
    if os.path.exists('d'+'://') == True:
        path = 'D:/vdo_packing'
    else:
        path = 'C:/vdo_packing'
    file_name = "{}/{}/{}{}.mp4".format(path,date, order, time)
    cap = cv2.VideoCapture(file_name)

    while True:
        _, frame = cap.read()
        if frame is None:
            break
        cv2.rectangle(frame, (0,0), (640,85), (255,255,255), cv2.FILLED)
        cv2.putText(frame, "Press q to escape", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                (0, 0, 0), 2)
        cv2.putText(frame, "Press p to play/pause", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 0, 0), 2)
        cv2.imshow('check_vdo', frame)
        k = cv2.waitKey(1)

        if k == ord('q'):
            break
        elif k == ord('p'):
            cv2.waitKey(0)

    cap.release()
    cv2.destroyWindow("check_vdo")

def editbox():
    global entry1,entry2,text3,edit
    edit = Tk()
    edit.title('Edit box size')
    edit.geometry('300x50+1100+120')
    text1 = Label(edit,text='ID',borderwidth=2, relief='ridge', anchor="w", bg='yellow')
    text1.grid(row=0, column=0)
    choices_id = choices_id_list()
    entry1 = Combobox(edit, values=choices_id, width=6)
    # entry1 = Entry(edit, width= 11)
    entry1.grid(row=0, column=1)
    text2 = Label(edit, text='Box size', borderwidth=2, relief='ridge', anchor="w", bg='yellow')
    text2.grid(row=0, column=2)
    choices = ['A', 'B', 'C', 'D', 'E']
    variable = StringVar(edit)
    variable.set('A')
    entry2 = Combobox(edit, values=choices,width=6)
    # entry2 = Entry(edit, width=11)
    entry2.grid(row=0, column=3)

    text3 = Label(edit, text=form_edit,fg='red')
    text3.grid(row=1, column=4)

    edit_box = Button(edit, text="submit", command=addsize)
    edit_box.grid(row=1, column=3, sticky='W', padx=5, pady=2)
    edit.mainloop()

def addsize():
    connection = sqlite3.connect(sqlite_dir)
    global form_edit
    cursor = connection.cursor()
    boxsize_array = ['A', 'B', 'C', 'D', 'E']
    ID = entry1.get()
    boxsize = entry2.get()

    detail = '(Added box size)'
    boxsizes = '000'+ boxsize
    ID = str(ID)

    if ID == '':
        form_edit = 'Error'
        # text3.configure(text='All ID is done!!')
    elif len(boxsizes) == 4:
        if boxsize in boxsize_array:
            form_edit = 'ID:{} SIZE:{}'.format(ID, boxsizes)
            cursor.execute("update backuppost set size = ? where ID = ? ", (boxsizes, ID))
            cursor.execute("update backuppost set detail = ? where ID = ? ", (detail, ID))
            # text3.configure(text=form_edit)
        else:
            form_edit = 'Size not match'
    else:
        form_edit = 'Error'
        # text3.configure(text='ID not in database')

    choices_id_list()

    connection.commit()
    connection.close()
    list_realtime()
    edit.destroy()
    editbox()
#----- tkinter -----

#----- necessary -----
def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

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

def draw_box(decoded, image):
    x = decoded.rect.left
    y = decoded.rect.top
    w = decoded.rect.width
    h = decoded.rect.height
    image = cv2.rectangle(image, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=5)
    return image, x, y, w, h

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

def delete_store(date_ref):
    if os.path.exists('d'+'://') == True:
        vdo_dir = 'D:/vdo_packing/'
    else:
        vdo_dir = 'C:/vdo_packing/'
    date_dir = date.today()
    for file in os.listdir(vdo_dir):
        yy,mm,dd = file.split('-')
        old_file = date(int(yy),int(mm),int(dd))
        check_old_file = date_dir-old_file
        if check_old_file.days > date_ref:
            # os.system('rm -rf {}{}'.format(vdo_dir,file))
            shutil.rmtree('{}{}'.format(vdo_dir,file))
            print('delete {}{}'.format(vdo_dir,file))
#----- necessary -----

#----- cut & post -----
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

        if total <= 60:
            end = total
        else:
            end = total-60
        ffmpeg_extract_subclip('{}bc{}.mp4'.format(mydata, a), start, end, targetname='{}{}.mp4'.format(mydata, a))
    else:
        if total >= 60:
            start = total - 60
        else:
            start = 0
        end = total-0.2
        # ffmpeg_extract_subclip('{}bc.mp4'.format(mydata), start, end, targetname='{}.mp4'.format(mydata))
        ffmpeg_extract_subclip('{}bc{}.mp4'.format(mydata,a), start, end, targetname='{}{}.mp4'.format(mydata,a))

def post_requests(size,forget_end,a, vdo,record,nameid,customid, order, tel, url,check_success):
    os.chdir(vdo)
    # file_name = "{}.mp4".format(order)
    file_name = "{}{}.mp4".format(order,a)
    name, extension = os.path.splitext(file_name)
    mac = getmac.get_mac_address()
    encoded = jwt.encode({'mac address': mac}, 'secret', algorithm='HS256')
    try:
        with open(file_name, "rb") as file:
            data = {"data": file}
            text = {"Username": nameid, "Customer ID": customid, "Order ID": order,
                    "Tel": tel, "Box size": size, "file_type": extension, "token": encoded,
                    "check_success": check_success}
            print(text)
            response = requests.post(url, files=data ,data=text)
            print('------posting------')
            if response.ok:
                check_post = 1
                print("Upload completed successfully!")
                backuppost(size,forget_end,date_dir, a, record, nameid, customid, order, tel)
                # os.remove('{}bc{}.mp4'.format(order, a))
                # file.close()
                # os.remove('{}{}.mp4'.format(order, a))

            else:
                response.raise_for_status()
                print("Something went wrong!")
                # backuppost(check_post, date_dir, a, record, nameid, customid, order, tel)
    except Exception as e:
        e = str(e)
        print(e)
        detail1, detail2 = e.split(':', 1)
        # check_post = 2
        backuppost(size,detail1, date_dir, a, record, nameid, customid, order, tel)

def multipost(box_size, a, vdo,record,nameid,customid, order, tel, url,check_success):
    print('------multipost------')
    if box_size == '-':
        forget_end = 'post limit timeout'
    else:
        forget_end = None
    post_requests(box_size, forget_end,a, vdo, record, nameid, customid, order, tel, url,check_success)
    # date_dir = datetime.date.today()
    # if check_post == 2:
    #     backuppost(check_post, date_dir, a, record, nameid, customid, order, tel)
    #     root3 = Tk()
    #     root3.withdraw()
    #     messagebox.showerror("Error Alert", "fail post")
#----- cut & post -----

#----- admin -----
def admin_control():
    Tk().withdraw()
    passw = tkinter.simpledialog.askstring("Password", "Enter password:", show='*')
    if passw == 'Advice#128':
        admin_root = Tk()
        admin_root.geometry('200x100+0+400')
        admin_root.title('ADMIN_Controller')
        num_report = Label(admin_root, text='ADMIN-CONTROLLER', fg='red', font=('Arial', 12))
        num_report.pack(padx=5, pady=5)
        git_c = Button(admin_root, text="git pull", width=20, bg='red', fg='white', command=git_c_botton)
        git_c.pack(padx=5, pady=5)
        restart = Button(admin_root, text="restart", width=20, bg='red', fg='white', command=restart_botton)
        restart.pack(padx=5, pady=5)


        admin_root.mainloop()

def git_c_botton():
    out = os.system('git pull')
    print(out)
    os.execv(sys.executable, ['python'] + sys.argv)

def restart_botton():
    os.execv(sys.executable, ['python'] + sys.argv)