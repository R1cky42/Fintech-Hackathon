import datetime
import random
from data_fetcher import fetch_all_themes, is_available as fred_available

# Cross-market causal impact map
# Each theme lists which other themes it influences and how
IMPACT_MAP = {
    "Inflation": {
        "GDP": "Rising inflation erodes purchasing power and slows growth",
        "Employment": "Cost pressures may trigger layoffs in rate-sensitive sectors",
        "Housing": "Higher inflation drives mortgage rate increases",
        "Energy": "Inflation expectations push commodity speculation"
    },
    "GDP": {
        "Employment": "Slowing growth leads to hiring freezes and reduced payrolls",
        "Tech": "GDP contraction reduces enterprise IT spending",
        "Energy": "Weak demand lowers energy consumption forecasts"
    },
    "Employment": {
        "GDP": "Strong labor markets support consumer-driven growth",
        "Inflation": "Tight labor pushes wages up, fueling demand-pull inflation",
        "Housing": "Employment gains boost mortgage applications"
    },
    "Housing": {
        "GDP": "Housing slowdown drags on construction and related GDP",
        "Employment": "Declining starts reduce construction and real estate jobs",
        "Inflation": "Shelter costs are a major component of CPI"
    },
    "Tech": {
        "GDP": "Tech sector drives productivity and growth",
        "Employment": "Tech hiring/layoffs ripple across the labor market",
        "Energy": "Data center expansion increases energy demand"
    },
    "Energy": {
        "Inflation": "Energy prices feed directly into CPI and PPI",
        "GDP": "High energy costs reduce margins and slow growth",
        "Tech": "Energy costs impact cloud and data center economics"
    }
}


