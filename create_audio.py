from pathlib import Path
from openai import OpenAI
import os 
client = OpenAI()


conversation = [
    {"speaker": "Interior Designer", "dialogue": "Hi Daniel, thank you so much for meeting with me today. As you can see, I’ve prepared a 3D rendering of your bedroom based on the initial ideas we discussed. The room embraces a contemporary style with light, neutral tones, soft blue walls, and natural wood accents. I’ve also included an abstract triptych over the bed in cool tones to bring some visual interest. There’s a low-profile upholstered bed and minimalist bedside tables for a clean, functional look. What do you think so far?"},
    {"speaker": "Daniel", "dialogue": "Thanks for showing me this. I do like the overall layout, it looks spacious, and I appreciate the calm vibe. But, honestly, the design is great, but it looks too plain and typical. It addresses the functionality, but I feel like it neglects giving the room any character or personality. It’s missing that something that makes it feel unique to me, you know?"},
    {"speaker": "Interior Designer", "dialogue": "Ah, I see where you’re coming from. You’re right—the room is quite functional, but we could definitely infuse more personality into the design to make it feel more like your own space. Perhaps adding a more distinctive focal point or incorporating some unique design elements would help. What kind of character do you envision for the room?"},
    {"speaker": "Daniel", "dialogue": "That’s a good question. I guess something that feels a little bolder, but still calming. Maybe more interesting textures or something that breaks up the minimal look. I don’t want it to be too over the top, but right now, it feels almost too safe."},
    {"speaker": "Interior Designer", "dialogue": "Absolutely, Daniel. We can definitely make some changes to give the room more character while maintaining the calm vibe you're after. How about we swap out the artwork for something more striking? Perhaps a bold piece that has more texture or depth? And we could also consider adding some decor elements with more unique materials or finishes."},
    {"speaker": "Daniel", "dialogue": "Yeah, that could help. The artwork is nice, but like I said earlier, it feels kind of flat and too similar to the wall. I think a piece with more personality or color might make a difference. Also, maybe we can play around with some of the furniture—something with a bit more flair would help, don’t you think?"},
    {"speaker": "Interior Designer", "dialogue": "That’s a great idea. We can explore adding furniture pieces that stand out a bit more. Maybe the chair could be swapped for something with a unique silhouette or a rich texture, like leather or velvet. And we could also explore mixed materials for the bedside tables, so they don’t feel too plain. A touch of wood, metal, or even stone could add a lot of character."},
    {"speaker": "Daniel", "dialogue": "Exactly. The bedside tables look almost too minimalist right now. I don’t need something too fancy, but maybe mixing materials or adding some texture would make them feel less generic. And yeah, the chair could definitely use an upgrade."},
    {"speaker": "Interior Designer", "dialogue": "Of course, we’ll look into more interesting options for both the chair and the bedside tables. Do you feel like the lighting could also contribute more to the room’s personality? The wall-mounted lamps are simple, but maybe there’s room for more unique fixtures."},
    {"speaker": "Daniel", "dialogue": "Yeah, I think so. The lamps are fine, but like the rest of the room, they don’t really stand out. I’d love to see something with more style, maybe a bolder design or a warmer material. And I know we talked about the ceiling fan earlier, but that feels a bit out of place too."},
    {"speaker": "Interior Designer", "dialogue": "We can definitely upgrade the lighting. I’ll look for some sculptural or bold designs to help the lamps stand out more. And as for the ceiling fan, we can replace it with a modern pendant light if you’d prefer. Or if you still want a fan, we can find a more cohesive design that blends with the overall look of the room."},
    {"speaker": "Daniel", "dialogue": "I think a pendant light might be better, especially if it’s something that adds personality to the space. The fan just feels too typical for the vibe I’m going for."},
    {"speaker": "Interior Designer", "dialogue": "Perfect! We’ll explore pendant lighting options to bring more character to the ceiling area. I think with these changes—a more striking focal point with the artwork, bolder furniture choices, textured materials, and more expressive lighting—you’ll get that personal touch you’re looking for."},
    {"speaker": "Daniel", "dialogue": "That sounds good. I feel like these tweaks will help give the room more personality while still keeping it functional."},
    {"speaker": "Interior Designer", "dialogue": "It’s great to hear we're on the right track, Daniel. Before we wrap up, is there anything else you’d like to discuss or that you feel isn’t quite working for you?"},
    {"speaker": "Daniel", "dialogue": "Now that you mention it, I’ve been wondering... What would this room look like at night? I know we’ve only looked at the daytime rendering, but I need to see how it feels when I’m winding down in the evening. Right now, I can’t really tell how the lighting will look. Will it be cozy enough? Or maybe too harsh?"},
    {"speaker": "Interior Designer", "dialogue": "That’s a great point. Right now, we’ve mostly focused on natural light and daytime ambience. For nighttime, we can explore adding warmer lighting tones to create that cozy, relaxing atmosphere. I can also prepare a rendering with the evening mood so you can see how it would feel."},
    {"speaker": "Daniel", "dialogue": "Yeah, that would be really helpful. Because, honestly, I feel like those bedside lamps could look really stark at night. Like, will they cast enough light without being too clinical? And will the light from the windows be too cold?"},
    {"speaker": "Interior Designer", "dialogue": "I understand. The bedside lamps are minimal, so we can look at upgrading them to a warmer, more diffused option—something that gives off softer, ambient light. Also, I could suggest adding dimmable overhead lights or even some hidden LED strip lighting along the bedframe or the ceiling to give the room a softer glow without relying too heavily on the lamps."},
    {"speaker": "Daniel", "dialogue": "Yes, exactly! I don’t want it to feel too sterile at night. The dimmable lights sound good, and maybe some indirect lighting would make it feel cozier. Also, are the curtains thick enough to block out city lights? I like waking up with natural light, but I also need darkness at night to sleep."},
    {"speaker": "Interior Designer", "dialogue": "Good observation! We can swap out the sheer curtains for something that still looks light and airy during the day, but with a blackout layer for night. That way, it’s versatile and functional for both day and evening. Do you feel like the window treatments need any other adjustments?"},
    {"speaker": "Daniel", "dialogue": "I think the blackout curtains will solve that problem. But... hmm... what about the rug? At night, with low lighting, it might look too dull or washed out. Is there a way to choose a material that catches the light a bit, or at least doesn’t look so flat?"},
    {"speaker": "Interior Designer", "dialogue": "Absolutely. We can explore a rug with a slightly reflective texture or a silk blend, which would add a subtle sheen and catch the light beautifully in the evening. That should help create more depth in the room, especially when paired with layered lighting."},
    {"speaker": "Daniel", "dialogue": "Great! And about that chair we talked about earlier, I’m also wondering, does it get lost in the shadows at night? It’s already kind of off to the side in the daylight, so I’m thinking it might disappear entirely in the evening unless it has its own light source."},
    {"speaker": "Interior Designer", "dialogue": "Good catch. We can add a floor lamp or a table lamp near the chair to create a reading nook, which will give it more presence and purpose. Plus, it’ll help define the space better when it’s darker. Would you prefer a softer, ambient light there or something more direct?"},
    {"speaker": "Daniel", "dialogue": "Something softer, for sure. I don’t need it to be super bright. Just enough to give the chair its own moment, so it feels like part of the room even at night."},
    {"speaker": "Interior Designer", "dialogue": "Got it! We’ll add a soft, ambient floor lamp or table lamp to that corner to create a cozy nook. This way, the chair won’t feel like an afterthought. We can also adjust the overall lighting to ensure the space has that warm, inviting feel even after the sun goes down."},
    {"speaker": "Daniel", "dialogue": "Perfect! It’s all starting to come together now. I feel like once I see it in both day and night renderings, I’ll have a better sense of how it’ll look when I’m actually using the space."},
    {"speaker": "Interior Designer", "dialogue": "I'll get those night renderings to you soon so we can fine-tune anything else if needed. Thanks again for all your feedback, Daniel—it's really helpful in making sure this room is exactly what you’re looking for."}
]




filename="0.mp3"
for i in range(len(conversation)):
    filename = str(i)+".mp3"
    speech_file_path = f"./3d_scenes/fbx/Bedroom/Conversation/C1/{filename}"
    
    voice="nova"

    if conversation[i]["speaker"] == "Interior Designer":
        voice="nova"
    else:
        voice="onyx"

    response = client.audio.speech.create(
        model="tts-1-hd",
        voice=voice,
        input=conversation[i]["dialogue"]
    )
    response.stream_to_file(speech_file_path)

    # Print progress
    print(f"Generated speech for conversation {i+1}/{len(conversation)}")

