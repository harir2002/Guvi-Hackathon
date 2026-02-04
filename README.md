# 🛡️ Agentic Scam Detection API

> A sophisticated **AI Honey-Pot System** that not only detects financial scams but engages scammers to waste their time and extract valuable intelligence.

## 🚀 Overview

This Application Programming Interface (API) serves as an intelligent shield against digital fraud. Unlike traditional spam filters, this system uses **Large Language Models (Groq Llama 3.3)** to actively converse with potential scammers.

**Key Capabilities:**
1.  **Stop the Scam**: Instantly flags messages with urgency, fear tactics, or suspicious links.
2.  **Waste Their Time**: Deploys an automated AI agent ("Ramesh Kumar") to engage the scammer in endless, confusing conversation.
3.  **Gather Intel**: Silently extracts bank accounts, UPI IDs, phone numbers, and phishing links from the conversation for reporting.

## 🛠️ Tech Stack

-   **Framework**: FastAPI (Python)
-   **AI Inference**: Groq API (Llama-3.3-70b-versatile)
-   **Vector Logic**: ChromaDB (for conversation context)
-   **Data Validation**: Pydantic v2
-   **Deployment**: Ready for Render / Vercel

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/harir2002/Guvi-Hackathon.git
cd Guvi-Hackathon
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file (copy from `.env.example`) and add your keys:
```env
API_KEY=your_secure_api_key
GROQ_API_KEY=your_groq_api_key
```

### 4. Run Server
```bash
uvicorn main:app --reload
```
API will run at: `http://127.0.0.1:8000`

## 🔌 API Reference

### **Endpoint: Detect & Engage**
`POST /api/scam-detection`

**Headers:**
-   `x-api-key`: `your_secure_api_key`
-   `Content-Type`: `application/json`

**Request Body:**
```json
{
  "message": {
    "sender": "scammer",
    "text": "Your SBI account is blocked! Update KYC immediately.",
    "timestamp": "2026-02-04T10:30:00Z"
  },
  "conversationHistory": []
}
```

**Success Response:**
```json
{
  "status": "success",
  "scamDetected": true,
  "agentResponse": "Oh my god! My pension comes in that account. What should I do sir? I am very worried.",
  "engagementMetrics": {
    "engagementDurationSeconds": 60,
    "totalMessagesExchanged": 2
  },
  "extractedIntelligence": {
    "bankAccounts": [],
    "upiIds": [],
    "phoneNumbers": ["+919876543210"],
    "phishingLinks": ["http://fake-sbi-update.com"]
  },
  "agentNotes": "Urgency tactic detected. Attempting to extract UPI ID."
}
```

## 🌍 Deployment

This project includes a `render.yaml` for one-click deployment on [Render](https://render.com).

1.  Connect your GitHub repo to Render.
2.  Render will automatically detect the configuration.
3.  The `API_KEY` will be auto-generated securely by Render.
4.  Add your `GROQ_API_KEY` in the Render dashboard.

## 📂 Project Structure
```
.
├── main.py                 # App entry point
├── models.py               # Data structures
├── prompts.py              # AI Personas & System Prompts
├── services/
│   ├── scam_detector.py    # Classification logic
│   ├── agent_service.py    # Conversation engine
│   └── intelligence.py     # Entity extraction
└── database/               # Session & Vector storage
```

---
*Built for the Guvi Hackathon 2026*
