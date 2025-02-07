import streamlit as st
import tempfile
import whisper
from pydub import AudioSegment
def run():
    st.title("🎙️ Speech to Text Converter")
    st.subheader("Extracting the text in the audio file:")

    uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])

    if uploaded_file:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(uploaded_file.read())
            audio_path = temp_audio.name
        
        st.audio(audio_path)

        # Convert MP3 to WAV
        if uploaded_file.name.endswith(".mp3"):
            audio = AudioSegment.from_mp3(audio_path)
            audio.export(audio_path, format="wav")

        st.info("Transcribing... Please wait.")

        # Load Whisper model and transcribe
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        
        st.subheader("📝 Transcription")
        st.write(result["text"])

        # Download transcription
        st.download_button("Download as TXT", result["text"], file_name="transcription.txt", mime="text/plain")
        
        st.success("✅ Done!")

if __name__=="__main__":
    run()