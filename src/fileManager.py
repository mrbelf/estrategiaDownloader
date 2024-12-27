import os
from downloader import *

ILLEGAL_CHARS = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
REPLACE_CHAR = '_'

class FileManager:
    def __init__(self, base_path):
        self.base_path = base_path
        self.selected_course = None
        self.selected_lesson = None

    def _format_path(self, original_name):
        name = original_name
        for illegal_char in ILLEGAL_CHARS:
            name = name.replace(illegal_char, REPLACE_CHAR)
        return name

    def _courseExist(self, course):
        return os.path.exists(course)
    
    def _get_current_path(self):
        path = self.base_path
        if(self.selected_course is not None):
            path = os.path.join(path, self.selected_course)
        if(self.selected_lesson is not None):
            path = os.path.join(path, self.selected_lesson)
        return path


    def _create_folder(self, folder_name):
        folder_path = os.path.join(self.base_path, folder_name)
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def add_all_courses(self, course_names):
        for course_name in course_names:
            self._create_folder(self._format_path(course_name))

    def select_course(self, course):
        self.selected_course = self._format_path(course)
        self._create_folder(self.selected_course)
    
    def select_lesson(self, lesson_name):
        if self.selected_course is None:
            print(f'No course was selected, cant select lesson {lesson_name}')
            return

        self.selected_lesson = self._format_path(lesson_name)
        folder_name = os.path.join(self.selected_course, self.selected_lesson)
        self._create_folder(folder_name)

    def add_video(self, title, url):
        formatted_title = self._format_path(title)
        download_video(url, os.path.join(self._get_current_path(), formatted_title+'.mp4'))
    
    def add_pdf(self, url):
        download_pdf(url, os.path.join(self._get_current_path(), self.selected_lesson+'.pdf'))
