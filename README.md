# BlitzInsight

## Description
Stats for WOT Blitz, Steam version.

## How to Set Up and Use BlitzInsight

### Before You Begin

Please make sure the following software is installed on your computer:

1. **Python 3.12**: You can download it here: [Download Python](https://www.python.org/downloads/). **Make sure you install version 3.12, as the latest version (3.13) won't work with this project.**
2. **Git**: You'll need Git to download the project files. You can download it here: [Download Git](https://git-scm.com/downloads/win).

### Important informtion:

1. For now it works only in **1920x1080 Fullscreen mode**. If you have other screen resolution you can change it Windows Settings.
2. Make sure that you set the scale to **100%**.
3. Works only for **Steam** version.

### Step-by-Step Instructions

1. **Create a folder on your computer eg. Desktop. Make sure that to not make it in OneDrive**:

   - Right-click on your desktop, select **New** and then **Folder**.
   - Name the folder, for example, "BlitzInsight".
   - Open this folder.

2. **Open a terminal in the folder**:

   - Right-click inside the folder (not on any file) and select **Open in terminal** (or **Open PowerShell window here** on some systems).

3. **Download the project files**:

   - In the terminal, type the following command and press **Enter**:
     ```bash
     git clone https://github.com/BlitzEnjoyer/BlitzInsight.git
     ```
   - Then, type this command to move into the project folder:
     ```bash
     cd BlitzInsight
     ```

4. **Set up a virtual environment**:

   A virtual environment helps manage all the necessary software components for the project.

   - In the same terminal window, type the following command and press **Enter** to create the environment:
     ```bash
     py -m venv venv
     ```
   - Then, activate it by typing:
     ```bash
     venv\Scripts\activate
     ```

5. **Install required software**:

   - With the virtual environment activated, type the following command and press **Enter** to install the necessary software:
     ```bash
     pip install -r requirements.txt
     ```

6. **Modify game files**:

   - To make this project work, you need to add a few files to the game folder.
   - Files are located in the **RES** folder in project directory.
   - In the **Steam** client, find **World of Tanks Blitz**, right-click on it, select **Manage**, and then **Browse local files**.
   - Once you're in the game files folder, follow these steps:

     1. Copy the file **WarHeliosCondCBoldA** into this folder:  
        `\World of Tanks Blitz\Data\Fonts`
     2. Copy the file **FontsFs** into this folder:  
        `\World of Tanks Blitz\Data\UI\Screens`
     3. Copy the file **BattleLoadingScreen** into this folder:  
        `\World of Tanks Blitz\Data\UI\Screens\Battle`
     ### Make sure to insert the files in the correct folders!

### How to Use BlitzInsight

1. To run the script, type the following command in the terminal. **Make sure to run it in virtual environment**:
   ```bash
   py BlitzInsight.py
   ```
2. To stop the script, press the **Numpad Add** key (the "+" key on the number pad).
3. If you're playing 10vs10 battles, you may need to edit the **config.ini** file to adjust the settings for this mode.

# Changelog 
## What's new in v0.4

- Statistics for the last 90 days are available for players who are tracked by BlitzStars. Those stats are marked with red border
- GUI hides after 40 seconds. You change that value in config file. 
- Stats are showing up **MUCH FASTER!**.
- The installation instructions have been updated to be clearer and easier to follow.
- Works better in case of slow internet connection. 


## What's new in v0.3

- Brand-new GUI with transparency and new colors
- Now works in 10vs10 mode
- Added config file to change region and battle mode


## What's new in v0.2

- Using modified game files, OCR gives about ~99%, a **huge** improvement over the previous version  
- Now BlitzInsight **automatically takes screenshots**. 
- Showing player stats in GUI is now faster



## Known Issues

- The mod crashes when player exits battle search screen, instead of loading into battle
- Currently, the software only supports a resolution of **1920x1080**.
- Sometimes the GUI of the script shows a black bar at the top of the screen. Just run again the mod.   



## Notice

I would like to thank BlitzStars very much <3. Without it, this project would not have happened 

Thanks to u/limejello99 for inspiration and advice <3

## Contact

- You can message me on Discord - blitzenjoyer. DM me for a link to my Discord server and Patreon

## Legal


Not affiliated with Wargaming or World of Tanks: Blitz

Wargaming content © Wargaming.net. All rights reserved.