import os
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 1. Set up the LLM using a free model from Hugging Face
# The token is read automatically from the HUGGINGFACEHUB_API_TOKEN environment variable
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    temperature=0.7,
    max_new_tokens=512,
)

# 2. Create a prompt template (this can remain the same)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# 3. Set up memory (this remains the same)
memory = ConversationBufferMemory(return_messages=True)

# 4. Create the runnable with message history (this remains the same)
chain = prompt | llm


# Note: For Hugging Face models, the output is a string, not an object with a 'content' attribute.
# We will access the response directly.
def get_response(input_dict, config):
    response = chatbot_with_history.invoke(input_dict, config)
    return response


chatbot_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="history",
)

# 5. Start the conversation
print("Chatbot is running with a free Hugging Face model! Type 'exit' to end...")
while True:
    try:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot shutting down. Goodbye!")
            break

        # Invoke the chain
        response = get_response(
            {"input": user_input},
            config={"configurable": {"session_id": "user_session"}}
        )
        print(f"Chatbot: {response}")

    except (KeyboardInterrupt, EOFError):
        print("\nChatbot shutting down. Goodbye!")
        break