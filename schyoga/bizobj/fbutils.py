import datetime
import pytz

__author__ = 'mzalota'


class FBUtils():
    def convertString2Date(self, dt_string):
        #parse the string and convert it to datetime object. Original format is: 2013-07-25T19:46:27+0000
        #dt = datetime.datetime.strptime(dt_string+'GMT', "%Y-%m-%dT%H:%M:%S+0000%Z")

        dt_string_no_timezone = dt_string[:-5]
        dt = datetime.datetime.strptime(dt_string_no_timezone + "GMT", "%Y-%m-%dT%H:%M:%S%Z")

        timezone_sign = dt_string[-5:-4]
        timezone_minutes = int(dt_string[-2:])
        timezone_hour = int(dt_string[-4:-2])
        timezone_offset_minutes = timezone_minutes + timezone_hour * 60

        #the string passed is in GMT. Convert it to the local time
        if timezone_offset_minutes != 0:
            if timezone_sign == '-':
                dt = dt + datetime.timedelta(minutes=int(timezone_offset_minutes))
            elif timezone_sign == '+':
                dt = dt - datetime.timedelta(minutes=int(timezone_offset_minutes))
                #dt = datetime.datetime.now()

        dt_localtime = pytz.utc.localize(dt)
        return dt_localtime