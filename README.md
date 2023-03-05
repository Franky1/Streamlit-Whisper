# Streamlit Openai Whisper 🗣️

[![Streamlit](https://img.shields.io/badge/Go%20To-Streamlit%20Cloud-red?logo=streamlit)](https://franky1-whisper-streamlit-app-ode4s8.streamlit.app/)

Streamlit demo project for Openai Whisper.

## Status ✔️

> Streamlit App works - Has some issues - Last changed: 2023-03-04

## Issues 🚩

- Dependencies of `whisper` are very heavy (pytorch, transformers, cuda...) and take a long time to install.
- Model is not pre-downloaded and very huge, so it takes a long time to download the first time.
- Larger models above the `small` model seems to crash on streamlit cloud, probably due to memory limits.
- The largest model that seems to run locally and on streamlit cloud is `small`.
- Usage of Git-LFS for pre-downloaded model also does not make sense, because at least in the free version of GitHub, you only get 1GB of storage space and 1GB of bandwidth per month.
- Transcribe takes a long time to run.
- The audiorecorder component is not working.

## ToDo ☑️

- [x] Test app locally with docker
- [x] Test app locally within virtual environment
- [x] Use temporary directory for uploaded file
- [x] Try deployment on streamlit cloud
- [x] Try larger models
- [x] Add custom audio recording component to streamlit app
- [ ] Fix and test audiorecorder issue
- [ ] Try other audio recording components
- [ ] Improve layout of the frontend
- [ ] Restructure file structure

## Resources 📚

- Streamlit ❤️
  - <https://docs.streamlit.io/>
- Openai Whisper ❤️
  - <https://github.com/openai/whisper>
- Streamlit Custom Components for Audio Recording
  - streamlit-webrtc 🤷‍♂️
    - <https://github.com/whitphx/streamlit-webrtc>
    - <https://github.com/whitphx/streamlit-stt-app>
  - streamlit-audiorecorder 🤷‍♂️
    - <https://github.com/theevann/streamlit-audiorecorder>
  - audio-recorder-streamlit 🤷‍♂️
    - <https://github.com/Joooohan/audio-recorder-streamlit>
  - streamlit_audio_recorder 🤔
    - <https://github.com/stefanrmmr/streamlit_audio_recorder>
