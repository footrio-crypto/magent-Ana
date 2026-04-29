import json
import datetime


def create_html_dashboard(results, signals, market_views):
    updated_at = datetime.datetime.utcnow().strftime("%d %B %Y, %H:%M UTC")

    data_json = json.dumps(results)
    signals_json = json.dumps(signals)
    views_json = json.dumps(market_views)

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Magent Market Intelligence Dashboard</title>

  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <style>
    body {{
      font-family: Arial, sans-serif;
      background: #f6f4ef;
      color: #1f2933;
      margin: 0;
      padding: 0;
    }}

    header {{
      background: #1f2933;
      color: white;
      padding: 24px;
      text-align: center;
    }}

    header h1 {{
      margin: 0;
      font-size: 28px;
    }}

    header p {{
      margin: 8px 0 0;
      opacity: 0.85;
    }}

    .container {{
      max-width: 1200px;
      margin: auto;
      padding: 24px;
    }}

    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 16px;
    }}

    .card {{
      background: white;
      border-radius: 16px;
      padding: 20px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}

    .card h2 {{
      margin-top: 0;
      font-size: 20px;
    }}

    .price {{
      font-size: 28px;
      font-weight: bold;
      margin: 8px 0;
    }}

    .positive {{
      color: #15803d;
      font-weight: bold;
    }}

    .negative {{
      color: #b91c1c;
      font-weight: bold;
    }}

    .neutral {{
      color: #92400e;
      font-weight: bold;
    }}

    .section-title {{
      margin-top: 36px;
      margin-bottom: 16px;
      font-size: 24px;
    }}

    canvas {{
      max-height: 260px;
    }}

    ul {{
      padding-left: 20px;
    }}

    footer {{
      text-align: center;
      color: #6b7280;
      padding: 30px;
      font-size: 13px;
    }}
  </style>
</head>

<body>
  <header>
    <h1>Felia Market Intelligence Dashboard</h1>
    <p>Gold • Silver • DBS • Bank of China • AI Stocks</p>
    <p>Last updated: {updated_at}</p>
  </header>

  <div class="container">

    <h2 class="section-title">Market Numbers</h2>
    <div class="grid" id="marketCards"></div>

    <h2 class="section-title">Charts</h2>
    <div class="grid" id="charts"></div>

    <h2 class="section-title">Signals</h2>
    <div class="grid" id="signals"></div>

    <h2 class="section-title">External Market Views</h2>
    <div class="grid" id="views"></div>

  </div>

  <footer>
    Monitoring tool only. Not financial advice.
  </footer>

<script>
const marketData = {data_json};
const signals = {signals_json};
const views = {views_json};

function pctClass(value) {{
  if (value > 0) return "positive";
  if (value < 0) return "negative";
  return "neutral";
}}

const marketCards = document.getElementById("marketCards");

Object.entries(marketData).forEach(([name, data]) => {{
  const card = document.createElement("div");
  card.className = "card";

  card.innerHTML = `
    <h2>${{name}}</h2>
    <div class="price">${{data.price}}</div>
    <p>YTD: <span class="${{pctClass(data.ytd)}}">${{data.ytd}}%</span></p>
    <p>1Y: <span class="${{pctClass(data["1y"])}}">${{data["1y"]}}%</span></p>
  `;

  marketCards.appendChild(card);
}});

const chartsDiv = document.getElementById("charts");

Object.entries(marketData).forEach(([name, data], index) => {{
  const card = document.createElement("div");
  card.className = "card";

  const canvasId = "chart" + index;

  card.innerHTML = `
    <h2>${{name}} - 1 Year</h2>
    <canvas id="${{canvasId}}"></canvas>
  `;

  chartsDiv.appendChild(card);

  const labels = data.chart.map(item => item.date);
  const prices = data.chart.map(item => item.price);

  new Chart(document.getElementById(canvasId), {{
    type: "line",
    data: {{
      labels: labels,
      datasets: [{{
        label: name,
        data: prices,
        borderWidth: 2,
        tension: 0.25,
        pointRadius: 0
      }}]
    }},
    options: {{
      responsive: true,
      plugins: {{
        legend: {{
          display: false
        }}
      }},
      scales: {{
        x: {{
          ticks: {{
            maxTicksLimit: 6
          }}
        }}
      }}
    }}
  }});
}});

const signalsDiv = document.getElementById("signals");

Object.entries(signals).forEach(([name, signal]) => {{
  const card = document.createElement("div");
  card.className = "card";

  card.innerHTML = `
    <h2>${{name}}</h2>
    <p>${{signal}}</p>
  `;

  signalsDiv.appendChild(card);
}});

const viewsDiv = document.getElementById("views");

Object.entries(views).forEach(([asset, data]) => {{
  const card = document.createElement("div");
  card.className = "card";

  let headlines = "";

  if (data.headlines && data.headlines.length > 0) {{
    headlines = "<ul>" + data.headlines.map(item => `<li>${{item.title}}</li>`).join("") + "</ul>";
  }} else {{
    headlines = "<p>No headlines found.</p>";
  }}

  card.innerHTML = `
    <h2>${{asset}}</h2>
    <p><strong>${{data.sentiment}}</strong></p>
    <p>Positive score: ${{data.positive_score}} | Negative score: ${{data.negative_score}}</p>
    ${{headlines}}
  `;

  viewsDiv.appendChild(card);
}});
</script>

</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
