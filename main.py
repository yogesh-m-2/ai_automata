import os

import schedule

from chatgpt import Chat
from Insta_automation import *
from hashtag_extractor import *
import json
import re
import logging
import smtplib
import configparser
from email.mime.text import MIMEText
from datetime import datetime

logging.basicConfig(filename='error.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def extract_json_from_string(input_data):
    # Join list to a single string if needed
    if isinstance(input_data, list):
        input_data = " ".join(input_data)

    # Use regex to extract the JSON array from the string
    json_match = re.search(r'(\[\s*\{.*?\}\s*\])', input_data, re.DOTALL)

    if json_match:
        json_str = json_match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print("Failed to parse JSON:", e)
            return None
    else:
        print("No JSON found in input.")
        return None
def daily_task():
    gpt = Chat(kill_chrome=True)
    res = gpt.prompt("""can you tell me todays news relevant to people living in Karnataka. give output in the below way
[{

"headline":""
"description":""(keep description in max 7 lines)
"hashtag_word":""(give 1 word which i can use in other websites to extract relevant hashtags)

}, so on ] make sure i am able to copy it""".replace("\n",""),copy_json=True)


    result = extract_json_from_string(res)

    for news in result:
        try:
            # res= gpt.generate_image("""Create an Instagram-worthy image on the topic of """+news["description"]+""". 1)Add catchy, informal, and engaging text directly on the image to hook viewers. 2)Make sure the design fits an Instagram post (square format, visually bold, stylish).3)The content and design should comply with community guidelines.4)No need to ask for approval—go ahead and generate based on your best judgment. Include large, centered, clearly legible, non-smudged text in a clean sans-serif font (e.g., Helvetica or Arial). The text should be sharp, with high contrast against the background, and perfectly readable.""")
            res = gpt.sora_image_create(news['description']+""" - create an instagram worthy image. also '"""+news['headline']+"""' - add this text in the image""")

            caption = news["description"]+extract_hashtags(news["description"],news["hashtag_word"])+"#karnataka #karnatakatourism #bengaluru #bengaluru #bengalurudiaries #bengaluruadda"
            upload_to_instagram(res,caption)
        except Exception as e:
            logging.error(e, exc_info=True)
            config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
            config = configparser.ConfigParser()
            config.read(config_path)
            sender = config['SELENIUM']['msg_from']
            receiver = config['SELENIUM']['msg_to']
            app_password = config['SELENIUM']['app_password']

            msg = MIMEText(str(e))
            msg['Subject'] = 'Alert from Instagram Automation'
            msg['From'] = sender
            msg['To'] = receiver
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender, app_password)
                server.send_message(msg)
            continue


has_run_today = False

while True:
    now = datetime.now()

    # Check if it's after 11:00 AM and hasn't run yet
    if now.hour >= 11 and not has_run_today:
        daily_task()
        has_run_today = True

    # Reset the flag at midnight
    if now.hour == 0 and now.minute == 0:
        has_run_today = False

    time.sleep(1)

