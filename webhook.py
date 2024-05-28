import requests
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

TEAMS_WEBHOOK_URL = 'https://ithacaedu.webhook.office.com/webhookb2/a12e8d06-d618-4d0a-bfb6-90cbd4c9f337@fa1ac8f6-5e54-4857-9f0b-4aa422c09689/IncomingWebhook/f8ef424f52bf4ec68ea841a1631d1196/2d584a1c-e5b6-4f2c-8dbe-157698fc0218'  # Replace with your actual webhook URL

def send_teams_message(name, check_in_time):
    message = {
        "text": f"{name} checked in at {check_in_time}"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(TEAMS_WEBHOOK_URL, json=message, headers=headers)
    if response.status_code != 200:
        logging.error(f"Failed to send message to Teams: {response.status_code}, {response.text}")
