# Streamlit Openai Whisper

[![Streamlit](https://img.shields.io/badge/Go%20To-Streamlit%20Cloud-red?logo=streamlit)](https://streamlit.io/)

Streamlit demo project for openai whisper.

## Status

> Work in progress - Not finished - Last changed: 2023-03-01

## Issues

- Dependencies are very heavy (whisper, pytorch, transformers, etc.) and take a long time to install.
- Model is not pre-downloaded and very huge, so it takes a long time to download the first time.
- Transcribe takes a long time to run.
- Uploaded file is stored in root directory, so it is not deleted after the app is closed.

## ToDo

- [x] Test app locally with docker
- [ ] Use temporary directory for uploaded file
- [ ] Add audio recording to app
- [ ] Test pre-download of model
- [ ] Use Git-LFS for model(?)
- [ ] Try deployment on streamlit cloud
- [ ] Improve layout of the frontend

## Resources

- <https://github.com/openai/whisper>
