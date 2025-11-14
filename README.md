# 🌍 Multilingual Blog Generator using LangChain + LangGraph + Groq + FastAPI  
Create high-quality blogs in **English, Hindi, and French** using an agentic LLM pipeline powered by **LangGraph**, **LangChain**, and **Groq**.

---

## 🚀 Project Overview

This project is a **production-ready multilingual blog generator** that automatically:
- Generates a **SEO-friendly blog title**
- Writes **full-length blog content** with Markdown formatting
- Translates it into **Hindi** or **French** with cultural adaptation
- Uses an **agentic routing graph** to decide which translation pipeline to trigger
- Exposes APIs via **FastAPI** for easy integration

---

## 🧠 Why LangGraph?

Traditional prompt chaining becomes messy as logic grows.  
**LangGraph** gives a structured, visual, stateful approach to building agent workflows with:
- Deterministic state management  
- Node-based execution flows  
- Routing logic (e.g., `route → translation`)  
- Well-defined return shapes  
- Streaming support  

Perfect for multilingual blog generation workflows.

---

## ⚙️ Tech Stack

### **Core**
- **Python 3.10+**
- **LangChain** – LLM orchestration
- **LangGraph** – agentic stateful pipeline
- **Groq (LLM API)** – ultra-fast inference for generation & translation
- **FastAPI** – build REST APIs
- **Uvicorn** – ASGI server

### **Other integrations**
- **Structured Output (LangChain)**  
- **Pydantic / TypedDict state management**  
- **Markdown formatting**  
- **Routing nodes for conditional language translation**

---

## 📁 Project Architecture

src/
│
├── states/
│ ├── blogstate.py # TypedDict / Pydantic definitions for BlogState
│
├── nodes/
│ ├── blog_node.py # Title generator, content generator, translation node
│
├── graphs/
│ ├── graph_builder.py # LangGraph graph creation, routing logic
│
├── server/
│ ├── app.py # FastAPI endpoints
│
└── main.py # Entry point

## 🧩 How the Workflow Works (LangGraph)

### **1️⃣ title_creation node**
- Creates an SEO-friendly blog title

### **2️⃣ content_generation node**
- Generates full blog content using Markdown
- Uses Groq LLM for fast results

### **3️⃣ route node**
- Reads `current_language`
- Passes routing decision to graph

### **4️⃣ translation node**
- Converts to Hindi / French
- Preserves tone, style, formatting
- Cultural adaptation rules

---

## 🛠 Installation

git clone https://github.com/your-username/blog-generator-langgraph.git
cd blog-generator-langgraph

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
'''
🔑 Environment Variables

Create a .env file:

GROQ_API_KEY=your_groq_key

▶️ Running the API
uvicorn app:app --reload


API will be available at:

👉 http://127.0.0.1:8000/docs

(OpenAPI UI)

📡 API Usage
POST /blogs
Request Body
{
  "topic": "Agentic AI vs AI Agents",
  "current_language": "hindi"
}

Response
{
  "blog": {
    "title": "...",
    "content": "..."
  }
}

📘 Learnings
🧠 LangGraph

State must always return a dict (never raw strings)

Conditional routing requires well-defined state keys

Graph debug logging is invaluable for tracing node failures

⚡ Groq

Extremely fast inference → perfect for real-time blog generation

GroqChat models perform well for multilingual translation

🌍 Translation Engineering

Simply “translate this” is not enough

Added cultural adaptation, formatting preservation, markdown integrity

🧱 Robust Design

Structured output prevents LLM hallucination in blog formats

Pydantic state ensures nodes produce correct schema

Resilient fallback mechanisms prevent graph crashes

⭐ Future Enhancements

Add more languages (Spanish, German, Arabic)

Add sentiment/style controls (formal, friendly, witty)

Add content length selection (short/medium/long)

Deploy on Docker + Kubernetes

Add Streamlit or Next.js frontend

🤝 Contributing

Pull requests are welcome!
Open an issue if you find bugs or want features.

💬 Author

Akshay Sharma
Feel free to connect on LinkedIn or GitHub!
