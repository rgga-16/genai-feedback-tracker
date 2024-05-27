<script>
    export let feedback_list;
    export let recording; 

    let mediaPlayer;
    let activeTab=0;  
    let selected_feedback; 

    let tabs = [
        "Positive Feedback", "Critical Feedback"
    ]

    function setActiveTab(index){
        activeTab=index;
    }
</script>

<div id="feedback-list-page" class="spaced">
    <div id="left-panel" >
        <div id="tabbed-area" class="bordered">
            <div id="tab-header" >
                {#each tabs as tab, i}
                    <button class="tab" on:click={()=>setActiveTab(i)} class:active={i===activeTab} class:right-bordered={i<tabs.length-1} >{tab}</button>
                {/each}

            </div>
            <div id="tab-content" class="padded">
                {#if activeTab===0}

                

                {:else if activeTab===1}
                    <div class="column spaced">
                        <div class="feedback-header row" >
                            <span style="width:10%;" class="bordered">
                                <strong>Time</strong>
                            </span>
                            <span style="width:45%;" class="bordered">
                                <strong>Feedback</strong>
                            </span>
                            <span style="width:15%;" class="bordered">
                                <strong>Speaker</strong>
                            </span>
                            <span id="feedback-buttons" style="width:25%;" class="bordered">
                                <strong>Actions</strong>
                            </span>
                            <span style="width:5%;" class="bordered">
                                <strong>Done?</strong>
                            </span>
                        </div>
                        {#each feedback_list as feedback, i}
                            {#if feedback.type==="critical"}
                                <div class="feedback-row row bordered padded" class:selected={feedback===selected_feedback} on:click={() => {selected_feedback=feedback}}>
                                    <span style="width:10%;" class="timestamp  centered" on:click={() => seekTo(excerpt.start_timestamp, mediaPlayer)}>
                                        
                                        [{recording.transcript_list.find(excerpt => excerpt.id=== feedback.dialogue_id).start_timestamp}]
                                    </span>
                                    <span style="width:45%;" class="">
                                        {feedback.quote}
                                    </span>
                                    <span style="width:15%;" class="centered">
                                        {feedback.speaker}
                                    </span>
                                    <span id="feedback-buttons" style="width:25%;" class="">
                                        
                                    </span>
                                    <span style="width:5%;" class="">
                                        
                                    </span>
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

        <div id="feedback-details-area" class="bordered padded spaced column">
            <span>Feedback details</span>

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

    

</style>