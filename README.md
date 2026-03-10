# Macro Economics Tracker
### Team: KVZ Clan

An intelligent dashboard for asset managers that transforms fragmented market news into actionable insights. It uses sentiment classification to track evolving macroeconomic themes, highlighting **HOT** (trending/high-risk) vs **COOL** (stable/low-risk) developments, and maps them to specific financial risk outcomes.

## Key Features
- **Real FRED Data Integration** — Pulls live macroeconomic data from the Federal Reserve (CPI, GDP, Unemployment, Housing Starts, NASDAQ, Oil)
- **Sentiment Heatmaps** — Visual HOT vs COOL classification with color-coded heat bars
- **Cross-Market Impact Chains** — Shows causal relationships between macro sectors
- **Institutional Memory** — Persists and logs past market developments over time
- **Trend-Change Alerts** — Detects when a sector flips from HOT to COOL or vice versa
- **Risk Mapping** — Automatically maps macro themes to financial risk outcomes
- **Live News Ticker** — Scrolling banner with breaking macro alerts
- **Sentiment History Charts** — Click any theme to see tracked sentiment over time
- **Theme Distribution** — Donut chart showing event distribution across sectors
- **AI Analysis Panel** — Market-wide narrative summary with risk assessment

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React.js, Recharts |
| Backend | Python, Flask, Flask-CORS |
| Data | FRED API (Federal Reserve Economic Data) |
| Deployment | Railway (Docker) |
| Design | Figma |

## Getting Started (Local Development)

### Prerequisites
- Python 3.10+
- Node.js 18+
- (Optional) FRED API key for real data — [Get one free here](https://fred.stlouisfed.org/docs/api/api_key.html)

### Backend
```bash
cd backend
pip install -r ../requirements.txt

# Optional: enable real FRED data (works without it in simulation mode)
set FRED_API_KEY=your_key_here

python app.py
```
The API server starts at `http://127.0.0.1:5000`.

### Frontend
```bash
cd frontend
npm install
npm start
```
The dashboard opens at `http://localhost:3000`.

## Deployment (Railway)

### Quick Deploy
1. Push this repo to GitHub
2. Go to [railway.app](https://railway.app) and create a new project
3. Select "Deploy from GitHub repo"
4. Railway auto-detects the Dockerfile and builds everything
5. Add environment variable `FRED_API_KEY` in the Railway dashboard (Settings > Variables)
6. Railway assigns a public URL like `https://your-app.up.railway.app`

### What happens on deploy
- React frontend is built with `REACT_APP_API_URL=''` (same-origin)
- Flask serves both the API endpoints and the React build
- Single service, single URL — no separate frontend/backend hosting needed

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/trends` | GET | Latest state for all 6 macro themes |
| `/api/memory` | GET | Recent institutional memory (last 50 events) |
| `/api/summary` | GET | AI-generated market summary and narrative |
| `/api/alerts` | GET | Trend-change alerts (HOT/COOL flips) |
| `/api/impacts/<theme>` | GET | Cross-market causal impact chain |
| `/api/distribution` | GET | Sentiment distribution across themes |
| `/api/theme-history/<theme>` | GET | Historical sentiment data for charting |

## Data Sources

When `FRED_API_KEY` is set, the dashboard pulls real data from:
| Series | Theme | Description |
|--------|-------|-------------|
| CPIAUCSL | Inflation | Consumer Price Index |
| GDP | GDP | Gross Domestic Product |
| UNRATE | Employment | Unemployment Rate |
| HOUST | Housing | Housing Starts |
| NASDAQCOM | Tech | NASDAQ Composite |
| DCOILWTICO | Energy | Crude Oil Price (WTI) |

Without a key, the app runs in simulation mode with realistic mock data.

## Project Structure
```
├── backend/
│   ├── app.py            # Flask REST API + serves React build
│   ├── analyzer.py       # MacroTracker engine (sentiment, risk, memory, impacts)
│   └── data_fetcher.py   # FRED API integration
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── Dashboard.js  # Main dashboard (tabbed layout, 10+ sub-components)
│   │   ├── Dashboard.css # Styles
│   │   └── index.js
│   └── public/
├── Dockerfile            # Multi-stage build for Railway deployment
├── railway.json          # Railway config
├── nixpacks.toml         # Nixpacks config (Railway alternative)
├── Procfile              # Process file
├── requirements.txt
└── README.md
```
