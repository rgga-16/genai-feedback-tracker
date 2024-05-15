<script>
    // https://www.youtube.com/watch?v=g8FyESxBLfk
    export let recordings = [];
    export let selectedRecording; 
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

    function viewTranscript(transcript) {
        alert(transcript);
    }

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

    async function stopRecording() {
        is_recording=false;
        is_paused=false;
        is_loading=true; 

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
        // file_load_status="Extracting video frames from transcript timestamps...";
        // let timestamp_frames = await extractFrames(videoPath, transcript);

        let newRecording = {video: videoSrc, audio: micSrc, transcription: transcript};

        recordings = [...recordings, newRecording];
        await incrementRecordNumber();
        file_load_progress=100;
        is_loading=false;
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

    async function extractFrames(videoPath, transcript) {
        const response = await fetch('/extract_frames_per_timestamp', {
            method: 'POST',
            body: JSON.stringify({"video_path": videoPath, "transcript": transcript}),
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if(!response.ok) {
            throw new Error('Failed to extract frames');
        } else {
            const json = await response.json();
            let timestamp_frames = json["timestamp_frames"];
            return frames;
        }
    }

    async function handleFilesUpload() {
        is_loading=true;
        if(files) {
            for (const file of files) {
                if(file.type.includes('video')) {
                    let videoSrc = URL.createObjectURL(file);
                    file_load_status="Retrieving audio...";
                    file_load_progress=10;
                    [micPath, videoPath] = await extractAudioFromVideo(file);
                    console.log({micPath, videoPath});
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

                    let newRecording = {video: videoSrc, audio: micSrc, transcription: transcript};
                    recordings = [...recordings, newRecording];
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
                    let newRecording = {video: null, audio: audioSrc, transcription: transcript};
                    recordings = [...recordings, newRecording];
                    micPath=null;
                    videoPath=null;
                    await incrementRecordNumber();
                }
            }
            // Clear the file input
            files=null;
            file_input.value='';
        }
    is_loading=false;
    }
</script>


<div class="column spaced" id="capture-page">
    <div id="recordings-panel" class="spaced padded bordered {recordings.length > 0 ? "grid" : "column centered"}" >
        {#if recordings.length > 0}
            {#each recordings as recording, i}
                <label for="option_{i}" class="recording column centered spaced bordered padded" class:selected={recording===selectedRecording}>
                    <input type="radio" bind:group={selectedRecording} name="option_{i}" value={recording}>
                    <span> <strong> Recording {i+1} </strong></span>
                    {#if recording.video}
                        <video src={recording.video} controls>
                            <track kind="captions" src="blank.vtt" srclang="en">
                        </video>
                    {:else if recording.audio}
                        <audio src={recording.audio} controls></audio>
                    {:else}
                        <span> No video and audio available </span>
                    {/if}
                    
                </label>
            {/each}
        {:else if is_loading}
            <label for="progress-bar">{file_load_status}</label>
            <progress id="progress-bar" value={file_load_progress} max=100></progress>
        {:else}
            <p >No recordings made yet. Please make a recording or upload your own.</p>
        {/if}
    </div>
    

    <div id="action-panel" class="row spaced centered bordered">
        <div class="column centered">
            <span>Screen record your video</span>
            <div class="row spaced">
                <button class="action-button" on:click={startRecording} disabled={is_recording || is_paused}>
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
                <button class="action-button" on:click={() => stopRecording()} disabled={!is_recording && !is_paused}>
                    <img src="./logos/record-video-stop-svgrepo-com.svg" alt="Stop recording" class="logo">
                    Stop
                </button>
            </div>
        </div>

        <span>or</span>

        <div class="column centered spaced">
            <label for="file_upload" >Upload your own video or audio recording: </label>
            <input name="file_upload" bind:files bind:this={file_input} type="file" id="file_upload" accept="video/*, audio/*" multiple/>
            <button on:click={()=> {handleFilesUpload(); }} disabled={is_loading}> Upload files</button> 
        </div>
    </div>

        
</div>

<style>
    #capture-page {
        position: relative;
        height:100%;
        width:100%;
    }

    #recordings-panel {
        position: relative;
        height: 85%;
        width: 100%;
    }

    #action-panel {
        position: relative;
        height: 15%;
        width: 100%;
    }

    video {
        height: 40%;
        max-height: 200px;
        width: 100%;
    }


    .action-button{
        height: 100%;
        width: auto; 
        border: 0 none;
    }

    .grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-gap: 10px;
        
    }

    .selected:hover {
        border: 0.25rem solid blue;
    }

    .selected {
        border: 0.25rem solid blue;
    }

    .recording:hover {
        cursor:pointer;
        border: 0.25rem solid lightgray;
    }

    /* .recording input[type="radio"] {
        opacity: 0;
        position: fixed;
        width:0; 
    } */
</style>