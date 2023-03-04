# Streamlit Openai Whisper

[![Streamlit](https://img.shields.io/badge/Go%20To-Streamlit%20Cloud-red?logo=streamlit)](https://franky1-whisper-streamlit-app-ode4s8.streamlit.app/)

Streamlit demo project for openai whisper.

## Status

> Work in progress - Not finished - Last changed: 2023-03-03

## Issues

- Dependencies are very heavy (whisper, pytorch, transformers, etc.) and take a long time to install.
- Model is not pre-downloaded and very huge, so it takes a long time to download the first time.
- Larger models seems to crash on streamlit cloud, probably due to memory limits.
- The largest model that seems to run locally and on streamlit cloud is `small`.
- Transcribe takes a long time to run.

## ToDo

- [x] Test app locally with docker
- [x] Use temporary directory for uploaded file
- [x] Try deployment on streamlit cloud
- [x] Try larger models
- [ ] Add audio recording to app
- [ ] Try pre-download of model(?)
- [ ] Use Git-LFS for model(?)
- [ ] Improve layout of the frontend

## Resources

- <https://github.com/openai/whisper>
