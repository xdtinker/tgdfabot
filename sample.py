import datetime
import pytz

today = datetime.datetime.now(pytz.timezone('Asia/Manila'))

dateToday = my_date.strftime("%m/%d/%Y %I:%M %p")

print(dateToday)