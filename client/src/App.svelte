<script>
	import { onMount } from 'svelte';

	import FeedbackSelector from './components/FeedbackSelector.svelte';
	import FeedbackList from './components/FeedbackList.svelte';

	let currentStep = 0;
	let steps=2;

	let recording={};
	let feedback_list=[];
	

	function next() {
		if (currentStep < steps - 1) {
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
			<FeedbackSelector bind:recording={recording} bind:feedback_list={feedback_list}/>
		{:else}
			<FeedbackList bind:feedback_list={feedback_list} bind:recording={recording}/>
		{/if}
	</div>
	<div class="navigation centered spaced bordered">
		<button on:click={prev} disabled={currentStep === 0}>Previous</button>
		<button on:click={next} disabled={currentStep === steps.length - 1 || feedback_list.length <=0}>Next</button>
		
	</div>
</main>

