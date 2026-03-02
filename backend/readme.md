# SOLUTION DOCUMENT: VOYAGER AI

**Project Name:** Voyager AI – Autonomous Vacation Planner  
**Student Name:** Rizki Ramadhan Lestariono  
**Submission Date:** March 2, 2026  

---

## 1. Problem Statement

In the current digital travel landscape, users are burdened with a passive "search-based" experience. Planning a vacation requires manually checking personal calendars, searching for flights and hotels separately, comparing prices across multiple platforms, and executing transactions individually. This process is time-consuming, fragmented, and prone to human error (e.g., booking a flight that conflicts with a personal meeting).

**The Challenge:** To design and implement an **Autonomous AI Agent** that moves beyond simple text recommendations. The agent must possess "agency"—the ability to:
1.  **Contextualize:** Check the user's personal constraints (Calendar availability).
2.  **Retrieve:** Fetch real-time data for accommodation and transport (via Mock API).
3.  **Execute:** Perform tangible actions (Booking transactions & Invoice generation).
4.  **Persist:** Remember transaction states across sessions using a database.

---

## 2. Approach & High-Level Architecture

### 2.1 Architectural Strategy: Agentic Tool-Use
Instead of using a traditional **RAG (Retrieval-Augmented Generation)** architecture—which is typically optimized for semantic document search—Voyager AI utilizes an **Agentic Tool-Use Architecture**.

We chose this approach because travel booking is **transactional and deterministic**. Users require exact prices, specific dates, and confirmed booking statuses, not probabilistic text summaries. The Large Language Model (LLM) acts as a "Router" or "Brain," determining which specific tool to call based on the user's intent.

### 2.2 System Workflow
1.  **User Input:** The user provides a natural language request (e.g., *"Book a hotel in Bali for next week"*).
2.  **Backend Orchestration (LangGraph):** The core agent analyzes the request state.
3.  **Tool Execution:**
    * **Calendar Tool:** Verifies schedule availability.
    * **Flight/Hotel Tools:** Queries the Mock Database (`hotels.json`) for inventory.
    * **Logic Handler:** Implements "Negative Testing" (e.g., returning a specific error if the destination is unavailable, avoiding hallucination).
4.  **Data Persistence:** Successful transactions are written to a JSON-based database (`bookings_db.json`), generating a unique Booking ID.
5.  **Response Generation:** The agent returns a structured JSON payload, which the Frontend intercepts to render a visual Booking Invoice.

### 2.3 Architecture Diagram
![Voyager AI Architecture](architecture.png)
*(Figure 1: High-Level Architecture demonstrating Agentic Tool-Use with Persistence)*

---

## 3. Tech Stack

The solution is built using an Open Source-first approach:

* **Core AI Engine:** **Meta Llama-3-8b (via Groq API)**
    * *Reason:* Selected for its extremely low latency (<1s) and strong reasoning capabilities in tool-calling scenarios.
* **Orchestration:** **LangChain & LangGraph**
    * *Reason:* Provides the state graph required to manage cyclic conversation flows and separate tool outputs from final answers.
* **Backend:** **Python FastAPI**
    * *Reason:* High-performance, asynchronous framework suitable for handling concurrent agent requests.
* **Frontend:** **HTML5, Tailwind CSS, Vanilla JS**
    * *Reason:* Implements a Server-Driven UI pattern where the backend controls visual components (Cards/Invoices) via JSON markers.
* **Database:** **JSON Mock DB**
    * *Reason:* Lightweight file-based storage to demonstrate data persistence and retrieval capabilities for the Proof of Concept (PoC).

---

## 4. Risk & Vulnerabilities Analysis

The following table outlines potential risks identified during the development of this PoC and their mitigation strategies.

| Risk ID | Risk Description | Likelihood / Impact | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **R-01** | **Prompt Injection:** Malicious users attempting to override system instructions to access unauthorized tools or reveal the system prompt. | High / High | Implementation of a strict **System Prompt** scope and an output **Interceptor** that sanitizes response data before it reaches the frontend. |
| **R-02** | **Model Hallucination:** The AI might invent flight numbers or hotel prices that do not exist in the database. | Low / Medium | **Tool-Level Validation:** The Python tools are coded to return explicit error messages if data is missing, preventing the LLM from "guessing" the data. |
| **R-03** | **Data Race Condition:** Since the database is a flat JSON file, simultaneous write requests could corrupt the file. | Medium / Medium | For the PoC, this is acceptable. For Production, migration to a Transactional SQL Database (PostgreSQL) with **Row-Level Locking** is required. |
| **R-04** | **PII Exposure:** Storing guest names and booking details in plain text logs. | Medium / High | In a real-world scenario, all Personally Identifiable Information (PII) must be encrypted (**AES-256**) at rest and transmitted via HTTPS. |

---

## 5. Conclusion

Voyager AI successfully demonstrates the capability of Generative AI to move beyond conversation into **Action Execution**. By integrating Llama-3 with a structured toolset and a persistent database, the system acts as a reliable travel assistant. 

Key achievements include:
1.  **Autonomous Planning:** Capability to check user availability before booking.
2.  **Persistence:** Robust saving and retrieval of booking data.
3.  **Visual Output:** Generation of downloadable digital invoices.

The ability to handle booking transactions, generate documents, and retrieve past data proves the viability of this architecture for enterprise-level travel applications.