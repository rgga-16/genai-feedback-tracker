from pathlib import Path
from openai import OpenAI
import os 
client = OpenAI()


dialogue = [
    "So, Ethan, welcome to your new bedroom! Let's start with a walkthrough. As you can see, we've gone for a minimalist urban design. The walls are in neutral tones, with this accent wall featuring a subtle stone texture. We've also introduced dark, textured furniture, like the bed and side tables, to give the space a grounded feel. By the window, we have this cozy seating area, perfect for enjoying your coffee in the morning while taking in the city view. We kept the decor minimal, just a few candles and books for that personal touch, and to maintain that uncluttered, peaceful vibe. The lighting is intentionally soft and diffused, with ambient lighting from the floor lamp and the nightstand lamp. The rug adds some warmth underfoot, complementing the dark tones of the bed linens.",
    "I really like the vibe in here; it’s calm and exactly what I need after work. The big window is great—the view really makes the room feel bigger, but I’m not so sure about the chair in the corner. It feels a little out of place? I can’t quite explain why, but maybe it just doesn’t match the bed and other furniture?",
    "Ah, I see what you mean. The chair is upholstered in a lighter tone, which we thought might add some contrast, but I understand if it feels too different from the more structured furniture. We could look at something that’s still comfortable but in a darker shade or with a more structured design to match the bed. How does that sound?",
    "Yeah, I think that would work better. Also, I like the candles on the shelf by the window—they’re nice—but maybe they could be a different color? Or maybe it’s the design of them. Something just feels a bit off with those.",
    "We can definitely switch those out for something more in line with your style. Perhaps something in a matte black or muted gray? That way, they’ll blend into the room without drawing too much attention.",
    "Yeah, that sounds like a good idea. And the side tables—don’t get me wrong, they’re the right size, but I kind of feel like I could use a bit more space for things, you know? Like my books or some other stuff I use often.",
    "We could consider slightly wider side tables or even some with an additional shelf for extra storage. That would give you space for your books without cluttering the surface.",
    "Yeah, extra storage would be nice. Now, the bed linens—I like the dark color, but do you think adding some texture or a lighter color would help? I’m worried it might look a bit too plain as it is.",
    "Great suggestion. We could layer the bed with a textured throw or some accent pillows in lighter, neutral tones—maybe something in a soft beige or muted green to tie in with the natural elements in the room. It’ll give the bed more depth while staying in line with the minimalist feel.",
    "That sounds nice. Oh, and one more thing—the floor lamp. It’s sleek and all, but is it enough? Sometimes I like to read, and I’m worried it might not be bright enough for that.",
    "That’s a good point. We can add a task light or maybe even swap the floor lamp for one with a more adjustable brightness. Another option is to add a small, directional reading light next to the seating area or by the bed. That way, you can adjust it based on your needs.",
    "I like that idea—maybe the small reading light could work better for what I need. Overall, I’m happy with the room. It’s really close to what I was looking for, just with a few small changes, it’ll be perfect.",
    "I’m glad you like it! So to summarize: we’ll swap out the chair for something that aligns better with the rest of the room, change the candles for a more cohesive look, possibly enlarge the side tables for more functionality, and add some layered texture to the bedding. Plus, we’ll explore adding more task-focused lighting. Anything else that comes to mind?",
    "No, I think that covers it for now. I’m excited to see how it all turns out after these updates!",
    "Absolutely! I’ll send over some options for the new chair and the lighting fixtures, and we can finalize the choices. Looking forward to perfecting your space!",
    "One other thing I noticed is the wooden paneling on the accent wall. It's great, but I’m wondering if we could add a bit more texture or maybe another material? The stone element is nice, but it feels like it could use a little something extra?",
    "We can definitely work with that. Would you be interested in something like a textured wallpaper or maybe some natural wood elements? It could add a subtle warmth to the space without disrupting the minimalist theme.",
    "Yeah, that sounds like a good idea. Maybe a mix of wood and stone would make it feel a little more interesting? But I don’t want it to be too busy, you know?",
    "We can absolutely do that! A subtle wood trim around the edges of the stone or alternating panels could bring in that variety without overwhelming the space. We could try samples and see what feels right.",
    "That sounds good to me. Oh, and about the curtains—they’re nice, but is there something that might feel a bit more... I don’t know, special? They feel kind of plain to me.",
    "Sure, we could go for something with a slightly richer texture or maybe a subtle pattern. Since the rest of the room is quite minimalist, some added texture in the curtains could provide a bit of luxury. Perhaps velvet in a dark, muted tone? It’ll elevate the space without distracting from the clean lines.",
    "Velvet sounds cool, but not too heavy, right? I still want it to feel light and open when the curtains are drawn back for the view.",
    "Understood. We’ll keep it elegant yet lightweight. I’ll send you a few fabric samples so we can decide on the best fit.",
    "Great! And about the bookshelf—I like keeping things minimal, but I need a little more room for my books. Is there a way to add storage without making it look too cluttered?",
    "We can definitely integrate built-in shelving. It could run along one side of the room or we could incorporate floating shelves. That way, you have storage, but it remains sleek and clean.",
    "Floating shelves would be great. I don’t want anything too bulky or that would make the room feel cramped.",
    "Perfect. Floating shelves with minimal hardware will maintain that streamlined look. We’ll use the same material as the side tables to ensure cohesion throughout the space.",
    "Yeah, that sounds great. I think with those updates, the room will be exactly what I wanted. Can’t wait to see it all come together!"
]






voice = "nova"
filename="0.mp3"
for i in range(len(dialogue)):
    if(i%2==0):
        voice="nova"
    else:
        voice="onyx"
    filename = str(i)+".mp3"
    speech_file_path = f"./3d_scenes/blend/Dark Bedroom/Conversation/{filename}"
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice=voice,
        input=dialogue[i]
    )
    response.stream_to_file(speech_file_path)

    # Print progress
    print(f"Generated speech for dialogue {i+1}/{len(dialogue)}")

