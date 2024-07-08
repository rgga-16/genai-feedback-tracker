from flask import Flask, send_from_directory, request, send_file, session
import os, shutil, subprocess, cv2, imagehash, ast
from PIL import Image
import time , base64, os, threading, json
from queue import Queue
import rag 


from datetime import datetime

from utils import makedir, emptydir
from transcribe import transcription_procedure, read_transcript
from embedding import *
from llms.chatgpt import *
from frame_extractor import extract_frames_by_timestamp
import time
import random

CWD = os.getcwd()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# log_queue = Queue()
# stop_log_thread = False

def log_writer():
    global log_queue, stop_log_thread
    while not stop_log_thread or not log_queue.empty():
        session_dir = os.path.join(CWD, "data", f"session_{session['session_id']}")
        if not os.path.exists(session_dir):
            os.makedirs(session_dir)
        log_file_path = os.path.join(session_dir, "action_logs.jsonl")
        with open(log_file_path, "a") as log_file:
            while not log_queue.empty():
                log_entry = log_queue.get()
                json.dump(log_entry, log_file)
                log_file.write('\n')
        time.sleep(1)  # Adjust based on the expected frequency of log entries

def start_log_thread():
    global log_thread
    log_thread = threading.Thread(target=log_writer, daemon=True)
    log_thread.start()

# Ensure to properly stop the log thread on application shutdown
def stop_log_writer():
    global stop_log_thread
    stop_log_thread = True
    log_thread.join()

