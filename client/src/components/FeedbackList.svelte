<script>
    import { onMount, prevent_default } from 'svelte/internal';

    import {seekTo, focusOnFeedback, logAction, pause, focusOnFeedbackNote, copy, convertImageToBase64,saveBase64Image} from '../utils.js';
    import {saveFeedbackList, saveDisplayChatbotMessages, saveMyNotes, saveMyFeedbackNotes} from '../savers.js';
    import LoadingBar from './LoadingBar.svelte';
    import Range from './Range.svelte';

    export let feedback_list;
    export let recording; 
    export let documents = [];
    export let chatbot_messages = [{
        "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
        "role": "system"
    }];

    export let my_notes = [];
    export let feedback_notes = {};
    
    let show_chatbot_settings=false;
    let chatbot_models = {
        "GPT-4o":"gpt-4o",
        "GPT-4o Mini": "gpt-4o-mini",
        "The Interior Design Reference & Specification GPT": "ft:gpt-4o-mini-2024-07-18:im-lab:the-interior-des:9p9NTD1W",
        "Planning and Designers Handbook GPT": "ft:gpt-4o-mini-2024-07-18:im-lab:planning-and-des:9p9vtdRF",
        "Interior Design Illustrated GPT": "ft:gpt-4o-mini-2024-07-18:im-lab:int-illustrated:9qXQyPfI"
    }
    let selected_chatbot="GPT-4o";
    let chatbot_temperature = 0.0;
    let chatbot_max_output_tokens = 256; 

    let mediaPlayer;
    let inputMessage = "";
    
    let selected_feedback; 

    let active_right_tab=0;  
    let active_left_tab=0;
    

    let context;
    let selected_image;
    let image_url; 
    let image_files;
    let image_input;

    
    let document_files, document_file_input;


    let left_panel_tabs = [
        "Critical Feedback", "Positive Feedback"
    ]
    let right_panel_tabs = [
        "Transcript", "Chatbot","Notes"
    ]

    let is_loading=false; 
    let chatbot_load_status = "";
    let chatbot_load_progress= 0; 
    let ld_bar_chatbot; 

    let document_load_status="";
    let document_load_progress=0;
    let is_document_loading=false;

    

    async function handleImageUpload(image_files) {
        let image_file = image_files[0];
        if(image_file) {
            if(image_file.type.includes('image')) {
                console.log(image_file);
                let image_url = URL.createObjectURL(image_file);
                // alert("Image uploaded successfully.");
                return [image_url, image_file];
            } else {
                alert("Please select an image file.");
            }
        } else {
            console.log("No image selected.");
        }
        return null;

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

    async function sendMessage(inputMessage,  context=null) {
        let inputMessageClone = inputMessage.slice();
        if(is_loading) {
            alert("Please wait for the current message to be processed.");
            return;
        }

        is_loading=true; 
        if(inputMessage.trim() === "") {
            alert("Please enter a message.");
            return;
        }

        let message = {
            role: "user", 
            content: inputMessage
        };


        if (context) {
            message["context"] = context;
            let context_string = "\n\nHere is the piece of feedback as context.";
            context_string += "\nF#"+context.id+": \""+context.speaker+": "+context.quote+"\".";
            inputMessageClone += context_string;
        }

        let body = {
            message: inputMessageClone,
            image_data: null,
            max_output_tokens: chatbot_max_output_tokens,
            temperature: chatbot_temperature,
            model: chatbot_models[selected_chatbot]
        };

        image_url ? message["image"] = image_url : null;
        if(selected_image) {
            chatbot_load_status = "Uploading image...";
            chatbot_load_progress=30; 
            let image_base64 = await convertImageToBase64(selected_image);

            body["image_data"] = image_base64;
            message["image_path"] = await saveBase64Image(image_base64);
            body["image_path"] = message["image_path"];
        }

        chatbot_messages.push(message);
        chatbot_messages = chatbot_messages; console.log(chatbot_messages);
        feedback_list = feedback_list;
        await saveDisplayChatbotMessages(chatbot_messages);

        chatbot_load_status = "Thinking...";
        chatbot_load_progress=50;
        const response = await fetch("/message_chatbot", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        });
        if(!response.ok) {
            throw new Error("Failed to send message");
        }
        const json = await response.json();
        let chatbot_response = json["chatbot_response"];

        chatbot_load_status="Done!"
        chatbot_load_progress=100;
        await pause(1200);

        await logAction("FeedbackList: Sent message", [inputMessage, context, image_url]);

        let assistant_message = {
            role: "assistant",
            content: chatbot_response
        };

        context ? assistant_message["context"] = context : null;
        image_url ? assistant_message["image"] = image_url : null;
        
        chatbot_messages.push(assistant_message);
        chatbot_messages = chatbot_messages;
        feedback_list = feedback_list;
        await saveDisplayChatbotMessages(chatbot_messages);

        is_loading=false;
        chatbot_load_progress=0;
    }

    function addContext(feedback) {
        if(context===feedback) {
            alert("This feedback is already added as context.");
        } else {
            context = feedback;
        }
    }

    async function addDocument(event) {
        const files = event.target.files; 

        if (files) {
            for (const file of files) {

                const formData = new FormData();
                formData.append("file", file);

                document_load_progress=50;
                document_load_status = "Adding document... (this may take a while)";
                const response = await fetch("/add_document", {
                    method: "POST",
                    body: formData
                });
                if (!response.ok) {
                    return null;
                } 
                const json = await response.json();
                

                let document_name = json["document_name"];
                documents.push(document_name);
                documents=documents;
                document_load_status = "Done!";
                document_load_progress=100;
                await pause(1200);
            }
        }
    }

    
    async function deleteDocument(title,idx) {

        const response = await fetch("/delete_document", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({title: title})
        });
        if (!response.ok) {
            return console.log(`Failed to delete document ${title}`);
        } 

        // Remove document at idx
        documents.splice(idx, 1);
        documents=documents;
        return title
    }

    async function deleteAllDocuments() {
        document_load_status="Removing all documents...";
        for(let i=0; i<documents.length; i++) {
            let doc = documents[i];
            document_load_progress = (i)/documents.length*100;
            try {
                await deleteDocument(doc, i);
            } catch (error) {
                console.error(`Error deleting document ${doc}:`, error);
                // Optionally, break the loop or continue to the next document
            }
        }

        if(documents.length === 1) {
            await deleteDocument(documents[0], 0);
        }



        document_load_status="Done!";
        document_load_progress=100;
        await pause(1000);
        document_load_progress=0;
    }

    let adding_note=false;
    let temp_note="";

    async function addNote(note,feedback_id=null, image_url=null) {

        if(note.trim() == "") {
            alert("Please enter a note.");
            return;
        }

        if(feedback_id) {

            if(feedback_id in feedback_notes) {
                feedback_notes[feedback_id].notes.push(note);
                feedback_notes[feedback_id].notes = feedback_notes[feedback_id].notes;
                // image_url ? feedback_notes[feedback_id].image = image_url : null;
            } else {
                feedback_notes[feedback_id] = {notes:[note], is_adding:false};
                // image_url ? feedback_notes[feedback_id].image = image_url : null;
            }
        } else {
            my_notes.push(note);
            my_notes = my_notes;

        }
    }

    async function removeNote(note_idx, feedback_id=null) {
        if(feedback_id) {
            feedback_notes[feedback_id].notes.splice(note_idx, 1);
            feedback_notes[feedback_id].notes = feedback_notes[feedback_id].notes;
        } else {
            my_notes.splice(note_idx, 1);
            my_notes = my_notes;
        }
    }

    async function confirmNote(feedback_id=null) {
        adding_note=false;
        addNote(temp_note, feedback_id);
        temp_note="";
    }

    
