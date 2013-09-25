
class Page:
    ENUM_STUDIO_PROFILE = 1
    ENUM_STUDIO_SCHEDULE = 2
    ENUM_STUDIO_FACEBOOKFEED = 3
    ENUM_TEACHER_PROFILE = 4
    ENUM_TEACHER_SCHEDULE = 5
    ENUM_TEACHER_FACEBOOKFEED = 6


    def __init__(self, curPageID):
        self.id = curPageID