# Path for our main Svelte page
@app.route("/")
def base():
    if 'session_id' not in session:
        session['session_id'] = random.randint(100000, 999999)
        print(f"Session ID: {session['session_id']}")
        start_time= time.time()
        session['session_dir'] = os.path.join(DATA_DIR, f"session_{session['session_id']}"); makedir(session['session_dir'])
        init_document_db_pickle_path = os.path.join(CWD,"finetuning", f"document_db.pickle")

        document_db = pd.read_pickle(init_document_db_pickle_path)

        titles = document_db['title'].unique().tolist()
        for title in titles:
            title_load_path = os.path.join(CWD, "finetuning", "documents", f"{title}.pdf")
            title_save_path = os.path.join(session['session_dir'], f"{title}.pdf")
            shutil.copy(title_load_path, title_save_path)
            
        if(type(document_db['embedding'][0]) == str):
            document_db['embedding'] = document_db['embedding'].apply(ast.literal_eval)
            print("parsing string to list")
        else:
            print("No need to parse string to list")
        
        session['document_db_path'] = os.path.join(session['session_dir'], "document_db.pickle")

        document_db.to_pickle(session['document_db_path'])
        print("Initial startup time: ", time.time()-start_time)

    return send_from_directory('client/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)

@app.route("/get_session_id", methods=["GET"])
def get_session_id():
    return {"session_id": session['session_id']}

@app.route("/get_documents", methods=["GET"])
def get_documents():
    document_db = pd.read_pickle(session['document_db_path'])

    titles = []
    if 'title' in document_db.columns:
        # Get unique titles
        titles = document_db['title'].unique()
        # Convert to list
        titles = titles.tolist()
    
    return {"documents": titles}


@app.route("/log_action", methods=["POST"])
def log_action(): 
    form_data = request.get_json()
    action= form_data["action"]
    data = form_data["data"]
    session_dir = os.path.join(DATA_DIR, f"session_{session['session_id']}"); makedir(session_dir)
    # log_queue.put({"action": action, "data": data})

    log_file_path = os.path.join(session_dir, "action_logs.jsonl")
    with open(log_file_path, "a") as log_file:
        log_entry = {action: data}
        json.dump(log_entry, log_file)
        log_file.write('\n')

    return {"message": f"Action {action} logged"}

@app.route("/increment_record_number", methods=["POST"])
def increment_record_number():
    # global RECORD_I
    # RECORD_I += 1
    return {"message": "Record number incremented"}

@app.route("/fetch_audio", methods=["POST"])
def fetch_audio(): 
    form_data = request.get_json()
    audio_path = form_data["audio_path"]
    _, file_ext = os.path.splitext(audio_path)
    return send_file(audio_path, mimetype=f"audio/{file_ext[1:]}")

@app.route("/fetch_video", methods=["POST"])
def fetch_video(): 
    form_data = request.get_json()
    video_path = form_data["path"]
    _, file_ext = os.path.splitext(video_path)
    # return send_file(video_path, mimetype=f"{type}/{file_ext[1:]}")
    return send_file(video_path, as_attachment=True)

@app.route("/download_screen",methods=["POST"])
def download_screen_recording():
    # global RECORD_I
    video = request.files["file"]
    if video:
        filename = "screen.webm"
        session_dir = os.path.join(DATA_DIR, f"session_{session['session_id']}"); makedir(session_dir); filepath = os.path.join(session_dir, filename); 
        # recording_dir = os.path.join(DATA_DIR, f"recording_{RECORD_I+1}");makedir(recording_dir);filepath = os.path.join(recording_dir, filename); 
        video.save(filepath) 
        return {"message": "Screen recording saved", "filepath": filepath}
    return {"message": "Screen recording not saved"}

@app.route("/transcribe_mic", methods=["POST"])
def transcribe_mic_recording():
    form_data = request.get_json()
    mic_path = form_data["audio"]
    transcript_path, transcript_with_timestamps_path = transcription_procedure(mic_path)
    transcript = read_transcript(transcript_with_timestamps_path)
    return {"message": "Transcription complete", 
            "transcript": transcript}

def save_file(file):
    # global RECORD_I 
    if file:
        filename = file.filename
        # recording_dir = os.path.join(DATA_DIR, f"recording_{RECORD_I+1}") ;makedir(recording_dir);filepath = os.path.join(recording_dir, filename)
        session_dir = os.path.join(DATA_DIR, f"session_{session['session_id']}"); makedir(session_dir); filepath = os.path.join(session_dir, filename); 
        file.save(filepath)
        return filepath
    return None

@app.route("/download_mic", methods=["POST"])
def download_mic_recording():
    # global RECORD_I 
    files = request.files
    if "audio" not in files:
        return "No audio part", 400
    audio = request.files["audio"]  
    if audio:
        filepath = save_file(audio)
        # filename = "mic.webm"
        # recording_dir = os.path.join(DATA_DIR, f"recording_{RECORD_I+1}") 
        # makedir(recording_dir)
        # filepath = os.path.join(recording_dir, filename); audio.save(filepath)
        return {"message": "Mic recording saved", "filepath": filepath}
    return {"message": "Mic recording not saved"}

@app.route("/simplify_transcript", methods=["POST"])
def simplify_transcript():
    form_data = request.get_json()
    transcript = form_data["transcript"]
    simplified_transcript = simplify_transript(transcript,diarized=False)
    return {"simplified_transcript": simplified_transcript}

@app.route("/transcript_to_list", methods=["POST"])
def transcript_to_list():
    form_data = request.get_json()
    transcript = form_data["transcript"]
    transcript_list = extract_lines_from_srt_string(transcript)

    return {"transcript_list": transcript_list}

@app.route("/embed_transcript", methods=["POST"])
def embed_transcript():

    form_data = request.get_json()
    transcript = form_data["transcript"]

    embeddings = []

    transcript_text = convert_to_srt_string(transcript)
    text_chunks = divide_into_chunks(transcript,max_chunk_size=256)

    for chunk in text_chunks:
        embeddings.extend(convert_to_embedding(chunk))
    
    transcript_db = pd.DataFrame({
        'text': text_chunks,
        'embedding': embeddings
    })
    

    if(type(transcript_db['embedding'][0]) == str):
        transcript_db['embedding'] = transcript_db['embedding'].apply(ast.literal_eval)
        print("parsing string to list")

    session_dir = os.path.join(DATA_DIR, f"session_{session['session_id']}"); makedir(session_dir)
    session['transcript_db_path'] = os.path.join(session_dir, "transcript.pickle")


    transcript_db.to_pickle(session['transcript_db_path'])
    return {"message": "Transcripts embedded"}



def convert_to_ms(timestamp):
    h, m, s = map(str, timestamp.split(':'))
    h = int(h)
    m = int(m)
    s, ms = map(int, s.split(','))
    return (h * 3600 + m * 60 + s) * 1000 + ms
    

@app.route("/extract_frames_per_timestamp", methods=["POST"])
def extract_frames_per_timestamp():
    form_data = request.get_json()
    video_path = form_data["video_path"]
    transcript = form_data["transcript"]

    timestamps = re.findall(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})', transcript)

    timestamps = [(convert_to_ms(start), convert_to_ms(end)) for start, end in timestamps]
    cap = cv2.VideoCapture(video_path)

    timestamp_frames = []

    start_time = time.time()
    for i, (start, end) in enumerate(timestamps):   
        timestamp=timestamps[i]
        intermediate_start = time.time()
        midpoint = (start + end) / 2
        cap.set(cv2.CAP_PROP_POS_MSEC, midpoint)
        success, image = cap.read()
        
        session_dir = os.path.join(DATA_DIR, f"session_{session['session_id']}"); makedir(session_dir)
        # recording_dir = os.path.join(DATA_DIR, f"recording_{RECORD_I+1}");makedir(recording_dir)

        
        if image is not None:
            # save_path = os.path.join(recording_dir,f"frame_{i+1}.png")
            save_path = os.path.join(session_dir,f"frame_{i+1}.png")
            timestamp_frames.append({midpoint:save_path})
            cv2.imwrite(save_path, image)
        else:
            print(f"Frame extraction failed. Frame {i+1}/{len(timestamps)} not saved.")
            timestamp_frames.append({midpoint:None})

        intermediate_end = time.time()
        print(f"Time taken to extract frame {i+1}/{len(timestamps)}: {intermediate_end - intermediate_start} seconds")
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
    cap.release()
    return {"timestamp_frames": timestamp_frames}

