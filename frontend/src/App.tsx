import React, { useState } from 'react';

export default function App() {
  const [input, setInput] = useState('');
  const [expected, setExpected] = useState('');
  const [actual, setActual] = useState('');
  const [result, setResult] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch('/api/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input, expected_output: expected, actual_output: actual })
      });
      const data = await res.json();
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setResult('Error running evaluation');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>DeepEval Playground</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <textarea placeholder="Input" value={input} onChange={(e) => setInput(e.target.value)} />
        </div>
        <div>
          <textarea placeholder="Expected Output" value={expected} onChange={(e) => setExpected(e.target.value)} />
        </div>
        <div>
          <textarea placeholder="Actual Output" value={actual} onChange={(e) => setActual(e.target.value)} />
        </div>
        <button type="submit" disabled={loading}>{loading ? 'Evaluating...' : 'Evaluate'}</button>
      </form>
      {result && <pre>{result}</pre>}
    </div>
  );
}
