
from openai import OpenAI  #If first time using this repo, set the environment variable "OPENAI_API_KEY", to your API key from OPENAI
import tiktoken


client = OpenAI()
model_name = "gpt-4-1106-preview"
max_tokens=100000
encoding = tiktoken.get_encoding("cl100k_base")

temperature=0.0

system_prompt = """
Act like a design expert in multiple physical design domains like furniture design, interior design, architecture, industrial design, and more.
You will be provided with one or more transcripts of conversations among people like between a client and a designer, a senior designer and a junior designer, a design teacher and a design student, among a group of designers, or even within a designer talking to himself.
The transcripts may or may not contain the names of the people involved in the conversation. 
So, it is up to you to know who is talking to whom and what is the context of the conversation.

Your goal is to provide responses to the user's queries, comments, or questions by referring to the provided transcripts. 
You can also ask questions to the user to get more information about the context or the user's needs. 
You can also provide suggestions, feedback, or advice to the user based on the context of the conversation.
"""

message_history = [{"role":"system", "content":system_prompt}]



# Code borrowed from https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
def num_tokens_from_messages(messages, model=model_name):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo" or model=="gpt-3.5-turbo-16k":
        print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

def check_and_trim_message_history():
    offset=300
    global message_history
    global max_tokens
    global model_name 

    model_name_ = model_name
    if(model_name=="gpt-4-1106-preview"):
        model_name_="gpt-4"

    if num_tokens_from_messages(message_history, model=model_name_) > max_tokens:
        print("Current number of tokens in message history exceeds the maximum number of tokens allowed. Trimming message history.")
        while num_tokens_from_messages(message_history, model=model_name_) > max_tokens - offset:
            del message_history[1] # Delete the 2nd message in the history. The first message is always the system prompt, which should not be deleted.

def query(query,role="user", temp=temperature):
    global message_history

    # Retrieve n embeddings 
    


    message_history.append({"role":role, "content":query})
    check_and_trim_message_history()

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=message_history,
            temperature=temp
        )
        response_msg = response.choices[0].message.content
        message_history.append({"role":response.choices[0].message.role, "content":response_msg})
    except Exception as e:
        response_msg = f"Error: {e}"
    return response_msg

def initial_query(transcripts):
    transcripts_str = '\n'.join(transcripts) + '\n====================================================================================================\n'
    
    initial_prompt = f"""
    First, briefly introduce yourself.
    Next, based on the following transcripts provided, can you retrieve and provide potential to-do tasks, problems, insights, and important reminders raised?

    Transcripts: \n{transcripts_str}

    \n

    Lastly, answer with the tasks, problems, insights, and important reminders raised, as well as their respective timestamps. 
    Make sure that you describe the tasks, problems, and important reminders in a clear and concise manner.
    You can use the following format:

    [Introduction]

    Tasks:
    - Task 1: [Task description] (Timestamp: [Timestamp])
    ...
    - Task n: [Task description] (Timestamp: [Timestamp])

    Problems:
    - Problem 1: [Problem description] (Timestamp: [Timestamp])
    ...
    - Problem n: [Problem description] (Timestamp: [Timestamp])

    Important Reminders:
    - Reminder 1: [Reminder description] (Timestamp: [Timestamp])
    ...
    - Reminder n: [Reminder description] (Timestamp: [Timestamp])
    """

    initial_response = query(initial_prompt)
    return initial_response

def init():

    return 


if __name__ == "__main__":
    # response = query(initial_prompt)
    # print(response)
    print()


# transcript = """
# Okay, so let's say in a typical design session, usually in the stage of evaluating a 3D rendering, it's typically shown on a computer screen or on a piece of paper.
# So it's similar to this system. But what the system can do is that, let's say given a 3D rendering of some kind of product, the user or designer in this case could create different materials.
# And it could also apply different textures or colors onto different parts of an object.
# So I'll just give a simple demonstration here.
# So here, this uses artificial intelligence to first create a material texture.
# So if you look at this left spot, so this left panel here, it uses AI to create different materials.
# So let's say, given this, let's say nightstand, you can type in mahogany wood.
# And so what this does is that it generates texture maps that could be used to apply onto different parts of this nightstand in this case.
# So it usually takes a while, around 30 seconds.

# So it has a library already of different materials?

# Not really. It's incorporated, but not in the form of a library.
# So this is an AI that learns from a lot of data.

# 03:31.000 --> 03:39.000
# So in a sense, it learns from a library of images, including materials.
# And then you could actually refresh it again if you want, but let's say it creates a texture map like this.
# Let's say you want to apply this kind of material onto, let's say, you want to apply onto the drawers or the entire body of the nightstand.
# You can actually do that here on the spot.
# So that's kind of the generating part. So you could actually do this and you could save the rendering.
# Oh, and also it could, once it applies this, the system also keeps track of your material choices here.

# Could you also change the orientation or direction of the wood grain?

# 04:34.000 --> 04:41.000
# Not yet. Is that something that you're looking for in the...

# 04:41.000 --> 05:04.000
# Yes. Sometimes like for example the drawers, usually we do not apply it vertically yung grain. Usually it's horizontal. Same with what you see on the side. So it's more on horizontal direction yung grain niya, wood grain.
# So I would just suggest to add those options that it can be yung change na direction or like for example in case you want to use like in cars yung carbon fiber yung material,
# di ba parang it's sort of a textured, parang angled. So you could actually change or rotate. So that's my recommendation.

# 05:35.000 --> 05:42.000
# And sometimes we use it in diagonal form, diagonal direction also.

# 05:42.000 --> 06:00.000
# And I would also suggest if you would add or create options for like for example in this furniture, for example if you're designing furniture, including the type of weaving is important. So there are lots of options available or designs of weaving. So I suggest you also apply that as an option.

# 06:15.000 --> 06:31.000
# And another, if in case you want it darker, it can still be adjusted. For example sometimes when we use wood in its natural form, usually it's tinted also. They tint it if you want it darker or if you want it as is. So it's okay if you have the natural wood finish here but sometimes there are also different varieties of mahogany.
# So mayroon ding darker shade, mayroon ding lighter shade and also mayroon ding yung, I don't know yung sa may stem yung parang bilog na ganoon na para sometimes we add it to the texture.

# 07:03.000 --> 07:28.000
# So better to provide more options when it comes to... Just to tell you also sa mga 3Ds that some other people are using already and there are already libraries that you could download of those different materials.

# 07:28.000 --> 07:49.000
# Like if you're using for example 3ds max or if you're using rhinoceros and ayong mga 3D software, ayong mga what we call this yung parang yung keyshot, if you're using keyshot, do you know keyshot?

# 07:49.000 --> 08:08.000
# It's para siyang rendering software po. Rendering software na mga 3Ds. So they have this library of different material textures and if it's stainless, if it's mirror finish and if it's etching, you could actually have those options. You can even decide that if it's etching, the depth of the etch yung parang if it's shallow or deep or something like that.
# So you also have those different options to decide. So I suggest if you'll be using this as an AI, better provide those possible options also.

