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
    
        // const vidblob = new Blob(videoBlobs, {type: 'video/webm'});
        const vidblob = videoBlobs[0]; // workaround to resolve the following bug where creating a new Blob from videoBlobs ends up being empty.
        
        console.log("video blobs", {videoBlobs, vidblob});
        let data = new FormData();
        data.append('file', vidblob);

        const response = await fetch('/download_screen', {
            method: 'POST',
            body: data,
        });
        if(!response.ok) {
            micPath = null;
            videoPath = null;
            throw new Error('Failed to send video to server');
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

        // micRecorder.stop();
        // videoRecorder.stop();
        
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
        alert('pause recording');
        is_recording=false;
        is_paused=true;
    }

    function resumeRecording() {
        alert('resume recording');
        is_recording=true;
        is_paused=false;
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
        return json["audiopath"];
    }

    async function handleFilesUpload() {
        if(files) {
            for (const file of files) {
                if(file.type.includes('video')) {
                    let videoSrc = URL.createObjectURL(file);
                    micPath = await extractAudioFromVideo(file);
                    if(!micPath) {
                        micPath = null;
                        videoPath = null;
                        throw new Error('Failed to extract audio from video');
                    } 
                    let micSrc = await fetchAudio(micPath);
                    let transcript = await transcribeMic(micPath);
                    let newRecording = {video: videoSrc, audio: micSrc, transcription: transcript};
                    recordings = [...recordings, newRecording];
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
                    await incrementRecordNumber();
                }
            }
            // Clear the file input
            files=null;
        }
    }
</script>


<div class="column centered spaced bordered">
    <div id="recordings-panel" class="column centered spaced bordered">
        {#if recordings.length > 0}
            {#each recordings as recording, i}
                <div class="row centered space">
                    <span >Recording {i+1}</span>
                    <div class="column centered space">
                        {#if recording.video}
                            <video src={recording.video} controls></video>
                        {/if}
                        {#if recording.audio}
                            <audio src={recording.audio} controls></audio>
                        {/if}
                    </div>
                    <button on:click|preventDefault={()=>viewTranscript(recording.transcription)}> View Transcript </button>
                </div>
            {/each}
        {:else}
            <p >No captures made yet.</p>
        {/if}
        <div class="row centered spaced bordered">
            <label >Upload your own video or audio: </label>
            <input bind:files type="file" id="file_upload" accept="video/*, audio/*" on:change={()=>handleFilesUpload()}/>

        </div>
    </div>

    <div id='action-panel' class="row centered space bordered">

        <button on:click={startRecording} disabled={is_recording || is_paused}>Record</button>
        <!-- {#if is_paused}
            <button class="dark:text-gray-400" on:click={() => resumeRecording()} disabled={!is_paused}>Resume</button>
        {:else}
            <button class="dark:text-gray-400" on:click={() => pauseRecording()} disabled={!is_recording || is_paused}>Pause</button>
        {/if} -->
        <button on:click={() => stopRecording()} disabled={!is_recording && !is_paused}>Stop</button>
    </div>

</div>

<style>

    video {
        height: 15%;
        max-height: 200px;
        width: auto;
    }


</style>