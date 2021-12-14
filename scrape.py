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

    # df = df.append({'publishDate':dt.date.today(),'Posts':'Class cancelled for Alkeis1'}, ignore_index = True)

    # Extracting the posts that were published today
    df = df.loc[df.publishDate == dt.date.today()]
    df.reset_index(drop=True, inplace=True)

    matches = ["alkeis1", "alkeis 1"]
    if len(df) != 0:
        for i in range(len(df)):
            title = df['Posts'][i].lower()
            return(any(x in title for x in matches))
    else:
        return(-1)

get_updates()
