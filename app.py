import PySide6
from PySide6.QtWidgets import (QApplication,
                               QWidget,
                               QLabel,
                               QPushButton,
                               QLineEdit,
                               QFileDialog)

import os
import sys

import argparse
from dl_mv import download_youtube

# PySide6のアプリ本体（ユーザがコーディングしていく部分）
class MainWindow(QWidget):
    # main
    def __init__(self, parent=None):
        # 親クラスの初期化
        super().__init__(parent)
        
        # ウィンドウタイトル
        self.setWindowTitle("ダウンロード")
        
        # ウィンドウサイズ
        win_width = 650
        win_hegiht = 200
        self.resize(win_width, win_hegiht)
        
        # ラベルの表示
        self.SetLabel()
        
        # ボタンの表示
        self.SetButoon()
        
        # 入力欄の表示
        self.SetLineedit()

    #　ラベル メソッド
    def SetLabel(self):
        label = QLabel(self)
        label_dir = QLabel(self)
        
        # ラベルの見た目をQt Style Sheetで設定
        labelStyle = """QLabel {
            color:            #000000;  /* 文字色 */
            font-size:        16px;     /* 文字サイズ */
        }"""
        
        label.setStyleSheet(labelStyle)
        label_dir.setStyleSheet(labelStyle)
        
        label.setText("動画のURL :")
        label.move(35, 45)
        
        label_dir.setText("保存先 :")
        label_dir.move(35, 90)
    
    # ボタン メソッド
    def SetButoon(self):
        button = QPushButton(self)
        button.move(250, 135)
        button.setText("ダウンロード")
        
        button_dir = QPushButton(self)
        button_dir.move(500, 90)
        button_dir.setText("...")
        
        # ボタンのクリックによる実行処理
        button.pressed.connect(lambda: self.CallbackButtonPressed(self.lineEdit.text(), self.lineEdit_dir.text()))
        button_dir.pressed.connect(self.get_file_path)
        
        # ボタンを離した時に、実行される処理
        # button.released.connect(lambda: self.CallbackButtonReleased(90))  
    
    # ボタン　クリック　メソッド
    def CallbackButtonPressed(self, url, dir):
        print( url + "が入力されました。")
        
        parser = argparse.ArgumentParser(description='YouTubeの動画をダウンロードし、音声を分離します。')
        parser.add_argument('--url', '-i', type=str, help='YouTubeの動画URL')
        parser.add_argument('--output-dir', '-o', type=str, default='./movie', help='出力先ディレクトリ')

        args = parser.parse_args()
        if dir:
            download_youtube(url, dir)
        else:
            download_youtube(url, args.output_dir)
        
    #Inputの入力欄　メソッド
    def SetLineedit(self):
        self.lineEdit = QLineEdit(self)
        self.lineEdit.move(150, 45)
        self.lineEdit.resize(375, 25)
        
        self.lineEdit_dir = QLineEdit(self)
        self.lineEdit_dir.move(150, 90)
        self.lineEdit_dir.resize(325, 25)
        
        self.lineEdit.textChanged.connect(self.CallbaclReturnpressedLineedit)
        self.lineEdit_dir.textChanged.connect(self.CallbaclReturnpressedLineeditDir)
    
    #Inputのテキスト変更時　処理
    def CallbaclReturnpressedLineedit(self):
        print("テキストが変更されました。")
        
    def CallbaclReturnpressedLineeditDir(self):
        print("ディレクトリが変更されました。")

    def get_file_path(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        
        if dialog.exec():
            selected_files = dialog.selectedFiles()
            if selected_files:
                self.change_text(selected_files[0])
        return None
    
    def change_text(self, text):
        self.lineEdit_dir.setText(text)
        
        
        
        
if __name__ == "__main__":
    # 環境変数にPySide6を登録
    dirname = os.path.dirname(PySide6.__file__)
    plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
    
    app = QApplication(sys.argv)    # PySide6の実行
    window = MainWindow()           # ユーザがコーディングしたクラス
    window.show()                   # PySide6のウィンドウを表示
    sys.exit(app.exec())            # PySide6の終了