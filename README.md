# Ask-Your-Chat

This repository contains a fork of the original Chat-Your-Data app and has been modified to work with Telegram exported chats. 

With this modification, you can now feed messages from your Telegram chats to LLM (Language Model) to get relevant answers.

*Original README below:*

---

# Chat-Your-Data

Create a ChatGPT like experience over your custom docs using [LangChain](https://github.com/hwchase17/langchain).

See [this blog post](https://blog.langchain.dev/tutorial-chatgpt-over-your-data/) for a more detailed explanation.

## Ingest data

Ingestion of data is done over the `state_of_the_union.txt` file. 
Therefor, the only thing that is needed is to be done to ingest data is run `python ingest_data.py`

## Query data
Custom prompts are used to ground the answers in the state of the union text file.

## Running the Application

By running `python app.py` from the command line you can easily interact with your ChatGPT over your own data.
