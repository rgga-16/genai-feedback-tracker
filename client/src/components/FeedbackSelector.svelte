<script>
    export let recording;
    export let feedback_list;
    let positive_feedback = [];
    let critical_feedback = []; 
    let transcript_str;

    let videoPlayer; 

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

    let participants={};

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
        segregateFeedback(feedback_list);
        return feedback_list;   
    }

    function segregateFeedback(feedback_list) {
        for(let i=0; i < feedback_list.length; i++) {
            let feedback = feedback_list[i];
            if(feedback.type === "positive") {
                positive_feedback.push(feedback);
                positive_feedback=positive_feedback;
            } else if(feedback.type === "critical") {
                critical_feedback.push(feedback);
                critical_feedback=critical_feedback;
            }
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
                    deHighlightFeedback(dialogue_id, feedback_quote);

                    if(feedback.type==="positive") {
                        for(let j=0; j < positive_feedback.length; j++) {
                            if(positive_feedback[j].quote === feedback_quote) {
                                positive_feedback.splice(j, 1);
                                positive_feedback=positive_feedback;
                                break;
                            }
                        }
                    } else if(feedback.type==="critical") {
                        for(let j=0; j < critical_feedback.length; j++) {
                            if(critical_feedback[j].quote === feedback_quote) {
                                critical_feedback.splice(j, 1);
                                critical_feedback=critical_feedback;
                                break;
                            }
                        }
                    }
                    feedback_list.splice(i, 1);
                    feedback_list=feedback_list;
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
                let start_index = dialogue.indexOf(feedback_quote);
                let end_index = start_index + feedback_quote.length;
                // BUG: The highlight in the dialogue is not being removed
                let highlighted_dialogue = dialogue.slice(0, start_index) + feedback_quote + dialogue.slice(end_index);
                e.dialogue = highlighted_dialogue;
                e.dialogue = e.dialogue;
                break;
            }
        }
        recording.transcript_list = recording.transcript_list;
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
            excerpt.dialogue = excerpt.dialogue;
        }
        recording.transcript_list = recording.transcript_list;
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
            // transcript_str += `${id}<br>[${start} - ${end}]<br>${speaker}: ${dialogue}<br><br>`;
            transcript_str += `[${start}] - [${end}]<br>${speaker}: ${dialogue} <br><br>`;

        }
        transcript_str = transcript_str;
    }

    function getParticipants(transcript_list) {
        let participants_dict = {};
        for (let i = 0; i < transcript_list.length; i++) {

            let speaker = transcript_list[i].speaker;

            if(Object.keys(participants_dict).includes(speaker)) {
                participants_dict[speaker] += 1;
            } else {
                participants_dict[speaker] = 1;
            }
        }
        return participants_dict;
    }

    function timeToSeconds(time) {
        // time is in the format HH:MM:SS,MILISECONDS, e.g., 00:00:53,531
        let timeArray = time.split(":");
        let hours = parseInt(timeArray[0]);
        let minutes = parseInt(timeArray[1]);
        let seconds = parseInt(timeArray[2].split(",")[0]);
        let milliseconds = parseInt(timeArray[2].split(",")[1]);

        return hours*3600 + minutes*60 + seconds + milliseconds/1000;
    }

    function seekTo(time) {
        videoPlayer.currentTime = timeToSeconds(time);
        videoPlayer.play();
    }

    function findExcerptByQuote(transcript_list,quote) {
        for(let i=0; i < transcript_list.length; i++) {
            let excerpt = transcript_list[i];
            if(excerpt.dialogue.includes(quote)) {
                return excerpt;
            }
        }
        return null;
    }

    function highlightPositive() { 
        const selection = window.getSelection().toString();
        if(selection) {
            let feedback = {quote: selection, type: "positive"};
            let excerpt_reference = findExcerptByQuote(recording.transcript_list, selection);
            if(!excerpt_reference) {
                console.log("Error: Corresponding transcript excerpt not found")
                return;
            }
            feedback.dialogue_id = excerpt_reference.id;
            feedback.speaker=excerpt_reference.speaker;
            feedback_list.push(feedback);
            feedback_list=feedback_list;
            positive_feedback.push(feedback);
            positive_feedback=positive_feedback;
            autoHighlightFeedback([feedback]);
            
        }
    }

    function highlightCritical() {
        const selection = window.getSelection().toString();
        if(selection) {
            let feedback = {quote: selection, type: "critical"};
            let excerpt_reference = findExcerptByQuote(recording.transcript_list, selection);
            if(!excerpt_reference) {
                console.log("Error: Corresponding transcript excerpt not found")
                return;
            }
            feedback.dialogue_id = excerpt_reference.id;
            feedback.speaker=excerpt_reference.speaker;
            feedback_list.push(feedback);
            feedback_list=feedback_list;
            critical_feedback.push(feedback);
            critical_feedback=critical_feedback;
            autoHighlightFeedback([feedback]);
        }
    }

    function removeHighlight() {

    }