# 08:39.000 --> 08:55.000
# Okay. When you say etching or stainless, does that mean it gives different lighting conditions?

# 08:55.000 --> 09:10.000
# Not just lighting conditions. It's more on the material texture or finish. Like for example if it's sunblasted, it's matted like that. So if you want it glossy or high gloss,it's sort of a mirror finish or reflective mirror finish. So and if you want it like yung etching kasi, it's sort of a parang texture na like also matting, parang matt siya.

# 09:27.000 --> 09:45.000
# It's matt but more coarse yung when you say etching. If it's sunblasted, it's a little bit more fine but it deflects the light. It scatters the light so it has less reflective properties.

# 09:45.000 --> 10:10.000
# So something like that. So those options need to be available for designers to decide whether the design is okay. And of course having these options makes it easier for the designer or even the client to decide which finish to take.

# 10:10.000 --> 10:18.000
# Okay. So it's more on the glossiness or matte.

# 10:18.000 --> 10:45.000
# So I suggest not just wood, also texture and finish. Like for example even when using wood, you can even make it high gloss. And you can even make it yung matte or semi-gloss or something like that. So those options also needs to be available.

# 10:45.000 --> 11:02.000
# Okay. If I may ask, how do you manually using existing software like Rhino? How do you usually make like this wood in this case? Like how do you make it more glossy?

# 11:02.000 --> 11:25.000
# Because I heard that you also have to make like a bump map or like a reflectance map.

# I'm not that into 3D software but I only know how their capabilities. Because when I became head of industrial design in Panasonic, I only had my designers trained to use the software.

# 11:25.000 --> 11:48.000
# So I'm already in management when those 3D softwares became available. So yung mga staff ko, I evaluate those softwares depending on our need. Like what I'm telling you right now, I'm asking the suppliers, 3D software suppliers, what if we want to make it like this?

# 11:48.000 --> 11:59.000
# So that's how they demonstrate it and that's how I know that those softwares are capable.

# 11:59.000 --> 12:25.000
# So sa Keyshot is the most yung parang good reference because it's a third party software that they use for rendering. So usually Rhino or Solidworks are the most popular softwares that they are using.

# 12:25.000 --> 12:43.000
# Yung Rhinoceros, that's for designers, Rhinoceros and 3DS Max, Studio Max. And for the engineering software, we're using Solid Edge and Solidworks.

# 12:43.000 --> 13:04.000
# Yung Solidworks, I think it's built in already, yung 3D rendering. But for the Rhinoceros, I don't think so. So we have to use a third party software like Keyshot to render the 3D.

# 13:04.000 --> 13:18.000
# By any chance, do you know Blender? Blender, I heard about it but I'm not familiar in the usage or features of it.

# 13:18.000 --> 13:42.000
# So just to let you know, the rendering that this uses is Blender here. You just utilize the Blender then create an AI. That's what you're actually doing right now.

# 13:42.000 --> 13:53.000
# So I think Blender, if they're a 3D rendering software, probably they have a built in library already.

# 13:53.000 --> 14:16.000
# I don't know, maybe you need to buy it. Because in some cases, yung ibang companies, they buy those libraries. So you don't have to add or diba? As a feature, you just have to download yung material library.

# 14:16.000 --> 14:33.000
# So yun po, that's this feature of this material generator. I'll consider the reflectance comments.

# 14:33.000 --> 14:46.000
# So with this 3D rendering, you could actually save it on the existing rendering. So you could save in multiple ones. So you could do this. So that's like one AI that is responsible for generating.

# 14:46.000 --> 15:04.000
# As of now, these are like diffuse texture maps. So wala pa dito yung glossiness or reflectance. So if you look on the right side, this kind of AI acts as an advisor. So it's responsible for suggesting appropriate materials based on what you set in your design specification. So what I noticed during the design brief, if you look in this top, design briefs have like a target market or let's say a target place.

# 15:24.000 --> 15:42.000
# You want your product to be in or before. So you could actually set it here. So for example, in this case for a nightstand, you could actually set it to let's say, you could set it to hotel rooms or target market.

# 15:42.000 --> 15:57.000
# It's simply setting it to let's say for businessmen. So this is setting the target and place for the AI to know like who the product will be made for and like where it will be placed in.

# 15:57.000 --> 16:21.000
# And on the right side, these are material specifications. So what I noticed also is that they're looking, what I noticed in the design brief, you can correct me if I'm wrong, but their expected materials should be, you could write here like different adjectives like elegant. Or in some cases, let's say when you're designing outdoor furniture, you want, if you're making let's say, because in this case, these legs here are made of steel.

# 16:34.000 --> 16:48.000
# So it's expected that you want them to be non-corrosive. It doesn't have to be like objective descriptions. It could be something that's very subjective like elegant or something like that.

# And you can set it here. Probably you can set like weight, weight capacities or something like that, especially if you're designing chairs. Like for example, it should accommodate at least 300 kilogram person or something like that to the specifications. 

# And can I also suggest additional, it's more of a trend approach. Like for example, if you're placing that furniture inside a minimalist, so there are different design trends when it comes to interior design and where the furniture needs to go to. Like for example, if it's a minimalist design, so the AI should be able to provide options or like that when it comes to materials. So if it's minimalist, what are the different option materials?

# 18:00.000 --> 18:14.000
# Or if it will be located in a space where it's more of a tropical vibe or something like that. So I suggest you study those different interior trends. Like for if it's oriental, if it's Chinese style of furnishings or what do you call this? Western, modern, what do you call this? I forgot the terminologies. I suggest you also interview an interior designer for that to get those. Because interior designers have their specific style.

# 18:45.000 --> 19:10.000
# Like for example, a client asks, I want my room to look like Scandinavian inspired or minimalist. So those furnitures designed by IKEA are basically like that, Scandinavian minimalist designs.

# 19:10.000 --> 19:24.000
# So if you type something like that, they could probably recommend the AI should be able to recommend different material options or color options. And you can even specify the theme. Like for example, the theme of the room is black and white theme. So the AI can recommend like a black and white design option or maybe three types of material options. 


# Like what you can put in these material specifications like for example, should include color options. So wood is one. Wood or when you say industrial inspired, parang yung using of cement, yung parang polished cement, yung mga tiles or something like that. So what can match those materials when it comes to design? Do you understand what I'm saying? So kung ano yung trend, then the designer can select color palette options for trends. Kasi mayroon there are trends like in this case 2023 there's an incoming trend recommended by yung Pantone. They have this popular color trend for 2022 and 2023. So you have that group of options na lalabas doon. Then the AI can provide options already with regards to those colors.

# 21:09.000 --> 21:13.000
# Options you mean like materials? 

