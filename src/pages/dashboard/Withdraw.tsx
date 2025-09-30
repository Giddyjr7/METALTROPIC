import { useState } from "react";

export default function Withdraw() {
  const [selectedMethod, setSelectedMethod] = useState("USDT BEP20");
  const [amount, setAmount] = useState("");

  const paymentMethods = [
    { name: "USDT BEP20", icon: "🟢" },
    { name: "USDT TRC20", icon: "💠" },
    { name: "BITCOIN", icon: "₿" },
  ];

  return (
    <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
      {/* Header */}
      <div className="rounded-t-lg bg-primary px-4 py-2 text-center text-lg font-semibold text-primary-foreground">
        Withdraw
      </div>

      <div className="mt-6 grid gap-6 md:grid-cols-2">
        {/* Left side - Withdrawal Methods */}
        <div className="space-y-4">
          {paymentMethods.map((method) => (
            <label
              key={method.name}
              className={`flex items-center justify-between rounded-lg border px-4 py-3 cursor-pointer ${
                selectedMethod === method.name
                  ? "border-primary bg-muted"
                  : "border-border"
              }`}
            >
              <div className="flex items-center gap-3">
                <input
                  type="radio"
                  name="withdraw"
                  value={method.name}
                  checked={selectedMethod === method.name}
                  onChange={() => setSelectedMethod(method.name)}
                  className="text-primary focus:ring-primary"
                />
                <span className="font-medium">{method.name}</span>
              </div>
              <span className="text-xl">{method.icon}</span>
            </label>
          ))}
        </div>

        {/* Right side - Withdraw Form */}
        <div className="space-y-4">
          {/* Amount Input */}
          <div>
            <label className="block text-sm font-medium">Amount</label>
            <div className="mt-1 flex items-center rounded-md border border-border bg-background px-3 py-2">
              <span className="text-muted-foreground">$</span>
              <input
                type="number"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="0.00"
                className="ml-2 flex-1 bg-transparent text-sm focus:outline-none"
              />
            </div>
          </div>

          {/* Details */}
          <div className="space-y-2 text-sm text-muted-foreground">
            <div className="flex justify-between">
              <span>Limit</span>
              <span>$5.00 USD - $1,000,000.00 USD</span>
            </div>
            <div className="flex justify-between">
              <span>Processing Charge</span>
              <span>0.00 USD</span>
            </div>
            <div className="flex justify-between">
              <span>Receivable</span>
              <span>0.00 USD</span>
            </div>
            <div className="flex justify-between">
              <span>Conversion</span>
              <span>1 USD = 1.00 $</span>
            </div>
            <div className="flex justify-between">
              <span>In $</span>
              <span>0.00</span>
            </div>
          </div>

          {/* Confirm Button */}
          <button className="w-full rounded-lg bg-primary px-4 py-2 font-medium text-primary-foreground hover:opacity-90">
            Confirm Withdraw
          </button>

          {/* Info */}
          <p className="text-xs text-muted-foreground">
            Safely withdraw your funds using our highly secure process and
            various withdrawal method.
          </p>
        </div>
      </div>
    </div>
  );
}
