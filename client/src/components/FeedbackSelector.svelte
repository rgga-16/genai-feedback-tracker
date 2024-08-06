<script>
    import {onMount} from 'svelte';
    import LoadingBar from './LoadingBar.svelte';
    import {seekTo, focusOnFeedback, logAction, pause} from '../utils.js';
    import {saveFeedbackList, saveRecording} from '../savers.js';
    
    export let recording = {};
    export let feedback_list = [];

    let tooltip; 

    let to_transcribe=false;
    let feedback_idx = 0; 

    let mediaPlayer; 
    let ld_bar_transcript;

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

    let media_files, mediafile_input;
    let transcript_files, transcript_fileinput;

    let is_loading=false;
    let load_status = "";
    let progress = 0;

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

    async function embedTranscriptList(transcript_list) {
        const response = await fetch("/embed_transcript", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({transcript: transcript_list})
        });
        if(!response.ok) {
            throw new Error("Failed to embed transcript list");
        }
    }

    async function stopRecording() {
        is_recording=false;
        is_paused=false;
        
        
        videoStream.getTracks().forEach(track => track.stop());
        micStream.getTracks().forEach(track => track.stop());

        load_status="Saving video and audio ...";
        progress=20; 
        videoPath = await sendVideoToServer(videoChunks); //Bug workaround: Do this for the first time because newly created vidblob is empty during first time.
        videoPath = await sendVideoToServer(videoChunks); 
        videoChunks = [];
        
        let videoSrc = await fetchVideo(videoPath);
        
        micPath = await sendAudioToServer(micBlobs); 
        micBlobs = [];
        let micSrc = await fetchAudio(micPath);

        load_status="Transcribing audio (this may take a while) ...";
        progress=40;
        let transcript = await transcribeMic(micPath);

        load_status="Cleaning transcript..."
        progress=60;
        let simplified_transcript = await simplifyTranscript(transcript);
        let transcript_list = await convertTranscriptToList(simplified_transcript);

        load_status="Saving transcript as a database (this may take a while) ... "
        progress=80;
        await embedTranscriptList(transcript_list);

        load_status="Done!"
        progress=100;
        await pause(1500); 
        let newRecording = {
            video: videoSrc, 
            video_path: videoPath,
            audio: micSrc, 
            audio_path: micPath,
            transcript: simplified_transcript, 
            transcript_list : transcript_list
        };
        recording=newRecording;
        // await incrementRecordNumber();
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

    async function deleteRecording() {
        let response = await fetch("/delete_recording", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({recording: recording})
        });
        recording = {};

        let response_json = await response.json();
        if("message" in response_json) {
            console.log(response_json["message"]);
        }
        return response_json["message"];
    }

    


    async function handleMediaUpload() {
        if(media_files) {
            for (const file of media_files) {
                console.log(file.type);
                if(file.type.includes('video')) {
                    if(recording || "video" in recording || "audio" in recording || "transcript_list" in recording) {
                        if(recording.video || recording.audio || recording.transcript_list) {
                            let confirm = window.confirm("Uploading a new video will overwrite this recording. Do you want to proceed?");
                            if(!confirm) {
                                return;
                            }
                            await deleteRecording();
                        }
                    }
                    // feedback_list=[];

                    let videoSrc = URL.createObjectURL(file);
                    load_status="Uploading video...";
                    progress= to_transcribe ? 20 : 50;
                    [micPath, videoPath] = await extractAudioFromVideo(file);
                    if(!micPath || !videoPath) {
                        micPath = null;
                        videoPath = null;
                        throw new Error('Failed to extract audio from video');
                    } 

                    let micSrc = await fetchAudio(micPath);

                    let transcript=null; 
                    let transcript_list = null; 
                    if(to_transcribe) {
                        load_status="Transcribing audio (this may take a while) ...";
                        progress=40;
                        transcript = await transcribeMic(micPath);

                        load_status="Cleaning transcript...";
                        progress=60;
                        // load_status="Extracting video frames from transcript timestamps...";
                        // let timestamp_frames = await extractFrames(videoPath, transcript);
                        transcript = await simplifyTranscript(transcript);
                        transcript_list = await convertTranscriptToList(transcript);
                        
                        load_status="Saving transcript as a database (this may take a while) ... "
                        progress=80;
                        await embedTranscriptList(transcript_list);
                    }


                    load_status="Done!"
                    progress=100;
                    pause(1500);
                    progress=0;
                    let newRecording = {
                        video: videoSrc, 
                        video_path: videoPath,
                        audio: micSrc, 
                        audio_path: micPath,
                        transcript: transcript, 
                        transcript_list:transcript_list
                    };
                    recording=newRecording;
                    micPath=null;
                    videoPath=null;
                    // await incrementRecordNumber();
                } else if(file.type.includes('audio')) {
                    if(recording || "audio" in recording || "video" in recording || "transcript_list" in recording) {
                        if(recording.audio || recording.video || recording.transcript_list) {
                            let confirm = window.confirm("Uploading a new audio will overwrite this recording. Do you want to proceed?");
                            if(!confirm) {
                                return;
                            }
                            await deleteRecording();
                        }
                    }
                    // feedback_list=[];
                    let audioSrc = URL.createObjectURL(file);
                    // Save the audio file and get its path
                    load_status="Uploading audio...";
                    progress= to_transcribe ? 20 : 50;
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

                    let transcript=null; 
                    let transcript_list = null; 

                    if(to_transcribe) {
                        // Transcribe the audio
                        load_status="Transcribing audio (this may take a while) ...";
                        progress=40;
                        transcript = await transcribeMic(micPath);

                        load_status="Cleaning transcript...";
                        progress=60;
                        transcript = await simplifyTranscript(transcript);
                        transcript_list = await convertTranscriptToList(transcript);

                        load_status="Saving transcript as a database (this may take a while) ... "
                        progress=80;
                        await embedTranscriptList(transcript_list);
                    }

                    load_status="Done!"
                    progress=100; 
                    await pause(1500);
                    progress=0;
                    let newRecording = {
                        video: null,
                        video_path: null,
                        audio: audioSrc, 
                        audio_path: micPath,
                        transcript: transcript, 
                        transcript_list:transcript_list
                    };
                    recording = newRecording;
                    micPath=null;
                    videoPath=null;
                    // await incrementRecordNumber();

                } 
            }
            // Clear the file input
            media_files=null;
            mediafile_input.value='';
            
        }
        console.log("Recording", recording);
        progress=0;
        load_status="";
    
    }

    async function handleTranscriptUpload() {
        if(transcript_files) {
            for (const file of transcript_files) {
                console.log(file.type);
                if(file.name.endsWith('.srt')) {

                    if(recording || "transcript" in recording || "transcript_list" in recording) {
                        if(recording.transcript || recording.transcript_list) {
                            let confirm = window.confirm("Uploading a new transcript will overwrite the current transcript. Do you want to proceed?");
                            if(!confirm) {
                                return;
                            }
                            await deleteRecording();
                        }
                    }
                    // feedback_list=[];

                    let reader = new FileReader();

                    reader.onload = async function(e) {
                        console.log(ld_bar_transcript);
                        is_loading=true;
                        let text = e.target.result;
                        console.log(text);
                        load_status="Cleaning transcript...";
                        progress=30;
                        let transcript = await simplifyTranscript(text);
                        await pause(1500); 

                        let transcript_list = await convertTranscriptToList(transcript); 

                        let newRecording = {
                            video: null, 
                            video_path: null,
                            audio: null, 
                            audio_path: null,
                            transcript: transcript, 
                            transcript_list:transcript_list
                        };
                        if(recording && (("video" in recording && recording.video) || ("audio" in recording && recording.audio))) {
                            recording.transcript_list = transcript_list;
                            recording.transcript_list=recording.transcript_list;
                            recording.transcript=transcript;
                            recording.transcript=recording.transcript;
                            recording=recording;
                            recording=recording;
                        } else {
                            recording = newRecording;
                        }


                        load_status="Saving transcript as a database (this may take a while) ... "
                        progress=60;
                        await embedTranscriptList(transcript_list);

                        // await saveTranscriptList();
                        await saveRecording(recording);
                        console.log("Transcript list embedded")
                        load_status="Done!"
                        progress=100;
                        await pause(500); 
                        progress=0;
                        
                        is_loading=false;
                    }
                    reader.readAsText(file);
                }

            }
            // Clear the file input
            transcript_files=null;
            transcript_fileinput.value='';
            
        }
        console.log("Recording", recording);
        progress=0;
        load_status="";
    }

    async function simplifyTranscript(transcript) {
        const response = await fetch("/simplify_transcript", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({transcript: transcript})
        });
        if(!response.ok) {
            throw new Error("Failed to simplify transcript string");
        }
        const json = await response.json();
        return json["simplified_transcript"];
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
            throw new Error("Failed to convert transcript string to list of excerpts");
        }

        // 4) Send response back here to client
        const json = await response.json();
        let transcript_list = json["transcript_list"];

        return transcript_list;
    }

    function convertTranscriptListToStr(transcript_list) {
        let transcript_str = "";
        for (let i = 0; i < transcript_list.length; i++) {
            let excerpt = transcript_list[i];
            let id= excerpt.id;
            let start = excerpt.start_timestamp;
            let end = excerpt.end_timestamp;
            
            let dialogue = excerpt.dialogue;

            if("speaker" in excerpt && excerpt.speaker != ""){
                let speaker = excerpt.speaker;
                transcript_str += `${id}\n${start} --> ${end}\n${speaker}: ${dialogue}\n\n`;
            } else {
                transcript_str += `${id}\n${start} --> ${end}\n${dialogue}\n\n`;
            }
        }
        return transcript_str;
    }
    
    async function autoDetectFeedback(transcript_list) {
        let feedback_list = [];

        let transcript_str = convertTranscriptListToStr(transcript_list);
        
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

    function addFeedback(type) {
        const selection = window.getSelection().toString();
        if(selection.trim() === "") {
            alert("Please highlight text in the transcript with your mouse to add as feedback.");
            return "Error: No text highlighted";
        }
        if(selection) {
            let feedback = {quote: selection, type: type, done:false, speaker:null, dialogue_id:null};
            let excerpt_reference = findExcerptByQuote(recording.transcript_list, selection);
            // console.log(excerpt_reference);

            if(!excerpt_reference) {
                console.log("Error: Corresponding transcript excerpt not found")
                alert("Error: Corresponding transcript excerpt not found. Feedback not added.");
                return "Error: Corresponding transcript excerpt not found for selection: " + selection;
            }
            feedback.id = feedback_list.length+1;
            feedback.dialogue_id = excerpt_reference.id;
            feedback.speaker=excerpt_reference.speaker;
            feedback.excerpt_reference=excerpt_reference;
            feedback.chatbot_messages =[{"role":"system", "content":"You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. "}];
            feedback_list.push(feedback);
            feedback_list=feedback_list;

            recording.transcript_list = recording.transcript_list;

            autoHighlightFeedback([feedback]);
            return feedback;
        } else {
            alert("Please highlight text in the transcript with your mouse to add as feedback.");
            return "Error: No text highlighted";
        }
    }


    function removeFeedback() {
        const selection = window.getSelection().toString();
        if(selection.trim() === "") {
            alert("Please highlight the feedback you want to remove using your mouse.");
            return "Error: No text highlighted";
        }
        if(selection) {
            for(let i=0; i < feedback_list.length; i++) {
                let feedback = feedback_list[i];
                if(feedback.quote.includes(selection)) {

                    let dialogue_id = parseInt(feedback.dialogue_id);
                    let feedback_quote = feedback.quote;

                    feedback_list.splice(i, 1);
                    feedback_list=feedback_list;

                    deHighlightFeedback(dialogue_id, feedback_quote);
                    return feedback;
                }
            }  
        }
        return "Error: Feedback not found for selection: " + selection;
    }

    function removeAllFeedback() {
        for (let i = 0; i < feedback_list.length; i++) {
            let feedback = feedback_list[i];
            let dialogue_id = parseInt(feedback.dialogue_id);
            let feedback_quote = feedback.quote;
            deHighlightFeedback(dialogue_id, feedback_quote);

            feedback_list.splice(i, 1);
            feedback_list=feedback_list;
        }
    }

    function deHighlightFeedback(dialogue_id, feedback_quote) {
        for(let j = 0; j < recording.transcript_list.length; j++) {
            let e = recording.transcript_list[j];
            if(e.id === dialogue_id) {
                let dialogue = e.dialogue;
                let start_index = dialogue.indexOf("<mark");
                let end_index = dialogue.indexOf("</mark>") + 7;
                // BUG: The highlight in the dialogue is not being removed
                let highlighted_dialogue = dialogue.slice(0, start_index) + feedback_quote + dialogue.slice(end_index);
                
                e.dialogue = highlighted_dialogue;
                e.dialogue = e.dialogue;
                recording.transcript_list = recording.transcript_list;
                break;
            }
        }
        
    }

    function autoHighlightFeedback(feedback_list) {
        for(let i=0; i < feedback_list.length; i++) {
            let feedback=feedback_list[i];
            let feedback_type = feedback.type;
            if (feedback.type!="positive" && feedback.type!="critical") {
                continue;
            }

            let dialogue_id = parseInt(feedback.dialogue_id);
            let excerpt;
            for(let j = 0; j < recording.transcript_list.length; j++) {
                let e = recording.transcript_list[j];
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
            let highlighted_dialogue = dialogue.slice(0, start_index) + `<mark class="${feedback_type}" style="background-color:${feedback_type === "positive" ? "lightgreen" : "lightcoral"};">${feedback.quote}</mark>` + dialogue.slice(end_index);
            excerpt.dialogue = highlighted_dialogue;
        }
        recording.transcript_list = recording.transcript_list;
    }


    function findExcerptByID(transcript_list,id) {
        id=parseInt(id);
        for(let i=0; i < transcript_list.length; i++) {
            let excerpt = transcript_list[i];
            if(excerpt.id === id) {
                return excerpt;
            }
        }
        console.log("Error: Can't find excerpt with id", id);
        return null;
    }

    function findExcerptByQuote(transcript_list,quote) {
        console.log(quote);
        for(let i=0; i < transcript_list.length; i++) {
            let excerpt = transcript_list[i];
            let excerpt_str = excerpt.dialogue;
            if(excerpt.speaker){
                excerpt_str = excerpt.speaker + ": " + excerpt_str;
            }
            if(excerpt_str.includes(quote)) {
                return excerpt;
            }
        }
        return null;
    }

    

    

    onMount(async () => {
        console.log(recording);
    });
</script>

<div div class="row spaced" id="feedback-selector-page">
    <div id="left-panel" class="column spaced" >
        <div id="transcript-area" class="column bordered spaced">

            <div class="overlay centered padded" class:invisible={is_loading===false}> 
                    <LoadingBar bind:progress={progress} bind:status={load_status} />
            </div>

            <div id="traverse-feedback-area" class="bordered spaced" >
                {#if feedback_list && feedback_list.length > 0}
                    <span> {feedback_idx+1} of {feedback_list.length} feedback moments highlighted </span>
                {:else}
                    <span> No feedback moments highlighted. </span>
                {/if}
                <button disabled={!feedback_list || feedback_list.length <= 0} on:click={async () => {
                    if(feedback_idx > 0) {
                        feedback_idx--;
                    } else {
                        feedback_idx = feedback_list.length - 1;
                    }
                    focusOnFeedback(feedback_list[feedback_idx]);
                    await logAction("FeedbackSelector: Traverse to previous feedback", feedback_list[feedback_idx]);
                }}> 
                    <img src="./logos/up-arrow-5-svgrepo-com.svg" alt="Prev feedback" class="logo" style="width: 1.5rem; height: 1.5rem;">
                </button>
                <button disabled={!feedback_list || feedback_list.length <= 0} on:click={async () => {
                    if(feedback_idx < feedback_list.length - 1) {
                        feedback_idx++;
                    } else {
                        feedback_idx = 0;
                    }
                    focusOnFeedback(feedback_list[feedback_idx]);
                    await logAction("FeedbackSelector: Traverse to next feedback", feedback_list[feedback_idx]);
                }}> 
                    <img src="./logos/down-arrow-5-svgrepo-com.svg" alt="Next feedback" class="logo" style="width: 1.5rem; height: 1.5rem;">  
                </button>
            </div>
            {#if recording && recording.transcript_list}
                <p class="padded"> 
                    {#each recording.transcript_list as excerpt, i}
                        <div class="spaced">
                            <span class="timestamp" on:click={async () => {
                                seekTo(excerpt.start_timestamp, mediaPlayer); 
                                await logAction("FeedbackSelector: Seeked to start timestamp", excerpt.start_timestamp);
                            }}>[{excerpt.start_timestamp}]</span> 
                            - 
                            <span class="timestamp" on:click={async () => {
                                seekTo(excerpt.end_timestamp, mediaPlayer);
                                await logAction("FeedbackSelector: Seeked to end timestamp", excerpt.end_timestamp);
                            }}>[{excerpt.end_timestamp}]</span>
                            <br>
                            {excerpt.speaker ? excerpt.speaker+":" : ""}  
                            <span id={excerpt.id}>
                                {@html excerpt.dialogue} 
                            </span> <br><br>
                        </div>    
                    {/each}
                </p>
            {:else}
                <div class="centered" style="height: 100%; width: 100%;">
                    <span> No discussion transcript loaded. Please first record or upload your discussion. </span>
                </div>
                
            {/if}
        </div>
        <div id="transcript-buttons-area" class="row centered spaced bordered">
            <div id="capture-feedback-panel" class="column padded centered spaced">
                <span style="font-weight: bold; text-decoration: underline; margin-left: 1rem;"> Step 1: Upload your discussion.</span>
                <div class="row centered spaced">
                    <!-- <div class="column centered">
                        <span >Screen record your discussion</span>
                        <div class="row spaced">
                            <button class="action-button" on:click={async () => {
                                if("video" in recording || "audio" in recording || "transcript_list" in recording) {
                                    if(recording.video || recording.audio || recording.transcript_list ) {
                                        let confirm = window.confirm("Starting a new recording will clear all highlighted feedback and overwrite the existing recording. Do you want to proceed?");
                                        if(!confirm) {
                                            return;
                                        }
                                    }
                                }
                                // feedback_list=[]; 
                                startRecording();
                                await logAction("FeedbackSelector: Start recording", null);
                            }} disabled={is_recording || is_paused} >
                                <img src="./logos/record-video-svgrepo-com.svg" alt="Start recording" class="logo">
                                Record
                            </button>
                            {#if is_paused}
                                <button class="action-button" on:click={async () => {
                                        resumeRecording(); 
                                        await logAction("FeedbackSelector: Resume recording", null);
                                    }} disabled={!is_paused}>
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-play logo" style="border-radius: 50%; padding: 5px; background-color: #fff;">
                                        <polygon points="5 3 19 12 5 21 5 3"></polygon>
                                    </svg>
                                    Resume
                                </button>
                            {:else}
                                <button class="action-button" on:click={async () => {
                                        pauseRecording();
                                        await logAction("FeedbackSelector: Pause recording", null)
                                    }} disabled={!is_recording || is_paused}>
                                    <img src="./logos/pause-circle-svgrepo-com.svg" alt="Pause recording" class="logo">
                                    Pause
                                </button>
                            {/if}
                            <button class="action-button" 
                                on:click={ async () => {
                                    is_loading=true;
                                    await stopRecording();
                                    is_loading=false;
                                    await logAction("FeedbackSelector: Stop recording", recording);
                                }}
                                disabled={!is_recording && !is_paused}>
                                <img src="./logos/record-video-stop-svgrepo-com.svg" alt="Stop recording" class="logo">
                                Stop
                            </button>
                        </div>
                    </div>
                    <span>or</span> -->
                    <div class="row centered spaced">
                        <div class="column spaced centered">
                            <label for="file_upload" >Upload your own video or audio: </label>
                            <div class="row centered spaced">
                                <input style="width: 50%;" bind:value={media_files} bind:this={mediafile_input} name="mediafile_upload"type="file" id="mediafile_upload" accept="video/*, audio/*"
                                    on:change={async (e) => {
                                        media_files = e.target.files;
                                        console.log(media_files);
                                        
                                        await logAction("FeedbackSelector: Select media file", media_files);
                                    }}
                                />

                                <!-- <div class="column centered">
                                    <label for="to-transcribe">
                                        Transcribe 
                                        <a class="tooltip-link" style="color: blue;"
                                        on:mouseover={() => {tooltip.style.visibility = 'visible';}} 
                                        on:mouseout={() => {tooltip.style.visibility = 'hidden';}}>
                                            (?)
                                        </a>
                                    </label>
                                    <span bind:this={tooltip} class="tooltip">Checking this will automatically transcribe the video/audio.</span>
                                    <input id="to-transcribe" type="checkbox" bind:checked={to_transcribe} on:change={async () => {logAction("FeedbackSelector: Check transcribe",to_transcribe)}}/>
                                </div> -->
                                
                                <button class="action-button centered column " on:click={async () => {
                                            is_loading=true;
                                            await handleMediaUpload();
                                            
                                            is_loading=false;
                                            await saveRecording(recording);
                                            await logAction("FeedbackSelector: Upload media", recording);
                                        }} 
                                disabled={is_loading || !media_files || media_files.length===0}> 
                                    <img src="./logos/upload-svgrepo-com.svg" alt="Upload file" class="mini-icon">
                                    Upload file 
                                </button> 
                                
                            </div>
                        </div>

                        <div class="column spaced centered">
                            <label for="file_upload" >Upload your own transcript (in .srt only): </label>
                            <div class="row centered">
                                <input bind:value={transcript_files} bind:this={transcript_fileinput} name="transcirptfile_upload"type="file" id="transcriptfile_upload" accept=" .srt"
                                    on:change={async (e) => {
                                        transcript_files = e.target.files;
                                        await logAction("FeedbackSelector: Select transcript file", transcript_files);
                                    }}
                                />
                                <button class="action-button centered column " on:click={async () => {
                                            is_loading=true;
                                            await handleTranscriptUpload();
                                            is_loading=false;
                                            console.log(recording);
                                            await logAction("FeedbackSelector: Upload transcript", recording);
                                            
                                        }} 
                                disabled={is_loading || !transcript_files || transcript_files.length===0}> 
                                    <img src="./logos/upload-svgrepo-com.svg" alt="Upload file" class="mini-icon">
                                    Upload file
                                </button> 
                            </div>
                        </div>
                        
                    </div>
                </div>
            </div>
            <div id="feedback-highlight-panel" class ="column spaced padded ">
                <span style="font-weight: bold; text-decoration: underline; margin-left: 1rem;"> Step 2: Highlight feedback in the discussion's transcript.</span>
                <div class="centered" style="height: 100%; width: 100%;">
                    <div class="row centered spaced">
                        <button class = "action-button" 
                            disabled={!recording || !recording.transcript_list || is_loading}
                            on:click={async () => {
                                if(feedback_list.length > 0) {
                                    let confirm = window.confirm("Auto-detecting again will clear all feedback highlighted. Do you want to proceed?");
                                    if(!confirm) {
                                        return;
                                    }
                                }
    
                                is_loading=true;
                                progress=0;
                                let list = recording.transcript_list;
                                // Divide list into 4 equally sized chunks.
                                let chunk_size = Math.ceil(list.length / 4);
                                let chunk1 = list.slice(0, chunk_size);
                                let chunk2 = list.slice(chunk_size, 2 * chunk_size);
                                let chunk3 = list.slice(2 * chunk_size, 3 * chunk_size);
                                let chunk4 = list.slice(3 * chunk_size, list.length);
                                let chunks=[chunk1, chunk2, chunk3, chunk4];
                                load_status="Detecting feedback in transcript ...";
                                for(let i=0; i < chunks.length; i++) {
                                    let thing = await autoDetectFeedback(chunks[i]);
                                    feedback_list = feedback_list.concat(thing);
                                    progress = (i+1) * 20;
                                    await pause(250); 
                                }
                                feedback_list=feedback_list;
                                console.log(feedback_list);
                                for(let j = 0; j < feedback_list.length; j++) {
                                    feedback_list[j].id = j+1; // Assign unique id to each feedback
                                    let reference_id = feedback_list[j].dialogue_id;
                                    let excerpt = findExcerptByID(recording.transcript_list,reference_id);
                                    feedback_list[j].excerpt_reference=excerpt;
                                }
                                feedback_list=feedback_list;
                                load_status="Highlighting feedback ..."
                                autoHighlightFeedback(feedback_list);
                                await saveFeedbackList(feedback_list);
                                await saveRecording(recording);
                                await pause(500); 
                                progress=100; 
                                console.log("Feedback: " + feedback_list[0]);
                                is_loading=false;
                                progress=0; 
                                load_status="";
                                await logAction("FeedbackSelector: Auto-detect feedback", feedback_list);
                            }}
                        > 
                            <img src="./logos/magnifying-glass-for-search-3-svgrepo-com.svg" alt="Auto-detect Feedback" class="logo">
                            Auto-detect <br> Feedback
                        </button>
                        <button class="action-button"
                            disabled={!recording || !recording.transcript_list || is_loading}
                            on:click={async () => {
                                let selection = addFeedback("positive");
                                await saveFeedbackList(feedback_list);
                                await saveRecording(recording);
                                await logAction("FeedbackSelector: Add positive feedback", selection);
                            }}
                        > 
                            <img src="./logos/highlight-green-svgrepo-com.svg" alt="Highlight Positive Feedback" class="logo">
                            Highlight <br> Positive
                        </button>
                        <button class="action-button"
                            disabled={!recording || !recording.transcript_list || is_loading}
                            on:click={async () => {
                                let selection = addFeedback("critical");
                                await saveFeedbackList(feedback_list);
                                await saveRecording(recording);
                                await logAction("FeedbackSelector: Add critical feedback", selection);
                            }}
                        > 
                            <img src="./logos/highlight-red-svgrepo-com.svg" alt="Highlight Critical Feedback" class="logo">
                            Highlight <br> Critical 
                        </button>
                        <button class="action-button"
                            disabled={!recording || !recording.transcript_list || is_loading}
                            on:click={async () => {
                                let selection = removeFeedback();
                                await saveFeedbackList(feedback_list);
                                await saveRecording(recording);
                                await logAction("FeedbackSelector: Remove feedback", selection);
                            }}
                        > 
                            <img src="./logos/erase-svgrepo-com.svg" alt="De-highlight Feedback" class="logo">
                            Remove <br> Feedback
                        </button>
                        <button class="action-button"
                            disabled={!recording || !recording.transcript_list || is_loading}
                            on:click={async () => {
                                removeAllFeedback();
                                await saveFeedbackList(feedback_list);
                                await saveRecording(recording);
                                await logAction("FeedbackSelector: Removed all feedback", feedback_list);
                            }}
                        > 
                            <img src="./logos/delete-svgrepo-com.svg" alt="Delete all Feedback" class="logo">
                            Remove all <br> Feedback
                        </button>
                    </div>
                </div>
                
            </div>
        </div>
    </div>

    <div id="right-panel" class="column spaced" >
        <div id="media-player-area" class="bordered centered">
            {#if recording && recording.video}
                <video bind:this={mediaPlayer} src={recording.video} controls style="width: 100%; height: 100%;">
                    <track kind="captions" src="blank.vtt" srclang="en">
                </video>
            {:else if recording && recording.audio}
                <audio bind:this={mediaPlayer} src={recording.audio} controls style="width: 100%; height: 100%;"></audio>
            {:else}
                <video bind:this={mediaPlayer} src="video.mp4" controls style="width: 100%; height: 100%;">
                    <track kind="captions" src="blank.vtt" srclang="en">
                </video>
            {/if}
        </div>
        <div id="feedback-details-area" class="bordered padded spaced" style="overflow-y:auto;">
            <h3 style="font-weight: bold; text-decoration: underline;"> Discussion Transcript Details </h3>
            {#if recording && recording.transcript_list}
                {#if "speaker" in recording.transcript_list[0]} 
                    <strong> Number of participants: {Object.keys(recording.transcript_list.reduce((acc, cur) => {
                        acc[cur.speaker] = true;
                        return acc;
                    }, {})).length}</strong> <br>
                    <ul>
                        {#each Object.entries(recording.transcript_list.reduce((acc, cur) => {
                            acc[cur.speaker] = (acc[cur.speaker] || 0) + 1;
                            return acc;
                        }, {})) as [pa, count]}
                            <li> - {pa}: {count} utterances</li>
                            <!-- <li> - {pa} </li> -->
                        {/each}
                    </ul>
                    <br>
                {/if}
                
                
                {#if feedback_list}
                    <strong> Number of feedback utterances: {feedback_list.length} </strong>
                    <ul>
                        <li> - Number of positive feedback: {feedback_list.filter(feedback => feedback.type === 'positive').length}</li>
                        <li> - Number of critical feedback: {feedback_list.filter(feedback => feedback.type === 'critical').length}</li>
                    </ul>
                {/if}
            {/if}
        </div>
    </div>
    



</div>

<style>
    #feedback-selector-page{
        position: relative;
        padding-top: 1rem;
        display:flex;
        height:100%;
        width:100%;
        background-color: #F8F9FA;
    }

    #left-panel {
        position: relative;
        height: 100%;
        width: 60%;
        padding-bottom: 1rem;
    }

    #transcript-area {
        width:100%;
        height:72%;
        overflow-y: auto;
    }

    #traverse-feedback-area {
        align-self: flex-end; 
        display: flex; 
        padding: 0.5rem; 
        position: sticky; 
        top: 0; 
        right: 0; 
        z-index: 2; 
        justify-content: right; 
        text-align:right; 
        width: 35%; 
        background-color: #f0f0f0;
    }

    #transcript-buttons-area {
        width:100%;
        height:28%;
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
        padding-bottom: 1rem;
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
        /* background-color:lightgreen;
        color: black; */
        background-color: #28A745;
        color: #FFFFFF;
        
    }

    mark.critical{
        /* background-color:lightcoral;
        color: black; */
        background-color: #DC3545;
        color: #FFFFFF;
    }

    mark:hover {
        cursor: pointer;
    }

    span.timestamp {
        color: #007BFF;
    }

    span.timestamp:hover{
        /* font-weight: bold; */
        text-decoration: underline;
        cursor: pointer;
    }

    

</style>