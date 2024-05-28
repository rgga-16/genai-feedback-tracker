<script>
    
    import {timeToSeconds, seekTo} from '../utils.js';

    export let feedback_list;
    export let recording; 

    let mediaPlayer;
    let activeTab=0;  
    let selected_feedback; 

    let tabs = [
        "Critical Feedback", "Positive Feedback"
    ]

    function setActiveTab(index){
        activeTab=index;
    }

    async function paraphrasePositively(feedback, excerpt) {
        const response = await fetch("/positively_paraphrase_feedback", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({feedback: feedback, excerpt: excerpt})
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
</script>

<div id="feedback-list-page" class="spaced" on:window:click={deselectFeedback}>
    <div id="left-panel" >
        <div id="tabbed-area" class="bordered">
            <div id="tab-header" >
                {#each tabs as tab, i}
                    <button class="tab" on:click={()=>setActiveTab(i)} class:active={i===activeTab} class:right-bordered={i<tabs.length-1} >{tab}</button>
                {/each}

            </div>
            <div id="tab-content" class="padded" style="overflow-y: auto;">
                {#if activeTab===0}
                    <div class="column" style="overflow-y: auto;">
                        <div class="feedback-header row" >
                            <span style="width:10%;" class="centered">
                                <strong>Time</strong>
                            </span>
                            <span style="width:45%;" class="centered">
                                <strong>Feedback</strong>
                            </span>
                            <span style="width:15%;" class="centered">
                                <strong>Speaker</strong>
                            </span>
                            <span id="feedback-buttons" style="width:25%;" class="centered">
                                <strong>Actions</strong>
                            </span>
                            <span style="width:5%;" class="centered">
                                <strong>Done?</strong>
                            </span>
                        </div>
                        {#each feedback_list as feedback, i}
                            {#if feedback.type==="critical"}
                                <div class="feedback-row row bordered padded" class:selected={feedback===selected_feedback} on:click={(event) => selectFeedback(feedback, event)}>
                                    <span style="width:10%;" class="timestamp  centered" on:click={() => seekTo(feedback.excerpt_reference.start_timestamp, mediaPlayer)}>
                                        {feedback.excerpt_reference.start_timestamp}
                                    </span>
                                    <div class="column spaced" style="width:45%;">
                                        <span  class="">
                                            {#if feedback.positivised_quote}
                                                "{feedback.positivised_quote}"
                                            {:else}
                                                "{feedback.quote}"
                                            {/if}
                                            
                                        </span>
                                        <span>
                                            <strong>Task: </strong> 
                                            {#if feedback.task}
                                                {feedback.task}
                                            {:else}
                                                (None created yet)
                                            {/if}
                                        </span>
                                    </div>
                                    
                                    <span style="width:15%;" class="centered">
                                        {feedback.speaker}
                                    </span>
                                    <div id="feedback-buttons" style="width:25%;" class="centered spaced">
                                        <button class="action-button" on:click={async () => { 
                                            feedback.positivised_quote = await paraphrasePositively(feedback.quote, feedback.excerpt_reference.dialogue);
                                            feedback_list = feedback_list;
                                        
                                        }}>
                                            <img src="./logos/positive-paraphrase.png" alt="Paraphrase positively" class="action-icon">
                                        </button>
                                        <button class="action-button" on:click={() => removeFeedback(feedback)} >
                                            <img src="./logos/delete-svgrepo-com.svg" alt="Remove feedback" class="action-icon">
                                        </button>
                                    </div>
                                    <span style="width:5%;" class="centered">
                                        
                                    </span>
                                </div>
                            {/if}
                        {/each}
                    </div>
                {:else if activeTab===1}
                    
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

        <div id="feedback-details-area" class="bordered padded spaced column" style="overflow-y: auto;">
            {#if selected_feedback}
                <span style="text-decoration: underline;"><strong> Feedback details </strong></span>
                <p>
                    <span><strong> Timestamp: </strong></span> <span class="timestamp" on:click={() => seekTo(selected_feedback.excerpt_reference.start_timestamp, mediaPlayer)}>[{selected_feedback.excerpt_reference.start_timestamp}]</span> - <span class="timestamp" on:click={() => seekTo(selected_feedback.excerpt_reference.end_timestamp, mediaPlayer)}>[{selected_feedback.excerpt_reference.end_timestamp}]</span><br>
                    <span><strong> Excerpt: </strong> {@html selected_feedback.excerpt_reference.dialogue}  </span> 
                </p>
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
        width:70%;
        padding-bottom: 1rem;
    }

    #tabbed-area{
        height:100%;
        width:100%;
    }

    #tab-header{
        height:5%;
        width:100%;
        display:flex;
        flex-direction:row;
        border-bottom: 1px solid #ccc;
        border-radius: 2px;
        overflow-x:auto;
    }

    #tab-header button.tab {
        padding: 0.5rem 1rem;
        border-top: none;
        border-left: none;
        border-bottom: none ;
        background: #ddd;
        cursor: pointer;
    }

    #tab-header button.tab.active {
        background:#ccc;
        font-weight:bold;
        border-bottom:none;
    }

    #tab-content {
        height:95%;
        width:100%;
    }

    .right-bordered{
        border-right: 1px solid #000000;
    }

    #tab-header button.tab:active{
        background: #ccc;
        font-weight: bold;
    }

    .feedback-header {
        border-bottom: 1px solid #ccc;
    }

    .feedback-row:hover {
        background: #ccc; 
        border: 2px solid #000000;
        cursor:pointer;
    }

    .feedback-row.selected{
        background: #ccc; 
        border: 2px solid #000000;
    }

    #right-panel{
        position:relative;
        height:100%;
        width:30%;
        padding-bottom: 1rem;
    }

    #media-player-area{
        height:30%;
        width:100%;
    }

    #feedback-details-area{
        height:70%;
        width:100%;
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

    .action-button{
        height: 100%;
        width: auto; 
        border: 0 none;
    }

    .action-icon {
        height: 3rem;
        width: 3rem;
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

    

</style>