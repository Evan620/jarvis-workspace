import os
import requests
import json
from datetime import datetime

# Config
GITHUB_USERNAME = "your_github_username"  # Replace with your GitHub username
STATE_FILE = "star_state.json"

# Simulated WhatsApp send function - replace with your WhatsApp gateway integration

def send_whatsapp_message(message):
    print(f"Sending WhatsApp message: {message}")
    # Integrate with your WhatsApp API here


def load_previous_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    else:
        return {"stars": []}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def fetch_github_stars(username):
    url = f"https://api.github.com/users/{username}/starred"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch stars: {response.status_code}")
        return []


def check_new_stars():
    old_state = load_previous_state()
    old_starred = set(repo["id"] for repo in old_state.get("stars", []))

    current_stars = fetch_github_stars(GITHUB_USERNAME)
    current_starred = set(repo["id"] for repo in current_stars)

    new_star_ids = current_starred - old_starred
    if new_star_ids:
        new_stars = [repo for repo in current_stars if repo["id"] in new_star_ids]
        for star in new_stars:
            message = f"New GitHub star: {star['full_name']} - {star['html_url']}"
            send_whatsapp_message(message)
    else:
        print("No new stars.")

    save_state({"stars": current_stars})


if __name__ == "__main__":
    check_new_stars()
