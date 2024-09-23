# calendar_integration/google_calendar.py

import os
from django.conf import settings
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_credentials():
    creds = None
    credentials_path = settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON
    
    # Check if token.json exists and load the credentials from it
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no valid credentials, authenticate the user
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())  # Refresh access token
            except google.auth.exceptions.RefreshError:
                print("Token has expired or been revoked. Re-authenticating...")
                # Do not remove token.json here immediately; handle failure gracefully
                creds = None  # Reset credentials for full re-authentication
        
        # If no valid credentials after trying to refresh, perform full authentication
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

def get_calendar_service():
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)
    return service


from datetime import datetime, timedelta

def parse_datetime(datetime_str):
    # Adjust the format string to match the format of datetime_str
    return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')

def add_appointment_to_google_calendar(user_email, appointment_data, attendee_emails):
    service = get_calendar_service()
    # Parse the start_time and end_time from string format to datetime objects
    start_time = parse_datetime(appointment_data['start_time'])
    end_time = parse_datetime(appointment_data['end_time'])

    # Convert datetime objects to ISO 8601 strings
    start_time_iso = start_time.isoformat() + 'Z'  # Append 'Z' for UTC timezone
    end_time_iso = end_time.isoformat() + 'Z'  # Append 'Z' for UTC timezone

    event = {
        'summary': appointment_data['title'],
        'description': appointment_data['description'],
        'start': {
            'dateTime': start_time_iso,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time_iso,
            'timeZone': 'UTC',
        },
        'attendees': [{'email': email} for email in attendee_emails + [user_email]],
    }

    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        return event
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_user_busy_events(user_email):
    service = get_calendar_service()

    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    future = (datetime.utcnow() + timedelta(days=30)).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        timeMax=future,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    user_events = []
    busy_events = []

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        attendees = [attendee['email'] for attendee in event.get('attendees', [])]

        event_data = {
            'summary': event.get('summary', 'No Title'),
            'description': event.get('description', ''),
            'start': start,
            'end': end,
            'attendees': ', '.join(attendees)
        }

        if user_email in attendees:
            user_events.append(event_data)
        else:
            busy_events.append(event_data)
    return user_events, busy_events