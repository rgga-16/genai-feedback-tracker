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
            Based on the given text, create an array of conversations between the user and an assistant, where the assistant is an expert on interior design. 
            If the text contains irrelevant content like the table of contents, preface, index, or other things irrelevant to interior design please return an empty array.
            The conversations can vary, where the user can ask questions, seek clarification, ask for examples, or ask for suggestions. Be creative with the questions, where they should not necessarily be direct questions about the text.
            The assistant, in turn, should provide answers, explanations, examples, or suggestions based on the contents of the text.
            Also, the conversations should be distinct. 
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

def chat_completion_request(messages, tools=None, tool_choice=None, model="gpt-4o"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            temperature = 1.0,
            max_tokens=4096,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

textbooks = ["The Interior Design Reference & Specification Book.pdf", "Interior Design Illustrated.pdf"]

loader = PyPDFLoader("./finetuning/textbooks/The Interior Design Reference & Specification Book.pdf")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200,add_start_index=True)
pages = loader.load_and_split(text_splitter=text_splitter)

training_data = []

for page in tqdm(pages):
    messages = []
    messages.append({"role":"system","content":"Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
    messages.append({"role": "user", "content": f"Generate examples of conversations between you and the user about the content of this page below. The resulting conversation between the assistant and user should call convertToTrainingData. \n\n{page.page_content}"})
    chat_response = chat_completion_request(messages, tools=tools,tool_choice={"type":"function", "function": {"name": "convertToTrainingData"}},model="gpt-4o")
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
    if(len(training_data) > 0):
        with open("./finetuning/training_data.jsonl", "a") as f:
            for conversation in training_data:
                string = f"\"messages\": [{conversation}]"
                final_string = "{" + string + "}\n"
                f.write(final_string)





# with open("./finetuning/training_data.jsonl", "w") as f:
#     for conversation in training_data:
#         string = f"\"messages\": [{conversation}]"
#         final_string = "{" + string + "}\n"
#         f.write(final_string)


pass
    # print(len(page.page_content))


    # pass