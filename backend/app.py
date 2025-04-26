import openai
import gradio as gr
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.document_loaders import CSVLoader


OPENAI_API_KEY = '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'
loader = CSVLoader("finale.csv")
pages = loader.load()

embedding = OpenAIEmbeddings()
llm_name = "gpt-4o"
llm = ChatOpenAI(model_name=llm_name, temperature=0)

print("Beginning")
vectordb = Chroma.from_documents(pages, embedding)
print('Database Loaded')

# Building prompt
template_uz = """Use the following pieces of context to answer the question at the end.
Please write all of the information in uzbek language. If the user asks to find a disease by symptoms, firstly, give two possible diseases.
Then you have to include precaution for all two possible diseases. The last thing you have to do is include Description for only first possible disease and include information about Doctor.

{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT_uz = PromptTemplate(input_variables=["context", "question"], template=template_uz)

# Running chain
qa_chain_uz = RetrievalQA.from_chain_type(llm, retriever=vectordb.as_retriever(), return_source_documents=False,
                                          chain_type_kwargs={"prompt": QA_CHAIN_PROMPT_uz})


def yes_man(question, history):
    return str(qa_chain_uz({"query": question})['result'])


chat_interface = gr.ChatInterface(
    yes_man,
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(placeholder="Type", container=False, scale=7),
    title="Doctor Consultant",
    description="!!! Bu shunchaki sun'iy intellekt tomonidan berilgan maslahat ko'proq ma'lumot olish uchun tajribali doktorlar bilan bog'laning !!!",
    theme="soft",
    examples=["Menda bosh og'rig'i, bo'yinning qattiqligi, ovqat hazm qilish buzilishi, ko'rishning buzilishi, asabiylashish kuzatilyapti."],
    retry_btn=None,
    undo_btn="O'chirish",
    clear_btn="Tozalash",
)

import torch
from fastai import *
from fastai.vision.all import *

# Pneumonia section

learn = load_learner("model.pkl")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

text_input = gr.Image()


def image_processing_function(image):
    # Convert Gradio image object to a PyTorch tensor
    image_tensor = torch.tensor(image)

    # Make predictions using your model
    predictions = learn.predict(image_tensor, with_input=True)

    # Return predictions (assuming it's a text output)
    return f"{predictions[1]}: {int(predictions[3][predictions[3].argmax()] * 100)}%"


pneumo_interface = gr.Interface(
    fn=image_processing_function,
    inputs=text_input,
    outputs="text",
    title="Pneumonia",
    description="""!!! Bu shunchaki sun'iy intelekt tomonidan berilgan maslahat. Ko'proq ma'lumot olish uchun tajribali doktorlar bilan bog'laning !!! 
    Iltimos faqat o'pkaga oid bo'lgan sifatli rasm kiriting!""",
    theme="soft",
    examples=["data/norm.jpg"],
    live=False
)

# Tuberculosis

learntb = load_learner("modeltb.pkl")

text_input_tb = gr.Image()


def image_processing_function_tb(image):
    # Convert Gradio image object to a PyTorch tensor
    image_tensor_tb = torch.tensor(image)

    # Make predictions using your model
    predictions_tb = learntb.predict(image_tensor_tb, with_input=True)

    # Return predictions (assuming it's a text output)
    return f"{predictions_tb[1]}: {int(predictions_tb[3][predictions_tb[3].argmax()] * 100)}%"


tuber_interface = gr.Interface(
    fn=image_processing_function_tb,
    inputs=text_input_tb,
    outputs="text",
    title="Tuberculosis",
    description="""!!! Bu shunchaki sun'iy intellekt tomonidan berilgan maslahat. Ko'proq ma'lumot olish uchun tajribali doktorlar bilan bog'laning !!! 
    Iltimos faqat o'pkaga oid bo'lgan sifatli rasm kiriting!""",
    theme="soft",
    examples=["data/normtb.png"],
    live=False
)

# Brain Tumor

learnbt = load_learner("modelbt.pkl")

text_input_bt = gr.Image()


def image_processing_function_bt(image):
    # Convert Gradio image object to a PyTorch tensor
    image_tensor_bt = torch.tensor(image)

    # Make predictions using your model
    predictions_bt = learnbt.predict(image_tensor_bt, with_input=True)

    # Return predictions (assuming it's a text output)
    return f"{predictions_bt[1]}: {int(predictions_bt[3][predictions_bt[3].argmax()] * 100)}%"


bt_interface = gr.Interface(
    fn=image_processing_function_bt,
    inputs=text_input_bt,
    outputs="text",
    title="Brain Tumor",
    description="""!!! Bu shunchaki sun'iy intellekt tomonidan berilgan maslahat. Ko'proq ma'lumot olish uchun tajribali doktorlar bilan bog'laning !!! 
    Iltimos faqat o'pkaga oid bo'lgan sifatli rasm kiriting!""",
    theme="soft",
    examples=["data/normtb.png"],
    live=False
)

final = gr.TabbedInterface([chat_interface, pneumo_interface, tuber_interface, bt_interface],
                           tab_names=['Chatbot', 'Pneumonia', 'Tuberculosis', 'Brain Tumor'])
final.launch(share=True)

# from environs import Env
# Libraries
# pip install openai
# pip install langchain
# pip install unstructured
# pip install tiktoken
# pip install chromadb
# pip install langchain-community

# env = Env()
# env.read_env()
# sys.path.append('../..')

# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# docs = text_splitter.split_documents(pages)

# llm.predict("Hello world!")
# persist_directory = 'doc/chroma/'
# vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

