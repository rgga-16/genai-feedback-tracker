<script>
    import {onMount} from 'svelte';
    import {timeToSeconds, seekTo, focusOnFeedback} from '../utils.js';
    
    export let recording;
    export let feedback_list;

    let feedback_idx = 0; 

    let mediaPlayer; 

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
    let load_status = "";

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
        setLoadingProgress("ld-bar-transcript",20);
        videoPath = await sendVideoToServer(videoChunks); //Bug workaround: Do this for the first time because newly created vidblob is empty during first time.
        videoPath = await sendVideoToServer(videoChunks); 
        videoChunks = [];
        
        let videoSrc = await fetchVideo(videoPath);
        
        micPath = await sendAudioToServer(micBlobs); 
        micBlobs = [];
        let micSrc = await fetchAudio(micPath);

        load_status="Transcribing audio (this may take a while) ...";
        setLoadingProgress("ld-bar-transcript",40);
        let transcript = await transcribeMic(micPath);

        load_status="Cleaning transcript..."
        setLoadingProgress("ld-bar-transcript",60);
        let simplified_transcript = await simplifyTranscript(transcript);
        let transcript_list = await convertTranscriptToList(simplified_transcript);

        load_status="Saving transcript as a database..."
        setLoadingProgress("ld-bar-transcript",80);
        await embedTranscriptList(transcript_list);

        load_status="Done!"
        setLoadingProgress("ld-bar-transcript",100);
        await new Promise(resolve => setTimeout(resolve, 500));
        let newRecording = {video: videoSrc, audio: micSrc, transcript: simplified_transcript, transcript_list : transcript_list};
        recording=newRecording;
        await incrementRecordNumber();
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
                    load_status="Uploading video...";
                    setLoadingProgress("ld-bar-transcript",20);
                    [micPath, videoPath] = await extractAudioFromVideo(file);
                    if(!micPath) {
                        micPath = null;
                        videoPath = null;
                        throw new Error('Failed to extract audio from video');
                    } 
                    let micSrc = await fetchAudio(micPath);

                    load_status="Transcribing audio (this may take a while) ...";
                    setLoadingProgress("ld-bar-transcript",40);
                    let transcript = await transcribeMic(micPath);

                    load_status="Cleaning transcript...";
                    setLoadingProgress("ld-bar-transcript",60);
                    // load_status="Extracting video frames from transcript timestamps...";
                    // let timestamp_frames = await extractFrames(videoPath, transcript);
                    let simplified_transcript = await simplifyTranscript(transcript);
                    let transcript_list = await convertTranscriptToList(simplified_transcript);

                    load_status="Saving transcript as a database..."
                    setLoadingProgress("ld-bar-transcript",80);
                    await embedTranscriptList(transcript_list);

                    load_status="Done!"
                    setLoadingProgress("ld-bar-transcript",100);
                    await new Promise(resolve => setTimeout(resolve, 500));
                    let newRecording = {video: videoSrc, audio: micSrc, transcript: simplified_transcript, transcript_list:transcript_list};
                    recording=newRecording;
                    micPath=null;
                    videoPath=null;
                    await incrementRecordNumber();
                } else if(file.type.includes('audio')) {
                    let audioSrc = URL.createObjectURL(file);
                    // Save the audio file and get its path
                    load_status="Uploading audio...";
                    setLoadingProgress("ld-bar-transcript",20);
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
                    load_status="Transcribing audio (this may take a while) ...";
                    setLoadingProgress("ld-bar-transcript",40);
                    let transcript = await transcribeMic(micPath);

                    load_status="Cleaning transcript...";
                    setLoadingProgress("ld-bar-transcript",60);
                    let simplified_transcript = await simplifyTranscript(transcript);
                    let transcript_list = await convertTranscriptToList(simplified_transcript);

                    load_status="Saving transcript as a database..."
                    setLoadingProgress("ld-bar-transcript",80);
                    await embedTranscriptList(transcript_list);

                    load_status="Done!"
                    setLoadingProgress("ld-bar-transcript",100);
                    await new Promise(resolve => setTimeout(resolve, 500));
                    let newRecording = {video: null, audio: audioSrc, transcript: simplified_transcript, transcript_list:transcript_list};
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
        console.log("Recording", recording);
    
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
            let speaker = excerpt.speaker;
            let dialogue = excerpt.dialogue;

            if(excerpt.speaker){
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
        if(selection) {
            let feedback = {quote: selection, type: type, done:false, speaker:null, dialogue_id:null};
            let excerpt_reference = findExcerptByQuote(recording.transcript_list, selection);
            // console.log(excerpt_reference);

            if(!excerpt_reference) {
                console.log("Error: Corresponding transcript excerpt not found")
                alert("Error: Corresponding transcript excerpt not found. Feedback not added.");
                return;
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
        } else {
            alert("Please highlight text in the transcript with your mouse to add as feedback.");
        }
    }


    function removeFeedback() {
        const selection = window.getSelection().toString();
        if(selection) {
            for(let i=0; i < feedback_list.length; i++) {
                let feedback = feedback_list[i];
                if(feedback.quote.includes(selection)) {

                    let dialogue_id = parseInt(feedback.dialogue_id);
                    let feedback_quote = feedback.quote;

                    feedback_list.splice(i, 1);
                    feedback_list=feedback_list;

                    deHighlightFeedback(dialogue_id, feedback_quote);
                    break;
                }
            }
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

    function setLoadingProgress(loadbar_id, value) {
        var bar = document.getElementById(loadbar_id).ldBar;
        bar.set(value);
    }

    

    onMount(async () => {
        if(recording && recording.transcript_list) {
            await embedTranscriptList(recording.transcript_list);
            console.log("Transcript list embedded");
        }
    });
</script>

<div div class="row spaced" id="feedback-selector-page">
    <div id="left-panel" class="column spaced" >
        <div id="transcript-area" class="column bordered spaced">

            <div class="overlay centered padded" class:invisible={is_loading===false}> 
                <div id="ld-bar-transcript" class="ldBar centered column" data-preset="circle" data-value=0 style="width:100%; height: 20%;">
                    {load_status}
                </div>
            </div>

            <div id="traverse-feedback-area" class="bordered spaced" >
                {#if feedback_list && feedback_list.length > 0}
                    <span> {feedback_idx+1} of {feedback_list.length} feedback moments highlighted </span>
                {:else}
                    <span> No feedback moments highlighted. </span>
                {/if}
                <button disabled={!feedback_list || feedback_list.length <= 0} on:click={() => {
                    if(feedback_idx > 0) {
                        feedback_idx--;
                    } else {
                        feedback_idx = feedback_list.length - 1;
                    }
                    focusOnFeedback(feedback_list[feedback_idx]);
                }}> 
                    <img src="./logos/up-arrow-5-svgrepo-com.svg" alt="Prev feedback" class="logo" style="width: 1.5rem; height: 1.5rem;">
                </button>
                <button disabled={!feedback_list || feedback_list.length <= 0} on:click={() => {
                    if(feedback_idx < feedback_list.length - 1) {
                        feedback_idx++;
                    } else {
                        feedback_idx = 0;
                    }
                    focusOnFeedback(feedback_list[feedback_idx]);
                }}> 
                    <img src="./logos/down-arrow-5-svgrepo-com.svg" alt="Next feedback" class="logo" style="width: 1.5rem; height: 1.5rem;">  
                </button>
            </div>
            {#if recording && recording.transcript_list}
                <p class="spaced padded"> 
                    {#each recording.transcript_list as excerpt, i}
                        <span class="timestamp" on:click={() => seekTo(excerpt.start_timestamp, mediaPlayer)}>[{excerpt.start_timestamp}]</span> - <span class="timestamp" on:click={() => seekTo(excerpt.end_timestamp, mediaPlayer)}>[{excerpt.end_timestamp}]</span><br>
                        {excerpt.speaker ? excerpt.speaker+":" : ""}  
                        <span id={excerpt.id}>
                            {@html excerpt.dialogue} 
                        </span> <br><br>
                    {/each}
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
                                    is_loading=false;
                                }} 
                        disabled={is_loading || !files || files.length===0}> 
                            Upload files
                        </button> 
                    </div>
                </div>
            </div>
            <div id="feedback-highlight-panel" class ="column bordered spaced ">
                <span style="font-weight: bold; text-decoration: underline; margin-left: 1rem;"> Step 2: Highlight feedback in the discussion's transcript.</span>
                <div class="row centered spaced">
                    <button class = "action-button" 
                        disabled={!recording || !recording.transcript_list || is_loading}
                        on:click={async () => {
                            is_loading=true;
                            setLoadingProgress("ld-bar-transcript",0); 
                            feedback_list=[];

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
                                setLoadingProgress("ld-bar-transcript",(i+1) * 20); 
                            }
                            feedback_list=feedback_list;
                            console.log(feedback_list);
                            for(let j = 0; j < feedback_list.length; j++) {
                                let reference_id = feedback_list[j].dialogue_id;
                                let excerpt = findExcerptByID(recording.transcript_list,reference_id);
                                feedback_list[j].excerpt_reference=excerpt;
                            }
                            feedback_list=feedback_list;
                            load_status="Highlighting feedback ..."
                            autoHighlightFeedback(feedback_list);
                            await new Promise(resolve => setTimeout(resolve, 500));
                            setLoadingProgress("ld-bar-transcript",100); 
                            console.log("Feedback: " + feedback_list[0]);
                            is_loading=false;
                            setLoadingProgress("ld-bar-transcript",0); 
                            load_status="";
                        }}
                    > 
                        <img src="./logos/magnifying-glass-for-search-3-svgrepo-com.svg" alt="Auto-detect Feedback" class="logo">
                        Auto-detect <br> Feedback
                    </button>
                    <button class="action-button"
                        disabled={!recording || !recording.transcript_list || is_loading}
                        on:click={() => addFeedback("positive")}
                    > 
                        <img src="./logos/highlight-green-svgrepo-com.svg" alt="Highlight Positive Feedback" class="logo">
                        Highlight <br> Positive
                    </button>
                    <button class="action-button"
                        disabled={!recording || !recording.transcript_list || is_loading}
                        on:click={() => addFeedback("critical")}
                    > 
                        <img src="./logos/highlight-red-svgrepo-com.svg" alt="Highlight Critical Feedback" class="logo">
                        Highlight <br> Critical 
                    </button>
                    <button class="action-button"
                        disabled={!recording || !recording.transcript_list || is_loading}
                        on:click={() => removeFeedback()}
                    > 
                        <img src="./logos/erase-svgrepo-com.svg" alt="De-highlight Feedback" class="logo">
                        Remove <br> Feedback
                    </button>
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
        <div id="feedback-details-area" class="bordered padded spaced">
            <h3 style="font-weight: bold; text-decoration: underline;"> Discussion Transcript Details </h3>
            {#if recording && recording.transcript_list}
                <strong> Number of participants: {Object.keys(recording.transcript_list.reduce((acc, cur) => {
                    acc[cur.speaker] = true;
                    return acc;
                }, {})).length}</strong> <br>
                <ul>
                    {#each Object.entries(recording.transcript_list.reduce((acc, cur) => {
                        acc[cur.speaker] = (acc[cur.speaker] || 0) + 1;
                        return acc;
                    }, {})) as [pa, count]}
                        <!-- <li> - {pa}: {count} utterances</li> -->
                        <li> - {pa} </li>
                    {/each}
                </ul>
                <br>
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
        height:100%;
        width:100%;
    }

    #left-panel {
        position: relative;
        height: 100%;
        width: 60%;
        padding-bottom: 1rem;
    }

    #transcript-area {
        width:100%;
        height:80%;
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
        background-color:lightgreen;
        color: black;
    }

    mark.critical{
        background-color:lightcoral;
        color: black;
    }

    mark:hover {
        cursor: pointer;
    }

    span.timestamp {
        color: blue;
    }

    span.timestamp:hover{
        /* font-weight: bold; */
        color: blue;
        text-decoration: underline;
        cursor: pointer;
    }

    .overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.75); /* Semi-transparent black */
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        font-size: 1.5rem;
        z-index: 3;
    }

</style>