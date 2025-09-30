import { useLocation } from "react-router-dom";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const ConfirmDeposit = () => {
  const location = useLocation();
  const { amount } = location.state || { amount: "0.00" };

  // Example calculation (add fee, adjust dynamically)
  const fee = 1.5;
  const total = (parseFloat(amount) + fee).toFixed(2);

  const walletAddress = "bc1qcl84vkhs9aur0qcf02n8xfwk6pe95zrtq7f05w";

  return (
    <div className="p-6">
      {/* Top header bar */}
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold text-primary">Confirm Deposit</h2>
        <div className="flex items-center space-x-3">
          <span className="font-medium">John Doe</span>
          <img
            src="https://via.placeholder.com/40"
            alt="profile"
            className="w-10 h-10 rounded-full"
          />
        </div>
      </div>

      {/* Confirmation Card */}
      <Card className="rounded-2xl border border-border bg-card">
        <CardContent className="p-6 space-y-5">
          <div className="p-4 border border-border rounded-lg bg-background">
            <p>
              You are requesting{" "}
              <span className="font-bold text-primary">${amount} USD</span> to deposit.
              Please pay{" "}
              <span className="font-bold text-primary">{total} $</span> for
              successful payment.
            </p>
          </div>

          <p className="text-sm text-muted-foreground">
            Deposit to the USDT wallet address below
          </p>
          <div className="p-3 rounded-lg bg-background font-mono text-sm border border-border">
            {walletAddress}
          </div>

          <div className="space-y-2">
            <label className="font-medium text-foreground">Payment Proof</label>
            <input
              type="file"
              accept=".jpg,.jpeg,.png,.pdf"
              className="block w-full border border-border rounded-lg p-2 bg-background"
            />
            <p className="text-xs text-muted-foreground">
              Supported formats: jpg, jpeg, png, pdf
            </p>
          </div>

          <Button className="w-full bg-primary hover:opacity-90 text-primary-foreground rounded-xl">
            Pay Now
          </Button>
        </CardContent>
      </Card>
    </div>
  );
};

export default ConfirmDeposit;
