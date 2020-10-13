import logging
import tkinter
import xlrd
import os
import threading
import playsound
import logging

from tkinter import StringVar, Tk, Label, Button, Frame, FLAT, IntVar, Checkbutton
from kanji import Kanji


# logging.basicConfig(level=logging.INFO)

# setting here
ROOT = 'http://jls.vnjpclub.com/'
SOUNDS_FOLDER = 'sounds/'
EXCEL_NAME = 'excel_kanji_sub.xls'

class MyWindow(Tk):

    CURRENT_KANJI = None

    def __init__(self) -> None:
        super().__init__()
        self.title("Make you pro Kanjis")
        # self.geometry('1920x1080')
        self.iconbitmap('imgs/60718420_101234007792351_1661689307422785536_o.ico')

        # check excel
        if os.path.exists(EXCEL_NAME) == False:
            print('Có vẻ như không tồn tại file excel với tên '+ EXCEL_NAME +
                  ', nếu bạn đã tạo một file excel thì hãy xem thử tên của nó đã đúng là '+ EXCEL_NAME+' hay chưa, sau đó chạy lại chương trình')
            exit()

        # load kanji
        self.wb = xlrd.open_workbook(EXCEL_NAME)
        self.sheet = self.wb.sheet_by_index(0)
        self.listKanji = []
        for i in range(1, self.sheet.nrows):
            row = self.sheet.row(i)
            kanji = row[0].value
            hiragana = row[1].value
            han_viet = row[2].value
            mean = row[3].value
            bai = row[4].value
            sound_url = row[5].value
            sound_path = row[6].value
            kanji_object = Kanji(kanji, hiragana, han_viet, mean, bai, sound_url, sound_path)
            self.listKanji.append(kanji_object)

        # event keydown/up
        self.bind('<space>', self.spaceDown)
        self.bind('<KeyRelease-space>', self.spaceUp)
        self.bind('<Key-Right>', self.loadWord)
        self.bind('<Key-Escape>', lambda e: exit())


        # config app
        self.FONT_HIRAGANA = 30
        self.FONT_KANJI = 50
        self.FONT = ''
        self.ORDER_MODE = True
        self.KANJI_MODE = True
        self.FULLSCREEN = False
        self.ROW_ACTION_BUTTON = 0
        self.CURRENT_INDEX = 0

        # state
        self.listCurrentChoice = []
        self.enableCheckbox = []
        self.setupUI()


    def setupUI(self):

        self.kanji_var = StringVar(self)
        self.kanji = Label(master=self, font=('', self.FONT_KANJI), textvariable=self.kanji_var)
        self.kanji.pack(side=tkinter.TOP, pady=(200, 100))

        self.hiragana_var = StringVar(self)
        self.hiragana = Label(master=self, font=('', self.FONT_HIRAGANA), textvariable=self.hiragana_var)
        self.hiragana.pack()

        self.frame_bai = Frame(master=self)
        row = 0
        col = 0
        count = 0
        while True:
            if(col==10):
                col = 0
                row+=1
            if(row == 5):
                row==4
            self.enableCheckbox.append(IntVar())
            c = Checkbutton(master=self.frame_bai, text='Bài {}'.format(count+1), variable=self.enableCheckbox[count])
            c['command'] = self.loadKotoba
            c.grid(row=row, column=col)
            count+=1
            col+=1
            if count == 50:
                break
        self.frame_bai.pack(side=tkinter.BOTTOM)

        self.button_next = Button(master=self, text='Another')
        self.button_next['relief'] = FLAT
        self.button_next['background'] = '#fab1a0'
        self.button_next['command'] = self.loadWord
        self.button_next.place(x=0, y=self.ROW_ACTION_BUTTON, width=125, height=50)

        self.show_mode = StringVar(master=self, value='Hiragana')
        self.button_hiragana = Button(master=self, textvariable=self.show_mode)
        self.button_hiragana['relief'] = FLAT
        self.button_hiragana['background'] = '#e17055'
        self.button_hiragana['command'] = self.showHiragana
        self.button_hiragana.place(x=115, y=self.ROW_ACTION_BUTTON, width=125, height=50)

        self.button_excel = Button(master=self, text='Excel')
        self.button_excel['relief'] = FLAT
        self.button_excel['background'] = '#fdcb6e'
        self.button_excel['command'] = self.showExcel
        self.button_excel.place(x=230, y=self.ROW_ACTION_BUTTON, width=125, height=50)

        self.fullscreen = StringVar(master=self, value='Fullscreen')
        self.button_fullscreen = Button(master=self, textvariable=self.fullscreen)
        self.button_fullscreen['relief'] = FLAT
        self.button_fullscreen['background'] = '#00b894'
        self.button_fullscreen['command'] = self.fullScreen
        self.button_fullscreen.place(x=345, y=self.ROW_ACTION_BUTTON, width=125, height=50)

        self.loadWord()


    def loadWord(self, event=None):
        logging.info('Load word!!!')
        self.KANJI_MODE = True
        self.kanji['font'] = ('', self.FONT_KANJI)
        self.hiragana_var.set('')
        if self.CURRENT_INDEX < len(self.listKanji):
            self.CURRENT_KANJI = self.listKanji[self.CURRENT_INDEX]
            self.CURRENT_INDEX += 1
        else:
            self.CURRENT_INDEX = 0

        # kiem tra file am thanh da ton tai hay chua
        logging.debug('loadWord:File sound is exist: {}'.format(os.path.exists(self.CURRENT_KANJI.sound_path)))
        if os.path.exists(self.CURRENT_KANJI.sound_path) == False:
            self.CURRENT_KANJI.downloadSound()

        logging.debug('loadWord:current kanji:getKanji:{}'.format(self.CURRENT_KANJI.getKanji()))
        if self.CURRENT_KANJI.getKanji() == '':
            logging.info('loadWord:Kanji is Empty')
            self.show_mode.set('Mean')
            self.kanji_var.set(self.CURRENT_KANJI.getHiragana())
        else:
            self.show_mode.set('Hiragana')
            self.kanji_var.set(self.CURRENT_KANJI.getKanji())


    def showHiragana(self):
        if self.KANJI_MODE:
            self.KANJI_MODE = False
            show_hiragana = threading.Thread(target=self.thread_show_hiragana)
            show_hiragana.start()
        else:
            self.kanji['font'] = ('', self.FONT_KANJI)
            if self.CURRENT_KANJI.getKanji() == '':
                self.show_mode.set('Mean')
                self.kanji_var.set(self.CURRENT_KANJI.getHiragana())
            else:
                self.show_mode.set('Hiragana')
                self.kanji_var.set(self.CURRENT_KANJI.getKanji())
            self.KANJI_MODE = True


    def showExcel(self):
        tr = threading.Thread(target=lambda: os.system(EXCEL_NAME))
        tr.start()


    def spaceDown(self, event):
        logging.info('Space down')
        if self.KANJI_MODE:
            show_hiragana = threading.Thread(target=self.thread_show_hiragana)
            show_hiragana.start()
            self.KANJI_MODE = False
        else:
            self.hiragana_var.set('')
            self.kanji['font'] = ('', self.FONT_KANJI)
            self.show_mode.set('Hiragana')
            if self.CURRENT_KANJI.getKanji() == '':
                self.kanji_var.set(self.CURRENT_KANJI.getHiragana())
            else:
                self.kanji_var.set(self.CURRENT_KANJI.getKanji())
            self.KANJI_MODE = True


    def spaceUp(self, event):
        logging.info('Space Up')
        if self.KANJI_MODE == False:
            playsound.playsound(self.CURRENT_KANJI.getSoundPath(), block=True)


    def loadKotoba(self):
        logging.info('load new word')
        """Làm sao để học mà không biết học bài nào :D Không sao đã có hàm chọn bài giúp bạn thoải
        mái chọn những bài mà bạn cần ôn.
        
        @ làm mới lại listKanji và gọi lại LoadWord"""
        # clean and add lesson to listcurrentchoice
        self.listCurrentChoice = []
        for var in range(len(self.enableCheckbox)):
            if(self.enableCheckbox[var].get()==1):
                self.listCurrentChoice.append(var+1)
        
        # clean and load Kanji to list
        self.listKanji.clear()
        self.sheet = self.wb.sheet_by_index(0)

        # load all word when the app start
        if self.listCurrentChoice == []:
            self.sheet = self.wb.sheet_by_index(0)
            for i in range(1, self.sheet.nrows):
                row = self.sheet.row(i)
                kanji = row[0].value
                hiragana = row[1].value
                han_viet = row[2].value
                mean = row[3].value
                bai = row[4].value
                sound_url = row[5].value
                sound_path = row[6].value
                kanji_object = Kanji(kanji, hiragana, han_viet, mean, bai, sound_url, sound_path)
                self.listKanji.append(kanji_object)
        else:
            # load word base on lesson
            for i in range(1, self.sheet.nrows):
                if (self.sheet.row_values(i)[4] in self.listCurrentChoice):
                    row = self.sheet.row(i)
                    kanji = row[0].value
                    hiragana = row[1].value
                    han_viet = row[2].value
                    mean = row[3].value
                    bai = row[4].value
                    sound_url = row[5].value
                    sound_path = row[6].value
                    kanji_object = Kanji(kanji, hiragana, han_viet, mean, bai, sound_url, sound_path)
                    logging.info('Load kotoba:Kanji {}'.format(kanji_object.getHanViet()))
                    self.listKanji.append(kanji_object)
        logging.debug(self.listKanji)
        self.CURRENT_INDEX = 0
        self.loadWord()


    def readWord(self, path):
        playsound.playsound(path, block=True)


    def thread_show_hiragana(self):
        self.show_mode.set("Kanji")
        if self.CURRENT_KANJI.getKanji() == '':
            self.hiragana_var.set(self.CURRENT_KANJI.getMean())
        else:
            self.hiragana_var.set(
                self.CURRENT_KANJI.getHanViet()+'\n'+
                self.CURRENT_KANJI.getHiragana()+'\n'+
                self.CURRENT_KANJI.getMean())
        self.KANJI_MODE = False



    def fullScreen(self):
        if self.FULLSCREEN == False:
            self.state('zoomed')
            self.fullscreen.set('Normal')
            self.FULLSCREEN = True
        else:
            self.state('normal')
            self.fullscreen.set('Fullscreen')
            self.FULLSCREEN = False
        

if __name__ == "__main__":
    mywindow = MyWindow()
    mywindow.mainloop()