# Color also. Material and color. Since that's only our point of options right now, more on color, material, then probably the design has to be done by the designer.

# 21:33.000 --> 21:43.000
# The AI will not design for the designer. Is that your...

# 21:43.000 --> 22:00.000
# Currently the role of the AI is to simply apply different textures. But yeah to consider also putting in color. So different textures onto different parts.

# 22:00.000 --> 22:21.000
# So it helps with creation. But on the other hand, it could also suggest materials. So following your suggestion on trend, would it work if I say for material specifications?

# 22:21.000 --> 22:28.000
# Is it possible if I simply write minimalistic?

# 22:28.000 --> 22:41.000
# I would suggest that if you like for example that is a trend like design trend or what you call design approach. So I suggest if you talk to an interior designer, ask them the different design trends. Like if it's western classic or modern western or like Scandinavian or minimalist. 
# Because some designers won't have that luxury of they just immediately design it. But if the options are there, if you click that space you have already list of options to decide. So it's best to do it that way. Then if you select Scandinavian minimalist or industrial inspired, the AI can put some recommendations here on the right side.

# 23:37.000 --> 23:44.000
# So when you say options, these are the top trends?

# 23:44.000 --> 24:01.000
# Yes, design trend options. Because if you say modern western inspired or traditional western, that's two different things.

# So it can recommend different options just by selecting those. So lalabas na rito or light colored wood if you decide on modern western. So probably yung oak or light wood talabas as an option, yung light gray na wood.

# Kasi most modern yun ang ginagamit nila materials. Then if you decide on yung... like if in case you decide on what you call this yung parang Scandinavian na minimalist, if you chose a wood option, you can't see most of the grain. Very fine yung grain nila. So those materials that have high grain finish, very visible grain finish, that's more on western classic or traditional material.

# 25:18.000 --> 25:33.000
# Parang yung sa Baguio, they're more into wood. Yung mga bahay doon, yung mga lagkabin are more inspired by yung classic western parang ganoon or something like that. So the material are being decided based on the trend. Which trend do you want to go through? If you want to make it like Filipino, then what type of material?

# So probably it will recommend like a bamboo texture or something like that. Or oriental finish or parang Asian or… Yung parang Philippine traditional. If you select Philippine traditional, probably nandiyan yung mga bamboo material, yung bamboo finish, may texture ding yung bamboo. 

# They make it into slats then attach it side by side. So it becomes a traditional Filipino inspired material. So for a trend, a trend is associated with a certain type of material and color also.

# So that's my suggestion. You create an option of design trend. Since this is an AI supporting a design like a furniture designer, so it's best if I have those possible parang options when it comes to trend.

# 27:16.000 --> 27:32.000
# And basically the furniture that designers do depend on the preferences of the customer. So yung customer, pag sinabi ng customer, we want this type of approach. Similar with appliances. I have this client before na parang he's more into Apple and he wants me to design yung TV box. But his inspiration, he wants it to be more associated with Apple, yung Apple design. So that's very simple, very minimalist, tapos yung minimal details also very simple.

# 28:11.000 --> 28:25.000
# So even the curves are associated with, there are certain parang forms associated with Apple. So yun yung gusto niyan design ng ano. So yun yung sinasabi nila. So same with furniture.


# 28:25.000 --> 28:43.000
# Like for example, if you have a hotel sa client, so they have their type of inspiration for their rooms. So they give that in the form of inspirational pictures?

# 28:43.000 --> 28:55.000
# Pictures and also terminologies. Like I said, industrial inspired design.

# 28:55.000 --> 29:16.000
# Like Apple-like? 

# Apple-like inspired. There are certain designs that are also associated with brands like Apple. One is Apple. But there are also designs, especially if you're like for example in sports car. If you look at a Ferrari even from afar without looking at the brand itself, you know it's a Ferrari. So sometimes they say I want like a Ferrari inspired furniture or shoe.

# 29:30.000 --> 29:51.000
# Diba? There are shoes that may tatak na Ferrari. Yung I think that's Fila, they partnered with Ferrari to design a shoe for them or something like that. So there's sort of a parang identity, design identity when it comes to furniture.

# And like IKEA, it's identified to be like Scandinavian minimalist design of furniture and accessories or something like that.

# I suggest you add those options and provide the necessary. I suggest you also talk to an interior designer to ask those type of designs.

# And probably I think you can also search the internet. Probably it's available in the internet already. Interior design trends? Interior design trends. Baka nandun na mga options. Just include it in your, you don't have to talk to an interior designer.

# 30:41.000 --> 30:57.000
# Just search in the internet. Try to understand kung ano ba yung inspiration ng type of design trend. So you can associate. Yung lalabas na agad yung options dito.

# 30:57.000 --> 31:11.000
# So if it's Scandinavian, ganito lang yung materials, finish ganyan. Oh it should show a reason why it's suggested like these materials? Ganun po ba?

# Kasi yung material utilization is also based on the trend. So if it's American, sabi ko dapat nakikita yung mga wood. If you cut into a tree, yung parang may branch portion na may bilog-bilog na ganoon, they know that. So yung mga American inspired furniture also has those types of visible in the wood. Pero if you want minimalist wood, it's almost fine. Less visible yung mga grain.

# 31:54.000 --> 32:07.000
# So color lang ng wood. But if you look at it closely, saka mo naman di-determine na wood yung texture. Parang ganoon. If you talk about minimalist Scandinavian, ganoon ng karameya ng furnitures. Mostly fine-grained wood. 

# Okay. Sige po. Thank you for that. So if you set the target place or the market, there's another AI that could suggest different materials based on the descriptions you set.

# 32:30.000 --> 32:45.000
# Based on the trend. Design trend options. Pwede po. In the future, it could suggest based on that. But as of now, it suggests materials based on what you set here.

# 32:45.000 --> 33:02.000
# So if it's elegant or it's not corrosive. May bug po pala dito. Is it okay if I show a walkthrough? Because there's a bug here. Sorry for that. So this is just a walkthrough of this interface here.

# 33:02.000 --> 33:24.000
# So what the user first does is that it asks the AI to suggest what kind of material, whether it's wood, metal, fabric, or ceramic. So something like this. And then you select the kind of description to suggest it on, whether it's elegant or non-corrosive or minimalistic.And then to give context, you have to ask for what kind of product. So in this case, it's only just one product. So you can actually select if it's for a nightstand. And then if we select this, you could also select for what kind of part it's on.

# 33:41.000 --> 33:55.000
# So if it's not for a specific part, you could suggest it for overall for a nightstand. Because correct me if I'm wrong. Because the bedside tables, they tend to have one material across. So it really depends.

# 33:55.000 --> 34:12.000
# And then here, on the last part, you add more context by suggesting if it's for hotel rooms or if it's for businessmen. So essentially what this does po, is that it creates some kind of prompt here, a request.

