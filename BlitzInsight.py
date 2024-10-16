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
api_call_count = 0
with open('tankaverages.json', 'r') as file:
    tank_avg_file = json.load(file)

tank_avg = [
    {
        "tank_id": tank["tank_id"],
        "winrate_avg": tank["special"]["winrate"],
        "damagePerBattle_avg": tank["special"]["damagePerBattle"],
        "killsPerBattle_avg": tank["special"]["killsPerBattle"],
        "spotsPerBattle_avg": tank["special"]["spotsPerBattle"],
        "dropped_capture_points_avg": tank["all"]["dropped_capture_points"] / tank["all"]["battles"]
    }
    for tank in tank_avg_file
]


def getPlayerTanksData(playerID):
    url = f"https://api.wotblitz.{region}/wotb/tanks/stats/?application_id=e8ed145797b5db58934cc1bb98a2bc6a&account_id={playerID}"
    start_time = time.time()
    response = requests.get(url)
    res = json.loads(response.content)
    tanks_data = [
        {
            "tank_id": tank["tank_id"],
            "battles": tank["all"]["battles"],
            "damage_dealt_avg": tank["all"]["damage_dealt"] / tank["all"]["battles"] if tank["all"]["damage_dealt"] > 0 else 0,
            "spotted_avg": tank["all"]["spotted"] / tank["all"]["battles"] if tank["all"]["spotted"] > 0 else 0,
            "dropped_capture_points_avg": tank["all"]["dropped_capture_points"] / tank["all"]["battles"] if tank["all"]["dropped_capture_points"] > 0 else 0,
            "frags_avg": tank["all"]["frags"] / tank["all"]["battles"] if tank["all"]["frags"] > 0 else 0,
            "winrate": (tank["all"]["wins"] / tank["all"]["battles"]) * 100 if tank["all"]["battles"] > 0 else 0
        }
        for tank in res["data"][str(playerID)]
    ]
    end_time = time.time()
    print(f"getPlayerTanksData executed in {end_time - start_time:.4f} seconds")
    return tanks_data

def calcWN8(tankid, tanks_data):
    tankid = int(tankid)
    tank_data = next((tank for tank in tanks_data if tank["tank_id"] == tankid), None)
    tank_avg_data = next((tank for tank in tank_avg if tank["tank_id"] == tankid), None)
    if tank_data is None:
        print(f"Warning: No data found for tank ID {tankid} in player data.")
        return 0, tankid, 0, 0

    if tank_avg_data is None:
        print(f"Warning: No average data found for tank ID {tankid}.")
        return 0, tankid, 0, 0
    tankBattles = tank_data["battles"]
    tankwinrate = tank_data["winrate"]

    rDAMAGE = tank_data["damage_dealt_avg"] / tank_avg_data["damagePerBattle_avg"]
    rSPOT = tank_data["spotted_avg"] / tank_avg_data["spotsPerBattle_avg"]
    rFRAG = tank_data["frags_avg"] / tank_avg_data["killsPerBattle_avg"]
    rDEF = tank_data["dropped_capture_points_avg"] / tank_avg_data["dropped_capture_points_avg"]
    rWIN = tank_data["winrate"] / tank_avg_data["winrate_avg"]
    rWINc = max(0, (rWIN - 0.71) / (1 - 0.71))
    rDAMAGEc = max(0, (rDAMAGE - 0.22) / (1 - 0.22))
    rFRAGc = max(0, min(rDAMAGEc + 0.2, (rFRAG - 0.12) / (1 - 0.12)))
    rSPOTc = max(0, min(rDAMAGEc + 0.1, (rSPOT - 0.38) / (1 - 0.38)))
    rDEFc = max(0, min(rDAMAGEc + 0.1, (rDEF - 0.10) / (1 - 0.10)))
    WN8 = 980 * rDAMAGEc + 210 * rDAMAGEc * rFRAGc + 155 * rFRAGc * rSPOTc + 75 * rDEFc * rFRAGc + 145 * min(1.8, rWINc)
    return WN8, tankid, tankBattles, tankwinrate

