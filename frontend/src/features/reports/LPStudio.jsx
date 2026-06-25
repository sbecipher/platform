import React, { useState } from 'react';
import ReportViewer from './ReportViewer';
import ExceptionRegister from './ExceptionRegister';

export function LPStudio() {
  const [activeTab, setActiveTab] = useState('viewer');

  return (
    <div className="p-6 h-full bg-slate-950 flex flex-col gap-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-white">Diligence Studio</h1>
        <div className="flex gap-2 bg-slate-900 p-1 rounded-lg border border-slate-800">
          <button 
            className={`px-4 py-2 rounded-md transition-colors ${activeTab === 'viewer' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white hover:bg-slate-800'}`}
            onClick={() => setActiveTab('viewer')}
          >
            Daily PMS Monitor
          </button>
          <button 
            className={`px-4 py-2 rounded-md transition-colors ${activeTab === 'exceptions' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white hover:bg-slate-800'}`}
            onClick={() => setActiveTab('exceptions')}
          >
            Exception Register
          </button>
        </div>
      </div>
      
      {activeTab === 'viewer' && (
        <div className="w-full h-full min-h-[800px] pb-8">
          <ReportViewer reportType="daily" runId="pm-lp-scm-20260624T212419Z" />
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
