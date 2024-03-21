<script>
    import SvelteMarkdown from 'svelte-markdown';
    
    let is_enabled = false; 
    let is_loading = false;

    export let recordings = [];
    let selected_recordings = [];
    let messages = [];
    let inputMessage ="";

    function viewTranscript(transcript) {
        alert(transcript);
    }

    async function sendMessage(message) {
        inputMessage = "";
        messages = [...messages, {role: "User", text: message}];
        const response = await fetch("/message_chatbot", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({message: message})
        });

        if(!response.ok) {
            throw new Error("Failed to send message to ChatGPT");
        }

        const json = await response.json();
        let chatbot_response = json["chatbot_response"];
        messages = [...messages, {role: "Chatbot", text: chatbot_response}];
        
    }

    async function startChatbot() {
        
        // Get transcripts from selected recordings
        let recording_transcripts = [];
        for (let i = 0; i < selected_recordings.length; i++) {
            let recording = selected_recordings[i];
            let transcript = recording.transcription;
            recording_transcripts.push(transcript);
        }

        // Send transcripts to server, divide into chunks, and embed each chunk
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



<div id="chatbot-page" class="column centered spaced" style="position:relative; height:100%;">   
    {#if !(is_enabled)}
        <h3> <b> Recordings </b> </h3>
        <p> Please select recordings to add into chatbot </p>
        <div id="recordings-panel" class="spaced padded bordered {recordings.length > 0 ? "grid" : "column centered"}">
            {#if recordings.length > 0}
                {#each recordings as recording, i}
                    <div id="recording" class="column centered spaced bordered padded" class:selected = {selected_recordings.includes(recording)}>
                        <label>
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
                        <input type="checkbox" bind:group={selected_recordings} value={recording} />
                        </label>
                        {#if recording.transcription}
                            <button on:click|preventDefault={()=>viewTranscript(recording.transcription)}> View Transcript </button>
                        {:else}
                            <span> No transcription available </span>
                        {/if}
                    </div>
                {/each}
            {:else}
                <p class="centered"> No recordings added yet. Make or add your own recordings in the Capture Panel. </p>
            {/if}
        </div>
        <button disabled={selected_recordings.length <= 0} on:click|preventDefault={()=>startChatbot()}> Start Chatbot </button>
    {:else}
        <div id="messages" class="column spaced">
            {#each messages as message, i}
                <div id={message.role} class="column spaced">
                    <strong> {message.role} </strong>
                    <SvelteMarkdown source={message.text} />
                </div>
            {/each}
            <div id="white-gap" class="padded"> </div>
        </div>
        <div id="input" class="row centered padded spaced bordered">
            <textarea bind:value="{inputMessage}" id="user" placeholder="Type a message..."></textarea>
            <button id="send" on:click|preventDefault={()=>sendMessage(inputMessage)}> Send </button>
        </div>
    {/if}

    

</div>


<style>

    #chatbot-page {
        position: relative;
        height: 100%;
        width: auto;
    }

    #recordings-panel {
        position: relative;
        height: 85%;
        width: 100%;
    }

    #messages{
        justify-content: flex-start;
        align-items: flex-start;
        overflow-y:auto; 
        width: 100%;
        height: 82%;
    }

    #white-gap{
        height: 30%;
        width: 100%;
        background-color: white;
        color:white;
    }

    .grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-gap: 10px;
        
    }

    #input {
        width: 100%;
        height: 18%;
    }

    #user {
        background-color: white;
    }

    #assistant {
        background-color: lightgray;
    }

    #input textarea#user {
        width:100%;
        height:100%;
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