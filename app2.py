import os
import streamlit as st
import asyncio
from time import sleep
import sys

from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
STR_JAPANESE = "日本語で訳して。"


async def main(agent):
    result = await agent.run()
    print(result)
    print('\n')
    print('【ここから】')
    if len(result.history) > 0:
        return result
    return ''



st.title("BROWSER-USE システム")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

input_message = st.chat_input("準備ができました。メッセージを入力してください。")
if input_message:
    st.session_state.messages.append({"role": "user", "content": input_message})
    print(f"入力されたメッセージ: {input_message}")
    
    # ===== ユーザ側マークダウン =====
    with st.chat_message("user"):
        st.markdown(input_message)

    # ===== アシスタント側マークダウン =====
    with st.chat_message("assistant"):
        agent = Agent(
            task=input_message + STR_JAPANESE,
            llm=ChatOpenAI(model="gpt-4o-mini"),
        )
        
        # 非同期関数で結果を取得
        try:
            result = asyncio.run(main(agent))
            
            # デバッグ用に結果を確認
            print(f"Result history: {result.history}")
            
            # データが存在するか確認
            if not result.history or len(result.history) == 0:
                response = "エージェントから結果を取得できませんでした。"
            else:
                # 安全にデータを取り出す
                last_result = result.history[-1]  # 最後の結果を取得
                if hasattr(last_result, 'result') and last_result.result:
                    response = last_result.result[0].extracted_content
                else:
                    response = "結果の形式が予期したものと異なります。"
        except Exception as e:
            response = f"エラーが発生しました: {e}"
            print(f"エラー詳細: {e}")
        
        # アシスタントのレスポンスを表示
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
