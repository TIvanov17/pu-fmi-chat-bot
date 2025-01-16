from enum import Enum

class EducationForm(Enum):
    REGULAR = "редовно"
    ABSENTIA = "задочно"

    def __str__(self):
        return self.value
