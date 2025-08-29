function StatsCard({ title, value, trend }) {
  return (
    <div className="card stats-card">
      <h5>{title}</h5>
      <p className="value">{value}</p>
      <span className={trend > 0 ? "up" : "down"}>
        {trend > 0 ? `▲ ${trend}%` : `▼ ${trend}%`}
      </span>
    </div>
  );
}

export default StatsCard;
