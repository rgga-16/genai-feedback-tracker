<script>
  export let progress = 0; // Progress is a value between 0 and 100
  export let status= ''; // Status is a string that can be used to display a message
</script>

<style>

    .container {
        height: 80%;
        width: 80%;
    }
    .loading-bar-container {
        width: 100%;
        background-color: #eee;
        border-radius: 0.5rem;
        overflow: hidden;
    }

    .loading-bar-progress {
        height: 2rem;
        background-color: #007bff;
        width: 0%;
        transition: width 0.5s ease;
        border-radius: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white; /* Color of the progress text */
        font-weight: bold;
        animation: pulse 2s infinite ease-in-out;
    }

    @keyframes pulse {
        0% { background-color: #007bff; }
        50% { background-color: #0056b3; }
        100% { background-color: #007bff; }
    }

    .status-text {
        text-align: center;
        margin-top: 0;
    }
</style>

<div class="container column centered spaced">
    <span class="status-text"> [{progress}%] {status} </span>
    <div class="loading-bar-container">
        <div class="loading-bar-progress" style="width: {progress}%;">
        </div>
    </div>
</div>
    


