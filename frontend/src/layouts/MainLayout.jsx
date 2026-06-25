import React from 'react';

import { HoldingsGrid } from '../features/portfolio/HoldingsGrid';
import { OrderTicket } from '../features/oms/OrderTicket';
import { TradeBlotter } from '../features/oms/TradeBlotter';

export const MainLayout = () => {
  return (
    <div className="dashboard-grid">
      
      {/* Main Panel: Holdings Grid */}
      <div className="dashboard-panel-main">
        <HoldingsGrid />
      </div>

      {/* Side Top Panel: Order Ticket */}
      <div className="dashboard-panel-side-top">
        <OrderTicket />
      </div>

      {/* Side Bottom Panel: Trade Blotter */}
      <div className="dashboard-panel-side-bottom">
        <TradeBlotter />
      </div>

    </div>
  );
};
