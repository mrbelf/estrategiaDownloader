import os
from videoDownloader import download_video
from estrategiaVideoScraper import get_video_links
from estrategiaVideoScraper import get_all_courses
from fileManager import FileManager
import json

login_url = "https://perfil.estrategia.com/login?source=legado-polvo&target=https%3A%2F%2Fwww.estrategiaconcursos.com.br%2Faccounts%2Flogin%3F"
test_url = "https://www.estrategiaconcursos.com.br/app/dashboard/cursos" 
test_dir = os.path.join(os.path.dirname(os.getcwd()), "..\\..\\Files\\test.mp4")

with open("../data.json", "r", encoding='utf-8') as file:
    data = json.load(file)


fm = FileManager(data["save_path"])

courses = get_all_courses(test_url, data)
fm.add_all_courses(courses)
#get_video_links(test_url, data)