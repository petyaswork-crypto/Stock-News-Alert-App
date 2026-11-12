import os
import requests
from twilio.rest import Client

# --- Config from environment variables (never hardcode secrets) ---
TWILIO_SID = os.environ["TWILIO_SID"]
AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_FROM = os.environ["TWILIO_FROM"]      # e.g. "whatsapp:+14155238886"
TWILIO_TO = os.environ["TWILIO_TO"]          # e.g. "whatsapp:+359..."

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHAVANTAGE_KEY = os.environ["ALPHAVANTAGE_KEY"]
NEWSAPI_KEY = os.environ["NEWSAPI_KEY"]

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_PARAMS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": ALPHAVANTAGE_KEY,
}

NEWS_PARAMS = {
    "q": COMPANY_NAME,
    "apiKey": NEWSAPI_KEY,
    "pageSize": 3,
}

THRESHOLD_PERCENT = 0.5  # alert only if |change| exceeds this


def get_stock_change():
    """Return (difference, percent_change) between the two most recent closes."""
    response = requests.get(STOCK_ENDPOINT, params=STOCK_PARAMS, timeout=10)
    response.raise_for_status()
    data = response.json()

    # Guard: Alpha Vantage returns an "Error Message" or "Note" key on failure
    if "Time Series (Daily)" not in data:
        raise RuntimeError(f"Unexpected stock response: {data}")

    time_series = data["Time Series (Daily)"]
    dates = sorted(time_series.keys(), reverse=True)  # newest first
    if len(dates) < 2:
        raise RuntimeError("Not enough daily data returned.")

    # NOTE: the key is "4. close" (with a space)
    latest_close = float(time_series[dates[0]]["4. close"])
    previous_close = float(time_series[dates[1]]["4. close"])

    difference = latest_close - previous_close
    percent_change = round((difference / previous_close) * 100, 2)
    return difference, percent_change


def get_top_articles():
    """Return up to 3 news articles for the company."""
    response = requests.get(NEWS_ENDPOINT, params=NEWS_PARAMS, timeout=10)
    response.raise_for_status()
    articles = response.json().get("articles", [])
    return articles[:3]


def format_articles(articles, direction, percent_change):
    formatted = []
    for article in articles:
        title = article.get("title", "No title")
        description = article.get("description") or "No description available."
        formatted.append(
            f"{STOCK_NAME}: {direction}{percent_change}%\n"
            f"Headline: {title}\n"
            f"Brief: {description}"
        )
    return formatted


def send_whatsapp(messages):
    client = Client(TWILIO_SID, AUTH_TOKEN)
    for body in messages:
        client.messages.create(
            body=body,
            from_=TWILIO_FROM,
            to=TWILIO_TO,
        )


def main():
    difference, percent_change = get_stock_change()

    if abs(percent_change) <= THRESHOLD_PERCENT:
        print(f"No significant change ({percent_change}%). No alert sent.")
        return

    direction = "🔺" if difference > 0 else "🔻"
    articles = get_top_articles()
    messages = format_articles(articles, direction, percent_change)

    for message in messages:
        print(message)

    send_whatsapp(messages)
    print(f"Sent {len(messages)} alert(s).")


if __name__ == "__main__":
    main()