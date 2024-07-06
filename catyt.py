from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import pyktok as pyk
pyk.specify_browser('chrome')

def download_video(link, id):
    print(f"Downloading video {id} from: {link}")
    cookies = {
        # Please get this data from the console network activity tool
        # This is explained in the video :)
    }

    headers = {
        # Please get this data from the console network activity tool
        # This is explained in the video :)
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': '', # NOTE: This value gets changed, please use the value that you get when you copy the curl command from the network console
    }
    
    print("STEP 4: Getting the download link")
    print("If this step fails, PLEASE read the steps above")
    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text[:500]}")  # Print the first 500 characters of the response for debugging

    download_soup = BeautifulSoup(response.text, "html.parser")
    print("Parsed HTML:", download_soup.prettify()[:500])  # Print the first 500 characters of the parsed HTML

    link_video = link + "?is_copy_url=1&is_from_webapp=v1"
    pyk.save_tiktok(link_video,True, 'video_data.csv','chrome')

def scrape_tiktok_videos():
    print("STEP 1: Open Chrome browser")
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)
    # Change the tiktok link
    driver.get("https://www.tiktok.com/search?q=cats%20of%20tiktok&t=1717164787014")

    # IF YOU GET A TIKTOK CAPTCHA, CHANGE THE TIMEOUT HERE
    # to 60 seconds, just enough time for you to complete the captcha yourself.
    time.sleep(10)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(2)

    scroll_pause_time = 1
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1

    print("STEP 2: Scrolling page")
    while True:
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(scroll_pause_time)
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        if (screen_height) * i > scroll_height:
            break 

    class_name = " css-1as5cen-DivWrapper e1cg0wnj1".strip()

    script  = "let l = [];"
    script += "Array.from(document.querySelectorAll(\"."
    script += class_name.replace(" ", ".")
    script += "\")).forEach(item => { l.push(item.querySelector('a').href)});"
    script += "return l;"

    urls_to_download = driver.execute_script(script)

    print(f"STEP 3: Time to download {len(urls_to_download)} videos")
    for index, url in enumerate(urls_to_download):
        print(f"Downloading video: {index}")
        download_video(url, index)
        time.sleep(10)
