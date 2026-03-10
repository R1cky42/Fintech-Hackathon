import React, { useState, useEffect, useCallback, useRef } from 'react';
import {
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid,
  PieChart, Pie, Cell
} from 'recharts';
import './Dashboard.css';

const API_URL = process.env.REACT_APP_API_URL ?? 'http://127.0.0.1:5000';
const POLL_INTERVAL = 10000;

const THEME_COLORS = {
  Inflation: '#ff6b6b',
  GDP: '#ffa726',
  Employment: '#66bb6a',
  Housing: '#ab47bc',
  Tech: '#42a5f5',
  Energy: '#ffca28'
};

const TABS = [
  { id: 'overview', label: 'Overview' },
  { id: 'impacts', label: 'Impacts' },
  { id: 'analytics', label: 'Analytics' },
  { id: 'memory', label: 'Memory' },
];

/* ===== Sub-components ===== */

const ConnectionIndicator = ({ status, dataSource }) => (
  <div className="connection-info">
    <span className={`connection-indicator ${status}`}>
      <span className="connection-dot" />
      {status === 'connected' ? 'Live' : status === 'error' ? 'Disconnected' : 'Connecting...'}
    </span>
    {dataSource && (
      <span className={`data-source-badge ${dataSource}`}>
        {dataSource === 'live' ? 'FRED DATA' : 'SIMULATED'}
      </span>
    )}
  </div>
);

const NewsTicker = ({ headlines }) => {
  if (!headlines || headlines.length === 0) return null;
  const items = [...headlines, ...headlines];
  return (
    <div className="news-ticker">
      <div className="news-ticker-content">
        {items.map((h, i) => (
          <span key={i}>
            <span className={`ticker-badge ${h.sentiment === 'HOT' ? 'hot' : 'cool'}`}>
              {h.theme}
            </span>
            {' '}{h.headline}
          </span>
        ))}
      </div>
    </div>
  );
};

const AlertBanner = ({ alerts }) => {
  if (!alerts || alerts.length === 0) return null;
  const latest = alerts[alerts.length - 1];
  return (
    <div className={`alert-banner ${latest.to === 'HOT' ? 'hot' : 'cool'}`}>
      <span className="alert-icon">{latest.to === 'HOT' ? '\u26A0' : '\u2744'}</span>
      <span className="alert-text">{latest.message}</span>
      <span className="alert-time">{new Date(latest.timestamp).toLocaleTimeString()}</span>
    </div>
  );
};

const TabBar = ({ activeTab, onTabChange, alertCount }) => (
  <div className="tab-bar">
    {TABS.map(tab => (
      <button
        key={tab.id}
        className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
        onClick={() => onTabChange(tab.id)}
      >
        {tab.label}
        {tab.id === 'memory' && alertCount > 0 && (
          <span className="tab-badge">{alertCount}</span>
        )}
      </button>
    ))}
  </div>
);

const TrendCard = ({ item, isSelected, isNew, onClick }) => (
  <div
    className={`trend-card ${isSelected ? 'selected' : ''} ${isNew ? 'updated' : ''}`}
    onClick={() => onClick(item)}
  >
    <div className="trend-card-header">
      <span className="trend-name">
        <span className="theme-dot" style={{ backgroundColor: THEME_COLORS[item.name] || '#888' }} />
        {item.name}
      </span>
      <div className="trend-card-badges">
        <span className="score-badge">{Math.round(item.score * 100)}%</span>
        <span className={`trend-badge ${item.trend === 'HOT' ? 'hot' : 'cool'}`}>
          {item.trend}
        </span>
      </div>
    </div>
    {item.headline && <div className="trend-headline">{item.headline}</div>}
    {item.real_value !== undefined && (
      <div className="real-data-row">
        <span className="real-label">{item.real_label}</span>
        <span className="real-value">{Number(item.real_value).toLocaleString()} {item.real_unit}</span>
        <span className={`real-change ${item.real_change > 0 ? 'up' : 'down'}`}>
          {item.real_change > 0 ? '+' : ''}{item.real_change}%
        </span>
      </div>
    )}
    <div className="heat-bar-track">
      <div
        className={`heat-bar-fill ${item.trend === 'HOT' ? 'hot' : 'cool'}`}
        style={{ width: `${item.heat}%` }}
      />
    </div>
  </div>
);

