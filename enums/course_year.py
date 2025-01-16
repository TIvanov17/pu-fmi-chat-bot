from enum import Enum

class CourseYear(Enum):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4

    @staticmethod
    def get_course_year(course_label_year):
        course_mapping = {
            "I курс": CourseYear.FIRST,
            "II курс": CourseYear.SECOND,
            "III курс": CourseYear.THIRD,
            "IV курс": CourseYear.FOURTH
        }
        return course_mapping.get(course_label_year, None).value
