import React from 'react';
import PMSUpload from './PMSUpload';
import ReportViewer from './ReportViewer';

export function LPStudio() {
  return (
    <div className="p-6 h-full bg-slate-950 flex flex-col gap-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-white">LP Diligence Studio</h1>
      </div>
      
      <div className="flex flex-col lg:flex-row gap-6 h-full pb-8">
        <div className="w-full lg:w-1/3 flex flex-col gap-6 shrink-0">
          <PMSUpload />
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 shadow-lg">
            <h3 className="text-lg font-semibold text-white mb-2">Instructions</h3>
            <p className="text-slate-400 text-sm">
              Upload the latest <code className="bg-slate-800 text-blue-400 px-1 py-0.5 rounded">pms_upload_positions.csv</code> snapshot to synchronize the live tracking database.
            </p>
          </div>
        </div>
        
        <div className="w-full lg:w-2/3 h-[800px] lg:h-full">
          <ReportViewer reportType="daily" />
        </div>
      </div>
    </div>
  );
}
