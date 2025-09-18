import React from 'react';
import { Activity, Lock, Zap, Compass, LineChart, Shield } from 'lucide-react';

export const features = [
  {
    icon: <Activity className="h-6 w-6" />,
    title: "Real-time Analytics",
    description: "Track your investments with advanced insights and performance reports updated in real-time"
  },
  {
    icon: <Lock className="h-6 w-6" />,
    title: "Bank-level Security",
    description: "Your funds are protected with military-grade encryption and multi-factor authentication."
  },
  {
    icon: <Zap className="h-6 w-6" />,
    title: "Instant Transactions",
    description: "Make deposits and withdrawals seamlessly with our high-performance system."
  },
  {
    icon: <Compass className="h-6 w-6" />,
    title: "Smart Portfolio",
    description: "Optimize your investments with AI-powered strategies and personalized recommendations."
  },
  {
    icon: <LineChart className="h-6 w-6" />,
    title: "Investment Alerts",
    description: "Stay ahead with customizable investment alerts and timely notifications."
  },
  {
    icon: <Shield className="h-6 w-6" />,
    title: "Secure Fund Management",
    description: "Majority of funds stored securely with top-tier financial protection."
  }
];
