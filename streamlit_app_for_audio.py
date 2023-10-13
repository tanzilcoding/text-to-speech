import os
import sys
import uuid
import traceback
import streamlit as st
from playsound import playsound

# Import the required module for text
# to speech conversion
# Run this command not in "venv" but in global: pip3.11 install gTTS
# Run this command not in "venv" but in global: pip3.11 install playsound
from gtts import gTTS

from pydub import AudioSegment
from pydub.playback import play

try:
    import environment_variables
except ImportError:
    pass

try:
    # Setting page title and header
    demo_number = 1
    st.set_page_config(
        page_title="Text to Speech", page_icon=":robot_face:")
    st.markdown("<h1 style='text-align: center;'>Text to Speech</h1>",
                unsafe_allow_html=True)

    with st.container():
        text_for_speech = st.text_area(
            "Text to convert",
            "",
        )
        button = st.button("Convert to speech", type="primary")
        if button:
            if len(text_for_speech) < 1:
                st.error("Please type some text and then try again.")
            else:
                # st.info(text_for_speech)
                # Language in which you want to convert
                language = 'en'

                # Passing the text and language to the engine,
                # here we have marked slow=False. Which tells
                # the module that the converted audio should
                # have a high speed
                myobj = gTTS(text=text_for_speech, lang=language, slow=False)

                # Saving the converted audio in a mp3 file named
                # welcome
                audio_file_name = f'audio-{uuid.uuid4().hex}.mp3'
                # audio_file_name = f'audio.mp3'
                cwd = os.getcwd()
                # audio_file_path = f'{cwd}/{audio_file_name}'
                myobj.save(audio_file_name)
                if os.path.isfile(audio_file_name):
                    st.info(f'Audio file name: {audio_file_name}')
                    # st.info(f'Audio file path: {audio_file_path}')

                    # Playing the converted file
                    # os.system(f"mpg321 {audio_file_name}.mp3")
                    # play the audio file
                    playsound(audio_file_name)
                    # playsound(audio_file_path)
                    # song = AudioSegment.from_mp3(audio_file_name)
                    # play(song)

                    with open(audio_file_name, 'rb') as f:
                        if st.download_button('Download Audio Speech File', f, file_name=audio_file_name):
                            st.success('Thanks for downloading!')

                    st.success(
                        "An audio file is generated. Please play it to test its quality.")
                else:
                    st.error(f'Audio path {audio_file_name} does not exist.')
except Exception as e:
    error_message = ''
    # st.text('Hello World')
    st.error('An error has occurred. Please try again.', icon="🚨")
    # Just print(e) is cleaner and more likely what you want,
    # but if you insist on printing message specifically whenever possible...
    if hasattr(e, 'message'):
        error_message = e.message
    else:
        error_message = e
    st.error('ERROR MESSAGE: {}'.format(error_message), icon="🚨")
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    st.error(f'Error Type: {exc_type}', icon="🚨")
    st.error(f'File Name: {fname}', icon="🚨")
    st.error(f'Line Number: {exc_tb.tb_lineno}', icon="🚨")
    st.error(traceback.format_exc())
