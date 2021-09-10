from tkinter import *
from multiprocessing import Process
from newpack import *
import urllib.request
import time
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
        self.Val1Txt.insert(0, '192.168.137.7')
        self.Val7Lbl = Label(stepOne, text="PORT1")
        self.Val7Lbl.grid(row=0, column=5, sticky='E', padx=5, pady=2)
        self.Val7Txt = Entry(stepOne)
        self.Val7Txt.grid(row=0, column=6, columnspan=1, pady=2, sticky='WE')
        self.Val7Txt.insert(0, '10080')
        self.Val2Lbl = Label(stepOne,text="IP cam2")
        self.Val2Lbl.grid(row=1, column=0, sticky='E', padx=5, pady=2)
        self.Val2Txt = Entry(stepOne)
        self.Val2Txt.grid(row=1, column=1, columnspan=3, pady=2, sticky='WE')
        self.Val8Lbl = Label(stepOne, text="PORT2")
        self.Val8Lbl.grid(row=1, column=5, sticky='E', padx=5, pady=2)
        self.Val8Txt = Entry(stepOne)
        self.Val8Txt.grid(row=1, column=6, columnspan=1, pady=2, sticky='WE')
        self.Val8Txt.insert(0, '81')
        self.Val3Lbl = Label(stepOne, text="IP cam3")
        self.Val3Lbl.grid(row=2, column=0, sticky='E', padx=5, pady=2)
        self.Val3Txt = Entry(stepOne)
        self.Val3Txt.grid(row=2, column=1, columnspan=3, pady=2, sticky='WE')
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
        SubmitBtn.grid(row=7, column=3, sticky='W', padx=5, pady=2)

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
        if connect() == False:
            print('No Internet connection!')
            continue
        else:
            print('Internet connected')
        try:
            # create new and remove old
            record, font, st, nameid, customid, order, tel, login = main(ip,port,vdo,logo,camID,positionx,positiony,record, font, nameid, login, array, img_aruco)
            print(nameid, customid, order, tel)
            cutvdo(order,vdo)
            os.remove('{}bc.mp4'.format(order))
            # post to url
            url = "https://globalapi.advice.co.th/api/upfile_json"
            post_requests(vdo,nameid,customid, order, tel, url)
        except Exception as e:
            print(e)

def quit_(root):
    root.destroy()

def run(ip,port,camID,positionx,positiony):
    t = Process(target=f, args=(ip,port,camID,positionx,positiony,))
    t.start()

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

        if ip1 is None or ip1 == '' and ip2 == '' and ip3 == '' and ip4 == '' and ip5 == '' and ip6 == '':
            pass
        else:
            root = Tk()
            root.title('test')
            root.geometry('200x240+0+0')
            root.config(bg='black')

        if ip1 != '' and ip1 != None:
            but1 = Button(root, text='opencam1', width=20, command=lambda
                camID='http://{}:{}/videostream.cgi?user=admin&pwd=888888'.format(ip1, port1),
                positionx=200, positiony=0: run(ip1,port1,camID, positionx, positiony))
            but1.pack(padx=5, pady=5)

        if ip2 != '' and ip2 != None:
            but2 = Button(root, text='opencam2', width=20, command=lambda
                camID='http://{}:{}/videostream.cgi?user=admin&pwd=888888'.format(ip2, port2),
                positionx=520, positiony=0: run(ip2,port2,camID, positionx, positiony))
            but2.pack(padx=5, pady=5)
        if ip3 != '' and ip3 != None:
            but3 = Button(root, text='opencam3', width=20, command=lambda
                camID='http://{}:{}/videostream.cgi?user=admin&pwd=888888'.format(ip3, port3),
                positionx=840, positiony=0: run(ip3,port3,camID, positionx, positiony))
            but3.pack(padx=5, pady=5)

        if ip4 != '' and ip4 != None:
            but4 = Button(root, text='opencam4', width=20, command=lambda
                camID='http://{}:{}/videostream.cgi?user=admin&pwd=888888'.format(ip4, port4),
                positionx=200, positiony=300: run(ip4,port4,camID, positionx, positiony))
            but4.pack(padx=5, pady=5)

        if ip5 != '' and ip5 != None:
            but5 = Button(root, text='opencam5', width=20, command=lambda
                camID='http://{}:{}/videostream.cgi?user=admin&pwd=888888'.format(ip5, port5),
                positionx=520, positiony=300: run(ip5,port5,camID, positionx, positiony))
            but5.pack(padx=5, pady=5)

        if ip6 != '' and ip6 != None:
            but6 = Button(root, text='opencam6', width=20, command=lambda
                camID='http://{}:{}/videostream.cgi?user=admin&pwd=888888'.format(ip6, port6),
                positionx=840, positiony=300: run(ip6,port6,camID, positionx, positiony))
            but6.pack(padx=5, pady=5)
        if ip1 is None:
            exit()
        elif ip1 == '' and ip2 == '' and ip3 == '' and ip4 == '' and ip5 == '' and ip6 == '':
            pass
        else:
            root.mainloop()