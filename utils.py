from pytube import YouTube
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import pickle
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.llms import OpenAI
import os
from prompt_template import DEFAULT_PROMPT


def get_video_id(url):
    try:
        yt = YouTube(url)
        return yt.video_id
    except Exception as e:
        print(f"Error: {e}")
        return None
# get transcript of the video


def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        if len(transcript) == 0:
            return None
        transcript_text = ""
        for entry in transcript:
            start_time = entry['start']
            minutes = int(start_time // 60)
            seconds = int(start_time % 60)
            formatted_time = f"{minutes:2d}:{seconds:02d}"
            text = entry['text']
            transcript_text += f"{formatted_time}: {text}\n"
        return transcript_text
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_embeddings(transcript, openai_api_key, video_id):
    try:
        if os.path.exists(f"{video_id}.pkl"):
            with open(f"{video_id}.pkl", "rb") as f:
                vectorstore = pickle.load(f)
        else:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=2048,
                chunk_overlap=20,
            )
            texts = text_splitter.split_text(transcript)
            vectorstore = FAISS.from_texts(
                texts,
                OpenAIEmbeddings(openai_api_key=openai_api_key),
                metadatas=[{"source": i} for i in range(len(texts))],
            )
            with open(f"{video_id}.pkl", "wb") as f:
                pickle.dump(vectorstore, f)
        return vectorstore
    except Exception as e:
        print(f"Error getting embeddings: {e}")


def get_answer(query, vectorstore, openai_api_key, transcript, model="gpt-3.5-turbo"):
    try:
        if not vectorstore:
            raise Exception("Failed to generate embeddings")
        texts = vectorstore.similarity_search(query)
        llm = OpenAI(temperature=0, model_name=model,
                     openai_api_key=openai_api_key)
        doc_chain = load_qa_with_sources_chain(
            llm=llm,
            chain_type="stuff",
            prompt=DEFAULT_PROMPT,
        )
        answer = doc_chain(
            {"input_documents": texts, "question": query}, return_only_outputs=True
        )
        return answer
    except Exception as e:
        print(f"Error generating response: {e}")
        return {"error": str(e)}

        # return None
