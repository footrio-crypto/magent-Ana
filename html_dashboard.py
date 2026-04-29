import json
import datetime


def create_html_dashboard(results, signals, market_views, alerts):
    updated_at = datetime.datetime.utcnow().strftime("%B %d, %Y %I:%M %p UTC")

    data_json = json.dumps(results)
    signals_json = json.dumps(signals)
    views_json = json.dumps(market_views)
    alerts_json = json.dumps(alerts)

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="theme-color" content="#020617" />
  <title>Market Intelligence Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <style>
    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      font-family: Inter, Arial, Helvetica, sans-serif;
      background:
        radial-gradient(circle at top left, rgba(12, 42, 72, 0.85), transparent 35%),
        radial-gradient(circle at top right, rgba(30, 20, 70, 0.45), transparent 28%),
        linear-gradient(135deg, #020617 0%, #07111f 48%, #020617 100%);
      color: #f8fafc;
      min-height: 100vh;
    }}

    .app {{
      max-width: 1540px;
      margin: 0 auto;
      padding: 28px 30px 20px;
    }}

    header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 22px;
      margin-bottom: 22px;
    }}

    .brand {{
      display: flex;
      gap: 18px;
      align-items: center;
    }}

    .logo {{
      width: 54px;
      height: 54px;
      border: 2px solid rgba(255,255,255,0.9);
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 30px;
      color: white;
    }}

    h1 {{
      margin: 0;
      font-size: 34px;
      letter-spacing: -0.8px;
    }}

    .subtitle {{
      margin-top: 6px;
      color: #cbd5e1;
      font-size: 16px;
    }}

    .updated {{
      text-align: right;
      font-size: 14px;
      color: #cbd5e1;
    }}

    .refresh {{
      margin-top: 8px;
      display: inline-flex;
      width: 48px;
      height: 48px;
      border-radius: 12px;
      border: 1px solid rgba(148,163,184,0.35);
      align-items: center;
      justify-content: center;
      font-size: 24px;
      background: rgba(15,23,42,0.75);
      cursor: pointer;
    }}

    .top-grid {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 16px;
      margin-bottom: 16px;
    }}

    .card {{
      background: linear-gradient(180deg, rgba(15,23,42,0.92), rgba(8,18,31,0.94));
      border: 1px solid rgba(148,163,184,0.24);
      border-radius: 14px;
      box-shadow: 0 18px 45px rgba(0,0,0,0.30);
      overflow: hidden;
    }}

    .metric-card {{
      padding: 20px;
      min-height: 118px;
      display: flex;
      gap: 16px;
      align-items: center;
    }}

    .metric-icon {{
      width: 58px;
      height: 58px;
      border-radius: 999px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 30px;
      flex-shrink: 0;
    }}

    .gold-bg {{ background: rgba(250,204,21,0.18); }}
    .silver-bg {{ background: rgba(203,213,225,0.16); }}
    .dbs-bg {{ background: rgba(239,68,68,0.18); }}
    .boc-bg {{ background: rgba(220,38,38,0.18); }}
    .ai-bg {{ background: rgba(168,85,247,0.20); }}

    .metric-title {{
      font-size: 16px;
      font-weight: 900;
      margin-bottom: 6px;
    }}

    .metric-price {{
      font-size: 27px;
      font-weight: 900;
      margin-bottom: 6px;
      letter-spacing: -0.4px;
    }}

    .positive {{ color: #22c55e; }}
    .negative {{ color: #ff3b30; }}
    .neutral {{ color: #facc15; }}
    .purple {{ color: #a78bfa; }}

    .alert {{
      margin-bottom: 14px;
      padding: 14px 20px;
      border-radius: 12px;
      border: 1px solid rgba(148,163,184,0.22);
      background: rgba(15,23,42,0.86);
      border-left: 4px solid #facc15;
      font-weight: 900;
    }}

    .main-grid {{
      display: grid;
      grid-template-columns: 1.45fr 0.95fr;
      gap: 18px;
      margin-bottom: 18px;
    }}

    .bottom-grid {{
      display: grid;
      grid-template-columns: 1.05fr 0.95fr;
      gap: 18px;
    }}

    .panel-title {{
      padding: 18px 22px 8px;
      font-size: 20px;
      font-weight: 900;
    }}

    .small-title {{
      font-size: 14px;
      color: #cbd5e1;
      margin-left: 6px;
      font-weight: 500;
    }}

    .chart-card {{
      padding: 0 22px 20px;
      height: 360px;
    }}

    .tabs {{
      display: flex;
      gap: 10px;
      margin-bottom: 16px;
      flex-wrap: wrap;
    }}

    .tab {{
      padding: 9px 17px;
      border-radius: 8px;
      background: rgba(15,23,42,0.88);
      border: 1px solid rgba(148,163,184,0.28);
      color: #e5e7eb;
      font-weight: 900;
      cursor: pointer;
      user-select: none;
    }}

    .tab.active {{
      background: #2563eb;
      border-color: #60a5fa;
      color: white;
      box-shadow: 0 0 20px rgba(37,99,235,0.35);
    }}

    #combinedChart {{
      height: 275px !important;
    }}

    .insights {{
      padding: 8px 24px 22px;
    }}

    .insight-row {{
      display: grid;
      grid-template-columns: 58px 1fr;
      gap: 16px;
      padding: 18px 0;
      border-bottom: 1px solid rgba(148,163,184,0.16);
    }}

    .insight-row:last-child {{
      border-bottom: none;
    }}

    .insight-icon {{
      width: 52px;
      height: 52px;
      border-radius: 999px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 25px;
    }}

    .insight-title {{
      font-size: 17px;
      font-weight: 900;
      margin-bottom: 7px;
    }}

    .insight-text {{
      color: #d1d5db;
      font-size: 15px;
      line-height: 1.45;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
    }}

    th, td {{
      padding: 14px 18px;
      text-align: left;
      border-bottom: 1px solid rgba(148,163,184,0.15);
      font-size: 15px;
    }}

    th {{
      background: rgba(15,23,42,0.35);
      font-weight: 900;
    }}

    .signal-badge {{
      font-weight: 900;
    }}

    .buy {{ color: #22c55e; }}
    .hold {{ color: #facc15; }}
    .watch {{ color: #60a5fa; }}
    .risk, .wait, .sell {{ color: #ff5a3d; }}

    .strength {{
      display: flex;
      gap: 5px;
    }}

    .bar {{
      width: 10px;
      height: 17px;
      border-radius: 3px;
      background: rgba(71,85,105,0.88);
    }}

    .bar.on.green {{ background: #22c55e; }}
    .bar.on.yellow {{ background: #facc15; }}
    .bar.on.blue {{ background: #3b82f6; }}

    .view-row {{
      display: grid;
      grid-template-columns: 38px 135px 1fr;
      gap: 14px;
      align-items: center;
      padding: 14px 22px;
      border-bottom: 1px solid rgba(148,163,184,0.15);
    }}

    .source-icon {{
      width: 30px;
      height: 30px;
      border-radius: 7px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #334155;
      font-weight: 900;
    }}

    .source-name {{
      font-weight: 900;
    }}

    .headline {{
      color: #d1d5db;
      font-size: 14px;
      line-height: 1.35;
    }}

    .disclaimer {{
      margin-top: 18px;
      color: #9ca3af;
      font-size: 14px;
      text-align: center;
    }}

    @media (max-width: 1100px) {{
      .top-grid {{
        grid-template-columns: repeat(2, 1fr);
      }}

      .main-grid,
      .bottom-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    @media (max-width: 640px) {{
      .app {{
        padding: 14px;
      }}

      header {{
        flex-direction: column;
      }}

      .brand {{
        align-items: flex-start;
      }}

      h1 {{
        font-size: 25px;
      }}

      .subtitle {{
        font-size: 14px;
      }}

      .updated {{
        text-align: left;
      }}

      .top-grid {{
        grid-template-columns: 1fr;
      }}

      .metric-card {{
        min-height: 104px;
      }}

      .main-grid,
      .bottom-grid {{
        gap: 14px;
      }}

      .chart-card {{
        height: 330px;
        padding: 0 14px 16px;
      }}

      th, td {{
        padding: 10px 8px;
        font-size: 12px;
      }}

      .view-row {{
        grid-template-columns: 32px 1fr;
      }}

      .headline {{
        grid-column: 2 / 3;
      }}
    }}
  </style>
</head>

<body>
<div class="app">

  <header>
    <div class="brand">
      <div class="logo">↗</div>
      <div>
        <h1>Market Intelligence Dashboard</h1>
        <div class="subtitle">Daily Market Overview with AI Insights & External Intelligence</div>
      </div>
    </div>
    <div class="updated">
      <div>Last Updated:</div>
      <strong>{updated_at}</strong>
      <div class="refresh" onclick="location.reload()">↻</div>
    </div>
  </header>

  <div class="top-grid" id="topCards"></div>
  <div id="alerts"></div>

  <div class="main-grid">
    <section class="card">
      <div class="panel-title">Price Trends <span class="small-title" id="rangeLabel">(1 Year)</span></div>
      <div class="chart-card">
        <div class="tabs">
          <div class="tab active" data-range="5y">5Y</div>
          <div class="tab" data-range="3y">3Y</div>
          <div class="tab" data-range="1y">1Y</div>
          <div class="tab" data-range="ytd">YTD</div>
          <div class="tab" data-range="1m">1M</div>
          <div class="tab" data-range="5d">5D</div>
        </div>
        <canvas id="combinedChart"></canvas>
      </div>
    </section>

    <section class="card">
      <div class="panel-title">AI Market Insights</div>
      <div class="insights" id="insights"></div>
    </section>
  </div>

  <div class="bottom-grid">
    <section class="card">
      <div class="panel-title">Trading Signals</div>
      <table>
        <thead>
          <tr>
            <th>Market</th>
            <th>Signal</th>
            <th>Strength</th>
            <th>Key Level</th>
            <th>Outlook</th>
          </tr>
        </thead>
        <tbody id="signalRows"></tbody>
      </table>
    </section>

    <section class="card">
      <div class="panel-title">External Market Views</div>
      <div id="views"></div>
    </section>
  </div>

  <div class="disclaimer">
    Disclaimer: This dashboard is for informational and educational purposes only and not financial advice.
  </div>

</div>

<script>
const marketData = {data_json};
const signals = {signals_json};
const views = {views_json};
const alerts = {alerts_json};

function pctClass(value) {{
  if (value > 0) return "positive";
  if (value < 0) return "negative";
  return "neutral";
}}

function symbolFor(name) {{
  const symbols = {{
    "Gold": "🟡",
    "Silver": "⚪",
    "DBS": "✖️",
    "Bank of China": "⭕",
    "NVIDIA": "🧠",
    "AI Stocks": "🧠"
  }};
  return symbols[name] || "📊";
}}

function iconClass(name) {{
  if (name === "Gold") return "gold-bg";
  if (name === "Silver") return "silver-bg";
  if (name === "DBS") return "dbs-bg";
  if (name === "Bank of China") return "boc-bg";
  return "ai-bg";
}}

function formatPrice(name, price) {{
  if (name === "DBS") return "S$" + price;
  if (name === "Bank of China") return "HK$" + price;
  return "$" + price;
}}

function badgeClass(signal) {{
  const s = String(signal).toLowerCase();
  if (s.includes("buy")) return "buy";
  if (s.includes("risk")) return "risk";
  if (s.includes("sell")) return "sell";
  if (s.includes("wait")) return "wait";
  if (s.includes("watch")) return "watch";
  return "hold";
}}

function strengthColor(signal) {{
  const s = String(signal).toLowerCase();
  if (s.includes("wait") || s.includes("hold")) return "yellow";
  if (s.includes("watch")) return "blue";
  return "green";
}}

function strengthBars(level, signal) {{
  const color = strengthColor(signal);
  let html = '<div class="strength">';
  for (let i = 1; i <= 5; i++) {{
    html += `<span class="bar ${{i <= level ? "on " + color : ""}}"></span>`;
  }}
  html += '</div>';
  return html;
}}

const topCards = document.getElementById("topCards");
const preferredTop = ["Gold", "Silver", "DBS", "Bank of China", "NVIDIA"];

preferredTop.forEach(name => {{
  if (!marketData[name]) return;
  const data = marketData[name];

  let title = name;
  if (name === "Gold") title = "Gold (XAU/USD)";
  if (name === "Silver") title = "Silver (XAG/USD)";
  if (name === "DBS") title = "DBS Group (D05.SI)";
  if (name === "Bank of China") title = "Bank of China (3988.HK)";
  if (name === "NVIDIA") title = "AI Market Sentiment";

  let priceText = formatPrice(name, data.price);
  let changeText = `${{data["1d"]}}%`;
  let changeClass = pctClass(data["1d"]);

  if (name === "NVIDIA") {{
    const aiSignal = signals["AI Stocks"] ? signals["AI Stocks"].signal : "Neutral";
    priceText = aiSignal;
    changeText = "Confidence: " + ((signals["AI Stocks"]?.strength || 3) * 20) + "%";
    changeClass = "purple";
  }}

  const card = document.createElement("div");
  card.className = "card metric-card";
  card.innerHTML = `
    <div class="metric-icon ${{iconClass(name)}}">${{symbolFor(name)}}</div>
    <div>
      <div class="metric-title">${{title}}</div>
      <div class="metric-price ${{name === "NVIDIA" ? "purple" : ""}}">${{priceText}}</div>
      <div class="${{changeClass}}"><strong>${{changeText}}</strong></div>
    </div>
  `;
  topCards.appendChild(card);
}});

const alertsDiv = document.getElementById("alerts");
alerts.forEach(alert => {{
  const div = document.createElement("div");
  div.className = "alert";
  div.innerHTML = "⚠️ " + alert;
  alertsDiv.appendChild(div);
}});

const chartNames = ["Gold", "Silver", "DBS", "Bank of China"];
const chartColors = {{
  "Gold": "#facc15",
  "Silver": "#e5e7eb",
  "DBS": "#ff3b30",
  "Bank of China": "#22c55e"
}};

let chartInstance = null;

function cutoffDate(range) {{
  const now = new Date();
  if (range === "5d") now.setDate(now.getDate() - 5);
  if (range === "1m") now.setMonth(now.getMonth() - 1);
  if (range === "ytd") return new Date(new Date().getFullYear(), 0, 1);
  if (range === "1y") now.setFullYear(now.getFullYear() - 1);
  if (range === "3y") now.setFullYear(now.getFullYear() - 3);
  if (range === "5y") now.setFullYear(now.getFullYear() - 5);
  return now;
}}

function rangeLabel(range) {{
  return {{
    "5d": "(5 Days)",
    "1m": "(1 Month)",
    "ytd": "(Year To Date)",
    "1y": "(1 Year)",
    "3y": "(3 Years)",
    "5y": "(5 Years)"
  }}[range];
}}

function buildChart(range) {{
  const cutoff = cutoffDate(range);
  const firstName = chartNames.find(n => marketData[n]);
  const filteredFirst = marketData[firstName].chart.filter(item => new Date(item.date) >= cutoff);
  const labels = filteredFirst.map(item => item.date);

  const datasets = chartNames
    .filter(name => marketData[name])
    .map(name => {{
      const series = marketData[name].chart.filter(item => new Date(item.date) >= cutoff);
      const first = series.length ? series[0].price : 1;
      const normalized = series.map(item => Number((((item.price - first) / first) * 100).toFixed(2)));

      return {{
        label: name,
        data: normalized,
        borderColor: chartColors[name],
        backgroundColor: chartColors[name],
        borderWidth: 2,
        tension: 0.25,
        pointRadius: 0
      }};
    }});

  if (chartInstance) chartInstance.destroy();

  chartInstance = new Chart(document.getElementById("combinedChart"), {{
    type: "line",
    data: {{ labels, datasets }},
    options: {{
      responsive: true,
      maintainAspectRatio: false,
      plugins: {{
        legend: {{
          position: "right",
          labels: {{
            color: "#e5e7eb",
            boxWidth: 10,
            boxHeight: 10,
            usePointStyle: true
          }}
        }},
        tooltip: {{
          callbacks: {{
            label: context => context.dataset.label + ": " + context.parsed.y + "%"
          }}
        }}
      }},
      scales: {{
        x: {{
          ticks: {{ color: "#cbd5e1", maxTicksLimit: 7 }},
          grid: {{ color: "rgba(148,163,184,0.12)" }}
        }},
        y: {{
          ticks: {{
            color: "#cbd5e1",
            callback: value => value + "%"
          }},
          grid: {{ color: "rgba(148,163,184,0.14)" }}
        }}
      }}
    }}
  }});

  document.getElementById("rangeLabel").textContent = rangeLabel(range);
}}

document.querySelectorAll(".tab").forEach(tab => {{
  tab.addEventListener("click", () => {{
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    tab.classList.add("active");
    buildChart(tab.dataset.range);
  }});
}});

buildChart("5y");

const insights = document.getElementById("insights");
insights.innerHTML = `
  <div class="insight-row">
    <div class="insight-icon" style="background:rgba(34,197,94,0.15); color:#22c55e;">↗</div>
    <div>
      <div class="insight-title positive">Precious Metals</div>
      <div class="insight-text">Gold signal is <strong>${{signals["Gold"]?.signal || "HOLD"}}</strong>. Monitor safe-haven demand, USD direction, and inflation expectations.</div>
    </div>
  </div>

  <div class="insight-row">
    <div class="insight-icon" style="background:rgba(239,68,68,0.15); color:#ef4444;">🏦</div>
    <div>
      <div class="insight-title negative">Financial Markets</div>
      <div class="insight-text">DBS signal is <strong>${{signals["DBS"]?.signal || "HOLD"}}</strong>. Bank of China remains policy-sensitive and linked to China macro sentiment.</div>
    </div>
  </div>

  <div class="insight-row">
    <div class="insight-icon" style="background:rgba(168,85,247,0.15); color:#a78bfa;">🌐</div>
    <div>
      <div class="insight-title purple">Overall Sentiment</div>
      <div class="insight-text">AI market signal is <strong>${{signals["AI Stocks"]?.signal || "HOLD"}}</strong>. Monitor DeepSeek disruption, valuation pressure, and momentum shifts.</div>
    </div>
  </div>
`;

const signalRows = document.getElementById("signalRows");
Object.entries(signals).forEach(([market, data]) => {{
  const row = document.createElement("tr");
  row.innerHTML = `
    <td>${{symbolFor(market)}} ${{market}}</td>
    <td><span class="signal-badge ${{badgeClass(data.signal)}}">${{data.signal}}</span></td>
    <td>${{strengthBars(data.strength || 3, data.signal)}}</td>
    <td>${{data.key_level || "-"}}</td>
    <td><span class="${{badgeClass(data.signal)}}">${{data.outlook || "-"}}</span></td>
  `;
  signalRows.appendChild(row);
}});

const viewsDiv = document.getElementById("views");
Object.entries(views).slice(0, 5).forEach(([asset, data]) => {{
  let headline = "No headline found.";
  if (data.headlines && data.headlines.length > 0) headline = data.headlines[0].title;

  const row = document.createElement("div");
  row.className = "view-row";
  row.innerHTML = `
    <div class="source-icon">${{asset[0]}}</div>
    <div class="source-name">${{asset}}</div>
    <div class="headline">${{headline}}</div>
  `;
  viewsDiv.appendChild(row);
}});
</script>

</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