def playerWN8(player_id):
    tanks_data = getPlayerTanksData(player_id)

    wn8all, battlesall, winrateall = 0, 0, 0
    for tank in tanks_data:
        stats = calcWN8(tank["tank_id"], tanks_data)
        wn8all += stats[0] * stats[2]
        winrateall += stats[3] * stats[2]
        battlesall += stats[2]

    playerWN8 = wn8all / battlesall if battlesall > 0 else 0
    playerWinrate = winrateall / battlesall if battlesall > 0 else 0
    stats = round(playerWN8), round(playerWinrate), battlesall
    return stats


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
            if len(row_values) == 4:
                from_period = row_values[3]
            else:
                from_period = False
            for j, number in enumerate(row_values[:3]):
                index = i * 3 + j
                if index >= len(self.entries1):
                    entry = QLineEdit(self)
                    entry.setText(str(number))
                    entry.setFont(self.custom_font)
                    entry.setFixedSize(80, 22)
                    entry.setStyleSheet("background: transparent; border: none;")
                    self.update_entry_color(entry, j, from_period)
                    self.layout1.addWidget(entry, i, j, alignment=Qt.AlignTop)
                    self.entries1.append(entry)
                else:
                    self.entries1[index].setText(str(number))
                    self.update_entry_color(self.entries1[index], j, from_period)

        for i, row_values in enumerate(values2):
            if len(row_values) == 4:
                from_period = row_values[3]
            else:
                from_period = False
            for j, number in enumerate(row_values[:3]):
                index = i * 3 + j
                if index >= len(self.entries2):
                    entry = QLineEdit(self)
                    entry.setText(str(number))
                    entry.setFixedSize(80, 22)
                    entry.setFont(self.custom_font)
                    entry.setStyleSheet("background: transparent; border: none; color: white;")
                    self.update_entry_color(entry, j, from_period)
                    self.layout2.addWidget(entry, i, j, alignment=Qt.AlignTop)
                    self.entries2.append(entry)
                else:
                    self.entries2[index].setText(str(number))
                    self.update_entry_color(self.entries2[index], j, from_period)

        self.layout1.setRowStretch(len(values), 1)
        self.layout2.setRowStretch(len(values2), 1)

    def update_entry_color(self, entry, column, from_period):
        try:
            value = int(entry.text())
            border_style = "border: 1px solid red;" if from_period else "border: none;"
            if column == 0:
                if value <= 300:
                    entry.setStyleSheet(f"background-color: transparent; color: #940D0D;{border_style}")
                elif 300 <= value <= 449:
                    entry.setStyleSheet(f"background-color: transparent; color: #CD3232;{border_style}")
                elif 450 <= value <= 650:
                    entry.setStyleSheet(f"background-color: transparent; color: #CD7A00;{border_style}")
                elif 651 <= value <= 899:
                    entry.setStyleSheet(f"background-color: transparent; color: #CCB800;{border_style}")
                elif 900 <= value <= 1199:
                    entry.setStyleSheet(f"background-color: transparent; color: #839C24;{border_style}")
                elif 1200 <= value <= 1599:
                    entry.setStyleSheet(f"background-color: transparent; color: #4E7327;{border_style}")
                elif 1600 <= value <= 1999:
                    entry.setStyleSheet(f"background-color: transparent; color: #3F99BF;{border_style}")
                elif 2000 <= value <= 2449:
                    entry.setStyleSheet(f"background-color: transparent; color: #3A73C6;{border_style}")
                elif 2450 <= value <= 2899:
                    entry.setStyleSheet(f"background-color: transparent; color: #7A3DB6;{border_style}")
                elif value >= 2900:
                    entry.setStyleSheet(f"background-color: transparent; color: #6526a3;{border_style}")
                else:
                    entry.setStyleSheet("background-color: transparent; color: black;")

            elif column == 1:
                if value <= 45:
                    entry.setStyleSheet(f"background-color: transparent; color: #d10a0a;{border_style}")
                elif 45 <= value <= 49:
                    entry.setStyleSheet(f"background-color: transparent; color: #dbaf0f;{border_style}")
                elif 50 <= value <= 55:
                    entry.setStyleSheet(f"background-color: transparent; color: #79f00a;{border_style}")
                elif 56 <= value <= 60:
                    entry.setStyleSheet(f"background-color: transparent; color: #3A73C6;{border_style}")
                elif 61 <= value <= 64:
                    entry.setStyleSheet(f"background-color: transparent; color: #7A3DB6;{border_style}")
                elif value >= 65:
                    entry.setStyleSheet(f"background-color: transparent; color: #6526a3;{border_style}")
                else:
                    entry.setStyleSheet("background-color: white; color: black;")

            elif column == 2:
                if value <= 1000:
                    entry.setStyleSheet(f"background-color: transparent; color: #e6501e;{border_style}")
                elif 1000 <= value <= 5000:
                    entry.setStyleSheet(f"background-color: transparent; color: #e6cb1e;{border_style}")
                elif value >= 5000:
                    entry.setStyleSheet(f"background-color: transparent; color: #85e80c;{border_style}")
                else:
                    entry.setStyleSheet(f"background-color: transparent; color: black;{border_style}")
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
    timer = threading.Timer(timerconf, clear_gui)
    timer.start()
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
    if len(res) != 0 and response.status_code != 500 and res[0].get('period90d') != None and res[0]['period90d']['all']['battles'] >= 30:
        winPercent = math.trunc(res[0]['period90d']['special']['winrate'])
        battles = res[0]['period90d']['all']['battles']
        wn8 = math.trunc(res[0]['period90d']['wn8'])
        stat_list = [wn8, winPercent, battles, True]
        if len(values) < numberofplayers:
            values.append(stat_list)
        else:
            values2.append(stat_list)
    elif ID is None:
        stat_list = [0, 0, 0, False]
        if len(values) < numberofplayers:
            values.append(stat_list)
        else:
            values2.append(stat_list)
    else:
        stat_list = playerWN8(ID)
        stat_list = stat_list + (False,)
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
                        break

            time.sleep(0.125)
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
    timer = config.getfloat('settings', 'timer')
    return region, battle10vs10, timer


if __name__ == "__main__":
    app = QApplication([])
    config_file = 'config.ini'
    region, battle10vs10, timerconf = load_config(config_file)
    screenshots_folder = Path("./screenshotsmanual")
    if not screenshots_folder.exists():
        screenshots_folder.mkdir(parents=True, exist_ok=True)
    threading.Thread(target=monitor_screenshots_folder, args=(screenshots_folder,)).start()
    start_image_monitoring_thread()
    window_instance = TransparentWindow()
    window_instance.show()
    app.exec_()
    keyboard.wait()