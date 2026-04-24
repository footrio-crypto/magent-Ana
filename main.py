import yfinance as yf
import datetime
import schedule
import time
import os
import matplotlib.pyplot as plt
from analysis import analyze
from report_generator import create_pdf
import smtplib
from email.message import EmailMessage

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
SEND_TIME = os.environ.get("TIME", "08:00")

TICKERS = {
    "Gold": "GC=F",
    "Silver": "SI=F",
    "DBS": "D05.SI",
    "Bank of China": "3988.HK",
    "NVIDIA": "NVDA",
    "Amazon": "AMZN",
    "Alphabet": "GOOGL",
    "Broadcom": "AVGO"
}

def fetch_data(ticker):
    return yf.download(ticker, period="1y")

def calc(df):
    latest = df["Close"].iloc[-1]
    ytd_start = df[df.index >= f"{datetime.datetime.now().year}-01-01"]["Close"].iloc[0]
    ytd = (latest - ytd_start) / ytd_start * 100
    return round(latest,2), round(ytd,2)

def chart(df, name):
    plt.figure()
    df["Close"].plot(title=name)
    file = f"{name}.png"
    plt.savefig(file)
    plt.close()
    return file

def job():
    results = {}
    charts = []

    for k,v in TICKERS.items():
        df = fetch_data(v)
        price, ytd = calc(df)
        results[k] = {"price": price, "ytd": ytd}
        charts.append(chart(df,k))

    signals = analyze(results)

    report = "Market Summary\n\n"
    for k,v in results.items():
        report += f"{k}: {v['price']} | YTD: {v['ytd']}%\n"

    report += "\nSignals:\n"
    for k,v in signals.items():
        report += f"{k}: {v}\n"

    create_pdf(report, charts)
    send_email(report)

def send_email(text):
    msg = EmailMessage()
    msg["Subject"] = "Daily Market Report"
    msg["From"] = EMAIL
    msg["To"] = EMAIL
    msg.set_content(text)

    with open("market_report.pdf","rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename="report.pdf")

    with smtplib.SMTP("smtp.office365.com",587) as s:
        s.starttls()
        s.login(EMAIL,PASSWORD)
        s.send_message(msg)

schedule.every().day.at(SEND_TIME).do(job)

while True:
    schedule.run_pending()
    time.sleep(60)