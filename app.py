import streamlit as st
import pdfplumber
import io
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import chromadb
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Cold Email Generator",
    page_icon="✉️",
    layout="wide"
)

# Initialize ChromaDB client
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="my_collection")

# Initialize ChatGroq
llm = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("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"),
    model_name="llama-3.3-70b-versatile"
)

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file using pdfplumber"""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
            return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

def extract_job_details(job_url):
    """Extract job details from the provided URL"""
    try:
        response = requests.get(job_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # This is a basic implementation - you might need to adjust selectors based on the job site
        job_title = soup.find('h1').text if soup.find('h1') else "Job Title Not Found"
        job_description = soup.find('div', class_='job-description').text if soup.find('div', class_='job-description') else "Job Description Not Found"
        return job_title, job_description
    except Exception as e:
        st.error(f"Error extracting job details: {str(e)}")
        return None, None

def generate_email(resume_text, job_title, job_description):
    """Generate a personalized cold email using ChatGroq"""
    try:
        # Store the context in ChromaDB
        collection.upsert(
            documents=[resume_text, job_title, job_description],
            ids=["resume", "job_title", "job_description"]
        )

        prompt = f"""
        Based on the following resume and job details, generate a professional cold email:
        
        Resume:
        {resume_text}
        
        Job Title: {job_title}
        Job Description: {job_description}
        
        Generate a cold email that:
        1. Introduces the candidate professionally
        2. Highlights relevant experience from the resume that matches the job requirements
        3. Expresses genuine interest in the position
        4. Includes a call to action
        5. Maintains a professional yet engaging tone
        
        Format the email with proper greeting and signature.
        """
        
        # Generate email using ChatGroq
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        st.error(f"Error generating email: {str(e)}")
        return None

# Main app
st.title("✉️ Cold Email Generator")
st.write("Upload your resume and provide a job link to generate a personalized cold email.")

# Create two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Upload Resume")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        resume_text = extract_text_from_pdf(uploaded_file)
        if resume_text:
            st.success("Resume uploaded successfully!")

with col2:
    st.subheader("Job Details")
    job_url = st.text_input("Enter the job posting URL")
    
    if job_url:
        job_title, job_description = extract_job_details(job_url)
        if job_title and job_description:
            st.success("Job details extracted successfully!")

# Generate email button
if st.button("Generate Cold Email"):
    if 'resume_text' in locals() and job_url:
        with st.spinner("Generating your personalized cold email..."):
            email_content = generate_email(resume_text, job_title, job_description)
            
            if email_content:
                st.subheader("Generated Cold Email")
                st.write(email_content)
                
                # Add copy button
                st.button("Copy to Clipboard", on_click=lambda: st.write("Email copied to clipboard!"))
    else:
        st.warning("Please upload your resume and provide a job URL first.") 