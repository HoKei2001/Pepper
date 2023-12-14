import os
import time

import chardet

from linesplit import wrap_text
from langchain.chains import LLMChain
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter

from dotenv import load_dotenv, find_dotenv  # env API key
import os
from langchain.vectorstores import Chroma, FAISS

from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
import pywebio.input
from dotenv import load_dotenv
from pywebio.input import file_upload, actions
from pywebio.output import *
from pywebio.platform.tornado import start_server
import katex
import Nougat
from PDF_query import query
from Claude2 import Claude2bot, newClaude
from Nougat import pre_read
from langchain.memory import ChatMessageHistory

# 指定文件保存目录
UPLOAD_DIR = "files/"
target_file_path = None
# 引入MathJax库
mathjax_script = """
<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
"""


def clear_and_quit(path):
    directory_path = path  # 指定目录名称
    try:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                #print(f"Deleted file: {file_path}")
    except FileNotFoundError:
        print(f"Directory not found: {directory_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def read_and_display_markdown(filename):
    if filename:
        with open(filename, "r", encoding="utf-8") as file:
            markdown_text = file.read()
            return markdown_text
    else:
        return 'can not find file'


def bubble_with_text_Q(txt):
    text = f'''
        <div style="display: flex; justify-content: flex-end; align-items: center;">
            <div style="background-color: deepskyblue; color: white; border-radius: 5px; padding: 10px; margin-right: 10px;">
                {txt}
            </div>
            <h3 style="color: deepskyblue;">Q</h3>
        </div>
        '''
    return text


def bubble_with_text_A(txt):
    text = f'''
        <div style="display: flex; justify-content: flex-start; align-items: center;">
            <h3 style="color: grey;">A</h3>
            <div style="background-color: #99CC99; color: black; border-radius: 5px; padding: 10px; margin-left: 10px;">
                {txt}
            </div>
            
        </div>
        '''
    return text


def app():
    # file choose
    put_markdown("# 🌶 Pepper V_0.2.1")
    put_collapse('Paper evaluator', [
        put_markdown("""
    😀Now you can upload your paper and get the summary
    🤗Technical limitations, it is recommended to upload file <= 6 pages
    😘Excessively long essays may reduce accuracy or lose content"
    🥲Only ENGLISH papers supported
    ____Refresh the page to upload additional articles____
        """)
    ], open=True)

    put_collapse('User Guide', [
        put_markdown("""## User Guide
    #### Step 1 : Select and upload to submit your 【PDF file】 <= 6 pages
    #### Step 2 : Enter your OpenAI 【API Key】(You can use the test key below!)
                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
    #### Step 3 : Choose 【Summary】 and wait
    #### step 4 ：Chat with the article
    """)
    ], open=False)

    #pywebio.session.run_js("$('.custom-file-label').attr('data-browse', '浏览文件')")
    PDFfile = file_upload("Select a PDF file():", accept=".pdf", multiple=False)
    if PDFfile:
        pdf_file_name = PDFfile['filename']
        pdf_file_content = PDFfile['content']
        pdf_file_path = os.path.join(UPLOAD_DIR, pdf_file_name)

        with open(pdf_file_path, 'wb') as file:
            file.write(pdf_file_content)
        put_markdown(f" ## Your file -{pdf_file_name}- has been uploaded successfully!")

        # file transfer to mmd
        # put_text(f"Uploaded PDF file saved at: {pdf_file_path}")
        with put_loading(shape='border', color='primary'):
            put_text("Waiting for transfer...")
            Nougat.pre_read(pdf_file_path)
            # time.sleep(10)
        toast('Transfer finished', position='center', color='#2188ff', duration=3)
        file_name = os.path.splitext(pdf_file_path)[0]
        mmd_file_path = file_name + '.mmd'
        put_collapse('Paper Overview',
                     put_scrollable(put_markdown(read_and_display_markdown(mmd_file_path)), height=200), open=False)
        txt_file_path = file_name + '.txt'
        wrap_text(mmd_file_path, txt_file_path, 200)

        # file analyse
        put_markdown(f" # Paper Evaluator")
        api_key = pywebio.input.input('Please input your OPENAI key')
        # put_text(api_key)
        history = ChatMessageHistory()
        confirm = actions('Get summary first or only start chatbot?', ['Summary', 'chatbot'])
        if confirm == 'Summary':
            with put_loading(shape='border', color='primary'):
                put_text("Waiting for analysing...it will take a few minutes")
                result_text = query(api_key, txt_file_path)
                history.add_ai_message(result_text)
                # test_text = r"""
                # 1) Title: Studying the Placement of EV Charging Stations in Parking Facilities in Cities
                # 2) Authors: Jingpeng Ma, Qi He
                # 3) Aim of the article: The aim of the article is to study different EV charger placement strategies in reducing traffic congestion in parking facilities in cities.
                # 4) Method used to achieve aim: The authors implemented a SUMO (Simulation of Urban Mobility) based approach to simulate and study the placement of EV charging stations. They used a Monte Carlo method to assess the average waiting time for drivers under different charger placement strategies.
                # 5) Problem solved: The problem solved is the traffic congestion within parking facilities due to queuing or drivers waiting for available chargers. The article aims to find strategies to reduce this congestion and improve the placement of EV charging stations.
                # 6) Formulas used in the article:
                # - Poisson distribution formula: \(P(X=k)=\frac{\lambda^{k}}{k!}e^{-\lambda}\) (Equation 1) - This formula is used to calculate the probability distribution of the number of cars arriving at a parking lot per unit time.
                # - Dijkstra algorithm - This algorithm is used for route selection and finding the shortest path from one vertex to all others in a weighted graph. It is used to find the best path to achieve the shortest time for vehicles.
                # The authors use these formulas to model and simulate traffic flow, parking time, and route selection in their study.
                # """
            toast('Analyse finished', position='center', color='#2188ff', duration=3)
            put_html(mathjax_script)
            put_html(result_text)
            # print(result_text)
            # lines = test_text.splitlines()
            # for line in lines:
            #     put_html(mathjax_script)
            #     print(line)
            #     print("===")
            #     put_html(line)
            #     put_html("<br>")
            # put_collapse('Summary of the paper', open=True)
            # Not satisfied & Get more!
            put_markdown("## 🧊Not satisfied ? Get more details by chatbot!")

        # 记忆功能
        # Claude 2 限额弃用
        msg_box = output()
        # newClaude()
        put_scrollable(msg_box, height=500, keep_bottom=True)
        # default_question = """Act as a academic article evaluator for IEEE. Read the whole text below and extract the main point each part of the article and try to answer me in HTML format:
        #             1)the first line with # is probably the title,tell me the title
        #             2)the author name is generally following the title and with some order number after them,you need to tell me the authors
        #             3)the aim of the article?
        #             4)the way they use to achieve aim?
        #             5)what the problem it solved?"
        #             6)list the formular used in the article in latax form and explain why the author use them
        #             split the line and beautify your answer and only give me the HTML   !!!
        #             """
        #
        # msg_box.append(put_html(bubble_with_text_Q("Summary Analyse")))
        # with put_loading(shape='border', color='primary'):
        #     put_text("Waiting for analyse again...")
        #     msg_box.append(put_html(bubble_with_text_A(Claude2bot(mmd_file_path, default_question))))
        # while True:
        #     question = pywebio.input.input('Ask something about the article')
        #     msg_box.append(put_html(bubble_with_text_Q(question)))
        #     with put_loading(shape='border', color='primary'):
        #         put_text("Waiting...")
        #         msg_box.append(put_html(bubble_with_text_A(Claude2bot(mmd_file_path, question))))

        # OPENAI embedding
        os.environ["OPENAI_API_KEY"] = api_key  # "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"

        with open(txt_file_path, 'rb') as file:
            result = chardet.detect(file.read())
        encoding = result['encoding']
        with open(txt_file_path, 'r', encoding=encoding) as file:
            raw_text = file.read()
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=800,
            chunk_overlap=100,
            length_function=len,
        )
        texts = text_splitter.split_text(raw_text)
        embeddings = OpenAIEmbeddings()
        dosearch = FAISS.from_texts(texts, embeddings)
        # chain = load_qa_chain(OpenAI(), chain_type="stuff")
        msg_box.append(put_html(bubble_with_text_A("Any questions about this article?")))
        while True:
            question = pywebio.input.input('Ask something about the article')
            msg_box.append(put_html(bubble_with_text_Q(question)))
            history.add_user_message(question)
            with put_loading(shape='border', color='primary'):
                put_text("Waiting...")
                docs = dosearch.similarity_search(question)
                # print(docs)
                llm = ChatOpenAI(model_name="gpt-3.5-turbo-0613", temperature=0)

                prompt = PromptTemplate(
                    input_variables=["question1", "docs1"],
                    template="""Answer the questions in html format according to the context.
                                Beautify your answer for human to read easily.
                                Do not make up.If the context doesn't have the relevant information, just let me know.
                                question: {question1}
                                context: {docs1} ?""",
                )
                # prompt.format(question1=question, docs1=docs)
                chain = LLMChain(llm=llm, prompt=prompt)
                bot_answer = chain.run(question1=question, docs1=docs)

                # bot_answer = chain.run(input_documents=docs, question=question)
                put_html(mathjax_script)
                msg_box.append(put_html(bubble_with_text_A(bot_answer)))
                history.add_ai_message(bot_answer)


if __name__ == "__main__":

    clear_and_quit(UPLOAD_DIR)
    start_server(
        app,
        static_dir={'files': UPLOAD_DIR},
        port=57555,
        cdn=False,
    )