# 34:12.000 --> 34:30.000
# So this kind of sentence, examples of wood materials for hotel rooms are, the task of the AI is for this to autocomplete. So what it does is that it suggests materials based on this context.

# Okay, so I think there's a bug here. But essentially, sorry, going back to this slide. But if you look at the bottom right, if you look at number six, this is what the, if you could see this, this is what the AI says. So it suggests materials like mahogany, walnut, cherry, and it kind of gives a reason.

# 35:28.000 --> 35:41.000
# And then here it extracts the most, like it extracts the suggested inputs you would put in the material generator. So in this case, wood, mahogany, oak.

# 35:41.000 --> 36:04.000
# So you could use this to suggest materials that are elegant or minimalistic or like following your comment, but that are based on a specific trend. So and I would suggest these materials. So that's kind of the suggestion module.

# 36:04.000 --> 36:23.000
# And so these two parts. So the role of this AI is not to just suggest materials, but it could also evaluate materials based on these place or target market or specification set. Sorry, it's still a work in progress. But let's say you transfer a texture and it keeps track of your material choices. So this AI here, it could critique your design based on how it's appropriate for the environment that it's in.

# 36:40.000 --> 36:50.000
# Based on each of the specs and also based on how the parts are assembled together. Yeah, I'll just walk you through because it's a very low prototype.

# 36:50.000 --> 37:00.000
# So if you see, this is like a little simple prototype for each critique. So starting with the material specifications. So here this shows like an evaluation grid for each part of the material. So if you go back to this nightstand, it keeps track of which material is assigned to each part here.

# 37:13.000 --> 37:22.000
# So this is the first column here and the rows here are each of the material descriptions. And so each cell, it shows a score given by the AI and the score ranges from negative one to one. So it shows how like more positive or negative its response is. And so this is like the question here. If you look at the top here, the queue, this is the question that's being asked to the AI. And in each cell, it gives a response. And in each cell, it gives like an overall score based on how negative or positive it is. So if you click on the cell, for example. So if I click on, if you look at here, if you click on whether a black marble drawer is a suitable material that is non-corrosive, the AI would give like a long response like this. Or if I click on the steel leg, it would give a response like this.

# 38:17.000 --> 38:32.000
# So I suggest to make the response simpler like using keywords only because a lot of will not read text like this as a recommendation. So better if it's a bullet type, then just use simple phrases and keywords. It's faster and easier to understand. So that's my recommendation. 


# And I think for this one, for every material, I think you need to create rubrics for that. For the how to critique, it's similar to just how to grade. When you grade, you have rubrics.

# 39:16.000 --> 39:27.000
# What you're showing here is almost similar to a rubrics type of grading or evaluation. So you can use the rubrics and it needs to have description also when you say elegant in what aspect or the level of elegance based on the type of material or something like that.

# And sometimes when you say elegant, it's not only based on the material, it's sometimes also based on the design. Like for example an oak wood, if you design it or use it in a different aspect, like if you use it as a dining table, so oak wood can be graded a high score. So if it's designed for a specific type like for a bar or a stool, then probably it's not designed as an elegant material. So it can be elegant based on the application.

# 40:50.000 --> 41:01.000
# Okay. So it depends on the product po? 

# Depends on the product. Not basically based on the material.

# 41:01.000 --> 41:18.000
# Okay. Does this apply to let's say weatherproof or non-corrosive or should there be an option where you say it should be elegant for the product and not for the material?

# Probably when you specify weatherproof, usually we specify weatherproof if it's the material or the product is located outside or outdoors. But if it's outdoors, it doesn't have to be waterproof. It can be waterproof like for example if it's a dining table where you can spill off juices or water. Or probably if it's a parang counter, kitchen counter, so it requires.  But you can also add like oak wood then with like if you add a finish to it like epoxy, like clear epoxy or polyurethane coating to it, then it becomes waterproof. Not just the color or the type of material. Sometimes it's based on how you finish it, how you finish the material. So the recommendation here, like for example, probably it's created like that, then it can be waterproof if coated with polyurethane as a recommendation.

# 42:45.000 --> 42:54.000
# Or if it's like coated with clear epoxy, then it can be waterproof.


# 42:54.000 --> 43:05.000
# Okay. So given the evaluation, you're expecting some kind of recommendation to make it waterproof?

# 43:05.000 --> 43:33.000
# Yes. And of course wood is corrosive. Although it can be affected by water after a long span of time. So it can be as a recommendation to coat it with clear coat materials. At durable clear coat materials.

# 43:36.000 --> 43:47.000
# Okay. So when you mention you're not sure, but would it help if like instead of like a rubric table, there could be some blanks? Because like some certain descriptions doesn't apply to a certain like material or something like that. Does that make sense? You don't need to evaluate if the oak wood is non-corrosive because it's not something you would look for?

# 44:07.000 --> 44:24.000
# Probably if like for example, if it's oak wood only, then it's not weatherproof. It's corrosive because of course water destroys anything after a long span of time.

# 44:24.000 --> 44:38.000
# So it can be corrosive also. But as a recommendation, you need to add material to it like a coating. So probably it should have negative points for that if it's just base material. But I don't know if you can still like for example if it's coated or coated wood base here in the left side of the table, then probably it can be weatherproof or non-corrosive. So depending on not just the raw material, but including the finishing. 

# Okay. So going back, it should like specify an option for adding a finishing or something?

# 45:24.000 --> 45:37.000
# Yes. Going back to the rubric, do you think like showing these kinds of numbers are easy to see? Because you mentioned about changing this to a rubric type. So would it be better if there's like a letter grade instead?

# 45:45.000 --> 45:54.000
# Is that what you mean by changing the rubric? Sometimes it's like what you're presenting. It's how would you grade that?

# 45:54.000 --> 46:05.000
# There should be a legend or some sort of a legend that says if this points, it is not acceptable or something like that. So it has to have like a, what do you call this? Some sort of a legend.

# 46:20.000 --> 46:39.000
# Or parang ano ba yung highest point? What's the highest point that can be generated? Because I can't understand here kung ano yung ibig sabihin ng 0.37, 0.7, 0.07.

# 46:39.000 --> 46:54.000
# So is it good? Or is it bad? Or it's too low? Or is it too high? So dapat meron kang from 0 to ganyan is satisfactory or failed.

# 46:54.000 --> 47:18.000
# Or 0 to or is satisfactory then this point to this point is ano. So as a user of this table, how would I know if it passes that standard?

# 47:18.000 --> 47:32.000
# Yung passing grade ano ba yung passing grade? How would you rate that totally? Does it pass or is it failed or something like that?

# 47:32.000 --> 47:44.000
# Like for example if I add floating to the wood, it will increase the points then can this design pass or does it still fail?

# 47:44.000 --> 48:04.000
# So there should be a legend showing where does 0.37 fall if it's satisfactory, neutral, very satisfactory and then also an overall score of whether it's pass or fail.

