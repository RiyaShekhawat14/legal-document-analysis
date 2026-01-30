function RiskBadge({ level }) {
  const getColor = () => {
    if (level === "High") return "risk-high";
    if (level === "Medium") return "risk-medium";
    return "risk-low";
  };

  return (
    <span className={`risk-badge ${getColor()}`}>
      {level} Risk
    </span>
  );
}

export default RiskBadge;
