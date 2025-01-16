class StudentInfo:
    def __init__(self, major, education_form, university_year):
        self.major = major
        self.education_form = education_form
        self.university_year = university_year

    def __repr__(self):
        return f"StudentInfoDTO(major={self.major}, education_form={self.education_form}, university_year={self.university_year})"

    @staticmethod
    def get_major_by_code(code):
        for field, field_code in StudentInfo.majors.items():
            if field_code == code:
                return field
        return None

    majors = {
        "Информатика": 26,
        "Бизнес информационни технологии": 56,
        "Софтуерни технологии и дизайн": 68,
        "Софтуерно инженерство": 32,
        "Математика": 5,
        "Приложна математика": 39,
        "Бизнес математика": 23,
        "Информационни технологии, математика и образователен мениджмънт": 65,
        "Математика, информатика и информационни технологии": 18
    }
