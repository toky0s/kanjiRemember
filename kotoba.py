from typing import List
from bs4 import BeautifulSoup
import main
import requests
import xlwt
import os


URL  = 'http://jls.vnjpclub.com/tu-vung-minna-no-nihongo-bai-{}.html'

def runFirst():
    # Check folder when this script runs
    if os.path.exists(main.SOUNDS_FOLDER) == False:
        os.mkdir(main.SOUNDS_FOLDER)


def getListKanji(bai: int) -> List:
    r = requests.get(URL.format(bai))
    soup = BeautifulSoup(r.text, 'lxml')
    tbody = soup.select("#khungchinhgiua > table > tbody")[0]
    # all row in table
    listKanji = []
    for tr in tbody('tr'):
        hiragana = tr.td.string
        kanji = tr('td')[4].string
        han_viet = tr('td')[5].string
        mean = tr('td')[6].string
        try:
            sound_url = main.ROOT + str(tr(class_='sm2_button')[0]['href']).replace('\\','/')
            sound_path = main.SOUNDS_FOLDER + str(tr(class_='sm2_button')[0]['href']).replace('\\','_')
        except:
            sound_url = ''
            sound_path = ''
        listKanji.append({'kanji':kanji, 'hiragana':hiragana,'han_viet':han_viet,'nghia':mean, 'bai':bai,'sound_url':sound_url, 'sound_path':sound_path})
    return listKanji


def toExcelFile(f: str, k: List):
    workbook = xlwt.Workbook()  
    sheet = workbook.add_sheet("Kotoba") 

    # Writing on specified sheet 
    sheet.write(0,0, 'KANJI')
    sheet.write(0,1, 'HIRAGANA')
    sheet.write(0,2, 'HÁN VIỆT')
    sheet.write(0,3, 'NGHĨA')
    sheet.write(0,4, 'BÀI')
    sheet.write(0,5, 'SOUND URL')
    sheet.write(0,6, 'SOUND PATH')

    for i in range(len(k)):
        sheet.write(i+1,0, k[i]['kanji'])
        sheet.write(i+1,1, k[i]['hiragana'])
        sheet.write(i+1,2, k[i]['han_viet'])
        sheet.write(i+1,3, k[i]['nghia'])
        sheet.write(i+1,4, k[i]['bai'])
        sheet.write(i+1,5, k[i]['sound_url'])
        sheet.write(i+1,6, k[i]['sound_path'])
    workbook.save(f)


if __name__ == "__main__":
    runFirst()
    listKanji = []
    for i in range(1,51):
        listKanji += getListKanji(i)
    toExcelFile(main.EXCEL_NAME, listKanji)

