# Chat with Youtube Videos

<img width="1437" alt="Screenshot 2023-08-15 at 5 57 44 PM" src="https://github.com/ta-sakin/yt-chat/assets/47474230/a5587c90-9839-4054-8a7d-6f9a32fe74af">

## What is this?

This is a Streamlit chatbot app that allows you to chat with any youtube videos using Openai's Chat API model. It uses **text-embedding-ada-002** model to generate embeddings and **FAISS** as vector database.

## Usage

- Add your [Openai API key](https://platform.openai.com/account/api-keys) in the sidebar. **Your API key won't be stored in the database.**
- You can choose a model from the dropdown in the sidebar.
- Add a youtube video link in the top right input field.
- Type your question in the input field at the bottom of the app.

Live demo: [YT-Chat](https://yt-chat.streamlit.app/)

## Run on your machine.

Clone the repo

```console
git clone https://github.com/ta-sakin/yt-chat.git

```

Install dependencies

```console
pip install -r requirements.txt
```

Configure your [Openai API key](https://platform.openai.com/account/api-keys).

Run the app

```console
streamlit run app.py
```
