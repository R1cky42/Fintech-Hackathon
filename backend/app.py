import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from analyzer import MacroTracker

# In production, serve React build from ../frontend/build
BUILD_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build')

app = Flask(__name__, static_folder=BUILD_DIR, static_url_path='')
CORS(app)
tracker = MacroTracker()


# ===== API Routes =====

@app.route('/api/trends', methods=['GET'])
def get_trends():
    """Returns latest state for all 6 macro themes. Simulates 1-2 new events per call."""
    current_data = tracker.simulate_cycle()

    response_data = []
    for event in current_data:
        item = {
            "name": event['theme'],
            "headline": event['content'],
            "score": event['sentiment_score'],
            "heat": int(event['sentiment_score'] * 100),
            "trend": event['sentiment'],
            "risk": event['risk_implication'],
            "timestamp": event['timestamp'].isoformat(),
            "data_source": tracker.data_source,
        }
        # Include real FRED values when available
        if 'real_value' in event:
            item["real_value"] = event['real_value']
            item["real_unit"] = event['real_unit']
            item["real_label"] = event['real_label']
            item["real_change"] = event['real_change']
            item["real_date"] = event['real_date']
        response_data.append(item)

    return jsonify(response_data)


@app.route('/api/memory', methods=['GET'])
def get_memory():
    """Returns recent institutional memory — the last 50 tracked events."""
    memory = tracker.get_memory()
    return jsonify([
        {
            "timestamp": e['timestamp'].isoformat(),
            "theme": e['theme'],
            "headline": e['content'],
            "score": e['sentiment_score'],
            "sentiment": e['sentiment'],
            "risk": e['risk_implication']
        }
        for e in memory
    ])


@app.route('/api/summary', methods=['GET'])
def get_summary():
    """Returns an AI-generated market summary from institutional memory."""
    return jsonify(tracker.get_summary())


@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Returns recent trend-change alerts."""
    return jsonify([
        {
            "timestamp": a['timestamp'].isoformat(),
            "type": a['type'],
            "theme": a['theme'],
            "from": a['from'],
            "to": a['to'],
            "message": a['message']
        }
        for a in tracker.alerts
    ])


@app.route('/api/impacts/<theme>', methods=['GET'])
def get_impacts(theme):
    """Returns cross-market impact chain for a given theme."""
    impacts = tracker.get_cross_impacts(theme)
    return jsonify(impacts)


@app.route('/api/distribution', methods=['GET'])
def get_distribution():
    """Returns sentiment distribution across all tracked themes."""
    return jsonify(tracker.get_theme_distribution())


@app.route('/api/analytics-extended', methods=['GET'])
def get_analytics_extended():
    """Returns extended analytics: volatility, momentum, portfolio signals."""
    return jsonify(tracker.get_analytics_extended())


@app.route('/api/theme-history/<theme>', methods=['GET'])
def get_theme_history(theme):
    """Returns historical sentiment data for a specific theme (for charting)."""
    history = tracker.get_theme_history(theme)
    return jsonify([
        {
            "timestamp": e['timestamp'].isoformat(),
            "score": e['sentiment_score'],
            "sentiment": e['sentiment'],
            "headline": e['content']
        }
        for e in history
    ])


# ===== Serve React Frontend =====

@app.route('/')
def serve_react():
    return send_from_directory(app.static_folder, 'index.html')


@app.errorhandler(404)
def not_found(e):
    """Catch-all: serve React index.html for any non-API route."""
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
