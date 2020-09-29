from tkinter import StringVar, Tk, Label, Button, Frame, FLAT
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

    def getKanji(self):
        return self.kanji

    def getHiragana(self):
        return self.hiragana

    def getBoThu(self):
        return self.bo_thu

    def getMean(self):
        return self.mean


class MyWindow(Tk):

    def __init__(self) -> None:
        super().__init__()
        self.title("Help you pro Kanji")
        self.resizable(False, False)
        self.geometry('715x150')

        self.excel_name = 'excel_kanji.xlsx'
        if os.path.exists(self.excel_name)==False:
            print('Có vẻ như không tồn tại file excel với tên '+self.excel_name +
                  ', nếu bạn đã tạo một file excel thì hãy xem thử tên của nó đã đúng là '+self.excel_name+' hay chưa, sau đó chạy lại chương trình')
            exit()
        self.wb = xlrd.open_workbook(self.excel_name)
        self.sheet = self.wb.sheet_by_index(0)
        self.listKanji = [Kanji(self.sheet.row_values(i))
                          for i in range(1, self.sheet.nrows)]

        self.currentKanji = choice(self.listKanji)
        self.kanjiMode = True
        self.setupUI()

    def setupUI(self):

        self.kanji_var = StringVar(self)
        self.kanji = Label(master=self, text='漢字', font=(
            '', 50), textvariable=self.kanji_var)
        self.kanji['background'] = '#74b9ff'
        self.kanji.place(x=0, y=0, width=590, height=150)

        self.button_next = Button(master=self, text='Từ khác')
        self.button_next['relief'] = FLAT
        self.button_next['background'] = '#fab1a0'
        self.button_next['command'] = self.nextWord
        self.button_next.place(x=590, y=0, width=125, height=50)

        self.show_mode = StringVar(master=self, value='Hiragana')
        self.button_hiragana = Button(master=self, textvariable=self.show_mode)
        self.button_hiragana['relief'] = FLAT
        self.button_hiragana['background'] = '#e17055'
        self.button_hiragana['command'] = self.showHiragana
        self.button_hiragana.place(x=590, y=50, width=125, height=50)

        self.button_excel = Button(master=self, text='Excel')
        self.button_excel['relief'] = FLAT
        self.button_excel['background'] = '#fdcb6e'
        self.button_excel['command'] = self.showExcel
        self.button_excel.place(x=590, y=100, width=125, height=50)

        self.loadWord()

    def loadWord(self):
        self.kanji_var.set(self.currentKanji.getKanji())

    def nextWord(self):
        self.kanji['font'] = ('', 50)
        self.currentKanji = choice(self.listKanji)
        self.loadWord()

    def showHiragana(self):
        if self.kanjiMode:
            self.show_mode.set("Kanji")
            self.kanji_var.set(self.currentKanji.getHiragana() +
                               '\n'+self.currentKanji.getBoThu() +
                               '\n'+self.currentKanji.getMean())
            self.kanjiMode = False
            self.kanji['font'] = ('', 12)
        else:
            self.kanji['font'] = ('', 50)
            self.show_mode.set('Hiragana')
            self.kanji_var.set(self.currentKanji.getKanji())
            self.kanjiMode = True

    def showExcel(self):
        tr = threading.Thread(target=lambda: os.system(self.excel_name))
        tr.start()


if __name__ == "__main__":
    mywindow = MyWindow()
    mywindow.mainloop()
