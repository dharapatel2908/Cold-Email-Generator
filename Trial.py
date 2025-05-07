from langchain_groq import ChatGroq

llm = ChatGroq(
    temperature=0, 
    groq_api_key='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', 
    model_name="llama-3.3-70b-versatile"
)

response = llm.invoke("when India-Pakistan war happen?")
print(response.content)