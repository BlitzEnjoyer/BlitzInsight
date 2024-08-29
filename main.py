import threading
import tkinter as tk
from tkinter import font
import keyboard
import os
import signal
from PIL import Image
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from paddleocr import PaddleOCR
from time import sleep

ocr = PaddleOCR()

values = []
values2 = []

def close_script():

    print("Shortcut activated. Closing the script.")
    os.kill(os.getpid(), signal.SIGINT)

def clear_gui():
    global values, values2
    values.clear()
    values2.clear()

    for entry in entries1:
        entry.destroy()
    entries1.clear()

    for entry in entries2:
        entry.destroy()
    entries2.clear()

keyboard.add_hotkey('num add', close_script)

def set_window_size_and_position(window, width, height, x, y):
    window.geometry(f"{width}x{height}+{x}+{y}")

def perform_ocr_on_screenshot(screenshot_path):
    clear_gui()
    img = Image.open(screenshot_path)

    left1, top1, right1, bottom1 = 450, 360, 680, 660
    left2, top2, right2, bottom2 = 1230, 360, 1470, 660
    img_cropped1 = img.crop((left1, top1, right1, bottom1))
    img_cropped1.save('cropped1.png')
    img_cropped2 = img.crop((left2, top2, right2, bottom2))
    img_cropped2.save('cropped2.png')
    img_path1 = 'cropped1.png'
    img_path2 = 'cropped2.png'

    result = ocr.ocr(img_path1, cls=True)
    result2 = ocr.ocr(img_path2, cls=True)

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
    save_path = Path('./dane')
    save_path.mkdir(parents=True, exist_ok=True)
    output_file = save_path / f"output_{timestamp}.txt"

    with output_file.open("w") as f:
        cleaned_nicknames = [re.sub(r'[(\[{<][^)\]}|>]*[)\]}|>]', '', nick).strip() for nick in nicknames]
        f.write("\n".join(cleaned_nicknames))

    print(f"OCR completed and saved to {output_file}")
    process_file(output_file)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
dr = webdriver.Chrome(options=chrome_options)

def update_entry_color(entry):
    try:
        value = int(entry.get())
        if value < 300:
            entry.config(bg="#940D0D", fg="white")
        elif 300 <= value <= 449:
            entry.config(bg="#CD3232", fg="white")
        elif 450 <= value <= 650:
            entry.config(bg="#CD7A00", fg="white")
        elif 651 <= value <= 899:
            entry.config(bg="#CCB800", fg="white")
        elif 900 <= value <= 1199:
            entry.config(bg="#839C24", fg="white")
        elif 1200 <= value <= 1599:
            entry.config(bg="#4E7327", fg="white")
        elif 1600 <= value <= 1999:
            entry.config(bg="#3F99BF", fg="white")
        elif 2000 <= value <= 2449:
            entry.config(bg="#3A73C6", fg="white")
        elif 2450 <= value <= 2899:
            entry.config(bg="#7A3DB6", fg="white")
        elif value >= 2900:
            entry.config(bg="#7A3DB6", fg="white")
        else:
            entry.config(bg="white", fg="black")
    except ValueError:
        entry.config(bg="white", fg="black")

entries1 = []
entries2 = []
root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)

window2 = tk.Toplevel(root)
window2.overrideredirect(True)
window2.attributes("-topmost", True)
custom_font = font.Font(family="Helvetica", size=12, weight="bold")
set_window_size_and_position(root, 300, 200, 400, 1)
set_window_size_and_position(window2, 300, 200, 1200, 1)

def update_gui():
    for i, row_values in enumerate(values):
        for j, number in enumerate(row_values):
            index = i * 3 + j
            if index >= len(entries1):
                entry = tk.Entry(root, width=10, font=custom_font)
                entry.grid(row=i, column=j, padx=5, pady=2)
                entry.insert(0, str(number))
                if j == 0:
                    update_entry_color(entry)
                entries1.append(entry)
            else:
                entries1[index].delete(0, tk.END)
                entries1[index].insert(0, str(number))
                if j == 0:
                    update_entry_color(entries1[index])

    for i, row_values in enumerate(values2):
        for j, number in enumerate(row_values):
            index = i * 3 + j
            if index >= len(entries2):
                entry = tk.Entry(window2, width=10, font=custom_font)
                entry.grid(row=i, column=j, padx=5, pady=2)
                entry.insert(0, str(number))
                if j == 0:
                    update_entry_color(entry)
                entries2.append(entry)
            else:
                entries2[index].delete(0, tk.END)
                entries2[index].insert(0, str(number))
                if j == 0:
                    update_entry_color(entries2[index])

    root.after(100, update_gui)

def get_player_stat(nick):
    try:
        url = f"https://www.blitzstars.com/player/eu/{nick}"
        dr.get(url)
        sleep(1)
        bs = BeautifulSoup(dr.page_source, 'html.parser')
        mydivs = bs.find_all("div", "wn8-span")
        mywins = bs.find_all("p", "ps-cell ps-c ng-binding")
        wn8 = mydivs[4].get_text()
        wn8_clear = re.sub(r'\D', '', wn8)
        winPercent = mywins[0].get_text()
        battleCount = mywins[2].get_text()
        battle_count_clear = re.sub(r'\D', '', battleCount)
        stat_list = [wn8_clear, winPercent, battle_count_clear]

        if len(values) < 7:
            values.append(stat_list)
        else:
            values2.append(stat_list)

        print(f"Stats for player {nick}: {stat_list}")
    except Exception as e:
        print(f"Error scraping {nick}: {e}")
        stat_list = [0, 0, 0]
        if len(values) < 7:
            values.append(stat_list)
        else:
            values2.append(stat_list)

def process_file(file_path):
    with open(file_path, "r") as file:
        nicknames = file.read().splitlines()

    for nick in nicknames:
        get_player_stat(nick)

class ScreenshotHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        else:
            print(f"New screenshot detected: {event.src_path}")
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

if __name__ == "__main__":
    screenshots_folder = Path("./screenshots")

    if not os.path.exists(screenshots_folder):
        os.makedirs(screenshots_folder)

    threading.Thread(target=monitor_screenshots_folder, args=(screenshots_folder,)).start()

    root.after(100, update_gui)
    root.mainloop()

    keyboard.wait()
