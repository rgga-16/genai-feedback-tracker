<script>
  import { prevent_default } from 'svelte/internal';

    
    import {timeToSeconds, seekTo} from '../utils.js';

    export let feedback_list;
    export let recording; 

    let mediaPlayer;
    let inputMessage = "";
    
    let selected_feedback; 

    // let messages = [
    //     {role: "assistant", text: "Hello! How can I help you today?"},
    //     {role: "user", text: "I need help with my feedback."},
    //     {role: "assistant", text: "Sure! What feedback would you like help with?"},
    //     {role: "user", text: "I have some critical feedback that I need to paraphrase positively."},
    //     {role: "assistant", text: "I can help with that. Please provide the feedback you would like to paraphrase."},
    //     {role: "assistant", text: "Hello! How can I help you today?"},
    //     {role: "user", text: "I need help with my feedback."},
    //     {role: "assistant", text: "Sure! What feedback would you like help with?"},
    //     {role: "user", text: "I have some critical feedback that I need to paraphrase positively."},
    //     {role: "assistant", text: "I can help with that. Please provide the feedback you would like to paraphrase."},
    // ];

    
    let activeTab=0;  
    let tabs = [
        "Critical Feedback", "Positive Feedback"
    ]

    let activeDetailTab = 0; 
    let detail_tabs = ["Feedback Details", "Chatbot"]

    function setActiveTab(index){
        activeTab=index; 
    }

    function setActiveDetailTab(index){
        activeDetailTab=index; 
    }

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

    async function sendMessage(inputMessage) {
        if(inputMessage.trim() === "") {
            alert("Please enter a message.");
            return;
        }
        selected_feedback.chatbot_messages.push({role: "user", content: inputMessage});

        const response = await fetch("/message_chatbot", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({message_history: selected_feedback.chatbot_messages, message: inputMessage})
        });
        if(!response.ok) {
            throw new Error("Failed to send message");
        }
        const json = await response.json();
        let chatbot_response = json["chatbot_response"];

        
        selected_feedback.chatbot_messages.push({role: "assistant", content: chatbot_response});
        selected_feedback.chatbot_messages = selected_feedback.chatbot_messages;
        feedback_list = feedback_list;
        console.log(feedback_list)

        
        
    }
</script>

<div id="feedback-list-page" class="spaced" on:window:click={deselectFeedback}>
    <div id="left-panel" >
        <div id="tabbed-area" class="bordered">
            <div class="tab-header" >
                {#each tabs as tab, i}
                    <button class="tab" on:click={()=>setActiveTab(i)} class:active={i===activeTab} class:right-bordered={i<tabs.length-1} >{tab}</button>
                {/each}
            </div>
            <div class="tab-content padded" style="overflow-y: auto;">
                {#if activeTab===0}
                    <div class="column" style="overflow-y: auto;">
                        <div class="feedback-header row" >
                            <!-- <span style="width:3%;" class="centered">
                                <strong>ID</strong>
                            </span> -->
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
                            <span style="width:15%;" class="centered row spaced">
                                <strong>Speaker</strong>
                                <button class="action-button" on:click={() => sortFeedbackList('speaker')}>
                                    {#if sortAscending && sortKey==='speaker'}
                                        <img style="height: 1rem; width: 1rem;" src="./logos/ascending-sort-svgrepo-com.svg" alt="Sort ascending" class="mini-icon">
                                    {:else}
                                        <img style="height: 1rem; width: 1rem;" src="./logos/descending-sort-svgrepo-com.svg" alt="Sort descending" class="mini-icon">
                                    {/if}
                                </button>
                            </span>
                            <span id="feedback-buttons" style="width:15%;" class="centered row">
                                <strong>Actions</strong>
                            </span>
                            <span style="width:10%;" class="centered row spaced">
                                <strong>Done?</strong>
                                <button class="action-button" on:click={() => sortFeedbackList('done')}>
                                    {#if sortAscending && sortKey==='done'}
                                        <img style="height: 1rem; width: 1rem;" src="./logos/ascending-sort-svgrepo-com.svg" alt="Sort ascending" class="mini-icon">
                                    {:else}
                                        <img style="height: 1rem; width: 1rem;" src="./logos/descending-sort-svgrepo-com.svg" alt="Sort descending" class="mini-icon">
                                    {/if}
                                </button>
                            </span>
                        </div>
                        {#each feedback_list as feedback, i}
                            {#if feedback.type==="critical"}
                                <div class="feedback-row row bordered padded" class:done={feedback.done} class:selected={feedback===selected_feedback} on:click={(event) => selectFeedback(feedback, event)}>
                                    <!-- <span style="width:3%;">
                                        <strong> {feedback.id} </strong>
                                    </span> -->
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
                                    
                                    <span style="width:15%; " class="centered">
                                        {feedback.speaker}
                                    </span>
                                    <div id="feedback-buttons" style="width:15%;" class="centered spaced">
                                        <button class="action-button" on:click={async () => { 
                                            feedback.positivised_quote = await paraphrasePositively(feedback.quote, feedback.excerpt_reference.dialogue);
                                            showParaphrasedQuote(feedback, true);
                                            feedback_list = feedback_list;
                                        }}>
                                            <img src="./logos/ai-positive-paraphrase.png" alt="Paraphrase positively" class="action-icon">
                                        </button>
                                        <button class="action-button" on:click={() => removeFeedback(feedback)} >
                                            <img src="./logos/delete-svgrepo-com.svg" alt="Remove feedback" class="action-icon">
                                        </button>
                                    </div>
                                    <span style="width:10%;" class="centered">
                                        <input type="checkbox" bind:checked={feedback.done} />
                                    </span>
                                </div>
                            {/if}
                        {/each}
                    </div>
                {:else if activeTab===1}
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

    <div id="right-panel" class="column spaced">
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

        <div id="selected-feedback-area" class="bordered spaced column" >
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
                            <!-- <button class="padded" on:click={() => {
                                
                            }}>
                                Start Chatbot
                            </button> -->
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
                            </div> <!-- Filler div  -->
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
                                <!--  -->
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
        </div>

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

    #tabbed-area{
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

    #feedback-details{
        height:70%;
        width:100%;
    }

    #feedback-action-buttons{
        height:30%;
        width:100%;
    }

    #chatbot-messages{
        height:70%;
        width:100%;
        overflow-y: scroll;
    }

    #chatbot-actions{
        height:30%;
        width:100%;
        background-color: rgb(201, 201, 201);
    }

    #chatbot-input{
        width:100%;
    }

    #suggested-messages{
        width:100%;
    }

    .user {
		background-color: white;
		
	}
	.assistant {
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