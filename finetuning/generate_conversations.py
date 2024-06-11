from openai import OpenAI  #If first time using this repo, set the environment variable "OPENAI_API_KEY", to your API key from OPENAI
import tiktoken, ast, re
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain import hub
from tqdm import tqdm

client = OpenAI()
FINETUNE_MODEL="gpt-3.5-turbo"

tools = [
    {
        "type": "function",
        "function": {
            "name": "convertToTrainingData",
            "description": """
            Based on the given text, create an array of conversations between the user and an assistant, where the assistant is an expert on interior design, and the user is a practicing interior design student. 
            Pretend the user is working on a interior design project. Thus, the user should ask questions related to their project like "What is the best way to do X?" or "How do I do Y?".
            The assistant should provide explanations, examples, and clarifications to these questions by referring to the text. Furthermore, these answers should be short and concise.
            Be creative and generate a variety of questions and answers.
            If the text contains irrelevant content like table of contents, index, acknowledgements, etc., return an empty array. 
            """, 
            "parameters": {
                "type": "object",
                "properties": {
                    "conversations": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "role": {
                                        "type": "string",
                                        "enum": ["user", "assistant"],
                                        "description": "The name of the role that's currently responding.",
                                    },
                                    "content": {
                                        "type": "string",
                                        "description": "The message content.",
                                    },
                                },
                                "required": ["role", "content"],
                            },
                        },
                    },
                },
                "required": ["conversations"],
            }
        }
    }
]

def chat_completion_request(messages, tools=None, tool_choice=None, model="gpt-4o", temperature=1.0, max_tokens=4096):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            temperature = temperature,
            max_tokens=max_tokens,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

textbooks = ["The Interior Design Reference & Specification Book.pdf", "Interior Design Illustrated.pdf"]

loader = PyPDFLoader("./finetuning/textbooks/Interior Design Illustrated.pdf")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=800,add_start_index=True)
pages = loader.load_and_split(text_splitter=text_splitter)

training_data = []

last_page=0
n_conversations=5
for i in tqdm(range(len(pages))):
    page = pages[i]
    messages = []
    messages.append({"role":"system","content":"Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
    messages.append({"role": "user", "content": f"""
                    Generate {n_conversations} well-crafted examples of conversations between you and the user, where you can refer to the content of this text below. 
                    You are an assistant who is an expert on interior design, and the user is a practicing interior design student. 
                    Pretend the user is working on a interior design project, and the project is a work-in-progress. Furthermore, the project has also been receiving feedback from teachers on how to improve it. Thus the user should ask questions related to their project like "What is the best way to do W?", "How do I do X?", "What are some examples of Y?", or "My teacher gave this feedback Z. Based on the feedback I received, how can I improve my project?".
                    The assistant should provide answers like explanations, examples, and clarifications to these questions by referring to the text. Furthermore, these answers should be short and concise.
                    Be creative and generate a variety of questions and answers.
                    The conversation should have at least 2 exchanges between the user and assistant. Feel free to generate more than 2 exchanges in a conversation.
                    If the text contains irrelevant content like table of contents, index, acknowledgements, etc., return an empty array. 
                    The resulting conversation between the assistant and user should call convertToTrainingData. \n\n
                    Text:
                    {page.page_content}"""})
    chat_response = chat_completion_request(messages, tools=tools,tool_choice={"type":"function", "function": {"name": "convertToTrainingData"}},model="gpt-4o",temperature=1.0)
    response_message = chat_response.choices[0].message
    tool_calls = response_message.tool_calls
    try:
        conversations_response = tool_calls[0].function.arguments
        conversations = ast.literal_eval(conversations_response)["conversations"]
    except Exception as e:
        print(f"Unable to extract conversations from response_message: {conversations_response}")
        print(f"Error: {e}")
        conversations = []
    training_data.extend(conversations)

    # Write the training_data as a .jsonl file. If the file exists, simply append to it.
    if(i % (len(pages)//4) == 0 and i != 0 or i == len(pages)-1):
        with open(f"./finetuning/train_page_{last_page}to{i}.jsonl", "a") as f:
            for conversation in training_data:
                string = f"\"messages\": [{conversation}]"
                final_string = "{" + string + "}\n"
                f.write(final_string)
            print(f"Saving training data for pages {last_page} to {i} to file: train_page_{last_page}to{i}.jsonl")
        last_page = i
        training_data = []




pass