 #!/usr/bin/env python
# -*- encoding: utf-8 -*-

import openai
import pywebio, html
from pywebio.input import input
from pywebio.output import put_html

# 注册的api_key
openai.api_key = "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"

def get_answer(question):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=question,
        temperature=0.5,
        max_tokens=1024 )
    return response.choices[0].text

def chatbot():
    messages = []
    while True:
        if len(messages) == 0:
            put_html(f'<h3>我是ChatGPT聊天机器人，可以回答你的任何问题！</h3>')
            user_input = input('你好，请输入你想说的话：（并耐心等待几秒）')
        else:
            user_input = input('请输入你想说的话：（并耐心等待几秒）')

        # 记录用户输入
        messages.append(f'用户：{user_input}')
        put_html(f'<p>用户：{user_input}</p>')

        # 机器人回复
        bot_response = get_answer(user_input).strip()
        #bot_response = answer[2:]
        print(bot_response)
        messages.append(f'机器人：{bot_response}')
        put_html(f'<font color="#FF0000">机器人：</font>')
        put_html(f'<pre><font color="#FF0000">{html.escape(bot_response)}</font></pre>')
        put_html(f'<br><br>')

if __name__ == '__main__':
    pywebio.start_server(chatbot, port=8803)