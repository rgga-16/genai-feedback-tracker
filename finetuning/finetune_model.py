from openai import OpenAI  #If first time using this repo, set the environment variable "OPENAI_API_KEY", to your API key from OPENAI
import tiktoken, ast, re
from io import BytesIO
import base64


base_model = "gpt-3.5-turbo"



if __name__ == "__main__":
    client = OpenAI()

    # file_response = client.files.create ( # Add train file to fine-tune
    #     file= open("./finetuning/dataset/train.jsonl","rb"),
    #     purpose="fine-tune"
    # )
    # train_id = file_response.id

    # file_response = client.files.create ( # Add train file to fine-tune
    #     file= open("./finetuning/dataset/val.jsonl","rb"),
    #     purpose="fine-tune"
    # )
    # val_id = file_response.id

    # print(client.files.list()) # List files

    # print(client.files.delete('file-8mnlB1V74D3LnZyy7ieluN2P')) #Delete a file

    # client.fine_tuning.jobs.create( # Create fine-tuning job
    #     training_file=train_id,
    #     validation_file=val_id,
    #     model=base_model,
    #     seed=42,
    #     suffix="int-des-full",
    # )

    ft_job = client.files.retrieve('file-hLo4A6kuPVM3QLCrBSR0IA9m') # Get fine-tuning job content and metrics
    ft_job_content = client.files.content(ft_job.id).content
    ft_metrics = base64.b64decode(ft_job_content)
    
    # print(client.fine_tuning.jobs.list(limit=1)) # List fine-tuning jobs

    # ft_job = client.fine_tuning.jobs.list_events(fine_tuning_job_id='ftjob-5qsMbjYYWqMAEgF9wuKBFZ9N') # Get fine-tuning job events
    pass
    