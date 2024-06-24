<script>
    import { prevent_default } from 'svelte/internal';

    import {timeToSeconds, seekTo, focusOnFeedback} from '../utils.js';

    export let feedback_list;
    export let recording; 

    let mediaPlayer;
    let inputMessage = "";
    
    let selected_feedback; 

    let active_right_tab=0;  
    let active_left_tab=0;
    let chatbot_messages = [{
        "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
        "role": "system"
    }];

    let contexts = [];


    let left_panel_tabs = [
        "Critical Feedback", "Positive Feedback"
    ]
    let right_panel_tabs = [
        "Transcript", "Chatbot"
    ]

    let is_loading=false; 
    let load_status = "";



    async function paraphrasePositively(feedback_quote, excerpt) {
        const response = await fetch("/positively_paraphrase_feedback", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({feedback: feedback_quote, excerpt: excerpt})
        });
        if(!response.ok) {
            throw new Error("Failed to detect feedback");
        }
        const json = await response.json();
        let paraphrased_feedback = json["paraphrased_feedback"];
        return paraphrased_feedback;   
    }

    function removeFeedback(feedback) {
        if (selected_feedback === feedback) {
            selected_feedback = null;
        }
        feedback_list = feedback_list.filter(f => f !== feedback);
        feedback_list=feedback_list;
    }

    function selectFeedback(feedback, event) {
        selected_feedback = feedback;
        event.stopPropagation(); // Prevents the event from bubbling up to the window
    }

    function deselectFeedback() {
        selected_feedback = null;
    }

    function showParaphrasedQuote(feedback,show=true) {
        feedback.show_paraphrased = show;
    }

    async function generateTask(feedback_quote, excerpt) {
        const response = await fetch("/generate_task", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({feedback: feedback_quote, excerpt: excerpt})
        });
        if(!response.ok) {
            throw new Error("Failed to generate task");
        }
        const json = await response.json();
        let task = json["task"];
        return task;   
    }

    let sortKey = null;
    let sortAscending = true;

    function sortFeedbackList(key) {
        if (sortKey === key) {
            sortAscending = !sortAscending;
        } else {
            sortKey = key;
            sortAscending = true;
        }

        feedback_list.sort((a, b) => {
            if (a[key] < b[key]) return sortAscending ? -1 : 1;
            if (a[key] > b[key]) return sortAscending ? 1 : -1;
            return 0;
        });
        feedback_list = feedback_list;
    }

    async function sendMessage(inputMessage, contexts=null) {
        if(inputMessage.trim() === "") {
            alert("Please enter a message.");
            return;
        }
        

        if (contexts && contexts.length > 0) {
            let context_string = "\n\nHere are the pieces of feedback as context.";
            for(let i =0; i < contexts.length; i++) {
                let context = contexts[i];
                console.log(context);
                context_string += "\nFeedback #"+context.id+": \""+context.speaker+": "+context.quote+"\".";
            }
            inputMessage += context_string;
        }

        chatbot_messages.push({role: "user", content: inputMessage});
        chatbot_messages = chatbot_messages;
        feedback_list = feedback_list;

        const response = await fetch("/message_chatbot", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({message_history: chatbot_messages, message: inputMessage})
        });
        if(!response.ok) {
            throw new Error("Failed to send message");
        }
        const json = await response.json();
        let chatbot_response = json["chatbot_response"];
        
        chatbot_messages.push({role: "assistant", content: chatbot_response});
        chatbot_messages = chatbot_messages;
        feedback_list = feedback_list;
        console.log(feedback_list)
    }

    function addContext(feedback) {
        if (!contexts.includes(feedback)) {
            contexts.push(feedback);
            contexts = contexts;
            console.log(contexts);
        } else {
            alert("This feedback is already added to the context.");
        }
    }

    
</script>

