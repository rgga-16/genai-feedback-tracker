


export function timeToSeconds(time) {
    // time is in the format HH:MM:SS,MILISECONDS, e.g., 00:00:53,531
    let timeArray = time.split(":");
    let hours = parseInt(timeArray[0]);
    let minutes = parseInt(timeArray[1]);
    let seconds = parseInt(timeArray[2].split(",")[0]);
    let milliseconds = parseInt(timeArray[2].split(",")[1]);

    return hours*3600 + minutes*60 + seconds + milliseconds/1000;
}

export function seekTo(time, videoPlayer) {
    videoPlayer.currentTime = timeToSeconds(time);
    videoPlayer.play();
}

export function focusOnFeedback(feedback) {
    let dialogue_id = parseInt(feedback.dialogue_id);
    let quoteElement = document.getElementById(dialogue_id);
    if(quoteElement) {
        quoteElement.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
    } else {
        console.log("Error: Can't focus on feedback. Corresponding transcript excerpt not found.")
    }
}