import os
import datetime
import smtplib
from email.message import EmailMessage

import yfinance as yf
import matplotlib.pyplot as plt

from analysis import analyze
from report_generator import create_pdf
from news_sentiment import collect_market_views, format_market_views


EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

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

    return {
        "price": round(float(latest), 2),
        "ytd": round(float(ytd), 2),
        "1y": round(float(one_year), 2),
    }


def create_chart(df, name):
    close = get_close_series(df)

    if close.empty:
        return None

    filename = f"{name.replace(' ', '_')}.png"

    plt.figure(figsize=(8, 4))
    close.plot(title=f"{name} - 1 Year Price Chart")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

    return filename


def send_email(report_text):
    if not EMAIL or not PASSWORD:
        raise ValueError("Missing EMAIL or PASSWORD GitHub secret.")

    msg = EmailMessage()
    msg["Subject"] = "Daily Market Report"
    msg["From"] = EMAIL
    msg["To"] = EMAIL
    msg.set_content(report_text)

    with open("market_report.pdf", "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename="market_report.pdf",
        )

    print("Using Gmail SMTP...")

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)


def job():
    print("Running market job...")

    results = {}
    charts = []

    for name, ticker in TICKERS.items():
        print(f"Fetching {name}...")

        df = fetch_data(ticker)

        if df.empty:
            print(f"No data for {name}")
            continue

        metrics = calculate_metrics(df)

        if metrics is None:
            print(f"Skipping {name} - no metrics")
            continue

        results[name] = metrics

        chart_file = create_chart(df, name)
        if chart_file:
            charts.append(chart_file)

    if not results:
        raise ValueError("No market data retrieved.")

    signals = analyze(results)

    today = datetime.datetime.now().strftime("%d %B %Y")

    report = f"Daily Market Report - {today}\n\n"

    report += "Market Numbers\n"
    report += "----------------------\n"

    for name, data in results.items():
        report += (
            f"{name}: {data['price']} | "
            f"YTD: {data['ytd']}% | "
            f"1Y: {data['1y']}%\n"
        )

    report += "\nSignals\n"
    report += "----------------------\n"

    for name, signal in signals.items():
        report += f"{name}: {signal}\n"

    print("Collecting external market views...")
    market_views = collect_market_views()
    report += format_market_views(market_views)

    report += "\n\nNote: Monitoring tool only, not financial advice.\n"

    create_pdf(report, charts)
    send_email(report)

    print("Email sent successfully.")


print("Running scheduled market report now...")
job()
print("Job completed.")
