import datetime
from django.utils import timezone
from pytz import timezone as pytz_timezone

def milliseconds_to_local_datetime(milliseconds):
    m_t = int(milliseconds)
    my_datetime = datetime.datetime.fromtimestamp(m_t / 1000)

    return my_datetime



def convert_timezone_to_localtime(sub):
# Original naive datetime
    naive_datetime = datetime.strptime(sub, "%Y-%m-%d %H:%M:%S")

    # Define the time zone you want to convert to
    desired_timezone = pytz_timezone('America/New_York')  # Replace with your desired time zone

    # Make the datetime aware by associating the desired time zone
    aware_datetime = timezone.make_aware(naive_datetime, timezone=desired_timezone)

    # Convert to the current time zone using localtime()
    converted_datetime = timezone.localtime(aware_datetime)

    return converted_datetime