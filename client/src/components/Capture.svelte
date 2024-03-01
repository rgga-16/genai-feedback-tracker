<script>
    // https://www.youtube.com/watch?v=g8FyESxBLfk
    export let recordings = [];
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

    let files;

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
        // let vidblob = videoBlobs[0]; // workaround to resolve the following bug where creating a new Blob from videoBlobs ends up being empty.
        
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

        videoStream.getTracks().forEach(track => track.stop());
        micStream.getTracks().forEach(track => track.stop());

        videoPath = await sendVideoToServer(videoChunks); //Bug workaround: Do this for the first time because newly created vidblob is empty during first time.
        videoPath = await sendVideoToServer(videoChunks); 
        videoChunks = [];
        let videoSrc = await fetchVideo(videoPath);
        
        micPath = await sendAudioToServer(micBlobs); 
        micBlobs = [];
        let micSrc = await fetchAudio(micPath);

        let transcript = await transcribeMic(micPath);

        let newRecording = {video: videoSrc, audio: micSrc, transcription: transcript};

        recordings = [...recordings, newRecording];
        await incrementRecordNumber();
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
            let frames = json["frames"];
            return frames;
        }
    }

    async function handleFilesUpload() {
        if(files) {
            for (const file of files) {
                if(file.type.includes('video')) {
                    let videoSrc = URL.createObjectURL(file);
                    [micPath, videoPath] = await extractAudioFromVideo(file);

                    console.log({micPath, videoPath});

                    if(!micPath) {
                        micPath = null;
                        videoPath = null;
                        throw new Error('Failed to extract audio from video');
                    } 
                    let micSrc = await fetchAudio(micPath);
                    let transcript = await transcribeMic(micPath);

                    // let frames = await extractFrames(videoPath, transcript);

                    let newRecording = {video: videoSrc, audio: micSrc, transcription: transcript};
                    recordings = [...recordings, newRecording];
                    micPath=null;
                    videoPath=null;
                    await incrementRecordNumber();
                } else if(file.type.includes('audio')) {
                    let audioSrc = URL.createObjectURL(file);
                    // Save the audio file and get its path
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
        }
    }
</script>


<div class="column centered spaced" id="capture-page">
    <div id="recordings-panel" class="spaced padded bordered {recordings.length > 0 ? "grid" : "column centered"}" >
        {#if recordings.length > 0}
            {#each recordings as recording, i}
                <div class="column centered spaced bordered">
                    <span> <strong> Recording {i+1} </strong></span>
                    {#if recording.video}
                        <video src={recording.video} controls></video>
                    {:else}
                        <span> No video available </span>
                    {/if}
                    {#if recording.audio}
                        <audio src={recording.audio} controls></audio>
                    {:else}
                        <span> No audio available </span>
                    {/if}
                    {#if recording.transcription}
                        <button on:click|preventDefault={()=>viewTranscript(recording.transcription)}> View Transcript </button>
                    {:else}
                        <span> No transcription available </span>
                    {/if}
                </div>
            {/each}
        {:else}
            <p >No recordings made yet.</p>
        {/if}
    </div>
    
    <div id='action-panel' class="row centered spaced padded bordered">

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

        <div class="column centered spaced bordered">
            <label >Upload your own video or audio: </label>
            <input bind:files type="file" id="file_upload" accept="video/*, audio/*" on:change={()=>handleFilesUpload()}/>
        </div>
    </div>
</div>

<style>

    #capture-page {
        position: relative;
        height:100%;
        width:auto;
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


</style>