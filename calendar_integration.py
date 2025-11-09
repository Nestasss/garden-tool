from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from config import GOOGLE_CALENDAR_API_KEY, GOOGLE_CALENDAR_ID

def create_calendar_event(summary, location, start_time, end_time):
    service = build("calendar", "v3", developerKey=GOOGLE_CALENDAR_API_KEY)

    event = {
        'summary': summary,
        'location': location,
        'start': {
            'dateTime': start_time,
            'timeZone': 'Europe/Moscow',  # Учитываем ваш часовой пояс
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Europe/Moscow',
        },
    }

    event = service.events().insert(calendarId=GOOGLE_CALENDAR_ID, body=event).execute()
    return event.get('htmlLink')
