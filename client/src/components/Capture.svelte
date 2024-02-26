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

    function viewTranscript(transcript) {
        alert(transcript);
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

    async function downloadVideo(vidChunks) {
        const blob = new Blob(vidChunks, {type: 'video/webm'});
        console.log("video blobs", {vidChunks, blob});
        let data = new FormData();
        data.append('file', blob, 'video.webm');
    }

    async function sendVideoToServer(videoBlobs) {

        const vidblob = new Blob(videoBlobs, {type: 'video/webm'});
        // BUG: videoBlobs is empty.
        console.log("video blobs", {videoBlobs, vidblob});
        let data = new FormData();
        data.append('file', vidblob, 'video.webm');
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
            // let transcript_path = json["transcript_path"];
            // let transcript_with_timestamps_path = json["transcript_with_timestamps_path"];
            
            return transcript
        }
    }


    async function stopRecording() {
        is_recording=false;
        is_paused=false;

        videoStream.getTracks().forEach(track => track.stop());
        micStream.getTracks().forEach(track => track.stop());

        micRecorder.stop();
        videoRecorder.stop();

        console.log("videoChunks", videoChunks);
        
        videoPath = await sendVideoToServer(videoChunks); 
        videoChunks = [];
        let videoSrc = await fetchVideo(videoPath);
        
        micPath = await sendAudioToServer(micBlobs); 
        micBlobs = [];
        let micSrc = await fetchAudio(micPath);

        let transcript = await transcribeMic(micPath);

        
        
        let newRecording = {video: videoSrc, audio: micSrc, transcription: transcript};

        recordings = [...recordings, newRecording];
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

</script>


<div class="column centered spaced bordered">
    <div id="recordings-panel" class="column centered spaced bordered">
        {#if recordings.length > 0}
            {#each recordings as recording, i}
                <div class="row centered space">
                    <span >Recording {i+1}</span>
                    <div class="column centered space">
                        <!-- BUG: micPath and videoPath are incorrect.  -->
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
    .container {
        max-width: 100%;
    }
    .block {
        display: block;
    }
    .dark\:text-gray-400 {
        --text-opacity: 1;
        color: #cbd5e0;
        color: rgba(203,213,224,var(--text-opacity));
    }
</style>