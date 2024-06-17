from openai import OpenAI  #If first time using this repo, set the environment variable "OPENAI_API_KEY", to your API key from OPENAI
import tiktoken, ast, re

# Code borrowed from https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
def num_tokens_from_messages(messages, model):
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

def check_and_trim_message_history(message_history, model_name, max_tokens):
    offset=300

    if num_tokens_from_messages(message_history, model=model_name) > max_tokens:
        print("Current number of tokens in message history exceeds the maximum number of tokens allowed. Trimming message history.")
        while num_tokens_from_messages(message_history, model=model_name) > max_tokens - offset:
            del message_history[1] # Delete the 2nd message in the history. The first message is always the system prompt, which should not be deleted.

def query(query, model_name, temp, max_output_tokens, message_history,role="user"):

    # Retrieve n embeddings 
    message_history.append({"role":role, "content":query})
    check_and_trim_message_history(message_history, model_name, max_tokens)

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


finetuned_model = "ft:gpt-3.5-turbo-0125:im-lab:int-des:9ZuJ98O6"
max_tokens=16000

if __name__ == "__main__":
    client = OpenAI()

    message_history = [{"role":"system", "content":"You are a helpful assistant."}]
    while(True):
        message = input("User: ")
        response = query(message,model_name=finetuned_model,temp=1.0,max_output_tokens=256,message_history=message_history,role="user")
        print(f"Assistant: {response}")

    print()