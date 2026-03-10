# Global Macro Tracker — 5-Minute Video Script
### Team Pandas (4 speakers)

---

## SPEAKER 1 — The Problem & Vision (0:00 - 1:15)

**[Screen: Title slide or dashboard landing page]**

"Hey everyone, we're Pandas and this is the Global Macro Tracker."

"So here's the problem we set out to solve. If you're an asset manager or portfolio analyst today, you're drowning in data. CPI reports, GDP revisions, employment numbers, oil prices, tech earnings — they come from dozens of different sources, in different formats, at different times. By the time you piece together the full picture, the market has already moved."

"We asked ourselves: what if we could take all of that fragmented macro data and turn it into a single, real-time intelligence dashboard — one that doesn't just show you what's happening, but tells you what it means for your portfolio?"

**[Screen: Show the live dashboard with cards updating]**

"That's the Global Macro Tracker. It monitors six core macro sectors — Inflation, GDP, Employment, Housing, Tech, and Energy — and classifies each one as either HOT, meaning elevated risk, or COOL, meaning stable. It updates live, every ten seconds, and gives you actionable portfolio signals so you can make decisions faster."

"Let me hand it over to [Speaker 2] to walk you through the core features."

---

## SPEAKER 2 — Overview Tab & Core Features (1:15 - 2:30)

**[Screen: Overview tab visible]**

"Thanks. So what you're looking at here is the Overview tab. Right at the top we have the Market Pulse — this is our aggregate risk gauge. It scores the entire market from 0 to 100 based on how many sectors are running hot and how intense those signals are. Right now it's sitting at [read the number], which means [interpret it]."

"Next to it we track total events processed, the number of trend flips we've detected, and which sector is currently the most volatile."

**[Screen: Click on a theme card on the left]**

"On the left side, these are our Live Market Theme cards. Each card shows the sector name, a sentiment score as a percentage, a HOT or COOL badge, and the latest headline driving that classification. When I click one — say Inflation — the chart on the right updates to show its sentiment history over time."

**[Screen: Scroll down to AI Analysis panel]**

"Below the chart is our AI Analysis panel. This generates a written market narrative automatically — it tells you how many sectors are running hot, what the overall risk level is, and which theme is dominating the market right now. For an asset manager, this is your morning briefing in two seconds."

"Now [Speaker 3] will show you the real analytical power under the hood."

---

## SPEAKER 3 — Impacts, Analytics & Portfolio Signals (2:30 - 3:50)

**[Screen: Click Impacts tab]**

"So this is where it gets really interesting. The Impacts tab shows cross-market causal chains. When I select a theme — let's say Inflation — it maps out exactly how inflation movements ripple across other sectors. Inflation affects Housing through mortgage rates, it affects Energy through input costs, it affects Employment through wage pressure. Each link has a severity score so you can see which connections are the strongest."

**[Screen: Scroll down to Portfolio Signal panel]**

"And at the bottom, we generate a Portfolio Signal for the selected sector. Based on the recent activity pattern — the HOT percentage, the momentum direction, the volatility — our engine recommends an action. It might say Hedge, Reduce Exposure, Accumulate, or Hold, along with a rationale explaining why. This turns raw data into a decision."

**[Screen: Click Analytics tab]**

"Switching to Analytics — here we have our theme distribution donut chart showing how events are spread across sectors, the sector breakdown table with bias badges, and two new panels. The Volatility Ranking chart shows which sectors are fluctuating the most, and the Theme Momentum grid tells you whether each sector is heating up, cooling down, or flat — with a visual HOT-to-COOL ratio bar."

"Over to [Speaker 4] to cover the data pipeline and tech."

---

## SPEAKER 4 — Data, Memory & Tech Stack (3:50 - 5:00)

**[Screen: Click Memory tab]**

"Thanks. So every event our engine processes gets logged in Institutional Memory — you can see it here in the Memory tab. At the top we have stats: total events tracked, the HOT rate percentage, how many themes are active, and the time span covered. You can filter by any sector using these chips — click Inflation and you only see inflation events."

"Each entry has a colored border — red for HOT, blue for COOL — plus the sentiment score, timestamp, headline, and risk implication. This is your audit trail."

**[Screen: Show the news ticker scrolling at the top]**

"The ticker at the top scrolls all recent headlines in real time, and if a sector flips from HOT to COOL or vice versa, you get an alert banner right below the header."

**[Screen: Switch to a slide or show the README/tech stack]**

"On the technical side — the frontend is React with Recharts for all the visualizations. The backend is Python and Flask, serving both the API and the React build as a single service. For real data, we integrate with the FRED API — that's the Federal Reserve Economic Data — pulling live series for CPI, GDP, unemployment, housing starts, NASDAQ, and oil prices. The whole thing is deployed on Railway using a multi-stage Docker build."

"What makes this project special is that it's not just a dashboard — it's an analytical engine. It computes volatility, tracks momentum, detects regime changes, maps causal impacts, and generates portfolio-level recommendations, all updating in real time."

**[Screen: Show the live dashboard one final time]**

"We're Pandas, and this is the Global Macro Tracker. Thanks for watching."

---

## Tips for Recording

- **Total runtime target**: 5:00 (each speaker gets roughly 1:00 - 1:20)
- **Screen recording**: Use OBS or the built-in screen recorder. Keep the dashboard open in fullscreen on Chrome
- **Transitions**: Each speaker can record their segment separately if needed, then stitch together. Or do it live with handoffs
- **Audio**: Use a decent microphone or quiet room. Speak at a steady pace — don't rush
- **Before recording**: Let the dashboard run for 30-60 seconds first so it has populated data in all tabs (memory, charts, distribution, etc.)
- **Backup plan**: If the live site is slow, run it locally with `python backend/app.py` and `npm start` — it looks identical
- **Engagement**: When demoing a tab, actually click things on screen — click theme cards, switch tabs, click filter chips. Movement keeps the video engaging
- **Time check**: Practice once through with a timer. Cut filler words. Each section should feel tight
