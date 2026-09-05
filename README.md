# 🩸 AI Blood Report Analyzer

A full-stack, containerized web application that leverages **Google Gemini 1.5 Flash Multimodal LLM** to automatically analyze medical blood reports. It extracts complex biomarkers directly from images and generates easy-to-understand health summaries translated into English, Hindi, and Punjabi.

## 🚀 Features
- **Multimodal Report Understanding**: Uses Gemini 1.5 Flash Vision capabilities to extract biomarkers directly from medical images.
- **Strict Data Validation**: Enforces structured JSON output using Pydantic.
- **Multi-Lingual Summaries**: Automatically translates complex medical jargon into plain English, Hindi, and Punjabi.
- **Containerized Architecture**: Completely containerized using Docker, isolating the frontend, backend, and database for reliable deployments.

## 🛠️ Tech Stack
- **Frontend:** Streamlit (Python)
- **Backend:** FastAPI (Python)
- **Database:** MongoDB (NoSQL)
- **AI/LLM:** Google Gemini 1.5 Flash API
- **DevOps:** Docker, Docker Compose

## 🏗️ Architecture
The application is built using a Containerized Service Architecture:
1. **Frontend Service:** A Streamlit UI that accepts image uploads and displays localized results.
2. **Backend Service:** A FastAPI REST API that handles prompt engineering, communicates with the Gemini AI, and enforces JSON schemas.
3. **Database Service:** A MongoDB instance that stores historical report data.

## 🔍 Key Engineering Highlights
- **Structured LLM Outputs**: Enforced strict JSON responses from the Gemini API using Pydantic schema validation.
- **Robust Prompt Engineering**: Minimized hallucinated biomarker values through highly specific system instructions.
- **Containerized Service Architecture**: Deployed frontend, backend, and database as independent Docker services using Docker Compose.
- **Persistent Storage**: Utilized MongoDB to store historical report data and patient schemas.
- **RESTful Communication**: Designed seamless HTTP communication between the Streamlit frontend and FastAPI backend.

## ⚙️ How to Run Locally

Because the entire application is containerized, you can spin it up with a single command:

1. Clone this repository:

```bash
git clone https://github.com/ShobhitMonga/blood-report-analyzer.git
```

2. Add your Gemini API key:
- Create a `.env` file in the root directory.
- Add your key: `GEMINI_API_KEY=your_api_key_here`

3. Run with Docker:

```bash
docker compose up -d
```

4. Open your browser and go to `http://localhost:8501`.
