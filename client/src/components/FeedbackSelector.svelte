<script>
    export let recording;

    let is_recording=false;
    let is_paused=false;

    let videoStream;
    let micStream;
    let settings;

    let micBlobs=[];
    let videoChunks = [];

    let videoRecorder;
    let micRecorder;

    let videoPath;
    let micPath; 

    let files, file_input;
    let is_loading=false;
    let file_load_progress=0; 
    let file_load_status = "";

    let html_break = "<br>";

    let premade_transcript =`
1 
00:00:00,000 --> 00:00:10,000 
Professor: Alright, let's start with Sarah's 3D rendering. Sarah, could you give us a brief overview of your design concept? 
2 
00:00:10,000 --> 00:00:20,000 
Sarah: Sure, my concept is based on creating a serene and airy living space that maximizes natural light and uses sustainable materials. 
3 
00:00:20,000 --> 00:00:30,000 
Guest Professional 1: I appreciate the focus on sustainability. Can you tell us more about the materials you chose and why? 
4 
00:00:30,000 --> 00:00:40,000 
Sarah: I used reclaimed wood for the flooring and bamboo for the furniture. The idea was to create a warm, inviting atmosphere while being eco-friendly. 
5 
00:00:40,000 --> 00:00:50,000 
Student 1: The use of bamboo is interesting. It reminds me of some modern Japanese interiors I've seen. 
6 
00:00:50,000 --> 00:01:00,000 
Professor: Yes, I see that influence. But I think the space could benefit from more contrast. Right now, it feels a bit too uniform. 
7 
00:01:00,000 --> 00:01:10,000 
Guest Professional 2: I agree. Maybe you could introduce some darker elements to create depth and dimension. What do you think about that? 
8 
00:01:10,000 --> 00:01:20,000 Sarah: That's a good point. I was worried about making it too dark, but I see how it could add more interest. 
9 
00:01:20,000 --> 00:01:30,000 
Student 2: I think the lighting is really well done. It gives a very airy feel to the space. 
10 
00:01:30,000 --> 00:01:40,000 
Professor: Yes, the lighting is a strong point. But I would suggest rethinking the placement of the windows. They seem a bit too high. 
11 
00:01:40,000 --> 00:01:50,000 
Guest Professional 1: And I would definitely take away the coloring. I think it’s not working for the intent that you want and that you could just use blue Styrofoam. 
12 
00:01:50,000 --> 00:02:00,000 
Sarah: I see. I was trying to create a gradient effect, but maybe it's not coming through as I intended. 
13 
00:02:00,000 --> 00:02:10,000 
Student 3: It reminds me of a Scandinavian design, very minimalistic and clean. 
14 
00:02:10,000 --> 00:02:20,000 
Guest Professional 2: Yes, but Scandinavian designs often have a pop of color or a statement piece. Maybe you could incorporate something like that? 
15 
00:02:20,000 --> 00:02:30,000 
Professor: Good suggestion. Also, consider the long-term vision. How will this space age over time? Will it still feel fresh and inviting? 
16 
00:02:30,000 --> 00:02:40,000 
Sarah: That's a great point. I hadn't thought about the aging aspect. 
17 
00:02:40,000 --> 00:02:50,000 
Guest Professional 1: What made you put color on it with this? 
18 
00:02:50,000 --> 00:03:00,000 
Sarah: I wanted to create a calming effect with soft blues and greens, but I can see how it might be too subtle. 
19 
00:03:00,000 --> 00:03:10,000 
Student 4: I think the furniture layout is very functional. It seems like a space where you could really relax. 
20 
00:03:10,000 --> 00:03:20,000 
Professor: Functional, yes, but it could be more dynamic. Maybe try experimenting with different furniture arrangements. 
21 
00:03:20,000 --> 00:03:30,000 
Guest Professional 2: And consider layering different textures. It could add more depth and interest to the space.
22 
00:03:30,000 --> 00:03:40,000 
Sarah: Layering textures sounds like a good idea. I could try incorporating some textiles or different finishes.  
23 
00:03:40,000 --> 00:03:50,000 
Student 5: The open shelving is a nice touch. It makes the space feel more open and accessible. 
24 
00:03:50,000 --> 00:04:00,000 
Professor: Yes, but be careful with open shelving. It can easily become cluttered. Think about how you can maintain that clean look.  
25 
00:04:00,000 --> 00:04:10,000 
Guest Professional 1: I think we need to explore other ways of creating dimension. Maybe it is about materials? Maybe layering? Maybe it is about bunching?  
26 
00:04:10,000 --> 00:04:20,000 
Sarah: I'll definitely experiment with those ideas. Thank you for the suggestions.  
27 
00:04:20,000 --> 00:04:30,000 
Student 6: The use of natural light is really effective. It gives the space a very welcoming feel.  
28 
00:04:30,000 --> 00:04:40,000 
Professor: Agreed, but I think the lighting could be improved. The current fixtures don't seem to complement the overall design.  
29 
00:04:40,000 --> 00:04:50,000 
Guest Professional 2: And I would suggest looking into different types of lighting fixtures. Maybe something more modern or industrial to contrast with the natural elements.  
30 
00:04:50,000 --> 00:05:00,000 
Sarah: That's a great idea. I'll look into some different lighting options.  
31 
00:05:00,000 --> 00:05:10,000 
Student 7: The color palette is very soothing. It makes the space feel very calm and peaceful.  
32 
00:05:10,000 --> 00:05:20,000 
Professor: Yes, but as mentioned earlier, it could use more contrast. Maybe introduce some bolder colors in small accents.  
33 
00:05:20,000 --> 00:05:30,000 
Guest Professional 1: And think about the flow of the space. How do people move through it? Are there any areas that feel cramped or awkward?  
34 
00:05:30,000 --> 00:05:40,000 
Sarah: I'll take another look at the layout and see if there are any areas that need more space.  
35 
00:05:40,000 --> 00:05:50,000 
Student 8: The use of plants is a nice touch. It adds a bit of life to the space.  
36 
00:05:50,000 --> 00:06:00,000 
Professor: Yes, but be mindful of maintenance. Some plants require a lot of care. Choose ones that are easy to maintain.  
37 
00:06:00,000 --> 00:06:10,000 
Guest Professional 2: And consider the placement of the plants. They should enhance the space, not clutter it.  
38 
00:06:10,000 --> 00:06:20,000 
Sarah: I'll make sure to choose low-maintenance plants and place them strategically.  
39 
00:06:20,000 --> 00:06:30,000 
Student 9: The overall design feels very cohesive. Everything seems to work well together.
40 
00:06:30,000 --> 00:06:40,000 
Professor: Cohesive, yes, but don't be afraid to take some risks. Sometimes a bold choice can really elevate a design. 
41 
00:06:40,000 --> 00:06:50,000 
Guest Professional 1: And speaking of risks, have you considered incorporating any unique or unconventional elements? 
42 
00:06:50,000 --> 00:07:00,000 
Sarah: I was thinking about adding a statement piece, like a large piece of art or a unique light fixture. 
43 
00:07:00,000 --> 00:07:10,000 
Student 10: That could be interesting. It might add a focal point to the space. 
44 
00:07:10,000 --> 00:07:20,000 
Professor: Yes, a focal point could really help anchor the design. Just make sure it complements the overall aesthetic. 
45 
00:07:20,000 --> 00:07:30,000 
Guest Professional 2: And think about how it interacts with the other elements in the room. It should enhance, not overpower. 
46 
00:07:30,000 --> 00:07:40,000 
Sarah: I'll definitely consider that. Thank you for the feedback. 
47 
00:07:40,000 --> 00:07:50,000 
Student 11: The use of mirrors is clever. It makes the space feel larger and more open. 
48 
00:07:50,000 --> 00:08:00,000 
Professor: Mirrors are a great tool, but be careful not to overdo it. Too many mirrors can make a space feel disorienting. 
49 
00:08:00,000 --> 00:08:10,000 
Guest Professional 1: And think about the placement of the mirrors. They should reflect something interesting, not just another wall. 
50 
00:08:10,000 --> 00:08:20,000 
Sarah: I'll make sure to place them thoughtfully. Thank you for the advice. 
51 
00:08:20,000 --> 00:08:30,000 
Student 12: The choice of furniture is very comfortable-looking. It seems like a space where you could really relax. 
52 
00:08:30,000 --> 00:08:40,000 
Professor: Comfort is important, but also consider the scale of the furniture. Some pieces look a bit oversized for the space. 
53 
00:08:40,000 --> 00:08:50,000 
Guest Professional 2: And think about the balance between form and function. The furniture should be both beautiful and practical. 
54 
00:08:50,000 --> 00:09:00,000 
Sarah: I'll take another look at the furniture choices and see if I can find a better balance. 
55 
00:09:00,000 --> 00:09:10,000 
Student 13: The overall layout is very intuitive. It seems like a space that would be easy to navigate. 
56 
00:09:10,000 --> 00:09:20,000 
Professor: Intuitive, yes, but consider the flow of traffic. Are there any bottlenecks or areas that might feel cramped? 
57 
00:09:20,000 --> 00:09:30,000 
Guest Professional 1: And think about how the space will be used. Are there enough areas for different activities, like reading, entertaining, or working? 
58 
00:09:30,000 --> 00:09:40,000 
Sarah: I'll make sure to consider the different uses of the space and adjust the layout accordingly. 
59 
00:09:40,000 --> 00:09:50,000 
Student 14: The use of natural materials is very appealing. It gives the space a warm, inviting feel. 
60 
00:09:50,000 --> 00:10:00,000 
Professor: Natural materials are great, but be mindful of how they age. Some materials might require more maintenance over time. 
61 
00:10:00,000 --> 00:10:10,000 
Guest Professional 2: And consider mixing natural materials with more modern elements. It could create an interesting contrast. 
62 
00:10:10,000 --> 00:10:20,000 
Sarah: I'll definitely explore that idea. Thank you for the suggestion. 
63 
00:10:20,000 --> 00:10:30,000 
Student 15: The overall design feels very balanced. It seems like a space where everything has its place. 
64 
00:10:30,000 --> 00:10:40,000 
Professor: Balance is important, but don't be afraid to play with asymmetry. Sometimes a bit of imbalance can make a design more dynamic. 
65 
00:10:40,000 --> 00:10:50,000 
Guest Professional 1: And think about how you can create focal points. What elements do you want to draw attention to? 
66 
00:10:50,000 --> 00:11:00,000 
Sarah: I'll experiment with some asymmetrical elements and see how it affects the overall design. 
67 
00:11:00,000 --> 00:11:10,000 
Student 16: The use of color is very soothing. It makes the space feel very calm and peaceful. 
68 
00:11:10,000 --> 00:11:20,000 
Professor: Soothing, yes, but as mentioned earlier, it could use more contrast. Maybe introduce some bolder colors in small accents. 
69 
00:11:20,000 --> 00:11:30,000 
Guest Professional 2: And think about how the colors interact with the lighting. Different lighting can change the way colors appear. 
70 
00:11:30,000 --> 00:11:40,000 
Sarah: I'll make sure to consider the lighting when choosing colors. Thank you for the feedback. 
71 
00:11:40,000 --> 00:11:50,000 
Student 17: The overall design feels very cohesive. Everything seems to work well together. 
72 
00:11:50,000 --> 00:12:00,000 
Professor: Cohesive, yes, but don't be afraid to take some risks. Sometimes a bold choice can really elevate a design. 
73 
00:12:00,000 --> 00:12:10,000 
Guest Professional 1: And speaking of risks, have you considered incorporating any unique or unconventional elements? 
74 
00:12:10,000 --> 00:12:20,000 
Sarah: I was thinking about adding a statement piece, like a large piece of art or a unique light fixture. 
75 
00:12:20,000 --> 00:12:30,000 
Student 18: That could be interesting. It might add a focal point to the space. 
76 
00:12:30,000 --> 00:12:40,000 
Professor: Yes, a focal point could really help anchor the design. Just make sure it complements the overall aesthetic. 
77 
00:12:40,000 --> 00:12:50,000 
Guest Professional 2: And think about how it interacts with the other elements in the room. It should enhance, not overpower. 
78 
00:12:50,000 --> 00:13:00,000 
Sarah: I'll definitely consider that. Thank you for the feedback. 
79 
00:13:00,000 --> 00:13:10,000 
Student 19: The use of mirrors is clever. It makes the space feel larger and more open. 
80 
00:13:10,000 --> 00:13:20,000 
Professor: Mirrors are a great tool, but be careful not to overdo it. Too many mirrors can make a space feel disorienting. 
81 
00:13:20,000 --> 00:13:30,000 
Guest Professional 1: And think about the placement of the mirrors. They should reflect something interesting, not just another wall. 
82 
00:13:30,000 --> 00:13:40,000 
Sarah: I'll make sure to place them thoughtfully. Thank you for the advice. 
83 
00:13:40,000 --> 00:13:50,000 
Student 20: The choice of furniture is very comfortable-looking. It seems like a space where you could really relax. 
84 
00:13:50,000 --> 00:14:00,000 
Professor: Comfort is important, but also consider the scale of the furniture. Some pieces look a bit oversized for the space. 
85 
00:14:00,000 --> 00:14:10,000 
Guest Professional 2: And think about the balance between form and function. The furniture should be both beautiful and practical. 
86 
00:14:10,000 --> 00:14:20,000 
Sarah: I'll take another look at the furniture choices and see if I can find a better balance. 
87 
00:14:20,000 --> 00:14:30,000 
Professor: Alright, I think we've covered a lot of ground. Sarah, you've received some excellent feedback. Take some time to digest it and see how you can incorporate it into your design. 
88 
00:14:30,000 --> 00:14:40,000 
Guest Professional 1: Yes, you've done a great job so far. Keep pushing yourself and exploring new ideas. 
89 
00:14:40,000 --> 00:14:50,000 
Guest Professional 2: And remember, design is an iterative process. Don't be afraid to make changes and try new things. 
90 
00:14:50,000 --> 00:15:00,000 
Sarah: Thank you all for the feedback. I really appreciate it and will definitely take it into consideration as I move forward with my design. 
91 
00:15:00,000 --> 00:15:10,000 
Professor: Great. Let's move on to the next student's work. Thank you, Sarah.


    
    
    `;

    let premade_transcript_list = [
    {
        start_timestamp: "00:00:00,000",
        end_timestamp: "00:00:10,000",
        speaker: "Professor",
        dialogue: "Alright, let's start with Sarah's 3D rendering. Sarah, could you give us a brief overview of your design concept?"
    },
    {
        start_timestamp: "00:00:10,000",
        end_timestamp: "00:00:20,000",
        speaker: "Sarah",
        dialogue: "Sure, my concept is based on creating a serene and airy living space that maximizes natural light and uses sustainable materials."
    },
    {
        start_timestamp: "00:00:20,000",
        end_timestamp: "00:00:30,000",
        speaker: "Guest Professional 1",
        dialogue: "I appreciate the focus on sustainability. Can you tell us more about the materials you chose and why?"
    },
    {
        start_timestamp: "00:00:30,000",
        end_timestamp: "00:00:40,000",
        speaker: "Sarah",
        dialogue: "I used reclaimed wood for the flooring and bamboo for the furniture. The idea was to create a warm, inviting atmosphere while being eco-friendly."
    },
    {
        start_timestamp: "00:00:40,000",
        end_timestamp: "00:00:50,000",
        speaker: "Student 1",
        dialogue: "The use of bamboo is interesting. It reminds me of some modern Japanese interiors I've seen."
    },
    {
        start_timestamp: "00:00:50,000",
        end_timestamp: "00:01:00,000",
        speaker: "Professor",
        dialogue: "Yes, I see that influence. But I think the space could benefit from more contrast. Right now, it feels a bit too uniform."
    },
    {
        start_timestamp: "00:01:00,000",
        end_timestamp: "00:01:10,000",
        speaker: "Guest Professional 2",
        dialogue: "I agree. Maybe you could introduce some darker elements to create depth and dimension. What do you think about that?"
    },
    {
        start_timestamp: "00:01:10,000",
        end_timestamp: "00:01:20,000",
        speaker: "Sarah",
        dialogue: "That's a good point. I was worried about making it too dark, but I see how it could add more interest."
    },
    {
        start_timestamp: "00:01:20,000",
        end_timestamp: "00:01:30,000",
        speaker: "Student 2",
        dialogue: "I think the lighting is really well done. It gives a very airy feel to the space."
    },
    {
        start_timestamp: "00:01:30,000",
        end_timestamp: "00:01:40,000",
        speaker: "Professor",
        dialogue: "Yes, the lighting is a strong point. But I would suggest rethinking the placement of the windows. They seem a bit too high."
    },
    {
        start_timestamp: "00:01:40,000",
        end_timestamp: "00:01:50,000",
        speaker: "Guest Professional 1",
        dialogue: "And I would definitely take away the coloring. I think it’s not working for the intent that you want and that you could just use blue Styrofoam."
    },
    {
        start_timestamp: "00:01:50,000",
        end_timestamp: "00:02:00,000",
        speaker: "Sarah",
        dialogue: "I see. I was trying to create a gradient effect, but maybe it's not coming through as I intended."
    },
    {
        start_timestamp: "00:02:00,000",
        end_timestamp: "00:02:10,000",
        speaker: "Student 3",
        dialogue: "It reminds me of a Scandinavian design, very minimalistic and clean."
    },
    {
        start_timestamp: "00:02:10,000",
        end_timestamp: "00:02:20,000",
        speaker: "Guest Professional 2",
        dialogue: "Yes, but Scandinavian designs often have a pop of color or a statement piece. Maybe you could incorporate something like that?"
    },
    {
        start_timestamp: "00:02:20,000",
        end_timestamp: "00:02:30,000",
        speaker: "Professor",
        dialogue: "Good suggestion. Also, consider the long-term vision. How will this space age over time? Will it still feel fresh and inviting?"
    },
    {
        start_timestamp: "00:02:30,000",
        end_timestamp: "00:02:40,000",
        speaker: "Sarah",
        dialogue: "That's a great point. I hadn't thought about the aging aspect."
    },
    {
        start_timestamp: "00:02:40,000",
        end_timestamp: "00:02:50,000",
        speaker: "Guest Professional 1",
        dialogue: "What made you put color on it with this?"
    },
    {
        start_timestamp: "00:02:50,000",
        end_timestamp: "00:03:00,000",
        speaker: "Sarah",
        dialogue: "I wanted to create a calming effect with soft blues and greens, but I can see how it might be too subtle."
    },
    {
        start_timestamp: "00:03:00,000",
        end_timestamp: "00:03:10,000",
        speaker: "Student 4",
        dialogue: "I think the furniture layout is very functional. It seems like a space where you could really relax."
    },
    {
        start_timestamp: "00:03:10,000",
        end_timestamp: "00:03:20,000",
        speaker: "Professor",
        dialogue: "Functional, yes, but it could be more dynamic. Maybe try experimenting with different furniture arrangements."
    },
    {
        start_timestamp: "00:03:20,000",
        end_timestamp: "00:03:30,000",
        speaker: "Guest Professional 2",
        dialogue: "And consider layering different textures. It could add more depth and interest to the space."
    },
    {
        start_timestamp: "00:03:30,000",
        end_timestamp: "00:03:40,000",
        speaker: "Sarah",
        dialogue: "Layering textures sounds like a good idea. I could try incorporating some textiles or different finishes."
    },
    {
        start_timestamp: "00:03:40,000",
        end_timestamp: "00:03:50,000",
        speaker: "Student 5",
        dialogue: "The open shelving is a nice touch. It makes the space feel more open and accessible."
    },
    {
        start_timestamp: "00:03:50,000",
        end_timestamp: "00:04:00,000",
        speaker: "Professor",
        dialogue: "Yes, but be careful with open shelving. It can easily become cluttered. Think about how you can maintain that clean look."
    },
    {
        start_timestamp: "00:04:00,000",
        end_timestamp: "00:04:10,000",
        speaker: "Guest Professional 1",
        dialogue: "I think we need to explore other ways of creating dimension. Maybe it is about materials? Maybe layering? Maybe it is about bunching?"
    },
    {
        start_timestamp: "00:04:10,000",
        end_timestamp: "00:04:20,000",
        speaker: "Sarah",
        dialogue: "I'll definitely experiment with those ideas. Thank you for the suggestions."
    },
    {
        start_timestamp: "00:04:20,000",
        end_timestamp: "00:04:30,000",
        speaker: "Student 6",
        dialogue: "The use of natural light is really effective. It gives the space a very welcoming feel."
    },
    {
        start_timestamp: "00:04:30,000",
        end_timestamp: "00:04:40,000",
        speaker: "Professor",
        dialogue: "Agreed, but I think the lighting could be improved. The current fixtures don't seem to complement the overall design."
    },
    {
        start_timestamp: "00:04:40,000",
        end_timestamp: "00:04:50,000",
        speaker: "Guest Professional 2",
        dialogue: "And I would suggest looking into different types of lighting fixtures. Maybe something more modern or industrial to contrast with the natural elements."
    },
    {
        start_timestamp: "00:04:50,000",
        end_timestamp: "00:05:00,000",
        speaker: "Sarah",
        dialogue: "That's a great idea. I'll look into some different options for lighting fixtures."
    }
    ];

    async function incrementRecordNumber() {
        let response = await fetch('/increment_record_number', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if(!response.ok) {
            throw new Error('Failed to increment record number');
        } 
    }

    async function sendVideoToServer(videoBlobs) {
        const vidblob = new Blob(videoBlobs, {type: 'video/webm'});
        
        console.log("video blobs", {videoBlobs, vidblob});
        let data = new FormData();
        data.append('file', vidblob);

        if(vidblob.length === 0 || !vidblob) {
            return null;
        }

        const response = await fetch('/download_screen', {
            method: 'POST',
            body: data,
        });
        if(!response.ok) {
            micPath = null;
            videoPath = null;
            // throw new Error('Failed to send video to server');
            console.log('Failed to send video to server');
        } else {
            const json = await response.json();
            videoPath = json["filepath"];
        }
        return videoPath;
    }

    async function sendAudioToServer(audioBlobs) {
        const blob = new Blob(audioBlobs, {type: 'audio/webm'});
        console.log("audio blobs", {audioBlobs, blob})
        let data = new FormData();
        data.append('audio', blob, 'audio.webm');
        const response = await fetch('/download_mic', {
            method: 'POST',
            body: data,
        });
        if(!response.ok) {
            micPath = null;
            videoPath = null;
            throw new Error('Failed to send audio to server');
        } else {
            const json = await response.json();
            micPath = json["filepath"];
        }
        return micPath;
    }

    async function fetchVideo(video_path) {
        try {   
            const response = await fetch("/fetch_video", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    "path": video_path,
                }),
            });
            const blob = await response.blob();
            let video_source = URL.createObjectURL(blob);
            return video_source;
        } catch (error) {
            console.error(error);
        } 
    }

    async function fetchAudio(audio_path) {
        try {   
            const response = await fetch("/fetch_audio", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    "audio_path": audio_path,
                }),
            });
            const blob = await response.blob();
            let audio_source = URL.createObjectURL(blob);
            return audio_source;
        } catch (error) {
            console.error(error);
        } 
    }

    async function transcribeMic(micPath) {
        const response = await fetch('/transcribe_mic', {
            method: 'POST',
            body: JSON.stringify({"audio": micPath}),
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if(!response.ok) {
            throw new Error('Failed to transcribe audio');
        } else {
            const json = await response.json();
            let transcript = json["transcript"]
            return transcript
        }
    }

    async function startRecording() {
        is_recording = true;
        videoStream = await navigator.mediaDevices.getDisplayMedia({
            video: {frameRate:60},
            //@ts-ignore
            selfBrowserSurface:'include',
        })
        videoRecorder = new MediaRecorder(videoStream, {mimeType: 'video/webm'});
        videoRecorder.videoChunks = [];
        videoRecorder.addEventListener('dataavailable', event => {
            if (event.data.size > 0) {
                videoChunks.push(event.data);
            }
        });
        videoRecorder.addEventListener('stop', () => {
            
            // sendVideoToServer(videoChunks);
            // console.log("video chunks", videoChunks);
            // videoChunks = [];
        });

        micStream = await navigator.mediaDevices.getUserMedia({audio: true});
        micRecorder = new MediaRecorder(micStream);
        micRecorder.audioBlobs = [];
        micRecorder.addEventListener('dataavailable', event => {
            if (event.data.size > 0) {
                micBlobs.push(event.data);
            }
        });
        micRecorder.addEventListener('stop', () => {
            // sendAudioToServer(micBlobs);
            // micBlobs = [];
        });
        videoRecorder.start();
        micRecorder.start();
    }

    function pauseRecording() {
        is_recording=false;
        is_paused=true;
        videoRecorder.pause();
        micRecorder.pause();
    }

    function resumeRecording() {

        is_recording=true;
        is_paused=false;

        videoRecorder.resume();
        micRecorder.resume();
    }

    async function stopRecording() {
        is_recording=false;
        is_paused=false;
        is_loading=true; 

        videoStream.getTracks().forEach(track => track.stop());
        micStream.getTracks().forEach(track => track.stop());

        videoPath = await sendVideoToServer(videoChunks); //Bug workaround: Do this for the first time because newly created vidblob is empty during first time.
        videoPath = await sendVideoToServer(videoChunks); 
        videoChunks = [];
        
        let videoSrc = await fetchVideo(videoPath);
        
        micPath = await sendAudioToServer(micBlobs); 
        micBlobs = [];
        let micSrc = await fetchAudio(micPath);

        file_load_status="Transcribing audio (this may take a while) ...";
        file_load_progress=50;
        let transcript = await transcribeMic(micPath);
        file_load_progress=80;

        let transcript_list = await convertTranscriptToList(transcript);

        let newRecording = {video: videoSrc, audio: micSrc, transcript: transcript, transcript_list : transcript_list};
        recording=newRecording;
        await incrementRecordNumber();
        file_load_progress=100;
        is_loading=false;
    }

    async function extractAudioFromVideo(videoFile) {
        const formData = new FormData();
        formData.append('file', videoFile);
        const response = await fetch('/extract_audio_from_video', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            return null;
        } 
        const json = await response.json();
        return [json["audiopath"], json["videopath"]];
    }

    async function handleFilesUpload() {
        
        if(files) {
            for (const file of files) {
                if(file.type.includes('video')) {
                    let videoSrc = URL.createObjectURL(file);
                    file_load_status="Retrieving audio...";
                    file_load_progress=10;
                    [micPath, videoPath] = await extractAudioFromVideo(file);
                    if(!micPath) {
                        micPath = null;
                        videoPath = null;
                        throw new Error('Failed to extract audio from video');
                    } 
                    let micSrc = await fetchAudio(micPath);
                    file_load_status="Transcribing audio (this may take a while) ...";
                    file_load_progress=50;
                    let transcript = await transcribeMic(micPath);
                    file_load_progress=80;
                    // file_load_status="Extracting video frames from transcript timestamps...";
                    // let timestamp_frames = await extractFrames(videoPath, transcript);

                    let transcript_list = await convertTranscriptToList(transcript);

                    let newRecording = {video: videoSrc, audio: micSrc, transcript: transcript, transcript_list:transcript_list};
                    recording=newRecording;
                    micPath=null;
                    videoPath=null;
                    await incrementRecordNumber();
                    file_load_progress=100;
                } else if(file.type.includes('audio')) {
                    let audioSrc = URL.createObjectURL(file);
                    // Save the audio file and get its path
                    file_load_status="Retrieving audio...";
                    file_load_progress=10;
                    const formData = new FormData();
                    formData.append('audio', file);
                    const response = await fetch('/download_mic', {
                        method: 'POST',
                        body: formData,
                    });
                    if(!response.ok) {
                        micPath = null;
                        videoPath = null;
                        throw new Error('Failed to save uploaded audio');
                    }
                    let json = await response.json();
                    micPath = json["filepath"];

                    // Transcribe the audio
                    file_load_status="Transcribing audio (this may take a while) ...";
                    file_load_progress=50;
                    let transcript = await transcribeMic(micPath);

                    let transcript_list = await convertTranscriptToList(transcript);

                    let newRecording = {video: null, audio: micSrc, transcript: transcript, transcript_list:transcript_list};
                    recording = newRecording;
                    micPath=null;
                    videoPath=null;
                    await incrementRecordNumber();
                }
            }
            // Clear the file input
            files=null;
            file_input.value='';
        }
    
    }

    async function convertTranscriptToList(transcript) {
        const response = await fetch("/transcript_to_list", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({transcript: transcript})
        });
        if(!response.ok) {
            throw new Error("Failed to receive initial message from ChatGPT");
        }

        // 4) Send response back here to client
        const json = await response.json();
        let transcript_list = json["transcript_list"];

        return transcript_list;
    }


    
    
    let feedback_list = [];
</script>

<div div class="row spaced" id="feedback-selector-page">
    <div id="left-panel" class="column spaced" style="padding-bottom: 1rem;">

        <!-- #BUG: this div clips the transcript even if overflow-y is set.  -->
        <div id="transcript-area" class="column bordered spaced">
            {#if recording && recording.transcript_list || premade_transcript_list}
                <p class="spaced padded"> 
                    {#each (recording && recording.transcript_list) || premade_transcript_list as excerpt, index}
                        {#if index !== 0}
                            <br>
                        {/if}
                        [{excerpt.start_timestamp} - {excerpt.end_timestamp}]<br>{excerpt.speaker ? `${excerpt.speaker}: ` : ""}{excerpt.dialogue}<br>
                    {/each}
                </p>
            {:else}
                <span> No discussion transcript loaded. Please first record or upload your discussion. </span>
            {/if}
        </div>
        <div id="transcript-buttons-area" class="row centered spaced">
            <div id="capture-feedback-panel" class="column bordered spaced">
                <span style="font-weight: bold; text-decoration: underline; margin-left: 1rem;"> Step 1: Record or upload your discussion.</span>
                <div class="row centered spaced">
                    <div class="column centered">
                        <span >Screen record your discussion</span>
                        <div class="row spaced">
                            <button class="action-button" on:click={() => startRecording()} disabled={is_recording || is_paused} >
                                <img src="./logos/record-video-svgrepo-com.svg" alt="Start recording" class="logo">
                                Record
                            </button>
                            {#if is_paused}
                                <button class="action-button" on:click={() => resumeRecording()} disabled={!is_paused}>
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-play logo" style="border-radius: 50%; padding: 5px; background-color: #fff;">
                                        <polygon points="5 3 19 12 5 21 5 3"></polygon>
                                    </svg>
                                    Resume
                                </button>
                            {:else}
                                <button class="action-button" on:click={() => pauseRecording()} disabled={!is_recording || is_paused}>
                                    <img src="./logos/pause-circle-svgrepo-com.svg" alt="Pause recording" class="logo">
                                    Pause
                                </button>
                            {/if}
                            <button class="action-button" 
                                on:click={() => 
                                    stopRecording()
                                }
                                disabled={!is_recording && !is_paused}>
                                <img src="./logos/record-video-stop-svgrepo-com.svg" alt="Stop recording" class="logo">
                                Stop
                            </button>
                        </div>
                    </div>
                    <span>or</span>
                    <div class="column centered spaced">
                        <label for="file_upload" >Upload your own video or audio recording: </label>
                        <input bind:files bind:this={file_input} name="file_upload"type="file" id="file_upload" accept="video/*, audio/*"/>
                        <button on:click={async () => {
                                    is_loading=true;
                                    await handleFilesUpload();
                                    console.log(recording.transcript_list);
                                    is_loading=false;
                                }} 
                        disabled={is_loading}> Upload files</button> 
                    </div>
                </div>
            </div>
            <div id="feedback-highlight-panel" class ="column bordered spaced ">
                <span style="font-weight: bold; text-decoration: underline; margin-left: 1rem;"> Step 2: Highlight feedback in the transcript.</span>
                <div class="row centered spaced">
                    <button class = "action-button"> 
                        <img src="./logos/magnifying-glass-for-search-3-svgrepo-com.svg" alt="Auto-detect Feedback" class="logo">
                        Auto-detect
                    </button>
                    <button class="action-button"> 
                        <img src="./logos/highlight-svgrepo-com.svg" alt="Highlight Feedback" class="logo">
                        Highlight 
                    </button>
                    <button class="action-button"> 
                        <img src="./logos/delete-svgrepo-com.svg" alt="De-highlight Feedback" class="logo">
                        De-highlight
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div id="right-panel" class="column spaced" style="padding-bottom: 1rem;">
        <div id="media-player-area" class="bordered">
            {#if recording && recording.video}
                <video src={recording.video} controls style="width: 100%; height: 100%;">
                    <track kind="captions" src="blank.vtt" srclang="en">
                </video>
            {:else if recording && recording.audio}
                <audio src={recording.audio} controls style="width: 100%; height: auto;"></audio>
            {:else}
                <video src="video.mp4" controls style="width: 100%; height: 100%;">
                    <track kind="captions" src="blank.vtt" srclang="en">
                </video>
            {/if}
        </div>
        <div id="feedback-details-area" class="bordered">

        </div>

    </div>



</div>

<style>
    #feedback-selector-page{
        position: relative;
        height:100%;
        width:100%;
    }

    #left-panel {
        position: relative;
        height: 100%;
        width: 60%;
    }

    #transcript-area {
        width:100%;
        height:80%;
        overflow-y: auto;
    }

    #transcript-buttons-area {
        width:100%;
        height:20%;
    }

    #capture-feedback-panel {
        position:relative;
        height: 100%;
        width: 60%;
    }

    #feedback-highlight-panel {
        position:relative;
        height: 100%;
        width: 40%;
    }

    #right-panel {
        position: relative;
        height: 100%;
        width: 40%;
    }

    #media-player-area {
        position:relative;
        height: 50%;
        width: 100%;
    }

    #feedback-details-area {
        position:relative;
        height: 50%;
        width: 100%;
    }

    .action-button{
        height: 100%;
        width: auto; 
        border: 0 none;
    }

</style>