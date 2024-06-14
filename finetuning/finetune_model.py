from openai import OpenAI  #If first time using this repo, set the environment variable "OPENAI_API_KEY", to your API key from OPENAI
import tiktoken, ast, re



base_model = "gpt-3.5-turbo"



if __name__ == "__main__":
    client = OpenAI()
    # file_response = client.files.create (
    #     file= open("./finetuning/cleaned/The Interior Design Reference & Specification Book/train.jsonl","rb"),
    #     purpose="fine-tune"
    # )
    # file_id = file_response.id

    # client.fine_tuning.jobs.create(
    #     training_file=file_id,
    #     model=base_model,
    #     seed=42,
    #     suffix="int-des",
    # )
    fine_tune_jobs = client.fine_tuning.jobs.list()
    print(fine_tune_jobs)
    