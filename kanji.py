import logging
from urllib.request import urlretrieve

class Kanji:
    """Class này đại diện cho 1 từ Kanji vì mình học tiếng Nhật, nó tham chiếu đường dẫn của file âm thanh tới file được lưu
    trong một folder, và mình đéo biết nến lưu nó ở folder nào :D"""
    
    ROOT = 'http://jls.vnjpclub.com/'
    SOUNDS_FOLDER = 'sounds/'

    def __init__(self, kanji: str, hiragana: str, han_viet: str, mean: str, bai: str, sound_url: str, sound_path:str) -> None:
        self.kanji = kanji
        self.hiragana = hiragana
        self.bo_thu = han_viet
        self.mean = mean
        self.bai = bai
        self.sound_url = sound_url
        self.sound_path = sound_path

    def getKanji(self):
        return self.kanji

    def getHiragana(self):
        return self.hiragana

    def getHanViet(self):
        return self.bo_thu

    def getMean(self):
        return self.mean

    def getBai(self):
        return self.bai

    def getSoundURL(self):
        """Get full sound file url"""
        return self.sound_url

    def getSoundPath(self):
        """Get full path"""
        return self.sound_path

    def getSoundFileName(self) -> str:
        return self.sound_url.replace('\\','_')


    def downloadSound(self) -> None:
        logging.info(self.getSoundURL())
        urlretrieve(self.getSoundURL(), self.getSoundPath())
        
