# Scrape and Email

**Background**

*I am currently enrolled in the Finnish language course provided by [Villa Victor](https://www.ouka.fi/oulu/villavictor/). Students were informed that it was not possible to notify/email us individually if classes were cancelled. Instead, we had to check the website everyday to check if the classes were cancelled.*

This python script
 - scrapes the website to check if there is any new **relevant** news
    * in this case, the script detects any news about the elementary finnish language course named "Alkeis 1".
    * if there is a new **relevant** post on the page, it extracts and includes the title and link to the post in the email notification.
 - is executed *every weekday morning* via Github Actions
 - sends me email notifications
