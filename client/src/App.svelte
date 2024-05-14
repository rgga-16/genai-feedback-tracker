<script>
	import { onMount } from 'svelte';

	import Capture from './components/Capture.svelte';
	import FeedbackSelector from './components/FeedbackSelector.svelte';
	import FeedbackList from './components/FeedbackList.svelte';

	let currentStep = 0;

	let recordings;
	let recording=null;

	function next() {
		if (currentStep < steps.length - 1) {
		currentStep += 1;
		}
	}

	function prev() {
		if (currentStep > 0) {
		currentStep -= 1;
		}
	}

	
</script>

<style>
	.carousel-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 95%;
	}

	.navigation {
		/* margin-top: 10px; */
		height: 5%;
	}

	button {
		margin: 0 10px;
	}
</style>

<main>
	<div class="carousel-container">
		{#if currentStep===0}
			<Capture bind:recordings={recordings} bind:selectedRecording={recording}/>
		{:else if currentStep===1}
			<FeedbackSelector bind:recording={recording}/>
		{:else}
			<FeedbackList />
		{/if}
	</div>
	<div class="navigation centered spaced bordered">
		{#if currentStep===0}
			<button on:click={prev} disabled={currentStep === 0}>Previous</button>
			<button on:click={next} disabled={recording === null}>Next</button>
		{:else if currentStep===1}
			<button on:click={prev} disabled={currentStep === 0}>Previous</button>
			<button on:click={next} disabled={currentStep === steps.length - 1}>Next</button>
		{:else}
			<button on:click={prev} disabled={currentStep === 0}>Previous</button>
			<button on:click={next} disabled={currentStep === steps.length - 1}>Next</button>
		{/if}
	</div>
</main>

