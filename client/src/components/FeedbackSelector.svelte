<script>
    export let recording;
    export let feedback_list;

    let transcript_str;

    let is_recording=false;
    let is_paused=false;

    let videoStream;
    let micStream;
    let settings;

    let micBlobs=[];
    let videoChunks = [];

    let videoRecorder;
    let micRecorder;

    let videoPath;
    let micPath; 

    let files, file_input;
    let is_loading=false;
    let file_load_progress=0; 
    let file_load_status = "";

    let premade_transcript_list = [
    {
        start_timestamp: "00:00:00,000",
        end_timestamp: "00:00:10,000",
        speaker: "Professor",
        dialogue: "Alright, let's start with Sarah's 3D rendering. Sarah, could you give us a brief overview of your design concept?"
    },
    {
        start_timestamp: "00:00:10,000",
        end_timestamp: "00:00:20,000",
        speaker: "Sarah",
        dialogue: "Sure, my concept is based on creating a serene and airy living space that maximizes natural light and uses sustainable materials."
    },
    {
        start_timestamp: "00:00:20,000",
        end_timestamp: "00:00:30,000",
        speaker: "Guest Professional 1",
        dialogue: "I appreciate the focus on sustainability. Can you tell us more about the materials you chose and why?"
    },
    {
        start_timestamp: "00:00:30,000",
        end_timestamp: "00:00:40,000",
        speaker: "Sarah",
        dialogue: "I used reclaimed wood for the flooring and bamboo for the furniture. The idea was to create a warm, inviting atmosphere while being eco-friendly."
    },
    {
        start_timestamp: "00:00:40,000",
        end_timestamp: "00:00:50,000",
        speaker: "Student 1",
        dialogue: "The use of bamboo is interesting. It reminds me of some modern Japanese interiors I've seen."
    },
    {
        start_timestamp: "00:00:50,000",
        end_timestamp: "00:01:00,000",
        speaker: "Professor",
        dialogue: "Yes, I see that influence. But I think the space could benefit from more contrast. Right now, it feels a bit too uniform."
    },
    {
        start_timestamp: "00:01:00,000",
        end_timestamp: "00:01:10,000",
        speaker: "Guest Professional 2",
        dialogue: "I agree. Maybe you could introduce some darker elements to create depth and dimension. What do you think about that?"
    },
    {
        start_timestamp: "00:01:10,000",
        end_timestamp: "00:01:20,000",
        speaker: "Sarah",
        dialogue: "That's a good point. I was worried about making it too dark, but I see how it could add more interest."
    },
    {
        start_timestamp: "00:01:20,000",
        end_timestamp: "00:01:30,000",
        speaker: "Student 2",
        dialogue: "I think the lighting is really well done. It gives a very airy feel to the space."
    },
    {
        start_timestamp: "00:01:30,000",
        end_timestamp: "00:01:40,000",
        speaker: "Professor",
        dialogue: "Yes, the lighting is a strong point. But I would suggest rethinking the placement of the windows. They seem a bit too high."
    },
    {
        start_timestamp: "00:01:40,000",
        end_timestamp: "00:01:50,000",
        speaker: "Guest Professional 1",
        dialogue: "And I would definitely take away the coloring. I think it’s not working for the intent that you want and that you could just use blue Styrofoam."
    },
    {
        start_timestamp: "00:01:50,000",
        end_timestamp: "00:02:00,000",
        speaker: "Sarah",
        dialogue: "I see. I was trying to create a gradient effect, but maybe it's not coming through as I intended."
    },
    {
        start_timestamp: "00:02:00,000",
        end_timestamp: "00:02:10,000",
        speaker: "Student 3",
        dialogue: "It reminds me of a Scandinavian design, very minimalistic and clean."
    },
    {
        start_timestamp: "00:02:10,000",
        end_timestamp: "00:02:20,000",
        speaker: "Guest Professional 2",
        dialogue: "Yes, but Scandinavian designs often have a pop of color or a statement piece. Maybe you could incorporate something like that?"
    },
    {
        start_timestamp: "00:02:20,000",
        end_timestamp: "00:02:30,000",
        speaker: "Professor",
        dialogue: "Good suggestion. Also, consider the long-term vision. How will this space age over time? Will it still feel fresh and inviting?"
    },
    {
        start_timestamp: "00:02:30,000",
        end_timestamp: "00:02:40,000",
        speaker: "Sarah",
        dialogue: "That's a great point. I hadn't thought about the aging aspect."
    },
    {
        start_timestamp: "00:02:40,000",
        end_timestamp: "00:02:50,000",
        speaker: "Guest Professional 1",
        dialogue: "What made you put color on it with this?"
    },
    {
        start_timestamp: "00:02:50,000",
        end_timestamp: "00:03:00,000",
        speaker: "Sarah",
        dialogue: "I wanted to create a calming effect with soft blues and greens, but I can see how it might be too subtle."
    },
    {
        start_timestamp: "00:03:00,000",
        end_timestamp: "00:03:10,000",
        speaker: "Student 4",
        dialogue: "I think the furniture layout is very functional. It seems like a space where you could really relax."
    },
    {
        start_timestamp: "00:03:10,000",
        end_timestamp: "00:03:20,000",
        speaker: "Professor",
        dialogue: "Functional, yes, but it could be more dynamic. Maybe try experimenting with different furniture arrangements."
    },
    {
        start_timestamp: "00:03:20,000",
        end_timestamp: "00:03:30,000",
        speaker: "Guest Professional 2",
        dialogue: "And consider layering different textures. It could add more depth and interest to the space."
    },
    {
        start_timestamp: "00:03:30,000",
        end_timestamp: "00:03:40,000",
        speaker: "Sarah",
        dialogue: "Layering textures sounds like a good idea. I could try incorporating some textiles or different finishes."
    },
    {
        start_timestamp: "00:03:40,000",
        end_timestamp: "00:03:50,000",
        speaker: "Student 5",
        dialogue: "The open shelving is a nice touch. It makes the space feel more open and accessible."
    },
    {
        start_timestamp: "00:03:50,000",
        end_timestamp: "00:04:00,000",
        speaker: "Professor",
        dialogue: "Yes, but be careful with open shelving. It can easily become cluttered. Think about how you can maintain that clean look."
    },
    {
        start_timestamp: "00:04:00,000",
        end_timestamp: "00:04:10,000",
        speaker: "Guest Professional 1",
        dialogue: "I think we need to explore other ways of creating dimension. Maybe it is about materials? Maybe layering? Maybe it is about bunching?"
    },
    {
        start_timestamp: "00:04:10,000",
        end_timestamp: "00:04:20,000",
        speaker: "Sarah",
        dialogue: "I'll definitely experiment with those ideas. Thank you for the suggestions."
    },
    {
        start_timestamp: "00:04:20,000",
        end_timestamp: "00:04:30,000",
        speaker: "Student 6",
        dialogue: "The use of natural light is really effective. It gives the space a very welcoming feel."
    },
    {
        start_timestamp: "00:04:30,000",
        end_timestamp: "00:04:40,000",
        speaker: "Professor",
        dialogue: "Agreed, but I think the lighting could be improved. The current fixtures don't seem to complement the overall design."
    },
    {
        start_timestamp: "00:04:40,000",
        end_timestamp: "00:04:50,000",
        speaker: "Guest Professional 2",
        dialogue: "And I would suggest looking into different types of lighting fixtures. Maybe something more modern or industrial to contrast with the natural elements."
    },
    {
        start_timestamp: "00:04:50,000",
        end_timestamp: "00:05:00,000",
        speaker: "Sarah",
        dialogue: "That's a great idea. I'll look into some different options for lighting fixtures."
    }
    ];

    async function incrementRecordNumber() {
        let response = await fetch('/increment_record_number', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if(!response.ok) {
            throw new Error('Failed to increment record number');
        } 
    }

    async function sendVideoToServer(videoBlobs) {
        const vidblob = new Blob(videoBlobs, {type: 'video/webm'});
        
        console.log("video blobs", {videoBlobs, vidblob});
        let data = new FormData();
        data.append('file', vidblob);

        if(vidblob.length === 0 || !vidblob) {
            return null;
        }

        const response = await fetch('/download_screen', {
            method: 'POST',
            body: data,
        });
        if(!response.ok) {
            micPath = null;
            videoPath = null;
            // throw new Error('Failed to send video to server');
            console.log('Failed to send video to server');
        } else {
            const json = await response.json();
            videoPath = json["filepath"];
        }
        return videoPath;
    }

    async function sendAudioToServer(audioBlobs) {
        const blob = new Blob(audioBlobs, {type: 'audio/webm'});
        console.log("audio blobs", {audioBlobs, blob})
        let data = new FormData();
        data.append('audio', blob, 'audio.webm');
        const response = await fetch('/download_mic', {
            method: 'POST',
            body: data,
        });
        if(!response.ok) {
            micPath = null;
            videoPath = null;
            throw new Error('Failed to send audio to server');
        } else {
            const json = await response.json();
            micPath = json["filepath"];
        }
        return micPath;
    }

    async function fetchVideo(video_path) {
        try {   
            const response = await fetch("/fetch_video", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    "path": video_path,
                }),
            });
            const blob = await response.blob();
            let video_source = URL.createObjectURL(blob);
            return video_source;
        } catch (error) {
            console.error(error);
        } 
    }

    async function fetchAudio(audio_path) {
        try {   
            const response = await fetch("/fetch_audio", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    "audio_path": audio_path,
                }),
            });
            const blob = await response.blob();
            let audio_source = URL.createObjectURL(blob);
            return audio_source;
        } catch (error) {
            console.error(error);
        } 
    }

    async function transcribeMic(micPath) {
        const response = await fetch('/transcribe_mic', {
            method: 'POST',
            body: JSON.stringify({"audio": micPath}),
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if(!response.ok) {
            throw new Error('Failed to transcribe audio');
        } else {
            const json = await response.json();
            let transcript = json["transcript"]
            return transcript
        }
    }

    async function startRecording() {
        is_recording = true;
        videoStream = await navigator.mediaDevices.getDisplayMedia({
            video: {frameRate:60},
            //@ts-ignore
            selfBrowserSurface:'include',
        })
        videoRecorder = new MediaRecorder(videoStream, {mimeType: 'video/webm'});
        videoRecorder.videoChunks = [];
        videoRecorder.addEventListener('dataavailable', event => {
            if (event.data.size > 0) {
                videoChunks.push(event.data);
            }
        });
        videoRecorder.addEventListener('stop', () => {
            
            // sendVideoToServer(videoChunks);
            // console.log("video chunks", videoChunks);
            // videoChunks = [];
        });

        micStream = await navigator.mediaDevices.getUserMedia({audio: true});
        micRecorder = new MediaRecorder(micStream);
        micRecorder.audioBlobs = [];
        micRecorder.addEventListener('dataavailable', event => {
            if (event.data.size > 0) {
                micBlobs.push(event.data);
            }
        });
        micRecorder.addEventListener('stop', () => {
            // sendAudioToServer(micBlobs);
            // micBlobs = [];
        });
        videoRecorder.start();
        micRecorder.start();
    }

    function pauseRecording() {
        is_recording=false;
        is_paused=true;
        videoRecorder.pause();
        micRecorder.pause();
    }

    function resumeRecording() {

        is_recording=true;
        is_paused=false;

        videoRecorder.resume();
        micRecorder.resume();
    }

    async function stopRecording() {
        is_recording=false;
        is_paused=false;
        

        videoStream.getTracks().forEach(track => track.stop());
        micStream.getTracks().forEach(track => track.stop());

        videoPath = await sendVideoToServer(videoChunks); //Bug workaround: Do this for the first time because newly created vidblob is empty during first time.
        videoPath = await sendVideoToServer(videoChunks); 
        videoChunks = [];
        
        let videoSrc = await fetchVideo(videoPath);
        
        micPath = await sendAudioToServer(micBlobs); 
        micBlobs = [];
        let micSrc = await fetchAudio(micPath);

        file_load_status="Transcribing audio (this may take a while) ...";
        file_load_progress=50;
        let transcript = await transcribeMic(micPath);
        file_load_progress=80;

        let transcript_list = await convertTranscriptToList(transcript);

        let newRecording = {video: videoSrc, audio: micSrc, transcript: transcript, transcript_list : transcript_list};
        recording=newRecording;
        await incrementRecordNumber();
        file_load_progress=100;
    }

    async function extractAudioFromVideo(videoFile) {
        const formData = new FormData();
        formData.append('file', videoFile);
        const response = await fetch('/extract_audio_from_video', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            return null;
        } 
        const json = await response.json();
        return [json["audiopath"], json["videopath"]];
    }

    async function handleFilesUpload() {
        
        if(files) {
            for (const file of files) {
                if(file.type.includes('video')) {
                    let videoSrc = URL.createObjectURL(file);
                    file_load_status="Retrieving audio...";
                    file_load_progress=10;
                    [micPath, videoPath] = await extractAudioFromVideo(file);
                    if(!micPath) {
                        micPath = null;
                        videoPath = null;
                        throw new Error('Failed to extract audio from video');
                    } 
                    let micSrc = await fetchAudio(micPath);
                    file_load_status="Transcribing audio (this may take a while) ...";
                    file_load_progress=50;
                    let transcript = await transcribeMic(micPath);
                    file_load_progress=80;
                    // file_load_status="Extracting video frames from transcript timestamps...";
                    // let timestamp_frames = await extractFrames(videoPath, transcript);

                    let transcript_list = await convertTranscriptToList(transcript);

                    let newRecording = {video: videoSrc, audio: micSrc, transcript: transcript, transcript_list:transcript_list};
                    recording=newRecording;
                    micPath=null;
                    videoPath=null;
                    await incrementRecordNumber();
                    file_load_progress=100;
                } else if(file.type.includes('audio')) {
                    let audioSrc = URL.createObjectURL(file);
                    // Save the audio file and get its path
                    file_load_status="Retrieving audio...";
                    file_load_progress=10;
                    const formData = new FormData();
                    formData.append('audio', file);
                    const response = await fetch('/download_mic', {
                        method: 'POST',
                        body: formData,
                    });
                    if(!response.ok) {
                        micPath = null;
                        videoPath = null;
                        throw new Error('Failed to save uploaded audio');
                    }
                    let json = await response.json();
                    micPath = json["filepath"];

                    // Transcribe the audio
                    file_load_status="Transcribing audio (this may take a while) ...";
                    file_load_progress=50;
                    let transcript = await transcribeMic(micPath);

                    let transcript_list = await convertTranscriptToList(transcript);

                    let newRecording = {video: null, audio: micSrc, transcript: transcript, transcript_list:transcript_list};
                    recording = newRecording;
                    micPath=null;
                    videoPath=null;
                    await incrementRecordNumber();
                }
            }
            // Clear the file input
            files=null;
            file_input.value='';
        }
    
    }

    async function convertTranscriptToList(transcript) {
        const response = await fetch("/transcript_to_list", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({transcript: transcript})
        });
        if(!response.ok) {
            throw new Error("Failed to receive initial message from ChatGPT");
        }

        // 4) Send response back here to client
        const json = await response.json();
        let transcript_list = json["transcript_list"];

        return transcript_list;
    }

    async function autoDetectFeedback(transcript_list) {
        let feedback_list = [];

        let transcript_str = "";
        for (let i = 0; i < transcript_list.length; i++) {
            let excerpt = transcript_list[i];
            let id= excerpt.id;
            let start = excerpt.start_timestamp;
            let end = excerpt.end_timestamp;
            let speaker = excerpt.speaker;
            let dialogue = excerpt.dialogue;
            transcript_str += `${id}\n${start} --> ${end}\n${speaker}: ${dialogue}\n\n`;
        }
        // console.log(transcript_str);

        const response = await fetch("/autodetect_feedback", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({transcript: transcript_str})
        });
        if(!response.ok) {
            throw new Error("Failed to detect feedback");
        }
        const json = await response.json();
        feedback_list = json["feedback_list"];
        console.log(feedback_list);


        
        return feedback_list;   
    }

    function autoHighlightFeedback(feedback_list, transcript_list) {
        for(let i=0; i < feedback_list.length; i++) {
            let feedback=feedback_list[i];
            let feedback_type = feedback.type;
            if (feedback.type!="positive" && feedback.type!="critical") {
                continue;
            }

            let dialogue_id = parseInt(feedback.dialogue_id);
            let excerpt;
            for(let j = 0; j < transcript_list.length; j++) {
                let e = transcript_list[j];
                if(e.id === dialogue_id) {
                    excerpt = e;
                    break;
                }
                
            }
            if (!excerpt){
                console.log("Error: Corresponding transcript excerpt not found")
                continue;
            }
            
            let dialogue = excerpt.dialogue;
            let start_index = dialogue.indexOf(feedback.quote);
            let end_index = start_index + feedback.quote.length;
            let highlighted_dialogue = dialogue.slice(0, start_index) + `<mark class="${feedback_type}">${feedback.quote}</mark>` + dialogue.slice(end_index);
            excerpt.dialogue = highlighted_dialogue;
        }
        transcript_list = transcript_list;
    }

    function displayTranscript(transcript_list, feedback_list) {
        console.log("transcript list", transcript_list)
        transcript_str = "";
        for (let i = 0; i < transcript_list.length; i++) {
            let excerpt = transcript_list[i];
            let id = excerpt.id;
            let start = excerpt.start_timestamp;
            let end = excerpt.end_timestamp;
            let speaker = excerpt.speaker;
            let dialogue = excerpt.dialogue;
            // transcript_str += `${id}<br>${start} --> ${end}<br>${speaker}: ${dialogue}<br>`;
            transcript_str += `${start} --> ${end}<br>${speaker}: ${dialogue} <br>`;

        }
        transcript_str = transcript_str;
    }
