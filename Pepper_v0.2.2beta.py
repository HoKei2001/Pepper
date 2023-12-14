import os
import time
import threading
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


def read_and_display_markdown(filename):
    if filename:
        with open(filename, 'r', encoding='utf-8') as file:
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


def long_time_answer(question, docs, stop_event):
    while not stop_event:
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
        return bot_answer


def chatbot(question, docs):
    stop_event = threading.Event()

    # 创建一个线程来执行上述代码
    code_thread = threading.Thread(target=long_time_answer(question, docs,), args=(stop_event,))

    # 启动线程
    code_thread.start()

    # 等待线程执行完毕，设置超时时间为10秒
    code_thread.join(timeout=3)

    # 如果线程在规定时间内执行完毕
    if not code_thread.is_alive():
        print("代码执行完毕")
        return
    else:
        # 如果线程超时仍未执行完毕，执行以下操作
        print("代码执行超时，执行其他操作")
        # 设置 stop_event，通知线程终止执行
        stop_event.set()


def app():
    # file choose
    put_markdown('''# Paper evaluator 🌶 Pepper V_0.2.2
    😀Now you can upload your paper and get the summary
    🤗Technical limitations, it is recommended to upload file <= 6 pages
    😘Excessively long essays may reduce accuracy or lose content"
    🥲Only ENGLISH papers supported
    ''')
    put_markdown("""## Test api_key
    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""")
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
        wrap_text(mmd_file_path, txt_file_path, 100)

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
        with open(txt_file_path, 'r', encoding='utf-8') as file:
            raw_text = file.read()
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=500,
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
                bot_answer = chatbot(question, docs)
                put_html(mathjax_script)
                msg_box.append(put_html(bubble_with_text_A(bot_answer)))
                history.add_ai_message(bot_answer)


if __name__ == "__main__":
    start_server(
        app,
        static_dir={'files': UPLOAD_DIR},
        port=80,
        cdn=False,
    )
