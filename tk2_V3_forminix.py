import os
import cv2
from tkinter import *
from tkinter.ttk import *
# from multiprocessing import Process
from threading import Thread
from newpack_V3_forminix import *
import urllib.request
import time
from datetime import date
import mariadb
import jwt
from getmac import getmac
from tkinter import messagebox
import webbrowser

def create_database():
    try:
        connection = mariadb.connect(host="localhost", user="root", passwd="123456")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE advicev3")
    except:
        pass

def repost():
    global root2, i, form_edit
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

    # i = 1
    # for list in lists:
    #     for j in range(len(list)):
    #         if j%8 == 0 and j != 0:
    #             e = Label(root2, width=30, text=list[j],
    #                         borderwidth=2, relief='ridge', anchor="w")
    #             e.grid(row=i, column=j)
    #         else:
    #             e = Label(root2, width=11, text=list[j],
    #                         borderwidth=2, relief='ridge', anchor="w")
    #             e.grid(row=i, column=j)
    #
    #     e = Button(root2, text='Check vdo', bg='#32CD32',fg='white'
    #                   , command=lambda order=list[3],date=list[6],time=list[7]: check_vdo(order,date,time))
    #     e.grid(row=i, column=9)
    #     i = i + 1
    i = list_realtime()

    connection.commit()
    connection.close()

    # repost2 = Button(root2, text="POST", command=post)
    # repost2.grid(row=i+1, column=4, sticky='W', padx=5, pady=2)
    edit_box = Button(root2, text="Edit box size", command=editbox)
    edit_box.grid(row=i + 1, column=0, sticky='W', padx=5, pady=2)
    root2.mainloop()

def list_realtime():
    try:
        connection = mariadb.connect(host="localhost", user="root", passwd="123456", database="advicev3")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
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
    try:
        connection = mariadb.connect(host="localhost", user="root", passwd="123456", database="advicev3")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
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
    try:
        connection = mariadb.connect(host="localhost", user="root", passwd="123456", database="advicev3")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
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

def post():
    try:
        connection = mariadb.connect(host="localhost", user="root", passwd="123456", database="advicev3")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    cursor = connection.cursor()
    cursor.execute("select * from backuppost limit 0,20")
    lists = cursor.fetchall()
    url = "https://globalapi2.advice.co.th/api/upfile_json"
    for list in lists:
        _, nameid, customid, order, tel, size, date, a, _ = list
        # file_name = "D:/vdo_packing/{}/{}.mp4".format(date_dir,order)
        if os.path.exists('d' + '://') == True:
            path = 'D:/vdo_packing'
        else:
            path = 'C:/vdo_packing'
        file_name = "{}/{}/{}{}.mp4".format(path,date, order, a)
        name, extension = os.path.splitext(file_name)
        mac = getmac.get_mac_address()
        encoded = jwt.encode({'mac address': mac}, 'secret', algorithm='HS256')

        try:
            if size == '-':
                pass
            else:
                with open(file_name, "rb") as file:
                    data = {"data": file}
                    text = {"Username": nameid, "Customer ID": customid, "Order ID": order, "Tel": tel, "Box size": size,
                            "file_type": extension, "token": encoded}
                    print(nameid, customid, order, tel, size)
                    response = requests.post(url, files=data, data=text)

                    if response.ok:
                        print("Upload completed successfully!")
                        cursor.execute("delete from backuppost where orderid = ? and time = ?", (order,a))
                    else:
                        response.raise_for_status()
                        # print("Something went wrong!")
        except Exception as e:
            e = str(e)
            detail1, detail2 = e.split(':',1)
            # cursor.execute("update backuppost set detail = 'No such file' where orderid = ? and time = ?", (order, a))
            cursor.execute("update backuppost set detail = ? where orderid = ? and time = ?", (detail1, order, a))

    connection.commit()
    connection.close()
    root2.destroy()

def count_unpost():
    global after_id
    try:
        connection = mariadb.connect(host="localhost", user="root", passwd="123456", database="advicev3")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    lists = None
    count = '0'
    cursor = connection.cursor()
    try:
        cursor.execute("select * from backuppost ")
        lists = cursor.fetchall()
    except:
        pass
    connection.commit()
    connection.close()
    if lists is not None:
        count = len(lists)

    num_report.configure(text = 'UNPOST = {}'.format(count))
    after_id  = root.after(1000, count_unpost)

