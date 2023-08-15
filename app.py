import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import openai
from openai.error import OpenAIError
from utils import (get_video_id, get_video_transcript,
                   get_embeddings, get_answer)
load_dotenv()
icon = Image.open("favicon.ico")
st.set_page_config(page_title="YT-Chat - Chat with Youtube",
                   page_icon=icon, layout="centered", menu_items=None)

# Add custom CSS to hide the GitHub icon
st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True
)

centered_style = (
    "text-align: center;"
    "margin-top: -50px;"
)
# Create a centered header using Markdown
st.markdown(
    f'<h4 style="{centered_style}">Chat with Youtube Videos</h4>',
    unsafe_allow_html=True
)


def main():
    try:
        openai_api_key = st.sidebar.text_input(
            "OpenAI API Key", key="file_qa_api_key", type="password", placeholder="***************"
        )
        if not openai_api_key:
            st.sidebar.warning(
                "Please enter your [OpenAI API Key](https://platform.openai.com/account/api-keys) to continue. We'll not store your API key.")
        elif openai_api_key and "sk" not in openai_api_key:
            st.sidebar.warning("Please enter a valid OpenAI API Key")
            openai_api_key = None
        else:
            openai.api_key = openai_api_key
            try:
                model_list = openai.Model.list()
                models = [
                    model['id'] for model in model_list['data']]
                default_model = "gpt-3.5-turbo"
                selected_model = st.sidebar.selectbox(
                    "Choose a openai model", models, index=models.index(default_model))
            except OpenAIError as e:
                st.error(e._message)
                openai_api_key = None

        if "url" not in st.session_state.keys():
            st.session_state.url = False
        if "embeddings" not in st.session_state.keys():
            st.session_state.embeddings = False

        def clear_chat():
            st.session_state.messages = [
                {"role": "assistant", "content": "How can I assist you with this video?"}]

        def url_change():
            st.session_state.url = False
            st.session_state.embeddings = False
            clear_chat()
        # get youtube video url
        url = st.text_input(
            "Enter a youtube video url", placeholder="https://www.youtube.com/watch?v=WnzlbyTZsQY", disabled=not openai_api_key, on_change=url_change)
        if url and not st.session_state.url:
            with st.spinner("Processing..."):
                # check for valid url
                if len(url) < 28 or "youtu" not in url.lower():
                    st.warning("Please enter a valid youtube url", icon='⚠️')
                    return
                video_id = get_video_id(url)
                if not video_id:
                    st.warning("Please enter a valid youtube url", icon='⚠️')
                    return

                transcript = get_video_transcript(video_id)
                if "url" in st.session_state.keys() and not st.session_state.url:
                    st.session_state.url = True
                if not transcript:
                    st.warning("Please enter a valid youtube url", icon='⚠️')
                    return
                if not st.session_state.embeddings:
                    # Store embeddings
                    vector_store = get_embeddings(
                        transcript, openai_api_key, video_id)
                    if "embeddings" in st.session_state.keys():
                        st.session_state.embeddings = vector_store

        if url and st.session_state.url:
            if "messages" not in st.session_state.keys():
                st.session_state.messages = [
                    {"role": "assistant", "content": "How can I assist you with this video?"}]

            # Display or clear chat messages
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

            st.sidebar.button("Clear Chat", on_click=clear_chat)

            # User-provided prompt
            if prompt := st.chat_input(placeholder="What's this video about?", disabled=not openai_api_key and not transcript):
                st.session_state.messages.append(
                    {"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.write(prompt)

            vectorstore = st.session_state.embeddings
            if st.session_state.messages[-1]["role"] != "assistant":
                with st.chat_message("assistant"):
                    with st.spinner("Generating response..."):
                        model_response = get_answer(
                            prompt,
                            vectorstore,
                            openai_api_key,
                            transcript='',
                            model=selected_model
                        )
                        if "error" in model_response.keys():
                            st.warning(
                                model_response["error"])
                            return
                        response = model_response["output_text"]
                        placeholder = st.empty()
                        full_response = ''
                        for item in response:
                            full_response += item
                            placeholder.markdown(full_response)
                        placeholder.markdown(full_response)
                message = {"role": "assistant", "content": full_response}
                st.session_state.messages.append(message)

    except Exception as e:
        # st.exception(e)
        print(e)


if __name__ == "__main__":
    main()
