from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import smtplib

YT_TRENDING_URL = 'https://youtube.com/feed/trending'

SENDER_EMAIL = 'sendsometrends@gmail.com'
RECEIVER_EMAIL = 'SENDER_EMAIL'


def send_email():
  s = smtplib.SMTP('smtp.gmail.com', 587)
  s.starttls()
  s.login(SENDER_EMAIL, 'seleniumworkshop')
  message = "This is a message from AWS Lambda"
  s.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)
  s.quit()


def extract_videos(browser):
  """Open YouTube trending feed and extract videos"""
  browser.get(YT_TRENDING_URL)
  video_tag_name = 'ytd-video-renderer'
  video_tags = browser.find_elements(By.TAG_NAME, video_tag_name)
  return video_tags


def parse_video(video):
  """Extract information for a single video"""
  title_a = video.find_element(By.ID, 'video-title')
  title = title_a.text
  url = title_a.get_attribute('href')
  channel = video.find_element(By.ID, 'channel-name').text
  description = video.find_element(By.ID, 'description-text').text
  thumbnail_div = video.find_element(By.ID, 'thumbnail')
  thumbnail_url = thumbnail_div.find_element(By.TAG_NAME,
                                             'img').get_attribute('src')
  metadata_line = video.find_element(By.ID, 'metadata-line')
  metadata_spans = metadata_line.find_elements(By.TAG_NAME, 'span')
  views = metadata_spans[0].text.replace(' views', '')
  uploaded = metadata_spans[1].text
  return {
      'title': title,
      'url': url,
      'channel': channel,
      'description': description,
      'thumbnail_url': thumbnail_url,
      'views': views,
      'uploaded': uploaded
  }


def lambda_handler(event, context):
  options = Options()
  options.binary_location = '/opt/headless-chromium'
  options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--single-process')
  options.add_argument('--disable-dev-shm-usage')

  driver = webdriver.Chrome('/opt/chromedriver', chrome_options=options)

  videos = extract_videos(driver)
  videos_data = [parse_video(video) for video in videos[:10]]

  send_email()

  driver.close()
  driver.quit()

  response = {"statusCode": 200, "body": videos_data}

  return response
