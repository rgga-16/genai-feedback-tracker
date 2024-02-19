<script>
    // https://www.youtube.com/watch?v=g8FyESxBLfk
    let recordings_list = [];
    let is_recording=false;
    let is_paused=false;

    let videoStream;
    let micStream;
    let settings;
    let videoE1;
    let micE1;
    let micBlobs=[];

    let videoRecorder;
    let micRecorder;


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
                videoE1.src = URL.createObjectURL(event.data);
                console.log(URL.createObjectURL(event.data));
            }
        });

        micStream = await navigator.mediaDevices.getUserMedia({audio: true});
        micRecorder = new MediaRecorder(micStream);
        micRecorder.audioBlobs = [];
        micRecorder.addEventListener('dataavailable', event => {
            if (event.data.size > 0) {
                micRecorder.audioBlobs.push(event.data);
                micBlobs.push(event.data);
                micE1.src = URL.createObjectURL(event.data);
                console.log(URL.createObjectURL(event.data));
                
            }
        });
        micRecorder.addEventListener('stop', () => {
            downloadAudioRecording(micRecorder.audioBlobs);
            micBlobs = [];
        });

        videoRecorder.start();
        micRecorder.start();
    }

    function downloadAudioRecording(micBlobs) {
        const blob = new Blob(micBlobs, {type: 'audio/webm'});
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'audio.webm';
        a.click();
    }

    async function stopRecording() {
        is_recording=false;
        is_paused=false;

        videoStream.getTracks().forEach(track => track.stop());
        micStream.getTracks().forEach(track => track.stop());

        
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
        <!-- {#if recordings_list.length > 0}

        {:else}
            <p class="text-sm dark:text-gray-400">No captures made yet.</p>
            
        {/if} -->
    </div>

    <div class="container mx-auto">
        <video bind:this={videoE1} controls autoplay ></video>
    </div>

    <div class = "container mx-auto">
        <audio bind:this={micE1} controls autoplay></audio>
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
    {#if settings}
        <pre>{JSON.stringify(settings,null,2)}</pre>
    {/if}


    
</div>