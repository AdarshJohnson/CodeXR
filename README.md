# CodeXR Project

This repository contains the source code for the **CodeXR** AI Assistant, a multi-phase project that demonstrates the use of the Gemini 2.5 API for a variety of coding tasks.

The project is structured into three distinct phases, showcasing the evolution from a simple web application to a fully integrated VS Code extension.

## 📁 Project Structure

The project is organized into the following directories:

-   `phase1-streamlit/`: A basic Streamlit web application that introduces the core concepts of the AI assistant using mock data.
-   `phase2-debug-rag/`: An enhanced Streamlit application that integrates the Gemini 2.5 API for real-time RAG (Retrieval-Augmented Generation) and error debugging.
-   `phase3-vscode/`: The final project, a full-fledged VS Code extension with native IDE integration and advanced features.

---

## 🚀 Getting Started

### Prerequisites

To run any part of this project, you'll need the following installed:

-   [Python 3.9+](https://www.python.org/downloads/)
-   [Node.js 18+](https://nodejs.org/en/download/) (for Phase 3)
-   [Visual Studio Code](https://code.visualstudio.com/) (for Phase 3)
-   A **Gemini API Key**. You can get one from the [Google AI Studio](https://aistudio.google.com/app/apikey).

### Phase 1: Streamlit Mock Demo

This phase demonstrates the UI without needing an API key.

1.  Navigate to the directory:
    `cd phase1-streamlit`
2.  Install dependencies:
    `pip install -r requirements.txt`
3.  Run the app:
    `streamlit run app.py`

### Phase 2: RAG + Debugging App

This phase connects to the Gemini API.

1.  Create a file named `.env` in the `phase2-debug-rag/` directory.
2.  Add your API key to the `.env` file in this format:
    `GEMINI_API_KEY=your_actual_api_key_here`
3.  Navigate to the directory:
    `cd phase2-debug-rag`
4.  Install dependencies:
    `pip install -r requirements.txt`
5.  Run the app:
    `streamlit run app.py`

### Phase 3: VS Code Extension

This phase is a native VS Code extension.

1.  Navigate to the directory:
    `cd phase3-vscode`
2.  Install dependencies:
    `npm install`
3.  Compile the TypeScript code:
    `npm run compile`
4.  Open the folder in VS Code and press **F5** to launch the Extension Development Host.
5.  Inside the new VS Code window, open the Command Palette and run the command **`CodeXR: Set Gemini API Key`**. Your key is securely saved in VS Code's SecretStorage.
6.  Use the `CodeXR Assistant` panel to interact with the extension's features.

---

## ✅ Core Features

-   **Task Planner**: Breaks down complex tasks into a series of subtasks.
-   **Code Generator**: Generates concise code snippets based on a request.
-   **Error Debugger**: Provides a diagnosis and fix for a given error message and code snippet.
-   **RAG-Lite**: Allows for context-aware responses by providing documentation or code as input.
-   **Native Integration**: The VS Code extension provides a dedicated sidebar panel, Command Palette actions, and direct code insertion.

---

## 🔒 Security

[cite_start]Your Gemini API key is stored securely in VS Code's SecretStorage for Phase 3 and is not exposed in your local files[cite: 395]. For the Phase 2 demo, it is stored in a `.env` file which should be excluded from version control.
