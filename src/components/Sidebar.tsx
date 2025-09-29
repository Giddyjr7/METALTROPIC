import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { Home, Briefcase, ArrowDownCircle, ArrowUpCircle, Clock, BarChart2, FileText, Settings, HelpCircle, Menu } from "lucide-react";

const menuItems = [
  { name: "Dashboard", path: "/dashboard", icon: <Home size={20} /> },
  { name: "Portfolio", path: "/dashboard/portfolio", icon: <Briefcase size={20} /> },
  { name: "Deposit", path: "/dashboard/deposit", icon: <ArrowDownCircle size={20} /> },
  { name: "Withdraw", path: "/dashboard/withdraw", icon: <ArrowUpCircle size={20} /> },
  { name: "Transactions", path: "/dashboard/transactions", icon: <Clock size={20} /> },
  { name: "Plans", path: "/dashboard/plans", icon: <BarChart2 size={20} /> },
  { name: "Reports", path: "/dashboard/reports", icon: <FileText size={20} /> },
  { name: "Settings", path: "/dashboard/settings", icon: <Settings size={20} /> },
  { name: "Support", path: "/dashboard/support", icon: <HelpCircle size={20} /> },
];

const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  return (
    <>
      {/* Mobile toggle button */}
      <button
        className="lg:hidden p-4 text-white fixed top-2 left-2 z-50"
        onClick={() => setIsOpen(!isOpen)}
      >
        <Menu size={24} />
      </button>

      {/* Sidebar */}
      <aside className={`fixed lg:static top-0 left-0 h-full w-64 bg-crypto-blue/90 backdrop-blur-lg shadow-lg transform transition-transform duration-300 z-40 
        ${isOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}
      `}>
        <div className="p-6 text-white text-2xl font-bold">
          Metal<span className="text-crypto-purple">Tropic</span>
        </div>

        <ul className="mt-6 space-y-2">
          {menuItems.map((item) => (
            <li key={item.name}>
              <Link
                to={item.path}
                className={`flex items-center gap-3 px-6 py-3 rounded-lg transition-colors 
                  ${location.pathname === item.path ? "bg-crypto-purple text-white" : "text-gray-300 hover:bg-crypto-purple/30"}
                `}
                onClick={() => setIsOpen(false)} // Close on mobile
              >
                {item.icon}
                <span>{item.name}</span>
              </Link>
            </li>
          ))}
        </ul>
      </aside>
    </>
  );
};

export default Sidebar;