@app.route("/chatbot_init_message", methods=["POST"])
def get_initial_message():
    form_data = request.get_json()
    transcripts = form_data["transcripts"]
    initial_message = initial_query(transcripts) 
    return {"chatbot_init_message": initial_message}

@app.route("/message_chatbot", methods=["POST"])
def message_chatbot():
    start_query = time.time()
    form_data = request.get_json()
    message = form_data["message"]
    max_output_tokens = form_data.get("max_output_tokens", 256)
    temperature = form_data.get("temperature", 0.0)
    model = form_data.get("model", "gpt-4o")

    image_data = form_data.get("image_data", None)

    document_db = pd.read_pickle(session['document_db_path'])
    transcript_db = pd.read_pickle(session['transcript_db_path'])

    visual_response=None
    if(image_data):
        visual_history = [{"role":"system", "content":"You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. "}]
        visual_instruction = f"""
            Make a description of the image attached in 1-2 sentences. Next, with the context of the image, answer the query in 1-2 sentences.
            Query: {message}
        """
        visual_response = query(visual_instruction, model_name="gpt-4o", temp=0.0, max_output_tokens=256, message_history=visual_history, image=image_data)


    n_rows = transcript_db.shape[0]
    top_n = 5
    transcript_excerpts, relatednesses = strings_ranked_by_relatedness(
        message, 
        transcript_db,
        top_n=top_n
    )
    transcript_excerpts_string = "\n".join(transcript_excerpts)

    n_rows = document_db.shape[0]
    top_n = 5
    document_excerpts, relatednesses = strings_ranked_by_relatedness(
        message, 
        document_db,
        top_n=top_n
    )
    document_excerpts_string = "\n".join(document_excerpts)

    instruction = f"""
    Please provide a response to the following query.
    Query: {message}"""


    contexts = f"""
    Moreover, you can use following transcript excerpts and document excerpts as references to your answer, although you do not need to use them if they are not relevant to the query.
    Here are the top related transcript excerpts: 
    {transcript_excerpts_string}
    If your answer is based on a specific transcript excerpt, please mention the speaker and the timestamp of the excerpt, or the timestamp if there is no speaker mentioned.
    
    Here are the top related document excerpts:
    {document_excerpts_string}
    If your answer is based on a specific document excerpt, please mention the page number of the excerpt and the reference (e.g. book) name.

    If the query is not related to any of the transcripts or documents, answer the query as best as possible based on your own knowledge as an interior design expert.
    """

    visual_context = ""
    if visual_response:
        visual_context = f"\nMoreover, the user attached an image for visual context. Here is the reponse to the image: \n{visual_response}. \nYou may use this response as context and to help with your answer."

    last_instruction="\n\nTogether with the contexts retrieved, and the visual context (if any), please respond concisely the query. Please answer in 1-3 sentences at most."
    
    full_instruction = instruction + visual_context + contexts + last_instruction


    # response =  query(full_instruction, model_name="gpt-4o", temp=0.0, max_output_tokens=256, message_history=message_history)
    response =  query(full_instruction, model_name=model, temp=temperature, max_output_tokens=max_output_tokens, message_history=message_history)
    

    
    end_query = time.time()
    print(f"Time taken to query chatbot: {end_query - start_query} seconds")
    return {"chatbot_response": response}

