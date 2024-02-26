<script>
    let is_enabled = false; 

    export let recordings = [];
    let selected_recordings = [];
    let messages = [];

    function viewTranscript(transcript) {
        alert(transcript);
    }

    async function startChatbot() {
        
        // Send transcripts to server 
        // A) Server-side: 
        // 1) Divide to chunks
        // 2) Embed each chunk 
        let recording_transcripts = [];
        for (let i = 0; i < selected_recordings.length; i++) {
            let recording = selected_recordings[i];
            let transcript = recording.transcription;
            recording_transcripts.push(transcript);
        }

        const embed_response = await fetch("/embed_transcripts", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({transcripts: recording_transcripts})
        });

        if(!embed_response.ok) {
            throw new Error("Failed to embed transcripts");
        } 

        // 3) Send initial message to ChatGPT
        const initial_response = await fetch("/chatbot_init_message", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({transcripts: recording_transcripts})
        });

        if(!initial_response.ok) {
            throw new Error("Failed to receive initial message from ChatGPT");
        }

        // 4) Send response back here to client
        const initial_json = await initial_response.json();
        let initial_message = initial_json["chatbot_init_message"];
        is_enabled = true; 

        messages = [...messages, {role: "Chatbot", text: initial_message}];
    }

    


</script>

<div class="column centered spaced">   
    {#if !(is_enabled)}
        {#if recordings.length > 0}
            <h3> <b> Recordings </b> </h3>
            <p> Please select recordings to add into chatbot </p>
            {#each recordings as recording, i}
                <label>
                    <div id="recording" class="row centered spaced" class:selected = {selected_recordings.includes(recording)}>
                        Recording {i+1}: 
                        <!-- <video class="rounded-lg" controls>
                            <source src={recording.video} type="video/mp4">
                            Your browser does not support the video tag.
                        </video> -->
                        <audio class="rounded-lg" controls>
                            <source src={recording.audio} type="audio/webm">
                        </audio>
                        <!-- <p class="centered"> {recording.transcription} </p> -->
                    </div>
                    <input type="checkbox" bind:group={selected_recordings} value={recording} />
                </label>
                <button on:click|preventDefault={()=>viewTranscript(recording.transcription)}> View Transcript </button>
            {/each}

            <button disabled={selected_recordings.length <= 0} on:click|preventDefault={()=>startChatbot()}> Start Chatbot </button>

        {:else}
            <p class="centered"> No recordings added yet. Make or add your own recordings in the Capture Panel. </p>
        {/if}
    {:else}
        <h3> <b> Chatbot </b> </h3>
        <div id="messages" class="column spaced">
            {#each messages as message, i}
                <div id="message" class="column spaced">
                    <strong> {message.role} </strong>
                    <p>{message.text}</p>
                </div>
            {/each}
        </div>
        <div id="input" class="row centered spaced">
            <input type="text" id="user" placeholder="Type a message..." />
            <button id="send"> Send </button>
        </div>
            
    {/if}

    

</div>


<style>
    #messages{
        justify-content: flex-start;
        align-items: flex-start;
        overflow-y:auto; 
    }

    #user {
        background-color: white;
    }

    #assistant {
        background-color: lightgray;
    }

    .selected:hover {
        border: 0.25rem solid blue;
    }

    .selected {
        border: 0.25rem solid blue;
    }

    #recording:hover {
        cursor:pointer;
        border: 0.25rem solid lightgray;
    }

    input[type="checkbox"] {
        opacity: 0;
        position: fixed;
        width:0; 
    }

</style>