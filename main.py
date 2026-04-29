import datetime
import yfinance as yf

from analysis import analyze
from news_sentiment import collect_market_views
from html_dashboard import create_html_dashboard


TICKERS = {
    "Gold": "GC=F",
    "Silver": "SI=F",
    "DBS": "D05.SI",
    "Bank of China": "3988.HK",
    "NVIDIA": "NVDA",
    "Amazon": "AMZN",
    "Alphabet": "GOOGL",
    "Broadcom": "AVGO",
}


def fetch_data(ticker):
    return yf.download(ticker, period="5y", progress=False)


def get_close_series(df):
    close = df["Close"]

    if hasattr(close, "columns"):
        close = close.iloc[:, 0]

    return close.dropna()


def calculate_metrics(df):
    close = get_close_series(df)

    if close.empty:
        return None

    latest = close.iloc[-1]
    previous = close.iloc[-2] if len(close) > 1 else latest

    current_year = datetime.datetime.now().year
    ytd_data = close[close.index >= f"{current_year}-01-01"]

    if ytd_data.empty:
        return None

    ytd_start = ytd_data.iloc[0]
    one_year_start = close[close.index >= close.index[-1] - datetime.timedelta(days=365)].iloc[0]
    three_year_start = close[close.index >= close.index[-1] - datetime.timedelta(days=365 * 3)].iloc[0]
    five_year_start = close.iloc[0]

    one_day = (latest - previous) / previous * 100
    ytd = (latest - ytd_start) / ytd_start * 100
    one_year = (latest - one_year_start) / one_year_start * 100
    three_year = (latest - three_year_start) / three_year_start * 100
    five_year = (latest - five_year_start) / five_year_start * 100

    chart_data = []

    for date, price in close.items():
        chart_data.append({
            "date": str(date.date()),
            "price": round(float(price), 2)
        })

    return {
        "price": round(float(latest), 2),
        "1d": round(float(one_day), 2),
        "ytd": round(float(ytd), 2),
        "1y": round(float(one_year), 2),
        "3y": round(float(three_year), 2),
        "5y": round(float(five_year), 2),
        "chart": chart_data
    }


def create_gold_alerts(results):
    alerts = []

    gold = results.get("Gold", {})
    gold_price = gold.get("price", 0)
    gold_ytd = gold.get("ytd", 0)

    if gold_price < 170:
        alerts.append("Gold Strategy: BUY ZONE below 170")
    elif gold_price > 200:
        alerts.append("Gold Strategy: WAIT / OVERHEATED above 200")
    else:
        alerts.append("Gold Strategy: HOLD / MONTHLY GAUGE between 170 and 200")

    if gold_ytd > 20:
        alerts.append("Gold has strong YTD performance. Avoid chasing emotionally.")
    elif gold_ytd < 5:
        alerts.append("Gold momentum is calmer. Watch for accumulation zone.")

    return alerts


def job():
    print("Running market dashboard update...")

    results = {}

    for name, ticker in TICKERS.items():
        print(f"Fetching {name}...")
        df = fetch_data(ticker)

        if df.empty:
            print(f"No data for {name}")
            continue

        metrics = calculate_metrics(df)

        if metrics is None:
            print(f"Skipping {name}")
            continue

        results[name] = metrics

    if not results:
        raise ValueError("No market data retrieved.")

    signals = analyze(results)
    alerts = create_gold_alerts(results)

    print("Collecting external market views...")
    market_views = collect_market_views()

    create_html_dashboard(results, signals, market_views, alerts)

    print("index.html created successfully.")


job()
