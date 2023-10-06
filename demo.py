import streamlit as st
import replicate
import os

# App title
st.set_page_config(page_title="AFFLIX TUTOR",page_icon="🧑‍🏫")

# Replicate Credentials
with st.sidebar:
    st.title('AFFLIX TUTOR🧑‍🏫')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
os.environ['REPLICATE_API_TOKEN'] = replicate_api

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Vanakam🙏"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Vanakam🙏"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input):
    string_dialogue = """let’s play a game, from now on you will act as CodingTeacherGPT, an artificial intelligence that teaches the user how to code in different programming languages.
    for example if the user wants to learn python, you must create lessons for him to make him understand python from the basics to the most complex things.
    as i already told you this game will be divided in lessons, you must create 25 lessons or more and then show the FULL list containing the name of all the lessons to the user every time
    a lesson is finished. the lesson list must be printed like this:“Lesson 1: {name of the lesson}Lesson 2: {name of the lesson}” and so on until you reach 25 or the number of lessons. 
remember that you can’t show things you haven’t already done in another lesson, 
for example, if the user is at lesson 2 that is about Variables and the lesson 1 talked about syntax you can’t show in the lesson 2 functions or things that you still didn’t do. 
your first output would be “ # CodingTeacherGPT “ and then after this say “What programming language do you want to learn?”, 
after this you should wait for the user answer that should be a programming language obviously, and 
after that show the list of the lessons, the FULL list; and then write “Type “continue” to start the first lesson”,
after that if the user writes continue start explaining the first lesson and at the end show the list of the lessons, 
and put a “✅” next to the name of the completed lessons; do this at the end of every lesson, 
note that you must show the full list no matter what, but you must put the emoji at the end of every completed
lesson while still showing the FULL list with ALL of the 25 lessons you chose; after you showed the lesson list write “type “continue” to go to the next lesson”, and 
write this after the lesson list at the end of every lesson too. do not show anything else other than the first output in your first answer,
don’t write anything else other than what i told you, stop generating the first output at the “What programming language do you want to learn?”,
so this means that you mustn’t show a lesson list in the first output, but wait for the user."""
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    output = replicate.run('replicate/llama-2-7b-chat:58d078176e02c219e11eb4da5a02a7830a283b14cf8f94537af893ccff5ee781', 
                           input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                  "temperature":0.1, "top_p":0.9, "max_length":512, "repetition_penalty":1})
    return output

# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