</script>

<div div class="row spaced" id="feedback-selector-page">
    <div id="left-panel" class="column spaced" style="padding-bottom: 1rem;">

        <!-- #BUG: this div clips the transcript even if overflow-y is set.  -->
        <div id="transcript-area" class="column bordered spaced">
            {#if recording && recording.transcript_list && transcript_str}
                <p class="spaced padded"> 
                    {@html transcript_str} 
                    <!-- {#each (recording && recording.transcript_list) as excerpt, index}
                        {#if index !== 0}
                            <br>
                        {/if}
                        [{excerpt.start_timestamp} - {excerpt.end_timestamp}]<br>
                        {excerpt.speaker ? `${excerpt.speaker}: ` : ""}{excerpt.dialogue}<br>
                    {/each} -->
                </p>
            {:else}
                <span> No discussion transcript loaded. Please first record or upload your discussion. </span>
            {/if}
        </div>
        <div id="transcript-buttons-area" class="row centered spaced">
            <div id="capture-feedback-panel" class="column bordered spaced">
                <span style="font-weight: bold; text-decoration: underline; margin-left: 1rem;"> Step 1: Record or upload your discussion.</span>
                <div class="row centered spaced">
                    <div class="column centered">
                        <span >Screen record your discussion</span>
                        <div class="row spaced">
                            <button class="action-button" on:click={() => startRecording()} disabled={is_recording || is_paused} >
                                <img src="./logos/record-video-svgrepo-com.svg" alt="Start recording" class="logo">
                                Record
                            </button>
                            {#if is_paused}
                                <button class="action-button" on:click={() => resumeRecording()} disabled={!is_paused}>
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-play logo" style="border-radius: 50%; padding: 5px; background-color: #fff;">
                                        <polygon points="5 3 19 12 5 21 5 3"></polygon>
                                    </svg>
                                    Resume
                                </button>
                            {:else}
                                <button class="action-button" on:click={() => pauseRecording()} disabled={!is_recording || is_paused}>
                                    <img src="./logos/pause-circle-svgrepo-com.svg" alt="Pause recording" class="logo">
                                    Pause
                                </button>
                            {/if}
                            <button class="action-button" 
                                on:click={ async () => {
                                    is_loading=true;
                                    await stopRecording();
                                    displayTranscript(recording.transcript_list, feedback_list);
                                    is_loading=false;
                                }}
                                disabled={!is_recording && !is_paused}>
                                <img src="./logos/record-video-stop-svgrepo-com.svg" alt="Stop recording" class="logo">
                                Stop
                            </button>
                        </div>
                    </div>
                    <span>or</span>
                    <div class="column centered spaced">
                        <label for="file_upload" >Upload your own video or audio recording: </label>
                        <input bind:files bind:this={file_input} name="file_upload"type="file" id="file_upload" accept="video/*, audio/*"/>
                        <button on:click={async () => {
                                    is_loading=true;
                                    await handleFilesUpload();
                                    displayTranscript(recording.transcript_list, feedback_list);
                                    is_loading=false;
                                }} 
                        disabled={is_loading || !files || files.length===0}> Upload files</button> 
                    </div>
                </div>
            </div>
            <div id="feedback-highlight-panel" class ="column bordered spaced ">
                <span style="font-weight: bold; text-decoration: underline; margin-left: 1rem;"> Step 2: Highlight feedback in the transcript.</span>
                <div class="row centered spaced">
                    <button class = "action-button" 
                        disabled={!recording || !recording.transcript_list || is_loading}
                        on:click={async () => {
                            is_loading=true;
                            feedback_list =  await autoDetectFeedback(recording.transcript_list);
                            console.log("feedback list", feedback_list)
                            console.log("transcript list", recording.transcript_list)
                            autoHighlightFeedback(feedback_list, recording.transcript_list);
                            displayTranscript(recording.transcript_list, feedback_list);
                            console.log(feedback_list)
                            console.log(recording.transcript_list)
                            is_loading=false;
                        }}
                    > 
                        <img src="./logos/magnifying-glass-for-search-3-svgrepo-com.svg" alt="Auto-detect Feedback" class="logo">
                        Auto-detect
                    </button>
                    <button class="action-button"
                        disabled={!recording || !recording.transcript_list || is_loading}
                    > 
                        <img src="./logos/highlight-svgrepo-com.svg" alt="Highlight Feedback" class="logo">
                        Highlight 
                    </button>
                    <button class="action-button"
                        disabled={!recording || !recording.transcript_list || is_loading}
                    > 
                        <img src="./logos/delete-svgrepo-com.svg" alt="De-highlight Feedback" class="logo">
                        De-highlight
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div id="right-panel" class="column spaced" style="padding-bottom: 1rem;">
        <div id="media-player-area" class="bordered">
            {#if recording && recording.video}
                <video src={recording.video} controls style="width: 100%; height: 100%;">
                    <track kind="captions" src="blank.vtt" srclang="en">
                </video>
            {:else if recording && recording.audio}
                <audio src={recording.audio} controls style="width: 100%; height: auto;"></audio>
            {:else}
                <video src="video.mp4" controls style="width: 100%; height: 100%;">
                    <track kind="captions" src="blank.vtt" srclang="en">
                </video>
            {/if}
        </div>
        <div id="feedback-details-area" class="bordered">

        </div>

    </div>



</div>

<style>
    #feedback-selector-page{
        position: relative;
        height:100%;
        width:100%;
    }

    #left-panel {
        position: relative;
        height: 100%;
        width: 60%;
    }

    #transcript-area {
        width:100%;
        height:80%;
        overflow-y: auto;
    }

    #transcript-buttons-area {
        width:100%;
        height:20%;
    }

    #capture-feedback-panel {
        position:relative;
        height: 100%;
        width: 60%;
    }

    #feedback-highlight-panel {
        position:relative;
        height: 100%;
        width: 40%;
    }

    #right-panel {
        position: relative;
        height: 100%;
        width: 40%;
    }

    #media-player-area {
        position:relative;
        height: 50%;
        width: 100%;
    }

    #feedback-details-area {
        position:relative;
        height: 50%;
        width: 100%;
    }

    .action-button{
        height: 100%;
        width: auto; 
        border: 0 none;
    }

    mark.positive {
        background-color:lightgreen;
        color: black;
    }

    mark.critical{
        background-color:lightcoral;
        color: black;
    }

</style>