# 48:04.000 --> 48:17.000
# So just to give information, the scores here it's based on a method called sentiment analysis. Basically what the AI does is that given this text, it checks if the text sounds more positive or more negative. So more positive means like let's say black marble is very good. So that's leaning towards let's say the score of 1 and then let's say black marble is very bad. That's more leaning towards negative 1. So the reason why I'm telling you this is because the AI doesn't have a notion of what elegance is but it gives a score based on how positive or negative its response is in relation to the material and the aspect being assessed together. So yun pa. I'll take note of your comments.

# 49:16.000 --> 49:22.000
# So going to the next slide po. So this is for critiquing the material specs. So here this is, so if you look at the third tab on the right, this assesses how each parts can be assembled together. Kasi po correct me if I'm wrong but the way you, the things that you use to attach different parts, it's dependent also on the material. Does that also play a factor?

# 49:44.000 --> 49:52.000
# I don't understand what you're saying.

# 49:52.000 --> 49:57.000
# So let's say with this example.

# 49:57.000 --> 50:11.000
# So the question I ask to the AI is, can this certain material of a part can be attached to a part of this material?

# 50:11.000 --> 50:21.000
# So for example, can a black marble drawer be attached to the oak wood base or can the granite handle be attached to the drawer?

# 50:21.000 --> 50:30.000
# Meaning like joined together or just, is that what you're saying?

# 50:30.000 --> 50:33.000
# Yes but like can it be joined together?

# 50:33.000 --> 50:45.000
# Okay. So with the right type of, I think it can be. So the AI will decide whether it can be or not?

# 50:45.000 --> 50:51.000
# Yes but like it gives like evaluation here.

# 50:51.000 --> 50:56.000
# So it's similar to like the previous critiques. It kind of gives a score also.

# 50:56.000 --> 51:07.000
# And here if you click on the button, it gives a response. So here I'm showing like two different types of responses. Kasi po yung AI, it's to be frank, di siya consistent.

# 51:07.000 --> 51:17.000
# So in the top response, it says that you need to drill holes or add screws and fixings to attach your legs onto an oak base.

# 51:17.000 --> 51:26.000
# So it shows it's this kind of response. And on the other hand, this is more of a negative response. So the top is a positive response.

# 51:26.000 --> 51:34.000
# It shows what you can use but the negative response, it sometimes it could say no, but it's not in this case, it's not necessarily the reason.

# 51:34.000 --> 51:46.000
# Like the reason here is because the part should be consistent. Does the bottom response also make sense to you?

# 51:46.000 --> 52:03.000
# I don't think that's because basically you can use steel. So it's not a negative thing to use steel because steel is more durable especially for when you add like for legs when weight is utilized.

# Like for example, if it's heavy or wood is sort of not recommended material for this one. But if you say that steel is more expensive like something like that compared to wood.

# In comparison to cost, probably you can use wood. But if you want it to be durable or long lasting, steel is the most recommended one.

# And it can be attached kasi nga using nuts and bolts or screws can also be used to attach those different materials.

# 53:09.000 --> 53:30.000
# Okay. So it gives a score whether how like possible it could like attach them together. So what are your thoughts on this kind of critique? Like how helpful would this be for the designer?

# 53:30.000 --> 53:42.000
# Since these are all recommendations, you need to… So with the questions, there shouldn't be any negative response to my suggestions. But there should be options.  Like for example, i When attached to like a marble cannot be done. But you can basically attach it using... You cannot use adhesive. Like for example, any type of adhesive to attach marble to… It will definitely still break apart. But if you use nuts and bolts or different, there are even hinges that you could fix. But like for example, in this case marble, it's sometimes difficult to screw in or sometimes it cracks. Drilling a hole is also not that recommended.

# So if you add too much pressure to it or parang pupuk-pukin mo, holes can cause cracking or breaking. So kaya nga karamihan ng marbles doesn't have any... But there are even materials that you could use in marble to attach it to wood like yung mga countertops.

# Di ba may special type of adhesive that they are using. I don't know what it is. You can ask and ano. Pwede siya. Based on specific purpose. But if it's designed to be furniture, probably that's not recommended. Kasi nakapatong lang siya. Walang masyadong movement. But if there are movement like for example the legs or sometimes you move furniture around, baka matanggal din yun.

# So it's best to screw it together with the adhesive or something like that. So the AI should know the process. Also knows different material options. Then of course depends on the application also.

# 56:21.000 --> 56:26.000
# So application you mean depending on the product?

# 56:26.000 --> 56:41.000
# The product usage. Depending on the product usage. If it's just a bar top like yung marble, if it's just a bar top or a fixed table, attached to a cement stand, so probably it will not be easily damaged just by using adhesive. Special type of epoxy adhesive.

# 57:00.000 --> 57:11.000
# So it can be fixed. But if you usually like lalagay mo ng legs that are just vertical without any frame or something like that, probably matatanggal yung legs na yun. It will not firmly attached to it. But depending on how the product is used.

# 57:21.000 --> 57:32.000
# So yung legs needs both a frame and adhesive? If nakapatong lang siya and it's not moving around, so it can be firmly attached.

# 57:32.000 --> 57:52.000
# Okay. So it depends on the usage. Depende talaga sa usage. Kaya designing is sort of like assembly requires also expertise and knowledge of material.

# 57:52.000 --> 58:04.000
# It's not just yung design. When we talk about design, kagaya na kami, we're designers, we design it. But sometimes mechanical engineers are the ones assembling it or designing it to be assembled. So it requires two different. Like in construction, you have a structural engineer. Then yung architect yung designer or kaya yung interior designer ang nag-design. But they only design it that way.

# 58:28.000 --> 58:42.000
# And the ones executing the designs are structural engineers or civil engineers. Sila yung nag-execute.

# 58:42.000 --> 58:58.000
# And when it comes to furniture, same interior designer, industrial designer, we design the furniture. Then the person executing it are the manufacturers and usually they have engineers with them.

# 58:58.000 --> 59:25.000
# So ang kasi nito, it's not design based already. It's more on the assembly. So is that your intention also, pati yung complete AI that including the manufacturability of the product is considered? 

# Yes po. So the scope of this project po, it's very material driven.

# 59:36.000 --> 01:00:00.000
# So the intention of this product is to assign textures but also remind designers that you should make sure that whatever material assigned to this product, it should help them check if this material or color follows the trend or if it's of a certain style desired by the client.

# 01:00:15.000 --> 01:00:29.000
# Or in the special case of making furniture, if it has these specific material properties, if not the AI should suggest what to do to coat it. And lastly, it should assess if the type of material based on the part can be assembled together. So following your comment here, so instead of just showing a grade, it should also show what the options it could use to attach these parts together. Is that correct?

# Yes. So that part you decide the option should be provided by AI.

# 01:01:01.000 --> 01:01:17.000
# Ayun po. So that's for assembly. The last part is essentially if the material is a suitable material for the environment that it's in. So parang baliktad po siya from the suggestion.

