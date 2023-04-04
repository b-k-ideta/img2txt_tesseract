import pytesseract as tess
import cv2
from configparser import ConfigParser
import docx
import os


class Img2Text:

    def __init__(self) -> None:
        self.__config_ini = ConfigParser()
        self.__config_ini.read('.\\config\\config.ini')
        tess.pytesseract.tesseract_cmd = self.__config_ini.get(
            'Tesseract', 'path')
        self.__processed_img_number = 0
        self.__output = ''
        self.__img_threshold = False
        self.__current_dir = os.getcwd()

    def process_and_dump(self, img_path: str, lang_setting='jpn'):
        img_file = img_path
        img = cv2.imread(img_file)

        if self.__img_threshold == True:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            img = cv2.adaptiveThreshold(
                img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

        ocr_result = tess.image_to_string(img, lang=lang_setting)
        ocr_result = str(ocr_result).replace(" ", "").replace("　", "")

        match self.__output:
            case 'txt':
                self.__processed_img_number += 1
                self.__create_dump_folder()
                filename = self.__current_dir+"\\dump\\processed-" + \
                    (str(self.__processed_img_number).zfill(4))
                with open(filename+'.txt', mode='w', encoding='utf-8') as f:
                    f.writelines(ocr_result)
            case 'docx':
                processed_txt = ''
                for i in ocr_result.splitlines():
                    if len(i) == 0:
                        processed_txt += '\n'
                    else:
                        processed_txt += i
                self.__document.add_paragraph(processed_txt, style='Normal')
                self.__document.add_page_break()

    def get_language(self):
        return tess.get_languages()

    def image_thresholding_on(self):
        self.__img_threshold = True

    def get_output(self, mode='txt'):
        match mode:
            case 'txt':
                self.__output = 'txt'
            case 'docx':
                self.__output = 'docx'
                self.__document = docx.Document()

    def save_docx(self):
        # file_path = self.__current_dir+'\\dump\\'
        self.__create_dump_folder()
        self.__document.save('./dump/processed.docx')

    def __create_dump_folder(self):
        if not os.path.exists(self.__current_dir+"\\dump"):
            os.makedirs(self.__current_dir+"\\dump")
