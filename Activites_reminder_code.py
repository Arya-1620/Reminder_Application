from datetime import datetime, timezone, timedelta
from time import sleep
from notifypy import Notify
import pyttsx3

# Initialize the notification tracker for each minute in an hour
is_notification_sent = [0] * 60

tts_engine = pyttsx3.init()

def send_reminder(msg):
    notification = Notify()
    notification.title = 'Urgent Reminder'
    notification.message = msg
    notification.duration = 5  # duration in seconds
    notification.send()
    # Speak the reminder message
    tts_engine.say(msg)
    tts_engine.runAndWait()

def schedule(date):
    hour = date.hour

    # Remind for lunch+water time at 1 PM
    if hour == 20 and is_notification_sent[hour] == 0:
        is_notification_sent[hour] = 1
        send_reminder("It's time for dinner and water!!")

    # Remind for snacks at 4 PM
    if hour == 16 and is_notification_sent[hour] == 0:
        is_notification_sent[hour] = 1
        send_reminder("It's time for snacks and water!!")

    # Remind to log out from work
    if hour == 18 and is_notification_sent[hour] == 0:
        is_notification_sent[hour] = 1
        send_reminder("It's time to log off from work!!")

    # Remind for drinking water during office time
    for i in range(9, 18):
        if hour == i and hour not in [13, 16] and is_notification_sent[hour] == 0:
            is_notification_sent[hour] = 1
            send_reminder("It's time to drink water!!")

if __name__ == "__main__":
    prev_date = datetime.now(timezone.utc).astimezone() - timedelta(days=1)
    while True:
        # Get current local date and time
        date = datetime.now(timezone.utc).astimezone()
        
        # Reset the notifications at the start of each new day
        if date.day == 1 or date.day > prev_date.day:
            is_notification_sent = [0] * 24
            prev_date = date
        
        # Schedule reminders based on the current time
        schedule(date)
        
        # Sleep for 5 minutes before checking again
        sleep(300)
