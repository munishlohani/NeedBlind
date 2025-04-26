from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from typing_extensions import TypedDict
from typing import Annotated, List
from langgraph.graph import add_messages
from langchain_community.document_loaders import CSVLoader
from langchain_ollama import ChatOllama

#embedding model

embedding = OllamaEmbeddings(model="nomic-embed-text")

#llm model

llm = ChatOllama(model="llama3.2", temperature=0)
llm_json_model = ChatOllama(
    model="llama3.2", format="json", temperature=0
) 

#vector database

loader = CSVLoader("finale.csv")
pages = loader.load()

vectordb = Chroma.from_documents(pages, embedding)
retriever = vectordb.as_retriever()

# Doc format
def format_doc(docs):
    return "\n\n".join(doc.page_content for doc in docs)

#langgraph
class GraphState(TypedDict):
    """
    Graph is a state dictionary that contains infomation we want to propagate to, and modify in, each graph node.
    """

    summary: str
    question: Annotated[List[str], add_messages]
    generation: Annotated[List[str], add_messages]
    documents: List[str]

import json
from langchain_core.messages import SystemMessage, HumanMessage

router_instructions = """
you are an expert at distinguishing the questions that may be related health and medical issues. If you think the question is related to health, wellbeing, diseases, or any thing that is related to health and medicine and wellbeing, you give out "yes". Else you output "no".

#Instructions
- If the question is **relevant** return a JSON with a single key, {"datasource": "yes"}.
- If the question does **not align with** the summary, the keywords or any general medical/health, return  a JSON with a single key {"datasource": "no"}.
"""

router_prompts="""
The summary of your conversation if it exists: \n{summary}\n


The question may be different from the summary above.
The question: \n{question}\n

"""

#Start Route
def start_route(state: GraphState):
    """Routes question to fail_rag or RAG"""

    question = state["question"][-1].content
    summary = state.get("summary", "Summary Not Found")
    router_prompts_format = router_prompts.format(summary=summary, question=question)

    route_question = llm_json_model.invoke(
        [
            SystemMessage(content=router_instructions),
            HumanMessage(content=router_prompts_format),
        ]
    )

    print(json.loads(route_question.content))
    source = json.loads(route_question.content)["datasource"].lower()
    return source

irrelevent_instructions="""You are an expert at responding to an irrelevant question. If You try to analyze the summary of the conversation, if it exists, and reply the user. However, you also make sure to answer back about the irrelevancy of the question

For generic starting questions like "Hey", "Hi",etc. you can reply them with "Hi! Im DoCC, your personal medical assistant. How can I help you today?"

Here are some Relevent Questions:

1. What is the cause of the disease?
2. What are the symptoms of the disease?
3. What is the treatment for the disease?
4. What is the prevention of the disease?
5. What is the cause of the disease?

"""


irrelevent_prompt = """
Here is the question that was deemed irrelevant:

{question}

Here is the summary of the chat (formatted as QQQQ-AAAA):

{summary}

Note: The portion below is not a part of the summary or previous interaction.

Here is the query result for the given question if it exists:

{documents}

Response Guidance:

1. Politely inform the user that you cannot answer the question.
2. Reference previous questions from the summary and suggest similar but relevant inquiries.
3. Keep the response clear and structured to help the user stay on track.
"""

def irrelevent_check(state):
    print("---Irrelevent---")
    question = state["question"][-1].content
    summary = state.get("summary", "Summary Does not Exist")
    document = format_doc(state.get("documents", []))
    irrelevent_prompt_format = irrelevent_prompt.format(
        question=question, summary=summary, documents=document
    )

    result = llm.invoke(
        [SystemMessage(content=irrelevent_instructions)]
        + [HumanMessage(content=irrelevent_prompt_format)]
    )

    return {"generation": [result.content]}

# Retriever
def doc_retriever(state: GraphState):
    """Retrieve Documents from vectorstore"""
    print("---Retrieve---")
    question = state["question"][-1].content
    documents = retriever.invoke(question)
    print(documents)
    return {"documents": documents}


generator_instruction="""
You are an AI trained to act as a **highly experienced medical doctor with multidisciplinary expertise**.

Use the **context only and documents** to generate your response.  
 **Do not infer, guess, fabricate information, or introduce external knowledge**.  
Maintain a **professional, cautious, and medically responsible tone** at all times.

Here are the document: {documents}\n

Think carefully about the context above. Now, review the user question:
{question}

---

### If the user asks to identify a disease based on symptoms:

1. **Begin by identifying two possible diseases** from the context.
2. **List all precautions separately for both diseases.**
3. **Provide a description for the *first* possible disease only.**
4. **Clearly recommend which type of doctor the user should consult.**
5. **If there is any uncertainty, advise the user to consult a qualified medical professional immediately.**

---

### Response Format Guidelines:

- Respond in **English**.
- Use **Markdown** for all the response with appropriate tags.
- Include **headers**,  **line breaks**, **bullets** in your response.
- If the **user's query is unrelated to the medical domain**, **do not respond**.
"""

#generator
def generator(state: GraphState):
    print("--Generator--")
    docs = state["documents"]

    formatted_doc = format_doc(docs)

    question = state["question"][-1].content

    generator_prompt_format = generator_instruction.format(
        documents=formatted_doc, question=question
    )
    result = llm.invoke([HumanMessage(content=generator_prompt_format)])
    print(result)
    return {"generation": [result]}

# At least 3 iterations to generate a summary
from langgraph.graph import StateGraph, END

def should_continue(state: GraphState):
    print("--Should Continue--")
    """Return the Next Node to Continue"""

    if len(state["question"]) >= 3:
        return "chat_summary"
    else:
        return END
    
def chat_summary(state: GraphState):
    print("--Summary Step--")

    summary = state.get("summary", "")
    questions = state.get("question", [])[-1].content
    generations = state.get("generation", [])

    format_question = "\n".join(q for q in questions)
    format_generation = "\n".join(gen.content for gen in generations)

    if summary:
        sum_message = format_question + "\n" + format_generation
        response = llm.invoke(
            [
                SystemMessage(
                    content="""Extend the given summery with the questions"""
                ),
                HumanMessage(content=sum_message),
            ]
        )

    else:
        sum_message = """
            You are a helpful assistant. Please create a summary based on the following context:

            Context:
            {format_question}

            Responses:
            {format_generation}

            Please summarize the main points and provide a concise response in a paragraph format.
        """

        sum_message_format = sum_message.format(
            format_question=format_question, format_generation=format_generation
        )
        response = llm.invoke([HumanMessage(content=sum_message_format)])

    delete_questions = questions[-3:]

    return {"summary": response.content, "question": delete_questions}

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver


builder = StateGraph(GraphState)

#Nodes
builder.add_node("retriever", doc_retriever)
builder.add_node("generate", generator)
builder.add_node("check_summary", should_continue)
builder.add_node("chat_summary", chat_summary)
builder.add_node("irrelevent_check", irrelevent_check)

# Conditional entry points
builder.set_conditional_entry_point(
    start_route, {"yes": "retriever", "no": "irrelevent_check"}
)

#Edges
builder.add_edge("irrelevent_check", END)
builder.add_edge("retriever", "generate")
builder.add_conditional_edges("generate", should_continue)
builder.add_edge("chat_summary", END)

#Memory Saver
memory_saver = MemorySaver()


#Graph
graph = builder.compile(checkpointer=memory_saver)
config = {"configurable": {"thread_id": "1"}}


#Run
def bot_run(question: str):
    input_message = [HumanMessage(question)]
    output = graph.invoke({"question": input_message}, config=config)
    return output["generation"][-1].content