/* ===== Tab Content: Overview ===== */

const OverviewTab = ({ selectedTrend, themeHistory, summary }) => {
  const color = selectedTrend?.trend === 'HOT' ? '#ff4d4d' : '#4d79ff';

  const chartData = themeHistory.length > 0
    ? themeHistory.map((e, i) => ({
        name: `#${i + 1}`,
        score: Math.round(e.score * 100),
      }))
    : Array.from({ length: 10 }, (_, i) => ({
        name: `#${i + 1}`,
        score: Math.round((selectedTrend?.score || 0.5) * 100 + (Math.random() * 10 - 5))
      }));

  return (
    <div className="tab-content">
      {/* Chart */}
      <div className="panel">
        <h3>
          {selectedTrend ? `Sentiment History: ${selectedTrend.name}` : 'Select a Trend'}
          {themeHistory.length > 0 && (
            <span className="panel-subtitle">{themeHistory.length} data points</span>
          )}
        </h3>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={color} stopOpacity={0.8} />
                  <stop offset="95%" stopColor={color} stopOpacity={0} />
                </linearGradient>
              </defs>
              <XAxis dataKey="name" stroke="#555" tick={{ fill: '#888', fontSize: 11 }} />
              <YAxis stroke="#555" tick={{ fill: '#888', fontSize: 11 }} domain={[0, 100]} />
              <CartesianGrid strokeDasharray="3 3" stroke="#2a2a4a" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1a1a2e', borderColor: '#333', color: '#fff', borderRadius: '8px' }}
                itemStyle={{ color: '#fff' }}
                labelStyle={{ color: '#888' }}
                formatter={(value) => [`${value}%`, 'Sentiment']}
              />
              <Area type="monotone" dataKey="score" stroke={color} strokeWidth={2} fillOpacity={1} fill="url(#colorValue)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* AI Analysis */}
      {summary && (
        <div className="panel">
          <div className="analysis-header">
            <h3>AI Analysis</h3>
            <span className={`market-status ${summary.overall_sentiment.toLowerCase()}`}>
              {summary.overall_sentiment}
            </span>
          </div>
          <p className="analysis-narrative">{summary.narrative}</p>
          <div className="analysis-stats">
            <div className="stat">
              <span className="stat-value hot">{summary.hot_count}</span>
              <span className="stat-label">HOT Signals</span>
            </div>
            <div className="stat">
              <span className="stat-value cool">{summary.cool_count}</span>
              <span className="stat-label">COOL Signals</span>
            </div>
            <div className="stat">
              <span className="stat-value">{summary.risk_level}</span>
              <span className="stat-label">Risk Level</span>
            </div>
            {summary.dominant_theme && (
              <div className="stat">
                <span className="stat-value">{summary.dominant_theme}</span>
                <span className="stat-label">Dominant</span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

/* ===== Tab Content: Impacts ===== */

const ImpactsTab = ({ impacts, selectedTheme }) => {
  if (!impacts || impacts.length === 0) {
    return (
      <div className="tab-content">
        <div className="panel">
          <h3>Cross-Market Impact Chain</h3>
          <p className="loading-text">Select a theme on the left to view its cross-market impacts.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="tab-content">
      <div className="panel">
        <h3>Cross-Market Impact Chain: {selectedTheme}</h3>
        <p className="impact-intro">
          How <strong>{selectedTheme}</strong> movements ripple across other macro sectors.
        </p>
        <div className="impact-list">
          {impacts.map((impact, i) => (
            <div key={i} className="impact-item">
              <div className="impact-header">
                <span className="impact-arrow">{selectedTheme}</span>
                <span className="impact-connector">&rarr;</span>
                <span className="impact-target">{impact.target}</span>
                <span className={`impact-status ${impact.target_sentiment === 'HOT' ? 'hot' : 'cool'}`}>
                  {impact.target_sentiment}
                </span>
              </div>
              <div className="impact-description">{impact.description}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

/* ===== Tab Content: Analytics ===== */

const AnalyticsTab = ({ distribution, summary }) => {
  if (!distribution || distribution.length === 0) {
    return (
      <div className="tab-content">
        <div className="panel">
          <h3>Analytics</h3>
          <p className="loading-text">Collecting data for analytics...</p>
        </div>
      </div>
    );
  }

  const pieData = distribution.map(d => ({
    name: d.theme,
    value: d.total,
    color: THEME_COLORS[d.theme] || '#888'
  }));

  return (
    <div className="tab-content">
      {/* Distribution */}
      <div className="panel">
        <h3>Theme Distribution</h3>
        <div className="distribution-content">
          <div className="distribution-chart">
            <ResponsiveContainer width="100%" height={220}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={90}
                  paddingAngle={3}
                  dataKey="value"
                >
                  {pieData.map((entry, i) => (
                    <Cell key={i} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ backgroundColor: '#1a1a2e', borderColor: '#333', color: '#fff', borderRadius: '8px' }}
                  formatter={(value, name) => [`${value} events`, name]}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="distribution-legend">
            {distribution.map((d, i) => (
              <div key={i} className="legend-item">
                <span className="legend-dot" style={{ backgroundColor: THEME_COLORS[d.theme] || '#888' }} />
                <span className="legend-theme">{d.theme}</span>
                <span className="legend-stats">
                  <span className="legend-hot">{d.hot} hot</span>
                  {' / '}
                  <span className="legend-cool">{d.cool} cool</span>
                </span>
                <span className="legend-avg">avg {Math.round(d.avg_score * 100)}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Sector Breakdown Table */}
      <div className="panel">
        <h3>Sector Breakdown</h3>
        <table className="sector-table">
          <thead>
            <tr>
              <th>Sector</th>
              <th>Events</th>
              <th>HOT</th>
              <th>COOL</th>
              <th>Avg Score</th>
              <th>Bias</th>
            </tr>
          </thead>
          <tbody>
            {distribution.map((d, i) => (
              <tr key={i}>
                <td>
                  <span className="legend-dot" style={{ backgroundColor: THEME_COLORS[d.theme] || '#888' }} />
                  {d.theme}
                </td>
                <td>{d.total}</td>
                <td className="hot">{d.hot}</td>
                <td className="cool">{d.cool}</td>
                <td>{Math.round(d.avg_score * 100)}%</td>
                <td>
                  <span className={`bias-badge ${d.hot > d.cool ? 'hot' : d.cool > d.hot ? 'cool' : 'neutral'}`}>
                    {d.hot > d.cool ? 'Risk-On' : d.cool > d.hot ? 'Stable' : 'Neutral'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

/* ===== Tab Content: Memory ===== */

const MemoryTab = ({ memory }) => {
  if (!memory || memory.length === 0) {
    return (
      <div className="tab-content">
        <div className="panel">
          <h3>Institutional Memory</h3>
          <p className="loading-text">No events recorded yet...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="tab-content">
      <div className="panel">
        <h3>Institutional Memory <span className="panel-subtitle">{memory.length} events tracked</span></h3>
        <div className="memory-list">
          {memory.slice().reverse().map((event, i) => (
            <div key={i} className="memory-item">
              <div className="memory-item-header">
                <span className={`memory-badge ${event.sentiment === 'HOT' ? 'hot' : 'cool'}`}>
                  {event.theme}
                </span>
                <span className="memory-time">
                  {new Date(event.timestamp).toLocaleTimeString()}
                </span>
              </div>
              <div className="memory-headline">{event.headline}</div>
              <div className="memory-risk">{event.risk}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

/* ===== Main Dashboard ===== */

const MacroDashboard = () => {
  const [data, setData] = useState([]);
  const [selectedTrend, setSelectedTrend] = useState(null);
  const [themeHistory, setThemeHistory] = useState([]);
  const [memory, setMemory] = useState([]);
  const [summary, setSummary] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [impacts, setImpacts] = useState([]);
  const [distribution, setDistribution] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState('connecting');
  const [lastUpdated, setLastUpdated] = useState(null);
  const [updatedThemes, setUpdatedThemes] = useState(new Set());
  const [dataSource, setDataSource] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const selectedRef = useRef(null);
  const prevDataRef = useRef({});

  const handleTrendClick = useCallback(async (item) => {
    setSelectedTrend(item);
    selectedRef.current = item.name;

    try {
      const [historyRes, impactsRes] = await Promise.all([
        fetch(`${API_URL}/api/theme-history/${item.name}`),
        fetch(`${API_URL}/api/impacts/${item.name}`)
      ]);
      const historyData = await historyRes.json();
      const impactsData = await impactsRes.json();
      setThemeHistory(historyData);
      setImpacts(impactsData);
    } catch (err) {
      console.error('Error fetching theme data:', err);
    }
  }, []);

  const fetchData = useCallback(async () => {
    try {
      const [trendsRes, memoryRes, summaryRes, alertsRes, distRes] = await Promise.all([
        fetch(`${API_URL}/api/trends`),
        fetch(`${API_URL}/api/memory`),
        fetch(`${API_URL}/api/summary`),
        fetch(`${API_URL}/api/alerts`),
        fetch(`${API_URL}/api/distribution`)
      ]);

      const trends = await trendsRes.json();
      const memoryData = await memoryRes.json();
      const summaryData = await summaryRes.json();
      const alertsData = await alertsRes.json();
      const distData = await distRes.json();

      // Detect which themes just got new data
      const changed = new Set();
      trends.forEach(t => {
        const prev = prevDataRef.current[t.name];
        if (!prev || prev.timestamp !== t.timestamp) {
          changed.add(t.name);
        }
      });
      const newPrev = {};
      trends.forEach(t => { newPrev[t.name] = t; });
      prevDataRef.current = newPrev;

      setData(trends);
      setMemory(memoryData);
      setSummary(summaryData);
      setAlerts(alertsData);
      setDistribution(distData);
      setConnectionStatus('connected');
      setLastUpdated(new Date());
      if (trends.length > 0 && trends[0].data_source) {
        setDataSource(trends[0].data_source);
      }

      if (changed.size > 0) {
        setUpdatedThemes(changed);
        setTimeout(() => setUpdatedThemes(new Set()), 2000);
      }

      if (trends.length > 0 && !selectedRef.current) {
        handleTrendClick(trends[0]);
      }

      if (selectedRef.current) {
        try {
          const historyRes = await fetch(`${API_URL}/api/theme-history/${selectedRef.current}`);
          const historyData = await historyRes.json();
          setThemeHistory(historyData);
        } catch (_) { /* ignore */ }
      }
    } catch (err) {
      console.error('API Error:', err);
      setConnectionStatus('error');
    }
  }, [handleTrendClick]);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, POLL_INTERVAL);
    return () => clearInterval(interval);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return <OverviewTab selectedTrend={selectedTrend} themeHistory={themeHistory} summary={summary} />;
      case 'impacts':
        return <ImpactsTab impacts={impacts} selectedTheme={selectedTrend?.name} />;
      case 'analytics':
        return <AnalyticsTab distribution={distribution} summary={summary} />;
      case 'memory':
        return <MemoryTab memory={memory} />;
      default:
        return null;
    }
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1 className="dashboard-title">Global Macro Tracker</h1>
        <div className="header-meta">
          <ConnectionIndicator status={connectionStatus} dataSource={dataSource} />
          {lastUpdated && (
            <span className="last-updated">
              Updated {lastUpdated.toLocaleTimeString()}
            </span>
          )}
        </div>
      </header>

      <NewsTicker headlines={memory} />
      <AlertBanner alerts={alerts} />

      <div className="dashboard-grid">
        {/* Left Column: Trend Feed */}
        <div className="left-column">
          <div className="feed-panel">
            <h3>Live Market Themes</h3>
            {data.length === 0 && <p className="loading-text">Connecting to satellite feed...</p>}
            {data.map((item) => (
              <TrendCard
                key={item.name}
                item={item}
                isSelected={selectedTrend?.name === item.name}
                isNew={updatedThemes.has(item.name)}
                onClick={handleTrendClick}
              />
            ))}
          </div>
        </div>

        {/* Right Column: Tabbed Content */}
        <div className="right-column">
          <TabBar activeTab={activeTab} onTabChange={setActiveTab} alertCount={memory.length} />
          {renderTabContent()}
        </div>
      </div>
    </div>
  );
};

export default MacroDashboard;
