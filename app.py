import subprocess
from datetime import datetime
from tempfile import NamedTemporaryFile

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


def init_session_state() -> None:
    if 'assistant_history' not in st.session_state:
        st.session_state['assistant_history'] = []


def btn_on_click_callback() -> None:
    _instruction = st.session_state['instruction']
    user_instruction = f'Hello you just submitted command:\n{_instruction}'
    st.session_state['assistant_history'].append(user_instruction)


def get_file_location_from_name(filename: str) -> str:
    return '\\'.join(filename.split('\\')[:-1])


def load_mysql_dump_file(input_file: UploadedFile) -> None:
    with NamedTemporaryFile(mode='w') as f:
        f.write(input_file.read().decode('utf-8'))
        input_file.seek(0)
        print(input_file.read().decode('utf-8'))
        cmd_result = subprocess.Popen([
            'docker',
            'exec', '-i', 'mysql_server', 'mysql',
            '-uroot', '-proot', '<sql_code/query.sql'
        ],
            shell=True,
            stdout=subprocess.PIPE,
            encoding='utf-8'
        )
        if cmd_result.returncode is None:
            output = cmd_result.stdout.read()
            for line in output.split('\n'):
                st.write(line)
            print(f'mysql --dump={f.name}')
        else:
            st.write('Error loading dump_file')


def save_credentials_into_file(cred_file: UploadedFile) -> str:
    dt_now = str(datetime.now()) \
        .replace(':', '_') \
        .replace(' ', '_')
    filename = f'creds/creds_{dt_now}.txt'
    with open(filename, mode='w') as f:
        f.write(cred_file.getvalue().decode('utf-8'))
    return filename


def main() -> None:
    init_session_state()

    st.title('Instruction2SQL tool')
    st.text('Drop your MySQL dump file and enter search instruction to LLM')
    # SIDEBAR TEXT
    st.sidebar.text_area(
        label='Input instruction text here',
        max_chars=350,
        key='instruction'
    )
    # SUBMIT BUTTON
    st.sidebar.button(
        'Submit instruction',
        type='primary',
        on_click=btn_on_click_callback
    )

    # LOAD FILE
    dump_file = st.file_uploader(
        label='Upload your file.dump.mysql',
        type=['.txt'],
        accept_multiple_files=False
    )

    chat_placeholder = st.container()

    with chat_placeholder:
        for message in st.session_state['assistant_history']:
            st.chat_message("assistant").write(message)

    # if btn_result and dump_file is not None:
    #     load_mysql_dump_file(dump_file)
    #     output_chat.write(f'Hello you just submitted command:\n{instruction}')


if __name__ == '__main__':
    main()
