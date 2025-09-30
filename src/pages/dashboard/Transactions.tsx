export default function Transactions() {
  const history = [
  { id: 1, type: "Deposit", amount: "$500", date: "2025-09-15" },
  { id: 2, type: "Withdraw", amount: "$200", date: "2025-09-20" },
  { id: 3, type: "Deposit", amount: "$1,000", date: "2025-09-22" },
  { id: 4, type: "Withdraw", amount: "$150", date: "2025-09-23" },
  { id: 5, type: "Deposit", amount: "$2,500", date: "2025-09-24" },
  { id: 6, type: "Deposit", amount: "$300", date: "2025-09-25" },
  { id: 7, type: "Withdraw", amount: "$100", date: "2025-09-26" },
  { id: 8, type: "Deposit", amount: "$750", date: "2025-09-27" },
  { id: 9, type: "Withdraw", amount: "$400", date: "2025-09-28" },
  { id: 10, type: "Deposit", amount: "$1,200", date: "2025-09-29" },
];

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Transaction History</h1>
      <div className="overflow-x-auto">
        <table className="min-w-full border border-border text-sm">
          <thead className="bg-muted">
            <tr>
              <th className="px-4 py-2 text-left">Type</th>
              <th className="px-4 py-2 text-left">Amount</th>
              <th className="px-4 py-2 text-left">Date</th>
            </tr>
          </thead>
          <tbody>
            {history.map((tx) => (
              <tr key={tx.id} className="border-t border-border">
                <td className="px-4 py-2">{tx.type}</td>
                <td className="px-4 py-2">{tx.amount}</td>
                <td className="px-4 py-2">{tx.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
