import React, { useRef } from 'react';
import { Layout, Model } from 'flexlayout-react';
import 'flexlayout-react/style/dark.css';

import { HoldingsGrid } from '../features/portfolio/HoldingsGrid';
import { OrderTicket } from '../features/oms/OrderTicket';
import { TradeBlotter } from '../features/oms/TradeBlotter';
import { PortfolioModeling } from '../features/modeling/PortfolioModeling';

// FlexLayout JSON configuration
const json = {
  global: {
    tabEnableClose: true,
    tabEnableRename: false,
    tabSetEnableMaximize: true,
    tabEnableFloat: true,
    tabSetTabStripHeight: 35,
  },
  borders: [],
  layout: {
    type: "row",
    weight: 100,
    children: [
      {
        type: "tabset",
        weight: 60,
        children: [
          {
            type: "tab",
            name: "Portfolio Holdings",
            component: "HoldingsGrid",
          },
          {
            type: "tab",
            name: "Modeling & Rebalancing",
            component: "PortfolioModeling",
          }
        ]
      },
      {
        type: "column",
        weight: 40,
        children: [
          {
            type: "tabset",
            weight: 50,
            children: [
              {
                type: "tab",
                name: "Order Ticket",
                component: "OrderTicket",
              }
            ]
          },
          {
            type: "tabset",
            weight: 50,
            children: [
              {
                type: "tab",
                name: "Trade Blotter",
                component: "TradeBlotter",
              }
            ]
          }
        ]
      }
    ]
  }
};

export const MainLayout = () => {
  const model = useRef(Model.fromJson(json));

  const factory = (node) => {
    const component = node.getComponent();
    switch (component) {
      case "HoldingsGrid":
        return <HoldingsGrid />;
      case "OrderTicket":
        return <OrderTicket />;
      case "TradeBlotter":
        return <TradeBlotter />;
      case "PortfolioModeling":
        return <PortfolioModeling />;
      default:
        return <div>Component not found</div>;
    }
  };

  return (
    <div style={{ position: 'relative', width: '100%', height: 'calc(100vh - 70px)' }}>
      <Layout 
        model={model.current} 
        factory={factory} 
      />
    </div>
  );
};
