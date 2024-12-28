# Estrategia Downloader

The study platform Estratégia allows for downloading classes, but not many at once.  
The courses last for 1 year and after that you'll loose access and you might want to keep your access to it.  
Therefore a downloader application is useful for downloading all courses at once.

# How to use

- Clone the project
- Include a data.json file in the root of the file with your data using the following format:
  > {  
  > "email": "YOUR_LOGIN_EMAIL",  
  > "password": "YOUR_PASSWORD",  
  > "save_path": "FULL_PATH_TO_EXISTING_FOLDER",  
  > "headless": true  
  > }
- Run with main.py file

It will download all video files and the original pdf for the lesson.  
If you face any conection instability you may want to tweek the variables in estrategiaVideoScraper.py, also in case you want to run selenium headless.
You may need to install:

- requests
- selenium

# Update

This was last updated on december 2024, I will not likely update it any further since I wont have access to the plataform anymore.  
Fell free to use and make changes as you see fit.
