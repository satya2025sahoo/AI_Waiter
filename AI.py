#AI.py

import chromadb
from llama_cloud import MessageRole
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import SimpleDirectoryReader
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import ServiceContext, VectorStoreIndex
from llama_index.core.storage.storage_context import StorageContext
#from llama_index.embeddings.huggingface import HuggingFaceEmbedding

import google.generativeai as genai
import warnings

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ".\organic-dryad-434803-u3-4b45fed68b4b.json"

warnings.filterwarnings("ignore")

# Set up Google Generative AI API key
genai.configure(api_key='AIzaSyCkxCJOK8tCLz2OayEeHmu-SEQSNPgoc78')

# Initialize the Gemini model
model = Gemini(models='gemini-pro', api_key='AIzaSyCkxCJOK8tCLz2OayEeHmu-SEQSNPgoc78')
gemini_embed_model = GeminiEmbedding(model_name="models/embedding-001")
#embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Define role mappings for Gemini model
ROLES_TO_GEMINI = {
    'user': 'Customer',       # Maps the 'user' role
    'system': 'system_role',   # Maps the 'system' role (could be prompt or system message)
    MessageRole.USER: 'Customer',  # Maps the 'user' role
    MessageRole.SYSTEM: 'system_role',  # Maps the 'system' role
    MessageRole.MODEL: 'model',  # Maps the 'model' role to Gemini's assistant role
}


class AIVoiceAssistant:
    def __init__(self):
        self._chroma_client = chromadb.EphemeralClient()  # Correct client instantiation
        self._llm = model
        self._service_context = ServiceContext.from_defaults(
            llm=self._llm, embed_model=gemini_embed_model, chunk_size=800, chunk_overlap=20
        )
        self._index = None
        self._create_kb()
        self._create_chat_engine()

    def _create_kb(self):
        try:
            #db = chromadb.PersistentClient(path="./chroma_db_nccn")
            #chroma_collection = db.get_or_create_collection("kitchen_db")
            reader = SimpleDirectoryReader(
                input_files=[r".\rag\restaurant_file.txt"]
            )
            documents = reader.load_data()
            chroma_collection = self._chroma_client.create_collection("quickstart")
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            self._index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, embed_model=gemini_embed_model)
            print("Knowledgebase created successfully!")
        except Exception as e:
            print(f"Error while creating knowledgebase: {e}")
            self._index = None

    def _create_chat_engine(self):
        if self._index is None:
            print("Knowledgebase is not created. Cannot create chat engine.")
            return
        memory = ChatMemoryBuffer.from_defaults(token_limit=1500)
        self._chat_engine = self._index.as_chat_engine(
            chat_mode="context",
            memory=memory,
            system_prompt=self._prompt,
            llm=self._llm,
            role_map=ROLES_TO_GEMINI,

        )

    def interact_with_llm(self, customer_query):
        try:
            print("Debug: Sending query to chat engine")
            AgentChatResponse = self._chat_engine.chat(customer_query)
            print("Debug: Received response from chat engine")
            answer = AgentChatResponse.response
            return answer
        except KeyError as e:
            print(f"KeyError: {e}")
            return "An error occurred while processing your query."

    @property
    def _prompt(self):
        return """
            You are a professional AI Assistant receptionist working in Bangalore's one of the best restaurant called Bangalore Kitchen.
            Ask questions one by one and keep the conversation engaging. Always ask these:
            [Ask Name and contact number, what they want to order, and end the conversation with greetings.]
            
            If you don't know the answer, just say that you don't know.
            Keep your answers concise, under 10 words.
        """

# Initialize the AI Assistant
#pia = AIVoiceAssistant()