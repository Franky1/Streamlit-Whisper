import re
import shutil
import tempfile
import uuid
from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path

import streamlit as st
import whisper
from audiorecorder import audiorecorder


st.set_page_config(page_title='Openai Whisper Transcriber',
                page_icon='📜',
                layout="wide",
                initial_sidebar_state="expanded")


# apply custom css
with open(Path('utils/style.css')) as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)


@st.cache_resource(ttl=60*60*24, show_spinner=False)
def cleanup_tempdir() -> None:
    '''Cleanup temp dir for all user sessions.
    Filters the temp dir for uuid4 subdirs.
    Deletes them if they exist and are older than 1 day.
    '''
    deleteTime = datetime.now() - timedelta(days=1)
    uuid4_regex = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    uuid4_regex = re.compile(uuid4_regex)
    tempfiledir = Path(tempfile.gettempdir())
    if tempfiledir.exists():
        subdirs = [x for x in tempfiledir.iterdir() if x.is_dir()]
        subdirs_match = [x for x in subdirs if uuid4_regex.match(x.name)]
        for subdir in subdirs_match:
            itemTime = datetime.fromtimestamp(subdir.stat().st_mtime)
            if itemTime < deleteTime:
                shutil.rmtree(subdir)


def get_all_uuid4_subdirs_from_tempdir() -> None:
    '''Get all uuid4 subdirs from temp dir for all user sessions.'''
    uuid4_regex = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    uuid4_regex = re.compile(uuid4_regex)
    tempfiledir = Path(tempfile.gettempdir())
    if tempfiledir.exists():
        subdirs = [x for x in tempfiledir.iterdir() if x.is_dir()]
        subdirs_match = [x for x in subdirs if uuid4_regex.match(x.name)]
        subdirs_match = [str(x) for x in subdirs_match]
        return subdirs_match
    else:
        return None


@st.cache_data(show_spinner=False)
def make_tempdir() -> Path:
    '''Make temp dir for each user session and return path to it
    returns: Path to temp dir
    '''
    if 'tempfiledir' not in st.session_state:
        tempfiledir = Path(tempfile.gettempdir())
        tempfiledir = tempfiledir.joinpath(f"{uuid.uuid4()}")   # make unique subdir
        tempfiledir.mkdir(parents=True, exist_ok=True)  # make dir if not exists
        st.session_state['tempfiledir'] = tempfiledir
    return st.session_state['tempfiledir']


def store_file_in_tempdir(tmpdirname: Path, uploaded_file: BytesIO) -> Path:
    '''Store file in temp dir and return path to it
    params: tmpdirname: Path to temp dir
            uploaded_file: BytesIO object
    returns: Path to stored file
    '''
    # store file in temp dir
    tmpfile = tmpdirname.joinpath(uploaded_file.name)
    with open(tmpfile, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    return tmpfile


def write_file_in_tempdir(tmpdirname: Path, uploaded_file: bytearray, filename: str) -> Path:
    '''Write file in temp dir and return path to it
    params: tmpdirname: Path to temp dir
            uploaded_file: bytearray
            filename: str
    returns: Path to stored file
    '''
    # store file in temp dir
    tmpfile = tmpdirname.joinpath(filename)
    with open(tmpfile, 'wb') as f:
        f.write(uploaded_file)
    return tmpfile


@st.cache_resource(show_spinner=False)
def load_model(name: str):
    model = whisper.load_model(name)
    return model


@st.cache_data(show_spinner=False)
def transcribe(_model, audio_file):
    transcription = _model.transcribe(audio_file, fp16=False)
    return transcription["text"]


if __name__ == "__main__":
    cleanup_tempdir()  # cleanup temp dir from previous user sessions
    tmpdirname = make_tempdir()  # make temp dir for each user session

    lcol, ccol, rcol = st.columns([1, 4, 1], gap="small")
    with ccol:
        st.title("Convert Speech to Text 🗣️ ➡️ 📜")
        # st.write("Note: This Model can only transcribe from English speech to English text")
        # st.info(tmpdirname)
        # st.table(get_all_uuid4_subdirs_from_tempdir())

    with st.sidebar:
        st.image('resources/openai2.png')
        st.header("About")
        st.markdown('''
                            This transcriber uses Openai's Whisper Model:
                            - <https://github.com/openai/whisper>

                            Github Project:
                            - <https://github.com/Franky1/whisper>
                            ''')
        st.markdown('''---''')
        st.header("How to use this app 👈")
        st.markdown('''
                    1. Upload Audio File or Record Audio
                    2. Click on "**Transcribe Audio**" button and wait until result generated
                    3. Result can be downloaded in .txt format
                    ''')
        st.markdown('''---''')

    with ccol:
        with st.spinner("Loading Openai Model for the first time, please wait..."):
            model = load_model(name="small")

        col1, col2 = st.columns([5, 3], gap="large")
        with col1:
            st.subheader("Upload Audio File 🎵")
            audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a", "ogg"], label_visibility="collapsed")
        with col2:
            st.subheader("Record Audio 🎤")
            audio = audiorecorder("Click to record", "Recording...")

        if audio_file is not None:
            tmpfile = store_file_in_tempdir(tmpdirname, audio_file)
            audio_file_path = Path(audio_file.name)
        elif len(audio) > 0:
            audio_file_bytes = audio.tobytes()
            tmpfile = write_file_in_tempdir(tmpdirname, audio_file_bytes, filename="audio.mp3")
            audio_file_path = Path("audio.mp3")
        else:
            st.sidebar.warning("Please Upload an Audio File")
            st.stop()

        st.sidebar.header("Play Original Audio File 🔊")
        st.sidebar.audio(audio_file)
        if st.sidebar.button("Transcribe Audio ✍️"):
            st.sidebar.info("Transcribing Audio...")
            with st.spinner("Running Transcribe, please wait..."):
                transcription = transcribe(model, str(tmpfile.resolve()))
            st.sidebar.success("Transcription Complete")
            st.subheader("Transcription Result ✍️")
            st.success(audio_file.name)
            st.markdown(transcription)
            st.download_button(label='Download Text File ',
                        data=transcription,
                        file_name=audio_file_path.with_suffix(".txt").name)
