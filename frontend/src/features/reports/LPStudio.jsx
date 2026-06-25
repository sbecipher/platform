import React, { useState } from 'react';
import PMSUpload from './PMSUpload';
import ReportViewer from './ReportViewer';
import ExceptionRegister from './ExceptionRegister';

export function LPStudio() {
  const [activeTab, setActiveTab] = useState('reports');
  const [reportType, setReportType] = useState('daily');
  const [runId, setRunId] = useState('pm-lp-scm-20260624T212419Z');

  return (
    <div className="p-6 h-full bg-slate-950 flex flex-col gap-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-white">LP Diligence Studio</h1>
        <div className="flex gap-2 bg-slate-900 p-1 rounded-lg border border-slate-800">
          <button 
            className={`px-4 py-2 rounded-md transition-colors ${activeTab === 'reports' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white hover:bg-slate-800'}`}
            onClick={() => setActiveTab('reports')}
          >
            Configuration & Upload
          </button>
          <button 
            className={`px-4 py-2 rounded-md transition-colors ${activeTab === 'viewer' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white hover:bg-slate-800'}`}
            onClick={() => setActiveTab('viewer')}
          >
            Report Viewer
          </button>
          <button 
            className={`px-4 py-2 rounded-md transition-colors ${activeTab === 'exceptions' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white hover:bg-slate-800'}`}
            onClick={() => setActiveTab('exceptions')}
          >
            Exception Register
          </button>
        </div>
      </div>
      
      {activeTab === 'reports' && (
        <div className="w-full flex flex-col gap-6 h-full pb-8">
          <PMSUpload />
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 shadow-lg flex flex-col gap-4">
            <h3 className="text-lg font-semibold text-white">Report Configuration</h3>
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1">
                <label className="block text-xs text-slate-400 mb-1">Report Type</label>
                <select value={reportType} onChange={e => setReportType(e.target.value)} className="w-full bg-slate-950 border border-slate-700 rounded p-2 text-white">
                  <option value="daily">Daily PMS Monitor</option>
                  <option value="pm_report">PM Decision Memo</option>
                  <option value="lp_brief">Institutional LP Brief</option>
                </select>
              </div>
              <div className="flex-1">
                <label className="block text-xs text-slate-400 mb-1">Run ID</label>
                <input type="text" value={runId} onChange={e => setRunId(e.target.value)} className="w-full bg-slate-950 border border-slate-700 rounded p-2 text-white" placeholder="Run ID..." />
              </div>
            </div>
            <div className="mt-4">
              <button 
                onClick={() => setActiveTab('viewer')} 
                className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-medium transition-colors"
              >
                View Report
              </button>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'viewer' && (
        <div className="w-full h-full min-h-[800px] pb-8">
          <ReportViewer reportType={reportType} runId={runId} />
        </div>
      )}

      {activeTab === 'exceptions' && (
        <div className="h-[800px] lg:h-full pb-8">
          <ExceptionRegister />
        </div>
      )}
    </div>
  );
}