# 01:01:17.000 --> 01:01:31.000
# The suggestion module gives materials that are appropriate for an environment. In this case, it could be chen here. But it follows the same thing. It shows a score but I didn't write it yet.

# 01:01:31.000 --> 01:01:41.000
# But these are some of the responses shown by the AI. If you click on the view critique, it shows the full response here.

# 01:01:41.000 --> 01:02:05.000
# I may ask, is it okay if you could pick a read on both of these responses and if these actually make sense?

# 01:02:05.000 --> 01:02:32.000
# Looking at the first question, the answer is sort of like for example when you talk about heat, where should be the heat coming from? If it's in a hotel room, why is heat considered? Probably cool or lower temperatures. So I think it's inaccurate when it comes to recommendations.

# 01:03:11.000 --> 01:03:33.000
# So where should be the heat? And when it comes to the thermal coefficient and what does that mean? It's sort of an indirect answer. Parang masyadong pinaiikot-ikot na eventually.

# 01:03:46.000 --> 01:04:03.000
# To be safe, I would suggest testing the effect of heat. So sana magkukunin yung heat in the hotel room, where's the heat coming from? It should be a normal temperature lang. Can you say convenient temperature? You surely maintain around 26 or 27 degrees ambient temperature. So where is the heat coming from? So why is it not recommended or why is there an issue about it?

# 01:04:24.000 --> 01:04:53.000
# So in the lower portion, just read it a bit.

# 01:04:53.000 --> 01:05:21.000
# So in this case, you're talking about yung oak wood and dapat hindi veneer. And that's the recommendation. Like I said, medyo mahirap intindihan. Do you know ang infographics? So usually it's easier to read it through bullets. Sometimes you could easily understand and it will retain longer in our memory. So in this case, medyo some phrases are conflicting.

# 01:05:58.000 --> 01:06:14.000
# Not advisable to do it yourself. Do what? In case you don't want to bed stand for a couple of weeks, do what? So sana gagawin niya? Is it directed to the designer or is it directed to the user itself? So kasi even will not survive abuse, why is the oak that low quality material? So if it is, it shouldn't be recommended in the first place as a material.

# 01:06:49.000 --> 01:07:03.000
# So parang ganoon. Dapat sa uno pa lang. And usually when designers do, they are already familiar with the type of materials that they are using.

# 01:07:03.000 --> 01:07:25.000
# And sometimes it is cost related. If you have a high end hotel room design, like if it's designed for Manila Hotel or Sopitel or something like that, probably you would use Nara or Mahogany or something like that. But if it's a lower, like a 3-star or a business hotel, probably you would just use... Actually veneer type or veneer laminated medium density fiber board can be sufficient enough for cabinets.

# 01:08:00.000 --> 01:08:11.000
# Particle board is the lowest form. Yung laminated lang, vene laminated, yun ang pinakamura. But there are also high end like particle boards that are laminated with melamine. Parang wood design pero plastic siya. So melamine is a bit expensive, more expensive depending on the type of veneer that you are using.

# So sometimes cost should be considered. Like if you chose Mahogany, it should be recommended that it is an expensive material. But highly durable when it comes to something like that. So wear and tear especially with Nara. But it needs to be cleaned and dried properly.

# So yun yung mga... Dapat ano lang keywords lang yung mga sagot ng hindi. Not a text like this. It's difficult to understand.



# 01:09:25.000 --> 01:09:47.000
# So the role of the AI material advisor is to assess if the material you chose is appropriate. In this case, if it's appropriate for the target environment, for descriptions, and based on the material, if the parts of a product can be linked together.

# 01:09:47.000 --> 01:10:08.000
# I would suggest also to change the term like critique. Kasi when you say critique, it's more of a design aspect, more an aesthetic or style of design.

# Or best to use the word like if it's feasible or not feasible, like feasibility rather than critique. Like view feasibility like that. Although critique can be used in other terms like when you read a book, it can be critique. But usually when you critique, emotions are considered.

# Like if you're happy with the design or it's sort of a critique based on your emotional response to a specific design or aesthetics.

# 01:11:07.000 --> 01:11:23.000
# But if you talk about technical aspects, like if this design is okay or not, or this design requires to be accepted like lamination or coating. So it's more of talking about feasibility.

# 01:11:41.000 --> 01:11:57.000
# If you're assessing a material based on its feasibility, for example, in the case of hotel rooms, is material feasibility in a hotel room based on feasibility or is that more on aesthetic?

# 01:11:57.000 --> 01:12:18.000
# Kasi like I said earlier, when you say hotel room, it doesn't define any specific level. Probably if you say na yung five-star hotel or hotel room or even the five-star hotel room have their economy suites, they have the presidential suites or the high-end. So it doesn't define specifically.

# 01:12:32.000 --> 01:12:55.000
# I suggest to utilize more on the design aspect. Yung sinasabi ko kanina yung trend, the aspect of trend. Yung parang industrial or minimalist or the style based on the design style. And you could even grade it based on yung level of cost. Like for example elegant, you can claim that as highest. Then yung mid-range tapos yung lower cost.

# 01:13:16.000 --> 01:13:28.000
# Pag sinabi mong hotel room, it doesn't define any specific level of quality or level of… Okay. So it's important to be specific. In the hotel, it's important to be specific. It's more on the specific trend of space, utilize for the space. Yung design.




# 01:13:46.000 --> 01:14:03.000
# What are your design approach for that space? Ano ba ito, high-end? Is it high-end, middle or low-end? Kahit yung tatlo lang yun, yung high-end, mid-range tapos yung low-end.Then I would also suggest if you're talking about feasibility, cost should be a factor also.

# 01:14:12.000 --> 01:14:28.000
# Okay. When you say cost, do you mean in this case the system has to be aware of a budget amount or does it mean the general notion of cost?

# 01:14:28.000 --> 01:14:47.000
# It can be the general emotion or general approach to a client. Kasi it can still be expensive but in a different sense. Like for example pagka-high-end, ito yung material na pwede mong gamitin. If it's mid-range, these are the cheaper ones, then these are the cheapest material but it can still be associated with the look.

# 01:14:59.000 --> 01:15:24.000
# Yung Scandinavian minimalist, you can decide whether it's high-end, mid-range or low-end. Then you can provide different options. If it's high-end na Scandinavian, then materials needs to be really expensive.

# 01:15:24.000 --> 01:15:38.000
# Like IKEA, it's more of a mid-range target market. Kasi it's even knocked down. You have to assemble it yourself. So it's easier on the packaging and also designed to be durable. But for the high-end material, usually it's fabricated as a whole.

# 01:15:55.000 --> 01:16:09.000
# It's designed specifically for that specific purpose or given space or given function.

# 01:16:09.000 --> 01:16:27.000
# So yung cost, it would depend on what trend you choose? What trend and what level of market. Yung market mo dapat ganoon nalang nilalagay mo, high-end, mid-range or low-end.

