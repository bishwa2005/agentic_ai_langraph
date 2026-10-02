from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import os

os.environ['LANGCHAIN_PROJECT']='sequential llm app'

load_dotenv()

prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a 5 pointer summary from the following text \n {text}',
    input_variables=['text']
)

model = ChatGoogleGenerativeAI(
    model='gemini-3.1-flash-lite',
    google_api_key=os.getenv('GEMINI_API_KEY')
)

parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser

config={
    'tags' : ['llm_app','report_generate'],
    'metadata' : {'model' : 'gemini_model'}
}

result = chain.invoke({'topic': 'Unemployment in India'},config=config)

print(result)
