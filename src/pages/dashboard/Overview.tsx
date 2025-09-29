export default function Overview() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Overview</h1>
      <p className="text-muted-foreground">
        Welcome to your investment dashboard. Here you can track balances, deposits, and withdrawals.
      </p>

      <div className="grid gap-4 md:grid-cols-3">
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
      </div>
    </div>
  );
}
