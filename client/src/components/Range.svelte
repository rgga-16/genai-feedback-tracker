<script>

  export let min = 0.0;
  export let max = 2.0;
  export let step = 0.1;
  export let value = 1.0;


</script>

<div class="centered spaced" style="width: 100%; height: 100%;">
  <input type="range" min={min} max={max} step={step} bind:value={value}  id="rangeSlider">
  <span id="sliderValue">{value}</span>
</div>




<style>
  /* General styles for the slider */
  input[type=range] {
    -webkit-appearance: none; /* Override default CSS styles */
    appearance: none;
    width: 100%; /* Full-width */
    height: 1rem; /* Specified height */
    background: #d3d3d3; /* Grey background */
    outline: none; /* Remove outline */
    opacity: 0.7; /* Set transparency (cross-browser) */
    -webkit-transition: .2s; /* 0.2 seconds transition on hover */
    transition: opacity .2s;
  }

  /* Mouse-over effects */
  input[type=range]:hover {
    opacity: 1; /* Fully opaque on hover */
  }

  /* Styles for the slider thumb */
  input[type=range]::-webkit-slider-thumb {
    -webkit-appearance: none; /* Override default look */
    appearance: none;
    width: 1.3rem; /* Width and height of the thumb */
    height: 1.3rem;
    background: #3071a9; /* Green background */
    cursor: pointer; /* Cursor on hover */
    border-radius: 50%; /* Circular shape */
  }

  input[type=range]::-moz-range-thumb {
    width: 1.3rem; /* Width and height of the thumb */
    height: 1.3rem;
    background: #3071a9; /* Green background */
    cursor: pointer; /* Cursor on hover */
    border-radius: 50%; /* Circular shape */
  }

  /* Styles for the slider track */
  input[type=range]::-webkit-slider-runnable-track {
    width: 100%;
    height: 1rem;
    background: lightgray; /* Blue background */
    border: none; /* No border */
  }

  input[type=range]::-moz-range-track {
    width: 100%;
    height: 1rem;
    background: lightgray; /* Blue background */
    border: none; /* No border */
  }
</style>