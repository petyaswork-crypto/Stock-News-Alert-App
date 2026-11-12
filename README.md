# 📰 Stock News Alert App

Hello! Welcome to my stock alerting app! It is a Python pipeline that monitors the stock's daily price movements and, 
when a significant change is detected, delivers the news to you via the Twilio API (WhatsApp).


## How it works

1. Extracts the last two daily closing prices from the API and the latest news
   articles.
2. Transforms the price change, turns it into a
   percentage, and skips the day if the change is below the alert level.
3. Delivers the big changes by formatting the top 3 headlines and sending them
   as WhatsApp messages via the Twilio API.


## Running on a schedule

You can use GitHub Actions to run the app automatically every day.

- In your repository, go to Settings → Secrets and variables → Actions, and add each credential 
(TWILIO_SID, ALPHAVANTAGE_KEY, and the rest) as a repository secret.

- Update main.py to read them from the environment, for example TWILIO_SID = os.environ.get("TWILIO_SID"). 
GitHub hides these values in the logs, so they never appear publicly.

- Create a workflow file at .github/workflows/daily.yml. Set it to run on a schedule with a cron line 
(for example 0 9 * * * for 9:00 AM UTC every day), check out the repo, set up Python, install requirements.txt, 
and run main.py with your secrets passed in as environment variables.

- Go to the Actions tab, select the workflow, and click "Run workflow" to test it manually 
before waiting for the schedule.

- Two things to keep in mind: cron times are in UTC, not your local time, so adjust the hour accordingly. 
And GitHub disables scheduled workflows after about 60 days of repository inactivity, 
so a small commit now and then keeps it running.


## Credits
Inspired by Day 36 of the course
"100 Days of Code: The Complete Python Pro Bootcamp".

The project idea, overall structure, and learning path came from the course.
The code in this repository was written by me as I followed along,
and I have added my own comments and tweaks along the way.


### 💬 P.S Thank you for taking the time to read this. It's a small project, but I'm just getting started. 
### Now go check your stocks. 📈