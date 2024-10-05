import math
import threading
import os
import signal
import keyboard
import pyautogui
from PIL import Image
import time
from pathlib import Path
import re
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from paddleocr import PaddleOCR
import json
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QGridLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import configparser


model_path = r"ch_PP-OCRv4_rec_server_infer"
ocr = PaddleOCR(rec_model_dir=model_path, det_db_score_mode='slow')
values = []
values2 = []

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
dr = webdriver.Chrome(options=chrome_options)


def close_script():

    print("Shortcut activated. Closing the script.")
    os.kill(os.getpid(), signal.SIGINT)

keyboard.add_hotkey('num add', close_script)
class TransparentWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout1 = QGridLayout()
        self.layout2 = QGridLayout()
        self.custom_font = QFont("Helvetica", 15, QFont.Bold)
        self.layout1.setVerticalSpacing(4)
        self.layout1.setHorizontalSpacing(2)
        self.layout2.setHorizontalSpacing(2)
        self.layout2.setVerticalSpacing(4)
        self.entries1 = []
        self.entries2 = []
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setGeometry(400, -10, 200, 1)
        self.setLayout(self.layout1)
        self.show()
        self.window2 = QWidget()
        self.window2.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        self.window2.setAttribute(Qt.WA_TranslucentBackground, True)
        self.window2.setAttribute(Qt.WA_NoSystemBackground, True)
        self.window2.setGeometry(1200, -10, 200, 1)
        self.window2.setLayout(self.layout2)
        self.window2.show()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(100)

    def clear_gui(self):
        global values, values2
        values.clear()
        values2.clear()

        for entry in self.entries1:
            entry.deleteLater()
        self.entries1.clear()
        self.layout1.setRowStretch(0, 0)
        self.layout1.setColumnStretch(0, 0)

        self.resize(300, 10)

        for entry in self.entries2:
            entry.deleteLater()
        self.entries2.clear()
        self.layout2.setRowStretch(0, 0)
        self.layout2.setColumnStretch(0, 0)

        self.window2.resize(300, 10)


    def update_gui(self):

        self.layout1.setRowStretch(0, 0)
        self.layout2.setRowStretch(0, 0)

        for i, row_values in enumerate(values):
            for j, number in enumerate(row_values):
                index = i * 3 + j
                if index >= len(self.entries1):
                    entry = QLineEdit(self)
                    entry.setText(str(number))
                    entry.setFont(self.custom_font)
                    entry.setFixedSize(80, 22)
                    entry.setStyleSheet("background: transparent; border: none;")
                    self.update_entry_color(entry, j)
                    self.layout1.addWidget(entry, i, j, alignment=Qt.AlignTop)
                    self.entries1.append(entry)
                else:
                    self.entries1[index].setText(str(number))
                    self.update_entry_color(self.entries1[index], j)

        for i, row_values in enumerate(values2):
            for j, number in enumerate(row_values):
                index = i * 3 + j
                if index >= len(self.entries2):
                    entry = QLineEdit(self)
                    entry.setText(str(number))
                    entry.setFixedSize(80, 22)
                    entry.setFont(self.custom_font)
                    entry.setStyleSheet("background: transparent; border: none; color: white;")
                    self.update_entry_color(entry, j)
                    self.layout2.addWidget(entry, i, j, alignment=Qt.AlignTop)
                    self.entries2.append(entry)
                else:
                    self.entries2[index].setText(str(number))
                    self.update_entry_color(self.entries2[index], j)

        self.layout1.setRowStretch(len(values), 1)
        self.layout2.setRowStretch(len(values2), 1)

    def update_entry_color(self, entry, column):
        try:
            value = int(entry.text())
            if column == 0:
                if value < 300:
                    entry.setStyleSheet("background-color: transparent; color: #940D0D;border: none;")
                elif 300 <= value <= 449:
                    entry.setStyleSheet("background-color: transparent; color: #CD3232;border: none;")
                elif 450 <= value <= 650:
                    entry.setStyleSheet("background-color: transparent; color: #CD7A00;border: none;")
                elif 651 <= value <= 899:
                    entry.setStyleSheet("background-color: transparent; color: #CCB800;border: none;")
                elif 900 <= value <= 1199:
                    entry.setStyleSheet("background-color: transparent; color: #839C24;border: none;")
                elif 1200 <= value <= 1599:
                    entry.setStyleSheet("background-color: transparent; color: #4E7327;border: none;")
                elif 1600 <= value <= 1999:
                    entry.setStyleSheet("background-color: transparent; color: #3F99BF;border: none;")
                elif 2000 <= value <= 2449:
                    entry.setStyleSheet("background-color: transparent; color: #3A73C6;border: none;")
                elif 2450 <= value <= 2899:
                    entry.setStyleSheet("background-color: transparent; color: #7A3DB6;border: none;")
                elif value >= 2900:
                    entry.setStyleSheet("background-color: transparent; color: #6526a3;border: none;")
                else:
                    entry.setStyleSheet("background-color: transparent; color: black;")

            elif column == 1:
                if value < 45:
                    entry.setStyleSheet("background-color: transparent; color: #d10a0a;border: none;")
                elif 45 <= value <= 49:
                    entry.setStyleSheet("background-color: transparent; color: #dbaf0f;border: none;")
                elif 50 <= value <= 55:
                    entry.setStyleSheet("background-color: transparent; color: #79f00a;border: none;")
                elif 56 <= value <= 60:
                    entry.setStyleSheet("background-color: transparent; color: #3A73C6;border: none;")
                elif 61 <= value <= 64:
                    entry.setStyleSheet("background-color: transparent; color: #7A3DB6;border: none;")
                elif value > 65:
                    entry.setStyleSheet("background-color: transparent; color: #6526a3;border: none;")
                else:
                    entry.setStyleSheet("background-color: white; color: black;")

            elif column == 2:
                if value < 1000:
                    entry.setStyleSheet("background-color: transparent; color: #e6501e;border: none;")
                elif 1000 <= value <= 5000:
                    entry.setStyleSheet("background-color: transparent; color: #e6cb1e;border: none;")
                elif value > 5000:
                    entry.setStyleSheet("background-color: transparent; color: #85e80c;border: none;")
                else:
                    entry.setStyleSheet("background-color: transparent; color: black;border: none;")
        except ValueError:
            entry.setStyleSheet("background-color: transparent; color: black;")

    def hide_gui(self):
        self.hide()
        self.window2.hide()

    def show_gui(self):
        self.show()
        self.window2.show()


