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
    global_instruction="YOUR A DOCUMENT GENERATOR ", 
    generate_content_config=types.GenerateContentConfig(
                temperature=0,
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

call_agent("create a divorce document between sandeep and sathvik ")