import chainlit as cl
from chainlit import user_session
from chainlit import on_message, on_chat_start

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.document_loaders import WebBaseLoader
from langchain.memory import ConversationBufferMemory


OPENAI_KEY =

@on_chat_start
def init():
    loader = WebBaseLoader("https://eodorshop.com/collections/all")

    data = loader.load()
    data[0].page_content = data[0].page_content.replace('\n', ' ')

    sale_template = f"""
    You are a saleman, you are texting with a customer.
    You are advertising for a product, the product's information is provided in product context.
    Based on product context, answer the customer reasonably an politely.
    Answer must be in Vietnamese.
    You must call yourself “em" and call customer “anh".

    Context information is below.
    ---------------------
    Product context:
    {data[0].page_content}
    ---------------------
    {{chat_history}}
    {{message}}
    """

    sale_prompt = PromptTemplate(template=sale_template, input_variables=['message', 'chat_history'])
    memory_sale = ConversationBufferMemory(memory_key="chat_history", ai_prefix="NB", human_prefix="KH")

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1, openai_api_key=OPENAI_KEY)
    qa_chain_sale = LLMChain(llm=llm, prompt=sale_prompt, memory=memory_sale)
    cl.user_session.set("conversation_chain", qa_chain_sale)

@on_message
async def main(message: str):
    # Read chain from user session variable
    chain = cl.user_session.get("conversation_chain")

    # Run the chain asynchronously with an async callback
    res = await chain.arun({"message": message},callbacks=[cl.AsyncLangchainCallbackHandler()])

    # Send the answer and the text elements to the UI
    await cl.Message(content=res).send()