def f(camID,positionx,positiony):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    qrcode = os.path.join(base_dir, "qrcode")
    # vdo = os.path.join(base_dir, "vdo")
    date_dir = date.today()
    if os.path.exists('d'+'://') == True:
        vdo_dir = 'D:/vdo_packing'
    else:
        vdo_dir = 'C:/vdo_packing'
    vdo = '{}/{}'.format(vdo_dir,date_dir)
    logo = os.path.join(base_dir, "image")
    try:
        os.mkdir(vdo_dir)
        os.mkdir(qrcode)
        os.mkdir(logo)
    except:
        pass
    try:
        os.mkdir(vdo)
    except:
        pass
    record = 0
    array = []
    font = cv2.FONT_HERSHEY_SIMPLEX
    st = 0
    nameid = "-"
    order_dummy = 1
    login = False
    cap = cv2.VideoCapture(camID)
    # cap = cv2.VideoCapture('test_box_color.mp4')
    while True:
        try:
            # create new and remove old
            box_size, a, record, font, st, nameid, customid, order, tel, login = main(cap,order_dummy,vdo,logo,camID,positionx,positiony,record, font, nameid, login, array)
            # order_dummy = 'C' + customid + 'O' + order + 'T' + tel
            print(nameid, customid, order, tel, box_size)
            # เพิ่ม a เวลา
            # c = Process(target=cutvdo , args=(order,vdo,a,))
            # c.start()
            if box_size == '--':
                no_box_1min = 1
                box_size = '-'
            else:
                no_box_1min = 0
            cutvdo(order,vdo,a,no_box_1min)

            if box_size == '-' or box_size == '--':
                check_success = 'fall'
            else:
                check_success = 'success'

            # os.remove('{}bc.mp4'.format(order))
            # post to url
            url = "https://globalapi2.advice.co.th/api/upfile_json"
            if connect() == False:
                root4 = Tk()
                root4.withdraw()
                forget_end = 'no internet'
                backuppost(box_size, forget_end, date_dir, a, record, nameid, customid, order, tel)
                messagebox.showerror("Network error", "No internet connection")
                webbrowser.open('http://google.com', new=2)
                continue
            elif connect() == True:
                print('Internet connected')
                # m = Process(target=multipost ,args=(box_size, a, vdo,record,nameid,customid, order, tel, url,check_success,))
                # m.start()
                multipost(box_size, a, vdo,record,nameid,customid, order, tel, url,check_success)
            else:
                pass_func = Tk()
                pass_func.withdraw()
                messagebox.showerror("Error Skip", 'Failed Skip post process')
        except Exception as e:
            print(e)
            root3 = Tk()
            root3.withdraw()
            messagebox.showerror("Error Process", e)

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


def testDeviceusb(source,positionx,positiony):
    global log_processing
    cap = cv2.VideoCapture(source)
    if cap.isOpened():
        t = Thread(target=f, args=(source, positionx, positiony,))
        t.daemon = True
        t.start()
        # log_processing.append(t)
        # f(camID=source, positionx=positionx, positiony=positiony)
        return True
    else:
        return False

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

def confirm_yesno(message = 'ยืนยันที่จะปิดโปรแกรมหรือไม่'):
    # answer = messagebox.askyesno(title='confirmation',
    #                 message=message)
    if messagebox.askyesno(title='confirmation',
                    message=message):
        # for i in log_processing:
        #     i.terminate()
        root.destroy()
        sys.exit(1)

if __name__ == '__main__':
    create_database()
    log_processing = []
    if os.path.exists('d'+'://') == True:
        path = 'D:/vdo_packing'
    else:
        path = 'C:/vdo_packing'
    if os.path.isdir(path) == True:
        delete_store(7)
    check_but7, check_but8, check_but9 = False, False, False
    while True:
        root = Tk()
        root.title('CAMERA LIST')
        root.geometry('200x240+0+0')

        if check_but7 == False:
            check_but7 = testDeviceusb(source=0, positionx=100, positiony=100)

        if check_but7 == True:
            but7 = Label(root,text = 'USB-cam1', width=20, bg='#32CD32',fg='white', font=('Arial', 15))
            # but7 = Button(root, text='USB-cam1', width=20, bg='#32CD32',fg='white', command=lambda
            #     camID=0,
            #     positionx=100, positiony=100: f(camID, positionx, positiony))
            but7.pack(padx=5, pady=5)

        repost = Button(root, text="Re-post", width=20, bg='red' ,fg='white', command=repost)
        repost.pack(padx=5, pady=5)

        count = '0'
        num_report = Label(root,text = 'UNPOST = {}'.format(count), fg='red', font=('Arial', 15))
        num_report.pack(padx=5, pady=5)
        count_unpost()
        root.protocol('WM_DELETE_WINDOW', confirm_yesno)
        # Button(root, text='ปิดโปรแกรม', command=lambda root=root, message='ยืนยันที่จะปิดโปรแกรมหรือไม่': confirm_yesno(root,message)).pack(expand=True)
        # print(len(log_processing))

        root.mainloop()