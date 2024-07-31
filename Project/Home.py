import streamlit as st
from openai import OpenAI
from pathlib import Path
import time
import utils


PASTA_ARQUIVOS = Path(__file__).parent

#python -m streamlit run Home.py  --server.enableXsrfProtection false

def sidebar():
    for arquivo in PASTA_ARQUIVOS.glob("*.xlsx"):
        arquivo.unlink()

    csv_file = st.file_uploader("Upload your xlsx files here", type=".xlsx")
    file_path = None
    if csv_file is not None:
        file_path = PASTA_ARQUIVOS / csv_file.name
        with open(file_path, "wb") as f:
            f.write(csv_file.getbuffer())

    label_button = "Iniciar Chatbot"
    if 'chain' in st.session_state:
        label_button = "Atualizar Chatbot"
        
    if st.button(label_button, use_container_width=True):
        if len(list(PASTA_ARQUIVOS.glob("*.xlsx"))) == 0:
            st.error("Nenhum arquivo foi carregado.")
        else:
            st.success("Inicializando Chatbot...")
            time.sleep(2)
            st.session_state.chain = True
            st.session_state.chat_history = []
            st.session_state.thread_id = None
            st.rerun()
    return file_path

def chat_window(file_path):
    
    st.header("Chatbot", divider=True)

    if not 'chain' in st.session_state:
        st.error("Faça o upload de um arquivo para começar.")
        st.stop()

    #chain = st.session_state['chain']

    container = st.container()
    new_message = st.chat_input("Digite uma mensagem")

    for msg in st.session_state.chat_history:
        chat = container.chat_message(msg["role"])
        chat.markdown(msg["content"])

    if new_message:
        st.session_state.chat_history.append({"role": "user", "content": new_message})
        chat = container.chat_message('human')
        chat.markdown(new_message)

        chat = container.chat_message('ai')
        chat.markdown('Gerando resposta...')
        response, thread_id = utils.create_assistant(file_path, new_message, st.session_state.get("thread_id"))
        st.session_state.thread_id = thread_id
        st.session_state.chat_history.append({"role": "ai", "content": response})
        chat.markdown(response)
        st.rerun()

def main():
    with st.sidebar:
        file_path = sidebar()
    chat_window(file_path)

if __name__ == "__main__":
    main()
