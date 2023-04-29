import json
import pickle
import typing
from datetime import datetime

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.faiss import FAISS

JSON = typing.Dict[str, typing.Any]


def read_json(path: str) -> typing.List[JSON]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def merge_consecutive_messages(messages: typing.List[JSON]) -> JSON:
    result = {}
    for message in messages:
        # discard old messages
        if (
            datetime.fromisoformat(message["date"]).date()
            < datetime.fromisoformat("2022-02-24").date()
        ):
            continue
        speech_id = message["speech_id"]
        if speech_id not in result:
            result[speech_id] = {
                "speech_id": speech_id,
                "message_id": str(message["message_id"]),
                "author_id": message["author_id"],
                "date": message["date"],
                "text": message["text"],
            }
        else:
            result[speech_id]["message_id"] += f" - {str(message['message_id'])}"
            result[speech_id]["date"] = message["date"]
            result[speech_id]["text"] += f" {message['text']}"
    return result


def load_documents(path: str) -> typing.List[Document]:
    data = read_json(path)
    merged = merge_consecutive_messages(data)
    return [
        Document(
            page_content=message["text"],
            metadata={k: v for k, v in message.items() if k != "text"},
        )
        for message in merged.values()
    ]


def main() -> int:
    raw_documents = load_documents("./processed.json")
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(raw_documents)

    # multilingual
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    vectorstore = FAISS.from_documents(documents, embeddings)

    with open("./vectorstore.pkl", "wb") as f:
        pickle.dump(vectorstore, f)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
