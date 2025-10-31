# Audio Transcription and Gemini Response App

This is a full-stack web application that allows you to record audio from your browser, transcribe it using `faster-whisper`, and generate a response using a Google Gemini model.

## Features

- **Audio Recording:** Record audio directly from your browser's microphone.
- **Transcription:** Transcribe the recorded audio using a selection of `faster-whisper` models.
- **Language Selection:** Choose the transcription language from a list of supported languages.
- **Gemini Integration:** Generate a response from the transcription using a selection of Google Gemini models.
- **Modern UI:** A clean and user-friendly interface for a smooth user experience.

## Project Structure

```
.
├── backend
│   ├── app.py
│   └── requirements.txt
├── frontend
│   ├── index.html
│   ├── script.js
│   └── style.css
└── README.md
```

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install backend dependencies:**
    The backend dependencies are listed in `backend/requirements.txt`.
    ```bash
    pip install -r backend/requirements.txt
    ```

3.  **Set up the Gemini API Key:**
    You will need a Google Gemini API key to use the response generation feature.

    -   Get your API key from the [Google AI Studio](https://aistudio.google.com/).
    -   Set the API key as an environment variable:
        ```bash
        export GEMINI_API_KEY="your-api-key-here"
        ```

## Usage

1.  **Start the backend server:**
    ```bash
    python backend/app.py
    ```
    The backend server will run on `http://localhost:5000`.

2.  **Start the frontend server:**
    Open a new terminal and run the following command from the `frontend` directory:
    ```bash
    cd frontend
    python -m http.server 8000
    ```
    The frontend will be available at `http://localhost:8000`.

3.  **Open the application in your browser:**
    Navigate to `http://localhost:8000` in your web browser.

## Configuration

The application provides the following configuration options in the UI:

-   **Whisper model:** Select the `faster-whisper` model to use for transcription.
-   **Transcription language:** Choose the language of the audio being transcribed.
-   **Gemini model:** Select the Gemini model to use for generating a response.
-   **Auto-send after stop:** If checked, the transcription will be automatically sent to the Gemini model for a response after you stop recording.
