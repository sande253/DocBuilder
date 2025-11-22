import asyncio
import uuid # For unique session IDs
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.agents.callback_context import CallbackContext

# --- OpenAPI Tool Imports ---
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
from google.adk.auth import AuthConfig, AuthCredential, AuthCredentialTypes, OAuth2Auth
from fastapi.openapi.models import OAuth2, OAuthFlows, OAuthFlowAuthorizationCode
from google.adk.auth.auth_credential import HttpAuth, HttpCredentials
import json
import hashlib
import base64
import os
import os, base64, hashlib, urllib.parse
from google.adk.auth import OpenIdConnectWithConfig

from google.genai import types

from typing import Tuple
from urllib.parse import urlparse, quote,unquote
import json

from services.converter import Handler
handler=Handler()
from google.adk.tools import FunctionTool
from dotenv import load_dotenv
import os

# Load variables from .env into os.environ
load_dotenv()
from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService # Optional
from google.adk.planners import BasePlanner, BuiltInPlanner, PlanReActPlanner
from google.adk.models import LlmRequest

from google.genai.types import ThinkingConfig
from google.genai.types import GenerateContentConfig

# auth_credential = AuthCredential(
#     auth_type=AuthCredentialTypes.OAUTH2,
#     oauth2=OAuth2Auth(
#         client_id=sharepoint_config.client_id, 
#         client_secret=sharepoint_config.client_secret, redirect_uri=sharepoint_config.redirect_url,
#         # scopes=sharepoint_config.scopes
#     ),
# )

# auth_scheme = OAuth2(
#         flows=OAuthFlows(
#             authorizationCode=OAuthFlowAuthorizationCode(
#                 authorizationUrl= sharepoint_config.auth_url,
#                 tokenUrl=sharepoint_config.token_url,
#                 scopes={
#                      "Sites.Read.All" : "reads all data"
#                 },
#             )
#         )
#     )




def temperature():
    return "25"
    
pre_process_link=FunctionTool(
    
    func=temperature
   
)


ACCESS_TOKEN = ""
def before_agent_callback(callback_context: CallbackContext):
    print(f"\n{'*'*60}\n{'*'*60}\n\nservice_now CALLBACK_CONTEXT [STATE] (Before agent):\n{callback_context._invocation_context.session.state}\n\n{'*'*60}\n{'*'*60}\n")
    tools = [pre_process_link]
    if callback_context._invocation_context.session.state:
        state = callback_context._invocation_context.session.state.copy()
        print(f"state : {state} \n")
        for key, value in state.items():  
            if 'temp:sharepoint' in key:
                print(f"\n{'*'*60}\nUPDATED [SERVICE NOW] ACCESS TOKEN STATE:\n{value}\n{'*'*60}\n")
                auth_credential = AuthCredential(
                    auth_type=AuthCredentialTypes.HTTP,
                    http=HttpAuth(
                        scheme="bearer",
                        credentials=HttpCredentials(
                            token=value,)
                    ),
                )
               
                tools = [pre_process_link]
                print("REINITIALIZED SERVICENOW TOOLS SUCCESSFULLY")
            else:
                print("INITIALIZED SERVICENOW TOOLS FOR FIRST TIME") 
                callback_context._invocation_context.session.state['temp:sharepoint']= ACCESS_TOKEN

                # print(f"\n{'*'*60}\nUPDATED [SERVICE NOW] ACCESS TOKEN STATE:\n{value}\n{'*'*60}\n")

        callback_context._invocation_context.agent.tools= tools






# --- Agent Definition ---
root_agent = Agent(
    
    name="Dochandler",
    model="gemini-2.5-flash",
    tools=handler.get_all_tools(), # Pass the list of RestApiTool objects
    global_instruction=f"""YOU ARE A DOCUMENT GENERATOR AGENT.  
YOUR MAIN GOAL IS TO GENERATE TEXT AND HELP THE USER CREATE WELL-FORMATTED DOCUMENTS.  
ASK VERY FEW QUESTIONS TO THE USER — BE PROACTIVE AND SELF-SUFFICIENT.

### TOOLS (Functions)
- create_new_document(text: str): Create a new document from the provided text. Returns a session_id.
- update_document(session_id: str, new_text: str): Update the existing document with new or modified text.
- get_document(session_id: str): Retrieve the current document and its LaTeX code.
- compile_to_pdf(session_id: str): Compile the document’s LaTeX code into a PDF.
-generate_statistical_chart(text:str): You can use the tool for generating graphs from statistical text it returns full image path , make sure to pass it during document creation and updation
-generate_video_from_text(prompt:str) : Define what the user want clearly and allobrate  , it will return a url , render in markdown fromat [name](url)
### RULES:
1. When creating a document for the first time, **always** use the tool `create_new_document(text)` — it returns a **session_id**.
2. The **returned session_id** must be reused automatically for all subsequent operations.  
   - Never ask the user to provide the session_id manually.
3. Always use `get_document(session_id)` to retrieve the latest context or existing content before making edits or updates.
4. Never pass raw LaTeX code as input to any tool — always work with human-readable text.
5. After **every tool call**, always run the tool `compile_to_pdf(session_id)` to ensure the latest content is compiled.
6. Maintain minimal conversation — focus on helping the user generate and update their document efficiently.
7 . Always display the url in Markdown format [name](url)


##TIPS :
Title & Headings — Clearly indicate what the document is about.
Sections/Subsections — Logical division of content (e.g., Introduction, Methods, Results, Conclusion).
Paragraph Flow — Smooth transitions; each paragraph should have one key idea.
Formatting Consistency — Font, spacing, margins, bullet styles, etc.

### EXAMPLES (Behavioral)
- If the user says “create a new report,” use `create_new_document("report content...")`.
- If the user modifies or adds text, use `update_document(session_id, "updated text...")` followed by `compile_to_pdf(session_id)`.
- If the user asks to see what’s written, use `get_document(session_id)`.

YOUR ROLE:  
Act as an intelligent writing assistant that handles document text, keeps track of session automatically, and ensures each change is compiled into a ready-to-view PDF.
 """, 
    generate_content_config=types.GenerateContentConfig(
                temperature=0.7,
          ),
    before_agent_callback=before_agent_callback
)

APP_NAME = "agents"  # must match the directory name that contains your agent.py
USER_ID = "1234"
SESSION_ID = "session1234d"

session_service = InMemorySessionService()

# Use asyncio.run() to execute the async session creation**
session_service = InMemorySessionService()

# Use asyncio.run() to execute the async session creation**
session = asyncio.run(session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID
))

print(session)
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

def call_agent(query):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    
    for event in events:
        print(f"Content: {event.content}")
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("Agent Response: ", final_response)

    return final_response

#call_agent("create a divorce document between sandeep and sathvik ")