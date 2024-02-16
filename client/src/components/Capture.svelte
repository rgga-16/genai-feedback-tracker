<script>

    let recordings_list = [];


</script>


<div class="container mx-auto relative py-4">

    <div id='captures-panel' class="container mx-auto">
        {#if recordings_list.length > 0}

        {:else}
            <p class="text-sm dark:text-gray-400">No captures made yet.</p>
            
        {/if}
    </div>

    <div id='action-panel' class="container  block mx-auto">
        <button>button</button>
        <button>button</button>
        <button>button</button>
    </div>


    
</div>