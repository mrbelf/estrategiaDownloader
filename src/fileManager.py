import os

class FileManager:
    def __init__(self, base_path):
        self.base_path = base_path
        #self.select_course = None

    def _courseExist(self, course):
        return os.path.exists(course)

    def _create_folder(self, folder_name):
        folder_path = os.path.join(self.base_path, folder_name)
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def add_all_courses(self, course_names):
        for course_name in course_names:
            self._create_folder(course_name)

    def select_course(self, course):
        self.selected_course = course
        self._create_folder(course)
    
    def select_lesson(self, lesson_name):
        if self.selected_course is None:
            print('No course was selected')
            return

        self.selected_lesson = lesson_name
        folder_name = os.path.join(self.selected_course, lesson_name)
        self._create_folder(folder_name)
