from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from config import GOOGLE_CALENDAR_ID
import json
import os

# Загружаем ключ из GitHub Secrets
SERVICE_ACCOUNT_KEY = os.getenv("GOOGLE_SERVICE_ACCOUNT_KEY")
if SERVICE_ACCOUNT_KEY:
    creds_info = json.loads(SERVICE_ACCOUNT_KEY)
    creds = Credentials.from_service_account_info(creds_info, scopes=['https://www.googleapis.com/auth/calendar'])
else:
    raise ValueError("GOOGLE_SERVICE_ACCOUNT_KEY not set")

def create_calendar_event(summary, location, start_time, end_time):
    service = build('calendar', 'v3', credentials=creds)

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