</script>

<div id="feedback-list-page" class="spaced" on:window:click={deselectFeedback}>
    <div id="left-panel" class="column">
        <div class="tabbed-area bordered">
            <div class="tab-header" >
                {#each left_panel_tabs as tab, i}
                    <button class="tab" on:click={async  ()=>{
                            active_left_tab=i;
                            await logAction("FeedbackList: Switched left panel tab", left_panel_tabs[active_left_tab]);
                        }} 
                        class:active={i===active_left_tab} class:right-bordered={i<left_panel_tabs.length-1} >{tab}</button>
                {/each}
            </div>
            <div class="tab-content padded" style="overflow-y: auto;">
                {#if active_left_tab===0}
                    <div class="column" style="overflow-y: auto;">
                        <div class="feedback-header row" >
                            <span class="centered id-col">
                                <strong>ID</strong>
                            </span>
                            <span  class="centered row spaced feedback-col">
                                <strong>Feedback</strong>
                                <button class="action-button" on:click={async () => {sortFeedbackList('quote'); await logAction("FeedbackList: Sorted feedback", 'quote')}}>
                                    {#if sortAscending && sortKey==='quote'}
                                        <img style="height: 1rem; width: 1rem;" src="./logos/ascending-sort-svgrepo-com.svg" alt="Sort ascending" class="mini-icon">
                                    {:else}
                                        <img style="height: 1rem; width: 1rem;" src="./logos/descending-sort-svgrepo-com.svg" alt="Sort descending" class="mini-icon">
                                    {/if}
                                </button>
                            </span>
                            <span class="centered row spaced speaker-col">
                                <strong>Speaker</strong>
                                <button class="action-button" on:click={async () => {sortFeedbackList('speaker'); await logAction("FeedbackList: Sorted feedback", 'speaker')}}>
                                    {#if sortAscending && sortKey==='speaker'}
                                        <img style="height: 1rem; width: 1rem;" src="./logos/ascending-sort-svgrepo-com.svg" alt="Sort ascending" class="mini-icon">
                                    {:else}
                                        <img style="height: 1rem; width: 1rem;" src="./logos/descending-sort-svgrepo-com.svg" alt="Sort descending" class="mini-icon">
                                    {/if}
                                </button>
                            </span>
                            <span id="feedback-buttons"  class="centered row actions-col">
                                <strong>Actions</strong>
                            </span>
                            <span  class="centered row spaced done-col">
                                <strong>Done?</strong>
                                <button class="action-button" on:click={async () => {sortFeedbackList('done'); await logAction("FeedbackList: Sorted feedback", 'done')}}>
                                    <img style="height: 1rem; width: 1rem;" src={sortAscending && sortKey==='done' ? "./logos/ascending-sort-svgrepo-com.svg" :  "./logos/descending-sort-svgrepo-com.svg"} alt={sortAscending && sortKey==='done' ? "Sort ascending" : "Sort descending"} class="mini-icon">
                                </button>
                            </span>
                        </div>
                        {#each feedback_list as feedback, i}
                            {#if feedback.type==="critical"}
                                <div class="feedback-row row bordered padded" class:done={feedback.done} class:selected={feedback===selected_feedback} 
                                    on:click={async (event) => {
                                        selectFeedback(feedback, event);
                                        focusOnFeedback(feedback);
                                        await logAction("FeedbackList: Selected feedback", feedback);
                                    }}
                                >
                                    <span class="id-col">
                                        <strong> {feedback.id} </strong>
                                    </span>
                                    <div class="column feedback-col" >
                                        <span  class="">
                                            <span class="timestamp" on:click={
                                                async () => {
                                                    active_right_tab = 0;
                                                    if("excerpt_reference" in feedback) {
                                                        if("start_timestamp" in feedback.excerpt_reference) {
                                                            seekTo(feedback.excerpt_reference.start_timestamp, mediaPlayer);
                                                            await logAction("FeedbackList: Seeked to timestamp", feedback.excerpt_reference.start_timestamp);
                                                        }
                                                    }
                                                }}>
                                                {#if "excerpt_reference" in feedback} 
                                                    {#if "start_timestamp" in feedback.excerpt_reference}
                                                        [{feedback.excerpt_reference.start_timestamp}]
                                                    {:else}
                                                        [00:00:00]
                                                    {/if}
                                                {:else}
                                                    [00:00:00]  
                                                {/if}
                                            </span> 
                                            {#if feedback.positivised_quote && feedback.show_paraphrased}
                                                <strong>(Paraphrased Feedback)</strong> "{feedback.positivised_quote}" 
                                                <span class="clickable" 
                                                on:click={async () => {showParaphrasedQuote(feedback, false); await logAction("FeedbackList: Show original quote", feedback.original_quote)}}>
                                                (View original quote)</span>
                                            {:else}
                                                "{feedback.quote}" {#if feedback.positivised_quote && !feedback.show_paraphrased } 
                                                <span class="clickable" 
                                                on:click={async () => {showParaphrasedQuote(feedback, true); await logAction("FeedbackList: Show paraphrased quote", feedback.positivised_quote)}}>(View paraphrased quote)</span> {/if}
                                            {/if}
                                        </span>
                                    </div>
                                    <span  class="centered speaker-col">
                                        {feedback.speaker ? feedback.speaker : "Unknown"}
                                    </span>
                                    <div id="feedback-buttons"  class="row centered spaced actions-col">
                                        <button class="action-button" on:click={async () => { 
                                            feedback.positivised_quote = await paraphrasePositively(feedback.quote, feedback.excerpt_reference.dialogue);
                                            showParaphrasedQuote(feedback, true);
                                            feedback_list = feedback_list;
                                            await logAction("FeedbackList: Positivize Quote", feedback);
                                        }}>
                                            <img src="./logos/ai-positive-paraphrase.png" alt="Paraphrase positively" class="action-icon">
                                            Positivize
                                        </button>

                                        <button class="action-button centered column" on:click={async () => {
                                            active_right_tab=1;
                                            addContext(feedback);
                                            await logAction("FeedbackList: Select as context", context);
                                        }}>
                                            <img src="./logos/select-context.svg" alt="Select feedback as context" style="height: 3.3rem; width: 3.3rem;">
                                            Select Context
                                        </button>
                                        <button class="action-button" on:click={async () => {
                                            active_right_tab = 2;
                                            if(feedback.id in feedback_notes) {
                                                feedback_notes[feedback.id].is_adding = true;
                                            } else {
                                                feedback_notes[feedback.id] = {notes:[], is_adding:true};
                                            }
                                        }}>
                                            <img src="./logos/note-svgrepo-com.svg" alt="Remove feedback" class="action-icon">
                                            Add Note
                                        </button>
                                        <button class="action-button" on:click={async () => {
                                            let confirm = window.confirm("Are you sure you want to delete this feedback? This cannot be undone.");
                                            if(!confirm) {
                                                return;
                                            }
                                            
                                            removeFeedback(feedback);
                                            await saveFeedbackList(feedback_list);
                                            await logAction("FeedbackList: Remove critical feedback", feedback);
                                        }}>
                                            <img src="./logos/delete-svgrepo-com.svg" alt="Remove feedback" class="action-icon">
                                            Delete
                                        </button>
                                        
                                    </div>
                                    <span  class="centered done-col">
                                        <input type="checkbox" bind:checked={feedback.done} />
                                    </span>
                                </div>
                            {/if}
                        {/each}
                    </div>
                {:else if active_left_tab===1}
                    <div class="grid" style="overflow-y: auto;">
                        {#each feedback_list as feedback, i}
                            {#if feedback.type==="positive"}
                                <div class="positive-feedback-note" class:selected={feedback===selected_feedback} 
                                    on:click={ async (event) => {
                                        selectFeedback(feedback, event);
                                        focusOnFeedback(feedback);
                                        await logAction("FeedbackList: Selected feedback", feedback);
                                }}>
                                    <div class="note-header row space-between">
                                        <small class="timestamp" on:click={
                                            async () => {
                                                active_right_tab = 0;
                                                if("excerpt_reference" in feedback) {
                                                    if("start_timestamp" in feedback.excerpt_reference) {
                                                        seekTo(feedback.excerpt_reference.start_timestamp, mediaPlayer);
                                                        await logAction("FeedbackList: Seeked to timestamp", feedback.excerpt_reference.start_timestamp);
                                                    }
                                                }
                                            }}>
                                            {#if "excerpt_reference" in feedback} 
                                                {#if "start_timestamp" in feedback.excerpt_reference}
                                                    [{feedback.excerpt_reference.start_timestamp}]
                                                {:else}
                                                    [00:00:00]
                                                {/if}
                                            {:else}
                                                [00:00:00]  
                                            {/if}
                                        </small>

                                        <div class="row spaced">
                                            <button class="action-button" on:click = {async () => {
                                                active_right_tab = 1;
                                                addContext(feedback);
                                                await logAction("FeedbackList: Select as context", context);
                                            }}>
                                                <img src="./logos/select-context.svg" alt="Select feedback as context" style="height: 2.3rem; width: 2.3rem;">
                                            </button>

                                            <button class="action-button" on:click = {async () => {
                                                active_right_tab = 2;
                                                if(feedback.id in feedback_notes) {
                                                    feedback_notes[feedback.id].is_adding = true;
                                                } else {
                                                    feedback_notes[feedback.id] = {notes:[], is_adding:true};
                                                }
                                            }}>
                                                <img src="./logos/note-svgrepo-com.svg" alt="Add note" class="mini-icon" >
                                            </button>

                                            <button class="action-button" on:click = {async () => {
                                                removeFeedback(feedback);
                                                await saveFeedbackList(feedback_list);
                                                await logAction("FeedbackList: Remove positive feedback", feedback);
                                            }}>
                                                <img src="./logos/delete-svgrepo-com.svg" alt="Paraphrase positively" style="height: 2rem; width: 2rem;">
                                            </button>

                                        </div>
                                    </div>
                                    
                                    <br>
                                    <p>"{feedback.quote}"</p>
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
                    <button class="tab" on:click={async ()=>{active_right_tab=i; await logAction("FeedbackList: Switched right panel tab", right_panel_tabs[active_right_tab]);}} class:active={i===active_right_tab} class:right-bordered={i<right_panel_tabs.length-1} >{tab}</button>
                {/each}
            </div>
            <div class="tab-content column" >
                {#if active_right_tab===0}
                    <div class="column padded spaced" style="width: 100%; height: 100%;">
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
                                        <span class="timestamp" on:click={async () => {seekTo(excerpt.start_timestamp, mediaPlayer); await logAction("FeedbackList: Seek to start timestamp", excerpt.start_timestamp)}}>[{excerpt.start_timestamp}]</span> - <span class="timestamp" on:click={async () => {seekTo(excerpt.end_timestamp, mediaPlayer); await logAction("FeedbackList: Seek to end timestamp", excerpt.end_timestamp)}}>[{excerpt.end_timestamp}]</span>
                                        <br>
                                        {excerpt.speaker ? excerpt.speaker+":" : ""}  
                                        <span id={excerpt.id}>
                                            {@html excerpt.dialogue} 
                                        </span> <br><br>
                                    {/each}
                                </p>
                            {/if}
                        </div>
                    </div>
                    
                {:else if active_right_tab===1}
                    <div id="chatbot-tab-content" class="column">
                        <div id="chatbot-header" class="padded row space-between">
                            <div class:gone={show_chatbot_settings} class="row spaced centered" style="height: auto; width: 100%;">
                                <span>Model: </span>
                                <select bind:value={selected_chatbot} >
                                    {#each Object.keys(chatbot_models) as model}
                                        <option value={model}>{model}</option>
                                    {/each}
                                </select>
                            </div>
                            
                            <button class="action-button" on:click={async ()=> {
                                    show_chatbot_settings=!show_chatbot_settings;
                                    await logAction("FeedbackList: Toggled chatbot settings", show_chatbot_settings);
                                }}>
                                <img class="action-icon" 
                                src={show_chatbot_settings ? "./logos/exit-svgrepo-com.svg" : "./logos/settings-svgrepo-com.svg" }
                                alt={show_chatbot_settings ? "Exit chatbot settings" : "Open chatbot settings"}
                                style="width: 2.5rem; height: 2.5rem;">
                            </button>
                        </div>

                        {#if !show_chatbot_settings} 
                            <div id="chatbot-messages" class="column spaced bordered padded">
                                <div class="assistant padded">
                                    <p> <strong> assistant: </strong> Hello! How can I help you today? </p>
                                </div>
                                {#each chatbot_messages as message} 
                                    {#if message.role != "system"}
                                        <div class="{message.role} padded column spaced">
                                            <div class="message-header row {"context" in message || "image" in message ? 'with-context' : 'no-context'}" >
                                                <div class="row spaced">
                                                    {#if "context" in message}
                                                        <div class="context-tag feedback">
                                                            <small>Context: F#{message.context.id} {
                                                                message.context.quote.length > 40 ? message.context.quote.slice(0,40)+"..." : message.context.quote
                                                            }</small>
                                                        </div>
                                                    {/if}
                                                    {#if "image" in message}
                                                        <div class="context-tag image">
                                                            <small>
                                                                {message.role === "user" ? "Attached image" : "Response to image"}
                                                            </small>
                                                        </div>
                                                    {/if}
                                                </div>
                                                <div class="row spaced">
                                                    <button class="action-button row spaced centered" on:click={async () => {
                                                        active_right_tab = 2;
                                                        addNote(message.role+": "+message.content);
                                                        await saveMyNotes(my_notes);
                                                        await logAction("FeedbackList: Added note to My Notes", message);                                                        
                                                    }}> 
                                                        <small> Add to My Notes </small>
                                                        <img src="./logos/note-svgrepo-com.svg" alt="Add to my notes" class="mini-icon">
                                                    </button>
                                                    
                                                    {#if "context" in message}
                                                        <button class="action-button row spaced centered" on:click={async () => {
                                                            active_right_tab = 2;
                                                            addNote(message.role+": "+message.content, "id" in message.context ? message.context.id : null);
                                                            await saveMyFeedbackNotes(feedback_notes);
                                                            await logAction("FeedbackList: Added note to Feedback ID"+message.context.id, message);                                                        
                                                        }}> 
                                                            <small> Add to F#{message.context.id} Notes </small>
                                                            <img src="./logos/note-svgrepo-com.svg" alt="Add feedback note" class="mini-icon">
                                                        </button>
                                                    {/if}

                                                    <div class="row">
                                                        <button class="action-button column centered" on:click = {async () => {
                                                            // navigator.clipboard.writeText(message.role+": "+message.content);
                                                            copy(message.role+": "+message.content);
                                                            await logAction("FeedbackList: Copied message", message);
                                                        }}> 
                                                            <img src="./logos/copy-svgrepo-com.svg" alt="Copy note" class="mini-icon">
                                                        </button>

                                                        {#if message.role==="user"} 
                                                            <button disabled={is_loading} class="action-button column centered" on:click = {async () => {
                                                                let confirm = window.confirm("Are you sure you want to delete this message? This cannot be undone.");
                                                                if(!confirm) {
                                                                    return;
                                                                }
                                                                

                                                                // Get index of assistant message in chatbot_messages. Delete assistant message too. 
                                                                //BUG: NOt being deleted
                                                                let idx = chatbot_messages.indexOf(message);
                                                                let assistant_idx = idx+1;
                                                                let assistant_message = chatbot_messages[assistant_idx];
                                                                

                                                                await fetch("/remove_from_backend_chatbot_messages", {
                                                                    method: "POST",
                                                                    headers: {
                                                                        "Content-Type": "application/json"
                                                                    },
                                                                    body: JSON.stringify({user_message_idx: idx, assistant_message_idx: assistant_idx})
                                                                });

                                                                chatbot_messages = chatbot_messages.filter(m => m !== message);
                                                                if(assistant_message.role==="assistant") {
                                                                    chatbot_messages = chatbot_messages.filter(m => m !== assistant_message);
                                                                }


                                                                chatbot_messages = chatbot_messages;
                                                                await saveDisplayChatbotMessages(chatbot_messages);
                                                                await logAction("FeedbackList: Removed message", message);
                                                            }}> 
                                                                <img src="./logos/delete-x-svgrepo-com.svg" alt="Delete message" class="mini-icon">
                                                            </button>
                                                        {/if}

                                                        
                                                    </div>
                                        
                                                    
                                                </div>
                                            </div>
                                            <div class="row">
                                                <strong> {message.role}: </strong>
                                                <md-block>  {message.content} </md-block>
                                            </div>
                                            {#if "image" in message && message.role==="user"}
                                                <div class="column centered" style="width: 100%;">
                                                    <img src={message.image} alt="Visual context" style="width:50%; height:auto;">
                                                </div>
                                            {/if}
                                            
                                        </div>
                                    {/if}
                                {/each}
                                <div class="assistant padded column" class:invisible={is_loading===false}>
                                    <p> <strong> assistant: </strong>  </p>
                                    <LoadingBar bind:progress={chatbot_load_progress} bind:status={chatbot_load_status} />
                                </div>
                                <div style="height: 20%; width: 100%; background-color:white; color:white; cursor: default;"></div> 
                            </div>

                            <div id="chatbot-actions" class="column padded spaced centered">
                                <div id="chatbot-utilities" class="row centered spaced" >
                                    <div id="contexts" class="column centered bordered" style={image_url ? "width:30%;" : "width:45%;"}>
                                        <span><strong>Feedback Context:</strong></span>
                                        {#if context}
                                            <div class="suggested-message row "> 
                                                <span>F#{context.id}:{context.quote.slice(0, 30)}... </span>
                                                <button on:click|preventDefault={
                                                    async () => {
                                                        await logAction("FeedbackList: Removed context", context);
                                                        context=null;
                                                    }}>
                                                    <img src="./logos/delete-x-svgrepo-com.svg" alt="Remove context" class="mini-icon">
                                                </button>
                                            </div>
                                        {:else}
                                            <span> None. Add by selecting from the feedback.</span>
                                        {/if}
                                    </div>
                                    <div id="suggested-messages" class="column centered bordered" style={image_url ? "width:30%;" : "width:45%;"}>
                                        <span><strong>Suggested messages:</strong></span>
                                        <div class="suggested-message" on:click|preventDefault={
                                                async () => {
                                                    if(!is_loading) {
                                                        await sendMessage("Can you paraphrase the following feedback positively?",context);
                                                    }
                                                }
                                            } >
                                            Explain feedback.
                                        </div>
                                        <div class="suggested-message" on:click|preventDefault={
                                                async () => {
                                                    if(!is_loading) {
                                                        await sendMessage("Can you brainstorm a set of actions to address the following feedback?",context);
                                                    }
                                                }
                                            }>
                                            Brainstorm actions.
                                        </div>
                                    </div>
                                    <div id="visual-context" class="column centered bordered" style={image_url ? "width:30%;" : "display:none;"}>
                                        {#if image_url}
                                            <span><strong>Attached image:</strong></span>
                                            <div class="row" style="width:100%; height:100%;">
                                                <img src={image_url} alt="Visual context" style="width:100%; height:100%;">
                                                <button on:click|preventDefault={
                                                    async () => {
                                                        await logAction("FeedbackList: Removed image", image_url);
                                                        image_url = null;
                                                        selected_image = null;
                                                    }}>
                                                    <img src="./logos/delete-x-svgrepo-com.svg" alt="Remove image" class="mini-icon">
                                                </button>
                                            </div>
                                            
                                        {:else}
                                            
                                        {/if}
                                    </div>
                                </div>
                                <div id="chatbot-input" class="row spaced centered" >
                                    <div class="column spaced">
                                        <!-- <button class="action-button centered column" on:click|preventDefault={async () => { 
                                                // Take screenshot.
                                                // Attach screenshotted image as a context. 
                                            }}>
                                            <img src="./logos/screenshot-tile-noroot-svgrepo-com.svg" alt="Screenshot" class="action-icon">
                                        </button> -->
                                        
                                        <label for="image_upload" style="display: none;"></label>
                                        <input bind:value={image_files} bind:this={image_input} 
                                            accept="image/png, image/jpeg" type="file" style="display: none;"
                                            id="image_upload" name="image_upload" 
                                            on:change = { async () => {
                                                image_files = image_input.files;
                                                [image_url,selected_image] = await handleImageUpload(image_files);
                                                await logAction( image_url ? "FeedbackList: Uploaded image": "FeedbackList: Canceled uploading image", image_url);
                                            }}
                                        />
                                        <button class="action-button centered column" on:click|preventDefault={async () => { 
                                                // Add image
                                                image_input.click();
                                            }}>
                                            
                                            <img src="./logos/image-svgrepo-com.svg" alt="Attach image" class="action-icon">
                                        </button>
                                    </div>
                                    
                                    <textarea bind:value="{inputMessage}" style="width:100%;height:100%;" on:keydown="{e => e.key==='Enter' && sendMessage(inputMessage, context)}"  placeholder="Type your message here..." id="textarea"></textarea>
                                    <button class="action-button centered column" disabled={is_loading} on:click|preventDefault={async () => { 
                                            
                                            await sendMessage(inputMessage,  context);
                                            
                                            inputMessage = "";
                                        }}>
                                        <img src="./logos/send-svgrepo-com.svg" alt="Send" class="action-icon">
                                    </button>
                                </div>
                            </div>
                        {:else}
                            <div id="chatbot-settings" class="column padded spaced" style="width: 100%; height: 95%;">
                                <div id="chatbot-configurations" class="column centered spaced padded bordered">
                                    <span> <strong> Configurations </strong> </span>
                                    <div class="row spaced centered" style="height: auto; width: 100%;">
                                        <span>Model: </span>
                                        <select bind:value={selected_chatbot} >
                                            {#each Object.keys(chatbot_models) as model}
                                                <option value={model}>{model}</option>
                                            {/each}
                                        </select>
                                    </div>
                                    <div class="row spaced" style="height: auto; width: 100%;">
                                        <span>Temperature: </span>
                                        <Range min=0.0 max=2.0 step=0.1 bind:value={chatbot_temperature} />
                                    </div>
                                    <div class="row spaced" style="height: auto; width: 100%;">
                                        <span>Max Output Tokens: </span>
                                        <Range min=10.0 max=4095.0 step=1.0 bind:value={chatbot_max_output_tokens} />
                                    </div>

                                </div>
                                <div id="chatbot-rag-panel" class="column centered spaced padded bordered" >
                                    <span> <strong> Chatbot's Resources </strong> </span>

                                    <div id="chatbot-rag-sources" class="column centered spaced padded bordered" style="width:100%; height:auto; overflow-y:auto;">
                                        <div class="overlay centered padded" class:invisible = {is_document_loading===false}>
                                            <LoadingBar bind:progress={document_load_progress} bind:status={document_load_status} />
                                        </div>

                                        {#if documents.length > 0}
                                            {#each documents as doc,i}
                                                <div class="row centered spaced centered">
                                                    {doc}
                                                    <button disabled={is_document_loading} class="action-button" on:click|preventDefault={
                                                        async () => {
                                                            let confirm = window.confirm("Are you sure you want to delete this document? This cannot be undone.");
                                                            if(!confirm) {
                                                                return;
                                                            }
                                                            is_document_loading=true;
                                                            document_load_progress=50;
                                                            document_load_status="Removing document...";
                                                            let result = await deleteDocument(doc,i);
                                                            document_load_status="Done!";
                                                            document_load_progress=100;
                                                            is_document_loading=false;
                                                            logAction("FeedbackList: Removed document", result);
                                                        }}>
                                                        <img src="./logos/delete-x-svgrepo-com.svg" alt="Remove document" class="mini-icon">
                                                    </button>
                                                </div>
                                            {/each}
                                        {:else}
                                            <span> No resources available. </span>
                                        {/if}
                                    </div>

                                    <div id="chatbot-rag-buttons" class="row centered  padded spaced" style="width:100%; height:auto;"> 
                                        <input bind:this={document_file_input} type="file" id="document_file_input" class="gone" on:change={
                                            async (e) => {
                                                is_document_loading=true;
                                                await addDocument(e);
                                                is_document_loading=false;
                                                await logAction("FeedbackList: Added document", e.target.files);
                                            }}
                                        />
                                        <button disabled={is_document_loading} class="centered spaced column action-button"
                                            
                                            on:click={async () => {
                                                // Add document
                                                let confirm = window.confirm("Adding a new document will take a long time, since its information will be extracted. Do you want to proceed?");
                                                if(!confirm) {
                                                    return;
                                                }
                                                document.getElementById("document_file_input").click();
                                                await logAction("FeedbackList: Added document", "Document");
                                            }}
                                        >
                                            <img src="./logos/add-ellipse-svgrepo-com.svg" alt="Add document" class="action-icon">
                                            Add Document
                                        </button>
                                        <button disabled={is_document_loading} class="centered spaced column action-button"
                                            on:click={async () => {
                                                // Remove all documents
                                                let confirm = window.confirm("Are you sure you want to remove all documents? This cannot be undone.");
                                                if(!confirm) {
                                                    return;
                                                }
                                                is_document_loading=true;
                                                await deleteAllDocuments();
                                                is_document_loading=false;
                                                await logAction("FeedbackList: Removed all documents", documents);
                                            }}
                                        >
                                            <img src="./logos/delete-svgrepo-com.svg" alt="Remove all documents" class="action-icon">
                                            Remove All
                                        </button>
                                    </div>
                                </div>

                            </div>

                        {/if}



                        

                    </div>
                    
                    
                {:else if active_right_tab===2}
                    <div class="column spaced padded" style="width: 100%; height: 100%; overflow-y: auto;">
                        <div class="column centered spaced padded" style="width:100%; height:auto;">
                            <div class="row centered" style="width:100%; height:auto;">
                                <span style="text-decoration: underline;"> <strong>  My Notes </strong></span>
                            </div>
                            <div class="column bordered" class:centered={my_notes.length <= 0} style="width:100%; height:auto;">
                                {#if my_notes.length > 0}
                                    {#each my_notes as note, i}
                                        <div class="row padded bordered space-between"> 
                                            <p>{note}</p>
                                            <div class="row spaced">
                                                <!-- <button> Edit </button> -->
                                                <button class="action-button" on:click={async () => {
                                                    removeNote(i);
                                                    await saveMyNotes(my_notes);
                                                    await logAction("FeedbackList: Removed note", note);
                                                }}> 
                                                    <img src="./logos/delete-x-svgrepo-com.svg" alt="Delete note" class="mini-icon">
                                                </button>
                                            </div>
                                        </div>
                                    {/each}
                                {:else}
                                    <div class="row padded space-between centered">
                                        <span> No notes added. Feel free to add a note. </span>
                                    </div>
                                {/if}
                                {#if adding_note} 
                                    <div class="row padded bordered space-between" style="width:100%; height:auto;"> 
                                        <input class="note-input" type="text" bind:value={temp_note} placeholder="Enter your note here"/>
                                        <div class="row spaced">
                                            <button class="action-button" on:click={async () => {
                                                confirmNote(); 
                                                adding_note=false;
                                                await saveMyNotes(my_notes);
                                                await logAction("FeedbackList: Added note to My Notes", temp_note);
                                            }}> 
                                                <img src="./logos/check-svgrepo-com.svg" alt="Confirm adding note" class="mini-icon">

                                            </button>
                                            <button class="action-button" on:click={async () => {
                                                adding_note=false;
                                                temp_note="";
                                                await logAction("FeedbackList: Cancelled adding note to My Notes", temp_note);
                                            }}> 
                                                <img src="./logos/delete-x-svgrepo-com.svg" alt="Cancel adding note" class="mini-icon">
                                            </button>
                                        </div>
                                    </div>
                                {/if}
                            </div>
                            
                            <div class="row centered spaced">
                                <button class="action-button centered column"
                                    on:click={async () => {
                                        adding_note=true;
                                        await logAction("FeedbackList: Clicked on My Notes' Add Note button", adding_note);
                                    }}
                                > 
                                    <img src="./logos/note-svgrepo-com.svg" alt="Add Note" class="action-icon">
                                    Add Note
                                </button>
                                <button class="action-button centered column"
                                    on:click={async() => {
                                        let confirm = window.confirm("Are you sure you want to delete all notes? This cannot be undone.");
                                        if(!confirm) {
                                            return;
                                        }
                                        my_notes=[];
                                        my_notes=my_notes;
                                        await saveMyNotes(my_notes);
                                        await logAction("FeedbackList: Removed all notes from My Notes", my_notes);
                                }}> 
                                    <img src="./logos/delete-svgrepo-com.svg" alt="Delete all notes" class="action-icon">
                                    Delete all 
                                    
                                </button>
                            </div>
                        </div>

                        <div class="row centered" style="width:100%; height:auto;">
                            <span style="text-decoration: underline;"> <strong>  My Feedback Notes </strong></span>
                        </div>
                        {#if Object.keys(feedback_notes).length > 0}
                            {#each Object.keys(feedback_notes).map(Number).sort((a, b) => a - b) as key}
                                <div id={"feedback-note-section-"+key} class="column centered spaced padded" style="width:100%; height:auto;">
                                    <div class="row space-between" style="width:100%; height:auto;">
                                        <span> <strong> Feedback #{key} Notes: </strong> {feedback_list[key-1].quote.slice(0, 70)}...</span>
                                        <button class="action-button" on:click={async () => {
                                            let string = "Are you sure you want to delete this feedback notes section? This cannot be undone";
                                            if(feedback_notes[key].notes.length > 0) {
                                                string = "Are you sure you want to delete this feedback notes section? This will delete all notes and cannot be undone.";
                                            }
                                            let confirm = window.confirm(string);
                                            if(!confirm) {
                                                return;
                                            }
                                            delete feedback_notes[key];
                                            feedback_notes = feedback_notes;
                                            await saveMyFeedbackNotes(feedback_notes);
                                            await logAction("FeedbackList: Removed feedback notes section", "Feedback ID"+key);
                                        }}> 
                                            <img src="./logos/delete-x-svgrepo-com.svg" alt="Remove feedback notes section" class="mini-icon">
                                        </button>
                                    </div>
                                    <div class="column bordered" class:centered={feedback_notes[key].notes.length <= 0} 
                                    style="width:100%; height:auto;">
                                        {#if feedback_notes[key].notes.length > 0}
                                            {#each feedback_notes[key].notes as note, i}
                                                <div class="row padded bordered space-between"> 
                                                    <p>{note}</p>
                                                    <div class="row spaced">
                                                        <!-- <button class="action-button"> Edit </button> -->
                                                        <button class="action-button" on:click={async () => {
                                                            removeNote(i, key);
                                                            await saveMyFeedbackNotes(feedback_notes);
                                                            await logAction("FeedbackList: Removed note from Feedback ID"+key, note);
                                                        }}> 
                                                            <img src="./logos/delete-x-svgrepo-com.svg" alt="Delete note from Feedback ID{key}" class="mini-icon">
                                                        </button>
                                                    </div>
                                                </div>
                                            {/each}
                                        {:else}
                                            <div class="row padded centered space-between">
                                                <span> No notes added. Feel free to add a note. </span>
                                            </div>
                                        {/if}   
                                        {#if feedback_notes[key].is_adding} 
                                            <div class="row padded bordered space-between" style="width:100%; height:auto;"> 
                                                <input class="note-input" type="text" bind:value={temp_note} placeholder="Enter your note here" />
                                                <div class="row spaced">
                                                    <button class="action-button" on:click={async () => {
                                                        confirmNote(key);
                                                        feedback_notes[key].is_adding=false;
                                                        await saveMyFeedbackNotes(feedback_notes);
                                                        await logAction("FeedbackList: Added note to Feedback ID"+key, temp_note);
                                                    }}> 
                                                        <img src="./logos/check-svgrepo-com.svg" alt="Confirm adding note" class="mini-icon">
                                                    </button>
                                                    <button class="action-button" on:click={async () => {
                                                        feedback_notes[key].is_adding=false;
                                                        await logAction("FeedbackList: Cancelled adding note to Feedback ID"+key, temp_note);
                                                        temp_note="";
                                                    }}> 
                                                        <img src="./logos/delete-x-svgrepo-com.svg" alt="Cancel adding note" class="mini-icon">
                                                    </button>
                                                </div>
                                            </div>
                                        {/if}
                                    </div>
                                    <div class="row centered spaced">
                                        <button class="action-button centered column"
                                            on:click={async () => {
                                                feedback_notes[key].is_adding=true;
                                                await logAction("FeedbackList: Clicked on Feedback ID"+key+"'s Add Note button", feedback_notes[key].is_adding);
                                            }}
                                        > 
                                            <img src="./logos/note-svgrepo-com.svg" alt="Add Note" class="action-icon">
                                            Add Note
                                        </button>
                                        <button class="action-button centered column"
                                            on:click={async() => {
                                                let confirm = window.confirm("Are you sure you want to delete all notes? This cannot be undone.");
                                                if(!confirm) {
                                                    return;
                                                }
                                                feedback_notes[key].notes=[];
                                                feedback_notes[key].notes=feedback_notes[key].notes;
                                                await saveMyFeedbackNotes(feedback_notes);
                                                await logAction("FeedbackList: Removed all notes from Feedback ID"+key, feedback_notes[key].notes);
                                            }}> 
                                            <img src="./logos/delete-svgrepo-com.svg" alt="Delete all notes" class="action-icon">
                                            Delete all  
                                        </button>
                                    </div>
                                </div>
                            {/each}
                        {:else}
                            <div class="column centered spaced padded" style="width:100%; height:auto;">
                                <div class="row space-between centered" style="width:100%; height:auto;">
                                    <span> No feedback notes added. Feel free to add notes on your feedback by clicking "Add Note" on any of the critical feedback.</span>
                                </div>
                            </div>
                        {/if}
                    </div>
                    

                    

                {/if}
            </div>


        </div>

        
    </div>

</div>

<style>

    #feedback-list-page{
        padding-top: 1rem;
        position:relative;
        display:flex;
        height:100%;
        width:100%;
        background-color: #F8F9FA;
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
        background-color: #FFFFFF;
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

    #chatbot-tab-content {
        height:100%;
        width:100%;
    }

    #chatbot-header{
        height:5%;
        width:100%;
        display:flex;
        flex-direction:row;
        justify-content: right;
        align-items: center;
        position: sticky;
        top: 0;
        z-index: 100;
        background-color: rgb(201, 201, 201);
        padding-top: 0.1rem;
        padding-bottom: 0.1rem;
    }

    #chatbot-messages{
        padding-top:1rem;
        height:65%;
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
        gap: 0.10rem;
    }

    #contexts{
        height:100%;
        gap: 0.10rem;
    }

    #visual-context{
        height:100%;
        gap: 0.10rem;
    }

    .user {
        /* margin-left:1rem; */
		background-color: white;
        border: 1px solid lightgray;
		
	}
	.assistant {
        /* margin-right:1rem; */
		background-color: lightgray;
	}

    .timestamp {
        color: #007BFF;
    }

    .timestamp:hover{
        /* font-weight: bold; */
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
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
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

    .id-col {
        width:3%;
    }

    .feedback-col {
        width:45%;
    }

    .speaker-col {
        width:15%;
    }

    .actions-col {
        width:30%;
    }

    .done-col {
        width:7%;
    }

    .context-tag {
        padding: 2px 4px; /* Small padding */
        border-radius: 4px; /* Rounded corners */
        font-size: 0.75rem; /* Smaller font size */
        margin-bottom: 4px; /* Space between the tag and the message */
        text-align: center; /* Center the text */
    }

    .context-tag.feedback {
        background-color: #ffbebe; /* Light red background */
    }

    .context-tag.image {
        background-color: #a1c2ff; /* Light blue background */
    }

    .message-header {
        display:flex;
        align-items:center;
    }

    .with-context {
        justify-content: space-between; /* Context on the left, button on the right */
    }
    .no-context {
        justify-content: flex-end; /* Button on the right */
    }

    .note-input {
        width: 80%;
    }
    
    #chatbot-configurations {
        background-color: #F8F9FA;
    }

    #chatbot-rag-panel {
        background-color: #F8F9FA;
    }


    

</style>




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
