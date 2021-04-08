from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import requests
import get_episode_link
start_ep = int(input('Enter the start episode number:')) # Get the start of episode
end_ep = int(input('Enter the end episode number:')) # Get the end of episode

options = Options()
options.binary_location = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe' # Use chrome driver with brave browser
driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)

episode_links = get_episode_link.get_episode_link()
for episode in range(start_ep,end_ep+1):
    #url = 'https://kissanimes.su/ep/naruto-shippuuden-dub-episode-' + str(episode) + '/288068/' # URL of the website from where we are downloading the episodes
    url = 'https://kissanimes.su'+episode_links[str(episode)].strip() # URL of the website from where we are downloading the episodes
    driver.get(url)

    video_xpath = '//*[@id="load_anime"]/div/div/iframe' # XPath of the video on the main page

    element = WebDriverWait(driver, 500).until(
        EC.presence_of_element_located((By.XPATH, video_xpath))) # Waits until the XPath is found

    video = driver.find_element_by_xpath(video_xpath) # Finds the video by XPath
    video_url = video.get_attribute('src')+'.mp4' # Gets the link to the video player on which the episode is played on
    driver.get(video_url) # Opens the player in the current tab

    play_button = '//*[@id="myVideo"]/div[2]/div[4]'
    time.sleep(2)
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(driver.find_element_by_xpath(play_button), 5, 5)
    action.click() # Clicks on a point around the play button to trigger the ads
    action.perform()

    time.sleep(2)
    driver_len = len(driver.window_handles)  # Fetching the number of opened tabs
    path = "D:\\Naruto Shippuden\\"
    if driver_len > 1:  # Will execute if more than 1 tabs found.
        for tab in range(driver_len - 1, 0, -1):
            driver.switch_to.window(driver.window_handles[tab])  # Will close the last tab first.
            driver.close()
        driver.switch_to.window(driver.window_handles[0])  # Switching the driver focus to first tab.
        action.move_to_element_with_offset(driver.find_element_by_xpath(play_button), 5, 5)
        action.click() # Clicks on a point around the play button to trigger the request to get the video URL
        action.perform()
    time.sleep(2)

    video_file = '//*[@id="myVideo"]/div[2]/div[4]/video' # XPath for the element that contains the video URL
    video_link = driver.find_element_by_xpath(video_file).get_attribute('src')
    video_file = requests.get(video_link).content
    print('Getting the link to download')
    with open(path+'episode_'+str(episode)+'.mp4', 'wb') as handler:
        print('Downloading episode ',str(episode))
        handler.write(video_file) # Saves the file to the path specified
        print('Downloaded episode ',str(episode))

