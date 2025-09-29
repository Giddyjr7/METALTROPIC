export default function Deposit() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Deposit Funds</h1>
      <form className="space-y-4 max-w-md">
        <div>
          <label className="block text-sm font-medium">Amount (USD)</label>
          <input
            type="number"
            placeholder="Enter amount"
            className="mt-1 w-full rounded-md border border-border bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
          />
        </div>
        <button
          type="submit"
          className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:opacity-90"
        >
          Deposit
        </button>
      </form>
    </div>
  );
}
