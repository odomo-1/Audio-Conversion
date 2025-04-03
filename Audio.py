import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import which
import os

# Set FFmpeg path for pydub
AudioSegment.converter = which("ffmpeg")

# Streamlit app title
st.title("Audio Transcription App")

# File uploader for audio files
uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "ogg"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    temp_audio_path = "temp_audio_file"
    wav_audio_path = None  # Initialize wav_audio_path to None
    try:
        with open(temp_audio_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.info(f"Temporary file saved at: {temp_audio_path}")

        # Check if the file exists
        if not os.path.exists(temp_audio_path):
            st.error("Temporary file not found. Please try uploading the file again.")
        else:
            # Convert audio to WAV format if necessary
            audio_format = uploaded_file.name.split('.')[-1]
            try:
                if audio_format != "wav":
                    st.info("Converting audio to WAV format...")
                    audio = AudioSegment.from_file(temp_audio_path, format=audio_format)
                    wav_audio_path = "temp_audio_file.wav"
                    audio.export(wav_audio_path, format="wav")
                    audio_path = wav_audio_path
                    st.success("Audio converted to WAV format successfully.")
                else:
                    audio_path = temp_audio_path

                # Play the uploaded audio file
                st.audio(audio_path, format="audio/wav")

                # Transcribe the audio
                recognizer = sr.Recognizer()
                try:
                    with sr.AudioFile(audio_path) as source:
                        audio_data = recognizer.record(source)
                        transcription = recognizer.recognize_google(audio_data)
                        st.subheader("Transcription:")
                        st.write(transcription)
                except sr.UnknownValueError:
                    st.error("Could not understand the audio.")
                except sr.RequestError as e:
                    st.error(f"Error with the transcription service: {e}")
                except Exception as e:
                    st.error(f"An unexpected error occurred during transcription: {e}")
            except Exception as e:
                st.error(f"An error occurred while converting the audio file: {e}")
    except Exception as e:
        st.error(f"An error occurred while saving the audio file: {e}")

    # Clean up temporary files
    if os.path.exists(temp_audio_path):
        os.remove(temp_audio_path)
    if wav_audio_path and os.path.exists(wav_audio_path):  # Check if wav_audio_path is defined
        os.remove(wav_audio_path)