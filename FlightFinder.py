from dotenv import load_dotenv
import os
from openai import OpenAI
import time
import json
import SerpAPI
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = API_KEY)
function_tools = [{
    "type": "function",
    "function": {
        "name": "search_flights",
        "description": "항공편 검색",
        "parameters": {
            "type": "object",
            "properties": {
                "departure_id" : {"type": "string", "description": "출발지 공항 코드 for examples ICN"},
                "arrival_id": {"type": "string", "description": "도착지 공항 코드 for examples NRT"},
                "outbound_date": {"type": "string", "description": "출발일 for examples 2024-01-20"},
                "return_date": {"type": "string", "description": "귀국일 for examples 2024-01-30"},
                "hl": {"type": "string", "description": "언어 for examples ko"},
                "currency": {"type": "string", "description": "통화단위, for examples KRW"},
                "outbound_times": {"type": "string", "description": "출국시 출발시간 for examples 0,23"},
                "return_times": {"type": "string", "description": "귀국시 출발시간 for examples 0,23"},
                "max_price": {"type": "string", "description": "최대 가격, for examples 0"}
            },
            "required" : ["departure_id", "arrival_id", "outbound_date"]
        }
    }
}]
#assistant 생성
assistants_id = "asst_PKvuiE7D3rQX9qPj2uPMLEAM"
def assistant_create():
    a = open('./FlightFinderInstructions.txt', 'r')
    assistant = client.beta.assistants.create(
        name="Flight Finder",
        instructions=a.read(),
        tools=function_tools,
        model="gpt-4-1106-preview"
    )
    return assistant
assistants = client.beta.assistants.list(
    order="desc",
    limit="20",
)
if not assistants.data:
    assistant = assistant_create()
else:
    assistant = assistants.data[0]

def run_check(thread_id):
    return run.status 
    
def wait_on_run(run):
    while run.status == "queued" or run.status == "in_progress":
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id,
            )
            
            time.sleep(0.5)    
    return run
# print(assistant)
    
#thread 생성
# thread = client.beta.threads.create()
# print(thread)
thread_id = "thread_QiN4bxeyIAlh0eraL7CL3CJ8"
run = client.beta.threads.runs.list(
    thread_id=thread_id
)
if (run.data[0].status == "queued" or run.data[0].status == "in_progress"):
    run = run.data[0]
    run = client.beta.threads.runs.cancel(
        thread_id=thread_id,
        run_id=run.id,
        )
def thread_message():
    thread_messages = client.beta.threads.messages.list(thread_id)
    return thread_messages

#msg_f7MmkNqk7FsgSeSaDMidMZDO
def startMessage(inputC):
    InputChat = inputC
    if InputChat:
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=InputChat
        )

        run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistants_id,
        )

        run = wait_on_run(run)

        if run.status == "requires_action":
            print(run.required_action.submit_tool_outputs.tool_calls)
            tool_call = run.required_action.submit_tool_outputs.tool_calls[0]
            arguments = json.loads(tool_call.function.arguments)
            print(arguments)
            task = SerpAPI.search_flights(**arguments)
            
            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=[
                    {
                        "tool_call_id": tool_call.id,
                        "output": str(task)
                    }
                ],
            )
            run = wait_on_run(run)
        messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )
        return messages.data[0].content[0].text.value