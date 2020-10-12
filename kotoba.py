from typing import List
from bs4 import BeautifulSoup
import requests
from main import Kanji
from urllib.request import urlretrieve
import xlwt


URL  = 'http://jls.vnjpclub.com/tu-vung-minna-no-nihongo-bai-{}.html'
ROOT = 'http://jls.vnjpclub.com/'


def getListKanji(bai: int) -> List[Kanji]:
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
        bai = str(bai)
        try:
            sound_url = tr(class_='sm2_button')[0]['href']
        except:
            sound_url = ''
        listKanji.append(Kanji(kanji, hiragana, han_viet, mean, bai, sound_url))
    return listKanji


def toExcelFile(f: str, k: List[Kanji]):
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
        sheet.write(i+1,0, k[i].getKanji())
        sheet.write(i+1,1, k[i].getHiragana())
        sheet.write(i+1,2, k[i].getHanViet())
        sheet.write(i+1,3, k[i].getMean())
        sheet.write(i+1,4, k[i].getBai())
        sheet.write(i+1,5, k[i].getSoundURL())
        sheet.write(i+1,6, k[i].getSoundPath())
    workbook.save(f)

if __name__ == "__main__":
    listKanji = []
    for i in range(1,51):
        listKanji += getListKanji(i)
    toExcelFile('excel_kanji.xls',listKanji)
    # a = getListKanji(2)[1]
    # print(a.getSoundPath())
    # print(a.getSoundURL())
