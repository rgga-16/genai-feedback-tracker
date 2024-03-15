from flask import Flask, send_from_directory, request, send_file
import os, shutil, subprocess, cv2, imagehash
from PIL import Image

from datetime import datetime

from utils import makedir, emptydir
from transcribe import transcription_procedure, read_transcript
from embedding import *
from chatgpt import *
from frame_extractor import extract_frames_by_timestamp
import time

CWD = os.getcwd()
RECORD_I = 0
TRANSCRIPT_DATABASE = None
DATA_DIR = os.path.join(CWD, "data"); makedir(DATA_DIR)

app = Flask(__name__)

# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('client/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)

@app.route("/increment_record_number", methods=["POST"])
def increment_record_number():
    global RECORD_I
    RECORD_I += 1
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
    global RECORD_I
    video = request.files["file"]
    if video:
        filename = "screen.webm"
        recording_dir = os.path.join(DATA_DIR, f"recording_{RECORD_I+1}")
        makedir(recording_dir)
        filepath = os.path.join(recording_dir, filename); 
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
    global RECORD_I 
    if file:
        filename = file.filename
        recording_dir = os.path.join(DATA_DIR, f"recording_{RECORD_I+1}") 
        makedir(recording_dir)
        filepath = os.path.join(recording_dir, filename); file.save(filepath)
        return filepath
    return None

@app.route("/download_mic", methods=["POST"])
def download_mic_recording():
    global RECORD_I 
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

@app.route("/embed_transcripts", methods=["POST"])
def embed_transcript():
    global TRANSCRIPT_DATABASE
    form_data = request.get_json()
    transcripts = form_data["transcripts"]
    for i in range(len(transcripts)):
        transcript = transcripts[i]
        dialogues = extract_lines_from_string(transcript)
        simplified_dialogues = dialogues
        if "speaker" in dialogues[0]:
            simplified_dialogues = simplify_dialogues(dialogues)
        srt = convert_to_srt_string(simplified_dialogues)
        text_chunks = divide_into_chunks(f"Transcript {i+1}",simplified_dialogues)
        embeddings = []
        for chunk in text_chunks:
            embeddings.extend(convert_to_embedding(chunk))
        if TRANSCRIPT_DATABASE is None:
            TRANSCRIPT_DATABASE = pd.DataFrame({
                'text': text_chunks,
                'embedding': embeddings
            })
        else:
            TRANSCRIPT_DATABASE = TRANSCRIPT_DATABASE.append(pd.DataFrame({
                'text': text_chunks,
                'embedding': embeddings
            }), ignore_index=True)
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
    timestamp_midpoints = [(int(round(start + end) / 2)) for start, end in timestamps]
    cap = cv2.VideoCapture(video_path)

    frames = []

    # BUG: Get the frames per second. But it's so slow!! How to make this better?
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    start_time = time.time()

    
    frames = extract_frames_by_timestamp(video_path, DATA_DIR, timestamp_midpoints, overwrite=False, every=25)

    # for i, (start, end) in enumerate(timestamps):   
    #     midpoint = (start + end) / 2
    #     cap.set(cv2.CAP_PROP_POS_MSEC, midpoint)
    #     success, image = cap.read()
    #     recording_dir = os.path.join(DATA_DIR, f"recording_{RECORD_I+1}") 
    #     makedir(recording_dir)
    #     frames.append({midpoint: image})
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
    cap.release()
    return {"frames": frames}

@app.route("/chatbot_init_message", methods=["POST"])
def get_initial_message():
    form_data = request.get_json()
    transcripts = form_data["transcripts"]
    initial_message = initial_query(transcripts) 
    return {"chatbot_init_message": initial_message}

@app.route("/message_chatbot", methods=["POST"])
def message_chatbot():
    form_data = request.get_json()
    user_query = form_data["message"]

    n_rows = TRANSCRIPT_DATABASE.shape[0]
    top_n = round(0.25*n_rows)

    strings, relatednesses = strings_ranked_by_relatedness(
        user_query, 
        TRANSCRIPT_DATABASE,
        top_n=top_n
    )

    transcript_instruction = "Use the following transcript excerpts as references to answer the subsequent query. If the query is not related to any of the transcripts, ignore this instruction, inform the user that the query is not related to the transcripts, and answer the query as best as possible."

    question = f"\n\n Query: {user_query}\n"
    message = f"{transcript_instruction}\nTranscript excerpts:\n"
    for string in strings:
        message += f"{string}\n"
    
    full_query = message + question

    response =  query(full_query)

    return {"chatbot_response": response}


@app.route("/extract_audio_from_video", methods=["POST"])
def extract_audio_from_video():
    global RECORD_I 
    if 'file' not in request.files:
        return 'No file sent', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.webm', '.wav', '.flv', '.wmv', '.mpeg', '.mpg', '.3gp', '.m4v')  # Add more video extensions if needed
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

if __name__ == "__main__":
    HISTORY_DIR = os.path.join(CWD, "data_history"); makedir(HISTORY_DIR)
    DATA_DIR = os.path.join(CWD, "data"); makedir(DATA_DIR)

    if os.path.exists(DATA_DIR) and os.listdir(DATA_DIR):
        src_dir = DATA_DIR
        current_date = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        dest_dir = os.path.join(HISTORY_DIR, f"[{current_date}]_data")
        shutil.copytree(src_dir, dest_dir) #BUG: does not work if using Windows. Reformat filenaming.
        # BUG: [WinError 123] The filename, directory name, or volume label syntax is incorrect: 
        # 'C:\\Users\\r-gal\\OneDrive\\Documents\\Academics\\PhD\\project-2\\data_history\\[14-03-2024 16:01:39] data'
        emptydir(src_dir, delete_dirs=True)

    
    app.run(debug=True)