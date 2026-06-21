function VoiceControl({ setVoiceLang, setSpeechRate }) {
  return (
    <div className="card">
      <span className="section-kicker">Voice output</span>
      <h3>Playback settings</h3>

      <div className="voice-row">
        <label htmlFor="voice-language">Voice language</label>
        <select id="voice-language" onChange={(e) => setVoiceLang(e.target.value)}>
          <option value="en">English</option>
          <option value="hi">Hindi</option>
        </select>
      </div>

      <div className="voice-row">
        <label htmlFor="speech-rate">Speech speed</label>
        <select
          id="speech-rate"
          onChange={(e) => setSpeechRate(parseFloat(e.target.value))}
        >
          <option value="0.8">0.8x</option>
          <option value="1">1x</option>
          <option value="1.2">1.2x</option>
        </select>
      </div>
    </div>
  );
}

export default VoiceControl;