# 01:16:27.000 --> 01:16:42.000
# Wag naman yung chip kasi chip doesn't compute. Pag sinabi mo chip, isirain din yun. It can still be durable but the target market is a low-end. So it's best to use cheaper material like tangili rather than mahogany or oak or nara.






# 01:16:52.000 --> 01:17:01.000
# So there should be a sense of what country it would be used in?

# 01:17:01.000 --> 01:17:30.000
# I think that doesn't have to be what country. Sometimes we export and we export our own design. It's even designed for the local market but other countries prefer those designs to be like an accent piece to their furniture or their inspiration for that design of the room.

# 01:17:30.000 --> 01:17:35.000
# Okay. Understood po.

# 01:17:35.000 --> 01:17:59.000
# Oh, it's 3.70 po. Sorry, I think we went overtime. Is it okay if we could wrap this up in like 5 minutes? Is that okay po? Sorry. So just one last point. You mentioned before that you're hoping that you could set the description.

# 01:17:59.000 --> 01:18:19.000
# You could let the user input a certain weight when you assign to us. Say that this could hold a 300kg person. So it should be able to check if it's durable in that kind of sense.

# 01:18:19.000 --> 01:18:26.000
# Yes. That could be an option or a specification.

# 01:18:26.000 --> 01:18:40.000
# If I may ask po, let's say I make this out of white marble and I want to assign this material po onto this base of the nightstand. So how does that change the shape of the design in your case to make it more feasible or manufacturable? Would there have to be a change of the shape if the base aims to be made out of marble?

# 01:18:59.000 --> 01:19:12.000
# It can be made of marble but it can be laminated one. Like for example marble finish but not an actual marble. Some melamine materials. Like I said melamine is a plastic material. It can look like a wood. It can look like a marble. Sometimes the marble finish is just printed on top of the melamine.
# Even the wood, when you fabricate the melamine, may texture na ng wood then the color is only applied later. Parang ganoon. It can be finished to look like a marble.

# 01:19:49.000 --> 01:20:03.000
# But probably it's difficult to make it a marble itself kasi like I said marble is difficult to fabricate. That's why usually they only use marble as a top, as a countertop, a table top. They don't even use that as a chair. Then the marble can be used as a sculpture.



# 01:20:23.000 --> 01:20:38.000
# Yung tinitistis lang or carved. Not carved kasi carved is for wood. So parang tinitistis lang. I don't know the term. Like parang sculpting. Using parang masonry ang approach. So it cannot be made to be like that. Usually just the top is marble then the rest are wood. Or you can even use like I said melamine as a marble finish. But it can't even be used as a veneer kasi masyado manipition. It will definitely break.

# 01:21:11.000 --> 01:21:27.000
# So those are some of the limitations that the AI should know about yung manufacturability of materials.

# 01:21:27.000 --> 01:21:42.000
# So if lower options, like for example if your client is low-end, you have a low-end market, it could look like the same.

# 01:21:42.000 --> 01:21:58.000
# And the AI would suggest differently. Like for example just using vinyl lamination. So you can even search yung sa Shopee. There are even vinyl rolled lamination that you could just use adhesive to apply it on your wooden table. So nilalaminate lang siya.

# 01:22:14.000 --> 01:22:29.000
# It even have its own adhesive already. So the material can be cheaper but still that can be achieved depending on the level of quality.

# 01:22:29.000 --> 01:22:45.000
# So if you want it high-end, that's the option. The top can be marble then the rest can be like melamine. Then melamine is laminated. Medyo matigas yung melamine and it's laminated on a medium-density fiberboard.

# 01:23:00.000 --> 01:23:21.000
# Dapat makahiwalay po. To finish the color. Okay, understood. Sorry last question po. When you're designing let's say furniture, do you usually evaluate renderings by individual product or do you also evaluate a family of furniture, like a furniture set? 

# It really depends. If you would talk to Kenneth Cobon po, do you know Kenneth Cobon po? So he doesn't create probably a theme. Tumagawa siya ng theme. But usually the pieces are sold individually. So it's up to the designer or gear designer how it would match other furniture designs.

# 01:23:57.000 --> 01:24:12.000
# It's not usual that high-end, probably the mid-range and the low-end is where matching furnitures are available. Probably also in the high-end but like for example the couch and the center table is a set. But mostly for the high-end furniture, you buy it in different sets.

# 01:24:30.000 --> 01:24:49.000
# The couch is different. Then it's up to the interior designer to match it. Kasi if you buy it in sets, it's most probable that you would also see it in other houses.And some clients want their own style or own individual design. Something that they own. This is my living room and you can't see it anywhere else. So something like that. 

# END SUGGESTIONS

# 01:25:12.000 --> 01:25:36.000
# I think that sums up the consultation for today. So overall, the goal of the system again is to help designers with material texturing while considering feasibility.

# 01:25:36.000 --> 01:25:56.000
# So with your impression of this right now, how helpful do you think this would be if you applied this to let's say in an actual design session looking ahead into the big picture of this project?

# 01:25:56.000 --> 01:26:18.000
# Sometimes this can be improved based on the presentation. For example, you have that main furniture on the center and it should be expanded. I'm talking about the layout. When it comes to feasibility or if it can be used by designers, then I think so. But presentation wise, you have to focus on the viewability.

# 01:26:39.000 --> 01:26:52.000
# Kasi I'm looking at it, parang maliit yung furniture, I can't appreciate it. So if you make it majority of the space, then nandiyan naman yung mga options.

# 01:26:52.000 --> 01:27:07.000
# Or if you click the specific menu, lalabas yung mga options. Then when you select it, immediately. So dapat medyo mabilis kasi, hindi nang antay ang client.
# So that's what furniture or best presented. So this material can be used as not just a personal tool of the designer but something that he can use as a presentation to the client.Hindi lang para sa designer, para sa client din. So if the client sees this, I think I wanted something more ganyan, then he could provide options in front of the client. Then if the client says, oh that's okay, I want that design already, then you can have faster or quicker approval. 

# So the difficulties with dealing with clients is that their satisfaction is really important because they're the ones paying you for your design. And you cannot present really bad designs. But sometimes even though you presented your best design recommendation, yung clients are still looking for something different. So it's also best to have options like this one. Then you could change material. So it's easier too. You could create those options already at the bottom. Then present it to them in different...

# 01:28:48.000 --> 01:29:05.000
# And I would even suggest that if this can be placed with a background, for example if I click the Scandinavian minimalist, you have a background na Scandinavian minimalist, then placing it in that location, then does it match or not? Then the client can appreciate it already. So sometimes when we present to clients, products are usually even virtual, products are placed on their specific scene. So kung gusto ng western inspired hotel rooms or something like that, if it's a hotel room, if it's a condominium unit, then show a condominium unit with that style or inspiration.

