import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

## langsmith tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="1-Q&A_Chatbot"


##prompt template

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","you are a helpful assistant,please response to the asked queries"),
        ("user","question:{question}")
    ]
)


##creating a function

def generate_response(question,llm,temperature,max_tokens):
    llm=Ollama(model=llm)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({"question":question})
    return answer


##using straemlt

st.title("Q & A CHATBOT")

##sidebars for setting
st.sidebar.title("Settings")

##selecting models
llm=st.sidebar.selectbox("select your prefered model",["gemma2:2b"])

##adjusting response parameters
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)

max_tokens=st.sidebar.slider("Max Tokens",min_value=50,max_value=300,value=150)


## Main Interface for user input
st.write("Go ahead and ask any question")
user_input=st.text_input("You: ")

if user_input:
    response=generate_response(user_input,llm,temperature,max_tokens)
    st.write(response)
else:
    st.write("Please enter a question")

