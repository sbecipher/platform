import React, { useState, useEffect } from 'react';
import { ShieldAlert, Plus, Trash2, Save } from 'lucide-react';

export default function ExceptionRegister() {
  const [exceptions, setExceptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [formData, setFormData] = useState({
    ticker: '',
    approved_min: 0,
    approved_target: 0,
    approved_cap: 0,
    fiduciary_caveat: ''
  });

  const fetchExceptions = async () => {
    try {
      setLoading(true);
      const res = await fetch('/api/governance/exceptions');
      const data = await res.json();
      if (res.ok) setExceptions(data);
      else throw new Error(data.detail || 'Failed to fetch');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchExceptions();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch('/api/governance/exceptions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      if (!res.ok) throw new Error('Failed to save exception');
      fetchExceptions();
      setFormData({ ticker: '', approved_min: 0, approved_target: 0, approved_cap: 0, fiduciary_caveat: '' });
    } catch (err) {
      alert(err.message);
    }
  };

  const handleDelete = async (ticker) => {
    try {
      const res = await fetch(`/api/governance/exceptions/${ticker}`, { method: 'DELETE' });
      if (!res.ok) throw new Error('Failed to delete');
      fetchExceptions();
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div className="flex flex-col h-full bg-slate-900 border border-slate-800 rounded-lg shadow-lg overflow-hidden text-slate-200">
      <div className="flex items-center justify-between p-4 bg-slate-800 border-b border-slate-700">
        <h2 className="text-xl font-bold flex items-center gap-2">
          <ShieldAlert className="text-amber-400" />
          PM Exception Register
        </h2>
      </div>

      <div className="flex-1 overflow-auto p-6 flex flex-col gap-8">
        {/* Form */}
        <form onSubmit={handleSubmit} className="bg-slate-800 p-4 rounded-lg border border-slate-700 flex flex-col gap-4">
          <h3 className="font-semibold text-slate-300">Add / Edit Fiduciary Caveat</h3>
          <div className="grid grid-cols-4 gap-4">
            <div>
              <label className="block text-xs text-slate-400 mb-1">Ticker</label>
              <input required type="text" value={formData.ticker} onChange={e => setFormData({...formData, ticker: e.target.value.toUpperCase()})} className="w-full bg-slate-900 border border-slate-700 rounded p-2 text-white" placeholder="AAPL" />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">Min (%)</label>
              <input required type="number" step="0.01" value={formData.approved_min} onChange={e => setFormData({...formData, approved_min: parseFloat(e.target.value)})} className="w-full bg-slate-900 border border-slate-700 rounded p-2 text-white" />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">Target (%)</label>
              <input required type="number" step="0.01" value={formData.approved_target} onChange={e => setFormData({...formData, approved_target: parseFloat(e.target.value)})} className="w-full bg-slate-900 border border-slate-700 rounded p-2 text-white" />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">Cap (%)</label>
              <input required type="number" step="0.01" value={formData.approved_cap} onChange={e => setFormData({...formData, approved_cap: parseFloat(e.target.value)})} className="w-full bg-slate-900 border border-slate-700 rounded p-2 text-white" />
            </div>
          </div>
          <div>
            <label className="block text-xs text-slate-400 mb-1">Fiduciary Caveat Justification</label>
            <textarea required value={formData.fiduciary_caveat} onChange={e => setFormData({...formData, fiduciary_caveat: e.target.value})} className="w-full bg-slate-900 border border-slate-700 rounded p-2 text-white h-24" placeholder="Enter justification..."></textarea>
          </div>
          <div className="flex justify-end">
            <button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded flex items-center gap-2">
              <Save size={16} /> Save Caveat
            </button>
          </div>
        </form>

        {/* List */}
        <div>
          <h3 className="font-semibold text-slate-300 mb-4">Active Exceptions</h3>
          {loading ? (
            <div className="text-slate-400 animate-pulse">Loading exceptions...</div>
          ) : error ? (
            <div className="text-rose-400">{error}</div>
          ) : exceptions.length === 0 ? (
            <div className="text-slate-500 italic">No active exceptions.</div>
          ) : (
            <div className="flex flex-col gap-3">
              {exceptions.map(exc => (
                <div key={exc.id} className="bg-slate-800 border border-amber-900/50 rounded-lg p-4 flex justify-between items-start">
                  <div>
                    <div className="flex items-center gap-3 mb-2">
                      <span className="font-bold text-amber-400 text-lg">{exc.ticker}</span>
                      <span className="text-xs bg-slate-900 px-2 py-1 rounded text-slate-300 border border-slate-700">Band: {exc.approved_min}% - {exc.approved_target}% - {exc.approved_cap}%</span>
                    </div>
                    <p className="text-sm text-slate-300">{exc.fiduciary_caveat}</p>
                  </div>
                  <button onClick={() => handleDelete(exc.ticker)} className="text-rose-400 hover:text-rose-300 p-2" title="Deactivate">
                    <Trash2 size={18} />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
