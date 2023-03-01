from pathlib import Path
import streamlit as st
import whisper


@st.cache_resource(show_spinner=False)
def load_model(name: str):
    model = whisper.load_model(name)
    return model


@st.cache_data(show_spinner=False)
def transcribe(_model, audio_file):
    transcription = _model.transcribe(audio_file, fp16=False)
    return transcription["text"]


header = st.container()
explain = st.container()

with header:
    st.title("Convert Speech to Text")
    # st.write("Note: This Model can only transcribe from English speech to English text")
    st.markdown('''
                1. Upload Audio File
                2. Wait until `Transcribe Audio` button appears
                3. Click on `Transcribe Audio` button and wait until result generated
                4. You can download the result in .txt format
                ''')

with st.spinner("Loading Model for the first time, please wait..."):
    model = load_model(name="small")

with explain:
    audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a", "ogg"])
    # FIXME: Write to temp file instead of root folder
    if audio_file is not None:
        audio_file_path = Path(audio_file.name)
        with open(audio_file.name, "wb") as f:
            f.write(audio_file.getvalue())

    if st.sidebar.button("Transcribe Audio"):
        if audio_file is not None:
            st.sidebar.success("Transcribing Audio")
            with st.spinner("Running Transcribe, please wait..."):
                transcription = transcribe(model, audio_file_path.name)
            st.sidebar.success("Transcription Complete")
            st.markdown(transcription)
            st.download_button(label='Download Text',
                        data=transcription,
                        file_name=audio_file_path.with_suffix(".txt").name)
        else:
            st.sidebar.error("Please Upload an Audio File")

    st.sidebar.header("Play Original Audio File")
    st.sidebar.audio(audio_file)
