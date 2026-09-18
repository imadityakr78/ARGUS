import { useEffect, useState } from 'react';
import { AlertTriangle } from 'lucide-react';
import { getInvestigation } from './services/api';
import type { InvestigationResponse } from './services/types';

// TODO(member4): Break these into separate components under src/components/
// TODO(member4): Add CameraGrid, VideoPlayer, EventTimeline, EvidenceCoverageView
// TODO(member4): Add InvestigationQuery input, TrajectoryView, HypothesisComparison

function TrustBadge({ state }: { state: string }) {
  return (
    <span className={`badge ${state.toLowerCase()}`}>
      {state}
    </span>
  );
}

function App() {
  const [data, setData] = useState<InvestigationResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getInvestigation('inv_001')
      .then(setData)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="dashboard-container">Loading ARGUS Engine...</div>;
  if (error) return <div className="dashboard-container">Error: {error}</div>;
  if (!data) return <div className="dashboard-container">No data available.</div>;

  return (
    <div className="dashboard-container">
      <header>
        <h1>ARGUS</h1>
        <p>Evidence-Aware Event Reconstruction Dashboard</p>
      </header>

      <div className="card" style={{ borderLeft: '4px solid #fff' }}>
        <h2>{data.summary}</h2>
      </div>

      {/* Evidence Coverage — TODO(member4): M4-005 EvidenceCoverageView */}
      {data.coverage && (
        <div className="card">
          <h2>Evidence Coverage</h2>
          <div style={{ display: 'flex', gap: '1rem' }}>
            <div><TrustBadge state="OBSERVED" /> {(data.coverage.observedFraction * 100).toFixed(0)}%</div>
            <div><TrustBadge state="INFERRED" /> {(data.coverage.inferredFraction * 100).toFixed(0)}%</div>
            <div><TrustBadge state="UNKNOWN" /> {(data.coverage.unknownFraction * 100).toFixed(0)}%</div>
          </div>
        </div>
      )}

      <div className="grid">
        {/* Claims Panel */}
        <div className="card">
          <h2>Investigation Claims</h2>
          <div className="timeline">
            {data.claims?.map((claim, idx) => (
              <div key={idx} className={`timeline-item ${claim.epistemicState.toLowerCase()}`}>
                <div style={{ flex: 1 }}>
                  <p>{claim.description}</p>
                </div>
                <TrustBadge state={claim.epistemicState} />
              </div>
            ))}
          </div>
        </div>

        {/* PACE Rejected Hypotheses */}
        <div className="card">
          <h2><AlertTriangle size={20} color="var(--color-rejected)" /> PACE Verifier Checks</h2>
          <div className="timeline">
            {data.rejectedHypotheses?.map((hyp, idx) => (
              <div key={idx} className="timeline-item rejected">
                <div style={{ flex: 1 }}>
                  <p style={{ color: 'var(--color-rejected)', fontWeight: 600 }}>REJECTED HYPOTHESIS</p>
                  <p style={{ marginTop: '0.5rem', marginBottom: '0.5rem' }}>{hyp.description}</p>
                  {hyp.checks.map((check, cidx) => (
                    <p key={cidx} className="monospace" style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                      [PACE] {check.reason}
                    </p>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Unknowns — TODO(member4): M4-006 UnknownGap component */}
      {data.unknowns && data.unknowns.length > 0 && (
        <div className="card">
          <h2>Unknown Intervals</h2>
          {data.unknowns.map((u, i) => (
            <div key={i} className="timeline-item" style={{ borderLeftColor: 'var(--color-unknown)' }}>
              <TrustBadge state="UNKNOWN" />
              <p style={{ marginLeft: '0.5rem' }}>{u}</p>
            </div>
          ))}
        </div>
      )}

      {/* Warnings */}
      {data.warnings && data.warnings.length > 0 && (
        <div className="card" style={{ borderLeft: '3px solid var(--color-unknown)' }}>
          {data.warnings.map((w, i) => (
            <p key={i} style={{ color: 'var(--text-secondary)', fontStyle: 'italic' }}>{w}</p>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
