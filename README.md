# GitHub Follower Tracker and Auto-Unfollower

This Python script monitors your GitHub followers, detects unfollows, and automatically unfollows users who don’t follow you back (with an option to exclude special users). Keep your GitHub follows reciprocal with ease!

## Features
- Tracks follower changes over time
- Detects new followers and recent unfollowers
- Identifies non-reciprocating follows
- Auto-unfollows users who don’t follow back (excluding special people)
- Persists data locally in JSON files

## Prerequisites
- Python 3.x
- requests library
- GitHub Personal Access Token with user scope

## Setup
1. Clone the Repo: git clone https://github.com/tomemme/followerTracker.git
   Then: cd your_repo_name
2. Install Dependencies: pip3 install requests
3. Configure:
   - Open ghunfollowers.py in a text editor
   - Set USERNAME = "your_username"
   - Set TOKEN = "your_personal_access_token"
   - Generate token at https://github.com/settings/tokens with user scope
4. Optional Special People:
   - Edit special_people.json with usernames to keep, e.g., ["user1", "user2"]

## Usage
Run the script: python3 ghunfollowers.py

### Output
- Shows follower/following counts
- Lists new followers, recent unfollowers
- Unfollows and lists non-reciprocators
- Updates local files

## Files
- ghunfollowers.py: Main script
- followers.json: Previous followers
- following.json: Previous following
- special_people.json: Exempt users

## Notes
- Rate Limits: 5000 requests/hour; 1-second delays included
- First Run: Builds baseline; unfollow detection starts next run
- Safety: Skips special people

## License
MIT License - free to use and modify

## Acknowledgments
Created with Grok (xAI), March 29, 2025