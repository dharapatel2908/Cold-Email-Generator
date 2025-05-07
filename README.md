# Cold Email Generator

An AI-powered tool that generates personalized cold emails using LLAMA, LangChain, and ChromaDB. It automates context-aware message drafting tailored to recipient profiles, improving outreach efficiency and engagement.

## Features

- Upload your resume in PDF format
- Input job posting URL
- Automatically extracts job details from the posting
- Generates a personalized cold email using AI
- Copy the generated email to clipboard

## Setup

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided local URL (usually http://localhost:8501)

3. Upload your resume (PDF format)
4. Enter the job posting URL
5. Click "Generate Cold Email"
6. Copy the generated email using the "Copy to Clipboard" button

## Requirements

- Python 3.7+
- Groq API key
- Internet connection for job posting extraction

## Note

The job details extraction feature works best with well-structured job posting websites. Some websites may require additional configuration for proper extraction.
