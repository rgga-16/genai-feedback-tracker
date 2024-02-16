<script>
	export let name;
	import Capture from "./components/Capture.svelte";
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
		<div class="hidden rounded-lg bg-gray-50 dark:bg-gray-800" id="capture" role="tabpanel" aria-labelledby="capture-tab">
			<Capture />
		</div>

		
		<div class="hidden rounded-lg bg-gray-50 dark:bg-gray-800" id="chatbot" role="tabpanel" aria-labelledby="chatbot-tab">
			<p class="text-sm text-gray-500 dark:text-gray-400">This is some placeholder content the <strong class="font-medium text-gray-800 dark:text-white">Dashboard tab's associated content</strong>. Clicking another tab will toggle the visibility of this one for the next. The tab JavaScript swaps classes to control the content visibility and styling.</p>
		</div>
	</div>

</main>
