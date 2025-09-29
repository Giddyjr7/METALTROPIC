import React from "react";
import {
  Grid,
  TrendingUp,
  Bell,
  Search,
  UserCircle,
  DollarSign,
} from "lucide-react";
import { Button } from "@/components/ui/button";

/**
 * Dashboard.tsx
 * Drop this file into src/pages/ and then add a route in App.tsx:
 *   <Route path="/dashboard" element={<Dashboard />} />
 *
 * Replace dummy data with real API values when ready.
 */

const marketData = [
  { label: "DJA", value: "32,778.64", change: "+293", pct: "+0.90" },
  { label: "NAS", value: "32,778.64", change: "-78.81", pct: "-0.90" },
  { label: "S&P", value: "39,345.64", change: "+4.00", pct: "+0.10" },
];

const watchlist = [
  { symbol: "PLTR", change: "+4.48%", last: "124.20" },
  { symbol: "ETSY", change: "+2.42%", last: "221.11" },
  { symbol: "PINS", change: "+0.32%", last: "80.49" },
  { symbol: "SNOW", change: "-0.78%", last: "37.85" },
];

const transactions = [
  { symbol: "PINS", type: "Buy", qty: 15, price: "71.75", total: "1,076.25" },
  { symbol: "TWLO", type: "Sell", qty: 12, price: "36.9", total: "442.8" },
  { symbol: "PLTR", type: "Buy", qty: 45, price: "27.05", total: "1,217.25" },
  { symbol: "SQ", type: "Buy", qty: 10, price: "242", total: "2,420" },
];

const notifications = [
  {
    id: 1,
    title: "George N.",
    text: "Are you investing in FNTS? It is a great opportunity.",
    time: "10 min ago",
  },
  {
    id: 2,
    title: "APPLE (NASDAQ)",
    text: "Movement +0.35 (0.27%)",
    time: "15 min ago",
  },
  {
    id: 3,
    title: "SPLK (NASDAQ)",
    text: "Splunk Inc. Announces Fiscal Fourth Quarter",
    time: "3 hours ago",
  },
];

function Sidebar() {
  return (
    <aside className="w-20 bg-[#0f0f12] min-h-screen p-4 flex flex-col items-center gap-6">
      <div className="w-10 h-10 rounded-full bg-crypto-purple flex items-center justify-center text-white font-bold">
        M
      </div>
      <nav className="flex flex-col gap-4 mt-2">
        <button className="p-2 rounded-lg bg-[#16161a] text-white">
          <Grid size={18} />
        </button>
        <button className="p-2 rounded-lg text-gray-400 hover:text-white">
          <TrendingUp size={18} />
        </button>
        <button className="p-2 rounded-lg text-gray-400 hover:text-white">
          <DollarSign size={18} />
        </button>
        <button className="p-2 rounded-lg text-gray-400 hover:text-white">
          <UserCircle size={18} />
        </button>
      </nav>

      <div className="mt-auto">
        <div className="w-12 h-12 rounded-lg bg-crypto-purple flex items-center justify-center text-white relative">
          🎧
          <span className="absolute -top-1 -right-1 bg-white text-crypto-purple rounded-full w-5 h-5 flex items-center justify-center text-xs">
            1
          </span>
        </div>
      </div>
    </aside>
  );
}

function Topbar() {
  return (
    <div className="flex items-center justify-between py-4 px-6">
      <div>
        <h2 className="text-2xl font-semibold">Dashboard</h2>
        <p className="text-sm text-muted-foreground">A quick preview of what's going on with markets</p>
      </div>

      <div className="flex items-center gap-4">
        <button className="p-2 rounded-lg bg-crypto-purple text-white">Trade</button>
        <div className="flex items-center gap-3 bg-[#111214] rounded-lg px-3 py-2">
          <Search size={16} className="text-gray-300" />
          <Bell size={16} className="text-purple-300" />
          <div className="w-8 h-8 rounded-full bg-[#20202a] flex items-center justify-center overflow-hidden">
            <img src="https://i.pravatar.cc/40" alt="avatar" />
          </div>
        </div>
      </div>
    </div>
  );
}

