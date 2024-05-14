<script>
    export let recording;

</script>

<div div class="row spaced" id="feedback-selector-page">
    <div id="left-panel" class="column centered spaced bordered padded">
        <div id="transcript-area" class="bordered">
            <textarea bind:value={recording.transcription} style="width=100%;height=100%;"></textarea>
        </div>
        <div id="transcript-buttons-area" class="row centered spaced bordered">
            <button> Auto-detect Feedback</button>
            <button> Highlight Feedback </button>
            <button> De-highlight Feedback </button>
        </div>
        
    </div>

    <div id="right-panel" class="column centered spaced bordered padded">
        <div id="media-player-area" class="bordered">

        </div>
        <div id="feedback-details-area" class="bordered">

        </div>

    </div>



</div>

<style>
    #feedback-selector-page{
        position: relative;
        height:100%;
        width:100%;
    }

    #left-panel {
        position: relative;
        height: 100%;
        width: 50%;
    }

    #transcript-area {
        position: relative;
        width:100%;
        height:80%;
    }

    #transcript-buttons-area {
        position: relative;
        width:100%;
        height:20%;
    }

    #right-panel {
        position: relative;
        height: 100%;
        width: 50%;
    }

    #media-player-area {
        position:relative;
        height: 50%;
        width: 100%;
    }

    #feedback-details-area {
        position:relative;
        height: 50%;
        width: 100%;
    }

</style>