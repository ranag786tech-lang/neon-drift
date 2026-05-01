import React, { useState, useEffect } from 'react';

// Main Dashboard Component
const TrustTransparencyDashboard = () => {
  const [explanations, setExplanations] = useState([]);
  const [selectedExplanation, setSelectedExplanation] = useState(null);
  const [fairnessMetrics, setFairnessMetrics] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchExplanations();
    fetchFairnessMetrics();
  }, []);

  const fetchExplanations = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/v1/explanations', {
        headers: { 'X-API-Key': 'your-api-key' }
      });
      const data = await response.json();
      setExplanations(data);
    } catch (error) {
      console.error('Error fetching explanations:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchFairnessMetrics = async () => {
    try {
      const response = await fetch('/api/v1/metrics/fairness', {
        headers: { 'X-API-Key': 'your-api-key' }
      });
      const data = await response.json();
      setFairnessMetrics(data);
    } catch (error) {
      console.error('Error fetching fairness metrics:', error);
    }
  };

  const calculateAvgFairness = () => {
    if (explanations.length === 0) return 'N/A';
    const avg = explanations.reduce((sum, exp) => sum + exp.fairness_score, 0) / explanations.length;
    return (avg * 100).toFixed(1) + '%';
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>🏛️ Trust & Transparency Dashboard</h1>
        <p>AI Decision Explanations & Fairness Monitoring</p>
      </header>

      <div className="dashboard-grid">
        <OverviewCard title="Total Decisions" value={explanations.length} icon="📊" />
        <OverviewCard title="Avg Fairness Score" value={calculateAvgFairness()} icon="⚖️" />
        <OverviewCard title="Compliance Status" value="COMPLIANT" icon="✅" />

        <Card className="explanation-list">
          <CardHeader>
            <h2>Recent AI Decisions</h2>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="loading">Loading...</div>
            ) : (
              <ul>
                {explanations.map(exp => (
                  <ExplanationListItem
                    key={exp.decision_id}
                    explanation={exp}
                    onClick={() => setSelectedExplanation(exp)}
                  />
                ))}
              </ul>
            )}
          </CardContent>
        </Card>

        {selectedExplanation && (
          <ExplanationDetail 
            explanation={selectedExplanation}
            onClose={() => setSelectedExplanation(null)}
          />
        )}

        <FairnessMetricsChart metrics={fairnessMetrics} />
      </div>
    </div>
  );
};

const ExplanationListItem = ({ explanation, onClick }) => {
  const impactColors = {
    positive: 'bg-green-100 text-green-800',
    negative: 'bg-red-100 text-red-800',
    neutral: 'bg-gray-100 text-gray-800'
  };

  return (
    <li className="explanation-item" onClick={onClick}>
      <div className="explanation-header">
        <span className="decision-id">{explanation.decision_id}</span>
        <Badge variant={explanation.outcome === 'approved' ? 'success' : 'danger'}>
          {explanation.outcome}
        </Badge>
      </div>
      <div className="explanation-meta">
        <span className="model-name">{explanation.model_name}</span>
        <span className="confidence">Confidence: {(explanation.confidence * 100).toFixed(0)}%</span>
      </div>
      <div className="explanation-factors">
        {explanation.top_factors.slice(0, 2).map((factor, idx) => (
          <span key={idx} className={`factor-badge ${impactColors[factor.impact]}`}>
            {factor.name}: {factor.weight * 100}%
          </span>
        ))}
      </div>
    </li>
  );
};