def hide_gui():
    global window_instance
    window_instance.hide_gui()

def show_gui():
    global window_instance
    window_instance.show_gui()

def clear_gui():
    global window_instance
    window_instance.clear_gui()

def perform_ocr_on_screenshot(screenshot_path):
    clear_gui()
    img = Image.open(screenshot_path)
    left1, top1, right1, bottom1 = 450, 320, 760, 620
    left2, top2, right2, bottom2 = 1125, 320, 1470, 620
    if battle10vs10 is True:
        left1, top1, right1, bottom1 = 450, 380, 760, 780
        left2, top2, right2, bottom2 = 1125, 380, 1470, 780
    img_cropped1 = img.crop((left1, top1, right1, bottom1))
    img_cropped1.save('cropped1.png')
    img_cropped2 = img.crop((left2, top2, right2, bottom2))
    img_cropped2.save('cropped2.png')

    result = ocr.ocr('cropped1.png', cls=True)
    result2 = ocr.ocr('cropped2.png', cls=True)

    nicknames = []
    for outer_list in result:
        for inner_list in outer_list:
            for item in inner_list:
                if isinstance(item, tuple) and isinstance(item[1], float):
                    name = item[0]
                    nicknames.append(name)
    for outer_list in result2:
        for inner_list in outer_list:
            for item in inner_list:
                if isinstance(item, tuple) and isinstance(item[1], float):
                    name = item[0]
                    nicknames.append(name)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = Path('./OCRoutput')
    save_path.mkdir(parents=True, exist_ok=True)
    output_file = save_path / f"output_{timestamp}.txt"

    with output_file.open("w", encoding='utf-8') as f:
        cleaned_nicknames = [re.sub(r'&', 'l', re.sub(r'=', 'I', re.sub(r'\?', '_', re.sub(r'\+', '0', re.sub(r'<', 'O', re.sub(r'>', 'o', nick)))))).strip() for nick in nicknames]
        f.write("\n".join(cleaned_nicknames))

    print(f"OCR completed and saved to {output_file}")
    process_file(output_file)

def process_file(file_path):
    with open(file_path, "r") as file:
        nicknames = file.read().splitlines()

    for nick in nicknames:
        get_player_stat(nick)

def get_player_id(nick):
    try:
        url = f"https://api.wotblitz.{region}/wotb/account/list/?application_id=e8ed145797b5db58934cc1bb98a2bc6a&search={nick}&type=exact"
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, headers=headers)
        res = json.loads(response.content)
        player_id = res['data'][0]['account_id']
        return player_id
    except Exception as e:
        player_id = None
        print(e)


