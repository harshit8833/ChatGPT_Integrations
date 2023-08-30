import os
import streamlit as st
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent
from langchain.chat_models import ChatOpenAI
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor
from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
from langchain import LLMMathChain



st.set_page_config(page_title="Chat with multiple Integrations",page_icon=':bar_chart:')



def initialize_memory():
    """Initialize or return existing memory."""
    MEMORY_KEY = "chat_history"
    if 'memory' not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(memory_key=MEMORY_KEY, return_messages=True)
    return st.session_state.memory


# ...

def main():
    
    foot = f"""
    <div style="
        position: fixed;
        bottom: 0;
        right: 5px;
        padding: 0px;
        text-align: left;
    ">
        <p><a href='mailto:harshit09795@gmail.com'>Contact</a></p>
    </div>
    """


    st.markdown(foot, unsafe_allow_html=True)

    st.markdown(
    """
    <style>
        /* Hide main menu and footer */
        #MainMenu, footer {
            visibility: hidden;
        }

        /* Card styling */
        .css-card {
            border-radius: 10px; /* Rounded corners */
            padding: 30px 15px 15px 15px;
            background-color: #f8f9fa;
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.12), 0 2px 4px rgba(0, 0, 0, 0.08); /* Slight increase in shadow for depth */
            margin-bottom: 20px;
            font-family: "IBM Plex Sans", sans-serif;
            transition: transform 0.3s ease, box-shadow 0.3s ease; /* Smooth transition for hover effect */
        }
        
        /* Card hover effect */
        .css-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15), 0 3px 6px rgba(0, 0, 0, 0.10);
        }

        /* Card tag styling */
        .card-tag {
            border-radius: 3px; /* Slight rounded corners */
            padding: 4px 8px;
            margin-bottom: 10px;
            position: absolute;
            left: 10px; /* Some spacing from the left edge */
            top: 10px; /* Some spacing from the top edge */
            font-size: 0.7rem;
            font-family: "IBM Plex Sans", sans-serif;
            color: white;
            background-color: #27ae60; /* Slightly darker green */
            transition: background-color 0.3s ease; /* Smooth transition for hover effect */
        }

        /* Card tag hover effect */
        .card-tag:hover {
            background-color: #2ecc71; /* Slightly lighter green on hover */
        }
        
        .css-zt5igj {
            left: 0;
        }
        
        span.css-10trblm {
            margin-left: 0;
        }
        
        div.css-1kyxreq {
            margin-top: -40px;
        }
    </style>
        """,
        unsafe_allow_html=True,
)

    st.sidebar.image("img/logo1.png")
   

    st.write(
    f"""
    <div style="display: flex; align-items: center; margin-left: 0;">
        <h2 style="display: inline-block;">Chat with multiple Roles and Integrations</h2>
    </div>
    """,
    unsafe_allow_html=True,
        )
    
    st.write(
    f"""
    <div style="display: flex; align-items: center; margin-left: 0;">
        <h6 style="display: inline-block;">Welcome to our application, designed to answer your questions based on a selected role. To get started, please enter your OpenAI API key. Once your key is entered, you'll see a list of available integrations on the left sidebar. A few notable integrations include Google Search, which helps overcome ChatGPT's data limitation up to 2021 by providing current information, and a Calculator integration to assist the language model in performing calculations. Choose your desired role and tick the boxes next to the integrations you wish to use. Follow these steps to customize your experience and proceed within the application.</h6>
    </div>
    """,
    unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
        .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
        .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
        .viewerBadge_text__1JaDK {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    
    st.sidebar.title("Select Integrations")


    Assistants_type = st.sidebar.selectbox(
        "Choose Assistants", ["doctor", "teacher", "engineer", "farmer", "nurse", "scientist", "firefighter", "police officer", "soldier", "chef"])
    

    # Tool options
    tool_options = [
        {
            'name': "Search",
            'func': None,  # Placeholder, will initialize later
            'description': "Useful for answering questions about current events."
        },
        {
            'name': "Calculator",
            'func': None,  # Placeholder, will initialize later
            'description': "Useful for answering math questions."
        }
    ]

    if 'openai_api_key' not in st.session_state:
        openai_api_key = st.text_input(
            'Slide in your OpenAI API key! or [secure your free key here](https://platform.openai.com/account/api-keys)', value="", placeholder="Enter the OpenAI API key which begins with sk-")
        if openai_api_key:
            st.session_state.openai_api_key = openai_api_key
            os.environ["OPENAI_API_KEY"] = openai_api_key
        else:
            return
    else:
        os.environ["OPENAI_API_KEY"] = st.session_state.openai_api_key

    llm = ChatOpenAI(temperature=0)

    # Initialize an empty list to store selected tools
    selected_tools = []

    # sidebar to appear
    st.sidebar.header("Select Tools")
    
    for tool_option in tool_options:
        is_selected = st.sidebar.checkbox(f"{tool_option['name']} - {tool_option['description']}")
        if is_selected:
            # Initialize library instance and update the func attribute
            if tool_option['name'] == "Search":
                if 'serpapi_api_key' not in st.session_state:
                    serpapi_api_key = st.sidebar.text_input(
                        'Slide in your Google search API key! or [secure your free key here](https://serpapi.com/dashboard)',
                        value="",
                        placeholder="Enter the Google search API key"
                    )
                    if serpapi_api_key:
                        st.session_state.serpapi_api_key = serpapi_api_key
                        os.environ["SERPAPI_API_KEY"] = serpapi_api_key
                    else:
                        continue  # Skip to next iteration 

                else:
                    os.environ["SERPAPI_API_KEY"] = st.session_state.serpapi_api_key

                search = SerpAPIWrapper()
                tool_option['func'] = search.run
            elif tool_option['name'] == "Calculator":
                llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
                tool_option['func'] = llm_math_chain.run

            selected_tools.append(Tool(**tool_option))



    st.sidebar.markdown("Search - Free for 100 queries / month \n Calculator - Free")

    chosen_role = Assistants_type
    pp = f"You are a expert nice {chosen_role} chatbot having a conversation with a human. You are not a AI language model developed by OpenAI. Your purpose is to assist and provide helpful responses based on the input I receive as expert nice {chosen_role}"
    print(pp)
    system_message = SystemMessage(content=pp)

    MEMORY_KEY = "chat_history"
    prompt = OpenAIFunctionsAgent.create_prompt(
        system_message=system_message,
        extra_prompt_messages=[MessagesPlaceholder(variable_name=MEMORY_KEY)]
    )

    memory = initialize_memory()

    if not selected_tools:
        dummy_option = {
            'name': "DummyTool",
            'func': lambda: None,  # No-op function
            'description': "This tool does nothing."
        }
        
        selected_tools.append(Tool(**dummy_option))


    agent = OpenAIFunctionsAgent(llm=llm, tools=selected_tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=selected_tools, memory=memory, verbose=True)
    
    user_question = st.text_input("Enter your question:")
    if user_question:
        results = agent_executor.run(user_question)
        answer = results
        st.write("Answer:", answer)

    

if __name__ == "__main__":
    main()