function MarketCards() {
  return (
    <div className="flex gap-4">
      {marketData.map((m) => (
        <div key={m.label} className="flex-1 bg-[#121217] rounded-xl p-4">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-xs text-muted-foreground">{m.label}</div>
              <div className="text-lg font-semibold">{m.value}</div>
            </div>
            <div className={`text-sm ${m.pct.startsWith("+") ? "text-emerald-400" : "text-red-400"} bg-[#0f0f12] px-3 py-1 rounded-full`}>
              <div className="text-xs">{m.change}</div>
              <div className="text-xs">{m.pct}</div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

function ChartArea() {
  // Simple SVG area chart placeholder with purple gradient
  return (
    <div className="bg-transparent rounded-xl p-6 mt-6">
      <div className="bg-[#0f0f12] rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="text-sm text-muted-foreground">US MARKET</div>
          <div className="text-sm text-muted-foreground">1 Month • 6 Months • Year • Total</div>
        </div>

        <div className="w-full h-56">
          <svg viewBox="0 0 800 220" className="w-full h-full">
            <defs>
              <linearGradient id="g1" x1="0" x2="0" y1="0" y2="1">
                <stop offset="0%" stopColor="#9B87F5" stopOpacity="0.85" />
                <stop offset="100%" stopColor="#1E2233" stopOpacity="0.1" />
              </linearGradient>
              <linearGradient id="stroke" x1="0" x2="1">
                <stop offset="0%" stopColor="#B189FF" />
                <stop offset="100%" stopColor="#8C63F0" />
              </linearGradient>
              <filter id="blur" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="6" />
              </filter>
            </defs>

            <path d="M0,140 C80,100 160,150 240,120 320,90 400,160 480,130 560,100 640,140 720,120 800,110" fill="url(#g1)" stroke="none" />
            <path d="M0,140 C80,100 160,150 240,120 320,90 400,160 480,130 560,100 640,140 720,120 800,110" fill="none" stroke="url(#stroke)" strokeWidth="3" strokeLinecap="round" />
          </svg>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-2 gap-4">
        <div className="bg-[#0f0f12] rounded-xl p-4">
          <h4 className="text-sm text-muted-foreground">WATCHLIST</h4>
          <table className="w-full mt-3 text-sm">
            <thead>
              <tr className="text-left text-xs text-muted-foreground">
                <th>Symbol</th>
                <th>Change</th>
                <th>Last</th>
              </tr>
            </thead>
            <tbody>
              {watchlist.map((w) => (
                <tr key={w.symbol} className="border-t border-[#1b1b1f]">
                  <td className="py-2">{w.symbol}</td>
                  <td className={`py-2 ${w.change.startsWith("+") ? "text-emerald-400" : "text-red-400"}`}>{w.change}</td>
                  <td className="py-2 text-muted-foreground">{w.last}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="bg-[#0f0f12] rounded-xl p-4">
          <h4 className="text-sm text-muted-foreground">LATEST TRANSACTIONS</h4>
          <table className="w-full mt-3 text-sm">
            <thead>
              <tr className="text-left text-xs text-muted-foreground">
                <th>Symbol</th>
                <th>Type</th>
                <th>Qty</th>
                <th>Price</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              {transactions.map((t, idx) => (
                <tr key={idx} className="border-t border-[#1b1b1f]">
                  <td className="py-2">{t.symbol}</td>
                  <td className={`py-2 ${t.type === "Buy" ? "text-emerald-400" : "text-red-400"}`}>{t.type}</td>
                  <td className="py-2">{t.qty}</td>
                  <td className="py-2">{t.price}</td>
                  <td className="py-2">{t.total}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

function RightSidebar() {
  return (
    <aside className="w-80 flex-shrink-0">
      <div className="space-y-4">
        <div className="bg-[#0f0f12] rounded-xl p-4">
          <h5 className="text-sm text-muted-foreground">OVERVIEW</h5>
          <div className="mt-3 text-sm">
            <div className="flex justify-between">
              <div>Account</div>
              <div className="text-muted-foreground">55EWASS2</div>
            </div>
            <div className="flex justify-between mt-2">
              <div>Portfolio value</div>
              <div className="font-semibold">$12,581</div>
            </div>
            <div className="flex justify-between mt-2">
              <div>Total invested</div>
              <div className="text-muted-foreground">8,210$</div>
            </div>
            <div className="flex justify-between mt-2">
              <div>Available funds</div>
              <div className="text-emerald-400">+1,020.11</div>
            </div>
            <div className="flex justify-between mt-2">
              <div>Daily P&L</div>
              <div className="text-muted-foreground">2,384$</div>
            </div>
            <div className="flex justify-between mt-2">
              <div>Upcoming Dividends</div>
              <div className="text-muted-foreground">55,705</div>
            </div>
          </div>
        </div>

        <div className="bg-[#0f0f12] rounded-xl p-4">
          <h5 className="text-sm text-muted-foreground">NOTIFICATIONS</h5>
          <div className="mt-3 space-y-3">
            {notifications.map((n) => (
              <div key={n.id} className="flex items-start gap-3">
                <div className="w-10 h-10 rounded-full bg-[#20202a] flex items-center justify-center text-sm">A</div>
                <div>
                  <div className="text-sm font-medium">{n.title}</div>
                  <div className="text-xs text-muted-foreground">{n.text}</div>
                  <div className="text-xs text-muted-foreground mt-1">{n.time}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-[#0f0f12] rounded-xl p-4">
          <h5 className="text-sm text-muted-foreground">QUICK ACTIONS</h5>
          <div className="mt-3 grid gap-2">
            <Button className="bg-crypto-purple text-white">Deposit</Button>
            <Button variant="ghost" className="text-white">Withdraw</Button>
            <Button variant="ghost" className="text-white">Transfer</Button>
          </div>
        </div>
      </div>
    </aside>
  );
}

export default function Dashboard() {
  return (
    <div className="min-h-screen flex bg-background text-foreground">
      <Sidebar />

      <main className="flex-1 px-6 py-6 overflow-auto">
        <Topbar />
        <MarketCards />
        <ChartArea />
      </main>

      <RightSidebar />
    </div>
  );
}
