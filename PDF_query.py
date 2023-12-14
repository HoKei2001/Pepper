import chardet
import markdown
from IPython.display import HTML
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from dotenv import load_dotenv, find_dotenv  # env API key
import os


def query(api, path):
    _ = load_dotenv(find_dotenv())
    os.environ["OPENAI_API_KEY"] = api  # "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"

    with open(path, 'rb') as file:
        result = chardet.detect(file.read())
    encoding = result['encoding']
    with open(path, 'r', encoding=encoding) as file:
        raw_text = file.read()
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=16100,
        chunk_overlap=0,
        length_function=len,
    )
    texts = text_splitter.split_text(raw_text)[0]

    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0)  # gpt-3.5-turbo-16k
    prompt = PromptTemplate(
        input_variables=["txt"],
        template="""Act as a academic article evaluator for IEEE. Read the whole text below and extract the main point each part of the article and try to answer me in HTML format:
            1)the first line with # is probably the title,tell me the title
            2)the author name is generally following the title and with some order number after them,you need to tell me the authors
            3)the aim of the article?
            4)the way they use to achieve aim?
            5)what the problem it solved?"
            6)list the formular used in the article in latax form and explain why the author use them
            split the line and beautify your answer and only give me the HTML   !!!
    {txt}?""",
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.run(texts)
    print(result)
    return result


if __name__ == '__main__':
    testPath = 'files_old/temporary.mmd'
    query(testPath)
