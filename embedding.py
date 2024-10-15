import openai
import re, codecs
import pandas as pd

import ast, time
import numpy as np

def cosine_similarity(a, b):
    a_np = np.array(a,dtype=np.float64)
    b_np = np.array(b,dtype=np.float64)
    cosine_similarity = np.dot(a_np, b_np) / (np.linalg.norm(a_np) * np.linalg.norm(b_np))

    return cosine_similarity


EMBEDDING_MODEL = "text-embedding-3-small"

def extract_lines_from_srt_string(content, diarized=False):
    result = []
    if diarized:
        pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?): (.+?)(?=\n\n\d+|\Z)', re.DOTALL)
        matches = pattern.findall(content)
        for match in matches:
            result.append({
                'id': int(match[0]),
                'start_timestamp': match[1],
                'end_timestamp': match[2],
                'speaker': match[3],
                'dialogue': match[4].replace('\n', ' ')
            })
    else:
        pattern = re.compile(r'(\d+)\s+(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\s+(.+?)\s+(?=\d+\s+\d{2}:\d{2}:\d{2},\d{3} -->|\Z)', re.DOTALL)
        matches = pattern.findall(content)
        for match in matches:
            result.append({
                'id': int(match[0]),
                'start_timestamp': match[1],
                'end_timestamp': match[2],
                'dialogue': match[3].replace('\n', ' ')
            })
    return result

def extract_lines_from_srt_file(file_path, diarized=True):
    result = []
    with codecs.open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    result = extract_lines_from_srt_string(content, diarized)
    f.close()
    return result

def simplify_transcript_list(transcript_list):
    simplified = []
    for excerpt in transcript_list:
        if simplified and simplified[-1]['speaker'] == excerpt['speaker']:
            # If the speaker is the same as the previous one, update the end timestamp and append the dialogue
            simplified[-1]['end_timestamp'] = excerpt['end_timestamp']
            simplified[-1]['dialogue'] += ' ' + excerpt['dialogue']
        else:
            # If the speaker is different, append the current dialogue to the result list
            simplified.append(excerpt)
    return simplified

def simplify_transript(transcript:str,diarized=False): 
    transcript_list = extract_lines_from_srt_string(transcript,diarized)
    simplifed_transcript_list=transcript_list

    if len(transcript_list) > 0 and transcript_list[0].get('speaker') is not None:
        simplifed_transcript_list = simplify_transcript_list(transcript_list)

    simplified_transcript =  convert_to_srt_string(simplifed_transcript_list)

    return simplified_transcript

def convert_to_srt_string(dialogues):
    srt_format = ''
    for i, dialogue in enumerate(dialogues, start=1):
        if "speaker" in dialogue:
            srt_format += f"{i}\n{dialogue['start_timestamp']} --> {dialogue['end_timestamp']}\n{dialogue['speaker']}: {dialogue['dialogue']}\n\n"
        else:
            srt_format += f"{i}\n{dialogue['start_timestamp']} --> {dialogue['end_timestamp']}\n{dialogue['dialogue']}\n\n"
    return srt_format[:-2] # Remove the last two newlines

def divide_into_chunks(dialogues,max_chunk_size=512):
    chunks = []
    chunk = ''
    for dialogue in dialogues:
        # Add the dialogue to the chunk
        if "speaker" in dialogue:
            string = f"{dialogue['start_timestamp']} --> {dialogue['end_timestamp']}\n{dialogue['speaker']}: {dialogue['dialogue']}\n"
        else:
            string = f"{dialogue['start_timestamp']} --> {dialogue['end_timestamp']}\n{dialogue['dialogue']}\n"
        
        new_chunk = chunk + string if chunk else string 

        #if the new chunk exceeds max chunk size, add the current chunk to the chunks list and start a new chunk
        if len(new_chunk) > max_chunk_size:
            chunks.append(chunk)
            chunk = string
        else:
            chunk = new_chunk
    # Add the last chunk if it's not empty
    if chunk:
        chunks.append(chunk)
    return chunks

def convert_to_embedding(text, model_name=EMBEDDING_MODEL):
    response = openai.embeddings.create(
        input=text,
        model=model_name
    )
    for i, be in enumerate(response.data):
        assert i == be.index # double check embeddings are in same order as input
    embedding = [be.embedding for be in response.data]
    return embedding

def strings_ranked_by_relatedness(
        query:str, 
        df:pd.DataFrame,
        relatedness_fn = cosine_similarity,
        top_n:int=10
    ):
    query=query.replace('\n',' ')
    df_clone=df.copy()

    start_time = time.time()
    query_embedding_response = openai.embeddings.create(
        input=query,
        model=EMBEDDING_MODEL,
    )
    query_embedding = query_embedding_response.data[0].embedding
    print(f"Time taken to calculate query embedding: {time.time()-start_time}")


    strings_and_relatedness = []
    start_time = time.time()
    # if(type(df_clone['embedding'][0]) == str):
    #     df_clone['embedding'] = df_clone['embedding'].apply(ast.literal_eval)
    #     print('parsing string to list')
    #     pass
    # if(type(df_clone['embedding'][0]) == list and len(df_clone['embedding'][0])==1):
    #     df_clone['embedding'] = df_clone['embedding'].apply(lambda x: x[0])
    #     print('converting list of list to list')
    #     pass
    print(f"Time taken to convert embeddings to list: {time.time()-start_time}")
    
    # Test speed
    start_time=time.time()
    df_clone['similarities'] = df_clone['embedding'].apply(lambda x: relatedness_fn(x,query_embedding))

    if 'title' in df_clone.columns:
        df_clone['text'] = df_clone['title'] + ': ' + df_clone['text']
    strings_and_relatedness = list(zip(df_clone['text'],df_clone['similarities']))

    strings_and_relatedness.sort(key=lambda x: x[1], reverse=True)
    print(f"Time taken to calculate similarities using vectorization: {time.time()-start_time}")

    # # Test speed
    # start_time=time.time()
    # strings_and_relatedness2 = [
    #     (row["text"], relatedness_fn(query_embedding, row["embedding"])) for i,row in df_clone.iterrows()
    # ]
    # strings_and_relatedness2.sort(key=lambda x: x[1], reverse=True)
    # print(f"Time taken to calculate similarities normally: {time.time()-start_time}")

    # strings_and_relatedness.sort(key=lambda x: x[1], reverse=True)
    start_time = time.time()
    strings,relatednesses = zip(*strings_and_relatedness)
    print(f"Time taken to unzip strings and relatednesses: {time.time()-start_time}")

    return strings[:top_n], relatednesses[:top_n]


if __name__ == '__main__':
    dialogues = extract_lines_from_srt_file('./sample_recording/whisper_diarization/audio1751904076.srt')
    simplified_dialogues = dialogues
    if "speaker" in dialogues[0]:
        simplified_dialogues = simplify_transcript_list(dialogues)
    srt = convert_to_srt_string(simplified_dialogues)

    text_chunks = divide_into_chunks("Transcript 1",simplified_dialogues)

    embeddings = []
    for chunk in text_chunks:
        embeddings.extend(convert_to_embedding(chunk))
    
    df = pd.DataFrame({
        'text': text_chunks,
        'embedding': embeddings
    })

    print(df.head())

    pass