from gtts import gTTS
import os
import uuid

def text_to_speech(text):
    if not text:
        return None

    filename = f"audio_{uuid.uuid4()}.mp3"
    filepath = os.path.join("uploads", filename)

    tts = gTTS(text)
    tts.save(filepath)

    return filepath