import React, { useMemo, useRef, useEffect, useState } from 'react';
import {
  flexRender,
  getCoreRowModel,
  useReactTable,
} from '@tanstack/react-table';
import { useVirtualizer } from '@tanstack/react-virtual';
import { useWorkspaceStore } from '../../store/workspaceStore';
import { useWebSocket } from '../../hooks/useWebSocket';

export const HoldingsGrid = () => {
  const data = useWorkspaceStore((state) => state.holdings);
  const livePrices = useWorkspaceStore((state) => state.livePrices);
  
  // Connect to the FastAPI WebSocket
  useWebSocket('ws://localhost:8000/ws/market-data');

  const columns = useMemo(
    () => [
      {
        accessorKey: 'symbol',
        header: 'Symbol',
        cell: info => <span style={{ fontWeight: 600 }}>{info.getValue()}</span>,
      },
      {
        accessorKey: 'quantity',
        header: 'Quantity',
      },
      {
        accessorKey: 'price',
        header: 'Last Price',
        cell: info => {
          const symbol = info.row.original.symbol;
          const liveData = livePrices[symbol];
          
          if (liveData) {
            const color = liveData.direction === 'up' ? 'var(--status-positive)' : liveData.direction === 'down' ? 'var(--status-negative)' : 'inherit';
            return <span style={{ color, transition: 'color 0.3s' }}>${liveData.price.toFixed(2)}</span>;
          }
          return <span>-</span>;
        }
      },
      {
        accessorKey: 'value',
        header: 'Market Value',
      },
      {
        accessorKey: 'pnl',
        header: 'Unrealized PnL',
        cell: info => {
          const val = info.getValue();
          const isPositive = val && val.startsWith('+');
          return <span className={isPositive ? 'text-positive' : 'text-negative'}>{val}</span>;
        }
      },
      {
        accessorKey: 'exposure',
        header: 'Exposure (NAV)',
      },
    ],
    [livePrices]
  );

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  const tableContainerRef = useRef(null);

  const { rows } = table.getRowModel();
  
  const rowVirtualizer = useVirtualizer({
    count: rows.length,
    getScrollElement: () => tableContainerRef.current,
    estimateSize: () => 40,
    overscan: 10,
  });

  return (
    <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', height: '100%', width: '100%', boxSizing: 'border-box' }}>
      <div style={{ padding: '16px 24px', borderBottom: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2 style={{ fontWeight: 600, margin: 0, fontSize: '1.125rem' }}>Portfolio Holdings (IBOR)</h2>
        <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
          <span style={{ display: 'inline-block', width: 8, height: 8, borderRadius: '50%', backgroundColor: 'var(--status-positive)', marginRight: 6 }}></span>
          {rows.length} Positions Live
        </span>
      </div>
      
      <div 
        ref={tableContainerRef}
        className="modern-table-container" 
        style={{ flex: 1, overflow: 'auto', position: 'relative' }}
      >
        <table className="modern-table" style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead style={{ position: 'sticky', top: 0, backgroundColor: 'var(--bg-panel)', zIndex: 1, display: 'flex', width: '100%' }}>
            {table.getHeaderGroups().map(headerGroup => (
              <tr key={headerGroup.id} style={{ display: 'flex', width: '100%' }}>
                {headerGroup.headers.map(header => (
                  <th key={header.id} style={{ flex: 1, padding: '12px 24px', textAlign: 'left', borderBottom: '1px solid var(--border-color)', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                    {header.isPlaceholder
                      ? null
                      : flexRender(
                          header.column.columnDef.header,
                          header.getContext()
                        )}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody style={{ height: `${rowVirtualizer.getTotalSize()}px`, position: 'relative' }}>
            {rowVirtualizer.getVirtualItems().map(virtualRow => {
              const row = rows[virtualRow.index];
              return (
                <tr 
                  key={row.id}
                  style={{
                    display: 'flex',
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    transform: `translateY(${virtualRow.start}px)`,
                  }}
                >
                  {row.getVisibleCells().map(cell => (
                    <td key={cell.id} style={{ flex: 1, padding: '12px 24px', borderBottom: '1px solid var(--border-glass)' }}>
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