class MacroTracker:
    def __init__(self):
        self.institutional_memory = []
        self.alerts = []
        self.real_data = None         # Cached FRED data
        self.data_source = "simulated"
        self._seed_real_data()

    def _seed_real_data(self):
        """On startup, try to fetch real FRED data and seed the dashboard."""
        if not fred_available():
            print("[MacroTracker] No FRED_API_KEY set — running in simulation mode")
            return

        print("[MacroTracker] Fetching real data from FRED...")
        data = fetch_all_themes()
        if data:
            self.real_data = data
            self.data_source = "live"
            # Seed institutional memory with one real event per theme
            for theme, info in data.items():
                self.add_market_event(theme, info['headline'], info['sentiment_score'])
            print(f"[MacroTracker] Loaded real data for {len(data)} themes")
        else:
            print("[MacroTracker] FRED fetch failed — falling back to simulation")

    def add_market_event(self, theme, news_snippet, sentiment_score):
        """Stores news and identifies risk implications."""
        event = {
            "timestamp": datetime.datetime.now(),
            "theme": theme,
            "content": news_snippet,
            "sentiment_score": round(sentiment_score, 2),
            "sentiment": "HOT" if sentiment_score > 0.7 else "COOL",
            "risk_implication": self.calculate_risk(theme, sentiment_score)
        }

        # Attach real data values if available
        if self.real_data and theme in self.real_data:
            rd = self.real_data[theme]
            event["real_value"] = rd["current_value"]
            event["real_unit"] = rd["unit"]
            event["real_label"] = rd["label"]
            event["real_change"] = rd["change_pct"]
            event["real_date"] = rd["date"]

        # Detect trend flips
        self._detect_trend_change(event)

        self.institutional_memory.append(event)
        return event

    def _detect_trend_change(self, new_event):
        """Detects when a theme flips from HOT to COOL or vice versa."""
        theme = new_event['theme']
        previous = None
        for e in reversed(self.institutional_memory):
            if e['theme'] == theme:
                previous = e
                break

        if previous and previous['sentiment'] != new_event['sentiment']:
            direction = "heated up" if new_event['sentiment'] == "HOT" else "cooled down"
            self.alerts.append({
                "timestamp": new_event['timestamp'],
                "type": "TREND_FLIP",
                "theme": theme,
                "from": previous['sentiment'],
                "to": new_event['sentiment'],
                "message": f"{theme} has {direction}: {new_event['content']}"
            })
            self.alerts = self.alerts[-10:]

    def calculate_risk(self, theme, score):
        """Maps themes to specific financial risk outcomes, scaled by sentiment score."""
        risks = {
            "Inflation": "Increased Interest Rate Volatility",
            "GDP": "Currency Strength Fluctuations",
            "Employment": "Consumer Spending Shift",
            "Housing": "Real Estate Market Correction",
            "Tech": "Growth Stock Repricing",
            "Energy": "Commodity Price Disruption"
        }
        base_risk = risks.get(theme, "General Market Volatility")
        severity = "High" if score > 0.7 else "Moderate" if score > 0.4 else "Low"
        return f"{base_risk} ({severity})"

    def get_latest_by_theme(self):
        """Returns the most recent event for each theme."""
        all_themes = ["Inflation", "GDP", "Employment", "Housing", "Tech", "Energy"]
        latest = {}
        for e in reversed(self.institutional_memory):
            if e['theme'] not in latest:
                latest[e['theme']] = e
            if len(latest) == len(all_themes):
                break
        return [latest[t] for t in all_themes if t in latest]

    def simulate_cycle(self):
        """Simulates 1-2 new market events per cycle, returns latest state for all themes."""
        count = random.choice([1, 2])
        for _ in range(count):
            self.simulate_live_feed()
        return self.get_latest_by_theme()

    def get_memory(self, limit=50):
        """Returns the most recent events from institutional memory."""
        return self.institutional_memory[-limit:]

    def get_theme_history(self, theme):
        """Returns all events for a specific theme, for charting."""
        events = [e for e in self.institutional_memory if e['theme'] == theme]
        return events[-30:]

    def get_cross_impacts(self, theme):
        """Returns the cross-market impacts for a given theme."""
        impacts = IMPACT_MAP.get(theme, {})
        result = []
        for target_theme, description in impacts.items():
            latest = None
            for e in reversed(self.institutional_memory):
                if e['theme'] == target_theme:
                    latest = e
                    break
            result.append({
                "target": target_theme,
                "description": description,
                "target_sentiment": latest['sentiment'] if latest else "UNKNOWN",
                "target_score": latest['sentiment_score'] if latest else 0
            })
        return result

    def get_theme_distribution(self):
        """Returns sentiment distribution across all themes."""
        if not self.institutional_memory:
            return []

        themes = {}
        for e in self.institutional_memory:
            t = e['theme']
            if t not in themes:
                themes[t] = {"theme": t, "hot": 0, "cool": 0, "total": 0, "avg_score": 0}
            themes[t]["total"] += 1
            themes[t]["avg_score"] += e['sentiment_score']
            if e['sentiment'] == "HOT":
                themes[t]["hot"] += 1
            else:
                themes[t]["cool"] += 1

        result = []
        for t in themes.values():
            t["avg_score"] = round(t["avg_score"] / t["total"], 2)
            result.append(t)
        return sorted(result, key=lambda x: x["total"], reverse=True)

    def get_summary(self):
        """Generates a market summary from recent institutional memory."""
        if not self.institutional_memory:
            return {
                "overall_sentiment": "NEUTRAL",
                "hot_count": 0,
                "cool_count": 0,
                "dominant_theme": None,
                "risk_level": "Low",
                "narrative": "No market data available yet. Awaiting first data feed."
            }

        recent = self.institutional_memory[-20:]
        hot_count = sum(1 for e in recent if e['sentiment'] == 'HOT')
        cool_count = len(recent) - hot_count

        theme_counts = {}
        for e in recent:
            theme_counts[e['theme']] = theme_counts.get(e['theme'], 0) + 1
        dominant_theme = max(theme_counts, key=theme_counts.get)

        avg_score = sum(e['sentiment_score'] for e in recent) / len(recent)

        if hot_count > cool_count * 2:
            overall = "RISK-ON"
            risk_level = "Elevated"
        elif hot_count > cool_count:
            overall = "CAUTIOUS"
            risk_level = "Moderate"
        else:
            overall = "STABLE"
            risk_level = "Low"

        hot_themes = list(set(e['theme'] for e in recent if e['sentiment'] == 'HOT'))
        cool_themes = list(set(e['theme'] for e in recent if e['sentiment'] == 'COOL'))

        narrative_parts = []
        narrative_parts.append(
            f"Market conditions are currently {overall.lower()} with an average sentiment intensity of {avg_score:.0%}."
        )
        if hot_themes:
            narrative_parts.append(
                f"Elevated activity detected in {', '.join(hot_themes)}. "
                f"These sectors are showing heightened volatility signals that warrant close monitoring."
            )
        if cool_themes:
            narrative_parts.append(
                f"{', '.join(cool_themes)} {'remains' if len(cool_themes) == 1 else 'remain'} stable with subdued risk indicators."
            )
        narrative_parts.append(
            f"Portfolio recommendation: {'Increase hedging on HOT sectors and review stop-loss levels.' if risk_level != 'Low' else 'Standard monitoring. No immediate action required.'}"
        )

        return {
            "overall_sentiment": overall,
            "hot_count": hot_count,
            "cool_count": cool_count,
            "dominant_theme": dominant_theme,
            "risk_level": risk_level,
            "avg_score": round(avg_score, 2),
            "hot_themes": hot_themes,
            "cool_themes": cool_themes,
            "narrative": " ".join(narrative_parts),
            "data_source": self.data_source,
        }

    def get_analytics_extended(self):
        """Returns extended analytics: volatility, momentum, market pulse, and portfolio signals."""
        themes = ["Inflation", "GDP", "Employment", "Housing", "Tech", "Energy"]

        if len(self.institutional_memory) < 2:
            return {
                "volatility_ranking": [],
                "momentum": {},
                "market_pulse": 50,
                "total_events": len(self.institutional_memory),
                "active_alerts": len(self.alerts),
                "most_volatile": None,
                "portfolio_signals": {},
                "time_range_minutes": 0,
            }

        volatility = {}
        momentum = {}

        for theme in themes:
            events = [e for e in self.institutional_memory if e['theme'] == theme]
            if len(events) < 2:
                volatility[theme] = 0
                momentum[theme] = {"direction": "flat", "strength": 0}
                continue

            scores = [e['sentiment_score'] for e in events]

            # Volatility: standard deviation of scores
            mean = sum(scores) / len(scores)
            variance = sum((s - mean) ** 2 for s in scores) / len(scores)
            volatility[theme] = round(variance ** 0.5, 3)

            # Momentum: compare average of last 5 events vs previous 5
            recent = scores[-5:] if len(scores) >= 5 else scores
            older = scores[-10:-5] if len(scores) >= 10 else scores[:max(1, len(scores) // 2)]
            recent_avg = sum(recent) / len(recent)
            older_avg = sum(older) / len(older)
            diff = recent_avg - older_avg

            if diff > 0.05:
                direction = "heating"
            elif diff < -0.05:
                direction = "cooling"
            else:
                direction = "flat"

            momentum[theme] = {
                "direction": direction,
                "strength": round(abs(diff) * 100, 1),
                "recent_avg": round(recent_avg, 2),
                "older_avg": round(older_avg, 2),
            }

        # Sort by volatility descending
        volatility_ranking = sorted(
            [{"theme": t, "volatility": v} for t, v in volatility.items()],
            key=lambda x: x["volatility"],
            reverse=True
        )

        # Market pulse: 0-100 scale
        recent_20 = self.institutional_memory[-20:]
        hot_ratio = sum(1 for e in recent_20 if e['sentiment'] == 'HOT') / max(len(recent_20), 1)
        avg_intensity = sum(e['sentiment_score'] for e in recent_20) / max(len(recent_20), 1)
        market_pulse = round(hot_ratio * 60 + avg_intensity * 40, 0)

        most_volatile = volatility_ranking[0]["theme"] if volatility_ranking else None

        # Portfolio signals per theme
        portfolio_signals = {}
        for theme in themes:
            events = [e for e in self.institutional_memory if e['theme'] == theme]
            if not events:
                portfolio_signals[theme] = {"action": "Monitor", "rationale": "Insufficient data"}
                continue

            recent = events[-5:] if len(events) >= 5 else events
            hot_pct = sum(1 for e in recent if e['sentiment'] == 'HOT') / len(recent)
            avg = sum(e['sentiment_score'] for e in recent) / len(recent)
            vol = volatility.get(theme, 0)
            mom = momentum.get(theme, {}).get("direction", "flat")

            if hot_pct > 0.6 and mom == "heating":
                action = "Hedge"
                rationale = "Elevated risk with upward momentum — consider protective positions"
            elif hot_pct > 0.6:
                action = "Reduce Exposure"
                rationale = "High activity signals — trim positions in exposed assets"
            elif mom == "cooling" and hot_pct < 0.4:
                action = "Accumulate"
                rationale = "Cooling trend with stabilizing signals — opportunistic entry"
            elif vol > 0.15:
                action = "Watch Closely"
                rationale = "High volatility but no clear direction — await confirmation"
            else:
                action = "Hold"
                rationale = "Stable conditions — maintain current allocation"

            portfolio_signals[theme] = {
                "action": action,
                "rationale": rationale,
                "hot_pct": round(hot_pct * 100),
                "avg_score": round(avg * 100),
            }

        # Time range
        first_ts = self.institutional_memory[0]['timestamp']
        last_ts = self.institutional_memory[-1]['timestamp']
        time_range_minutes = round((last_ts - first_ts).total_seconds() / 60, 1)

        return {
            "volatility_ranking": volatility_ranking,
            "momentum": momentum,
            "market_pulse": int(market_pulse),
            "total_events": len(self.institutional_memory),
            "active_alerts": len(self.alerts),
            "most_volatile": most_volatile,
            "portfolio_signals": portfolio_signals,
            "time_range_minutes": time_range_minutes,
        }

    def simulate_live_feed(self):
        """Generates a simulated headline. If real data is available, scores are
        anchored to actual values with jitter to keep the demo dynamic."""
        headlines = [
            {"theme": "Inflation", "text": "CPI jumps 0.4% — exceeds analyst expectations", "score": 0.9},
            {"theme": "Inflation", "text": "Core PCE rises 0.3%, Fed signals caution", "score": 0.85},
            {"theme": "Inflation", "text": "Producer prices fall 0.1%, easing supply-side pressure", "score": 0.35},
            {"theme": "GDP", "text": "Growth slows to 1.1% amid global headwinds", "score": 0.3},
            {"theme": "GDP", "text": "Q3 GDP revised up to 2.1%, beats consensus", "score": 0.75},
            {"theme": "GDP", "text": "Manufacturing PMI contracts for third month", "score": 0.82},
            {"theme": "Employment", "text": "Jobless claims hit 5-year low, labor market tight", "score": 0.2},
            {"theme": "Employment", "text": "Nonfarm payrolls surge by 300K, wages up", "score": 0.8},
            {"theme": "Employment", "text": "Wage growth cools to 3.2%, in line with target", "score": 0.45},
            {"theme": "Housing", "text": "Mortgage rates climb to 7%, applications plunge", "score": 0.8},
            {"theme": "Housing", "text": "Home sales rebound 4.2% on seasonal demand", "score": 0.5},
            {"theme": "Housing", "text": "Housing starts fall to lowest since 2020", "score": 0.88},
            {"theme": "Tech", "text": "AI sector boom continues, valuations stretch", "score": 0.6},
            {"theme": "Tech", "text": "Semiconductor shortage eases, chip stocks rally", "score": 0.5},
            {"theme": "Tech", "text": "Big tech earnings beat estimates across the board", "score": 0.78},
            {"theme": "Energy", "text": "Oil prices drop on surplus supply report", "score": 0.4},
            {"theme": "Energy", "text": "OPEC announces surprise production cut", "score": 0.92},
            {"theme": "Energy", "text": "Natural gas inventories rise above 5-year average", "score": 0.3},
        ]
        news = random.choice(headlines)
        theme = news['theme']

        # If real data exists for this theme, anchor the score to the real sentiment
        if self.real_data and theme in self.real_data:
            real_score = self.real_data[theme]['sentiment_score']
            jitter = random.uniform(-0.1, 0.1)
            score = max(0.1, min(0.99, real_score + jitter))
        else:
            jitter = random.uniform(-0.05, 0.05)
            score = max(0.1, min(0.99, news['score'] + jitter))

        return self.add_market_event(theme, news['text'], score)


if __name__ == '__main__':
    tracker = MacroTracker()
    result = tracker.add_market_event("Inflation", "CPI rose by 0.5% this month, exceeding expectations.", 0.85)
    print(f"Theme: {result['theme']} | Status: {result['sentiment']} | Risk: {result['risk_implication']}")
