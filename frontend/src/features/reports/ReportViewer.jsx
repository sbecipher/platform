import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { FileText, RefreshCw } from 'lucide-react';

export default function ReportViewer({ reportType = 'daily', runId = '' }) {
  const [markdown, setMarkdown] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchReport = async () => {
    setLoading(true);
    setError(null);
    try {
      let endpoint = '/api/reports/pms/daily';
      if (reportType === 'lp_brief' && runId) {
        endpoint = `/api/reports/${runId}/markdown`;
      }

      const response = await fetch(endpoint);
      const data = await response.json();

      if (response.ok) {
        setMarkdown(data.markdown_content);
      } else {
        throw new Error(data.detail || 'Failed to fetch report');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReport();
  }, [reportType, runId]);

  return (
    <div className="flex flex-col h-full bg-slate-900 border border-slate-800 rounded-lg shadow-lg overflow-hidden text-slate-200">
      <div className="flex items-center justify-between p-4 bg-slate-800 border-b border-slate-700">
        <h2 className="text-xl font-bold flex items-center gap-2">
          <FileText className="text-blue-400" />
          {reportType === 'daily' ? 'Daily PMS Monitor' : 'LP Diligence Brief'}
        </h2>
        <button 
          onClick={fetchReport}
          disabled={loading}
          className="p-2 hover:bg-slate-700 rounded transition-colors disabled:opacity-50 text-slate-400 hover:text-white"
          title="Refresh Report"
        >
          <RefreshCw size={20} className={loading ? 'animate-spin' : ''} />
        </button>
      </div>

      <div className="flex-1 overflow-auto p-6 prose prose-invert prose-blue max-w-none">
        {loading && !markdown && (
          <div className="text-slate-400 animate-pulse">Generating report...</div>
        )}
        
        {error && (
          <div className="text-rose-400 bg-rose-900/20 p-4 rounded border border-rose-800/50">
            Error: {error}
          </div>
        )}

        {!loading && !error && markdown && (
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {markdown}
          </ReactMarkdown>
        )}
      </div>
    </div>
  );
}
