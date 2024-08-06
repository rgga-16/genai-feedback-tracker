
import {get} from 'svelte/store';
import { copyToClipboard } from '@svelte-put/copy'; //https://svelte-put.vnphanquang.com/docs/copy#installation

export async function pause(milliseconds) {
    return new Promise(resolve => setTimeout(resolve, milliseconds));
}

export async function saveBase64Image(image_base64) {
    const response = await fetch("/save_image", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({image_data: image_base64})
    });
    if(!response.ok) {
        throw new Error("Failed to save image");
    }
    const json = await response.json();
    return json["image_path"];
}

export async function convertImageToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result); // This is the base64 string
        reader.onerror = error => reject(error);
        reader.readAsDataURL(file);
    });
}

export function setCookie(name,value,daysToExpire) {
    var expires = "";
    if(daysToExpire) {
        var date = new Date();
        date.setTime(date.getTime() + (daysToExpire*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

export function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while(c.charAt(0) === ' ') c = c.substring(1,c.length);
        if(c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length,c.length);
    }
    return null;

}

export async function logAction(action, data) {

    // console.log("Action: " + action);
    // console.log(data);

    // Send data to server
    const response = await fetch("/log_action", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({action: action, data: data})
    });
    if(!response.ok) {
        throw new Error("Failed to log action");
    }
    const json = await response.json();
    console.log(json["message"]);
}

export function setLoadingProgress(loadbar, value) {
    let bar = loadbar.ldBar;
    bar.set(value);
}

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

export function focusOnFeedbackNote(feedback) {
    let id = feedback.id;
    let noteElement = document.getElementById("feedback-note-section-"+id);
    if(noteElement) {
        noteElement.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
    } else {
        console.log("Error: Can't focus on feedback note. Corresponding note section not found.")
    }
}

export function copy(text) {
    copyToClipboard(text);
}