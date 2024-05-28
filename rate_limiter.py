from datetime import datetime, timedelta
from reddit import create_ssml
import calendar

days_in_month = 0
current_day = 0
current_month = 0

monthly_limit = 1000000
monthly_count = 0
daily_limit = 0
daily_count = 0

def update_days():
    global days_in_month, current_day, current_month, monthly_limit, monthly_count, daily_limit, daily_count

    current_year = datetime.now().year

    if current_month != datetime.now().month:
        monthly_count = 0
        daily_count = 0
        current_month = datetime.now().month
        days_in_month = calendar.monthrange(current_year, current_month)[1]

    if current_day != datetime.now().day:
        daily_count = 0
        current_day = datetime.now().day
        remaining_days = days_in_month - current_day + 1
        if remaining_days > 0:
            daily_limit = (monthly_limit - monthly_count) / remaining_days
        else:
            daily_limit = monthly_limit - monthly_count  # Just in case of edge case

def isValid(text):
    global daily_count, monthly_count
    update_days()

    ssml_text, segments = create_ssml(text)

    if daily_count + len(ssml_text) > daily_limit:
        print('Hit daily limit')
        return False
    daily_count += len(ssml_text)
    monthly_count += len(ssml_text)
    return True
