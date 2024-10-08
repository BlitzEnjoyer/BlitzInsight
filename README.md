# BlitzGauge

## Description
Stats for WOT Blitz, Steam version.

## Prerequisites
Ensure that the following are installed on your system:

- **Python 3.12**: [Download Python](https://www.python.org/downloads/) **Do not use the latest Python 3.13, it won't work for now**
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
Files are located in **RES** folder
   1. Insert **WarHeliosCondCBoldA** to \World of Tanks Blitz\Data\Fonts folder.
   2. Insert **FontsFs** to \World of Tanks Blitz\Data\UI\Screens folder.
   3. Insert **BattleLoadingScreen** to \World of Tanks Blitz\Data\UI\Screens\Battle folder.
    
## Usage

- Run the script:
   ```bash
   py BlitzGauge.py
- You can close the script pressing the **Numpad Add** key.
- For 10vs10 battles, modify the config.ini file.


# Changelog 

## What's new in v0.3

- Brand-new GUI with transparency and new colors
- Now works in 10vs10 mode
- Added config file to change region and battle mode


## What's new in v0.2

- Using modified game files, OCR gives about ~99%, a **huge** improvement over the previous version  
- Now BlitzGauge **automatically takes screenshots**. 
- Showing player stats in GUI is now faster



## Known Issues

- The mod crashes when player exits battle search screen, instead of loading into battle
- Currently, the software only supports a resolution of **1920x1080**.



## Notice

I would like to thank BlitzStars very much <3. Without it, this project would not have happened 

Thanks to u/limejello99 for inspiration and advice <3

## Contact

- You can message me on Discord - supermetalbeast
    