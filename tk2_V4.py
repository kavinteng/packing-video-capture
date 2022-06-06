from newpack_V4 import *
import sqlite3
from tkinter import *
import webbrowser
from threading import Thread

def count_unpost():
    global after_id
    connection = sqlite3.connect(sqlite_dir)
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

def confirm_yesno(message = 'ยืนยันที่จะปิดโปรแกรมหรือไม่'):
    if messagebox.askyesno(title='confirmation',message=message):
        root.destroy()
        sys.exit(1)

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
    login = False
    cap = cv2.VideoCapture(camID)
    # cap = cv2.VideoCapture('test_box_color.mp4')
    while True:
        try:
            # create new and remove old
            box_size, a, record, font, st, nameid, customid, order, tel, login = main(cap,vdo,logo,camID,positionx,positiony,record, font, nameid, login, array)
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

log_processing = []
if os.path.exists('d' + '://') == True:
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
        but7 = Label(root, text='USB-cam1', width=20, bg='#32CD32', fg='white', font=('Arial', 15))
        but7.pack(padx=5, pady=5)

    repost = Button(root, text="Re-post", width=20, bg='red', fg='white', command=repost)
    repost.pack(padx=5, pady=5)

    count = '0'
    num_report = Label(root, text='UNPOST = {}'.format(count), fg='red', font=('Arial', 15))
    num_report.pack(padx=5, pady=5)
    count_unpost()
    root.protocol('WM_DELETE_WINDOW', confirm_yesno)

    root.mainloop()