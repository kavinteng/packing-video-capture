import os
import cv2
from tkinter import *
from multiprocessing import Process
from newpack_V2 import *
import urllib.request
import time
from datetime import date
import mariadb
import jwt
from getmac import getmac
from tkinter import messagebox
import webbrowser

class GUI(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()
        stepOne = LabelFrame(self, text="Camera Config")
        stepOne.grid(row=0, columnspan=7, sticky='W',padx=5, pady=5, ipadx=5, ipady=5)
        self.Val1Lbl = Label(stepOne, text="IP cam1")
        self.Val1Lbl.grid(row=0, column=0, sticky='E', padx=5, pady=2)
        self.Val1Txt = Entry(stepOne)
        self.Val1Txt.grid(row=0, column=1, columnspan=3, pady=2, sticky='WE')
        self.Val1Txt.insert(0, '192.168.10.50')
        self.Val7Lbl = Label(stepOne, text="PORT1")
        self.Val7Lbl.grid(row=0, column=5, sticky='E', padx=5, pady=2)
        self.Val7Txt = Entry(stepOne)
        self.Val7Txt.grid(row=0, column=6, columnspan=1, pady=2, sticky='WE')
        self.Val7Txt.insert(0, '41272')
        self.Val2Lbl = Label(stepOne,text="IP cam2")
        self.Val2Lbl.grid(row=1, column=0, sticky='E', padx=5, pady=2)
        self.Val2Txt = Entry(stepOne)
        self.Val2Txt.grid(row=1, column=1, columnspan=3, pady=2, sticky='WE')
        self.Val2Txt.insert(0, '192.168.10.60')
        self.Val8Lbl = Label(stepOne, text="PORT2")
        self.Val8Lbl.grid(row=1, column=5, sticky='E', padx=5, pady=2)
        self.Val8Txt = Entry(stepOne)
        self.Val8Txt.grid(row=1, column=6, columnspan=1, pady=2, sticky='WE')
        self.Val8Txt.insert(0, '50000')
        self.Val3Lbl = Label(stepOne, text="IP cam3")
        self.Val3Lbl.grid(row=2, column=0, sticky='E', padx=5, pady=2)
        self.Val3Txt = Entry(stepOne)
        self.Val3Txt.grid(row=2, column=1, columnspan=3, pady=2, sticky='WE')
        self.Val3Txt.insert(0, '192.168.10.70')
        self.Val9Lbl = Label(stepOne, text="PORT3")
        self.Val9Lbl.grid(row=2, column=5, sticky='E', padx=5, pady=2)
        self.Val9Txt = Entry(stepOne)
        self.Val9Txt.grid(row=2, column=6, columnspan=1, pady=2, sticky='WE')
        self.Val9Txt.insert(0, '81')
        self.Val4Lbl = Label(stepOne, text="IP cam4")
        self.Val4Lbl.grid(row=3, column=0, sticky='E', padx=5, pady=2)
        self.Val4Txt = Entry(stepOne)
        self.Val4Txt.grid(row=3, column=1, columnspan=3, pady=2, sticky='WE')
        self.Val10Lbl = Label(stepOne, text="PORT4")
        self.Val10Lbl.grid(row=3, column=5, sticky='E', padx=5, pady=2)
        self.Val10Txt = Entry(stepOne)
        self.Val10Txt.grid(row=3, column=6, columnspan=1, pady=2, sticky='WE')
        self.Val10Txt.insert(0, '17218')
        self.Val5Lbl = Label(stepOne, text="IP cam5")
        self.Val5Lbl.grid(row=4, column=0, sticky='E', padx=5, pady=2)
        self.Val5Txt = Entry(stepOne)
        self.Val5Txt.grid(row=4, column=1, columnspan=3, pady=2, sticky='WE')
        self.Val11Lbl = Label(stepOne, text="PORT5")
        self.Val11Lbl.grid(row=4, column=5, sticky='E', padx=5, pady=2)
        self.Val11Txt = Entry(stepOne)
        self.Val11Txt.grid(row=4, column=6, columnspan=1, pady=2, sticky='WE')
        self.Val11Txt.insert(0, '9327')
        self.Val6Lbl = Label(stepOne, text="IP cam6")
        self.Val6Lbl.grid(row=5, column=0, sticky='E', padx=5, pady=2)
        self.Val6Txt = Entry(stepOne)
        self.Val6Txt.grid(row=5, column=1, columnspan=3, pady=2, sticky='WE')
        self.Val12Lbl = Label(stepOne, text="PORT6")
        self.Val12Lbl.grid(row=5, column=5, sticky='E', padx=5, pady=2)
        self.Val12Txt = Entry(stepOne)
        self.Val12Txt.grid(row=5, column=6, columnspan=1, pady=2, sticky='WE')
        self.Val12Txt.insert(0,'81')

        self.val1 = None
        self.val2 = None
        self.val3 = None
        self.val4 = None
        self.val5 = None
        self.val6 = None
        self.val7 = None
        self.val8 = None
        self.val9 = None
        self.val10 = None
        self.val11 = None
        self.val12 = None


        SubmitBtn = Button(stepOne, text="Submit", command=self.submit)
        SubmitBtn.grid(row=7, column=6, sticky='W', padx=5, pady=2)
        # repost = Button(stepOne, text="Re-post", command=self.repost)
        # repost.grid(row=7, column=0, sticky='W', padx=5, pady=2)

    # def repost(self):
    #     try:
    #         connection = mariadb.connect(host="localhost", user="root", passwd="123456", database="advice")
    #     except mariadb.Error as e:
    #         print(f"Error connecting to MariaDB Platform: {e}")
    #         sys.exit(1)
    #     cursor = connection.cursor()
    #     try:
    #         TableSql = """CREATE TABLE backuppost(ID INT(20) PRIMARY KEY AUTO_INCREMENT,nameid CHAR(20),customid CHAR(20),orderid CHAR(20),tel CHAR(20),time CHAR(20))"""
    #         cursor.execute(TableSql)
    #     except:
    #         pass
    #     self.root2 = Tk()
    #     self.root2.title('repost')
    #     # root2.geometry('0+0')
    #
    #     cursor.execute("select * from backuppost ")
    #     lists = cursor.fetchall()
    #     e = Label(self.root2, width=11, text='PRIMARY KEY', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
    #     e.grid(row=0, column=0)
    #     e = Label(self.root2, width=11, text='USER ID', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
    #     e.grid(row=0, column=1)
    #     e = Label(self.root2, width=11, text='CUSTOMER ID', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
    #     e.grid(row=0, column=2)
    #     e = Label(self.root2, width=11, text='ORDER ID', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
    #     e.grid(row=0, column=3)
    #     e = Label(self.root2, width=11, text='TEL', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
    #     e.grid(row=0, column=4)
    #     e = Label(self.root2, width=11, text='TIME', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
    #     e.grid(row=0, column=5)
    #
    #     i = 1
    #
    #     for list in lists:
    #         for j in range(len(list)):
    #             e = Label(self.root2, width=11, text=list[j],
    #                       borderwidth=2, relief='ridge', anchor="w")
    #             e.grid(row=i, column=j)
    #         i = i + 1
    #
    #     connection.commit()
    #     connection.close()
    #
    #     repost2 = Button(self.root2, text="POST", command=self.post)
    #     repost2.grid(row=i, column=2, sticky='W', padx=5, pady=2)
    #     self.root2.mainloop()

    # def post(self):
    #     try:
    #         connection = mariadb.connect(host="localhost", user="root", passwd="123456", database="advice")
    #     except mariadb.Error as e:
    #         print(f"Error connecting to MariaDB Platform: {e}")
    #         sys.exit(1)
    #     cursor = connection.cursor()
    #     cursor.execute("select * from backuppost ")
    #     lists = cursor.fetchall()
    #     url = "https://globalapi.advice.co.th/api/upfile_json"
    #
    #     for list in lists:
    #         _,nameid,customid, order, tel, a = list
    #         date_dir = date.today()
    #         # file_name = "D:/vdo_packing/{}/{}.mp4".format(date_dir,order)
    #         file_name = "D:/vdo_packing/{}/{}{}.mp4".format(date_dir, order,a)
    #         name, extension = os.path.splitext(file_name)
    #         mac = getmac.get_mac_address()
    #         encoded = jwt.encode({'mac address': mac}, 'secret', algorithm='HS256')
    #
    #         with open(file_name, "rb") as file:
    #             data = {"data": file}
    #             text = {"Username": nameid, "Customer ID": customid, "Order ID": order, "Tel": tel,
    #                     "file_type": extension, "token": encoded}
    #             response = requests.post(url, files=data, data=text)
    #
    #             if response.ok:
    #                 print("Upload completed successfully!")
    #                 cursor.execute("delete from backuppost where orderid = ?", (order,))
    #
    #             else:
    #                 response.raise_for_status()
    #                 print("Something went wrong!")
    #
    #     connection.commit()
    #     connection.close()
    #     self.root2.destroy()


    def submit(self):
        self.val1 = self.Val1Txt.get()
        self.val2 = self.Val2Txt.get()
        self.val3 = self.Val3Txt.get()
        self.val4 = self.Val4Txt.get()
        self.val5 = self.Val5Txt.get()
        self.val6 = self.Val6Txt.get()
        self.val7 = self.Val7Txt.get()
        self.val8 = self.Val8Txt.get()
        self.val9 = self.Val9Txt.get()
        self.val10 = self.Val10Txt.get()
        self.val11 = self.Val11Txt.get()
        self.val12 = self.Val12Txt.get()

        self.destroy()

def repost():
    try:
        connection = mariadb.connect(host="localhost", user="root", passwd="123456", database="advicev2")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    cursor = connection.cursor()
    try:
        TableSql = """CREATE TABLE backuppost(ID INT(20) PRIMARY KEY AUTO_INCREMENT,nameid CHAR(20),customid CHAR(20),orderid CHAR(20),tel CHAR(20),date CHAR(20),time CHAR(20),detail CHAR(50))"""
        cursor.execute(TableSql)
    except:
        pass
    global root2
    root2 = Tk()
    root2.title('repost')
    cursor.execute("select * from backuppost limit 0,10")
    lists = cursor.fetchall()

    e = Label(root2, width=11, text='PRIMARY KEY', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
    e.grid(row=0, column=0)
    e = Label(root2, width=11, text='USER ID', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
    e.grid(row=0, column=1)
    e = Label(root2, width=11, text='CUSTOMER ID', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
    e.grid(row=0, column=2)
    e = Label(root2, width=11, text='ORDER ID', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
    e.grid(row=0, column=3)
    e = Label(root2, width=11, text='TEL', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
    e.grid(row=0, column=4)
    e = Label(root2, width=11, text='DATE', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
    e.grid(row=0, column=5)
    e = Label(root2, width=11, text='TIME', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
    e.grid(row=0, column=6)
    e = Label(root2, width=30, text='Error detail', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
    e.grid(row=0, column=7)

    i = 1
    for list in lists:
        for j in range(len(list)):
            if j%7 == 0 and j != 0:
                e = Label(root2, width=30, text=list[j],
                            borderwidth=2, relief='ridge', anchor="w")
            else:
                e = Label(root2, width=11, text=list[j],
                            borderwidth=2, relief='ridge', anchor="w")
            e.grid(row=i, column=j)
        i = i + 1

    connection.commit()
    connection.close()

    repost2 = Button(root2, text="POST", command=post)
    repost2.grid(row=i+1, column=4, sticky='W', padx=5, pady=2)
    root2.mainloop()

def post():
    try:
        connection = mariadb.connect(host="localhost", user="root", passwd="123456", database="advicev2")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    cursor = connection.cursor()
    cursor.execute("select * from backuppost limit 0,10")
    lists = cursor.fetchall()
    url = "https://globalapi.advice.co.th/api/upfile_json"
    for list in lists:
        _, nameid, customid, order, tel, date, a, _ = list
        # file_name = "D:/vdo_packing/{}/{}.mp4".format(date_dir,order)
        file_name = "D:/vdo_packing/{}/{}{}.mp4".format(date, order, a)
        name, extension = os.path.splitext(file_name)
        mac = getmac.get_mac_address()
        encoded = jwt.encode({'mac address': mac}, 'secret', algorithm='HS256')

        try:
            with open(file_name, "rb") as file:
                data = {"data": file}
                text = {"Username": nameid, "Customer ID": customid, "Order ID": order, "Tel": tel,
                        "file_type": extension, "token": encoded}
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
        connection = mariadb.connect(host="localhost", user="root", passwd="123456", database="advicev2")
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

def quit():
    """Cancel all scheduled callbacks and quit."""
    for after_id in root.tk.eval('after info').split():
        root.after_cancel(after_id)
    root.destroy()

def confirm(ip,port):
    left = 'http://{}:{}/decoder_control.cgi?loginuse=admin&loginpas=888888&command=4&onestep=1'.format(ip,port)
    right = 'http://{}:{}/decoder_control.cgi?loginuse=admin&loginpas=888888&command=6&onestep=1'.format(ip, port)
    for i in range(2):
        if i ==0:
            urllib.request.urlopen(left)
        else:
            urllib.request.urlopen(right)
        time.sleep(1)

def f(ip,port,camID,positionx,positiony):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    qrcode = os.path.join(base_dir, "qrcode")
    # vdo = os.path.join(base_dir, "vdo")
    date_dir = date.today()
    vdo_dir = 'D:/vdo_packing'
    vdo = 'D:/vdo_packing/{}'.format(date_dir)
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
    img_aruco = cv2.imread("phone_aruco_marker.jpg")
    cap = cv2.VideoCapture(camID)
    while True:
        try:
            # create new and remove old
            a, record, font, st, nameid, customid, order, tel, login = main(cap,order_dummy,ip,port,vdo,logo,camID,positionx,positiony,record, font, nameid, login, array, img_aruco)
            # order_dummy = 'C' + customid + 'O' + order + 'T' + tel
            print(nameid, customid, order, tel)
            # เพิ่ม a เวลา
            # c = Process(target=cutvdo , args=(order,vdo,a,))
            # c.start()
            cutvdo(order,vdo,a)
            # os.remove('{}bc.mp4'.format(order))
            # post to url
            url = "https://globalapi.advice.co.th/api/upfile_json"
            if connect() == False:
                root4 = Tk()
                root4.withdraw()
                forget_end = 'no internet'
                backuppost(forget_end, date_dir, a, record, nameid, customid, order, tel)
                messagebox.showerror("Network error", "No internet connection")
                webbrowser.open('http://google.com', new=2)
                continue
            elif connect() == True:
                print('Internet connected')
                m = Process(target=multipost ,args=(a, vdo,record,nameid,customid, order, tel, url,))
                m.start()
            else:
                pass_func = Tk()
                pass_func.withdraw()
                messagebox.showerror("Error Skip", 'Failed Skip post process')
        except Exception as e:
            print(e)
            root3 = Tk()
            root3.withdraw()
            messagebox.showerror("Error Process", e)

def run(ip,port,camID,positionx,positiony):
    t = Process(target=f, args=(ip,port,camID,positionx,positiony,))
    t.start()

def multipost(a, vdo,record,nameid,customid, order, tel, url):
    print('------multipost------')
    post_requests(None,a, vdo, record, nameid, customid, order, tel, url)
    # date_dir = datetime.date.today()
    # if check_post == 2:
    #     backuppost(check_post, date_dir, a, record, nameid, customid, order, tel)
    #     root3 = Tk()
    #     root3.withdraw()
    #     messagebox.showerror("Error Alert", "fail post")


def testDeviceusb(source,positionx,positiony):
    cap = cv2.VideoCapture(source)
    if cap.isOpened():
        run(None, None, camID=source, positionx=positionx, positiony=positiony)
        return True
    else:
        return False

def testDeviceip(ip):
   check = os.system('ping {} /n 1'.format(ip))
   if check == 0:
       return True
   else:
       return False

if __name__ == '__main__':
    while True:
        app = GUI(None)
        app.title('Camera Config')
        app.mainloop()
        ip1 = app.val1
        ip2 = app.val2
        ip3 = app.val3
        ip4 = app.val4
        ip5 = app.val5
        ip6 = app.val6
        port1 = app.val7
        port2 = app.val8
        port3 = app.val9
        port4 = app.val10
        port5 = app.val11
        port6 = app.val12

        if ip1 == '' and ip2 == '' and ip3 == '' and ip4 == '' and ip5 == '' and ip6 == '':
            pass
        elif ip1 == None:
            exit()
        else:
            root = Tk()
            root.title('CAMERA LIST')
            root.geometry('200x240+0+0')

            # check_but1 = testDeviceip(ip1)
            # check_but2 = testDeviceip(ip2)
            # check_but3 = testDeviceip(ip3)
            check_but7 = testDeviceusb(source=0, positionx=0, positiony=380)
            check_but8 = testDeviceusb(source=1, positionx=530, positiony=380)
            check_but9 = testDeviceusb(source=2, positionx=1060, positiony=380)

            # if check_but1 == True:
            #     but1 = Button(root, text='opencam1', width=20, command=lambda
            #         camID='http://{}:{}/videostream.cgi?user=admin&pwd=888888'.format(ip1, port1),
            #         positionx=200, positiony=0: run(ip1,port1,camID, positionx, positiony))
            #     but1.pack(padx=5, pady=5)
            # if check_but2 == True:
            #     but2 = Button(root, text='opencam2', width=20, command=lambda
            #         camID='http://{}:{}/videostream.cgi?user=admin&pwd=888888'.format(ip2, port2),
            #         positionx=520, positiony=0: run(ip2,port2,camID, positionx, positiony))
            #     but2.pack(padx=5, pady=5)
            # if check_but3 == True:
            #     but3 = Button(root, text='opencam3', width=20, command=lambda
            #         camID='http://{}:{}/videostream.cgi?user=admin&pwd=888888'.format(ip3, port3),
            #         positionx=840, positiony=0: run(ip3,port3,camID, positionx, positiony))
            #     but3.pack(padx=5, pady=5)

            # if ip4 != '' and ip4 != None:
            #     but4 = Button(root, text='opencam4', width=20, command=lambda
            #         camID='http://{}:{}/videostream.cgi?user=admin&pwd=888888'.format(ip4, port4),
            #         positionx=200, positiony=300: run(ip4,port4,camID, positionx, positiony))
            #     but4.pack(padx=5, pady=5)
            #
            # if ip5 != '' and ip5 != None:
            #     but5 = Button(root, text='opencam5', width=20, command=lambda
            #         camID='http://{}:{}/videostream.cgi?user=admin&pwd=888888'.format(ip5, port5),
            #         positionx=520, positiony=300: run(ip5,port5,camID, positionx, positiony))
            #     but5.pack(padx=5, pady=5)
            #
            # if ip6 != '' and ip6 != None:
            #     but6 = Button(root, text='opencam6', width=20, command=lambda
            #         camID='http://{}:{}/videostream.cgi?user=admin&pwd=888888'.format(ip6, port6),
            #         positionx=840, positiony=300: run(ip6,port6,camID, positionx, positiony))
            #     but6.pack(padx=5, pady=5)
            if check_but7 == True:
                but7 = Button(root, text='USB-cam1', width=20, bg='#32CD32',fg='white', command=lambda
                    camID=0,
                    positionx=0, positiony=300: run(None, None, camID, positionx, positiony))
                but7.pack(padx=5, pady=5)
            if check_but8 == True:
                but8 = Button(root, text='USB-cam2', width=20, bg='#32CD32',fg='white', command=lambda
                    camID=1,
                    positionx=530, positiony=300: run(None, None, camID, positionx, positiony))
                but8.pack(padx=5, pady=5)
            if check_but9 == True:
                but9 = Button(root, text='USB-cam3', width=20, bg='#32CD32',fg='white', command=lambda
                    camID=2,
                    positionx=1060, positiony=300: run(None, None, camID, positionx, positiony))
                but9.pack(padx=5, pady=5)

            repost = Button(root, text="Re-post", width=20, bg='red' ,fg='white', command=repost)
            repost.pack(padx=5, pady=5)

            count = '0'
            num_report = Label(root,text = 'UNPOST = {}'.format(count), fg='red', font=('Arial', 15))
            num_report.pack(padx=5, pady=5)
            count_unpost()
            root.protocol('WM_DELETE_WINDOW', quit)
            root.mainloop()