import ChartCard from "./ChartCard";
import StatsCard from "./StatsCard";

function Dashboard() {
  return (
    <div className="dashboard">
      <div className="top-row">
        <ChartCard />
        <ChartCard />
      </div>
      <div className="bottom-row">
        <StatsCard title="Users" value="1,245" trend={5} />
        <StatsCard title="Sales" value="₹32K" trend={-2} />
        <StatsCard title="Sessions" value="8,432" trend={3} />
      </div>
    </div>
  );
}

export default Dashboard;