const ExplanationDetail = ({ explanation, onClose }) => {
  return (
    <Card className="explanation-detail">
      <CardHeader>
        <h2>Decision Explanation</h2>
        <Button onClick={onClose} variant="ghost">✕ Close</Button>
      </CardHeader>
      <CardContent>
        <div className="detail-section">
          <h3>Outcome</h3>
          <div className="outcome-display">
            <Badge variant={explanation.outcome === 'approved' ? 'success' : 'danger'} size="lg">
              {explanation.outcome.toUpperCase()}
            </Badge>
            <span className="confidence-score">{(explanation.confidence * 100).toFixed(1)}% confidence</span>
          </div>
        </div>

        <div className="detail-section">
          <h3>Fairness Score</h3>
          <ProgressBar value={explanation.fairness_score * 100} max={100} 
            color={explanation.fairness_score > 0.8 ? 'green' : 'yellow'} />
          <span>{(explanation.fairness_score * 100).toFixed(1)}%</span>
        </div>

        <div className="detail-section">
          <h3>Top Factors</h3>
          <ul className="factors-list">
            {explanation.top_factors.map((factor, idx) => (
              <li key={idx} className="factor-item">
                <div className="factor-header">
                  <strong>{factor.name}</strong>
                  <Badge variant={factor.impact}>{factor.impact}</Badge>
                </div>
                <p className="factor-description">{factor.description}</p>
                <ProgressBar value={factor.weight * 100} max={100} />
                <span className="factor-value">Weight: {(factor.weight * 100).toFixed(0)}%</span>
              </li>
            ))}
          </ul>
        </div>

        {explanation.alternative_outcomes.length > 0 && (
          <div className="detail-section">
            <h3>Alternative Outcomes</h3>
            {explanation.alternative_outcomes.map((alt, idx) => (
              <div key={idx} className="alternative-outcome">
                <Badge variant="warning">{alt.outcome}</Badge>
                <span>Probability: {(alt.probability * 100).toFixed(1)}%</span>
                <p className="condition">Condition: {alt.condition}</p>
              </div>
            ))}
          </div>
        )}

        <div className="detail-section">
          <h3>Explanation</h3>
          <p className="explanation-text">{explanation.explanation_text}</p>
          {explanation.explanation_urdu && (
            <div className="urdu-translation">
              <h4>اردو ترجمہ</h4>
              <p dir="rtl">{explanation.explanation_urdu}</p>
            </div>
          )}
        </div>

        <div className="detail-section">
          <h3>Metadata</h3>
          <div className="metadata-grid">
            <div>
              <label>Model:</label>
              <span>{explanation.model_name} ({explanation.model_version})</span>
            </div>
            <div>
              <label>Date:</label>
              <span>{new Date(explanation.timestamp).toLocaleString()}</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

const FairnessMetricsChart = ({ metrics }) => {
  return (
    <Card className="fairness-metrics">
      <CardHeader>
        <h2>Fairness Metrics</h2>
      </CardHeader>
      <CardContent>
        <div className="metrics-grid">
          {metrics.map((metric, idx) => (
            <div key={idx} className="metric-card">
              <h4>{metric.metric_type.replace('_', ' ').toUpperCase()}</h4>
              <div className="metric-value">{(metric.value * 100).toFixed(1)}%</div>
              <ProgressBar value={metric.value * 100} max={100} 
                color={metric.passed ? 'green' : 'red'} />
              <div className="metric-details">
                <span>Threshold: {metric.threshold * 100}%</span>
                <Badge variant={metric.passed ? 'success' : 'danger'}>
                  {metric.passed ? 'PASS' : 'FAIL'}
                </Badge>
              </div>
              <div className="metric-breakdown">
                <h5>Group Breakdown:</h5>
                {Object.entries(metric.breakdown).map(([group, value]) => (
                  <div key={group} className="group-metric">
                    <span>{group}:</span>
                    <span>{(value * 100).toFixed(1)}%</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

const OverviewCard = ({ title, value, icon }) => {
  return (
    <Card className="overview-card">
      <CardContent>
        <div className="overview-icon">{icon}</div>
        <div className="overview-content">
          <h3>{title}</h3>
          <p className="overview-value">{value}</p>
        </div>
      </CardContent>
    </Card>
  );
};

// Placeholder UI components (would be imported from a UI library)
const Card = ({ children, className }) => <div className={`card ${className}`}>{children}</div>;
const CardHeader = ({ children }) => <div className="card-header">{children}</div>;
const CardContent = ({ children }) => <div className="card-content">{children}</div>;
const Badge = ({ children, variant, size }) => <span className={`badge badge-${variant} badge-${size || 'md'}`}>{children}</span>;
const Button = ({ children, onClick, variant }) => <button className={`btn btn-${variant}`} onClick={onClick}>{children}</button>;
const ProgressBar = ({ value, max, color }) => (
  <div className="progress-bar">
    <div className="progress-fill" style={{ width: `${(value/max)*100}%`, backgroundColor: color }}></div>
  </div>
);

export default TrustTransparencyDashboard;
