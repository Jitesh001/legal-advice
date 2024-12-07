API_O = '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'

from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
import streamlit as st
from langchain.chains.conversation.memory import ConversationEntityMemory

# Define the legal context as part of the prompt template
legal_context = """
You are a knowledgeable legal assistant specializing in guiding users through various law-related case studies.
You have all knowledge of indian constitution and laws.
When the user asks questions or describes legal situations, provide detailed and informative guidance based on the respective legal topic.
"""

# Create a custom prompt template using the legal context
# Modify the template to accept input, entities, and history variables
prompt_template = f"""
{legal_context}
Current conversation history: {{history}}
Entities: {{entities}}
Human: {{input}}
Assistant:
"""

# Create a PromptTemplate object
template = PromptTemplate(input_variables=["input", "history", "entities"], template=prompt_template)

# Set Streamlit page configuration
st.set_page_config(page_title='🧠MemoryBot🤖', layout='wide')

# Initialize session states
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []

# Function to get user input
def get_text():
    input_text = st.text_area("You: ", st.session_state["input"], key="input",
                            placeholder="Your AI assistant here! Ask me anything ...", 
                            label_visibility='hidden', height=200)
    return input_text

# Function to start a new chat
def new_chat():
    save = []
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        save.append("User:" + st.session_state["past"][i])
        save.append("Bot:" + st.session_state["generated"][i])        
    st.session_state["stored_session"].append(save)
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["input"] = ""
    st.session_state.entity_memory.entity_store = {}
    st.session_state.entity_memory.buffer.clear()

# Set up sidebar with various options
with st.sidebar.expander("🛠️ ", expanded=False):
    if st.checkbox("Preview memory store"):
        with st.expander("Memory-Store", expanded=False):
            st.session_state.entity_memory.store
    if st.checkbox("Preview memory buffer"):
        with st.expander("Buffer-Store", expanded=False):
            st.session_state.entity_memory.buffer
    MODEL = st.selectbox(label='Model', options=['gpt-3.5-turbo','gpt-4'])
    K = st.number_input(' (#) Summary of prompts to consider', min_value=3, max_value=20000)

# Set the title and description
st.title("🤖 Chat Bot with 🧠")
st.subheader(" Powered by 🦜 LangChain + OpenAI + Streamlit")

# Check if API key is entered
if API_O:
    # Create a ChatOpenAI instance instead of OpenAI
    llm = ChatOpenAI(
        openai_api_key=API_O,  # Correct parameter for the API key
        model=MODEL,  # Model selected by the user
        temperature=0,  # Optional argument for controlling randomness
        verbose=False  # Optional logging
    )

    # Create a ConversationEntityMemory object if not already created
    if 'entity_memory' not in st.session_state:
        st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=K)

    # Create the ConversationChain object with the updated prompt template
    Conversation = ConversationChain(
        llm=llm, 
        prompt=template,  # Pass the PromptTemplate here
        memory=st.session_state.entity_memory
    )
else:
    st.sidebar.warning('API key required to try this app. The API key is not stored in any form.')

# Add a button to start a new chat
st.sidebar.button("New Chat", on_click=new_chat, type='primary')

# Get the user input
user_input = get_text()

# Generate output using the ConversationChain object
if user_input:
    # Extract history and entities from memory
    history = st.session_state.entity_memory.buffer
    entities = st.session_state.entity_memory.entity_store

    # Generate the response using the updated ConversationChain
    output = Conversation.run(input=user_input, history=history, entities=entities)

    # Update the session state with new user input and output
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

# Display conversation history
download_str = []
with st.expander("Conversation", expanded=True):
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        st.info(st.session_state["past"][i], icon="🧐")
        st.success(st.session_state["generated"][i], icon="🤖")
        download_str.append(st.session_state["past"][i])
        download_str.append(st.session_state["generated"][i])

    download_str = '\n'.join(download_str)
    if download_str:
        st.download_button('Download', download_str)

# Display stored conversation sessions in the sidebar
for i, sublist in enumerate(st.session_state.stored_session):
    with st.sidebar.expander(label=f"Conversation-Session:{i}"):
        st.write(sublist)

# Clear all stored conversation sessions
if st.session_state.stored_session:
    if st.sidebar.checkbox("Clear-all"):
        del st.session_state.stored_session

