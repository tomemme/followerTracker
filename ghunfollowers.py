import requests
import json
import time
from datetime import datetime

# Replace with your GitHub username and personal access token
USERNAME = "your_username"
TOKEN = "your_personal_access_token"  # Generate this from GitHub settings

# Files to store data
FOLLOWERS_FILE = "followers.json"
FOLLOWING_FILE = "following.json"
SPECIAL_PEOPLE_FILE = "special_people.json"

def get_followers():
    """Fetch current list of followers from GitHub API"""
    followers = []
    page = 1
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    while True:
        url = f"https://api.github.com/users/{USERNAME}/followers?page={page}&per_page=100"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error fetching followers: {response.status_code}")
            break
            
        page_followers = response.json()
        if not page_followers:
            break
            
        followers.extend([follower["login"] for follower in page_followers])
        page += 1
        time.sleep(1)  # Respect rate limits
        
    return set(followers)

def get_following():
    """Fetch list of people you follow from GitHub API"""
    following = []
    page = 1
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    while True:
        url = f"https://api.github.com/users/{USERNAME}/following?page={page}&per_page=100"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error fetching following: {response.status_code}")
            break
            
        page_following = response.json()
        if not page_following:
            break
            
        following.extend([user["login"] for user in page_following])
        page += 1
        time.sleep(1)  # Respect rate limits
        
    return set(following)

def unfollow_user(username):
    """Unfollow a specific user via GitHub API"""
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/user/following/{username}"
    response = requests.delete(url, headers=headers)
    
    if response.status_code == 204:
        print(f"Successfully unfollowed {username}")
    else:
        print(f"Failed to unfollow {username}: {response.status_code}")
    time.sleep(1)  # Rate limit respect

def load_previous_followers():
    """Load previous followers from file"""
    try:
        with open(FOLLOWERS_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_followers(followers):
    """Save current followers to file"""
    with open(FOLLOWERS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(followers), f)

def save_following(following):
    """Save current following to file"""
    with open(FOLLOWING_FILE, "w", encoding="utf-8") as f:
        json.dump(list(following), f)

def load_special_people():
    """Load special people list from file"""
    try:
        with open(SPECIAL_PEOPLE_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_special_people(special_people):
    """Save special people list to file"""
    with open(SPECIAL_PEOPLE_FILE, "w", encoding="utf-8") as f:
        json.dump(list(special_people), f)

def main():
    print(f"Checking GitHub status for {USERNAME} at {datetime.now()}")
    
    # Get current followers and following
    current_followers = get_followers()
    current_following = get_following()
    special_people = load_special_people()
    
    print(f"Current followers: {len(current_followers)}")
    print(f"Currently following: {len(current_following)}")
    print(f"Special people excluded from unfollow checks: {len(special_people)}")
    
    # Load previous followers
    previous_followers = load_previous_followers()
    
    # Find recent unfollowers
    recent_unfollowers = previous_followers - current_followers
    if recent_unfollowers:
        print("\nThese jerks unfollowed you since last check:")
        for user in recent_unfollowers:
            print(f"- {user}")
    else:
        print("\nNo recent unfollows since last check!")
    
    # Find new followers
    new_followers = current_followers - previous_followers
    if new_followers:
        print("\nNew followers:")
        for user in new_followers:
            print(f"- {user}")
    
    # Find and unfollow people you follow who don't follow you back
    non_reciprocators = current_following - current_followers - special_people
    if non_reciprocators:
        print("\nUnfollowing these people who don't follow you back:")
        for user in non_reciprocators:
            print(f"- {user}")
            unfollow_user(user)
            current_following.remove(user)  # Update local set after unfollowing
    else:
        print("\nEveryone you follow follows you back (excluding special people)!")
    
    # Save current data
    save_followers(current_followers)
    save_following(current_following)
    
    print(f"\nDone! Total followers now: {len(current_followers)}")
    print(f"Total following now: {len(current_following)}")

if __name__ == "__main__":
    main()