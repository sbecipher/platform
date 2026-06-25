import { create } from 'zustand';

const xDevHoldings = [
  { symbol: 'IE', quantity: '29,022', value: '$547,645', pnl: '+$188,566', exposure: '7.31%', isPositive: true },
  { symbol: 'UEC', quantity: '37,219', value: '$599,225', pnl: '+$283,819', exposure: '8.00%', isPositive: true },
  { symbol: 'AA', quantity: '30,324', value: '$1,763,643', pnl: '+$580,386', exposure: '23.54%', isPositive: true },
  { symbol: 'AMR', quantity: '3,780', value: '$789,112', pnl: '+$162,684', exposure: '10.53%', isPositive: true },
  { symbol: 'BTU', quantity: '37,460', value: '$1,311,474', pnl: '+$385,032', exposure: '17.50%', isPositive: true },
  { symbol: 'CDE', quantity: '62,778', value: '$1,302,643', pnl: '+$478,684', exposure: '17.39%', isPositive: true },
  { symbol: 'CLF', quantity: '82,492', value: '$1,198,608', pnl: '+$264,023', exposure: '16.00%', isPositive: true },
  { symbol: 'URG', quantity: '-1,982', value: '-$3,270', pnl: '-$652', exposure: '-0.04%', isPositive: false },
  { symbol: 'USAR', quantity: '-40,109', value: '-$943,764', pnl: '-$291,886', exposure: '-12.60%', isPositive: false }
];

export const useWorkspaceStore = create((set) => ({
  holdings: xDevHoldings,
  metrics: {
    totalNav: "$0.00",
    dayPnl: "$0.00",
    dayPnlPct: "0.00%",
    grossExposure: "0.00%",
    netExposure: "0.00%",
    portfolioBeta: "0.00",
    availableCash: "$0.00",
    activeOrders: "0",
    isDayPnlPositive: true
  },
  themePreference: 'system',
  livePrices: {}, // tracks symbol -> { price, direction }
  
  setHoldings: (newHoldings) => set({ holdings: newHoldings }),
  setThemePreference: (theme) => set({ themePreference: theme }),
  
  fetchPortfolio: async () => {
    try {
      const response = await fetch('/api/portfolio/sbecipher_pm_lp');
      if (response.ok) {
        const data = await response.json();
        const formattedHoldings = data.positions.map(p => ({
          symbol: p.symbol,
          quantity: p.quantity.toLocaleString(undefined, { maximumFractionDigits: 0 }),
          price: p.latest_price,
          value: '$' + p.market_value.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 0 }),
          pnl: (p.day_profit >= 0 ? '+$' : '-$') + Math.abs(p.day_profit).toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 0 }),
          exposure: p.exposure_pct.toFixed(2) + '%',
          isPositive: p.day_profit >= 0
        }));
        const formattedMetrics = {
          totalNav: '$' + data.metrics.portfolio_nav.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
          dayPnl: (data.metrics.day_pnl >= 0 ? '+$' : '-$') + Math.abs(data.metrics.day_pnl).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
          dayPnlPct: ((data.metrics.day_pnl / data.metrics.portfolio_nav) * 100).toFixed(2) + '%',
          grossExposure: data.metrics.gross_exposure_pct.toFixed(2) + '%',
          netExposure: data.metrics.net_exposure_pct.toFixed(2) + '%',
          portfolioBeta: "1.15", // mock beta
          availableCash: '$150,000.00', // mock cash
          activeOrders: "4", // mock active orders
          isDayPnlPositive: data.metrics.day_pnl >= 0
        };
        set({ holdings: formattedHoldings, metrics: formattedMetrics });
      }
    } catch (err) {
      console.error("Failed to fetch portfolio:", err);
    }
  },

  updatePrices: (ticks) => set((state) => {
    const newPrices = { ...state.livePrices };
    ticks.forEach(tick => {
      const prevPrice = newPrices[tick.symbol]?.price || tick.last_price;
      newPrices[tick.symbol] = {
        price: tick.last_price,
        direction: tick.last_price > prevPrice ? 'up' : tick.last_price < prevPrice ? 'down' : 'flat',
        timestamp: tick.timestamp
      };
    });
    return { livePrices: newPrices };
  })
}));
