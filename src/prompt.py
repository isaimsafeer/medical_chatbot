from langchain_core.prompts import ChatPromptTemplate

# Define system_prompt as a single string
system_prompt = (
    "You are an assistant for question answering task. "
    "Use the following pieces of retrieved information to answer the question. "
    "If you don't know the answer, just say 'I don't know.' "
    "Answer concisely.\n\n"
    "{context}"
)

# Create ChatPromptTemplate correctly
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])
