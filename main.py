import time
import os
import mido
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller as KeyboardController

'''

THIS SCRIPT WILL ONLY WORK ON MACOS DEVICES AND 

IMPORTANT:  Conditions before running script:
    
    1. Synthesia and OBS currently OPEN.
    2. Synthesia window in top left corner.
    3. OBS Screen and Audio Capture working as intended with Synthesia Window.
    4. midi_files folder has correct songs listed in .mid or .midi form.
    5. videos_to_edit is emptied.
    
'''

# Mouse and Keyboard controllers
mouse = Controller()
keyboard = KeyboardController()

# Function to open applications
def openApp(string):
    keyboard.press(Key.cmd)
    keyboard.press(Key.space)
    time.sleep(0.02) 
    keyboard.release(Key.cmd)
    keyboard.release(Key.space)
    time.sleep(0.02)
    for char in string:
        keyboard.press(char)
        keyboard.release(char)
        time.sleep(0.1)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(1)
    
def closeApp(string):
    openApp(string)
    keyboard.press(Key.cmd)
    time.sleep(0.02)
    keyboard.press("q")
    time.sleep(0.02)
    keyboard.release(Key.cmd)
    time.sleep(0.02)
    keyboard.release("q")
    time.sleep(1)

def moveClick(position, doubleClick = 0):
    if doubleClick == 0:
        mouse.position = position
        time.sleep(0.2)
        mouse.click(Button.left, 1)
        time.sleep(0.2)
    else:
        mouse.position = position
        time.sleep(0.2)
        mouse.click(Button.left, 2)
        time.sleep(0.2)
        print("double click success")

def prepPlay():
    moveClick((50, 90)) # Songs
    moveClick((50, 90)) # In-case dupe for middle of song
    moveClick((190, 220)) # Play a Song
    moveClick((45, 145)) # Songs
    mouse.scroll(0, 1000) # Scroll up reset
    time.sleep(1)
    moveClick((165, 235)) # All songs by folder
    moveClick((165, 195)) # Desktop
    moveClick((165, 195)) # python
    moveClick((165, 195)) # selenium
    moveClick((165, 195)) # midi files
    
def record(length):
    openApp("obs")
    moveClick((1200, 610))
    time.sleep(0.03)
    mouse.position = (1450, 30)
    time.sleep((length + 3.7))
    moveClick((1200, 610))
 
def get_midi_duration(midi_filename):
    mid = mido.MidiFile(midi_filename)
    return mid.length

def create_list_midi_files(directory):
    midi_files = [f for f in os.listdir(directory) if f.endswith('.mid') or f.endswith('.midi')]
    return midi_files
    
def process_list(song_number, directory):
    return os.path.join(directory, midi_files[song_number])

def create_list_youtube_files(directory):
    youtube_files = [f for f in os.listdir(directory) if f.endswith('.mp4')]
    return youtube_files

if __name__ == "__main__":
    
    # Retrieve Midi information
    midi_files = create_list_midi_files('/Users/yeubrook/Desktop/python/selenium/midifiles/')
    midi_files.sort()
    number_of_songs = len(midi_files)
    song_durations = []
    print("Number of songs: ", number_of_songs)

    for rotation in range(0, number_of_songs):
        midi_path = process_list(rotation, '/Users/yeubrook/Desktop/python/selenium/midifiles/')
        song_duration = get_midi_duration(midi_path)
        song_durations.append(song_duration)
        print(midi_path)
        print(midi_files[rotation])
        print(song_duration, "seconds")
        
        openApp("synthesia")
        prepPlay()
        mouse.scroll(0, 1000)
        time.sleep(0.1)
        moveClick((175, 195)) # Click first song
        time.sleep(0.5)
        for x in range(1, rotation+1):
            keyboard.press(Key.down)
            keyboard.release(Key.down)
            time.sleep(0.1)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(1)  
        
        
        moveClick((1050, 90)) # Continue button
        record(song_duration) # Record
    
        
    youtube_list = create_list_youtube_files('/Users/yeubrook/Desktop/python/selenium/videos_to_edit/')
    youtube_list.sort()
    
    
    # Set Chrome profile directory
    user_directory = "/Users/yeubrook/Library/Application Support/Google/Chrome/Profile 1/"
    google_directory = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

    # Set Chrome Options 
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    options.add_argument("--user-data-dir=" + user_directory) 

    for rotation in range(0, number_of_songs):
        print(youtube_list[rotation])
        # Launch the driver to YouTube Studio with correct options
        driver = webdriver.Chrome(options=options)
        driver.get("https://studio.youtube.com")


        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="create-icon"]'))
            )
        
        create_button = driver.find_element(By.XPATH, '//*[@id="create-icon"]')
        create_button.click()
        # Wait for YouTube Studio to load
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Upload')]"))
            )

        # Find and upload song
        upload_button = driver.find_element(By.XPATH, "//*[contains(text(), 'Upload')]")
        upload_button.click()
        time.sleep(1)

        # Upload file
        upload_files = driver.find_element(By.XPATH, '//*[@id="content"]/input')
        upload_files.send_keys("/Users/yeubrook/Desktop/python/selenium/videos_to_edit/" + youtube_list[rotation])

        time.sleep(2)
    
        title_input = WebDriverWait(driver, 4).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="textbox"]'))
        )
        
        time.sleep(1)
        
        piano_str = " [Piano Tutorial] (Synthesia)"
        
        title = midi_files[rotation]
        if title.endswith('.mid'):
            new_title = title[:-4]
        if title.endswith('.midi'):
            new_title = title[:-5]
            
        new_title = new_title + piano_str
        new_title = new_title.strip()
        new_title = new_title.replace("_", " ")
        title_input.send_keys("clear")
        #need to input before clearing, youtube automatically deletes if cleared first
        
        time.sleep(2)
        # clear the text in the title input
        title_input.clear()
        time.sleep(1)
        title_input.clear()
        time.sleep(1)
        title_input.clear()
        
        time.sleep(1)
        # send the new title
        
        for i in range(100):
            title_input.send_keys(Keys.BACKSPACE)
        title_input.send_keys(new_title)
        
        time.sleep(1)
    
        next_button = driver.find_element(By.XPATH, '//*[@id="next-button"]')
        for i in range(3):
            next_button.click()
            time.sleep(1)

        done_button = driver.find_element(By.XPATH, '//*[@id="done-button"]')
        done_button.click()
        time.sleep(song_durations[rotation] * 2.5)
        
        driver.quit()

    print("Process complete!")