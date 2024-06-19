
from openai import OpenAI  #If first time using this repo, set the environment variable "OPENAI_API_KEY", to your API key from OPENAI
import tiktoken, ast, re


client = OpenAI()
model_name = "gpt-4o"
max_tokens=128000
max_output_tokens=4095
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
    elif model == "gpt-4" or model=="gpt-4o":
        print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    elif model.startswith("ft:"):
        print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
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

def check_and_trim_message_history(message_history, model_name=model_name, max_tokens=max_tokens):
    offset=300

    if num_tokens_from_messages(message_history, model=model_name) > max_tokens:
        print("Current number of tokens in message history exceeds the maximum number of tokens allowed. Trimming message history.")
        while num_tokens_from_messages(message_history, model=model_name) > max_tokens - offset:
            del message_history[1] # Delete the 2nd message in the history. The first message is always the system prompt, which should not be deleted.

def query(query,role="user", model_name=model_name, temp=temperature, max_output_tokens=max_output_tokens, message_history=message_history):

    # Retrieve n embeddings 
    message_history.append({"role":role, "content":query})
    check_and_trim_message_history(message_history, model_name)

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=message_history,
            temperature=temp,
            max_tokens=max_output_tokens 
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

def detect_feedback(transcript):
    feedback_list =[]
    system_prompt = """
        You are an expert documentor with experience in analyzing transcripts of conversations in SRT format.
        You are tasked to determine if the following transcript or excerpt of a transcript contains positive feedback, critical feedback, or no feedback, based on the context of the discussion.
        If the transcript contains positive or critical feedback, quote which part of the transcript is the feedback.

        Positive feedback includes comments that are supportive, encouraging, or complimentary.
        Critical feedback includes comments that are constructive, evaluative, suggest areas for improvement, or are even harsh.
        
        Then, you have to also track the corresponding ID of the dialogue that contains the feedback, as well as the speaker's name who provided the feedback.
        Lastly, you have to respond in the form of a Python list of dictionaries with the following format:

        [{'type': 'positive'/'critical', 'quote': '<QUOTE>', 'dialogue_id':'<ID>', 'speaker': '<SPEAKER NAME>'}, ...]

        If there is no feedback detected, return an empty list.

        Here is an example, given an input transcript:
        Input transcript:
        4 
        00:00:30,000 --> 00:00:40,000 
        Sarah: I used reclaimed wood for the flooring and bamboo for the furniture. The idea was to create a warm, inviting atmosphere while being eco-friendly. 
        5 
        00:00:40,000 --> 00:00:50,000 
        Student 1: The use of bamboo is interesting. It reminds me of some modern Japanese interiors I've seen. 
        6 
        00:00:50,000 --> 00:01:00,000 
        Professor: Yes, I see that influence. But I think the space could benefit from more contrast. Right now, it feels a bit too uniform. 
        7 
        00:01:00,000 --> 00:01:10,000 
        Guest Professional 2: I agree. Maybe you could introduce some darker elements to create depth and dimension. What do you think about that? 


        You have to respond with the following output:
        [{'type': 'positive', 'quote': 'The use of bamboo is interesting. It reminds me of some modern Japanese interiors I've seen.', 'dialogue_id': '5', 'speaker': 'Student 1'}, 
        {'type': 'critical', 'quote': 'But I think the space could benefit from more contrast. Right now, it feels a bit too uniform.', 'dialogue_id': '6', 'speaker': 'Professor'},
        {'type': 'critical', 'quote': 'I agree. Maybe you could introduce some darker elements to create depth and dimension. What do you think about that?', 'dialogue_id': '7', 'speaker': 'Guest Professional 2'}], 
    """
    message_history = [{"role":"system", "content":system_prompt}]

    if(num_tokens_from_messages(message_history) > max_tokens):
        print("Warning: Number of tokens in message history exceeds the maximum number of tokens allowed.")
        return [{"type": "error", "quote": f"Number of tokens in message history exceeds the maximum number of tokens allowed."}]

    prompt=f"""
    {transcript}
    """
    
    response = query(prompt, message_history=message_history, max_output_tokens= max_output_tokens, temp=0.0)
    # Remove any unneeded characters before the [ and after the ] in response
    response =  re.sub(r'^.*?(\[.*\]).*$', r'\1', response, flags=re.DOTALL)
    # print(f"Response: {response}")
    try:
        feedback_list = ast.literal_eval(response)
        # print(f"Feedback detected: {feedback_list}")
        
        
        feedback_list = [{**feedback, 'id': i+1} for i, feedback in enumerate(feedback_list)] # Add a 'id' key to each feedback item to track the index of the feedback item.
        feedback_list = [{**feedback,'chatbot_messages': [{"role":"system", "content":"You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. "}]} for feedback in feedback_list] # Add a 'messages' key to each feedback item to store the messages associated with it
        feedback_list = [{**feedback, 'done': False} for feedback in feedback_list] # Add a 'done' key to each feedback item to track if it has been addressed
        feedback_list = [{'type': feedback['type'], 'quote': feedback['quote'], 'dialogue_id': int(feedback['dialogue_id']), 'speaker': feedback['speaker'], 'done': feedback['done']} for feedback in feedback_list] # Convert dialogue_id to int
        feedback_list = [{**feedback,'task':None} for feedback in feedback_list] # Add a 'task' key to each feedback item to store the task associated with it
        feedback_list = [{**feedback,'show_paraphrased':False} for feedback in feedback_list] # Add a 'show_paraphrased' key to each feedback item to track if the paraphrased feedback is shown or not.
        pass
    except Exception as e:
        print(f"Error: {e}")
        feedback_list = []
    return feedback_list

def positivise_feedback(quote, excerpt): 
    system_prompt="""
        Given a feedback quote, you are tasked to paraphrase the provided feedback quote to make it more positive and constructive.
        You will also be given an excerpt from the conversation where the feedback was provided for context.
        Your goal is to rephrase the feedback in a way that maintains the essence of the original feedback but presents it in a more positive and encouraging manner.
        If you think the feedback is already positive and constructive, but long, you can simply rephrase it to make it shorter.
        If the feedback is already positive, constructive, and short, you can simply leave it as is.
        Respond with the rephrased feedback quote only.
    """

    message_history = [{"role":"system", "content":system_prompt}]

    prompt=f"""
    Feedback Quote: {quote}
    Excerpt: {excerpt}
    """

    positive_quote = query(prompt, message_history=message_history, max_output_tokens= max_output_tokens, temp=0.7)
    return positive_quote

def generate_task_from_feedback(feedback_quote, excerpt):
    system_prompt="""
        Given a feedback quote, you are tasked to generate a task based on the feedback provided.
        You will also be given an excerpt from the conversation where the feedback was provided for context.
        The task should be actionable, specific, related to the feedback given, and should be 1 sentence as much as possible.

        Respond with the rephrased feedback quote only.
    """

    message_history = [{"role":"system", "content":system_prompt}]

    prompt=f"""
    Feedback Quote: {feedback_quote}
    Excerpt: {excerpt}
    """

    task = query(prompt, message_history=message_history, max_output_tokens= max_output_tokens, temp=0.7)

    return task

if __name__ == "__main__":
    message_history = [{"role":"system", "content":"You are a helpful assistant."}]
    while(True):
        message = input("User: ")
        response = query(message,model_name="ft:gpt-3.5-turbo-0125:personal:int-des:9Zfe0znW",temp=1.0)
        print(f"Assistant: {response}")

    print()

