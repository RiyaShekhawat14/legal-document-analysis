function RiskBadge({ level = "Unknown", compact = false }) {
  const normalized = level.toLowerCase();
  let variant = "risk-neutral";

  if (normalized.includes("high")) {
    variant = "risk-high";
  } else if (normalized.includes("medium")) {
    variant = "risk-medium";
  } else if (normalized.includes("low")) {
    variant = "risk-low";
  }

  return (
    <span className={`risk-badge ${variant}${compact ? " risk-badge-compact" : ""}`}>
      {level}
    </span>
  );
}

export default RiskBadge;