</script>

<div div class="row spaced" id="feedback-selector-page">
    <div id="left-panel" class="column spaced" style="padding-bottom: 1rem;">

        <div id="transcript-area" class="column bordered spaced">
            {#if recording && recording.transcript_list}
                <p class="spaced padded"> 
                    {#each recording.transcript_list as excerpt, i}
                        <span class="timestamp" on:click={() => seekTo(excerpt.start_timestamp)}>[{excerpt.start_timestamp}]</span> - <span class="timestamp" on:click={() => seekTo(excerpt.end_timestamp)}>[{excerpt.end_timestamp}]</span><br>
                        {excerpt.speaker}: {@html excerpt.dialogue} <br><br>

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
                                    participants = getParticipants(recording.transcript_list); 
                                    // displayTranscript(recording.transcript_list, feedback_list);
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
                                    participants = getParticipants(recording.transcript_list); 
                                    console.log(participants);
                                    // displayTranscript(recording.transcript_list, feedback_list);
                                    is_loading=false;
                                }} 
                        disabled={is_loading || !files || files.length===0}> Upload files</button> 
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
                            feedback_list =  await autoDetectFeedback(recording.transcript_list);
                            autoHighlightFeedback(feedback_list);
                            // displayTranscript(recording.transcript_list, feedback_list);
                            is_loading=false;
                        }}
                    > 
                        <img src="./logos/magnifying-glass-for-search-3-svgrepo-com.svg" alt="Auto-detect Feedback" class="logo">
                        Auto-detect <br> Feedback
                    </button>
                    <button class="action-button"
                        disabled={!recording || !recording.transcript_list || is_loading || !window.getSelection()}
                        on:click={highlightPositive}
                    > 
                        <img src="./logos/highlight-green-svgrepo-com.svg" alt="Highlight Positive Feedback" class="logo">
                        Highlight <br> Positive
                    </button>
                    <button class="action-button"
                        disabled={!recording || !recording.transcript_list || is_loading || !window.getSelection()}
                        on:click={highlightCritical}
                    > 
                        <img src="./logos/highlight-red-svgrepo-com.svg" alt="Highlight Critical Feedback" class="logo">
                        Highlight <br> Critical 
                    </button>
                    <button class="action-button"
                        disabled={!recording || !recording.transcript_list || is_loading || !window.getSelection()}
                        on:click={removeFeedback}
                    > 
                        <img src="./logos/delete-svgrepo-com.svg" alt="De-highlight Feedback" class="logo">
                        Remove <br> Feedback
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div id="right-panel" class="column spaced" style="padding-bottom: 1rem;">
        <div id="media-player-area" class="bordered">
            {#if recording && recording.video}
                <video bind:this={videoPlayer} src={recording.video} controls style="width: 100%; height: 100%;">
                    <track kind="captions" src="blank.vtt" srclang="en">
                </video>
            {:else if recording && recording.audio}
                <audio src={recording.audio} controls style="width: 100%; height: auto;"></audio>
            {:else}
                <video bind:this={videoPlayer} src="video.mp4" controls style="width: 100%; height: 100%;">
                    <track kind="captions" src="blank.vtt" srclang="en">
                </video>
            {/if}
        </div>
        <div id="feedback-details-area" class="bordered padded spaced">
            <h3 style="font-weight: bold; text-decoration: underline;"> Discussion Transcript Details </h3>

            {#if recording && recording.video && recording.transcript_list}
                <strong> Number of participants: {Object.keys(participants).length}</strong> <br>
                <ul>
                    {#each Object.entries(participants) as [pa,count]}
                        <li> - {pa}: {count} utterances</li>
                    {/each}
                </ul>
                <br>
                {#if feedback_list}
                    <strong> Number of feedback utterances: {feedback_list.length} </strong>
                    <ul>
                        <li> - Number of positive feedback: {positive_feedback.length}  </li>
                        <li> - Number of critical feedback: {critical_feedback.length}</li>
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

    mark:hover {
        cursor: pointer;
    }

    span.timestamp:hover{
        /* font-weight: bold; */
        color: blue;
        cursor: pointer;
    }

</style>