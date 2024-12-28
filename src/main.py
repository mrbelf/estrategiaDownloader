from dataScrapper import DataScrapper
from fileManager import FileManager
import json

courses_url = "https://www.estrategiaconcursos.com.br/app/dashboard/cursos" 

with open("../data.json", "r", encoding='utf-8') as file:
    data = json.load(file)

fm = FileManager(data["save_path"])
ds = DataScrapper(courses_url, data['email'], data['password'], False, data['headless'])

print(f'Getting courses list')
courses = ds.get_all_courses()
print(f'Got {len(courses)} courses to download')

for course in courses:
    print(f'Selecting course: {course}')
    fm.select_course(course)
    print(f'Getting lessons')
    lessons = ds.get_all_lessons(course)
    print(f'Got {len(lessons)} to download on course {course}')
    for lesson in lessons:
        print(f'Selecting lesson: {lesson}')
        fm.select_lesson(lesson)
        print(f'Getting lesson PDF')
        pdf_link = ds.get_pdf_link(course, lesson)
        print(f'Downloading lesson PDF')
        fm.add_pdf(pdf_link)
        print(f'PDF Downloaded')
        print(f'Getting video links')
        videos = ds.get_video_links(course, lesson)
        print(f'Got {len(videos)} to download on lesson {lesson} of course {course}')
        for video in videos:
            print(f'Starting download of {video[0]}')
            fm.add_video(video[0], video[1])
            print(f'Finished download of {video[0]}')
            
