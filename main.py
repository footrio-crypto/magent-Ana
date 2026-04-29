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
    return yf.download(ticker, period="1y", progress=False)


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
    current_year = datetime.datetime.now().year

    ytd_data = close[close.index >= f"{current_year}-01-01"]

    if ytd_data.empty:
        return None

    ytd_start = ytd_data.iloc[0]
    one_year_start = close.iloc[0]

    ytd = (latest - ytd_start) / ytd_start * 100
    one_year = (latest - one_year_start) / one_year_start * 100

    chart_data = []

    for date, price in close.items():
        chart_data.append({
            "date": str(date.date()),
            "price": round(float(price), 2)
        })

    return {
        "price": round(float(latest), 2),
        "ytd": round(float(ytd), 2),
        "1y": round(float(one_year), 2),
        "chart": chart_data
    }


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

    print("Collecting external market views...")
    market_views = collect_market_views()

    create_html_dashboard(results, signals, market_views)

    print("index.html created successfully.")


job()
