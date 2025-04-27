# Doctor Companion

![docc_logo](https://github.com/user-attachments/assets/f1ca81cc-bf30-4366-80a4-9a7e7fa31610)

## About Us
Welcome to Docc, a Doctor Companion at your service 25 hours a day (you see what we did here? ). We use machine learning to predict tuberculosis, pneumonia in the lungs, and brain tumors. In the future, we will expand to skin diseases and many more. Besides, we also have an AI chatbot capable of answering your health needs.  

## Our Services
Currently, we offer you three services:
1. Analyze your Lungs for tuberculosis.
2. Analyze your Lungs for Pneumonia.
3. Analyze your Brain for tumors.

## AI Bot
The AI bot we created is an agentic RAG that leverages disease symptoms to generate answers. Users can input their system, and get an answer from our powerful bot

## RAG System
We leverage the power of `LangGraph` to create a stateful, graph-based workflow with LLMs. We are currently using `llama3.2 3b model` as our LLM with `nomic-embed-text` as our embedding model and `chromaDb` as our vector database. 

As for our RAG, we have 5 main nodes: starting router, retriever, generator, summary, and irrelevant. The irrelevant node is used to deal with irrelevant queries.  As for our summary, it gets generated only after three consecutive successful generations.

![image](https://github.com/user-attachments/assets/18382c61-18de-4a10-94f9-219fb34f3c41)


## Tech
**Frontend**: We are using NextJs for our frontend.

**Backend**: We are using Flask as our backend to serve our NextJs frontend. We have two main functionalities: image detection and RAG conversation. 

### Image Detection

Our Flask API offers five pretrained pipelines for medical image analysis:

- **Knee Osteoarthritis**  
  • 10 000+ X-rays, 5 severity grades  
  • EfficientNet-B3 backbone, MixUp & label smoothing  
  • Val accuracy ~78%

- **Skin Disease Classification**  
  • DermNet dataset (20+ lesion types)  
  • ResNeXt-50 32×4d backbone, aggressive aug & MixUp  
  • Val accuracy ~80%

- **Brain Tumor Detection**  
  • 250+ MRI scans (tumor vs. non-tumor)  
  • EfficientNet-B2 backbone  
  • Val accuracy ~99–100%

- **Pneumonia Detection**  
  • 5800+ Chest X-rays (pneumonia vs. normal)  
  • DenseNet-121 backbone  
  • Val accuracy ~99–100%

- **Tuberculosis Detection**  
  • 4200+ Chest X-rays (TB vs. normal)  
  • DenseNet-121 backbone  
  • Val accuracy ~99–100%





