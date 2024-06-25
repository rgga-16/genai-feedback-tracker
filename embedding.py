import openai
import re, codecs
import pandas as pd
from scipy import spatial 
import ast


EMBEDDING_MODEL = "text-embedding-3-small"

def extract_lines_from_srt_string(content, diarized=True):
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

def simplify_transript(transcript:str,diarized=True): 
    transcript_list = extract_lines_from_srt_string(transcript,diarized)
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
        relatedness_fn = lambda x,y: 1 - spatial.distance.cosine(x,y),
        top_n:int=10
    ):

    query_embedding_response = openai.embeddings.create(
        input=query,
        model=EMBEDDING_MODEL,
    )
    query_embedding = query_embedding_response.data[0].embedding
    strings_and_relatedness = []

    for i, row in df.iterrows():
        embedding = row["embedding"]
        if type(embedding)==str:
            embedding = ast.literal_eval(embedding)
        if type(embedding)==list and len(embedding)==1:
            embedding = embedding[0]
        relatedness = relatedness_fn(query_embedding, embedding)
        text= row["text"]
        strings_and_relatedness.append((text, relatedness))

    strings_and_relatedness.sort(key=lambda x: x[1], reverse=True)
    strings,relatednesses = zip(*strings_and_relatedness)

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