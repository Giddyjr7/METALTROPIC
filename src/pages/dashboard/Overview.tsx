import { ArrowDownCircle, ArrowUpCircle, Clock, PlusCircle } from "lucide-react";

export default function Overview() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold">Overview</h1>
        <p className="text-muted-foreground">
          Welcome to your investment dashboard. Get a snapshot of your balances,
          deposits, withdrawals, and recent activity.
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid gap-4 md:grid-cols-5">
        <div className="rounded-xl border border-border bg-card p-4">
          <h2 className="text-sm font-medium text-muted-foreground">Total Balance</h2>
          <p className="mt-2 text-2xl font-bold text-primary">$12,540</p>
        </div>
        <div className="rounded-xl border border-border bg-card p-4">
          <h2 className="text-sm font-medium text-muted-foreground">Active Investments</h2>
          <p className="mt-2 text-2xl font-bold">5</p>
        </div>
        <div className="rounded-xl border border-border bg-card p-4">
          <h2 className="text-sm font-medium text-muted-foreground">Pending Withdrawals</h2>
          <p className="mt-2 text-2xl font-bold text-destructive">$1,200</p>
        </div>
        <div className="rounded-xl border border-border bg-card p-4">
          <h2 className="text-sm font-medium text-muted-foreground">Total Deposits</h2>
          <p className="mt-2 text-2xl font-bold text-green-500">$8,400</p>
        </div>
        <div className="rounded-xl border border-border bg-card p-4">
          <h2 className="text-sm font-medium text-muted-foreground">Total Withdrawals</h2>
          <p className="mt-2 text-2xl font-bold text-blue-500">$4,600</p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid gap-4 md:grid-cols-3">
        <button className="flex items-center justify-center gap-2 rounded-xl border border-border bg-card p-4 text-sm font-medium transition hover:bg-muted">
          <ArrowDownCircle size={18} /> Deposit Now
        </button>
        <button className="flex items-center justify-center gap-2 rounded-xl border border-border bg-card p-4 text-sm font-medium transition hover:bg-muted">
          <ArrowUpCircle size={18} /> Withdraw Now
        </button>
        <button className="flex items-center justify-center gap-2 rounded-xl border border-border bg-card p-4 text-sm font-medium transition hover:bg-muted">
          <Clock size={18} /> View Transactions
        </button>
      </div>

      {/* Recent Transactions */}
      <div className="rounded-xl border border-border bg-card p-4">
        <h2 className="text-lg font-semibold mb-4">Recent Transactions</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="text-muted-foreground text-left border-b border-border">
              <tr>
                <th className="py-2">Type</th>
                <th className="py-2">Date</th>
                <th className="py-2">Status</th>
                <th className="py-2 text-right">Amount</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-b border-border">
                <td className="py-2">Deposit</td>
                <td className="py-2">Sep 20, 2025</td>
                <td className="py-2 text-green-500">Completed</td>
                <td className="py-2 text-right">$500</td>
              </tr>
              <tr className="border-b border-border">
                <td className="py-2">Withdrawal</td>
                <td className="py-2">Sep 18, 2025</td>
                <td className="py-2 text-yellow-500">Pending</td>
                <td className="py-2 text-right">$200</td>
              </tr>
              <tr>
                <td className="py-2">Deposit</td>
                <td className="py-2">Sep 15, 2025</td>
                <td className="py-2 text-green-500">Completed</td>
                <td className="py-2 text-right">$1,000</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Investment Performance (Placeholder) */}
      <div className="rounded-xl border border-border bg-card p-4">
        <h2 className="text-lg font-semibold mb-4">Investment Performance</h2>
        <div className="h-48 flex items-center justify-center text-muted-foreground">
          📊 Chart Placeholder (Add Recharts/Chart.js later)
        </div>
      </div>
    </div>
  );
}
