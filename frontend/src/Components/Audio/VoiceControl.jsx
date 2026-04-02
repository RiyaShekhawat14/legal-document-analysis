import React from "react";

function VoiceControl({ setVoiceLang, setSpeechRate }) {
  return (
    <div className="card">
      <h3>🎙 Voice Settings</h3>

      <label>Voice Language:</label>
      <select onChange={(e) => setVoiceLang(e.target.value)}>
        <option value="en">English</option>
        <option value="hi">Hindi</option>
      </select>

      <label style={{ marginTop: "10px" }}>Speech Speed:</label>
      <select onChange={(e) => setSpeechRate(parseFloat(e.target.value))}>
        <option value="0.8">0.8x</option>
        <option value="1">1x</option>
        <option value="1.2">1.2x</option>
      </select>
    </div>
  );
}

export default VoiceControl;