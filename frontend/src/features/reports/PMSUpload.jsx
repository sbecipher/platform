import React, { useState } from 'react';
import { UploadCloud, CheckCircle, AlertCircle } from 'lucide-react';

export default function PMSUpload() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('idle');
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setStatus('idle');
      setMessage('');
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setStatus('uploading');
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/reports/pms/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      
      if (response.ok) {
        setStatus('success');
        setMessage(`Successfully processed ${data.rows_processed} positions.`);
      } else {
        setStatus('error');
        setMessage(data.detail || 'Upload failed');
      }
    } catch (error) {
      setStatus('error');
      setMessage(error.message);
    }
  };

  return (
    <div className="p-6 bg-slate-900 rounded-lg shadow-lg border border-slate-800 text-slate-200 w-full max-w-md">
      <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
        <UploadCloud className="text-blue-400" />
        Upload PMS Snapshot
      </h2>
      
      <div className="flex flex-col gap-4">
        <label className="border-2 border-dashed border-slate-700 p-8 text-center rounded-lg cursor-pointer hover:border-blue-500 transition-colors">
          <span className="text-slate-400">Select pms_upload_positions.csv</span>
          <input 
            type="file" 
            accept=".csv" 
            className="hidden" 
            onChange={handleFileChange} 
          />
        </label>
        
        {file && (
          <div className="text-sm bg-slate-800 p-2 rounded truncate text-slate-300">
            Selected: {file.name}
          </div>
        )}

        <button 
          onClick={handleUpload}
          disabled={!file || status === 'uploading'}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 text-white font-semibold py-2 px-4 rounded transition-colors"
        >
          {status === 'uploading' ? 'Uploading...' : 'Process Snapshot'}
        </button>

        {status === 'success' && (
          <div className="text-emerald-400 text-sm flex items-center gap-1">
            <CheckCircle size={16} /> {message}
          </div>
        )}
        
        {status === 'error' && (
          <div className="text-rose-400 text-sm flex items-center gap-1">
            <AlertCircle size={16} /> {message}
          </div>
        )}
      </div>
    </div>
  );
}
