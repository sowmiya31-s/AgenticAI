import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableMap, RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
import tempfile
import os

# 🔐 Step 1: Set Google Gemini API Key (HARD CODED - FOR TESTING PURPOSES ONLY)
GOOGLE_API_KEY = "AIzaSyCL6YH9Oji5IWPNIriG_FejN2IzKZfE1LE"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# 🧠 Gemini 2.0 Flash Model
llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash-latest", temperature=0)

# 🧱 Prompt Template
prompt = ChatPromptTemplate.from_template("""
You are an assistant answering questions based on a document.

Answer the following question based only on the provided context:

Context:
{context}

Question:
{question}
""")

# 🧠 HuggingFace Embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 🖼️ Streamlit UI
st.set_page_config(page_title="PDF Q&A with Gemini", layout="centered")
st.title("📄 Ask Your PDF (Powered by Gemini + LangChain)")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
question = st.text_input("Ask a question based on the PDF content:")

if st.button("Get Answer"):
    if not uploaded_file or not question.strip():
        st.warning("Please upload a PDF and enter a question.")
    else:
        try:
            # 🗃️ Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name

            # 📘 Load PDF
            loader = PyPDFLoader(tmp_path)
            docs = loader.load()

            # 📚 Split Text
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_documents(docs)

            # 📦 Create VectorStore
            vectorstore = FAISS.from_documents(chunks, embeddings)
            retriever = vectorstore.as_retriever()

            # 🔁 Chain with RAG
            rag_chain = (
                RunnableMap({"context": retriever, "question": RunnablePassthrough()})
                | prompt
                | llm
            )

            # 💬 Get Answer
            response = rag_chain.invoke(question)

            # ✅ Show Answer
            st.success("Answer extracted successfully!")
            st.markdown(f"**Q:** {question}")
            st.markdown(f"**A:** {response.content}")

        except Exception as e:
            st.error(f"An error occurred: {e}")
