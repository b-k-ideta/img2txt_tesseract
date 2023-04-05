from img2txt import Img2Text
from tkinter import filedialog
from os import getcwd

# Tesseractを使った画像→テキスト変換（要Tesseract-OCRインストール）
# 精度低め
# config.iniでTesseractのパスを指定できる
# 複数の.txtか一つにまとめて.docxに出力可能


def main():

    valid_language = False
    type = [('画像', '*')]
    dir = getcwd()
    files = filedialog.askopenfilenames(
        filetypes=type, initialdir=dir, title="画像を選んでください（複数可）")
    if len(files) < 1:
        exit()
    converter = Img2Text()

    while 1:
        try:
            input_format = int(input('[0]画像の二値化をする\t[1]そのまま'))
        except:
            print("無効な入力です")
            continue
        match input_format:
            case 0:
                converter.image_thresholding_on()
            case 1:
                pass
            case _:
                print("無効な入力です")
                continue
        break

    while 1:
        try:
            input_format = int(
                input('[0]txtファイル(一つずつ出力)\t[1]docxファイル(まとめて出力)'))
        except:
            print("無効な入力です")
            continue
        match input_format:
            case 0:
                file_format = 'txt'
                converter.get_output(file_format)
            case 1:
                file_format = 'docx'
                converter.get_output(file_format)
            case _:
                print("無効な入力です")
                continue
        break

    langs = converter.get_language()
    print(langs)
    while valid_language == False:
        input_lang = input('上記から言語を選択してください\n>>>')
        if input_lang in langs:
            valid_language = True
        else:
            print("無効な入力です")

    for file in files:
        converter.process_and_dump(file, input_lang)
    if file_format == 'docx':
        converter.save_docx()
    


if __name__ == "__main__":
    main()
