from estrategiaVideoScraper import get_all_courses
from estrategiaVideoScraper import get_all_lessons
from estrategiaVideoScraper import get_video_links
from estrategiaVideoScraper import get_pdf_link
from fileManager import FileManager
import json

courses_url = "https://www.estrategiaconcursos.com.br/app/dashboard/cursos" 

with open("../data.json", "r", encoding='utf-8') as file:
    data = json.load(file)

fm = FileManager(data["save_path"])

print(f'Getting courses list')
courses = get_all_courses(courses_url, data)
print(f'Got {len(courses)} courses to download')

for course in courses[:1]:
    print(f'Selecting course: {course}')
    fm.select_course(course)
    print(f'Getting lessons')
    lessons = get_all_lessons(courses_url, data, course)
    print(f'Got {len(lessons)} to download on course {course}')
    for lesson in lessons:
        print(f'Selecting lesson: {lesson}')
        fm.select_lesson(lesson)
        print(f'Getting lesson PDF')
        pdf_link = get_pdf_link(courses_url, data, course, lesson)
        print(f'Downloading lesson PDF')
        fm.add_pdf(pdf_link)
        print(f'PDF Downloaded')
        # print(f'Getting video links')
        # videos = get_video_links(courses_url, data, course, lesson)
        # print(f'Got {len(videos)} to download on lesson {lesson} of course {course}')
        # for video in videos:
        #     print(f'Starting download of {video[0]}')
        #     #fm.add_video(video[0], video[1])
        #     print(f'Finished download of {video[0]}')
            
