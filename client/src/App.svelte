<script>
  import { prevent_default } from "svelte/internal";
	let name;
	let recordings;
	import Capture from "./components/Capture.svelte";
	import Chatbot from "./components/Chatbot.svelte";




</script>

<main>
	<div class="mb-4 border-b border-gray-200 dark:border-gray-700">
		<ul class="flex flex-wrap -mb-px text-sm font-medium text-center w-full" id="default-tab" data-tabs-toggle="#default-tab-content" role="tablist">
			<li class="me-2" role="presentation">
				<button class="inline-block p-4 border-b-2 rounded-t-lg" id="capture-tab" data-tabs-target="#capture" type="button" role="tab" aria-controls="capture" aria-selected="false">Capture</button>
			</li>
			<li class="me-2" role="presentation">
				<button class="inline-block p-4 border-b-2 rounded-t-lg hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300" id="chatbot-tab" data-tabs-target="#chatbot" type="button" role="tab" aria-controls="chatbot" aria-selected="false">Chatbot</button>
			</li>
		</ul>
	</div>
	<div id="default-tab-content">
		<div class="hidden rounded-lg bg-white " id="capture" role="tabpanel" aria-labelledby="capture-tab">
			<Capture bind:recordings={recordings} />
		</div>

		
		<div class="hidden rounded-lg bg-white " id="chatbot" role="tabpanel" aria-labelledby="chatbot-tab">
			<Chatbot bind:recordings={recordings} />
		</div>
	</div>
</main>
