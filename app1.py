from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio

STR_JAPANESE = "日本語で訳して。"


async def main():
    agent = Agent(
        task="中居正広は示談金を支払ったが、なにがあった？" + STR_JAPANESE,
        llm=ChatOpenAI(model="gpt-4o-mini"),
    )
    result = await agent.run()
    print(result)
    print('\n')
    print('【ここから】')
    if len(result.history) > 0:
        print(result.history[len(result.history)-1].result[0].extracted_content)

asyncio.run(main())
