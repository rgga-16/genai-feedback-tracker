
from openai import OpenAI  #If first time using this repo, set the environment variable "OPENAI_API_KEY", to your API key from OPENAI
import tiktoken


client = OpenAI()
model_name = "gpt-4-1106-preview"
max_tokens=100000
encoding = tiktoken.get_encoding("cl100k_base")

temperature=0.0

system_prompt = """
Act like an expert documentor with experience in retrieving discussion points from a conversation.
You will be provided with one or more transcripts of conversations among people like between a client and a designer, a senior designer and a junior designer, a design teacher and a design student, among a group of designers, or even within a designer talking to himself.
The transcripts may or may not contain the names of the people involved in the conversation. 
So, it is up to you to know who is talking to whom and what is the context of the conversation.

Your goal is to provide responses to the user's queries, comments, or questions by referring to the provided transcripts. 
You can also ask questions to the user to get more information about the context or the user's needs. 
You can also provide suggestions, feedback, or advice to the user based on the context of the conversation.
"""

message_history = [{"role":"system", "content":system_prompt}]



# Code borrowed from https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
def num_tokens_from_messages(messages, model=model_name):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo" or model=="gpt-3.5-turbo-16k":
        print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

def check_and_trim_message_history():
    offset=300
    global message_history
    global max_tokens
    global model_name 

    model_name_ = model_name
    if(model_name=="gpt-4-1106-preview"):
        model_name_="gpt-4"

    if num_tokens_from_messages(message_history, model=model_name_) > max_tokens:
        print("Current number of tokens in message history exceeds the maximum number of tokens allowed. Trimming message history.")
        while num_tokens_from_messages(message_history, model=model_name_) > max_tokens - offset:
            del message_history[1] # Delete the 2nd message in the history. The first message is always the system prompt, which should not be deleted.

def query(query,role="user", temp=temperature):
    global message_history

    # Retrieve n embeddings 
    

    message_history.append({"role":role, "content":query})
    check_and_trim_message_history()

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=message_history,
            temperature=temp
        )
        response_msg = response.choices[0].message.content
        message_history.append({"role":response.choices[0].message.role, "content":response_msg})
    except Exception as e:
        response_msg = f"Error: {e}"
    return response_msg

def initial_query(transcripts):
    transcripts_str = '\n'.join(transcripts) + '\n====================================================================================================\n'
    
    initial_prompt = f"""
    First, briefly introduce yourself.
    Next, based on the following transcripts provided, can you retrieve and provide potential to-do tasks, problems, insights, and important reminders raised?

    Transcripts: \n{transcripts_str}

    \n

    Lastly, answer with the tasks, problems, insights, and important reminders raised, as well as their respective timestamps. 
    Make sure that you describe the tasks, problems, and important reminders in a clear and concise manner.
    You can use the following format:

    [Introduction]

    Tasks:
    - Task 1: [Task description] (Timestamp: [Timestamp])
    ...
    - Task n: [Task description] (Timestamp: [Timestamp])

    Problems:
    - Problem 1: [Problem description] (Timestamp: [Timestamp])
    ...
    - Problem n: [Problem description] (Timestamp: [Timestamp])

    Important Reminders:
    - Reminder 1: [Reminder description] (Timestamp: [Timestamp])
    ...
    - Reminder n: [Reminder description] (Timestamp: [Timestamp])

    
    """

    initial_response = query(initial_prompt)
    return initial_response

def init():

    return 


if __name__ == "__main__":
    # response = query(initial_prompt)
    # print(response)
    print()