# from langchain.chains import ConversationChain
# from langchain.chains.conversation.memory import ConversationEntityMemory
# from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
# from langchain.chat_models import ChatOpenAI
# import streamlit as st

# # Set Streamlit page configuration
# st.set_page_config(page_title='🧠MemoryBot🤖', layout='wide')

# # Initialize session states
# if "generated" not in st.session_state:
#     st.session_state["generated"] = []
# if "past" not in st.session_state:
#     st.session_state["past"] = []
# if "input" not in st.session_state:
#     st.session_state["input"] = ""
# if "stored_session" not in st.session_state:
#     st.session_state["stored_session"] = []

# # Function to get user input
# def get_text():
#     input_text = st.text_input("You: ", st.session_state["input"], key="input",
#                             placeholder="Your AI assistant here! Ask me anything ...", 
#                             label_visibility='hidden')
#     return input_text

# # Function to start a new chat
# def new_chat():
#     save = []
#     for i in range(len(st.session_state['generated'])-1, -1, -1):
#         save.append("User:" + st.session_state["past"][i])
#         save.append("Bot:" + st.session_state["generated"][i])        
#     st.session_state["stored_session"].append(save)
#     st.session_state["generated"] = []
#     st.session_state["past"] = []
#     st.session_state["input"] = ""
#     st.session_state.entity_memory.entity_store = {}
#     st.session_state.entity_memory.buffer.clear()

# # Set up sidebar with various options
# with st.sidebar.expander("🛠️ ", expanded=False):
#     if st.checkbox("Preview memory store"):
#         with st.expander("Memory-Store", expanded=False):
#             st.session_state.entity_memory.store
#     if st.checkbox("Preview memory buffer"):
#         with st.expander("Buffer-Store", expanded=False):
#             st.session_state.entity_memory.buffer
#     MODEL = st.selectbox(label='Model', options=['gpt-3.5-turbo','gpt-4'])
#     K = st.number_input(' (#) Summary of prompts to consider', min_value=3, max_value=1000)

# # Set the title and description
# st.title("🤖 Chat Bot with 🧠")
# st.subheader(" Powered by 🦜 LangChain + OpenAI + Streamlit")


# # Check if API key is entered
# if API_O:
#     # Create a ChatOpenAI instance instead of OpenAI
#     llm = ChatOpenAI(
#         openai_api_key=API_O,  # Correct parameter for the API key
#         model=MODEL,  # Model selected by the user
#         temperature=0,  # Optional argument for controlling randomness
#         verbose=False  # Optional logging
#     )

#     # Create a ConversationEntityMemory object if not already created
#     if 'entity_memory' not in st.session_state:
#         st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=K)

#     # Create the ConversationChain object
#     Conversation = ConversationChain(
#         llm=llm, 
#         prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
#         memory=st.session_state.entity_memory
#     )
# else:
#     st.sidebar.warning('API key required to try this app. The API key is not stored in any form.')

# # Add a button to start a new chat
# st.sidebar.button("New Chat", on_click=new_chat, type='primary')

# # Get the user input
# user_input = get_text()

# # Generate output using the ConversationChain object
# if user_input:
#     output = Conversation.run(input=user_input)
#     st.session_state.past.append(user_input)
#     st.session_state.generated.append(output)

# # Display conversation history
# download_str = []
# with st.expander("Conversation", expanded=True):
#     for i in range(len(st.session_state['generated'])-1, -1, -1):
#         st.info(st.session_state["past"][i], icon="🧐")
#         st.success(st.session_state["generated"][i], icon="🤖")
#         download_str.append(st.session_state["past"][i])
#         download_str.append(st.session_state["generated"][i])

#     download_str = '\n'.join(download_str)
#     if download_str:
#         st.download_button('Download', download_str)

# # Display stored conversation sessions in the sidebar
# for i, sublist in enumerate(st.session_state.stored_session):
#     with st.sidebar.expander(label=f"Conversation-Session:{i}"):
#         st.write(sublist)

# # Clear all stored conversation sessions
# if st.session_state.stored_session:
#     if st.sidebar.checkbox("Clear-all"):
#         del st.session_state.stored_session
