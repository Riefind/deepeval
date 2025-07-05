import React, { useState } from 'react';

interface TestCase {
  input: string;
  expected_output: string;
  actual_output: string;
}

export default function App() {
  const [metric, setMetric] = useState('correctness');
  const [tests, setTests] = useState<TestCase[]>([
    { input: '', expected_output: '', actual_output: '' }
  ]);
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const updateTest = (index: number, field: keyof TestCase, value: string) => {
    setTests(t => {
      const copy = [...t];
      copy[index] = { ...copy[index], [field]: value };
      return copy;
    });
  };

  const addTest = () => {
    setTests(t => [...t, { input: '', expected_output: '', actual_output: '' }]);
  };

  const removeTest = (i: number) => {
    setTests(t => t.filter((_, idx) => idx !== i));
  };

  const handleUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    file.text().then(text => {
      try {
        const data = JSON.parse(text);
        if (Array.isArray(data)) {
          setTests(data);
        }
      } catch (err) {
        console.error('Invalid file');
      }
    });
  };

  const download = () => {
    const blob = new Blob([JSON.stringify(tests, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'tests.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch('/api/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ metric, tests })
      });
      const data = await res.json();
      setResults(data);
    } catch (err) {
      setResults({ error: 'Failed to evaluate' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-3xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold mb-4">DeepEval Playground</h1>
      <div className="flex items-center space-x-4">
        <label className="block text-sm font-medium">Metric</label>
        <select
          value={metric}
          onChange={e => setMetric(e.target.value)}
          className="border px-2 py-1 rounded"
        >
          <option value="correctness">Correctness</option>
          <option value="answer_relevancy">Answer Relevancy</option>
        </select>
        <input type="file" accept="application/json" onChange={handleUpload} className="text-sm" />
        <button type="button" onClick={download} className="px-2 py-1 bg-gray-200 rounded">Download</button>
      </div>
      <form onSubmit={handleSubmit} className="space-y-6">
        {tests.map((t, idx) => (
          <div key={idx} className="border p-4 rounded space-y-2">
            <div className="flex justify-between">
              <span className="font-medium">Test {idx + 1}</span>
              {tests.length > 1 && (
                <button type="button" onClick={() => removeTest(idx)} className="text-red-600">Remove</button>
              )}
            </div>
            <textarea
              className="w-full border p-2 rounded"
              placeholder="Input"
              value={t.input}
              onChange={e => updateTest(idx, 'input', e.target.value)}
            />
            <textarea
              className="w-full border p-2 rounded"
              placeholder="Expected Output"
              value={t.expected_output}
              onChange={e => updateTest(idx, 'expected_output', e.target.value)}
            />
            <textarea
              className="w-full border p-2 rounded"
              placeholder="Actual Output"
              value={t.actual_output}
              onChange={e => updateTest(idx, 'actual_output', e.target.value)}
            />
          </div>
        ))}
        <button type="button" onClick={addTest} className="px-3 py-1 bg-blue-500 text-white rounded">
          Add Test
        </button>
        <div>
          <button
            type="submit"
            disabled={loading}
            className="px-4 py-2 bg-green-600 text-white rounded mt-2"
          >
            {loading ? 'Evaluating...' : 'Run Evaluation'}
          </button>
        </div>
      </form>
      {results && <pre className="bg-gray-100 p-4 rounded overflow-auto">{JSON.stringify(results, null, 2)}</pre>}
    </div>
  );
}