def get_player_stat(nick):
    numberofplayers = 7 if battle10vs10 is False else 10
    ID = get_player_id(nick)
    print(ID)
    url = 'https://www.blitzstars.com/api/top/playersbyclan'
    data = {'memberIds': f'{ID}'}
    response = requests.post(url, data=data)
    res = json.loads(response.content)
    print(res)
    if len(res) != 0 and response.status_code != 500:
        winPercent = math.trunc(res[0]['statistics']['special']['winrate'])
        battles = res[0]['statistics']['all']['battles']
        wn8 = math.trunc(res[0]['statistics']['wn8'])
        stat_list = [wn8, winPercent, battles]
        if len(values) < numberofplayers:
            values.append(stat_list)
        else:
            values2.append(stat_list)
    elif ID is None:
        stat_list = [0, 0, 0]
        if len(values) < numberofplayers:
            values.append(stat_list)
        else:
            values2.append(stat_list)
    else:
        url2 = f"https://www.blitzstars.com/player/{region}/{nick}"
        dr.get(url2)
        time.sleep(1)
        bs = BeautifulSoup(dr.page_source, 'html.parser')
        mydivs = bs.find_all("div", "wn8-span")
        mywins = bs.find_all("p", "ps-cell ps-c ng-binding")
        wn8 = mydivs[4].get_text()
        wn8_clear = re.sub(r'\D', '', wn8)
        winPercent = mywins[0].get_text()
        winPercent = winPercent[:-5]
        battleCount = mywins[2].get_text()
        battle_count_clear = re.sub(r'\D', '', battleCount)
        stat_list = [wn8_clear, winPercent, battle_count_clear]
        if len(values) < numberofplayers:
            values.append(stat_list)
        else:
            values2.append(stat_list)
    print(f"Stats for player {nick}: {stat_list}")

def check_for_image_and_capture():
    image_paths = ["./img/fun.png", "./img/rating.png", "./img/regular.png"]
    screenshot_folder = Path("./screenshots")
    if not screenshot_folder.exists():
        screenshot_folder.mkdir(parents=True, exist_ok=True)
    region = (883, 200, 150, 190)

    while True:
        try:
            found_image = None
            for image_path in image_paths:
                try:
                    location = pyautogui.locateOnScreen(image_path, region=region, confidence=0.8)
                    if location:
                        found_image = image_path
                        break
                except pyautogui.ImageNotFoundException:
                    continue

            if found_image is not None:
                print("Image found, waiting for it to disappear")
                while True:
                    time.sleep(0.25)
                    try:
                        pyautogui.locateOnScreen(image_path, region=region, confidence=0.8)
                        time.sleep(0.25)
                    except Exception as e:
                        time.sleep(3)
                        print("Image disappeared, capturing screenshot...")
                        show_gui()
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        screenshot_path = screenshot_folder / f"screenshot_{timestamp}.png"
                        pyautogui.screenshot(screenshot_path)
                        perform_ocr_on_screenshot(screenshot_path)
                        window_instance.after(40000, clear_gui())
                        break

            time.sleep(0.5)
        except Exception as e:
            print("Image not found in the region. Retrying")
            time.sleep(0.125)

def start_image_monitoring_thread():
    threading.Thread(target=check_for_image_and_capture, daemon=True).start()
class ScreenshotHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        else:
            print(f"New screenshot detected: {event.src_path}")
            show_gui()
            time.sleep(1)
            perform_ocr_on_screenshot(event.src_path)

def monitor_screenshots_folder(folder_path):
    event_handler = ScreenshotHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()
    print(f"Monitoring folder: {folder_path}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def load_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)

    region = config.get('settings', 'region')
    battle10vs10 = config.getboolean('settings', 'battle10vs10')
    return region, battle10vs10


if __name__ == "__main__":
    app = QApplication([])
    config_file = 'config.ini'
    region, battle10vs10 = load_config(config_file)
    screenshots_folder = Path("./screenshotsmanual")
    if not screenshots_folder.exists():
        screenshots_folder.mkdir(parents=True, exist_ok=True)
    threading.Thread(target=monitor_screenshots_folder, args=(screenshots_folder,)).start()
    start_image_monitoring_thread()
    window_instance = TransparentWindow()
    window_instance.show()
    app.exec_()
    keyboard.wait()
