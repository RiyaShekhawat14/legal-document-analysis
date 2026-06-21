function HighlightedText({ text, keywords }) {
  const parts = text.split(new RegExp(`(${keywords.join("|")})`, "gi"));

  return (
    <p className="highlighted-text">
      {parts.map((part, index) =>
        keywords.some((word) => word.toLowerCase() === part.toLowerCase()) ? (
          <span key={index} className="highlight">
            {part}
          </span>
        ) : (
          <span key={index}>{part}</span>
        ),
      )}
    </p>
  );
}

export default HighlightedText;
