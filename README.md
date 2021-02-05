# linebot-booking-system
## Description
It's a simple reservation system for the band practice room of nturockclub. It will ask a sequence of questions to users to get their personal information and book the practice room. It also connect with the google sheet which make the club manager easy to know who use the room at which time.\
App Appearence: \
<img src="READMEpic/app_appearance.jpg" width="250">\
Google Sheet Appearence (The first row of the sheet is the time and the fist column is the date that user borrowed): \
<img src="READMEpic/googlesheetpic.png" height="250">
## Usage
Fist, go to https://console.developers.google.com/ to create Google Sheet API credentials and put the JSON file to the current directory.And fix the blank:
```
scope = ["",'',"",""]
creds = ServiceAccountCredentials.from_json_keyfile_name("YOURJSONFILE", scope)
client = gspread.authorize(creds)
sheet = client.open("練團室時間表").sheet1  # Open the spreadhseet 
```
Second, deployed it on the heroku. And you will get an line QR code.\
Last, Feel free to justified the process to fit your needs.\
If you think it is helpful for your current project, plz press the star buttom for encouragement.\