@app.route("/autodetect_feedback", methods=["POST"])
def autodetect_feedback():
    form_data = request.get_json()

    transcript = form_data["transcript"]
    feedback_list = detect_feedback(transcript)

    return {"feedback_list": feedback_list}

@app.route("/positively_paraphrase_feedback",methods=["POST"])
def positively_paraphrase_feedback():
    form_data = request.get_json()
    feedback = form_data["feedback"]
    excerpt= form_data["excerpt"]
    paraphrased_feedback = positivise_feedback(feedback, excerpt)
    return {"paraphrased_feedback": paraphrased_feedback}


@app.route("/extract_audio_from_video", methods=["POST"])
def extract_audio_from_video():
    # global RECORD_I 
    if 'file' not in request.files:
        return 'No file sent', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.webm', '.wav', '.flv', '.wmv', '.mpeg', '.mpg', '.3gp', '.m4v','.aac')  # Add more video extensions if needed
    if file and file.filename.lower().endswith(video_extensions):
        videopath = save_file(file)
        videoext = videopath.split('.')[-1]
        audioext = 'mp3'
        audiopath = videopath.replace(videoext, audioext)
        subprocess.run(['ffmpeg','-y','-i',videopath,audiopath], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        if os.path.exists(audiopath):
            return {"message": "Audio extraction successful", "audiopath": audiopath, "videopath": videopath}
        else:
            return {"message":'Audio extraction failed'}
    else:
        return {"message":'Invalid file type'}

@app.route("/generate_task", methods=["POST"])
def generate_task():
    form_data = request.get_json()
    feedback = form_data["feedback"]
    excerpt= form_data["excerpt"]
    task = generate_task_from_feedback(feedback, excerpt)
    return {"task": task}

@app.route("/delete_document", methods=["POST"])
def delete_document(): 
    form_data = request.get_json()
    title = form_data["title"]

    document_db = pd.read_pickle(session['document_db_path'])
    document_db = document_db[document_db['title'] != title]
    document_db.to_pickle(session['document_db_path'])
    document_db.to_csv(session['document_db_path'].replace(".pickle", ".csv"))

    document_deleted = False
    for filename in os.listdir(session['session_dir']):
        if title in filename:
            file_path = os.path.join(session['session_dir'], filename)
            os.remove(file_path)  # Delete the file
            document_deleted = True
            break  # Assuming you want to delete only one document matching the title

    return {"document_name":title, "message": "Document removed successfully"}

@app.route("/add_document", methods=["POST"])
def add_document():
    files = request.files
    if 'file' not in request.files:
        return {"message": "No file sent"}, 400
    file = request.files['file']
    if file.filename == '':
        return {"message": "No selected file"}, 400
    
    if not file:
        return {"message": "No file sent"}, 400
    
    filepath = save_file(file); 
    title=file.filename.split('.')[0]

    texts = rag.load_document(filepath, remove_pages=[], extract_images=False)
    embeddings = rag.embed_document(texts)
    titles=[title]*len(texts)

    document_db = pd.read_pickle(session['document_db_path'])
    if document_db is None:
        document_db = pd.DataFrame({"text":texts, "embedding":embeddings, "title":titles})
    else:
        document_db = pd.concat([document_db, pd.DataFrame({"text":texts, "embedding":embeddings, "title":titles})])
    
    if(type(document_db['embedding'][0]) == str):
        document_db['embedding'] =document_db['embedding'].apply(ast.literal_eval)
    if(type(document_db['embedding'][0]) == list and len(document_db['embedding'][0])==1):
        document_db['embedding'] = document_db['embedding'].apply(lambda x: x[0])
    
    document_db.to_pickle(session['document_db_path'])

    return {"document_name":title, "message": "Document added successfully"}

if __name__ == "__main__":
    HISTORY_DIR = os.path.join(CWD, "data_history"); makedir(HISTORY_DIR)
    DATA_DIR = os.path.join(CWD, "data"); makedir(DATA_DIR)
    
    if os.path.exists(DATA_DIR) and os.listdir(DATA_DIR):
        src_dir = DATA_DIR
        current_date = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        dest_dir = os.path.join(HISTORY_DIR, f"[{current_date}]_data")
        shutil.copytree(src_dir, dest_dir) 
        emptydir(src_dir, delete_dirs=True)

        

    
    # start_log_thread(session['session_id'])
    
    app.run(debug=True)


