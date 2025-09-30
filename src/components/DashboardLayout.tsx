import { useState } from "react";
import { Link, Outlet } from "react-router-dom";
import {
  LayoutDashboard,
  ArrowDownCircle,
  ArrowUpCircle,
  Clock,
  User,
  Menu,
  X,
  ChevronDown,
} from "lucide-react";

export default function DashboardLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const menuItems = [
    { name: "Overview", icon: <LayoutDashboard size={18} />, path: "/dashboard" },
    { name: "Deposit", icon: <ArrowDownCircle size={18} />, path: "/dashboard/deposit" },
    { name: "Withdraw", icon: <ArrowUpCircle size={18} />, path: "/dashboard/withdraw" },
    { name: "Transactions", icon: <Clock size={18} />, path: "/dashboard/transactions" },
    { name: "Profile", icon: <User size={18} />, path: "/dashboard/profile" },
  ];

  return (
    <div className="flex min-h-screen bg-background text-foreground">
      {/* Sidebar */}
      <aside
        className={`fixed top-0 left-0 z-40 h-full w-64 transform border-r border-border bg-card transition-transform lg:translate-x-0 ${
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="flex items-center justify-between p-4 border-b border-border">
          <h1 className="text-lg font-bold text-primary">MetalTropic</h1>
          <button className="lg:hidden" onClick={() => setSidebarOpen(false)}>
            <X size={20} />
          </button>
        </div>
        <nav className="flex flex-col p-4 space-y-2">
          {menuItems.map((item) => (
            <Link
              key={item.name}
              to={item.path}
              className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors hover:bg-muted"
              onClick={() => setSidebarOpen(false)}
            >
              {item.icon}
              {item.name}
            </Link>
          ))}
        </nav>
      </aside>

      {/* Main Content */}
      <div className="flex flex-1 flex-col lg:ml-64">
        {/* Topbar */}
        <header className="flex items-center justify-between border-b border-border bg-card px-4 py-3 lg:px-6">
          {/* Mobile sidebar toggle */}
          <button className="lg:hidden" onClick={() => setSidebarOpen(true)}>
            <Menu size={22} />
          </button>

          {/* Page title */}
          <h2 className="text-lg font-semibold">Welcome Giddy</h2>

          {/* Profile section (dummy) */}
          <div className="flex items-center gap-3">
            <img
              src="https://via.placeholder.com/32"
              alt="Profile"
              className="h-8 w-8 rounded-full border border-border"
            />
            <span className="text-sm font-medium">Giddyjr7</span>
            <ChevronDown size={18} className="text-muted-foreground" />
          </div>
        </header>

        {/* Outlet for nested pages */}
        <main className="flex-1 p-4 lg:p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
