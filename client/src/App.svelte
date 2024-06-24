<script>
	import { onMount } from 'svelte';

	import FeedbackSelector from './components/FeedbackSelector.svelte';
	import FeedbackList from './components/FeedbackList.svelte';

	let currentStep = 0;
	let steps=2;

	// let recording={};
	let recording={
        "video": null,
        "audio": "blob:http://127.0.0.1:5000/e584c5ef-d146-4feb-b00e-d400823c7cc1",
        "transcript":`
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
            00:01:10,000 --> 00:01:20,000 
            Sarah: That's a good point. I was worried about making it too dark, but I see how it could add more interest. 

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
        `,
        "transcript_list": [
            {
                "dialogue": "Alright, let's start with Sarah's 3D rendering. Sarah, could you give us a brief overview of your design concept? ",
                "end_timestamp": "00:00:10,000 ",
                "id": 1,
                "speaker": "Professor",
                "start_timestamp": "00:00:00,000"
            },
            {
                "dialogue": "Sure, my concept is based on creating a serene and airy living space that maximizes natural light and uses sustainable materials. ",
                "end_timestamp": "00:00:20,000 ",
                "id": 2,
                "speaker": "Sarah",
                "start_timestamp": "00:00:10,000"
            },
            {
                "dialogue": "I appreciate the focus on sustainability. Can you tell us more about the materials you chose and why?",
                "end_timestamp": "00:00:30,000",
                "id": 3,
                "speaker": "Guest Professional 1",
                "start_timestamp": "00:00:20,000"
            },
            {
                "dialogue": "I used reclaimed wood for the flooring and bamboo for the furniture. The idea was to create a warm, inviting atmosphere while being eco-friendly. ",
                "end_timestamp": "00:00:43,014",
                "id": 4,
                "speaker": "Sarah",
                "start_timestamp": "00:00:42,333"
            },
            {
                "dialogue": "The use of bamboo is interesting. It reminds me of some modern Japanese interiors I've seen. ",
                "end_timestamp": "00:00:52,078",
                "id": 5,
                "speaker": "Student 1",
                "start_timestamp": "00:00:43,074"
            },
            {
                "dialogue": "Yes, I see that influence. But I think the space could benefit from more contrast. Right now, it feels a bit too uniform. ",
                "end_timestamp": "00:00:53,139",
                "id": 6,
                "speaker": "Professor",
                "start_timestamp": "00:00:52,098"
            },
            {
                "dialogue": "I agree. Maybe you could introduce some darker elements to create depth and dimension. What do you think about that? ",
                "end_timestamp": "00:00:59,197",
                "id": 7,
                "speaker": "Guest Professional 2",
                "start_timestamp": "00:00:57,136"
            },
            {
                "dialogue": "That's a good point. I was worried about making it too dark, but I see how it could add more interest. ",
                "end_timestamp": "00:01:08,821",
                "id": 8,
                "speaker": "Sarah",
                "start_timestamp": "00:00:59,837"
            },
            {
                "dialogue": "I think the lighting is really well done. It gives a very airy feel to the space. ",
                "end_timestamp": "00:01:11,933",
                "id": 9,
                "speaker": "Student 2",
                "start_timestamp": "00:01:09,471"
            },
            {
                "dialogue": "Yes, the lighting is a strong point. But I would suggest rethinking the placement of the windows. They seem a bit too high.",
                "end_timestamp": "00:01:41,357",
                "id": 10,
                "speaker": "Professor",
                "start_timestamp": "00:01:11,953"
            },
            {
                "dialogue": "And I would definitely take away the coloring. I think it’s not working for the intent that you want and that you could just use blue Styrofoam. ",
                "end_timestamp": "00:02:13,001",
                "id": 11,
                "speaker": "Guest Professional 1",
                "start_timestamp": "00:01:41,778"
            },
            {
                "dialogue": "I see. I was trying to create a gradient effect, but maybe it's not coming through as I intended. ",
                "end_timestamp": "00:02:24,721",
                "id": 12,
                "speaker": "Sarah",
                "start_timestamp": "00:02:15,034"
            },
            {
                "dialogue": "It reminds me of a Scandinavian design, very minimalistic and clean.",
                "end_timestamp": "00:02:37,590",
                "id": 13,
                "speaker": "Student 3",
                "start_timestamp": "00:02:26,402"
            },
            {
                "dialogue": "Yes, but Scandinavian designs often have a pop of color or a statement piece. Maybe you could incorporate something like that? ",
                "end_timestamp": "00:02:39,071",
                "id": 14,
                "speaker": "Guest Professional 2",
                "start_timestamp": "00:02:38,130"
            },
            {
                "dialogue": "Good suggestion. Also, consider the long-term vision. How will this space age over time? Will it still feel fresh and inviting? ",
                "end_timestamp": "00:02:42,052",
                "id": 15,
                "speaker": "Professor",
                "start_timestamp": "00:02:39,111"
            },
            {
                "dialogue": "That's a great point. I hadn't thought about the aging aspect. ",
                "end_timestamp": "00:02:55,776",
                "id": 16,
                "speaker": "Sarah",
                "start_timestamp": "00:02:42,293"
            },
            {
                "dialogue": "What made you put color on it with this? ",
                "end_timestamp": "00:02:58,977",
                "id": 17,
                "speaker": "Guest Professional 1",
                "start_timestamp": "00:02:55,796"
            },
            {
                "dialogue": "I think the furniture layout is very functional. It seems like a space where you could really relax. ",
                "end_timestamp": "00:03:03,523",
                "id": 18,
                "speaker": "Student 4",
                "start_timestamp": "00:02:59,398"
            },
            {
                "dialogue": "Functional, yes, but it could be more dynamic. Maybe try experimenting with different furniture arrangements. ",
                "end_timestamp": "00:03:28,492",
                "id": 19,
                "speaker": "Professor",
                "start_timestamp": "00:03:15,502"
            },
            {
                "dialogue": "And consider layering different textures. It could add more depth and interest to the space.",
                "end_timestamp": "00:03:32,215",
                "id": 20,
                "speaker": "Guest Professional 2",
                "start_timestamp": "00:03:29,013"
            },
            {
                "dialogue": "Layering textures sounds like a good idea. I could try incorporating some textiles or different finishes.",
                "end_timestamp": "00:03:50,046",
                "id": 21,
                "speaker": "Sarah",
                "start_timestamp": "00:03:32,836"
            },
            {
                "dialogue": "The open shelving is a nice touch. It makes the space feel more open and accessible. ",
                "end_timestamp": "00:03:55,969",
                "id": 22,
                "speaker": "Student 5",
                "start_timestamp": "00:03:50,887"
            },
            {
                "dialogue": "Yes, but be careful with open shelving. It can easily become cluttered. Think about how you can maintain that clean look.  ",
                "end_timestamp": "00:03:58,530",
                "id": 23,
                "speaker": "Professor",
                "start_timestamp": "00:03:55,989"
            },
            {
                "dialogue": "I think we need to explore other ways of creating dimension. Maybe it is about materials? Maybe layering? Maybe it is about bunching?",
                "end_timestamp": "00:04:05,833",
                "id": 24,
                "speaker": "Guest Professional 1",
                "start_timestamp": "00:03:59,810"
            },
            {
                "dialogue": "I'll definitely experiment with those ideas. Thank you for the suggestions.",
                "end_timestamp": "00:04:10,275",
                "id": 25,
                "speaker": "Sarah",
                "start_timestamp": "00:04:06,413"
            },
            {
                "dialogue": "The use of natural light is really effective. It gives the space a very welcoming feel.",
                "end_timestamp": "00:05:00,648",
                "id": 26,
                "speaker": "Student 6",
                "start_timestamp": "00:04:18,762"
            },
            {
                "dialogue": "Agreed, but I think the lighting could be improved. The current fixtures don't seem to complement the overall design.  ",
                "end_timestamp": "00:05:08,411",
                "id": 27,
                "speaker": "Professor",
                "start_timestamp": "00:05:01,328"
            },
            {
                "dialogue": "And I would suggest looking into different types of lighting fixtures. Maybe something more modern or industrial to contrast with the natural elements.",
                "end_timestamp": "00:05:14,614",
                "id": 28,
                "speaker": "Guest Professional 2",
                "start_timestamp": "00:05:08,431"
            },
            {
                "dialogue": "That's a great idea. I'll look into some different lighting options.  ",
                "end_timestamp": "00:05:18,035",
                "id": 29,
                "speaker": "Sarah",
                "start_timestamp": "00:05:16,134"
            },
            {
                "dialogue": "The color palette is very soothing. It makes the space feel very calm and peaceful.  ",
                "end_timestamp": "00:05:38,562",
                "id": 30,
                "speaker": "Student 7",
                "start_timestamp": "00:05:19,036"
            },
            {
                "dialogue": "Yes, but as mentioned earlier, it could use more contrast. Maybe introduce some bolder colors in small accents.",
                "end_timestamp": "00:05:52,257",
                "id": 31,
                "speaker": "Professor",
                "start_timestamp": "00:05:40,831"
            },
            {
                "dialogue": "And think about the flow of the space. How do people move through it? Are there any areas that feel cramped or awkward?  ",
                "end_timestamp": "00:05:56,359",
                "id": 32,
                "speaker": "Guest Professional 1",
                "start_timestamp": "00:05:54,898"
            },
            {
                "dialogue": "I'll take another look at the layout and see if there are any areas that need more space.  ",
                "end_timestamp": "00:05:57,340",
                "id": 33,
                "speaker": "Sarah",
                "start_timestamp": "00:05:56,699"
            },
            {
                "dialogue": "The use of plants is a nice touch. It adds a bit of life to the space.",
                "end_timestamp": "00:06:03,842",
                "id": 34,
                "speaker": "Student 8",
                "start_timestamp": "00:06:00,121"
            },
            {
                "dialogue": "Yes, but be mindful of maintenance. Some plants require a lot of care. Choose ones that are easy to maintain.",
                "end_timestamp": "00:06:12,103",
                "id": 35,
                "speaker": "Professor",
                "start_timestamp": "00:06:04,662"
            },
            {
                "dialogue": "And consider the placement of the plants. They should enhance the space, not clutter it.",
                "end_timestamp": "00:06:44,556",
                "id": 36,
                "speaker": "Guest Professional 2",
                "start_timestamp": "00:06:12,364"
            },
            {
                "dialogue": "I'll make sure to choose low-maintenance plants and place them strategically.",
                "end_timestamp": "00:06:50,058",
                "id": 37,
                "speaker": "Sarah",
                "start_timestamp": "00:06:44,696"
            },
            {
                "dialogue": "The overall design feels very cohesive. Everything seems to work well together.",
                "end_timestamp": "00:06:57,340",
                "id": 38,
                "speaker": "Student 9",
                "start_timestamp": "00:06:50,538"
            },
            {
                "dialogue": "Cohesive, yes, but don't be afraid to take some risks. Sometimes a bold choice can really elevate a design. ",
                "end_timestamp": "00:07:07,828",
                "id": 39,
                "speaker": "Professor",
                "start_timestamp": "00:07:01,623"
            },
            {
                "dialogue": "And speaking of risks, have you considered incorporating any unique or unconventional elements? ",
                "end_timestamp": "00:07:12,932",
                "id": 40,
                "speaker": "Guest Professional 1",
                "start_timestamp": "00:07:07,848"
            },
            {
                "dialogue": "I was thinking about adding a statement piece, like a large piece of art or a unique light fixture.",
                "end_timestamp": "00:07:42,117",
                "id": 41,
                "speaker": "Sarah",
                "start_timestamp": "00:07:14,053"
            },
            {
                "dialogue": "That could be interesting. It might add a focal point to the space.",
                "end_timestamp": "00:07:52,113",
                "id": 42,
                "speaker": "Student 10",
                "start_timestamp": "00:07:43,798"
            },
            {
                "dialogue": " Yes, a focal point could really help anchor the design. Just make sure it complements the overall aesthetic. ",
                "end_timestamp": "00:08:06,009",
                "id": 43,
                "speaker": "Professor",
                "start_timestamp": "00:07:52,754"
            },
            {
                "dialogue": "And think about how it interacts with the other elements in the room. It should enhance, not overpower. ",
                "end_timestamp": "00:08:15,117",
                "id": 44,
                "speaker": "Guest Professional 2",
                "start_timestamp": "00:08:06,850"
            },
            {
                "dialogue": "I'll definitely consider that. Thank you for the feedback.",
                "end_timestamp": "00:08:30,049",
                "id": 45,
                "speaker": "Sarah",
                "start_timestamp": "00:08:15,617"
            },
            {
                "dialogue": "The use of mirrors is clever. It makes the space feel larger and more open. ",
                "end_timestamp": "00:08:33,051",
                "id": 46,
                "speaker": "Student 11",
                "start_timestamp": "00:08:30,289"
            },
            {
                "dialogue": "Mirrors are a great tool, but be careful not to overdo it. Too many mirrors can make a space feel disorienting.",
                "end_timestamp": "00:08:34,712",
                "id": 47,
                "speaker": "Professor",
                "start_timestamp": "00:08:33,431"
            },
            {
                "dialogue": "And think about the placement of the mirrors. They should reflect something interesting, not just another wall. ",
                "end_timestamp": "00:09:12,684",
                "id": 48,
                "speaker": "Guest Professional 1",
                "start_timestamp": "00:08:35,533"
            },
            {
                "dialogue": "I'll make sure to place them thoughtfully. Thank you for the advice. ",
                "end_timestamp": "00:09:15,165",
                "id": 49,
                "speaker": "Sarah",
                "start_timestamp": "00:09:12,984"
            },
            {
                "dialogue": "The choice of furniture is very comfortable-looking. It seems like a space where you could really relax. ",
                "end_timestamp": "00:09:47,989",
                "id": 50,
                "speaker": "Student 12",
                "start_timestamp": "00:09:16,206"
            },
            {
                "dialogue": "Comfort is important, but also consider the scale of the furniture. Some pieces look a bit oversized for the space. ",
                "end_timestamp": "00:09:52,211",
                "id": 51,
                "speaker": "Professor",
                "start_timestamp": "00:09:48,469"
            },
            {
                "dialogue": "I'll take another look at the furniture choices and see if I can find a better balance. ",
                "end_timestamp": "00:10:09,650",
                "id": 52,
                "speaker": "Sarah",
                "start_timestamp": "00:09:54,838"
            },
            {
                "dialogue": "Alright, I think we've covered a lot of ground. Sarah, you've received some excellent feedback. Take some time to digest it and see how you can incorporate it into your design",
                "end_timestamp": "00:10:12,532",
                "id": 53,
                "speaker": "Professor",
                "start_timestamp": "00:10:10,190"
            },
            {
                "dialogue": "Yes, you've done a great job so far. Keep pushing yourself and exploring new ideas. ",
                "end_timestamp": "00:10:50,046",
                "id": 54,
                "speaker": "Guest Professional 1",
                "start_timestamp": "00:10:12,813"
            },
            {
                "dialogue": "And remember, design is an iterative process. Don't be afraid to make changes and try new things. ",
                "end_timestamp": "00:11:08,428",
                "id": 55,
                "speaker": "Guest Professional 2",
                "start_timestamp": "00:10:51,201"
            },
            {
                "dialogue": "Thank you all for the feedback. I really appreciate it and will definitely take it into consideration as I move forward with my design. ",
                "end_timestamp": "00:11:30,044",
                "id": 56,
                "speaker": "Sarah",
                "start_timestamp": "00:11:09,288"
            },
            {
                "dialogue": "Great. Let's move on to the next student's work. Thank you, Sarah.",
                "end_timestamp": "00:11:31,085",
                "id": 57,
                "speaker": "Professor",
                "start_timestamp": "00:11:30,845"
            },
        ]
    };
	
    // let feedback_list=[];

    let feedback_list = [
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 5,
            "done": false,
            "quote": "The use of bamboo is interesting. It reminds me of some modern Japanese interiors I've seen.",
            "show_paraphrased": false,
            "speaker": "Student 1",
            "task": null,
            "type": "positive",
            "excerpt_reference": {
                "dialogue": "<mark class=\"positive\" style=\"background-color:lightgreen;\">The use of bamboo is interesting. It reminds me of some modern Japanese interiors I've seen.</mark> ",
                "end_timestamp": "00:00:52,078",
                "id": 5,
                "speaker": "Student 1",
                "start_timestamp": "00:00:43,074"
            },
            "id":1,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 6,
            "done": false,
            "quote": "But I think the space could benefit from more contrast. Right now, it feels a bit too uniform.",
            "show_paraphrased": false,
            "speaker": "Professor",
            "task": null,
            "type": "critical",
            "excerpt_reference": {
                "dialogue": "Yes, I see that influence. <mark class=\"critical\" style=\"background-color:lightcoral;\">But I think the space could benefit from more contrast. Right now, it feels a bit too uniform.</mark> ",
                "end_timestamp": "00:00:53,139",
                "id": 6,
                "speaker": "Professor",
                "start_timestamp": "00:00:52,098"
            },
            "id":2,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 7,
            "done": false,
            "quote": "I agree. Maybe you could introduce some darker elements to create depth and dimension. What do you think about that?",
            "show_paraphrased": false,
            "speaker": "Guest Professional 2",
            "task": null,
            "type": "critical",
            "excerpt_reference": {
                "dialogue": "<mark class=\"critical\" style=\"background-color:lightcoral;\">I agree. Maybe you could introduce some darker elements to create depth and dimension. What do you think about that?</mark> ",
                "end_timestamp": "00:00:59,197",
                "id": 7,
                "speaker": "Guest Professional 2",
                "start_timestamp": "00:00:57,136"
            },
            "id":3,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 9,
            "done": false,
            "quote": "I think the lighting is really well done. It gives a very airy feel to the space.",
            "show_paraphrased": false,
            "speaker": "Student 2",
            "task": null,
            "type": "positive",
            "excerpt_reference": {
                "dialogue": "<mark class=\"positive\" style=\"background-color:lightgreen;\">I think the lighting is really well done. It gives a very airy feel to the space.</mark> ",
                "end_timestamp": "00:01:11,933",
                "id": 9,
                "speaker": "Student 2",
                "start_timestamp": "00:01:09,471"
            },
            "id":4,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 10,
            "done": false,
            "quote": "Yes, the lighting is a strong point.",
            "show_paraphrased": false,
            "speaker": "Professor",
            "task": null,
            "type": "positive",
            "excerpt_reference": {
                "dialogue": "<mark class=\"positive\" style=\"background-color:lightgreen;\">Yes, the lighting is a strong point.</mark> <mark class=\"critical\" style=\"background-color:lightcoral;\">But I would suggest rethinking the placement of the windows. They seem a bit too high.</mark>",
                "end_timestamp": "00:01:41,357",
                "id": 10,
                "speaker": "Professor",
                "start_timestamp": "00:01:11,953"
            },
            "id":5,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 10,
            "done": false,
            "quote": "But I would suggest rethinking the placement of the windows. They seem a bit too high.",
            "show_paraphrased": false,
            "speaker": "Professor",
            "task": null,
            "type": "critical",
            "excerpt_reference": {
                "dialogue": "<mark class=\"positive\" style=\"background-color:lightgreen;\">Yes, the lighting is a strong point.</mark> <mark class=\"critical\" style=\"background-color:lightcoral;\">But I would suggest rethinking the placement of the windows. They seem a bit too high.</mark>",
                "end_timestamp": "00:01:41,357",
                "id": 10,
                "speaker": "Professor",
                "start_timestamp": "00:01:11,953"
            },
            "id":6,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 11,
            "done": false,
            "quote": "And I would definitely take away the coloring. I think it’s not working for the intent that you want and that you could just use blue Styrofoam.",
            "show_paraphrased": false,
            "speaker": "Guest Professional 1",
            "task": null,
            "type": "critical",
            "excerpt_reference": {
                "dialogue": "<mark class=\"critical\" style=\"background-color:lightcoral;\">And I would definitely take away the coloring. I think it’s not working for the intent that you want and that you could just use blue Styrofoam.</mark> ",
                "end_timestamp": "00:02:13,001",
                "id": 11,
                "speaker": "Guest Professional 1",
                "start_timestamp": "00:01:41,778"
            },
            "id":7,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 13,
            "done": false,
            "quote": "It reminds me of a Scandinavian design, very minimalistic and clean.",
            "show_paraphrased": false,
            "speaker": "Student 3",
            "task": null,
            "type": "positive",
            "excerpt_reference": {
                "dialogue": "<mark class=\"positive\" style=\"background-color:lightgreen;\">It reminds me of a Scandinavian design, very minimalistic and clean.</mark>",
                "end_timestamp": "00:02:37,590",
                "id": 13,
                "speaker": "Student 3",
                "start_timestamp": "00:02:26,402"
            },
            "id":8,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 14,
            "done": false,
            "quote": "Yes, but Scandinavian designs often have a pop of color or a statement piece. Maybe you could incorporate something like that?",
            "show_paraphrased": false,
            "speaker": "Guest Professional 2",
            "task": null,
            "type": "critical",
            "excerpt_reference": {
                "dialogue": "<mark class=\"critical\" style=\"background-color:lightcoral;\">Yes, but Scandinavian designs often have a pop of color or a statement piece. Maybe you could incorporate something like that?</mark> ",
                "end_timestamp": "00:02:39,071",
                "id": 14,
                "speaker": "Guest Professional 2",
                "start_timestamp": "00:02:38,130"
            },
            "id":9,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 15,
            "done": false,
            "quote": "Good suggestion. Also, consider the long-term vision. How will this space age over time? Will it still feel fresh and inviting?",
            "show_paraphrased": false,
            "speaker": "Professor",
            "task": null,
            "type": "critical",
            "excerpt_reference": {
                "dialogue": "<mark class=\"critical\" style=\"background-color:lightcoral;\">Good suggestion. Also, consider the long-term vision. How will this space age over time? Will it still feel fresh and inviting?</mark> ",
                "end_timestamp": "00:02:42,052",
                "id": 15,
                "speaker": "Professor",
                "start_timestamp": "00:02:39,111"
            },
            "id":10,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 18,
            "done": false,
            "quote": "I think the furniture layout is very functional. It seems like a space where you could really relax.",
            "show_paraphrased": false,
            "speaker": "Student 4",
            "task": null,
            "type": "positive",
            "excerpt_reference": {
                "dialogue": "<mark class=\"positive\" style=\"background-color:lightgreen;\">I think the furniture layout is very functional. It seems like a space where you could really relax.</mark> ",
                "end_timestamp": "00:03:03,523",
                "id": 18,
                "speaker": "Student 4",
                "start_timestamp": "00:02:59,398"
            },
            "id":11,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 19,
            "done": false,
            "quote": "Functional, yes, but it could be more dynamic. Maybe try experimenting with different furniture arrangements.",
            "show_paraphrased": false,
            "speaker": "Professor",
            "task": null,
            "type": "critical",
            "excerpt_reference": {
                "dialogue": "<mark class=\"critical\" style=\"background-color:lightcoral;\">Functional, yes, but it could be more dynamic. Maybe try experimenting with different furniture arrangements.</mark> ",
                "end_timestamp": "00:03:28,492",
                "id": 19,
                "speaker": "Professor",
                "start_timestamp": "00:03:15,502"
            },
            "id":12,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 20,
            "done": false,
            "quote": "And consider layering different textures. It could add more depth and interest to the space.",
            "show_paraphrased": false,
            "speaker": "Guest Professional 2",
            "task": null,
            "type": "critical",
            "excerpt_reference": {
                "dialogue": "<mark class=\"critical\" style=\"background-color:lightcoral;\">And consider layering different textures. It could add more depth and interest to the space.</mark>",
                "end_timestamp": "00:03:32,215",
                "id": 20,
                "speaker": "Guest Professional 2",
                "start_timestamp": "00:03:29,013"
            },
            "id":13,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 22,
            "done": false,
            "quote": "The open shelving is a nice touch. It makes the space feel more open and accessible.",
            "show_paraphrased": false,
            "speaker": "Student 5",
            "task": null,
            "type": "positive",
            "excerpt_reference": {
                "dialogue": "<mark class=\"positive\" style=\"background-color:lightgreen;\">The open shelving is a nice touch. It makes the space feel more open and accessible.</mark> ",
                "end_timestamp": "00:03:55,969",
                "id": 22,
                "speaker": "Student 5",
                "start_timestamp": "00:03:50,887"
            },
            "id":14,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 23,
            "done": false,
            "quote": "Yes, but be careful with open shelving. It can easily become cluttered. Think about how you can maintain that clean look.",
            "show_paraphrased": false,
            "speaker": "Professor",
            "task": null,
            "type": "critical",
            "excerpt_reference": {
                "dialogue": "<mark class=\"critical\" style=\"background-color:lightcoral;\">Yes, but be careful with open shelving. It can easily become cluttered. Think about how you can maintain that clean look.</mark>  ",
                "end_timestamp": "00:03:58,530",
                "id": 23,
                "speaker": "Professor",
                "start_timestamp": "00:03:55,989"
            },
            "id":15,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 24,
            "done": false,
            "quote": "I think we need to explore other ways of creating dimension. Maybe it is about materials? Maybe layering? Maybe it is about bunching?",
            "show_paraphrased": false,
            "speaker": "Guest Professional 1",
            "task": null,
            "type": "critical",
            "excerpt_reference": {
                "dialogue": "<mark class=\"critical\" style=\"background-color:lightcoral;\">I think we need to explore other ways of creating dimension. Maybe it is about materials? Maybe layering? Maybe it is about bunching?</mark>",
                "end_timestamp": "00:04:05,833",
                "id": 24,
                "speaker": "Guest Professional 1",
                "start_timestamp": "00:03:59,810"
            },
            "id":16,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 26,
            "done": false,
            "quote": "The use of natural light is really effective. It gives the space a very welcoming feel.",
            "show_paraphrased": false,
            "speaker": "Student 6",
            "task": null,
            "type": "positive",
            "excerpt_reference": {
                "dialogue": "<mark class=\"positive\" style=\"background-color:lightgreen;\">The use of natural light is really effective. It gives the space a very welcoming feel.</mark>",
                "end_timestamp": "00:05:00,648",
                "id": 26,
                "speaker": "Student 6",
                "start_timestamp": "00:04:18,762"
            },
            "id":17,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 27,
            "done": false,
            "quote": "Agreed, but I think the lighting could be improved. The current fixtures don't seem to complement the overall design.",
            "show_paraphrased": false,
            "speaker": "Professor",
            "task": null,
            "type": "critical",
            "excerpt_reference": {
                "dialogue": "<mark class=\"critical\" style=\"background-color:lightcoral;\">Agreed, but I think the lighting could be improved. The current fixtures don't seem to complement the overall design.</mark>  ",
                "end_timestamp": "00:05:08,411",
                "id": 27,
                "speaker": "Professor",
                "start_timestamp": "00:05:01,328"
            },
            "id":18,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 28,
            "done": false,
            "quote": "And I would suggest looking into different types of lighting fixtures. Maybe something more modern or industrial to contrast with the natural elements.",
            "show_paraphrased": false,
            "speaker": "Guest Professional 2",
            "task": null,
            "type": "critical",
            "excerpt_reference": {
                "dialogue": "<mark class=\"critical\" style=\"background-color:lightcoral;\">And I would suggest looking into different types of lighting fixtures. Maybe something more modern or industrial to contrast with the natural elements.</mark>",
                "end_timestamp": "00:05:14,614",
                "id": 28,
                "speaker": "Guest Professional 2",
                "start_timestamp": "00:05:08,431"
            },
            "id":19,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 30,
            "done": false,
            "quote": "The color palette is very soothing. It makes the space feel very calm and peaceful.",
            "show_paraphrased": false,
            "speaker": "Student 7",
            "task": null,
            "type": "positive",
            "excerpt_reference": {
                "dialogue": "<mark class=\"positive\" style=\"background-color:lightgreen;\">The color palette is very soothing. It makes the space feel very calm and peaceful.</mark>  ",
                "end_timestamp": "00:05:38,562",
                "id": 30,
                "speaker": "Student 7",
                "start_timestamp": "00:05:19,036"
            },
            "id":20,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 31,
            "done": false,
            "quote": "Yes, but as mentioned earlier, it could use more contrast. Maybe introduce some bolder colors in small accents.",
            "show_paraphrased": false,
            "speaker": "Professor",
            "task": null,
            "type": "critical",
            "excerpt_reference": {
                "dialogue": "<mark class=\"critical\" style=\"background-color:lightcoral;\">Yes, but as mentioned earlier, it could use more contrast. Maybe introduce some bolder colors in small accents.</mark>",
                "end_timestamp": "00:05:52,257",
                "id": 31,
                "speaker": "Professor",
                "start_timestamp": "00:05:40,831"
            },
            "id":21,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 32,
            "done": false,
            "quote": "And think about the flow of the space. How do people move through it? Are there any areas that feel cramped or awkward?",
            "show_paraphrased": false,
            "speaker": "Guest Professional 1",
            "task": null,
            "type": "critical",
            "excerpt_reference": {
                "dialogue": "<mark class=\"critical\" style=\"background-color:lightcoral;\">And think about the flow of the space. How do people move through it? Are there any areas that feel cramped or awkward?</mark>  ",
                "end_timestamp": "00:05:56,359",
                "id": 32,
                "speaker": "Guest Professional 1",
                "start_timestamp": "00:05:54,898"
            },
            "id":22,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 34,
            "done": false,
            "quote": "The use of plants is a nice touch. It adds a bit of life to the space.",
            "show_paraphrased": false,
            "speaker": "Student 8",
            "task": null,
            "type": "positive",
            "excerpt_reference": {
                "dialogue": "<mark class=\"positive\" style=\"background-color:lightgreen;\">The use of plants is a nice touch. It adds a bit of life to the space.</mark>",
                "end_timestamp": "00:06:03,842",
                "id": 34,
                "speaker": "Student 8",
                "start_timestamp": "00:06:00,121"
            },
            "id":23,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 35,
            "done": false,
            "quote": "Yes, but be mindful of maintenance. Some plants require a lot of care. Choose ones that are easy to maintain.",
            "show_paraphrased": false,
            "speaker": "Professor",
            "task": null,
            "type": "critical",
            "excerpt_reference": {
                "dialogue": "<mark class=\"critical\" style=\"background-color:lightcoral;\">Yes, but be mindful of maintenance. Some plants require a lot of care. Choose ones that are easy to maintain.</mark>",
                "end_timestamp": "00:06:12,103",
                "id": 35,
                "speaker": "Professor",
                "start_timestamp": "00:06:04,662"
            },
            "id":24,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 36,
            "done": false,
            "quote": "And consider the placement of the plants. They should enhance the space, not clutter it.",
            "show_paraphrased": false,
            "speaker": "Guest Professional 2",
            "task": null,
            "type": "critical",
            "excerpt_reference": {
                "dialogue": "<mark class=\"critical\" style=\"background-color:lightcoral;\">And consider the placement of the plants. They should enhance the space, not clutter it.</mark>",
                "end_timestamp": "00:06:44,556",
                "id": 36,
                "speaker": "Guest Professional 2",
                "start_timestamp": "00:06:12,364"
            },
            "id":25,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 38,
            "done": false,
            "quote": "The overall design feels very cohesive. Everything seems to work well together.",
            "show_paraphrased": false,
            "speaker": "Student 9",
            "task": null,
            "type": "positive",
            "excerpt_reference": {
                "dialogue": "<mark class=\"positive\" style=\"background-color:lightgreen;\">The overall design feels very cohesive. Everything seems to work well together.</mark>",
                "end_timestamp": "00:06:57,340",
                "id": 38,
                "speaker": "Student 9",
                "start_timestamp": "00:06:50,538"
            },
            "id":26,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 39,
            "done": false,
            "quote": "Cohesive, yes, but don't be afraid to take some risks. Sometimes a bold choice can really elevate a design.",
            "show_paraphrased": false,
            "speaker": "Professor",
            "task": null,
            "type": "critical",
            "excerpt_reference": {
                "dialogue": "<mark class=\"critical\" style=\"background-color:lightcoral;\">Cohesive, yes, but don't be afraid to take some risks. Sometimes a bold choice can really elevate a design.</mark> ",
                "end_timestamp": "00:07:07,828",
                "id": 39,
                "speaker": "Professor",
                "start_timestamp": "00:07:01,623"
            },
            "id":27,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 40,
            "done": false,
            "quote": "And speaking of risks, have you considered incorporating any unique or unconventional elements?",
            "show_paraphrased": false,
            "speaker": "Guest Professional 1",
            "task": null,
            "type": "critical",
            "excerpt_reference": {
                "dialogue": "<mark class=\"critical\" style=\"background-color:lightcoral;\">And speaking of risks, have you considered incorporating any unique or unconventional elements?</mark> ",
                "end_timestamp": "00:07:12,932",
                "id": 40,
                "speaker": "Guest Professional 1",
                "start_timestamp": "00:07:07,848"
            },
            "id":28,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 42,
            "done": false,
            "quote": "That could be interesting. It might add a focal point to the space.",
            "show_paraphrased": false,
            "speaker": "Student 10",
            "task": null,
            "type": "positive",
            "excerpt_reference": {
                "dialogue": "<mark class=\"positive\" style=\"background-color:lightgreen;\">That could be interesting. It might add a focal point to the space.</mark>",
                "end_timestamp": "00:07:52,113",
                "id": 42,
                "speaker": "Student 10",
                "start_timestamp": "00:07:43,798"
            },
            "id":29,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 43,
            "done": false,
            "quote": "Yes, a focal point could really help anchor the design. Just make sure it complements the overall aesthetic.",
            "show_paraphrased": false,
            "speaker": "Professor",
            "task": null,
            "type": "positive",
            "excerpt_reference": {
                "dialogue": " <mark class=\"positive\" style=\"background-color:lightgreen;\">Yes, a focal point could really help anchor the design. Just make sure it complements the overall aesthetic.</mark> ",
                "end_timestamp": "00:08:06,009",
                "id": 43,
                "speaker": "Professor",
                "start_timestamp": "00:07:52,754"
            },
            "id":30,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 44,
            "done": false,
            "quote": "And think about how it interacts with the other elements in the room. It should enhance, not overpower.",
            "show_paraphrased": false,
            "speaker": "Guest Professional 2",
            "task": null,
            "type": "critical",
            "excerpt_reference": {
                "dialogue": "<mark class=\"critical\" style=\"background-color:lightcoral;\">And think about how it interacts with the other elements in the room. It should enhance, not overpower.</mark> ",
                "end_timestamp": "00:08:15,117",
                "id": 44,
                "speaker": "Guest Professional 2",
                "start_timestamp": "00:08:06,850"
            },
            "id":31,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 46,
            "done": false,
            "quote": "The use of mirrors is clever. It makes the space feel larger and more open.",
            "show_paraphrased": false,
            "speaker": "Student 11",
            "task": null,
            "type": "positive",
            "excerpt_reference": {
                "dialogue": "<mark class=\"positive\" style=\"background-color:lightgreen;\">The use of mirrors is clever. It makes the space feel larger and more open.</mark> ",
                "end_timestamp": "00:08:33,051",
                "id": 46,
                "speaker": "Student 11",
                "start_timestamp": "00:08:30,289"
            },
            "id":32,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 47,
            "done": false,
            "quote": "Mirrors are a great tool, but be careful not to overdo it. Too many mirrors can make a space feel disorienting.",
            "show_paraphrased": false,
            "speaker": "Professor",
            "task": null,
            "type": "critical",
            "excerpt_reference": {
                "dialogue": "<mark class=\"critical\" style=\"background-color:lightcoral;\">Mirrors are a great tool, but be careful not to overdo it. Too many mirrors can make a space feel disorienting.</mark>",
                "end_timestamp": "00:08:34,712",
                "id": 47,
                "speaker": "Professor",
                "start_timestamp": "00:08:33,431"
            },
            "id":33,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 48,
            "done": false,
            "quote": "And think about the placement of the mirrors. They should reflect something interesting, not just another wall.",
            "show_paraphrased": false,
            "speaker": "Guest Professional 1",
            "task": null,
            "type": "critical",
            "excerpt_reference": {
                "dialogue": "<mark class=\"critical\" style=\"background-color:lightcoral;\">And think about the placement of the mirrors. They should reflect something interesting, not just another wall.</mark> ",
                "end_timestamp": "00:09:12,684",
                "id": 48,
                "speaker": "Guest Professional 1",
                "start_timestamp": "00:08:35,533"
            },
            "id":34,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 50,
            "done": false,
            "quote": "The choice of furniture is very comfortable-looking. It seems like a space where you could really relax.",
            "show_paraphrased": false,
            "speaker": "Student 12",
            "task": null,
            "type": "positive",
            "excerpt_reference": {
                "dialogue": "<mark class=\"positive\" style=\"background-color:lightgreen;\">The choice of furniture is very comfortable-looking. It seems like a space where you could really relax.</mark> ",
                "end_timestamp": "00:09:47,989",
                "id": 50,
                "speaker": "Student 12",
                "start_timestamp": "00:09:16,206"
            },
            "id":35,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 51,
            "done": false,
            "quote": "Comfort is important, but also consider the scale of the furniture. Some pieces look a bit oversized for the space.",
            "show_paraphrased": false,
            "speaker": "Professor",
            "task": null,
            "type": "critical",
            "excerpt_reference": {
                "dialogue": "<mark class=\"critical\" style=\"background-color:lightcoral;\">Comfort is important, but also consider the scale of the furniture. Some pieces look a bit oversized for the space.</mark> ",
                "end_timestamp": "00:09:52,211",
                "id": 51,
                "speaker": "Professor",
                "start_timestamp": "00:09:48,469"
            },
            "id":36,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 54,
            "done": false,
            "quote": "Yes, you've done a great job so far. Keep pushing yourself and exploring new ideas.",
            "show_paraphrased": false,
            "speaker": "Guest Professional 1",
            "task": null,
            "type": "positive",
            "excerpt_reference": {
                "dialogue": "<mark class=\"positive\" style=\"background-color:lightgreen;\">Yes, you've done a great job so far. Keep pushing yourself and exploring new ideas.</mark> ",
                "end_timestamp": "00:10:50,046",
                "id": 54,
                "speaker": "Guest Professional 1",
                "start_timestamp": "00:10:12,813"
            },
            "id":37,
        },
        {
            "chatbot_messages": [
                {
                    "content": "You are an expert senior interior designer who is tasked to assist less experienced interior designers like students and junior interior designers with their work by answering their questions on a wide range of interior design topics. ",
                    "role": "system"
                }
            ],
            "dialogue_id": 55,
            "done": false,
            "quote": "And remember, design is an iterative process. Don't be afraid to make changes and try new things.",
            "show_paraphrased": false,
            "speaker": "Guest Professional 2",
            "task": null,
            "type": "positive",
            "excerpt_reference": {
                "dialogue": "<mark class=\"positive\" style=\"background-color:lightgreen;\">And remember, design is an iterative process. Don't be afraid to make changes and try new things.</mark> ",
                "end_timestamp": "00:11:08,428",
                "id": 55,
                "speaker": "Guest Professional 2",
                "start_timestamp": "00:10:51,201"
            },
            "id":38,
        }
    ]


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

		{#if currentStep==0}
			<button on:click={next} disabled={currentStep === steps.length - 1 || feedback_list.length <=0}>Next</button>
		{:else if currentStep===1}
			<button on:click={prev} disabled={currentStep === 0}>Previous</button>
		{/if}

		
		
	</div>
</main>