<div id="feedback-list-page" class="spaced" on:window:click={deselectFeedback}>
    <div id="left-panel" class="column">
        <div class="tabbed-area bordered">
            <div class="tab-header" >
                {#each left_panel_tabs as tab, i}
                    <button class="tab" on:click={()=>{
                            active_left_tab=i;
                        }} 
                        class:active={i===active_left_tab} class:right-bordered={i<left_panel_tabs.length-1} >{tab}</button>
                {/each}
            </div>
            <div class="tab-content padded" style="overflow-y: auto;">
                {#if active_left_tab===0}
                    <div class="column" style="overflow-y: auto;">
                        <div class="feedback-header row" >
                            <span style="width:3%;" class="centered">
                                <strong>ID</strong>
                            </span>
                            <span style="width:60%;" class="centered row spaced">
                                <strong>Feedback</strong>
                                <button class="action-button" on:click={() => sortFeedbackList('quote')}>
                                    {#if sortAscending && sortKey==='quote'}
                                        <img style="height: 1rem; width: 1rem;" src="./logos/ascending-sort-svgrepo-com.svg" alt="Sort ascending" class="mini-icon">
                                    {:else}
                                        <img style="height: 1rem; width: 1rem;" src="./logos/descending-sort-svgrepo-com.svg" alt="Sort descending" class="mini-icon">
                                    {/if}
                                </button>
                            </span>
                            <span style="width:10%;" class="centered row spaced">
                                <strong>Speaker</strong>
                                <button class="action-button" on:click={() => sortFeedbackList('speaker')}>
                                    {#if sortAscending && sortKey==='speaker'}
                                        <img style="height: 1rem; width: 1rem;" src="./logos/ascending-sort-svgrepo-com.svg" alt="Sort ascending" class="mini-icon">
                                    {:else}
                                        <img style="height: 1rem; width: 1rem;" src="./logos/descending-sort-svgrepo-com.svg" alt="Sort descending" class="mini-icon">
                                    {/if}
                                </button>
                            </span>
                            <span id="feedback-buttons" style="width:20%;" class="centered row">
                                <strong>Actions</strong>
                            </span>
                            <span style="width:7%;" class="centered row spaced">
                                <strong>Done?</strong>
                                <button class="action-button" on:click={() => sortFeedbackList('done')}>
                                    <img style="height: 1rem; width: 1rem;" src={sortAscending && sortKey==='done' ? "./logos/ascending-sort-svgrepo-com.svg" :  "./logos/descending-sort-svgrepo-com.svg"} alt={sortAscending && sortKey==='done' ? "Sort ascending" : "Sort descending"} class="mini-icon">
                                </button>
                            </span>
                        </div>
                        {#each feedback_list as feedback, i}
                            {#if feedback.type==="critical"}
                                <div class="feedback-row row bordered padded" class:done={feedback.done} class:selected={feedback===selected_feedback} 
                                    on:click={(event) => {
                                        selectFeedback(feedback, event);
                                        contexts=[];
                                        addContext(feedback);
                                        focusOnFeedback(feedback);
                                    }}
                                >
                                    <span style="width:3%;">
                                        <strong> {feedback.id} </strong>
                                    </span>
                                    <div class="column" style="width:60%;">
                                        <span  class="">
                                            {#if feedback.positivised_quote && feedback.show_paraphrased}
                                                <strong>(Paraphrased Feedback)</strong> "{feedback.positivised_quote}" <span class="clickable" on:click={() => showParaphrasedQuote(feedback, false)}>(View original quote)</span>
                                            {:else}
                                                "{feedback.quote}" {#if feedback.positivised_quote && !feedback.show_paraphrased } <span class="clickable" on:click={() => showParaphrasedQuote(feedback, true)}>(View paraphrased quote)</span> {/if}
                                            {/if}
                                        </span>
                                        <span>
                                            <strong>Task: </strong> 
                                            {#if feedback.task}
                                                {feedback.task}
                                                <button class="action-button" on:click={async () => {
                                                    feedback.task = await generateTask(feedback.quote, feedback.excerpt_reference.dialogue);
                                                    feedback_list = feedback_list;
                                                }}>
                                                    <img src="./logos/ai-create-task.png" alt="Generate Task" class="mini-icon">
                                                </button>
                                            {:else}
                                                (None created yet)
                                                <button class="action-button" on:click={async () => {
                                                    feedback.task = await generateTask(feedback.quote, feedback.excerpt_reference.dialogue);
                                                    feedback_list = feedback_list;
                                                }}>
                                                    <img src="./logos/ai-add.png" alt="Generate Task" class="mini-icon">
                                                </button>
                                            {/if}
                                        </span>
                                    </div>
                                    <span style="width:10%; " class="centered">
                                        {feedback.speaker}
                                    </span>
                                    <div id="feedback-buttons" style="width:20%;" class="row centered spaced">
                                        <button class="action-button" on:click={async () => { 
                                            feedback.positivised_quote = await paraphrasePositively(feedback.quote, feedback.excerpt_reference.dialogue);
                                            showParaphrasedQuote(feedback, true);
                                            feedback_list = feedback_list;
                                        }}>
                                            <img src="./logos/ai-positive-paraphrase.png" alt="Paraphrase positively" class="action-icon">
                                        </button>
                                        <button class="action-button centered column" on:click={() => addContext(feedback)}>
                                            <img src="./logos/add-ellipse-svgrepo-com.svg" alt="Add feedback as context" class="action-icon">
                                            Add Context
                                        </button>
                                        <button class="action-button" on:click={() => removeFeedback(feedback)} >
                                            <img src="./logos/delete-svgrepo-com.svg" alt="Remove feedback" class="action-icon">
                                        </button>
                                        
                                    </div>
                                    <span style="width:7%;" class="centered">
                                        <input type="checkbox" bind:checked={feedback.done} />
                                    </span>
                                </div>
                            {/if}
                        {/each}
                    </div>
                {:else if active_left_tab===1}
                    <div class="grid">
                        {#each feedback_list as feedback, i}
                            {#if feedback.type==="positive"}
                                <div class="positive-feedback-note" class:selected={feedback===selected_feedback} on:click={(event) => selectFeedback(feedback, event)}>
                                    <p>
                                        "{feedback.quote}" 
                                    </p>
                                    <br>
                                    <span> - {feedback.speaker} </span>
                                </div>
                            {/if}
                        {/each}
                    </div>
                {/if}

            </div>
        </div>

    </div>

    <div id="right-panel" class="column ">
        <div class="tabbed-area bordered">
            <div class="tab-header">
                {#each right_panel_tabs as tab, i}
                    <button class="tab" on:click={()=>active_right_tab=i} class:active={i===active_right_tab} class:right-bordered={i<right_panel_tabs.length-1} >{tab}</button>
                {/each}
            </div>
            <div class="tab-content padded column spaced " >
                {#if active_right_tab===0}
                    <div id="media-player-area" class="bordered">
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
                    <div id="transcript-area" class="column bordered spaced">
                        {#if recording && recording.transcript}
                            <p class="spaced padded"> 
                                {#each recording.transcript_list as excerpt, i}
                                    <span class="timestamp" on:click={() => seekTo(excerpt.start_timestamp, mediaPlayer)}>[{excerpt.start_timestamp}]</span> - <span class="timestamp" on:click={() => seekTo(excerpt.end_timestamp, mediaPlayer)}>[{excerpt.end_timestamp}]</span>
                                    <br>
                                    {excerpt.speaker ? excerpt.speaker+":" : ""}  
                                    <span id={excerpt.id}>
                                        {@html excerpt.dialogue} 
                                    </span> <br><br>
                                {/each}
                            </p>
                        {/if}
                    </div>
                {:else if active_right_tab===1}
                    <div id="chatbot-messages" class="column spaced bordered">
                        <div class="assistant padded">
                            <p> <strong> assistant: </strong> Hello! How can I help you today? </p>
                        </div>
                        {#each chatbot_messages as message} 
                            {#if message.role != "system"}
                                <div class="{message.role} padded">
                                    <p> <strong> {message.role}: </strong> {message.content} </p>
                                </div>
                            {/if}
                        {/each}
                        <div class="assistant padded" style="height:50%;">
                            <p> <strong> assistant: </strong>  </p>
                            <!-- WIP -->
                            <div id="ld-bar-chatbot" class="ldBar centered column" data-preset="bubble" data-value=50 style="width:100%; height: 80%; z-index: 3;">
                                hello 
                            </div>
                        </div>
                        <div style="height: 20px; width: 100%; background-color:white; color:white; cursor: default;"> 
                            <p>Lorem ipsum dolor sit amet. Eos libero voluptatem sit excepturi rerum vel porro odio est eligendi voluptatibus. At mollitia quam ea dolorum quae aut nemo ipsum est asperiores quibusdam est voluptatem accusamus. Ut eligendi porro quo autem illum non voluptatem rerum et nobis nisi est molestiae facilis quo magni perferendis.
                            Ea Quis molestiae cum minus consequatur At velit internos et omnis neque qui nihil consequatur et acc</p>
                        </div> 
                    </div>

                    <div id="chatbot-actions" class="column padded spaced centered">
                        <div id="chatbot-utilities" class="row centered spaced">
                            <div id="contexts" class="column centered bordered">
                                <span><strong>Contexts:</strong></span>
                                {#if contexts.length > 0}
                                    {#each contexts as context}
                                        <div class="suggested-message"> Feedback #{context.id}: {context.quote.slice(0, 5)}... </div>
                                    {/each}
                                {:else}
                                    <span> None. Add by selecting from the feedback.</span>
                                {/if}
                            </div>
                            <div id="suggested-messages" class="row centered bordered">
                                <span><strong>Suggested messages:</strong></span>
                                <div class="suggested-message" on:click|preventDefault={
                                    async () => {
                                        await sendMessage("Can you explain the following feedback?",contexts=contexts);
                                    }
                                } >
                                    Explain feedback.
                                </div>
                                <div class="suggested-message" on:click|preventDefault={
                                    async () => {
                                        await sendMessage("Can you brainstorm the tasks to do to address the following feedback?",contexts=contexts);
                                    }
                                }>
                                    Brainstorm actions.
                                </div>
                            </div>
                            
                        </div>
                        <div id="chatbot-input" class="row spaced centered" >
                            
                            <textarea bind:value="{inputMessage}" style="width:100%;height:100%;" on:keydown="{e => e.key==='Enter' && sendMessage(inputMessage)}"  placeholder="Type your message here..." id="textarea"></textarea>
                            <button class="action-button centered column" on:click|preventDefault={async () => { 
                                    await sendMessage(inputMessage);
                                    inputMessage = "";
                                }}>
                                <img src="./logos/send-svgrepo-com.svg" alt="Send" class="action-icon">
                            </button>
                        </div>
                    </div>

                {/if}
            </div>


        </div>

        

        <!-- <div id="selected-feedback-area" class="bordered spaced column" >
            {#if selected_feedback}
                <div class="tab-header" style="overflow-y: hidden; width: 100%; height: 10%;">
                    {#each detail_tabs as tab, i}
                        <button class="tab" on:click={()=>{
                            setActiveDetailTab(i);
                        }} 
                        class:active={i===activeDetailTab} class:right-bordered={i<detail_tabs.length-1} >{tab}</button>
                    {/each}
                </div>
                <div class="tab-content " style="width: 100%; height: 90%;">
                    {#if activeDetailTab===0}
                        <span style="text-decoration: underline; margin-left: 1rem; margin-top: 1rem;" class=""><strong> Feedback details </strong></span>
                        <div id="feedback-details" class="column padded" style="overflow-y: auto;">
                            <p>
                                <span class="clickable" on:click={() => seekTo(selected_feedback.excerpt_reference.start_timestamp, mediaPlayer)}>[{selected_feedback.excerpt_reference.start_timestamp}]</span> - <span class="clickable" on:click={() => seekTo(selected_feedback.excerpt_reference.end_timestamp, mediaPlayer)}>[{selected_feedback.excerpt_reference.end_timestamp}]</span>
                                <br>
                                <span>{@html selected_feedback.excerpt_reference.dialogue}</span> 
                            </p>
                        </div>
                        <div id="feedback-action-buttons" class=" padded row spaced bordered centered" style="border-left:none; border-right:none; border-bottom:none;">
                            <button class="action-button centered column" on:click={async () => { 
                                    selected_feedback.positivised_quote = await paraphrasePositively(selected_feedback.quote, selected_feedback.excerpt_reference.dialogue);
                                    showParaphrasedQuote(selected_feedback, true);
                                    feedback_list = feedback_list;
                                }}>
                                <img src="./logos/ai-positive-paraphrase.png" alt="Paraphrase positively" class="action-icon">
                                Paraphrase positively
                            </button>
                            <button class="action-button" on:click={() => removeFeedback(selected_feedback)}>
                                <img src="./logos/delete-svgrepo-com.svg" alt="Remove feedback" class="action-icon">
                                Delete
                            </button>
                        </div>  
                    {:else if activeDetailTab===1}
                        <div id="chatbot-messages" class="column spaced">
                            <div class="assistant padded">
                                <p> <strong> assistant: </strong> Hello! How can I help you today? </p>
                            </div>
                            {#each selected_feedback.chatbot_messages as message} 
                                {#if message.role != "system"}
                                    <div class="{message.role} padded">
                                        <p> <strong> {message.role}: </strong> {message.content} </p>
                                    </div>
                                {/if}
                            {/each}
                            <div style="height: 20px; width: 100%; background-color:white; color:white; cursor: default;"> 
                                <p>Lorem ipsum dolor sit amet. Eos libero voluptatem sit excepturi rerum vel porro odio est eligendi voluptatibus. At mollitia quam ea dolorum quae aut nemo ipsum est asperiores quibusdam est voluptatem accusamus. Ut eligendi porro quo autem illum non voluptatem rerum et nobis nisi est molestiae facilis quo magni perferendis.
                                Ea Quis molestiae cum minus consequatur At velit internos et omnis neque qui nihil consequatur et acc</p>
                            </div> 
                        </div>
                        
                        <div id="chatbot-actions" class="column padded spaced centered">
                            <div id="suggested-messages" class="row centered spaced">
                                <div class="suggested-message" on:click|preventDefault={
                                    async () => {
                                        await sendMessage("Can you explain the following feedback: \"" + selected_feedback.quote + "\"?");
                                    }
                                } >
                                    Explain feedback.
                                </div>
                                <div class="suggested-message" on:click|preventDefault={
                                    async () => {
                                        await sendMessage("Can you brainstorm the tasks to do to address the following feedback: \"" + selected_feedback.quote + "\"?");
                                    }
                                }>
                                    Brainstorm actions.
                                </div>
                            </div>
                            <div id="chatbot-input" class="row spaced centered" >
                                
                                <textarea bind:value="{inputMessage}" style="width:100%;height:100%;" on:keydown="{e => e.key==='Enter' && sendMessage(inputMessage)}"  placeholder="Type your message here..." id="textarea"></textarea>
                                <button class="action-button centered column" on:click|preventDefault={async () => { 
                                        await sendMessage(inputMessage);
                                        inputMessage = "";
                                    }}>
                                    <img src="./logos/send-svgrepo-com.svg" alt="Send" class="action-icon">
                                </button>
                            </div>
                        </div>
                        
                    {/if}
                </div>
            {/if}
        </div> -->

    </div>

</div>

<style>

    #feedback-list-page{
        position:relative;
        display:flex;
        height:100%;
        width:100%;
    }

    #left-panel{
        position:relative;
        height:100%;
        width:60%;
        padding-bottom: 1rem;
    }

    .tabbed-area{
        height:100%;
        width:100%;
    }



    .tab-header{
        height:5%;
        width:100%;
        display:flex;
        flex-direction:row;
        border-bottom: 1px solid #ccc;
        border-radius: 2px;
        overflow-x:auto;
    }

    .tab-header button.tab {
        padding: 0.5rem 1rem;
        border-top: none;
        border-left: none;
        border-bottom: none ;
        background: #ddd;
        cursor: pointer;
    }

    .tab-header button.tab.active {
        background:#ccc;
        font-weight:bold;
        border-bottom:none;
    }

    .tab-content {
        height:95%;
        width:100%;
    }

    .right-bordered{
        border-right: 1px solid #000000;
    }

    .tab-header button.tab:active{
        background: #ccc;
        font-weight: bold;
    }

    .feedback-header {
        border-bottom: 1px solid #ccc;
    }

    .feedback-row:hover {
        border: 2px solid #000000;
        cursor:pointer;
    }

    .feedback-row.selected{
        border: 2px solid #000000;
    }

    #right-panel{
        position:relative;
        height:100%;
        width:40%;
        padding-bottom: 1rem;
    }

    #media-player-area{
        height:40%;
        width:100%;
    }

    #selected-feedback-area{
        height:60%;
        width:100%;
    }

    #transcript-area {
        height: 60%;
        width: 100%;
        overflow-y: auto; 
    }

    #feedback-details{
        height:70%;
        width:100%;
    }

    #feedback-action-buttons{
        height:30%;
        width:100%;
    }

    #chatbot-messages{
        padding-top:1rem;
        height:70%;
        width:100%;
        overflow-y: auto;
    }

    #chatbot-actions{
        height:30%;
        width:100%;
        background-color: rgb(201, 201, 201);
    }

    #chatbot-input{
        height:60%;
        width:100%;
    }

    #chatbot-utilities{
        height:40%;
        width:100%;
    }

    #suggested-messages{
        height:100%;
        width:70%;
        gap: 0.10rem;
    }

    #contexts{
        height:100%;
        width:30%;
        gap: 0.10rem;
    }

    .user {
        /* margin-left:1rem; */
		background-color: white;
		
	}
	.assistant {
        /* margin-right:1rem; */
		background-color: lightgray;
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

    .suggested-message {
        border: 1px dashed; 
        border-radius: 5px; 
        padding: 5px; 
        margin-bottom: 5px;
    }

    .suggested-message:hover {
        cursor: pointer;
        text-decoration: underline;
        border: 2px dashed;   
    }

    .action-button{
        height: 100%;
        width: auto; 
        border: 0 none;
    }

    .action-icon {
        height: 3rem;
        width: 3rem;
    }

    .mini-icon {
        height: 1.5rem;
        width: 1.5rem;
    }

    span.clickable {
        color: blue;
    }

    span.clickable:hover{
        /* font-weight: bold; */
        color: blue;
        text-decoration: underline;
        cursor: pointer;
    }


    .done {
        background-color: #ccc;
        opacity: 0.5;
        text-decoration: line-through; /* Add this line to strikeout the text */
    }

    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 20px;
        padding: 20px;
    }

    .positive-feedback-note {
        background-color: #d4edda;
        padding: 10px;
        border-radius: 5px;
    }

    .positive-feedback-note:hover {
        border: 2px solid #000000;
        cursor:pointer;
    }

    .positive-feedback-note.selected{
        border: 2px solid #000000;
    }
    
    

    

</style>