from tkinter import Event, StringVar, Tk, Label, Button, Frame, FLAT, IntVar, Checkbutton
import xlrd
import os
import threading
from random import choice


class Kanji:

    def __init__(self, data) -> None:
        self.kanji = data[0]
        self.hiragana = data[1]
        self.bo_thu = data[2]
        self.mean = data[3]
        self.bai = data[4]

    def getKanji(self):
        return self.kanji

    def getHiragana(self):
        return self.hiragana

    def getBoThu(self):
        return self.bo_thu

    def getMean(self):
        return self.mean

    def getBai(self):
        return self.bai


class MyWindow(Tk):

    def __init__(self) -> None:
        super().__init__()
        self.title("Help you pro Kanji")
        self.attributes('-fullscreen', True)
        self.bind('<Key-Escape>', lambda e: exit())

        # check excel
        self.excel_name = 'excel_kanji.xls'
        if os.path.exists(self.excel_name) == False:
            print('Có vẻ như không tồn tại file excel với tên '+self.excel_name +
                  ', nếu bạn đã tạo một file excel thì hãy xem thử tên của nó đã đúng là '+self.excel_name+' hay chưa, sau đó chạy lại chương trình')
            exit()

        # load kanji
        self.wb = xlrd.open_workbook(self.excel_name)
        self.sheet = self.wb.sheet_by_index(0)
        self.listKanji = [Kanji(self.sheet.row_values(i))
                          for i in range(1, self.sheet.nrows)]
        self.currentKanji = choice(self.listKanji)

        # event keydown/up
        self.bind('<KeyPress-space>', self.spaceDown)
        self.bind('<KeyRelease-space>', self.spaceUp)
        self.bind('<Key-Right>', self.nextWord)
        self.kanjiMode = True

        # config app
        self.FONT_HIRAGANA = 50
        self.FONT_KANJI = 50
        self.FONT = ''

        # state
        self.listCurrentChoice = []
        self.enableCheckbox = []
        self.setupUI()

    def setupUI(self):

        self.kanji_var = StringVar(self)
        self.kanji = Label(master=self, font=(
            '', self.FONT_KANJI), textvariable=self.kanji_var)
        self.kanji.pack(expand=True)

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
        self.frame_bai.pack()

        self.button_next = Button(master=self, text='Từ khác')
        self.button_next['relief'] = FLAT
        self.button_next['background'] = '#fab1a0'
        self.button_next['command'] = self.nextWord
        self.button_next.place(x=0, y=100, width=125, height=50)

        self.show_mode = StringVar(master=self, value='Hiragana')
        self.button_hiragana = Button(master=self, textvariable=self.show_mode)
        self.button_hiragana['relief'] = FLAT
        self.button_hiragana['background'] = '#e17055'
        self.button_hiragana['command'] = self.showHiragana
        self.button_hiragana.place(x=115, y=100, width=125, height=50)

        self.button_excel = Button(master=self, text='Excel')
        self.button_excel['relief'] = FLAT
        self.button_excel['background'] = '#fdcb6e'
        self.button_excel['command'] = self.showExcel
        self.button_excel.place(x=230, y=100, width=125, height=50)

        self.loadWord()

    def loadWord(self):
        if self.currentKanji.getKanji() == '':
            self.kanji_var.set(self.currentKanji.getHiragana())
            return
        self.kanji_var.set(self.currentKanji.getKanji())

    def nextWord(self, event=None):
        self.kanji['font'] = ('', self.FONT_KANJI)
        self.currentKanji = choice(self.listKanji)
        self.loadWord()

    def showHiragana(self):
        if self.kanjiMode:
            self.show_mode.set("Kanji")
            self.kanji_var.set(self.currentKanji.getHiragana() +
                               '\n'+self.currentKanji.getBoThu() +
                               '\n'+self.currentKanji.getMean())
            self.kanjiMode = False
            self.kanji['font'] = ('', self.FONT_HIRAGANA)
        else:
            self.kanji['font'] = ('', self.FONT_KANJI)
            self.show_mode.set('Hiragana')
            self.kanji_var.set(self.currentKanji.getKanji())
            self.kanjiMode = True

    def showExcel(self):
        tr = threading.Thread(target=lambda: os.system(self.excel_name))
        tr.start()

    def spaceDown(self, event):
        self.show_mode.set("Kanji")
        self.kanji_var.set(self.currentKanji.getHiragana() +
                            '\n'+self.currentKanji.getBoThu() +
                            '\n'+self.currentKanji.getMean())
        self.kanjiMode = False
        self.kanji['font'] = ('', self.FONT_HIRAGANA)
    
    def spaceUp(self, event):
        self.kanji['font'] = ('', self.FONT_KANJI)
        self.show_mode.set('Hiragana')
        if self.currentKanji.getKanji() == '':
            self.kanji_var.set(self.currentKanji.getHiragana())
            return
        self.kanji_var.set(self.currentKanji.getKanji())
        self.kanjiMode = True

    def loadKotoba(self):
        self.listCurrentChoice = []
        for var in range(len(self.enableCheckbox)):
            if(self.enableCheckbox[var].get()==1):
                self.listCurrentChoice.append(var+1)
        
        # load Kanji to list
        self.listKanji = []
        self.sheet = self.wb.sheet_by_index(0)
        if self.listCurrentChoice == []:
            print('show all')
            self.sheet = self.wb.sheet_by_index(0)
            self.listKanji = [Kanji(self.sheet.row_values(i))
                          for i in range(1, self.sheet.nrows)]
        else:
            print(self.listCurrentChoice)
            for i in range(1, self.sheet.nrows):
                if (self.sheet.row_values(i)[4] in self.listCurrentChoice):
                    self.listKanji.append(Kanji(self.sheet.row_values(i)))
        self.nextWord()

        


if __name__ == "__main__":
    mywindow = MyWindow()
    mywindow.mainloop()