# 01:29:59.000 --> 01:30:14.000
# Okay, understood po. About the AI, so you mentioned before that you're hoping to also evaluate if a certain furniture could hold a certain weight.

# 01:30:14.000 --> 01:30:29.000
# Do you hope the AI could also give an evaluation on apart from whether it's appropriate for environment or specifications or if it could be assembled together?

# 01:30:29.000 --> 01:30:44.000
# The environment should also be considered if it's outdoor or indoor. Like you said, it should be waterproof or all weather. If it's all weather, it's different from being waterproof.

# 01:30:44.000 --> 01:30:59.000
# Because if it's all weather, the aspect of the sun is also considered. Then there are different materials that are mostly affected by the sun, especially the wood.

# 01:30:59.000 --> 01:31:14.000
# If it's an outdoor furniture, there's a specific type of coating is recommended or probably a different type of material is recommended.

# 01:31:14.000 --> 01:31:29.000
# Okay po. Would you hope if there's a way this could evaluate ergonomics also?

# 01:31:29.000 --> 01:31:50.000
# Actually, probably there's a possibility. For example, the height based on the usage. If it's sitting down or besides the bed. So what's the standard height is recommended. So there should be a range because ergonomics is also based on usage.

# For example, in cars, it's more on the lounging position. For sitting also, there are working positions like the sitting.

# 01:32:25.000 --> 01:32:43.000
# It should be upright straight. Then if you're lounging, the angle of the seat should be at least 3 to 5 degrees or something like that going towards the back.

# But if it's lounging, I think it's about 35 degrees towards the back. Then the angle of the backrest is also. So there's an ergonomic based on the actual usage. It should meet certain heights or angles but when you're using the product. 


# Okay po. So that wraps up the session. Sorry po for being over time.

# 01:33:15.000 --> 01:33:24.000
# Thank you po alit for your comments again. Is it okay if I could consult you every month or two months?

# 01:33:24.000 --> 01:33:39.000
# It's okay. When is your defense or presentation? Actually matagal po po. My final defense is next year 2024 siguro mga March 2024.

# 01:33:39.000 --> 01:33:46.000
# I just presented my proposal pa lang po and I'm doing the prototype.

# 01:33:46.000 --> 01:33:55.000
# So are you also consulting other designers? Yes po. Including interior designers and also furniture designers.

# 01:33:55.000 --> 01:34:05.000
# If you want to focus on furniture designers, you need to have furniture designers or furniture design professionals.

# 01:34:05.000 --> 01:34:18.000
# May pinigay ako sa yung dating name as a designer. Did you contact him? Yeah I contacted both of them. Tito de la Pena and yung creator ng vacuum.

# 01:34:18.000 --> 01:34:32.000
# Si Jantan. So did they also give you order? Actually they didn't respond po. Pero yeah I could follow up naman po again.

# 01:34:32.000 --> 01:34:44.000
# Yeah pero thank you. I think I should reach out to furniture interior. Did you mention that I recommended them to be...

# 01:34:44.000 --> 01:34:53.000
# I think I did. I think so. Pero I could follow up again naman po. Yung interview is still ongoing.

# 01:34:53.000 --> 01:35:03.000
# See you po. Thank you sir. Okay and you could even sought the help of Design Center of the Philippines if you want.

# 01:35:03.000 --> 01:35:18.000
# Do you know Design Center of the Philippines? Hindi po no. So I think they have a website and are you located in Japan ba?

# 01:35:18.000 --> 01:35:28.000
# Yes po. I'm located here in Japan po. So probably you can email to them. It's under DTI.

# 01:35:28.000 --> 01:35:39.000
# Department of Trade and Industry and Design Center of the Philippines or Product Development and Design Center of the Philippines.

# 01:35:39.000 --> 01:36:02.000
# Yung kanilang Facebook account. So they have employed many designers or have done a number of projects when it comes to furniture design or designing home accessories.

# 01:36:02.000 --> 01:36:15.000
# So I know some of them that worked there. Maybe you could also...

# 01:36:15.000 --> 01:36:44.000
# Agnoni. I don't know if... yun yung ano niya sa Facebook. AGnoni. Then there's also Ray Sullivan.

# 01:36:44.000 --> 01:37:01.000
# Parehas yan furniture designer. And you could also ask Leo Wapper.

# 01:37:01.000 --> 01:37:14.000
# But about... siguro if you want to talk to an interior designer.

# 01:37:14.000 --> 01:37:36.000
# Maybe Mike Suki. M-I-K-E. S-U-Q-U-I. So just tell them I recommended you not to be interviewed for your project na lang.

# 01:37:36.000 --> 01:37:46.000
# So if they do not respond, probably they have forgotten already. So hindi naman siguro pero probably they're too busy.

# 01:37:46.000 --> 01:38:06.000
# Medyo busy kasi yung mga yan. So si Ray Sullivan designing for a number of furniture manufacturers. Marami siyang ano.

# 01:38:06.000 --> 01:38:22.000
# Try si Ito Kish. Ito Kish is a well-known furniture designer. Pero by order na lang kasi yung furniture niya ngayon. Wala na siyang showroom.

# 01:38:22.000 --> 01:38:36.000
# You can search his name kilala yun. Ito. Ito Kish. Kish. K-I-S-H. So we met a number of times pero not too...

# 01:38:36.000 --> 01:39:03.000
# Sabi mo na lang maybe you can help me with my... at least furniture designer. Anyway, just giving you a number of options. Si Rachel Danielan.

# 01:39:03.000 --> 01:39:08.000
# How do you spell Danielan? D-N-D-A-N-Y-A-L-A-N?

# 01:39:08.000 --> 01:39:33.000
# D-N-Y-A-L-A-N-Y-A-L-A-N. Pero alam ko may G yun eh. Sorry hindi ako... pero anyway. Bihira naman yung name niya. Former faculty also of Binel. And also a known crafts at furniture designer.

# 01:39:33.000 --> 01:39:38.000
# I'll reach out to them. Thank you po very much for this.

# 01:39:38.000 --> 01:39:51.000
# Para may makuha kang ibang ano. Sa interior designer probably yun lang yung kakilala ko talaga pero there are marami naman silang furniture designers.

# 01:39:51.000 --> 01:40:12.000
# Pero when it comes to trend ka sabi ko you can search the internet. Yung sa style ng interior design. Different styles. Tapos yung sa color, yung sa pantong yung trend for 2023 or something like that. Para yung mga options.

# 01:40:12.000 --> 01:40:28.000
# Okay. Sige po. Thank you sir. Thank you sir ulit po. Okay. No problem. Just let me know if you want to have another interview. Pagka meron ko ng ano uli. Okay?

# 01:40:28.000 --> 01:40:42.000
# See you po sir. I'll see you whenever po. I'll end the meeting na po. Have a nice afternoon po. Sige. Welcome. Bye bye. Bye bye.

# """