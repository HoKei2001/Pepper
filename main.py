import openai
import os
from dotenv import load_dotenv, find_dotenv  # env API key
from PyPDF2 import PdfReader
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.text_splitter import CharacterTextSplitter

_ = load_dotenv(find_dotenv())
openai.api_key = os.environ['OPENAI_API_KEY']

# @tool
# def title(text:str)->str:
#

llm = ChatOpenAI(temperature=0)  # parameter settings


def pdf2text(file_path):  # pdf to txt
    reader = PdfReader(file_path)
    txt_file_path = 'files/raw.txt'
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            with open(txt_file_path, 'a', encoding='utf-8') as txt_file:
                txt_file.write(text)
    return txt_file_path


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]


with open('files/paper2.mmd', 'r', encoding='utf-8') as file:
    raw_text = file.read()

text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)
texts = text_splitter.split_text(raw_text)


template = """I want you to act as a academic article evaluator for IEEE. You need to read the whole text I give you 
below and extract the main point each part of the article and give me a report including the title, the author and every 
section part the structure has.
 
{txt}?"""

prompt = PromptTemplate(
    input_variables=["txt"],
    template=template,
)
prompt.format(txt=texts)
# -> I want you to act as a naming consultant for new companies.
# -> What is a good name for a company that makes colorful socks?
