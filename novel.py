import requests
from bs4 import BeautifulSoup
import random
from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
import tkinter.filedialog
from  tkinter  import ttk
from PIL import Image, ImageTk 
import os
import threading

class GUI:
    def __init__(self):
        #variable
        self.url = ''
        self.fileName = ''
        self.downloadPath = os.path.join(os.getcwd(), 'download')
        #initial
        self.app = tkinter.Tk()
        self.app.title('CK NOVEL DOWNLOADER')
        #self.app.iconbitmap('./img/icon.ico')
        img = tkinter.PhotoImage(file = './img/icon.ico')
        self.app.tk.call('wm', 'iconphoto', self.app._w, img)
        self.app.resizable(width = False, height = False)
        self.app.geometry('800x400')
        self.app.config(background = '#d6f4ff')
        self.app.option_add('*Font', '微軟正黑體')
        self.app.option_add('*background', '#d6f4ff')
        self.efont = Font(family = '微軟正黑體', size = 12)
        #title & bg
        bgimg =  self.openImg('./img/CKnovel_title.png', 600, 160)
        backbround = tkinter.Label(self.app, image = bgimg)
        backbround.bgimg = bgimg
        backbround.pack(side = 'top')
        f1 = tkinter.Frame(self.app, width = 700, height = 50)
        f1.pack_propagate(0)
        self.savePath(f1)
        f1.pack()
        f2 = tkinter.Frame(self.app, width = 700, height = 50)
        f2.pack_propagate(0)
        self.inputURL(f2)
        f2.pack()
        f3 = tkinter.Frame(self.app, width = 700, height = 50)
        f3.pack_propagate(0)
        self.inputName(f3)
        f3.pack()
        img = self.openImg('./img/start_icon.png', 200, 54)
        pathBtn = tkinter.Button(self.app, image = img)
        pathBtn.img = img
        pathBtn.config(borderwidth = 0, highlightthickness = 0)
        pathBtn.pack(pady = 30)
        pathBtn['command'] = lambda:self.thread(self.start)
        self.app.mainloop()


    def savePath(self, frame):
        dimg =  self.openImg('./img/download.png', 32, 32)
        downImg = tkinter.Label(frame, image = dimg)
        downImg.dimg = dimg
        downImg.pack(padx = (15, 0), pady = 5, side = 'left')
        pathText = tkinter.Label(frame)
        pathText['text'] = '下載路徑:'
        pathText.pack(pady = 5, side = 'left')
        self.pathField = tkinter.Entry(frame)
        self.pathField.config(borderwidth = 0, highlightthickness = 0, font = self.efont)
        self.pathField['bg'] = 'white'
        self.pathField['width'] = 55
        self.pathField.pack(padx = 5, pady = 5, ipadx = 0, ipady = 4, side = 'left')
        self.pathField.insert(0, self.downloadPath)
        img = self.openImg('./img/folder.png', 26, 26)
        pathBtn = tkinter.Button(frame, image = img)
        pathBtn.img = img
        pathBtn.config(borderwidth = 0, highlightthickness = 0)
        pathBtn.pack(padx = 5, pady = 5, side = 'left')
        pathBtn['command'] = self.selectPath

    def inputURL(self, frame):
        dimg =  self.openImg('./img/loupe.png', 32, 32)
        downImg = tkinter.Label(frame, image = dimg)
        downImg.dimg = dimg
        downImg.pack(padx = (15, 0), pady = 5, side = 'left')
        pathText = tkinter.Label(frame)
        pathText['text'] = '小說來源:'
        pathText.pack(pady = 5, side = 'left')
        self.urlField = tkinter.Entry(frame)
        self.urlField.config(borderwidth = 0, highlightthickness = 0, font = self.efont)
        self.urlField['bg'] = 'white'
        self.urlField['width'] = 59
        self.urlField.pack(padx = 5, pady = 5, ipadx = 0, ipady = 4, side = 'left')
        self.urlField.insert(0, self.url)

    def inputName(self, frame):
        dimg =  self.openImg('./img/txt.png', 32, 32)
        downImg = tkinter.Label(frame, image = dimg)
        downImg.dimg = dimg
        downImg.pack(padx = (15, 0), pady = 5, side = 'left')
        pathText = tkinter.Label(frame)
        pathText['text'] = '檔案名稱:'
        pathText.pack(pady = 5, side = 'left')
        self.nameField = tkinter.Entry(frame)
        self.nameField.config(borderwidth = 0, highlightthickness = 0, font = self.efont)
        self.nameField['bg'] = 'white'
        self.nameField['width'] = 55
        self.nameField.pack(padx = 5, pady = 5, ipadx = 0, ipady = 4, side = 'left')
        self.nameField.insert(0, self.fileName)
        txtText = tkinter.Label(frame)
        txtText['text'] = '.txt'
        txtText.pack(pady = 5, side = 'left')


    def download(self):
        my_headers = [
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
            "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
            'Opera/9.25 (Windows NT 5.1; U; en)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
            'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
            'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
        ]
        headers = {'User-Agent': random.choice(my_headers)}
        try:
            if not os.path.exists(self.downloadPath):
                os.makedirs(self.downloadPath)
            with open(os.path.join(self.downloadPath, self.fileName), 'w', encoding="utf-8") as f:
                while True:
                    r = requests.get(self.url, headers = headers)
                    if r.status_code == requests.codes.ok:
                        soup = BeautifulSoup(r.text, 'html.parser')
                        items = soup.select('td.t_f')
                        nxtpage = soup.find('a', 'nxt')
                    for i in items:       
                        f.write(i.text)
                    if nxtpage == None:
                        print('complete')
                        break
                    else:
                        print(nxtpage['href'])
                        self.url = nxtpage['href']
        except Exception as e:
            print(e)
            messagebox.showerror("錯誤", "下載出錯了！")
    
    def selectPath(self):
        filename = tkinter.filedialog.askdirectory()
        if filename != '':
            self.pathField.delete(0, END) 
            self.pathField.insert(0, filename)
        else:
            print('None')

    def openImg(self, imagePath, w_box, h_box):
        def resize( w, h, w_box, h_box, pil_image):
            f1 = 1.0 * w_box / w    
            f2 = 1.0 * h_box / h    
            factor = min([f1, f2])       
            # use best down-sizing filter    
            width = int(w * factor)    
            height = int(h*factor)    
            return pil_image.resize((width, height), Image.ANTIALIAS) 

        pil_image = Image.open(imagePath)
        w, h = pil_image.size
        pil_image_resize = resize(w, h, w_box, h_box, pil_image)
        tk_image = ImageTk.PhotoImage(pil_image_resize)
        return tk_image

    def start(self):
        self.app.config(cursor = 'watch')
        self.downloadPath = self.pathField.get()
        self.url = self.urlField.get()
        self.fileName = self.nameField.get()
        self.fileName = self.fileName + '.txt'
        self.download()
        self.app.config(cursor = '')


    def thread(self, func, *args):
        t = threading.Thread(target = func, args = args)
        t.setDaemon(True)
        t.start()

GUI = GUI()