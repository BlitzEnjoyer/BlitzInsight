# BlitzGauge

## Description
Stats for WOT Blitz. PC only.

## Prerequisites
Ensure that the following are installed on your system:

- **Python 3.x**: [Download Python](https://www.python.org/downloads/)
- **pip**: Python package installer (comes with Python)
- **(Optional)** **Software for screenshots management**: For example, [Greenshot](https://getgreenshot.org). Screenshots should be saved to the **screenshotsmanual** folder within the project directory.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/SuperMetalBeast/BlitzGauge.git
   cd BlitzGauge
2. **Create and activate a virtual environment**
    ```bash
    py -m venv venv
    venv\Scripts\activate
3. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
4. **Change the game files:**

This is essential to work. To access local files - Right-click World of Tanks Blitz in the list of games in the Steam client, then select the "Manage" item in the context menu and then "Browse local files"
   1. Insert **WarHeliosCondCBoldA** to \World of Tanks Blitz\Data\Fonts folder.
   2. Insert **FontsFs** to \World of Tanks Blitz\Data\UI\Screens folder.
   3. Insert **BattleLoadingScreen** to \World of Tanks Blitz\Data\UI\Screens\Battle folder.
    
## Usage

- Run the script:
   ```bash
   py BlitzGauge.py
- You can close the script pressing the **Numpad Add** key.

## What's new in v0.2

- Using modified game files, OCR gives about ~99%, a **huge** improvement over the previous version  
- Now BlitzGauge **automatically takes screenshots**. 
- Showing player stats in GUI is now faster



## Known Issues

- BlitzGauge is in alpha development.
- Currently, the software only supports a resolution of **1920x1080**.
- Script lookups for EU server players. If you want to change the server, modify the 23rd line 


## Notice

I would like to thank BlitzStars very much <3. Without it, this project would not have happened

## Contact

- You can message me on Discord - supermetalbeast
    