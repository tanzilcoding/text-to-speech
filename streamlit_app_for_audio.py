import os
import sys
import uuid
import base64
import traceback
import streamlit as st
from streamlit_chat import message
# Import the required module for text
# to speech conversion
# Run this command not in "venv" but in global: pip3.11 install gTTS
# Run this command not in "venv" but in global: pip3.11 install playsound
from gtts import gTTS

try:
    # Setting page title and header
    st.set_page_config(
        page_title="Text to Speech", page_icon=":robot_face:")
    st.markdown("<h1 style='text-align: center;'>Text to Speech</h1>",
                unsafe_allow_html=True)

    # Initialise session state variables
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
    if 'audio_file_name' not in st.session_state:
        st.session_state['audio_file_name'] = []
    if 'audio_file_path' not in st.session_state:
        st.session_state['audio_file_path'] = []

    def autoplay_audio(file_path: str):
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio controls autoplay="true">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(
                md,
                unsafe_allow_html=True,
            )

    # generate a response
    def generate_response(prompt):
        st.session_state['messages'].append(
            {"role": "user", "content": prompt})

        # Language in which you want to convert
        language = 'en'

        # Passing the text and language to the engine,
        # here we have marked slow=False. Which tells
        # the module that the converted audio should
        # have a high speed
        myobj = gTTS(text=prompt, lang=language, slow=False)

        # Saving the converted audio in a mp3 file named
        # welcome
        audio_file_name = f'audio-{uuid.uuid4().hex}.mp3'
        # audio_file_name = f'audio.mp3'
        cwd = os.getcwd()
        audio_file_path = f'{cwd}/{audio_file_name}'
        myobj.save(audio_file_name)

        return audio_file_name, audio_file_path

    # container for chat history
    response_container = st.container()
    # container for text box
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_area("You:", key='input', height=100)
            submit_button = st.form_submit_button(label='Convert to speech')

        if submit_button and user_input:
            audio_file_name, audio_file_path = generate_response(
                user_input)
            st.session_state['past'].append(user_input)
            st.session_state['audio_file_name'].append(audio_file_name)
            st.session_state['audio_file_path'].append(audio_file_path)

    if st.session_state['past']:
        with response_container:
            for i in range(len(st.session_state['past'])):
                message(st.session_state["past"][i],
                        is_user=True, key=str(i) + '_user')
                # message(st.session_state["generated"][i], key=str(i))
                audio_file_name = st.session_state["audio_file_name"][i]
                audio_file_path = st.session_state["audio_file_path"][i]

                if os.path.isfile(audio_file_path):
                    st.info(f'Audio file name: {audio_file_name}')
                    # st.info(f'Audio file path: {audio_file_path}')

                    # Playing the converted file
                    # os.system(f"mpg321 {audio_file_name}.mp3")
                    # play the audio file
                    # playsound(audio_file_name)
                    # playsound(audio_file_path)
                    # audio = AudioSegment.from_mp3(audio_file_name)
                    # play(audio)
                    autoplay_audio(audio_file_path)

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
