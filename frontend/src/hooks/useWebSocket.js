import { useEffect, useRef } from 'react';
import { useWorkspaceStore } from '../store/workspaceStore';

export const useWebSocket = (url) => {
  const ws = useRef(null);
  const updatePrices = useWorkspaceStore(state => state.updatePrices);

  useEffect(() => {
    ws.current = new WebSocket(url);

    ws.current.onopen = () => {
      console.log('WebSocket connected to', url);
    };

    ws.current.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        if (payload.type === 'MARKET_TICK') {
          if (updatePrices) {
             updatePrices(payload.data);
          }
        }
      } catch (err) {
        console.error('Failed to parse WS message', err);
      }
    };

    ws.current.onclose = () => {
      console.log('WebSocket disconnected from', url);
    };

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [url, updatePrices]);

  return ws.current;
};
