from django.core.urlresolvers import reverse


class Page:
    ENUM_STUDIO_PROFILE = 1
    ENUM_STUDIO_SCHEDULE = 2
    ENUM_STUDIO_FACEBOOKFEED = 3
    ENUM_TEACHER_PROFILE = 4
    ENUM_TEACHER_SCHEDULE = 5
    ENUM_TEACHER_FACEBOOKFEED = 6

    def __init__(self, curPageID):
        self.id = curPageID

    @classmethod
    def allPages(cls):
        return { Page.ENUM_STUDIO_PROFILE: 'studio-profile',
                 Page.ENUM_STUDIO_SCHEDULE: 'studio-schedule',
                 Page.ENUM_STUDIO_FACEBOOKFEED: 'studio-facebook-feed',
                 Page.ENUM_TEACHER_PROFILE: 'teacher-profile',
                 Page.ENUM_TEACHER_SCHEDULE: 'teacher-schedule',
                 Page.ENUM_TEACHER_FACEBOOKFEED: 'teacher-facebook-feed',
                 }

    @classmethod
    def createFromEnum(cls, page_enum_value):

        if not Page.allPages().has_key(page_enum_value):
            #Passed value is not one of the valid ones - return None
            return None

        newObj = cls(page_enum_value)
        newObj.id = page_enum_value
        return newObj


    def urlForStudioPage(self, studio):
        urlName=self.allPages()[self.id]
        stateUrlName=studio.state_name_url
        studioUrlName=studio.nameForURL

        return reverse(urlName, kwargs={'state_url_name': stateUrlName, 'studio_url_name': studioUrlName})


    def urlForTeacherPage(self, teacher):
        urlName=self.allPages()[self.id]
        stateUrlName=teacher.state_name_url
        teacherUrlName=teacher.name_url

        return reverse(urlName, kwargs={'state_url_name': stateUrlName, 'teacher_url_name': teacherUrlName})