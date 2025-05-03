import ollama
import streamlit as st
from db import models, get_description


st.sidebar.title(':blue[Local Llama]')

try:
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    if 'model' not in st.session_state:
        st.session_state['model'] = ''

    local_models = sorted([ollama.list()['models'][i]['model'] for i in range(len(ollama.list()['models']))])
    st.session_state['model'] = st.sidebar.selectbox('Locals list', options=local_models, index=None, placeholder='', 
                                                    help='Choose an installed model from the list. If avaliable, below will show the description.')

    def responses():
        stream = ollama.chat(
            model=st.session_state['model'],
            messages=st.session_state['messages'],
            stream=True)

        for chunk in stream:
            yield chunk['message']['content']

    def conversation():
        for message in st.session_state['messages']:
            with st.chat_message(message['role']):
                st.write(message['content'])

        if prompt := st.chat_input('Type here...'):
            st.session_state['messages'].append({'role': 'user', 'content': prompt})

            with st.chat_message('user'):
                st.write(prompt)
            
            with st.chat_message('assistant'):
                message = st.write_stream(responses())
                st.session_state['messages'].append({'role': 'assistant', 'content': message})

    if not st.session_state['model']:
        models.clear()

    elif st.session_state['model'] not in models:
        models.clear()
        models.add(st.session_state['model'])
        st.sidebar.write(get_description(st.session_state['model']))
        st.session_state['messages'] = []
        conversation()  

    else:
        st.sidebar.write(get_description(st.session_state['model']))
        conversation()

except ConnectionError:
    st.header('Ollama Connection Error!')
    st.write('You can run the desktop application from your computer or `ollama serve` command can be used when you want to start ollama without running the desktop application.')