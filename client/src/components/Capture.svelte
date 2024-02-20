<script>
    // https://www.youtube.com/watch?v=g8FyESxBLfk
    let recordings_list = [];
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


    async function startRecording() {
        is_recording = true;

        videoStream = await navigator.mediaDevices.getDisplayMedia({
            video: {frameRate:60},
            //@ts-ignore
            selfBrowserSurface:'include',
        })
        videoRecorder = new MediaRecorder(videoStream, {mimeType: 'video/webm;codecs=vp9'});
        videoRecorder.addEventListener('dataavailable', event => {
            if (event.data.size > 0) {
                videoChunks.push(event.data);
                // videoE1.src = URL.createObjectURL(event.data);
                // console.log(URL.createObjectURL(event.data));
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
                // micE1.src = URL.createObjectURL(event.data);
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
            micPath = json["filepath"]
        }
        return micPath;
    }

    async function sendVideoToServer(videoBlobs) {
        const blob = new Blob(videoBlobs, {type: 'video/webm'});
        let data = new FormData();
        data.append('video', blob, 'video.webm');
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
            videoPath = json["filepath"]
        }
        return videoPath;
    }

    async function transcribeMic() {
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
            let transcript_path = json["transcript_path"];
            let transcript_with_timestamps_path = json["transcript_with_timestamps_path"];
            let transcript = json["transcript_with_timestamps"]
            return transcript, transcript_path, transcript_with_timestamps_path;
        }
    }


    async function stopRecording() {
        is_recording=false;
        is_paused=false;

        videoStream.getTracks().forEach(track => track.stop());
        micStream.getTracks().forEach(track => track.stop());

        micRecorder.stop();
        videoRecorder.stop();

        

        videoPath = await sendVideoToServer(videoChunks);
        videoChunks = [];

        micPath = await sendAudioToServer(micBlobs);
        micBlobs = [];
        console.log('videoPath', videoPath);
        console.log('micPath', micPath);
        let newRecording = {video: videoPath, audio: micPath, transcription: null };
        if(micPath && videoPath) {
            let transcript, transcript_path, transcript_with_timestamps_path = await transcribeMic();
            newRecording.transcription = transcript;
        }
        
        recordings_list = [...recordings_list, newRecording];
        console.log(recordings_list);
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


<div class="container mx-auto relative py-4">

    <div id='captures-panel' class="container mx-auto">
        {#if recordings_list.length > 0}
            {#each recordings_list as recording, i}
                <div class="container mx-auto block">
                    <p class="dark:text-gray-400">Recording {i+1}</p>
                    <div class="container mx-auto">
                        <!-- BUG: micPath and videoPath are incorrect.  -->
                        {#if recording.video}
                            <video src={recording.video} controls></video>
                        {/if}
                        {#if recording.audio}
                            <audio src={recording.audio} controls></audio>
                        {/if}
                    </div>
                </div>
                
            {/each}
        {:else}
            <p class="text-sm dark:text-gray-400">No captures made yet.</p>
            
        {/if}
    </div>

    <div id='action-panel' class="container  block mx-auto">

        <button class="dark:text-gray-400" on:click={startRecording} disabled={is_recording || is_paused}>Record</button>
        <!-- {#if is_paused}
            <button class="dark:text-gray-400" on:click={() => resumeRecording()} disabled={!is_paused}>Resume</button>
        {:else}
            <button class="dark:text-gray-400" on:click={() => pauseRecording()} disabled={!is_recording || is_paused}>Pause</button>
        {/if} -->
        <button class="dark:text-gray-400" on:click={() => stopRecording()} disabled={!is_recording && !is_paused}>Stop</button>
    </div>

</div>

<style>
    #captures-panel {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    #action-panel {
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
    }
    video {
        height: 15%;
        max-height: 200px;
        width: auto;
    }
    audio {
        width: 100%;
        height: auto;
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