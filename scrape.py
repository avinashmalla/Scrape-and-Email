import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def get_updates():
    URL = "https://www.ouka.fi/oulu/villavictor/ajankohtaista"
    # request the URL and parse the JSON
    page = requests.get(URL)
    page.raise_for_status() # raise exception if invalid response

    soup = BeautifulSoup(page.content, "html.parser")

    #Extraction, Clean up and Date formatting
    dateSpan = soup.find_all('span', {'class' : 'metadata-entry metadata-publish-date'})
    publish_date_txt = [span.get_text().strip() for span in dateSpan]
    publish_date = [dt.datetime.strptime(dtm,'%d.%m.%Y').date() for dtm in publish_date_txt]

    #Extraction and Clean up of posts
    postSpan = soup.find_all('header', {'class' : 'ouka-ap-title-list-title'})
    posts = [span.get_text().strip() for span in postSpan]

    df = pd.DataFrame(list(zip(publish_date, posts)),columns =['publishDate', 'Posts'])
    # The df is now ready

    # df = df.append({'publishDate':dt.date.today(),'Posts':'Class cancelled for Alkeisf 1'}, ignore_index = True)

    # Extracting the posts that were published today
    df = df.loc[df.publishDate == dt.date.today()]
    df.reset_index(drop=True, inplace=True)

    matches = ["alkeis1", "alkeis 1"]
    if len(df) != 0:
        for i in range(len(df)):
            title = df['Posts'][i].lower()
            return(any(x in title for x in matches))
            #### CREATE A PACKET ALONG WITH THE RESULT
    else:
        return(-1)


import smtplib, ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

sender_email = os.environ['MAIL_USER']
receiver_email = "malla.avi@gmail.com"
password = os.environ['MAIL_PASS']
receiver_list = ['malla_avi@hotmail.com','malla.avi@gmail.com']

msg = MIMEMultipart()
msg['From'] = sender_email

# check for updates on the website
latestUpdate = get_updates()

if latestUpdate == -1:
    msg['To'] = receiver_email
    msg['Subject'] = 'No new posts today'
    body = 'The page does not have any new posts. Enjoy your day.'
elif latestUpdate == 1:
    msg['To'] = ','.join(receiver_list)
    msg['Subject'] = 'New Post on Villa Victor'
    body = 'Hello!! A new update has been posted on Villa Victor Website about Alkeis 1 course. Please check the website https://www.ouka.fi/oulu/villavictor/ajankohtaista'
elif latestUpdate == 0:
    msg['To'] = receiver_email
    msg['Subject'] = 'Nothing important to report today'
    body = 'Hello!! New post but NOT about Alkeis 1'



msg_content = MIMEText(body, 'plain', 'utf-8')
msg.attach(msg_content)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, msg['To'].split(","), msg.as_string())
