import { Home, BarChart, Settings, Activity } from "lucide-react";

function Sidebar() {
  return (
    <div className="sidebar">
      <h2 className="logo">AI Assist</h2>
      <ul>
        <li><Home size={20}/> Dashboard</li>
        <li><BarChart size={20}/> Analytics</li>
        <li><Activity size={20}/> Reports</li>
        <li><Settings size={20}/> Settings</li>
      </ul>
    </div>
  );
}

export default Sidebar;
