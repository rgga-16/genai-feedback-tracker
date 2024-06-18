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
    "transcript": "1\n00:00:19,740 --> 00:00:24,899\nSpeaker 2: I have a motorbike called Argy.\n\n2\n00:00:37,711 --> 00:00:39,092\nSpeaker 1: Oh, that's a model in Suzuki.\n\n3\n00:00:39,312 --> 00:00:41,973\nSpeaker 0: Yeah, yeah, RG Five Hundred is a Suzuki model.\n\n4\n00:00:42,333 --> 00:00:43,014\nSpeaker 2: I did not know that.\n\n5\n00:00:43,074 --> 00:00:52,078\nSpeaker 0: Yeah, there you go, so RG, great. How do I call you, Dwight? Michael, Michael's fine. Michael, okay. Now, how long have you been at Fun?\n\n6\n00:00:52,098 --> 00:00:53,139\nSpeaker 2: I've been here for...\n\n7\n00:00:57,136 --> 00:00:59,197\nSpeaker 1: More than one year now. It's my second year.\n\n8\n00:00:59,837 --> 00:01:08,821\nSpeaker 2: I arrived here last year on November, two thousand twenty one. Right. Because the pandemic, I haven't really seen.\n\n9\n00:01:09,471 --> 00:01:11,933\nSpeaker 0: I've never met you before, so that's quite unusual.\n\n10\n00:01:11,953 --> 00:01:41,357\nSpeaker 2: I usually go to all the student presentations. Yeah, I think I was, as of November, I think I was the only international student who was new, I was the only new international student who was here. a lot of the students are starting to come back, which is great. Yeah, the borders opened up again. Yeah, yeah.\n\n11\n00:01:41,778 --> 00:02:13,001\nSpeaker 0: My son goes to a university in Tokyo and it's an international university called International Christian University. and about forty percent of the students are international students. so in his first year during the pandemic the only students he met were Japanese. he's like i've come to this international university and there's no international students because the borders are closed. yeah and of course all the existing international students want nothing to do with the first years. yeah because he's like new.\n\n12\n00:02:15,034 --> 00:02:24,721\nSpeaker 2: But when it opened for that university, bit by bit, they were letting students in. Now, we said it's back to normal.\n\n13\n00:02:26,402 --> 00:02:37,590\nSpeaker 0: The excelling point of the university is that it's international curriculum, American, basically, curriculum. And it's very dynamic.\n\n14\n00:02:38,130 --> 00:02:39,071\nSpeaker 2: He loves it now.\n\n15\n00:02:39,111 --> 00:02:42,052\nSpeaker 1: He says it's great. Yeah, it's good to hear that.\n\n16\n00:02:42,293 --> 00:02:55,776\nSpeaker 2: I understand how that feels, like being the only international student here. Yeah, the big selling point, and I'm telling you, experience being a farmer, was the fact that it was an international university.\n\n17\n00:02:55,796 --> 00:02:58,977\nSpeaker 0: There's no students there, and you're on Zoom.\n\n18\n00:02:59,398 --> 00:03:03,523\nSpeaker 1: I'm like, What am I paying for? Absolutely not. I'm not a big fan.\n\n19\n00:03:15,502 --> 00:03:28,492\nSpeaker 2: I like the blended idea. I like to teach content online, but interaction and this kind of communication, even face-to-face.\n\n20\n00:03:29,013 --> 00:03:32,215\nSpeaker 0: Zoom is not good enough. Yeah, I'm not a fan of Zoom either.\n\n21\n00:03:32,836 --> 00:03:50,046\nSpeaker 2: Staring at lots of little titles or faces on my computer screen, I thought, no, I'm not doing this. This is rubbish. Yeah, it's not that immersive. And on the other hand, I was paying for my son to go to university to be one of those kids on Zoom.\n\n22\n00:03:50,887 --> 00:03:55,969\nSpeaker 0: So I was like, I don't like it as a teacher. I don't like it as a fee-paying father.\n\n23\n00:03:55,989 --> 00:03:58,530\nSpeaker 2: And my son doesn't like it as a student.\n\n24\n00:03:59,810 --> 00:04:05,833\nSpeaker 0: It's just all bad. Yeah, it was pretty bad. Yeah, it was pretty bad. There we go. OK, there we go.\n\n25\n00:04:06,413 --> 00:04:10,275\nSpeaker 2: OK. Now, thank you for sending this. Thanks for coming. Of course.\n\n26\n00:04:18,762 --> 00:05:00,648\nSpeaker 0: Think of me as, imagine you're at an international conference. Let's say you're on a plane. in England, and you're presenting in England, and most of the people are, say, from Europe, most likely. You know, you probably get some from Asia, some from Americas, some from Africa, possibly. But, you know, English, European conference, you mostly get European-English people, yeah? Yeah. So, when you present there, you'll have a different kind of personality will be observing you and giving you comments, questions, and maybe criticism, which you may not get in, say, Asia.\n\n27\n00:05:01,328 --> 00:05:08,411\nSpeaker 2: I used to work in Malaysia, I used to work in Singapore, I now work in Japan, so I know how things are in Asia.\n\n28\n00:05:08,431 --> 00:05:14,614\nSpeaker 0: Now, I will tell you, from Singapore and Malaysian and Japanese, the Singaporeans are very critical, and I love that.\n\n29\n00:05:16,134 --> 00:05:18,035\nSpeaker 2: They don't like your work, they'll say it.\n\n30\n00:05:19,036 --> 00:05:38,562\nSpeaker 0: Malaysians, kind of a bit more polite, should we say? Japanese, they don't say anything. cautious in what they say, so you don't get much criticism, feedback in Japan compared to what you would get in Singapore, compared to what you would get in somewhere like England.\n\n31\n00:05:40,831 --> 00:05:52,257\nSpeaker 2: What I'm trying to say is that I will give you some critical feedback, but it's not a criticism, it's the kind of feedback that you may be getting if you presented this at a conference in England.\n\n32\n00:05:54,898 --> 00:05:56,359\nSpeaker 0: So that's the way I go through things.\n\n33\n00:05:56,699 --> 00:05:57,340\nSpeaker 2: I think it's good.\n\n34\n00:06:00,121 --> 00:06:03,842\nSpeaker 0: It says, look, these are the challenges that you need to face.\n\n35\n00:06:04,662 --> 00:06:12,103\nSpeaker 2: If you can overcome these, you'll have no problem. But you won't know that until you are confronted with those challenges.\n\n36\n00:06:12,364 --> 00:06:44,556\nSpeaker 0: That is true. OK, so first of all, I will say, I made a comment here. First of all, I think this is a very, very well-written paper, very logical, follows in terms of the way you conducted the process of this evaluation, what the limitations are, are some of the finer details of the project.\n\n37\n00:06:44,696 --> 00:06:50,058\nSpeaker 2: Not your writing. Your writing is actually very good, very logical, very, very good.\n\n38\n00:06:50,538 --> 00:06:57,340\nSpeaker 0: So I want to point out some points to you with some questions that you may be able to answer to make this a better paper.\n\n39\n00:07:01,623 --> 00:07:07,828\nSpeaker 2: I'll give an overall summary there, and I've got a couple of recommendations, and then you can ask me some questions.\n\n40\n00:07:07,848 --> 00:07:12,932\nSpeaker 0: Now, because it's in PDF, what I normally do with a Word document, I usually use track changes.\n\n41\n00:07:14,053 --> 00:07:42,117\nSpeaker 2: But with a PDF, it's a bit problematic to do that, even though I've got Adobe Pro, Acrobat Pro, so I did it by pencil. So I tried to read my writing. a few, starting off with the very first line, okay, I wouldn't put in a word like tedious, because it means then, well if it's tedious, don't do it.\n\n42\n00:07:43,798 --> 00:07:52,113\nSpeaker 0: If you think your job, or if you think a design life cycle is tedious, then maybe you're not the person to do it.\n\n43\n00:07:52,754 --> 00:08:06,009\nSpeaker 2: Because a design life cycle for some people is very positive. It's a challenge and people like that challenge. And then it's not tedious.\n\n44\n00:08:06,850 --> 00:08:15,117\nSpeaker 0: It's actually completely opposite for some people. So you mentioned the word challenging later on. Let's put it straight in the beginning, shall we?\n\n45\n00:08:15,617 --> 00:08:30,049\nSpeaker 2: It's an iterative and challenging process because you've got the word challenge there. Straight away, it's challenging. Challenge could be positive. I think challenges are positive. If you see a barrier, it's an opportunity.\n\n46\n00:08:30,289 --> 00:08:33,051\nSpeaker 0: That wall is an opportunity, not a barrier.\n\n47\n00:08:33,431 --> 00:08:34,712\nSpeaker 2: So it's a challenge.\n\n48\n00:08:35,533 --> 00:09:12,684\nSpeaker 0: Great, okay, then I looked at what are you trying to do? Okay, you found in your summary of the abstract, yes, you've got a summary of all the key points that you found in your research. So a great abstract, I completely understand what this paper's going to tell me. Okay. So they come down, industrial sort, underline several stages, fantastic, fantastic. When I come across my first acronym, you need to write it out. Computer Aided Design, bracket CAD, later on, CAD. So just something there.\n\n49\n00:09:12,984 --> 00:09:15,165\nSpeaker 2: First mention, write it out in full.\n\n50\n00:09:16,206 --> 00:09:47,989\nSpeaker 0: Again, tedious, challenging. Yeah, OK. So in this sentence here, it looks like this. Okay, that phrase there, carry loads and endure drops from specific heights, kind of, it doesn't really flow from what you said before.\n\n51\n00:09:48,469 --> 00:09:52,211\nSpeaker 2: So why not say the product meets technical and safety specifications?\n\n52\n00:09:54,838 --> 00:10:09,650\nSpeaker 0: So carry loads and maybe specific guides are probably technical and safety specifications. So why not change that to that? Because it's kind of not in context with what you're saying before.\n\n53\n00:10:10,190 --> 00:10:12,532\nSpeaker 2: It sounds like a very concrete example.\n\n54\n00:10:12,813 --> 00:10:50,046\nSpeaker 0: Yeah, you're kind of being generalized there and specific there, suddenly. So if you make it generalized, you've probably got that phrase there. So this is why I'm saying, you know, your writing is very, very good. Then you've got this word, out of expertise, knowledge, generalized. Generalized knowledge. Because, you know, if you've got expert knowledge and general knowledge and no knowledge. So this would be generalized knowledge. Because that person's not an expert, they've just got general knowledge.\n\n55\n00:10:51,201 --> 00:11:08,428\nSpeaker 2: Right, but I think what I wanted to say here was it's – yeah, it's – I wouldn't say it's general knowledge, but it's knowledge that is specific to another domain. that's not in their domain. What would the right term for that – what would the right term would be for that?\n\n56\n00:11:09,288 --> 00:11:30,044\nSpeaker 1: Like in this case, for example, I mentioned that, well, I didn't really cite it specifically, maybe in the related work here, but in this study, what I was trying to say was that engineers had limited access to knowledge that was, not knowledge that pertains to manufacturing.\n\n57\n00:11:30,845 --> 00:11:31,085\nSpeaker 2: So...\n\n58\n00:11:34,908 --> 00:11:50,362\nSpeaker 0: Okay, so how about access to knowledge outside their expertise? Right, yeah, yeah. Yeah, yeah, that's outside. Do you want to make a view, right? Oh, right, yeah. You've got a pen? Knowledge outside their expertise.\n\n59\n00:11:50,382 --> 00:12:02,853\nSpeaker 2: Okay, I got it, I see what you've done. Okay, and then I just...\n\n60\n00:12:09,651 --> 00:12:33,316\nSpeaker 0: So you've got your research goals, one and two. Okay, two questions, very, very clear. And I'll come back to this later, because in your conclusion, you only had one. I'll come back to that later. So, let's start this one. Okay, must meet each of their requirements, just change it to specific requirements.\n\n61\n00:12:33,336 --> 00:12:34,256\nSpeaker 2: Okay, that's straightforward.\n\n62\n00:12:34,496 --> 00:13:38,760\nSpeaker 0: Just a little, maybe a typo, you've got a question mark, question mark there, that's probably a development, yeah. Yeah, I've got stakeholder, what have I got? Yeah, okay, this reference here to they're, I wasn't sure what you meant. Because you've got sue and lue, however you say that, they're refers to them. But actually when I read it again, they're refers to stakeholders. So there's a confusion because this is what we call a backward reference in, for what the word is, but there's a single backward reference. So thea is backward reference into the subject, which is these. In actual fact, it's these, which is a different kind of reference, exophoric reference. So you need to write the word in. But that's only because you write it many times, so you know who theas are. So when I read it for the first time, That's why you give your paper to your friend to read.\n\n63\n00:13:39,160 --> 00:13:42,641\nSpeaker 2: Exactly, that's why I consulted. Yeah, that's right.\n\n64\n00:13:42,661 --> 00:14:14,028\nSpeaker 0: So you come to me and go to your friends, yeah? So... Again, you then switch to... Ah, wait a minute. Okay, you've got the word... I've just changed the language a bit to make it a bit better. You've got verifying them, just say subsequent verification. Right, right. Just makes it sound better, okay? You've got stakeholders, then you've got users. So I put a question mark there.\n\n65\n00:14:14,108 --> 00:14:21,415\nSpeaker 2: Do you mean stakeholders? Because suddenly users have appeared. I don't know who these users are. Right. I think when\n\n66\n00:14:21,475 --> 00:14:22,376\nSpeaker 1: I meant users,\n\n67\n00:14:22,436 --> 00:14:25,539\nSpeaker 2: I meant like customers\n\n68\n00:14:25,739 --> 00:14:26,700\nSpeaker 1: who have been invited\n\n69\n00:14:27,120 --> 00:14:27,300\nSpeaker 2: for\n\n70\n00:14:31,600 --> 00:14:32,200\nSpeaker 1: for\n\n71\n00:14:32,540 --> 00:14:39,403\nSpeaker 0: this assessment. But the people that you get to assess design, are the people involved in the design?\n\n72\n00:14:41,103 --> 00:14:49,066\nSpeaker 1: In this study that I cited, no, they invited outside customers, like the survey of customers.\n\n73\n00:14:49,486 --> 00:15:11,833\nSpeaker 0: So when I said customers, I wrote the word users. So these are actually Oh, I see. So the designers there are bringing in outside people who are possible users of the device to give us a... Okay, I get it. I understand now.\n\n74\n00:15:12,373 --> 00:15:12,974\nSpeaker 1: Or maybe I should...\n\n75\n00:15:14,194 --> 00:15:24,677\nSpeaker 0: No, no, no, it's just me. Don't worry. That's fine. I see what you mean. now, because I'm not familiar with these papers, and I didn't check them, so... I understand.\n\n76\n00:15:25,178 --> 00:15:25,898\nSpeaker 2: No, I'm sure it's fine.\n\n77\n00:15:27,664 --> 00:15:40,939\nSpeaker 0: Again, just to rub this a bit better, I've taken that out, put in it, instead of raised, put the word reported, that's all. It's just stylistic more than anything else.\n\n78\n00:15:41,620 --> 00:16:03,083\nSpeaker 2: So instead of raised, You raise a point, you raise a motion, but actually these people are reporting information. You raise a concern, you report information. It's kind of slightly different, yeah. Okay, so it's more on, yeah, this is more appropriate to use. This is more appropriate, you report something.\n\n79\n00:16:03,123 --> 00:16:13,788\nSpeaker 0: You certainly raise something, but then a synonym of raise is pointed out, highlighted, which you don't mean there, you just mean reported.\n\n80\n00:16:14,693 --> 00:16:25,258\nSpeaker 1: So when you say the rays, you don't really use that when you're stating the results of a study that you're citing?\n\n81\n00:16:25,278 --> 00:16:38,305\nSpeaker 0: I don't want to say no, because it's not true. I think if you wanted to emphasize\n\n82\n00:16:38,365 --> 00:16:44,419\nSpeaker 2: something, contrast something with the previous research,\n\n83\n00:16:44,439 --> 00:16:46,820\nSpeaker 0: that would be possible, but probably emphasising\n\n84\n00:16:46,840 --> 00:16:50,162\nSpeaker 2: with your daughter, you know, that if you talk\n\n85\n00:16:50,182 --> 00:16:59,571\nSpeaker 0: about research that such and such raise the concern or raise the point that, you know, and then you're highlighting something\n\n86\n00:16:59,711 --> 00:17:00,311\nSpeaker 2: in addition,\n\n87\n00:17:01,352 --> 00:17:01,772\nSpeaker 1: which is\n\n88\n00:17:01,792 --> 00:17:03,853\nSpeaker 2: a level\n\n89\n00:17:04,093 --> 00:17:13,377\nSpeaker 0: above what you previously reported. Right. It's like, this is a little bit more important than that. Okay, okay. That's, but in this material, you're not, you're giving everything an equal status.\n\n90\n00:17:14,178 --> 00:17:40,934\nSpeaker 2: Ah, okay. So it raises, like, pinpointing on something very specific. Yeah, yeah, highlighted, pinpointed, I like that, yeah. I see. Yeah. But again, it's just, It's just the use of synonyms in a way, but that's better. I understand. Okay. Keeps going, I'll get more critical for later on. Address determined, it's a synonym, I don't know. Right, now here we go.\n\n91\n00:17:40,994 --> 00:17:51,617\nSpeaker 0: So, okay, so at the end of this part, which was two point one, you know, this is kind of like a, but related work leading up to your research question.\n\n92\n00:17:52,417 --> 00:17:52,677\nSpeaker 2: Fine.\n\n93\n00:17:53,917 --> 00:17:57,198\nSpeaker 0: So, this was your first aim, yeah?\n\n94\n00:17:59,102 --> 00:18:02,605\nSpeaker 2: So in this study, we aim to...\n\n95\n00:18:02,685 --> 00:18:09,250\nSpeaker 0: Fine, but when I read it further, you've actually got two aims, two questions.\n\n96\n00:18:09,370 --> 00:18:10,731\nSpeaker 2: Yeah, that's true.\n\n97\n00:18:10,992 --> 00:18:31,621\nSpeaker 0: So let's call this your first one, okay? That's your first aim. So in this study, our first aim is to... Then I read the second part. In this study, our second aim, or the second aim of this study is to... So you're making it very specific now, you've got two aims.\n\n98\n00:18:32,221 --> 00:18:33,181\nSpeaker 2: This one and this one.\n\n99\n00:18:34,141 --> 00:18:38,402\nSpeaker 0: Because I had to go back and thought, that's your aim there, but you've got an aim here, what's happening?\n\n100\n00:18:39,042 --> 00:18:41,702\nSpeaker 2: And then I went back, ah, I see.\n\n101\n00:18:41,722 --> 00:19:16,189\nSpeaker 0: You see what I mean? As a reader, I shouldn't do that. You've got to make it clear, one aim there, one aim there. So when I read the rest of the paper, I'm looking for the answers to these two questions. That's all. And then you've got, You've got goals and aims. Again, asking for, requesting, same thing. I'm not sure. I'm sure I know what to say anymore.\n\n102\n00:19:27,159 --> 00:19:32,287\nSpeaker 2: Is it male and female or men and women?\n\n103\n00:19:32,487 --> 00:19:35,852\nSpeaker 0: Well, I don't know. This is an area I'm a bit, you know, I've been in Japan too long.\n\n104\n00:19:35,912 --> 00:19:39,157\nSpeaker 2: If I went to America, maybe I'm not allowed to say that anymore.\n\n105\n00:19:39,177 --> 00:19:42,863\nSpeaker 0: I don't know anymore. Let's call it male and female, shall we?\n\n106\n00:19:43,328 --> 00:19:45,149\nSpeaker 2: Yeah, I think that would be better. Yeah.\n\n107\n00:19:45,769 --> 00:19:47,509\nSpeaker 0: Where is this going to be presented?\n\n108\n00:19:47,529 --> 00:19:50,330\nSpeaker 2: It's going to be presented in CHI.\n\n109\n00:19:51,110 --> 00:19:53,571\nSpeaker 1: CHI, it's a Human-Computer Interaction Conference.\n\n110\n00:19:53,651 --> 00:19:54,171\nSpeaker 2: Which city?\n\n111\n00:19:54,511 --> 00:19:56,392\nSpeaker 1: They'll be held in Hamburg.\n\n112\n00:19:57,112 --> 00:20:01,833\nSpeaker 0: Oh, Germany. No, I'm saying this is going to be presented in Los Angeles.\n\n113\n00:20:01,873 --> 00:20:06,695\nSpeaker 2: You might have a bit of an issue with what's going on at the moment. OK.\n\n114\n00:20:09,025 --> 00:20:13,890\nSpeaker 0: then you're, you know, because you're researching now, you're thinking, OK, you've got to be specific.\n\n115\n00:20:14,310 --> 00:20:29,004\nSpeaker 2: So most of the participants were from the Philippines. Actually, no. Tell me how many were from the Philippines. Yeah. OK. You've got to be dead right. All right. Six were. One wasn't. So one's Japanese, rather than most. Yeah.\n\n116\n00:20:29,804 --> 00:20:55,940\nSpeaker 0: Right. Now, this is where it gets a little bit. Yeah, you put in information there that either A, you need to explain to the reader, or B, you don't know. So this information there, I'm not sure if the reader's supposed to know, or maybe you don't know what it is. I don't know from this.\n\n117\n00:20:56,241 --> 00:21:04,025\nSpeaker 2: So you say, using grounded theory, fine. You're assuming that everybody knows grounded theory.\n\n118\n00:21:05,791 --> 00:21:31,036\nSpeaker 0: So it's quite important to define. grounded theory is. It does two things. One, it tells the reader what it is, because the reader might not know. And two, it demonstrates that you know what it is as the writer. So just one sentence, grounded theory is, and the benefits of grounded theory are. So in other words, why grounded theory?\n\n119\n00:21:31,396 --> 00:21:33,477\nSpeaker 2: Why not some other approach?\n\n120\n00:21:34,477 --> 00:21:48,684\nSpeaker 0: Why not do a survey? You know, qualitative data in that respect. Get some quantitative feedback. So you're using grounded theory, which is fine. Tell us what it is and why you used it.\n\n121\n00:21:49,584 --> 00:21:51,485\nSpeaker 2: Just a couple of sentences.\n\n122\n00:21:52,045 --> 00:22:34,741\nSpeaker 0: Same with, right, now, you quoted the transcripts. There's a red flag, code. What code did you use? So again, this is where you've got to explain what code you used and how the process of that code. Because in research, if you're going to code something, you must have a system of coding. You must have criteria for coding text, for coding what people write, basically.\n\n123\n00:22:39,825 --> 00:22:43,066\nSpeaker 1: Okay, so here, do I have to specify the criteria?\n\n124\n00:22:43,346 --> 00:23:01,491\nSpeaker 2: Yeah, I've got an example here for you. Yes, you could specify the criteria. Secondly, who checked it? Who did the coding and who checked your coding? How many people were involved? What was the inter-reliability rate? So\n\n125\n00:23:01,871 --> 00:23:03,532\nSpeaker 0: when you look at coding transcripts,\n\n126\n00:23:04,112 --> 00:23:05,412\nSpeaker 2: and you look at grounded\n\n127\n00:23:05,452 --> 00:23:16,515\nSpeaker 0: theory and qualitative research, and you look under the section coding transcripts, you'll find, this is actually quite common, that needs to be done, that you've got to decide\n\n128\n00:23:16,535 --> 00:23:19,256\nSpeaker 2: what the coding is, who checked\n\n129\n00:23:19,296 --> 00:23:30,459\nSpeaker 0: that coding, you then coded all the transcripts, you need a second person to code the transcripts, and then the two of you have got to get together and compare your results.\n\n130\n00:23:31,547 --> 00:23:44,975\nSpeaker 2: And that's called an inter-reliability rate. Oh, so that's how it works. That's how it works. And the more people you get coding, the better. So for example, when I was in Singapore, we'd have educational researchers with PhD students.\n\n131\n00:23:45,776 --> 00:23:48,858\nSpeaker 0: We'd be videotaping teachers teaching.\n\n132\n00:23:49,878 --> 00:23:54,061\nSpeaker 2: They'd come back, we'd have them transcribe all the videos.\n\n133\n00:23:54,541 --> 00:24:28,351\nSpeaker 0: And then we'd have thousands and thousands of lines of text, transcript, and these three or four or five or six researchers would then discuss a coding scheme. We've come up with a coding scheme, we've decided the coding scheme, fine. Now they go away and they assign parts of the transcript to each code. Right then, they come together and then they compare all their results. And if all\n\n134\n00:24:28,371 --> 00:24:29,671\nSpeaker 2: their results are too different,\n\n135\n00:24:30,171 --> 00:24:30,491\nSpeaker 0: they've got to\n\n136\n00:24:30,531 --> 00:24:31,492\nSpeaker 2: go back and start again\n\n137\n00:24:32,072 --> 00:24:33,913\nSpeaker 0: and do another, either do the coding,\n\n138\n00:24:34,413 --> 00:24:34,553\nSpeaker 2: the\n\n139\n00:24:34,953 --> 00:24:35,654\nSpeaker 0: criteria\n\n140\n00:24:36,094 --> 00:24:36,554\nSpeaker 2: selection\n\n141\n00:24:36,594 --> 00:25:00,968\nSpeaker 0: again, maybe narrow it down, widen it, probably narrow it down, then go back and then decide what part of the transcript goes with this code. And then they go back and do it again. And then until they get an inter-reliability rate of ninety percent, And then you say, okay, now we can analyze this data. Oh, so that's how coding works.\n\n142\n00:25:00,988 --> 00:25:03,409\nSpeaker 2: That's how coding works, yeah.\n\n143\n00:25:03,509 --> 00:26:58,041\nSpeaker 0: So, we've done it, myself and two colleagues here have done it, we did it two years ago during the pandemic, and we called it thematic analysis, which is explain that process. so you can use our paper as an example of the process of coding and how we came up, because we did something similar. So you need to explain that before you move on to the results, because without that foundation of coding then everything else is unreliable. Even though when I read your scripts, it made sense and I can understand why you did it, but at the same time, when I read your conclusion and transcripts that support your conclusion, somebody in the audience may put their hand up and say that's bias. You may be biased. In other words, you are cherry picking. You are picking out information to suit your outcome. Whereas what you should be doing is looking at the information and from the information determine that outcome. But what you could be accused of here is that the outcome has already been decided by you subconsciously, but you've kind of looked for the transcripts to match that. I'm not saying you did that, but that's what you could be accused of. It's not a big accusation, of course, but it's just that somebody may take issue with that. So you don't have to change anything there. I think what you need to do is just justify how you've done this thematic analysis. Even if you keep everything else the same, that's fine. But when you do it, you may change.\n\n144\n00:26:58,081 --> 00:27:02,125\nSpeaker 2: I don't think you'll change, because I think your discussion is actually very focused and very good.\n\n145\n00:27:02,145 --> 00:27:22,664\nSpeaker 0: But I think without this there, it seems very, well, you've already determined what you wanted to do, what you've decided at the end, based on whether the students get, whether these six Filipino designers, one Japanese designer, give that information anyway.\n\n146\n00:27:24,406 --> 00:27:40,651\nSpeaker 2: See what I mean? Because, hey, don't keep going. So think about that. So I'll come back, I'll show you my, okay? So there's my questions there. That, I think, is personally a kind of a weak part of this project, and that's your justification of the method.\n\n147\n00:27:41,771 --> 00:27:50,654\nSpeaker 0: Yeah, okay, so that's it. So as you can see now, from there on, look, the question, are there, this is, yeah.\n\n148\n00:27:51,394 --> 00:27:53,775\nSpeaker 2: Yeah, and then, okay, your results.\n\n149\n00:27:54,744 --> 00:28:08,795\nSpeaker 0: you know, your discussion, it's all very good, sorry, the overview of the results is all very good, and then when it came to the discussion I think this is what you've got to decide yourself.\n\n150\n00:28:09,015 --> 00:28:28,774\nSpeaker 2: In your discussion you said the aim of the study. But in the previous section there were two aims. So I actually personally, I like the fact that you've got it written down as one aim. You've connected the two into one. I like that. And I think it makes it more focused.\n\n151\n00:28:28,814 --> 00:28:41,413\nSpeaker 0: So what you could do at the end of What you could do, you've got aim one, aim two there. What you could do is possibly add another sentence saying the aim of this study is to...\n\n152\n00:28:43,294 --> 00:28:47,815\nSpeaker 2: Just copy that. Just copy that there. Right.\n\n153\n00:28:47,975 --> 00:28:52,216\nSpeaker 0: Yeah, so copy that, put it there, and then this matches this.\n\n154\n00:28:54,068 --> 00:29:04,296\nSpeaker 2: So your literature review output with the aim matches the introduction of the discussion aim. They are exactly the same.\n\n155\n00:29:04,817 --> 00:29:08,320\nSpeaker 0: At the moment you've got one, two, and then you've got one, so they're not the same.\n\n156\n00:29:10,501 --> 00:29:13,822\nSpeaker 1: Okay, so what you're saying is, instead of having two here...\n\n157\n00:29:13,842 --> 00:29:24,065\nSpeaker 0: So what you do, you put one there, and you put another new paragraph, which is one sentence. Overall, the aim of the study is two.\n\n158\n00:29:25,665 --> 00:29:30,547\nSpeaker 2: In summary, or something like that, the aim of the study is two, and then write it down as one sentence.\n\n159\n00:29:32,067 --> 00:30:12,983\nSpeaker 0: Or you have to change that to two. It's up to you. So you either want one aim like this, which connect the two together, or you have two separate aims. that you've done there, but that has to be really, really good. Because this has to match this. Okay? Because then the rest of it then, you know, you discuss. Yeah, and then you... So discuss, okay so you discuss. and then like I say this section is very good, I thought the first section was a little short, the successful based on target demographics. Yeah, it's very good.\n\n160\n00:30:13,003 --> 00:30:19,544\nSpeaker 2: I just wonder if you could explain this section a little bit more, maybe with an example.\n\n161\n00:30:19,564 --> 00:30:23,145\nSpeaker 0: I think you need like four to five more lines there.\n\n162\n00:30:23,845 --> 00:30:46,158\nSpeaker 2: I don't know what word count you're limited to. So if you could maybe explain that a bit more with examples. That would help me because I'm not familiar with the research, so I kind of needed an example there. Which in this one, I was very clear, you're very clear there.\n\n163\n00:30:48,799 --> 00:30:58,843\nSpeaker 0: And at the end of reading this, I thought, well, you've come to the end now, come to your conclusion, you've come to the end of your discussion, so what are you actually recommending?\n\n164\n00:31:08,907 --> 00:31:17,854\nSpeaker 2: So, in summary, or incrementally, before you write the conclusion, what are you actually recommending at the end of your discussion?\n\n165\n00:31:20,356 --> 00:31:25,661\nSpeaker 1: Okay, so, at the end of the discussion, I have to put a summary of what other things I recommend?\n\n166\n00:31:25,921 --> 00:31:39,439\nSpeaker 0: Yeah. To round it up, because you've got Section V.I, Section V.II, Okay, you know, what's next?\n\n167\n00:31:39,639 --> 00:31:49,808\nSpeaker 2: And then you put like a space, and then you can, you know, on the five point, five point, no, just put a space and one or two lines about what you're recommending.\n\n168\n00:31:50,068 --> 00:32:09,868\nSpeaker 0: Because you do recommend from doing all this, you know, the development of what, is it a database or something? Because I had a question at the end, you see. So this is all good, this is all good, really, really good, because at the end, You said, we then plan to develop a prototype focusing on changing material.\n\n169\n00:32:12,862 --> 00:32:18,124\nSpeaker 1: What's that? Yeah, I'm sorry about that. When I submitted the draft, I forgot to finish the sentence.\n\n170\n00:32:19,285 --> 00:32:30,010\nSpeaker 2: Yeah, it says here that this was a pilot study that I did before developing a system that aims to address the challenges that I raised up here.\n\n171\n00:32:30,210 --> 00:32:45,476\nSpeaker 1: Yeah, this was supposed to be a plan to develop a prototype focused specifically on changing materials of a for product design, but I'm not sure if that sentence is needed.\n\n172\n00:32:46,257 --> 00:33:06,128\nSpeaker 0: Probably not, because it's kind of really out of sync with everything that's gone before, because you say you're going to develop there, and I was thinking, well, wait a minute, you're recommending something there which I'm not quite sure, but then you're designing a prototype. So see where that confusion is.\n\n173\n00:33:06,549 --> 00:33:09,149\nSpeaker 2: Maybe the recommendation of the prototype should go there, I don't know.\n\n174\n00:33:09,870 --> 00:33:19,493\nSpeaker 0: So that was unclear to me. So think about that, okay? And then finally, that's an odd one, number twenty.\n\n175\n00:33:19,673 --> 00:33:20,153\nSpeaker 2: What's that?\n\n176\n00:33:20,213 --> 00:33:24,774\nSpeaker 1: I've never seen anything like that before. This was a huge collaborative project.\n\n177\n00:33:25,034 --> 00:33:25,835\nSpeaker 2: That's mad.\n\n178\n00:33:27,190 --> 00:33:29,933\nSpeaker 0: yeah that's mad because you've got it's there.\n\n179\n00:33:29,953 --> 00:33:33,736\nSpeaker 2: there that's the title and it stops there.\n\n180\n00:33:34,037 --> 00:33:34,957\nSpeaker 0: no that's number nineteen.\n\n181\n00:33:34,977 --> 00:33:37,660\nSpeaker 2: sorry that's just really odd.\n\n182\n00:33:38,200 --> 00:34:12,628\nSpeaker 0: yeah i don't know what to do. i've never seen anything like that. um i would probably I don't know. You have to check the journal and see what happens. See if you can find an example in the conference proceedings or a similar journal. that has something like this.\n\n183\n00:34:14,090 --> 00:34:21,856\nSpeaker 2: My intuition is it might be just the first name, et al. Because I think that's kind of ridiculous.\n\n184\n00:34:21,976 --> 00:34:38,755\nSpeaker 0: But I don't know what the general convention is on that one. Because I'm just thinking, if it's a report, and you have lots and lots of people in a report, You wouldn't put all their names on the front page, would you?\n\n185\n00:34:39,136 --> 00:34:54,648\nSpeaker 2: You'd put one person or two people. You can't imagine all these people writing this project. I don't think\n\n186\n00:34:56,728 --> 00:34:57,670\nSpeaker 1: this meant these were\n\n187\n00:34:57,790 --> 00:35:10,495\nSpeaker 0: authors who wrote the paper. So I hope all that kind of feedback is useful for you. What I've done is I've summarized what I've just said in a note there, okay? And I'll send you this in an email later.\n\n188\n00:35:26,323 --> 00:35:30,129\nSpeaker 2: okay so it's very well written and everything i've just said i've written down there.\n\n189\n00:35:30,830 --> 00:36:00,040\nSpeaker 0: and regarding thematic analysis this is a paper i wrote with two colleagues up here on uh during the pandemic and we used We use thematic analysis, and this is a justification. This has become our analytical framework, which is thematic analysis. And you can see the steps that we went through.\n\n190\n00:36:00,060 --> 00:36:20,941\nSpeaker 2: When we got all the students' feedback and transcripts, and we put them all together into a huge document, we then went through these. three of us went through these steps in order to determine what the themes were that came out of this research.\n\n191\n00:36:21,981 --> 00:36:33,244\nSpeaker 0: It's slightly different from yours, but at the same time I'm showing you that there's a method to, you know, doing this kind of grounded theory.\n\n192\n00:36:34,364 --> 00:36:35,084\nSpeaker 2: And that's what we did.\n\n193\n00:36:35,144 --> 00:37:00,457\nSpeaker 0: And then you can see, you can see how You can see the themes that came out together, you can see the percentage of examples. So we got a theme, we defined the theme, and then we looked for examples that represented the definitions of these themes. So we worked from basically nothing.\n\n194\n00:37:02,426 --> 00:37:13,717\nSpeaker 2: But we used the data to determine what the themes were. We didn't go in with themes. We went through our data, we found the themes. By going through this process, we determined what the themes were.\n\n195\n00:37:14,538 --> 00:37:20,042\nSpeaker 1: Then we went back to the data and looked for examples. Oh, okay. So it's a back and forth process.\n\n196\n00:37:20,222 --> 00:37:24,585\nSpeaker 2: Right. Yeah, that constant back and forth, which is what this is exploring.\n\n197\n00:37:25,946 --> 00:37:27,767\nSpeaker 1: So you've built up the themes from the ground up.\n\n198\n00:37:28,067 --> 00:37:28,887\nSpeaker 2: That's what we did. Yeah.\n\n199\n00:37:28,907 --> 00:37:42,896\nSpeaker 0: Grounded themes. You build themes from the ground up. So what we did is instead of deciding what the, we didn't know what the themes were because all we got was feedback from the students during the pandemic of using an online system. Right. With lots of\n\n200\n00:37:43,604 --> 00:37:44,144\nSpeaker 2: directed\n\n201\n00:37:44,164 --> 00:37:49,126\nSpeaker 0: and open-ended questions and then particularly from the open-ended\n\n202\n00:37:49,166 --> 00:38:00,329\nSpeaker 2: questions we encouraged them to type their answers and we got long answers and then from those very long answers we then put them all together\n\n203\n00:38:00,349 --> 00:38:10,324\nSpeaker 0: in one huge text file and then we went through it and we tried to pull out different common themes, like motivation, for example,\n\n204\n00:38:10,364 --> 00:38:10,865\nSpeaker 2: maybe\n\n205\n00:38:10,945 --> 00:38:14,032\nSpeaker 0: one motivation was grading, and students were motivated\n\n206\n00:38:14,112 --> 00:38:18,201\nSpeaker 2: by the grade that they wanted. Yeah, assessments.\n\n207\n00:38:18,281 --> 00:38:23,025\nSpeaker 0: There was a lot of mention about students were concerned about their grade.\n\n208\n00:38:23,925 --> 00:38:46,860\nSpeaker 2: So that came up quite a lot. So, you know, excluding this reference to a formalized achievement metrics such as course grade or GPA score. That was mentioned a lot because they were very worried about being online and how it would affect their GPA. So that was a common theme right across this group. That was a theme, and we looked for examples that fit with that theme.\n\n209\n00:38:47,921 --> 00:38:50,902\nSpeaker 0: In the end, we came up with five themes, or six themes.\n\n210\n00:38:52,042 --> 00:38:55,564\nSpeaker 2: Not five, that's four.\n\n211\n00:38:55,604 --> 00:39:13,823\nSpeaker 0: Okay, we cut it down to four. But I think if you want to have a look at the way we developed it, the analytical framework, that might help you think about how you're going to explain your your process. It might help you, I think it might.\n\n212\n00:39:15,704 --> 00:39:52,240\nSpeaker 2: About this, you mentioned you involved six PhD students? This was just the three of us. When I was in Singapore, before I came to Japan, we did research on, I was a teacher trainer, so what can I do? We'd get our students, which are BA pre-service teachers, and in the practicum, they would go out to schools and teach, practice. So, the schools we would go to is that we'd take video cameras and we could videotape the teachers teaching the kids, and the kids, you know, everything.\n\n213\n00:39:52,300 --> 00:40:34,899\nSpeaker 0: So everything was captured, professional mics hanging from the ceiling, good cameras, and then good audio pickups. Then they come back. and then those PhD students, they were doing a PhD in education. And they all had different theses to work on. But generally, their job, their paid job, was to transcribe and then basically Either A, they come up with their own coding scheme or B, they would use a Ministry of Education standardised coding scheme.\n\n214\n00:40:36,947 --> 00:41:09,825\nSpeaker 2: we prefer that they come up with their own coding scheme because they then did a lot more thematic analysis. If they use the standardised Ministry of Education coding scheme, then there's not much thinking going on, they're just looking for examples. Whereas to deep dive into the data, it's better for the student to come up with their own coding themes from the data. So when they're initially coding the data, it's up to them on how they interpret it at first?\n\n215\n00:41:10,366 --> 00:41:23,259\nSpeaker 0: It's up to them as they're going through it. See, when you're watching teachers teach, you may see things like, OK, maybe there's, say, three parts to a lesson.\n\n216\n00:41:23,319 --> 00:41:26,643\nSpeaker 2: There'll be a performance practice presentation.\n\n217\n00:41:26,663 --> 00:41:27,684\nSpeaker 0: There'll be a presentation.\n\n218\n00:41:30,917 --> 00:41:43,522\nSpeaker 2: the kids are practising something, then you've got performance, where the students then are performing to the teacher or to other students to display what they've learnt.\n\n219\n00:41:43,822 --> 00:41:46,683\nSpeaker 0: So you've got presentation, practice, performance.\n\n220\n00:41:46,763 --> 00:42:01,604\nSpeaker 2: And within those three parts of a lesson, things will be happening where the teacher may be presenting you to the PowerPoint, giving information, The teacher may ask a student a question.\n\n221\n00:42:01,624 --> 00:42:05,426\nSpeaker 0: The teacher may say, how many?\n\n222\n00:42:05,666 --> 00:42:07,367\nSpeaker 2: So we get group interaction.\n\n223\n00:42:08,088 --> 00:42:11,369\nSpeaker 0: One to one, what do you say? Or Jimmy, what do you say?\n\n224\n00:42:11,549 --> 00:42:12,690\nSpeaker 2: Jane, what do you think?\n\n225\n00:42:13,010 --> 00:42:42,394\nSpeaker 0: So it's one to one. What question? Is that right? What's the answer? Give me the answer. So you've got different, asks a question, demands an answer, makes a statement, what's the answer, give me an answer. It's very different. That's the way of teaching. Yeah, so you've got all these different ways of interacting with the kids as a presenter. Then you've got practice, what the students when they're practicing.\n\n226\n00:42:43,274 --> 00:42:58,300\nSpeaker 2: In the closed practice, maybe it's a worksheet that the kids are working on together or on their own. What's going on there? So lots and lots of things happening that the teachers can write little codes for in a lesson. And that's it.\n\n227\n00:42:58,561 --> 00:43:13,161\nSpeaker 0: And then they've determined from watching the video you know, the different codes and different actions. Then they get the transcript and they see how the transcript would fit these, and if they've got like twenty or thirty, can they narrow it down to say five or six?\n\n228\n00:43:15,383 --> 00:43:31,841\nSpeaker 2: So that's what coding does, we narrowed it down to four. But you can start off with a lot. So you could start off by looking at your transcripts and coming up with, let's say you've got forty answers, you could potentially have forty different codes.\n\n229\n00:43:32,422 --> 00:43:42,508\nSpeaker 0: But then you think away a bit. This answer, this answer, this answer is quite similar to a particular theme about, and then you could decide what that theme is.\n\n230\n00:43:42,528 --> 00:43:46,911\nSpeaker 2: And you say, OK, so that's one of my codes, those sorts, we could go there.\n\n231\n00:43:46,991 --> 00:43:48,532\nSpeaker 0: But what's he saying? What's he saying?\n\n232\n00:43:49,432 --> 00:43:51,774\nSpeaker 2: That's quite similar. What's that?\n\n233\n00:43:55,758 --> 00:44:00,442\nSpeaker 1: Is there a set number of times you have to define your themes?\n\n234\n00:44:01,983 --> 00:44:08,408\nSpeaker 0: I remember when I did this with... First of all, it was myself and Michiko.\n\n235\n00:44:08,448 --> 00:44:09,830\nSpeaker 2: We did it together. We did it.\n\n236\n00:44:11,571 --> 00:44:12,572\nSpeaker 0: We went through it three times.\n\n237\n00:44:15,751 --> 00:44:26,537\nSpeaker 2: And we were quite happy. Then we brought in our third researcher, which was the first author, Damien. He came in, then. Then he coded it his way and compared his...\n\n238\n00:44:26,817 --> 00:44:28,378\nSpeaker 0: So me and Richard compared with ourselves.\n\n239\n00:44:28,418 --> 00:44:35,141\nSpeaker 2: We did that three times, because we had too many. We wanted to narrow it down. We got it down to five.\n\n240\n00:44:35,702 --> 00:45:02,943\nSpeaker 0: Damien came in. He went through it. He came up with four themes. When we all three of us came together then, so that would be the one, two, seven, two, let's say we went through it. Let's say we went through the old text three or four times, we ended up with four themes. There's no hard and fast rule. and you've got to do it with at least one other person.\n\n241\n00:45:03,823 --> 00:45:14,825\nSpeaker 2: Oh, so a minimum of two people? You've got to have a minimum of two people, yeah, because you need that inter-reliability rate, because you can't depend on yourself, because then you're introducing bias.\n\n242\n00:45:15,165 --> 00:45:22,946\nSpeaker 1: Yeah, that's true. Every time I go back to the transcripts, I always come up with different codes and different themes each time.\n\n243\n00:45:23,826 --> 00:45:25,427\nSpeaker 0: But when you do it many times, you'll end up...\n\n244\n00:45:29,512 --> 00:45:30,832\nSpeaker 2: confirmatory bias.\n\n245\n00:45:30,933 --> 00:45:42,021\nSpeaker 0: In other words, you might be going back to something, and your bias might be confirming your original answer. But if you get somebody else looking at it, they say, what are you talking about?\n\n246\n00:45:42,041 --> 00:45:43,042\nSpeaker 2: That's not it. What's this?\n\n247\n00:45:44,162 --> 00:45:58,281\nSpeaker 0: And then you look at it three times, you then have this confirmatory bias, that you're confirming what you already think, you need to bring in a second person to overcome that.\n\n248\n00:46:00,542 --> 00:46:20,430\nSpeaker 2: So you need somebody else to, ideally, I don't know if you have time, but ideally you need another person to go through the text, to go through the process that you're going through. and then you come together and match them together, which is why, I don't know if you're doing this on your own, which is why it's really important to work together.\n\n249\n00:46:22,172 --> 00:46:45,660\nSpeaker 0: Ideally would it be like another PhD student? It'd be somebody working in the same area as you. You need somebody who's familiar with industrial design and design. And certainly another PhD student, absolutely. You need somebody of your level.\n\n250\n00:46:48,621 --> 00:46:51,882\nSpeaker 2: Or maybe somebody just finishing their Masters.\n\n251\n00:46:51,922 --> 00:46:57,663\nSpeaker 1: Would it be strange if we ask another faculty member?\n\n252\n00:46:57,703 --> 00:47:06,470\nSpeaker 2: Because I don't know any PhD students right now who are experts in this field. no but i wouldn't. i wouldn't bring\n\n253\n00:47:06,530 --> 00:47:08,594\nSpeaker 0: a faculty member into it because then\n\n254\n00:47:08,614 --> 00:47:09,155\nSpeaker 2: you've got the\n\n255\n00:47:11,330 --> 00:47:16,393\nSpeaker 1: You've got the hierarchical structure then, because then you can't disagree. Yeah, that's true.\n\n256\n00:47:17,934 --> 00:47:32,162\nSpeaker 2: You then have authority to bias. The authority will trump what you think. You can't argue about this. That is true. You need to find a friend.\n\n257\n00:47:32,182 --> 00:47:58,468\nSpeaker 0: A friend who's working in in design, user interface design, designer products, industrial design, product design. Somebody who's preferably an academic rather than a general designer from outside the industry, because they don't have the same thinking process. As an academic, you might be a designer, but you've got your academic head on for this.\n\n258\n00:47:59,188 --> 00:48:15,988\nSpeaker 2: And that's how you've got to approach it. So you've got preferably a lot of fellow If you've got time to do it.\n\n259\n00:48:16,148 --> 00:48:23,610\nSpeaker 0: I'm not saying it's a bad paper. I think it's a great paper. But I think if you've got time to enhance it, you could make it into a much better paper.\n\n260\n00:48:24,050 --> 00:48:26,910\nSpeaker 2: Thank you. Thank you for your comments. They're actually really awesome.\n\n261\n00:48:27,310 --> 00:48:38,622\nSpeaker 0: Two things I want to bring up. I've got to go. We've got ten minutes. You didn't reference, I'm not surprised anymore, but you know about this book?\n\n262\n00:48:39,542 --> 00:48:55,132\nSpeaker 2: Don Norman? I think I did. You did, yeah, because when you talk about the design process, there was no mention of the double diamond. I'm a big fan of the double diamond design process. Yeah.\n\n263\n00:48:55,552 --> 00:48:56,373\nSpeaker 1: The divergence.\n\n264\n00:48:56,493 --> 00:49:02,616\nSpeaker 2: Yeah, divergence converges, yeah. I didn't check your references but I'll be familiar with that.\n\n265\n00:49:03,056 --> 00:50:14,728\nSpeaker 0: The other one you said something about, you said something. either it's problematic or it's never been done before, you know when you're interviewing people about their design and interactions, that was kind of a limitation, people's design problems and challenges. and I'm surprised because If you were my student, you're not, but if you were my student, okay, I'd give you this book, and I'd say, take a look at all these UX, computer, software, and industrial product designers. These are interviews with lots and lots of people, okay, very short about their projects, and then here they talk about the challenges. And if you were my student, as part of your background, I'd get you to go through this, and for each one, I'd get you to tell me... Larry Tesla, Doug Engelbart, he invented the mouse.\n\n266\n00:50:15,209 --> 00:50:18,151\nSpeaker 2: Yeah. And I think also the Ethernet board.\n\n267\n00:50:18,732 --> 00:50:20,813\nSpeaker 0: McCain, oh yeah, the mouse.\n\n268\n00:50:20,833 --> 00:50:22,395\nSpeaker 2: Okay, what were his challenges?\n\n269\n00:50:24,316 --> 00:50:34,805\nSpeaker 0: Next slide. Bill Atkinson, he invented the Macintosh computer. What were his challenges? These are the famous people.\n\n270\n00:50:34,845 --> 00:50:37,207\nSpeaker 2: The Palm, the Palm pilot there, the Palm PDA.\n\n271\n00:50:38,908 --> 00:50:39,788\nSpeaker 0: What were their challenges?\n\n272\n00:50:39,968 --> 00:50:47,251\nSpeaker 2: So I get them to go through all these people, all these chapters, and just write down what challenges they had.\n\n273\n00:50:47,271 --> 00:51:31,873\nSpeaker 0: And I think that might help you provide a wider context to the challenges beyond the six, seven people that you interviewed. Because my guess is, my intuition, is that the challenges that your participants commented upon were probably commented upon in the seventies by these people who invented the mouse and the desktop and the Mac in the seventies, eighties and nineties. Because at the end of the day, the product design today The problems are probably no different to the problems that were designed thirty years ago. So, I'm not saying do it, I'm saying if you want\n\n274\n00:51:31,913 --> 00:51:34,393\nSpeaker 2: to, not for this, but if you want to, you know,\n\n275\n00:51:34,413 --> 00:51:39,454\nSpeaker 0: you're doing your doctorate, I think as part of your doctorate, to step away\n\n276\n00:51:39,554 --> 00:51:41,595\nSpeaker 2: and to look further afield,\n\n277\n00:51:42,555 --> 00:51:51,865\nSpeaker 0: I would suggest there needs to be a section in your paper, in your project, that introduces problems that have been\n\n278\n00:51:51,925 --> 00:52:04,091\nSpeaker 2: recognized by designers from overseas and what they are. Would it help if I also cite that textbook in this?\n\n279\n00:52:04,891 --> 00:52:58,775\nSpeaker 0: Well, I think what you'd have to do, I would say, Not for what you've done there, no, because I think you're being, there you're very specific about what you're doing. I'd say this is like a pilot study. I think this is an excellent pilot study, but for, it's a pilot study, but for your real research project, you need to widen the scope of your awareness of the literature and the problems beyond the seven students, the seven participants. I would suggest you need to go through something like this, you know you could search the internet but look it's all in one book, it's all there. So this is not for this, this is for your, like I said if I were your supervisor I would ask you to do that for your PhD writing.\n\n280\n00:52:59,096 --> 00:53:02,419\nSpeaker 2: There would have to be a section that would essentially be this.\n\n281\n00:53:03,649 --> 00:53:05,891\nSpeaker 1: Yeah, to get the bigger picture.\n\n282\n00:53:06,252 --> 00:53:33,314\nSpeaker 0: To get the bigger picture, yeah. Because when you get the bigger picture, this may put this into context. Or it may say that there are similarities, or they may say there are differences. And if there are differences, I think there's only two Japanese people in here. All these are mostly American, yeah? There's one guy, Japanese, Hiroshi Ishii, Maeda.\n\n283\n00:53:33,714 --> 00:53:41,136\nSpeaker 2: No, Maeda's not Japanese. Maeda's Japanese, but he's American Japanese. There's a guy who worked on the Apple company, Sakai.\n\n284\n00:53:41,436 --> 00:53:44,477\nSpeaker 0: Yeah, there's a few Japanese in it. Takeshi Natsuno.\n\n285\n00:53:44,497 --> 00:53:46,318\nSpeaker 2: There's quite a few Japanese in it. Oh, I didn't realize.\n\n286\n00:53:46,758 --> 00:54:43,307\nSpeaker 0: But I know on the Apple project in the '' the nineties, there was a couple of Japanese who bought it. What are the problems there? Could the problem be based on Filipino and one Japanese person's experience? Are these problems unique to the Filipinos? That's what I might say. You might say, OK, you've got more on Filipinos, so therefore it's not an international problem. It's a problem with designers in the Philippines, which is not true, I know. But the fact that you've only interviewed six Filipinos and one Japanese makes it kind of like, well, it's not a worldwide problem, is it? Doesn't sound like it. It sounds like it's just a Filipino-Japanese problem. Which is the criticism of all Western research, because the Western research comes out of America, therefore it's an American problem.\n\n287\n00:54:43,347 --> 00:54:44,629\nSpeaker 2: What's it going to do with us in Asia?\n\n288\n00:54:46,692 --> 00:55:03,978\nSpeaker 0: So if you want to generalise it more, then take something like this, which is multi-national, and come up with problems which then say, well actually the problems that these six Filipinos and one Japanese have are actually quite similar to the problems that all these multi-nationals have as well.\n\n289\n00:55:04,738 --> 00:55:34,563\nSpeaker 2: So their problems are not unique to the Philippines and Japan. I think what you're trying to say is that this could be a way to contribute to the challenges in a way that we're trying to address problems that are in Asia, outside the Western area? What you're doing is you're contextualizing.\n\n290\n00:55:35,044 --> 00:56:10,803\nSpeaker 0: You've got the problems which you've identified, which are applicable not only to designers in Asia and Japan, but applicable to designers worldwide, including Singapore, Malaysia, which are also part of Asia, but also America, Europe, Australia, and Africa. For example, which is why I think if you put it then in a broader context, this would provide that broader context. By connecting it to that. If there is a connection, yes, by connecting that, because there may not be a connection. After doing this, you might find that these problems are unique to Filipinos only.\n\n291\n00:56:11,184 --> 00:56:13,465\nSpeaker 2: Yes, that's true. At the moment, they are.\n\n292\n00:56:14,786 --> 00:56:27,753\nSpeaker 0: They are unique to those seven people, because you've only transcribed interviews from seven people. So they're not unique to me from England because I wasn't interviewed.\n\n293\n00:56:27,873 --> 00:56:57,455\nSpeaker 2: So how are you going to put that now into a more generalized context? What we have to do is either interview people from around the world, which is possible using the internet and creating Google Forms and contacting designers overseas and asking them to fill out your form. Yeah, that's possible. Get their nationality, get their gender, I guess. And, or, you know, take it from information that's readily available.\n\n294\n00:57:01,778 --> 00:57:09,894\nSpeaker 0: This book is in the library, I believe. This is mine, but this book is in the Farm Library. Do you have a phone?\n\n295\n00:57:09,914 --> 00:57:15,037\nSpeaker 2: You can take a picture of me if you want. Actually, I think I have a copy of that.\n\n296\n00:57:15,097 --> 00:57:21,901\nSpeaker 0: Yeah, it's quite famous, you know. These two are my two design bibles, you know.\n\n297\n00:57:21,941 --> 00:57:25,082\nSpeaker 2: Yeah. All right, got it. OK.\n\n298\n00:57:25,503 --> 00:57:41,842\nSpeaker 0: OK? Yeah. Great. It's two-thirty, I've got to go. I hope that was helpful for you. Like I say, I'm not being critical. I think it's really good. What I'm trying to do is give you information to make it much better.\n\n299\n00:57:41,862 --> 00:57:57,395\nSpeaker 2: Thank you, thank you. It was actually really helpful, especially with describing how you did the coding. Yeah, this is stuff that your supervisor should be telling you, but maybe they're not familiar with that.\n\n300\n00:57:58,342 --> 00:58:16,638\nSpeaker 0: which is why I printed that paper for you. But yeah, come back any time. Book another session, or if you want to chat to Kudo Sensei or Damien Rivers. I want to get a different perspective, because they are in different backgrounds to me. Please do so.\n\n301\n00:58:16,878 --> 00:58:21,322\nSpeaker 2: I'll book another session when you want to do this again. Yeah, got it.\n\n302\n00:58:21,342 --> 00:58:23,043\nSpeaker 0: Thank you very much. That's OK. Great. I enjoyed that.  ",
    "transcript_list": [
        {
            "dialogue": "I have a motorbike called Argy.",
            "end_timestamp": "00:00:24,899",
            "id": 1,
            "speaker": "Speaker 2",
            "start_timestamp": "00:00:19,740"
        },
        {
            "dialogue": "Oh, that's a model in Suzuki.",
            "end_timestamp": "00:00:39,092",
            "id": 2,
            "speaker": "Speaker 1",
            "start_timestamp": "00:00:37,711"
        },
        {
            "dialogue": "Yeah, yeah, RG Five Hundred is a Suzuki model.",
            "end_timestamp": "00:00:41,973",
            "id": 3,
            "speaker": "Speaker 0",
            "start_timestamp": "00:00:39,312"
        },
        {
            "dialogue": "I did not know that.",
            "end_timestamp": "00:00:43,014",
            "id": 4,
            "speaker": "Speaker 2",
            "start_timestamp": "00:00:42,333"
        },
        {
            "dialogue": "Yeah, there you go, so RG, great. How do I call you, Dwight? Michael, Michael's fine. Michael, okay. Now, how long have you been at Fun?",
            "end_timestamp": "00:00:52,078",
            "id": 5,
            "speaker": "Speaker 0",
            "start_timestamp": "00:00:43,074"
        },
        {
            "dialogue": "I've been here for...",
            "end_timestamp": "00:00:53,139",
            "id": 6,
            "speaker": "Speaker 2",
            "start_timestamp": "00:00:52,098"
        },
        {
            "dialogue": "More than one year now. It's my second year.",
            "end_timestamp": "00:00:59,197",
            "id": 7,
            "speaker": "Speaker 1",
            "start_timestamp": "00:00:57,136"
        },
        {
            "dialogue": "I arrived here last year on November, two thousand twenty one. Right. Because the pandemic, I haven't really seen.",
            "end_timestamp": "00:01:08,821",
            "id": 8,
            "speaker": "Speaker 2",
            "start_timestamp": "00:00:59,837"
        },
        {
            "dialogue": "I've never met you before, so that's quite unusual.",
            "end_timestamp": "00:01:11,933",
            "id": 9,
            "speaker": "Speaker 0",
            "start_timestamp": "00:01:09,471"
        },
        {
            "dialogue": "I usually go to all the student presentations. Yeah, I think I was, as of November, I think I was the only international student who was new, I was the only new international student who was here. a lot of the students are starting to come back, which is great. Yeah, the borders opened up again. Yeah, yeah.",
            "end_timestamp": "00:01:41,357",
            "id": 10,
            "speaker": "Speaker 2",
            "start_timestamp": "00:01:11,953"
        },
        {
            "dialogue": "My son goes to a university in Tokyo and it's an international university called International Christian University. and about forty percent of the students are international students. so in his first year during the pandemic the only students he met were Japanese. he's like i've come to this international university and there's no international students because the borders are closed. yeah and of course all the existing international students want nothing to do with the first years. yeah because he's like new.",
            "end_timestamp": "00:02:13,001",
            "id": 11,
            "speaker": "Speaker 0",
            "start_timestamp": "00:01:41,778"
        },
        {
            "dialogue": "But when it opened for that university, bit by bit, they were letting students in. Now, we said it's back to normal.",
            "end_timestamp": "00:02:24,721",
            "id": 12,
            "speaker": "Speaker 2",
            "start_timestamp": "00:02:15,034"
        },
        {
            "dialogue": "The excelling point of the university is that it's international curriculum, American, basically, curriculum. And it's very dynamic.",
            "end_timestamp": "00:02:37,590",
            "id": 13,
            "speaker": "Speaker 0",
            "start_timestamp": "00:02:26,402"
        },
        {
            "dialogue": "He loves it now.",
            "end_timestamp": "00:02:39,071",
            "id": 14,
            "speaker": "Speaker 2",
            "start_timestamp": "00:02:38,130"
        },
        {
            "dialogue": "He says it's great. Yeah, it's good to hear that.",
            "end_timestamp": "00:02:42,052",
            "id": 15,
            "speaker": "Speaker 1",
            "start_timestamp": "00:02:39,111"
        },
        {
            "dialogue": "I understand how that feels, like being the only international student here. Yeah, the big selling point, and I'm telling you, experience being a farmer, was the fact that it was an international university.",
            "end_timestamp": "00:02:55,776",
            "id": 16,
            "speaker": "Speaker 2",
            "start_timestamp": "00:02:42,293"
        },
        {
            "dialogue": "There's no students there, and you're on Zoom.",
            "end_timestamp": "00:02:58,977",
            "id": 17,
            "speaker": "Speaker 0",
            "start_timestamp": "00:02:55,796"
        },
        {
            "dialogue": "I'm like, What am I paying for? Absolutely not. I'm not a big fan.",
            "end_timestamp": "00:03:03,523",
            "id": 18,
            "speaker": "Speaker 1",
            "start_timestamp": "00:02:59,398"
        },
        {
            "dialogue": "I like the blended idea. I like to teach content online, but interaction and this kind of communication, even face-to-face.",
            "end_timestamp": "00:03:28,492",
            "id": 19,
            "speaker": "Speaker 2",
            "start_timestamp": "00:03:15,502"
        },
        {
            "dialogue": "Zoom is not good enough. Yeah, I'm not a fan of Zoom either.",
            "end_timestamp": "00:03:32,215",
            "id": 20,
            "speaker": "Speaker 0",
            "start_timestamp": "00:03:29,013"
        },
        {
            "dialogue": "Staring at lots of little titles or faces on my computer screen, I thought, no, I'm not doing this. This is rubbish. Yeah, it's not that immersive. And on the other hand, I was paying for my son to go to university to be one of those kids on Zoom.",
            "end_timestamp": "00:03:50,046",
            "id": 21,
            "speaker": "Speaker 2",
            "start_timestamp": "00:03:32,836"
        },
        {
            "dialogue": "So I was like, I don't like it as a teacher. I don't like it as a fee-paying father.",
            "end_timestamp": "00:03:55,969",
            "id": 22,
            "speaker": "Speaker 0",
            "start_timestamp": "00:03:50,887"
        },
        {
            "dialogue": "And my son doesn't like it as a student.",
            "end_timestamp": "00:03:58,530",
            "id": 23,
            "speaker": "Speaker 2",
            "start_timestamp": "00:03:55,989"
        },
        {
            "dialogue": "It's just all bad. Yeah, it was pretty bad. Yeah, it was pretty bad. There we go. OK, there we go.",
            "end_timestamp": "00:04:05,833",
            "id": 24,
            "speaker": "Speaker 0",
            "start_timestamp": "00:03:59,810"
        },
        {
            "dialogue": "OK. Now, thank you for sending this. Thanks for coming. Of course.",
            "end_timestamp": "00:04:10,275",
            "id": 25,
            "speaker": "Speaker 2",
            "start_timestamp": "00:04:06,413"
        },
        {
            "dialogue": "Think of me as, imagine you're at an international conference. Let's say you're on a plane. in England, and you're presenting in England, and most of the people are, say, from Europe, most likely. You know, you probably get some from Asia, some from Americas, some from Africa, possibly. But, you know, English, European conference, you mostly get European-English people, yeah? Yeah. So, when you present there, you'll have a different kind of personality will be observing you and giving you comments, questions, and maybe criticism, which you may not get in, say, Asia.",
            "end_timestamp": "00:05:00,648",
            "id": 26,
            "speaker": "Speaker 0",
            "start_timestamp": "00:04:18,762"
        },
        {
            "dialogue": "I used to work in Malaysia, I used to work in Singapore, I now work in Japan, so I know how things are in Asia.",
            "end_timestamp": "00:05:08,411",
            "id": 27,
            "speaker": "Speaker 2",
            "start_timestamp": "00:05:01,328"
        },
        {
            "dialogue": "Now, I will tell you, from Singapore and Malaysian and Japanese, the Singaporeans are very critical, and I love that.",
            "end_timestamp": "00:05:14,614",
            "id": 28,
            "speaker": "Speaker 0",
            "start_timestamp": "00:05:08,431"
        },
        {
            "dialogue": "They don't like your work, they'll say it.",
            "end_timestamp": "00:05:18,035",
            "id": 29,
            "speaker": "Speaker 2",
            "start_timestamp": "00:05:16,134"
        },
        {
            "dialogue": "Malaysians, kind of a bit more polite, should we say? Japanese, they don't say anything. cautious in what they say, so you don't get much criticism, feedback in Japan compared to what you would get in Singapore, compared to what you would get in somewhere like England.",
            "end_timestamp": "00:05:38,562",
            "id": 30,
            "speaker": "Speaker 0",
            "start_timestamp": "00:05:19,036"
        },
        {
            "dialogue": "What I'm trying to say is that I will give you some critical feedback, but it's not a criticism, it's the kind of feedback that you may be getting if you presented this at a conference in England.",
            "end_timestamp": "00:05:52,257",
            "id": 31,
            "speaker": "Speaker 2",
            "start_timestamp": "00:05:40,831"
        },
        {
            "dialogue": "So that's the way I go through things.",
            "end_timestamp": "00:05:56,359",
            "id": 32,
            "speaker": "Speaker 0",
            "start_timestamp": "00:05:54,898"
        },
        {
            "dialogue": "I think it's good.",
            "end_timestamp": "00:05:57,340",
            "id": 33,
            "speaker": "Speaker 2",
            "start_timestamp": "00:05:56,699"
        },
        {
            "dialogue": "It says, look, these are the challenges that you need to face.",
            "end_timestamp": "00:06:03,842",
            "id": 34,
            "speaker": "Speaker 0",
            "start_timestamp": "00:06:00,121"
        },
        {
            "dialogue": "If you can overcome these, you'll have no problem. But you won't know that until you are confronted with those challenges.",
            "end_timestamp": "00:06:12,103",
            "id": 35,
            "speaker": "Speaker 2",
            "start_timestamp": "00:06:04,662"
        },
        {
            "dialogue": "That is true. OK, so first of all, I will say, I made a comment here. First of all, I think this is a very, very well-written paper, very logical, follows in terms of the way you conducted the process of this evaluation, what the limitations are, are some of the finer details of the project.",
            "end_timestamp": "00:06:44,556",
            "id": 36,
            "speaker": "Speaker 0",
            "start_timestamp": "00:06:12,364"
        },
        {
            "dialogue": "Not your writing. Your writing is actually very good, very logical, very, very good.",
            "end_timestamp": "00:06:50,058",
            "id": 37,
            "speaker": "Speaker 2",
            "start_timestamp": "00:06:44,696"
        },
        {
            "dialogue": "So I want to point out some points to you with some questions that you may be able to answer to make this a better paper.",
            "end_timestamp": "00:06:57,340",
            "id": 38,
            "speaker": "Speaker 0",
            "start_timestamp": "00:06:50,538"
        },
        {
            "dialogue": "I'll give an overall summary there, and I've got a couple of recommendations, and then you can ask me some questions.",
            "end_timestamp": "00:07:07,828",
            "id": 39,
            "speaker": "Speaker 2",
            "start_timestamp": "00:07:01,623"
        },
        {
            "dialogue": "Now, because it's in PDF, what I normally do with a Word document, I usually use track changes.",
            "end_timestamp": "00:07:12,932",
            "id": 40,
            "speaker": "Speaker 0",
            "start_timestamp": "00:07:07,848"
        },
        {
            "dialogue": "But with a PDF, it's a bit problematic to do that, even though I've got Adobe Pro, Acrobat Pro, so I did it by pencil. So I tried to read my writing. a few, starting off with the very first line, okay, I wouldn't put in a word like tedious, because it means then, well if it's tedious, don't do it.",
            "end_timestamp": "00:07:42,117",
            "id": 41,
            "speaker": "Speaker 2",
            "start_timestamp": "00:07:14,053"
        },
        {
            "dialogue": "If you think your job, or if you think a design life cycle is tedious, then maybe you're not the person to do it.",
            "end_timestamp": "00:07:52,113",
            "id": 42,
            "speaker": "Speaker 0",
            "start_timestamp": "00:07:43,798"
        },
        {
            "dialogue": "Because a design life cycle for some people is very positive. It's a challenge and people like that challenge. And then it's not tedious.",
            "end_timestamp": "00:08:06,009",
            "id": 43,
            "speaker": "Speaker 2",
            "start_timestamp": "00:07:52,754"
        },
        {
            "dialogue": "It's actually completely opposite for some people. So you mentioned the word challenging later on. Let's put it straight in the beginning, shall we?",
            "end_timestamp": "00:08:15,117",
            "id": 44,
            "speaker": "Speaker 0",
            "start_timestamp": "00:08:06,850"
        },
        {
            "dialogue": "It's an iterative and challenging process because you've got the word challenge there. Straight away, it's challenging. Challenge could be positive. I think challenges are positive. If you see a barrier, it's an opportunity.",
            "end_timestamp": "00:08:30,049",
            "id": 45,
            "speaker": "Speaker 2",
            "start_timestamp": "00:08:15,617"
        },
        {
            "dialogue": "That wall is an opportunity, not a barrier.",
            "end_timestamp": "00:08:33,051",
            "id": 46,
            "speaker": "Speaker 0",
            "start_timestamp": "00:08:30,289"
        },
        {
            "dialogue": "So it's a challenge.",
            "end_timestamp": "00:08:34,712",
            "id": 47,
            "speaker": "Speaker 2",
            "start_timestamp": "00:08:33,431"
        },
        {
            "dialogue": "Great, okay, then I looked at what are you trying to do? Okay, you found in your summary of the abstract, yes, you've got a summary of all the key points that you found in your research. So a great abstract, I completely understand what this paper's going to tell me. Okay. So they come down, industrial sort, underline several stages, fantastic, fantastic. When I come across my first acronym, you need to write it out. Computer Aided Design, bracket CAD, later on, CAD. So just something there.",
            "end_timestamp": "00:09:12,684",
            "id": 48,
            "speaker": "Speaker 0",
            "start_timestamp": "00:08:35,533"
        },
        {
            "dialogue": "First mention, write it out in full.",
            "end_timestamp": "00:09:15,165",
            "id": 49,
            "speaker": "Speaker 2",
            "start_timestamp": "00:09:12,984"
        },
        {
            "dialogue": "Again, tedious, challenging. Yeah, OK. So in this sentence here, it looks like this. Okay, that phrase there, carry loads and endure drops from specific heights, kind of, it doesn't really flow from what you said before.",
            "end_timestamp": "00:09:47,989",
            "id": 50,
            "speaker": "Speaker 0",
            "start_timestamp": "00:09:16,206"
        },
        {
            "dialogue": "So why not say the product meets technical and safety specifications?",
            "end_timestamp": "00:09:52,211",
            "id": 51,
            "speaker": "Speaker 2",
            "start_timestamp": "00:09:48,469"
        },
        {
            "dialogue": "So carry loads and maybe specific guides are probably technical and safety specifications. So why not change that to that? Because it's kind of not in context with what you're saying before.",
            "end_timestamp": "00:10:09,650",
            "id": 52,
            "speaker": "Speaker 0",
            "start_timestamp": "00:09:54,838"
        },
        {
            "dialogue": "It sounds like a very concrete example.",
            "end_timestamp": "00:10:12,532",
            "id": 53,
            "speaker": "Speaker 2",
            "start_timestamp": "00:10:10,190"
        },
        {
            "dialogue": "Yeah, you're kind of being generalized there and specific there, suddenly. So if you make it generalized, you've probably got that phrase there. So this is why I'm saying, you know, your writing is very, very good. Then you've got this word, out of expertise, knowledge, generalized. Generalized knowledge. Because, you know, if you've got expert knowledge and general knowledge and no knowledge. So this would be generalized knowledge. Because that person's not an expert, they've just got general knowledge.",
            "end_timestamp": "00:10:50,046",
            "id": 54,
            "speaker": "Speaker 0",
            "start_timestamp": "00:10:12,813"
        },
        {
            "dialogue": "Right, but I think what I wanted to say here was it's – yeah, it's – I wouldn't say it's general knowledge, but it's knowledge that is specific to another domain. that's not in their domain. What would the right term for that – what would the right term would be for that?",
            "end_timestamp": "00:11:08,428",
            "id": 55,
            "speaker": "Speaker 2",
            "start_timestamp": "00:10:51,201"
        },
        {
            "dialogue": "Like in this case, for example, I mentioned that, well, I didn't really cite it specifically, maybe in the related work here, but in this study, what I was trying to say was that engineers had limited access to knowledge that was, not knowledge that pertains to manufacturing.",
            "end_timestamp": "00:11:30,044",
            "id": 56,
            "speaker": "Speaker 1",
            "start_timestamp": "00:11:09,288"
        },
        {
            "dialogue": "So...",
            "end_timestamp": "00:11:31,085",
            "id": 57,
            "speaker": "Speaker 2",
            "start_timestamp": "00:11:30,845"
        },
        {
            "dialogue": "Okay, so how about access to knowledge outside their expertise? Right, yeah, yeah. Yeah, yeah, that's outside. Do you want to make a view, right? Oh, right, yeah. You've got a pen? Knowledge outside their expertise.",
            "end_timestamp": "00:11:50,362",
            "id": 58,
            "speaker": "Speaker 0",
            "start_timestamp": "00:11:34,908"
        },
        {
            "dialogue": "Okay, I got it, I see what you've done. Okay, and then I just...",
            "end_timestamp": "00:12:02,853",
            "id": 59,
            "speaker": "Speaker 2",
            "start_timestamp": "00:11:50,382"
        },
        {
            "dialogue": "So you've got your research goals, one and two. Okay, two questions, very, very clear. And I'll come back to this later, because in your conclusion, you only had one. I'll come back to that later. So, let's start this one. Okay, must meet each of their requirements, just change it to specific requirements.",
            "end_timestamp": "00:12:33,316",
            "id": 60,
            "speaker": "Speaker 0",
            "start_timestamp": "00:12:09,651"
        },
        {
            "dialogue": "Okay, that's straightforward.",
            "end_timestamp": "00:12:34,256",
            "id": 61,
            "speaker": "Speaker 2",
            "start_timestamp": "00:12:33,336"
        },
        {
            "dialogue": "Just a little, maybe a typo, you've got a question mark, question mark there, that's probably a development, yeah. Yeah, I've got stakeholder, what have I got? Yeah, okay, this reference here to they're, I wasn't sure what you meant. Because you've got sue and lue, however you say that, they're refers to them. But actually when I read it again, they're refers to stakeholders. So there's a confusion because this is what we call a backward reference in, for what the word is, but there's a single backward reference. So thea is backward reference into the subject, which is these. In actual fact, it's these, which is a different kind of reference, exophoric reference. So you need to write the word in. But that's only because you write it many times, so you know who theas are. So when I read it for the first time, That's why you give your paper to your friend to read.",
            "end_timestamp": "00:13:38,760",
            "id": 62,
            "speaker": "Speaker 0",
            "start_timestamp": "00:12:34,496"
        },
        {
            "dialogue": "Exactly, that's why I consulted. Yeah, that's right.",
            "end_timestamp": "00:13:42,641",
            "id": 63,
            "speaker": "Speaker 2",
            "start_timestamp": "00:13:39,160"
        },
        {
            "dialogue": "So you come to me and go to your friends, yeah? So... Again, you then switch to... Ah, wait a minute. Okay, you've got the word... I've just changed the language a bit to make it a bit better. You've got verifying them, just say subsequent verification. Right, right. Just makes it sound better, okay? You've got stakeholders, then you've got users. So I put a question mark there.",
            "end_timestamp": "00:14:14,028",
            "id": 64,
            "speaker": "Speaker 0",
            "start_timestamp": "00:13:42,661"
        },
        {
            "dialogue": "Do you mean stakeholders? Because suddenly users have appeared. I don't know who these users are. Right. I think when",
            "end_timestamp": "00:14:21,415",
            "id": 65,
            "speaker": "Speaker 2",
            "start_timestamp": "00:14:14,108"
        },
        {
            "dialogue": "I meant users,",
            "end_timestamp": "00:14:22,376",
            "id": 66,
            "speaker": "Speaker 1",
            "start_timestamp": "00:14:21,475"
        },
        {
            "dialogue": "I meant like customers",
            "end_timestamp": "00:14:25,539",
            "id": 67,
            "speaker": "Speaker 2",
            "start_timestamp": "00:14:22,436"
        },
        {
            "dialogue": "who have been invited",
            "end_timestamp": "00:14:26,700",
            "id": 68,
            "speaker": "Speaker 1",
            "start_timestamp": "00:14:25,739"
        },
        {
            "dialogue": "for",
            "end_timestamp": "00:14:27,300",
            "id": 69,
            "speaker": "Speaker 2",
            "start_timestamp": "00:14:27,120"
        },
        {
            "dialogue": "for",
            "end_timestamp": "00:14:32,200",
            "id": 70,
            "speaker": "Speaker 1",
            "start_timestamp": "00:14:31,600"
        },
        {
            "dialogue": "this assessment. But the people that you get to assess design, are the people involved in the design?",
            "end_timestamp": "00:14:39,403",
            "id": 71,
            "speaker": "Speaker 0",
            "start_timestamp": "00:14:32,540"
        },
        {
            "dialogue": "In this study that I cited, no, they invited outside customers, like the survey of customers.",
            "end_timestamp": "00:14:49,066",
            "id": 72,
            "speaker": "Speaker 1",
            "start_timestamp": "00:14:41,103"
        },
        {
            "dialogue": "So when I said customers, I wrote the word users. So these are actually Oh, I see. So the designers there are bringing in outside people who are possible users of the device to give us a... Okay, I get it. I understand now.",
            "end_timestamp": "00:15:11,833",
            "id": 73,
            "speaker": "Speaker 0",
            "start_timestamp": "00:14:49,486"
        },
        {
            "dialogue": "Or maybe I should...",
            "end_timestamp": "00:15:12,974",
            "id": 74,
            "speaker": "Speaker 1",
            "start_timestamp": "00:15:12,373"
        },
        {
            "dialogue": "No, no, no, it's just me. Don't worry. That's fine. I see what you mean. now, because I'm not familiar with these papers, and I didn't check them, so... I understand.",
            "end_timestamp": "00:15:24,677",
            "id": 75,
            "speaker": "Speaker 0",
            "start_timestamp": "00:15:14,194"
        },
        {
            "dialogue": "No, I'm sure it's fine.",
            "end_timestamp": "00:15:25,898",
            "id": 76,
            "speaker": "Speaker 2",
            "start_timestamp": "00:15:25,178"
        },
        {
            "dialogue": "Again, just to rub this a bit better, I've taken that out, put in it, instead of raised, put the word reported, that's all. It's just stylistic more than anything else.",
            "end_timestamp": "00:15:40,939",
            "id": 77,
            "speaker": "Speaker 0",
            "start_timestamp": "00:15:27,664"
        },
        {
            "dialogue": "So instead of raised, You raise a point, you raise a motion, but actually these people are reporting information. You raise a concern, you report information. It's kind of slightly different, yeah. Okay, so it's more on, yeah, this is more appropriate to use. This is more appropriate, you report something.",
            "end_timestamp": "00:16:03,083",
            "id": 78,
            "speaker": "Speaker 2",
            "start_timestamp": "00:15:41,620"
        },
        {
            "dialogue": "You certainly raise something, but then a synonym of raise is pointed out, highlighted, which you don't mean there, you just mean reported.",
            "end_timestamp": "00:16:13,788",
            "id": 79,
            "speaker": "Speaker 0",
            "start_timestamp": "00:16:03,123"
        },
        {
            "dialogue": "So when you say the rays, you don't really use that when you're stating the results of a study that you're citing?",
            "end_timestamp": "00:16:25,258",
            "id": 80,
            "speaker": "Speaker 1",
            "start_timestamp": "00:16:14,693"
        },
        {
            "dialogue": "I don't want to say no, because it's not true. I think if you wanted to emphasize",
            "end_timestamp": "00:16:38,305",
            "id": 81,
            "speaker": "Speaker 0",
            "start_timestamp": "00:16:25,278"
        },
        {
            "dialogue": "something, contrast something with the previous research,",
            "end_timestamp": "00:16:44,419",
            "id": 82,
            "speaker": "Speaker 2",
            "start_timestamp": "00:16:38,365"
        },
        {
            "dialogue": "that would be possible, but probably emphasising",
            "end_timestamp": "00:16:46,820",
            "id": 83,
            "speaker": "Speaker 0",
            "start_timestamp": "00:16:44,439"
        },
        {
            "dialogue": "with your daughter, you know, that if you talk",
            "end_timestamp": "00:16:50,162",
            "id": 84,
            "speaker": "Speaker 2",
            "start_timestamp": "00:16:46,840"
        },
        {
            "dialogue": "about research that such and such raise the concern or raise the point that, you know, and then you're highlighting something",
            "end_timestamp": "00:16:59,571",
            "id": 85,
            "speaker": "Speaker 0",
            "start_timestamp": "00:16:50,182"
        },
        {
            "dialogue": "in addition,",
            "end_timestamp": "00:17:00,311",
            "id": 86,
            "speaker": "Speaker 2",
            "start_timestamp": "00:16:59,711"
        },
        {
            "dialogue": "which is",
            "end_timestamp": "00:17:01,772",
            "id": 87,
            "speaker": "Speaker 1",
            "start_timestamp": "00:17:01,352"
        },
        {
            "dialogue": "a level",
            "end_timestamp": "00:17:03,853",
            "id": 88,
            "speaker": "Speaker 2",
            "start_timestamp": "00:17:01,792"
        },
        {
            "dialogue": "above what you previously reported. Right. It's like, this is a little bit more important than that. Okay, okay. That's, but in this material, you're not, you're giving everything an equal status.",
            "end_timestamp": "00:17:13,377",
            "id": 89,
            "speaker": "Speaker 0",
            "start_timestamp": "00:17:04,093"
        },
        {
            "dialogue": "Ah, okay. So it raises, like, pinpointing on something very specific. Yeah, yeah, highlighted, pinpointed, I like that, yeah. I see. Yeah. But again, it's just, It's just the use of synonyms in a way, but that's better. I understand. Okay. Keeps going, I'll get more critical for later on. Address determined, it's a synonym, I don't know. Right, now here we go.",
            "end_timestamp": "00:17:40,934",
            "id": 90,
            "speaker": "Speaker 2",
            "start_timestamp": "00:17:14,178"
        },
        {
            "dialogue": "So, okay, so at the end of this part, which was two point one, you know, this is kind of like a, but related work leading up to your research question.",
            "end_timestamp": "00:17:51,617",
            "id": 91,
            "speaker": "Speaker 0",
            "start_timestamp": "00:17:40,994"
        },
        {
            "dialogue": "Fine.",
            "end_timestamp": "00:17:52,677",
            "id": 92,
            "speaker": "Speaker 2",
            "start_timestamp": "00:17:52,417"
        },
        {
            "dialogue": "So, this was your first aim, yeah?",
            "end_timestamp": "00:17:57,198",
            "id": 93,
            "speaker": "Speaker 0",
            "start_timestamp": "00:17:53,917"
        },
        {
            "dialogue": "So in this study, we aim to...",
            "end_timestamp": "00:18:02,605",
            "id": 94,
            "speaker": "Speaker 2",
            "start_timestamp": "00:17:59,102"
        },
        {
            "dialogue": "Fine, but when I read it further, you've actually got two aims, two questions.",
            "end_timestamp": "00:18:09,250",
            "id": 95,
            "speaker": "Speaker 0",
            "start_timestamp": "00:18:02,685"
        },
        {
            "dialogue": "Yeah, that's true.",
            "end_timestamp": "00:18:10,731",
            "id": 96,
            "speaker": "Speaker 2",
            "start_timestamp": "00:18:09,370"
        },
        {
            "dialogue": "So let's call this your first one, okay? That's your first aim. So in this study, our first aim is to... Then I read the second part. In this study, our second aim, or the second aim of this study is to... So you're making it very specific now, you've got two aims.",
            "end_timestamp": "00:18:31,621",
            "id": 97,
            "speaker": "Speaker 0",
            "start_timestamp": "00:18:10,992"
        },
        {
            "dialogue": "This one and this one.",
            "end_timestamp": "00:18:33,181",
            "id": 98,
            "speaker": "Speaker 2",
            "start_timestamp": "00:18:32,221"
        },
        {
            "dialogue": "Because I had to go back and thought, that's your aim there, but you've got an aim here, what's happening?",
            "end_timestamp": "00:18:38,402",
            "id": 99,
            "speaker": "Speaker 0",
            "start_timestamp": "00:18:34,141"
        },
        {
            "dialogue": "And then I went back, ah, I see.",
            "end_timestamp": "00:18:41,702",
            "id": 100,
            "speaker": "Speaker 2",
            "start_timestamp": "00:18:39,042"
        },
        {
            "dialogue": "You see what I mean? As a reader, I shouldn't do that. You've got to make it clear, one aim there, one aim there. So when I read the rest of the paper, I'm looking for the answers to these two questions. That's all. And then you've got, You've got goals and aims. Again, asking for, requesting, same thing. I'm not sure. I'm sure I know what to say anymore.",
            "end_timestamp": "00:19:16,189",
            "id": 101,
            "speaker": "Speaker 0",
            "start_timestamp": "00:18:41,722"
        },
        {
            "dialogue": "Is it male and female or men and women?",
            "end_timestamp": "00:19:32,287",
            "id": 102,
            "speaker": "Speaker 2",
            "start_timestamp": "00:19:27,159"
        },
        {
            "dialogue": "Well, I don't know. This is an area I'm a bit, you know, I've been in Japan too long.",
            "end_timestamp": "00:19:35,852",
            "id": 103,
            "speaker": "Speaker 0",
            "start_timestamp": "00:19:32,487"
        },
        {
            "dialogue": "If I went to America, maybe I'm not allowed to say that anymore.",
            "end_timestamp": "00:19:39,157",
            "id": 104,
            "speaker": "Speaker 2",
            "start_timestamp": "00:19:35,912"
        },
        {
            "dialogue": "I don't know anymore. Let's call it male and female, shall we?",
            "end_timestamp": "00:19:42,863",
            "id": 105,
            "speaker": "Speaker 0",
            "start_timestamp": "00:19:39,177"
        },
        {
            "dialogue": "Yeah, I think that would be better. Yeah.",
            "end_timestamp": "00:19:45,149",
            "id": 106,
            "speaker": "Speaker 2",
            "start_timestamp": "00:19:43,328"
        },
        {
            "dialogue": "Where is this going to be presented?",
            "end_timestamp": "00:19:47,509",
            "id": 107,
            "speaker": "Speaker 0",
            "start_timestamp": "00:19:45,769"
        },
        {
            "dialogue": "It's going to be presented in CHI.",
            "end_timestamp": "00:19:50,330",
            "id": 108,
            "speaker": "Speaker 2",
            "start_timestamp": "00:19:47,529"
        },
        {
            "dialogue": "CHI, it's a Human-Computer Interaction Conference.",
            "end_timestamp": "00:19:53,571",
            "id": 109,
            "speaker": "Speaker 1",
            "start_timestamp": "00:19:51,110"
        },
        {
            "dialogue": "Which city?",
            "end_timestamp": "00:19:54,171",
            "id": 110,
            "speaker": "Speaker 2",
            "start_timestamp": "00:19:53,651"
        },
        {
            "dialogue": "They'll be held in Hamburg.",
            "end_timestamp": "00:19:56,392",
            "id": 111,
            "speaker": "Speaker 1",
            "start_timestamp": "00:19:54,511"
        },
        {
            "dialogue": "Oh, Germany. No, I'm saying this is going to be presented in Los Angeles.",
            "end_timestamp": "00:20:01,833",
            "id": 112,
            "speaker": "Speaker 0",
            "start_timestamp": "00:19:57,112"
        },
        {
            "dialogue": "You might have a bit of an issue with what's going on at the moment. OK.",
            "end_timestamp": "00:20:06,695",
            "id": 113,
            "speaker": "Speaker 2",
            "start_timestamp": "00:20:01,873"
        },
        {
            "dialogue": "then you're, you know, because you're researching now, you're thinking, OK, you've got to be specific.",
            "end_timestamp": "00:20:13,890",
            "id": 114,
            "speaker": "Speaker 0",
            "start_timestamp": "00:20:09,025"
        },
        {
            "dialogue": "So most of the participants were from the Philippines. Actually, no. Tell me how many were from the Philippines. Yeah. OK. You've got to be dead right. All right. Six were. One wasn't. So one's Japanese, rather than most. Yeah.",
            "end_timestamp": "00:20:29,004",
            "id": 115,
            "speaker": "Speaker 2",
            "start_timestamp": "00:20:14,310"
        },
        {
            "dialogue": "Right. Now, this is where it gets a little bit. Yeah, you put in information there that either A, you need to explain to the reader, or B, you don't know. So this information there, I'm not sure if the reader's supposed to know, or maybe you don't know what it is. I don't know from this.",
            "end_timestamp": "00:20:55,940",
            "id": 116,
            "speaker": "Speaker 0",
            "start_timestamp": "00:20:29,804"
        },
        {
            "dialogue": "So you say, using grounded theory, fine. You're assuming that everybody knows grounded theory.",
            "end_timestamp": "00:21:04,025",
            "id": 117,
            "speaker": "Speaker 2",
            "start_timestamp": "00:20:56,241"
        },
        {
            "dialogue": "So it's quite important to define. grounded theory is. It does two things. One, it tells the reader what it is, because the reader might not know. And two, it demonstrates that you know what it is as the writer. So just one sentence, grounded theory is, and the benefits of grounded theory are. So in other words, why grounded theory?",
            "end_timestamp": "00:21:31,036",
            "id": 118,
            "speaker": "Speaker 0",
            "start_timestamp": "00:21:05,791"
        },
        {
            "dialogue": "Why not some other approach?",
            "end_timestamp": "00:21:33,477",
            "id": 119,
            "speaker": "Speaker 2",
            "start_timestamp": "00:21:31,396"
        },
        {
            "dialogue": "Why not do a survey? You know, qualitative data in that respect. Get some quantitative feedback. So you're using grounded theory, which is fine. Tell us what it is and why you used it.",
            "end_timestamp": "00:21:48,684",
            "id": 120,
            "speaker": "Speaker 0",
            "start_timestamp": "00:21:34,477"
        },
        {
            "dialogue": "Just a couple of sentences.",
            "end_timestamp": "00:21:51,485",
            "id": 121,
            "speaker": "Speaker 2",
            "start_timestamp": "00:21:49,584"
        },
        {
            "dialogue": "Same with, right, now, you quoted the transcripts. There's a red flag, code. What code did you use? So again, this is where you've got to explain what code you used and how the process of that code. Because in research, if you're going to code something, you must have a system of coding. You must have criteria for coding text, for coding what people write, basically.",
            "end_timestamp": "00:22:34,741",
            "id": 122,
            "speaker": "Speaker 0",
            "start_timestamp": "00:21:52,045"
        },
        {
            "dialogue": "Okay, so here, do I have to specify the criteria?",
            "end_timestamp": "00:22:43,066",
            "id": 123,
            "speaker": "Speaker 1",
            "start_timestamp": "00:22:39,825"
        },
        {
            "dialogue": "Yeah, I've got an example here for you. Yes, you could specify the criteria. Secondly, who checked it? Who did the coding and who checked your coding? How many people were involved? What was the inter-reliability rate? So",
            "end_timestamp": "00:23:01,491",
            "id": 124,
            "speaker": "Speaker 2",
            "start_timestamp": "00:22:43,346"
        },
        {
            "dialogue": "when you look at coding transcripts,",
            "end_timestamp": "00:23:03,532",
            "id": 125,
            "speaker": "Speaker 0",
            "start_timestamp": "00:23:01,871"
        },
        {
            "dialogue": "and you look at grounded",
            "end_timestamp": "00:23:05,412",
            "id": 126,
            "speaker": "Speaker 2",
            "start_timestamp": "00:23:04,112"
        },
        {
            "dialogue": "theory and qualitative research, and you look under the section coding transcripts, you'll find, this is actually quite common, that needs to be done, that you've got to decide",
            "end_timestamp": "00:23:16,515",
            "id": 127,
            "speaker": "Speaker 0",
            "start_timestamp": "00:23:05,452"
        },
        {
            "dialogue": "what the coding is, who checked",
            "end_timestamp": "00:23:19,256",
            "id": 128,
            "speaker": "Speaker 2",
            "start_timestamp": "00:23:16,535"
        },
        {
            "dialogue": "that coding, you then coded all the transcripts, you need a second person to code the transcripts, and then the two of you have got to get together and compare your results.",
            "end_timestamp": "00:23:30,459",
            "id": 129,
            "speaker": "Speaker 0",
            "start_timestamp": "00:23:19,296"
        },
        {
            "dialogue": "And that's called an inter-reliability rate. Oh, so that's how it works. That's how it works. And the more people you get coding, the better. So for example, when I was in Singapore, we'd have educational researchers with PhD students.",
            "end_timestamp": "00:23:44,975",
            "id": 130,
            "speaker": "Speaker 2",
            "start_timestamp": "00:23:31,547"
        },
        {
            "dialogue": "We'd be videotaping teachers teaching.",
            "end_timestamp": "00:23:48,858",
            "id": 131,
            "speaker": "Speaker 0",
            "start_timestamp": "00:23:45,776"
        },
        {
            "dialogue": "They'd come back, we'd have them transcribe all the videos.",
            "end_timestamp": "00:23:54,061",
            "id": 132,
            "speaker": "Speaker 2",
            "start_timestamp": "00:23:49,878"
        },
        {
            "dialogue": "And then we'd have thousands and thousands of lines of text, transcript, and these three or four or five or six researchers would then discuss a coding scheme. We've come up with a coding scheme, we've decided the coding scheme, fine. Now they go away and they assign parts of the transcript to each code. Right then, they come together and then they compare all their results. And if all",
            "end_timestamp": "00:24:28,351",
            "id": 133,
            "speaker": "Speaker 0",
            "start_timestamp": "00:23:54,541"
        },
        {
            "dialogue": "their results are too different,",
            "end_timestamp": "00:24:29,671",
            "id": 134,
            "speaker": "Speaker 2",
            "start_timestamp": "00:24:28,371"
        },
        {
            "dialogue": "they've got to",
            "end_timestamp": "00:24:30,491",
            "id": 135,
            "speaker": "Speaker 0",
            "start_timestamp": "00:24:30,171"
        },
        {
            "dialogue": "go back and start again",
            "end_timestamp": "00:24:31,492",
            "id": 136,
            "speaker": "Speaker 2",
            "start_timestamp": "00:24:30,531"
        },
        {
            "dialogue": "and do another, either do the coding,",
            "end_timestamp": "00:24:33,913",
            "id": 137,
            "speaker": "Speaker 0",
            "start_timestamp": "00:24:32,072"
        },
        {
            "dialogue": "the",
            "end_timestamp": "00:24:34,553",
            "id": 138,
            "speaker": "Speaker 2",
            "start_timestamp": "00:24:34,413"
        },
        {
            "dialogue": "criteria",
            "end_timestamp": "00:24:35,654",
            "id": 139,
            "speaker": "Speaker 0",
            "start_timestamp": "00:24:34,953"
        },
        {
            "dialogue": "selection",
            "end_timestamp": "00:24:36,554",
            "id": 140,
            "speaker": "Speaker 2",
            "start_timestamp": "00:24:36,094"
        },
        {
            "dialogue": "again, maybe narrow it down, widen it, probably narrow it down, then go back and then decide what part of the transcript goes with this code. And then they go back and do it again. And then until they get an inter-reliability rate of ninety percent, And then you say, okay, now we can analyze this data. Oh, so that's how coding works.",
            "end_timestamp": "00:25:00,968",
            "id": 141,
            "speaker": "Speaker 0",
            "start_timestamp": "00:24:36,594"
        },
        {
            "dialogue": "That's how coding works, yeah.",
            "end_timestamp": "00:25:03,409",
            "id": 142,
            "speaker": "Speaker 2",
            "start_timestamp": "00:25:00,988"
        },
        {
            "dialogue": "So, we've done it, myself and two colleagues here have done it, we did it two years ago during the pandemic, and we called it thematic analysis, which is explain that process. so you can use our paper as an example of the process of coding and how we came up, because we did something similar. So you need to explain that before you move on to the results, because without that foundation of coding then everything else is unreliable. Even though when I read your scripts, it made sense and I can understand why you did it, but at the same time, when I read your conclusion and transcripts that support your conclusion, somebody in the audience may put their hand up and say that's bias. You may be biased. In other words, you are cherry picking. You are picking out information to suit your outcome. Whereas what you should be doing is looking at the information and from the information determine that outcome. But what you could be accused of here is that the outcome has already been decided by you subconsciously, but you've kind of looked for the transcripts to match that. I'm not saying you did that, but that's what you could be accused of. It's not a big accusation, of course, but it's just that somebody may take issue with that. So you don't have to change anything there. I think what you need to do is just justify how you've done this thematic analysis. Even if you keep everything else the same, that's fine. But when you do it, you may change.",
            "end_timestamp": "00:26:58,041",
            "id": 143,
            "speaker": "Speaker 0",
            "start_timestamp": "00:25:03,509"
        },
        {
            "dialogue": "I don't think you'll change, because I think your discussion is actually very focused and very good.",
            "end_timestamp": "00:27:02,125",
            "id": 144,
            "speaker": "Speaker 2",
            "start_timestamp": "00:26:58,081"
        },
        {
            "dialogue": "But I think without this there, it seems very, well, you've already determined what you wanted to do, what you've decided at the end, based on whether the students get, whether these six Filipino designers, one Japanese designer, give that information anyway.",
            "end_timestamp": "00:27:22,664",
            "id": 145,
            "speaker": "Speaker 0",
            "start_timestamp": "00:27:02,145"
        },
        {
            "dialogue": "See what I mean? Because, hey, don't keep going. So think about that. So I'll come back, I'll show you my, okay? So there's my questions there. That, I think, is personally a kind of a weak part of this project, and that's your justification of the method.",
            "end_timestamp": "00:27:40,651",
            "id": 146,
            "speaker": "Speaker 2",
            "start_timestamp": "00:27:24,406"
        },
        {
            "dialogue": "Yeah, okay, so that's it. So as you can see now, from there on, look, the question, are there, this is, yeah.",
            "end_timestamp": "00:27:50,654",
            "id": 147,
            "speaker": "Speaker 0",
            "start_timestamp": "00:27:41,771"
        },
        {
            "dialogue": "Yeah, and then, okay, your results.",
            "end_timestamp": "00:27:53,775",
            "id": 148,
            "speaker": "Speaker 2",
            "start_timestamp": "00:27:51,394"
        },
        {
            "dialogue": "you know, your discussion, it's all very good, sorry, the overview of the results is all very good, and then when it came to the discussion I think this is what you've got to decide yourself.",
            "end_timestamp": "00:28:08,795",
            "id": 149,
            "speaker": "Speaker 0",
            "start_timestamp": "00:27:54,744"
        },
        {
            "dialogue": "In your discussion you said the aim of the study. But in the previous section there were two aims. So I actually personally, I like the fact that you've got it written down as one aim. You've connected the two into one. I like that. And I think it makes it more focused.",
            "end_timestamp": "00:28:28,774",
            "id": 150,
            "speaker": "Speaker 2",
            "start_timestamp": "00:28:09,015"
        },
        {
            "dialogue": "So what you could do at the end of What you could do, you've got aim one, aim two there. What you could do is possibly add another sentence saying the aim of this study is to...",
            "end_timestamp": "00:28:41,413",
            "id": 151,
            "speaker": "Speaker 0",
            "start_timestamp": "00:28:28,814"
        },
        {
            "dialogue": "Just copy that. Just copy that there. Right.",
            "end_timestamp": "00:28:47,815",
            "id": 152,
            "speaker": "Speaker 2",
            "start_timestamp": "00:28:43,294"
        },
        {
            "dialogue": "Yeah, so copy that, put it there, and then this matches this.",
            "end_timestamp": "00:28:52,216",
            "id": 153,
            "speaker": "Speaker 0",
            "start_timestamp": "00:28:47,975"
        },
        {
            "dialogue": "So your literature review output with the aim matches the introduction of the discussion aim. They are exactly the same.",
            "end_timestamp": "00:29:04,296",
            "id": 154,
            "speaker": "Speaker 2",
            "start_timestamp": "00:28:54,068"
        },
        {
            "dialogue": "At the moment you've got one, two, and then you've got one, so they're not the same.",
            "end_timestamp": "00:29:08,320",
            "id": 155,
            "speaker": "Speaker 0",
            "start_timestamp": "00:29:04,817"
        },
        {
            "dialogue": "Okay, so what you're saying is, instead of having two here...",
            "end_timestamp": "00:29:13,822",
            "id": 156,
            "speaker": "Speaker 1",
            "start_timestamp": "00:29:10,501"
        },
        {
            "dialogue": "So what you do, you put one there, and you put another new paragraph, which is one sentence. Overall, the aim of the study is two.",
            "end_timestamp": "00:29:24,065",
            "id": 157,
            "speaker": "Speaker 0",
            "start_timestamp": "00:29:13,842"
        },
        {
            "dialogue": "In summary, or something like that, the aim of the study is two, and then write it down as one sentence.",
            "end_timestamp": "00:29:30,547",
            "id": 158,
            "speaker": "Speaker 2",
            "start_timestamp": "00:29:25,665"
        },
        {
            "dialogue": "Or you have to change that to two. It's up to you. So you either want one aim like this, which connect the two together, or you have two separate aims. that you've done there, but that has to be really, really good. Because this has to match this. Okay? Because then the rest of it then, you know, you discuss. Yeah, and then you... So discuss, okay so you discuss. and then like I say this section is very good, I thought the first section was a little short, the successful based on target demographics. Yeah, it's very good.",
            "end_timestamp": "00:30:12,983",
            "id": 159,
            "speaker": "Speaker 0",
            "start_timestamp": "00:29:32,067"
        },
        {
            "dialogue": "I just wonder if you could explain this section a little bit more, maybe with an example.",
            "end_timestamp": "00:30:19,544",
            "id": 160,
            "speaker": "Speaker 2",
            "start_timestamp": "00:30:13,003"
        },
        {
            "dialogue": "I think you need like four to five more lines there.",
            "end_timestamp": "00:30:23,145",
            "id": 161,
            "speaker": "Speaker 0",
            "start_timestamp": "00:30:19,564"
        },
        {
            "dialogue": "I don't know what word count you're limited to. So if you could maybe explain that a bit more with examples. That would help me because I'm not familiar with the research, so I kind of needed an example there. Which in this one, I was very clear, you're very clear there.",
            "end_timestamp": "00:30:46,158",
            "id": 162,
            "speaker": "Speaker 2",
            "start_timestamp": "00:30:23,845"
        },
        {
            "dialogue": "And at the end of reading this, I thought, well, you've come to the end now, come to your conclusion, you've come to the end of your discussion, so what are you actually recommending?",
            "end_timestamp": "00:30:58,843",
            "id": 163,
            "speaker": "Speaker 0",
            "start_timestamp": "00:30:48,799"
        },
        {
            "dialogue": "So, in summary, or incrementally, before you write the conclusion, what are you actually recommending at the end of your discussion?",
            "end_timestamp": "00:31:17,854",
            "id": 164,
            "speaker": "Speaker 2",
            "start_timestamp": "00:31:08,907"
        },
        {
            "dialogue": "Okay, so, at the end of the discussion, I have to put a summary of what other things I recommend?",
            "end_timestamp": "00:31:25,661",
            "id": 165,
            "speaker": "Speaker 1",
            "start_timestamp": "00:31:20,356"
        },
        {
            "dialogue": "Yeah. To round it up, because you've got Section V.I, Section V.II, Okay, you know, what's next?",
            "end_timestamp": "00:31:39,439",
            "id": 166,
            "speaker": "Speaker 0",
            "start_timestamp": "00:31:25,921"
        },
        {
            "dialogue": "And then you put like a space, and then you can, you know, on the five point, five point, no, just put a space and one or two lines about what you're recommending.",
            "end_timestamp": "00:31:49,808",
            "id": 167,
            "speaker": "Speaker 2",
            "start_timestamp": "00:31:39,639"
        },
        {
            "dialogue": "Because you do recommend from doing all this, you know, the development of what, is it a database or something? Because I had a question at the end, you see. So this is all good, this is all good, really, really good, because at the end, You said, we then plan to develop a prototype focusing on changing material.",
            "end_timestamp": "00:32:09,868",
            "id": 168,
            "speaker": "Speaker 0",
            "start_timestamp": "00:31:50,068"
        },
        {
            "dialogue": "What's that? Yeah, I'm sorry about that. When I submitted the draft, I forgot to finish the sentence.",
            "end_timestamp": "00:32:18,124",
            "id": 169,
            "speaker": "Speaker 1",
            "start_timestamp": "00:32:12,862"
        },
        {
            "dialogue": "Yeah, it says here that this was a pilot study that I did before developing a system that aims to address the challenges that I raised up here.",
            "end_timestamp": "00:32:30,010",
            "id": 170,
            "speaker": "Speaker 2",
            "start_timestamp": "00:32:19,285"
        },
        {
            "dialogue": "Yeah, this was supposed to be a plan to develop a prototype focused specifically on changing materials of a for product design, but I'm not sure if that sentence is needed.",
            "end_timestamp": "00:32:45,476",
            "id": 171,
            "speaker": "Speaker 1",
            "start_timestamp": "00:32:30,210"
        },
        {
            "dialogue": "Probably not, because it's kind of really out of sync with everything that's gone before, because you say you're going to develop there, and I was thinking, well, wait a minute, you're recommending something there which I'm not quite sure, but then you're designing a prototype. So see where that confusion is.",
            "end_timestamp": "00:33:06,128",
            "id": 172,
            "speaker": "Speaker 0",
            "start_timestamp": "00:32:46,257"
        },
        {
            "dialogue": "Maybe the recommendation of the prototype should go there, I don't know.",
            "end_timestamp": "00:33:09,149",
            "id": 173,
            "speaker": "Speaker 2",
            "start_timestamp": "00:33:06,549"
        },
        {
            "dialogue": "So that was unclear to me. So think about that, okay? And then finally, that's an odd one, number twenty.",
            "end_timestamp": "00:33:19,493",
            "id": 174,
            "speaker": "Speaker 0",
            "start_timestamp": "00:33:09,870"
        },
        {
            "dialogue": "What's that?",
            "end_timestamp": "00:33:20,153",
            "id": 175,
            "speaker": "Speaker 2",
            "start_timestamp": "00:33:19,673"
        },
        {
            "dialogue": "I've never seen anything like that before. This was a huge collaborative project.",
            "end_timestamp": "00:33:24,774",
            "id": 176,
            "speaker": "Speaker 1",
            "start_timestamp": "00:33:20,213"
        },
        {
            "dialogue": "That's mad.",
            "end_timestamp": "00:33:25,835",
            "id": 177,
            "speaker": "Speaker 2",
            "start_timestamp": "00:33:25,034"
        },
        {
            "dialogue": "yeah that's mad because you've got it's there.",
            "end_timestamp": "00:33:29,933",
            "id": 178,
            "speaker": "Speaker 0",
            "start_timestamp": "00:33:27,190"
        },
        {
            "dialogue": "there that's the title and it stops there.",
            "end_timestamp": "00:33:33,736",
            "id": 179,
            "speaker": "Speaker 2",
            "start_timestamp": "00:33:29,953"
        },
        {
            "dialogue": "no that's number nineteen.",
            "end_timestamp": "00:33:34,957",
            "id": 180,
            "speaker": "Speaker 0",
            "start_timestamp": "00:33:34,037"
        },
        {
            "dialogue": "sorry that's just really odd.",
            "end_timestamp": "00:33:37,660",
            "id": 181,
            "speaker": "Speaker 2",
            "start_timestamp": "00:33:34,977"
        },
        {
            "dialogue": "yeah i don't know what to do. i've never seen anything like that. um i would probably I don't know. You have to check the journal and see what happens. See if you can find an example in the conference proceedings or a similar journal. that has something like this.",
            "end_timestamp": "00:34:12,628",
            "id": 182,
            "speaker": "Speaker 0",
            "start_timestamp": "00:33:38,200"
        },
        {
            "dialogue": "My intuition is it might be just the first name, et al. Because I think that's kind of ridiculous.",
            "end_timestamp": "00:34:21,856",
            "id": 183,
            "speaker": "Speaker 2",
            "start_timestamp": "00:34:14,090"
        },
        {
            "dialogue": "But I don't know what the general convention is on that one. Because I'm just thinking, if it's a report, and you have lots and lots of people in a report, You wouldn't put all their names on the front page, would you?",
            "end_timestamp": "00:34:38,755",
            "id": 184,
            "speaker": "Speaker 0",
            "start_timestamp": "00:34:21,976"
        },
        {
            "dialogue": "You'd put one person or two people. You can't imagine all these people writing this project. I don't think",
            "end_timestamp": "00:34:54,648",
            "id": 185,
            "speaker": "Speaker 2",
            "start_timestamp": "00:34:39,136"
        },
        {
            "dialogue": "this meant these were",
            "end_timestamp": "00:34:57,670",
            "id": 186,
            "speaker": "Speaker 1",
            "start_timestamp": "00:34:56,728"
        },
        {
            "dialogue": "authors who wrote the paper. So I hope all that kind of feedback is useful for you. What I've done is I've summarized what I've just said in a note there, okay? And I'll send you this in an email later.",
            "end_timestamp": "00:35:10,495",
            "id": 187,
            "speaker": "Speaker 0",
            "start_timestamp": "00:34:57,790"
        },
        {
            "dialogue": "okay so it's very well written and everything i've just said i've written down there.",
            "end_timestamp": "00:35:30,129",
            "id": 188,
            "speaker": "Speaker 2",
            "start_timestamp": "00:35:26,323"
        },
        {
            "dialogue": "and regarding thematic analysis this is a paper i wrote with two colleagues up here on uh during the pandemic and we used We use thematic analysis, and this is a justification. This has become our analytical framework, which is thematic analysis. And you can see the steps that we went through.",
            "end_timestamp": "00:36:00,040",
            "id": 189,
            "speaker": "Speaker 0",
            "start_timestamp": "00:35:30,830"
        },
        {
            "dialogue": "When we got all the students' feedback and transcripts, and we put them all together into a huge document, we then went through these. three of us went through these steps in order to determine what the themes were that came out of this research.",
            "end_timestamp": "00:36:20,941",
            "id": 190,
            "speaker": "Speaker 2",
            "start_timestamp": "00:36:00,060"
        },
        {
            "dialogue": "It's slightly different from yours, but at the same time I'm showing you that there's a method to, you know, doing this kind of grounded theory.",
            "end_timestamp": "00:36:33,244",
            "id": 191,
            "speaker": "Speaker 0",
            "start_timestamp": "00:36:21,981"
        },
        {
            "dialogue": "And that's what we did.",
            "end_timestamp": "00:36:35,084",
            "id": 192,
            "speaker": "Speaker 2",
            "start_timestamp": "00:36:34,364"
        },
        {
            "dialogue": "And then you can see, you can see how You can see the themes that came out together, you can see the percentage of examples. So we got a theme, we defined the theme, and then we looked for examples that represented the definitions of these themes. So we worked from basically nothing.",
            "end_timestamp": "00:37:00,457",
            "id": 193,
            "speaker": "Speaker 0",
            "start_timestamp": "00:36:35,144"
        },
        {
            "dialogue": "But we used the data to determine what the themes were. We didn't go in with themes. We went through our data, we found the themes. By going through this process, we determined what the themes were.",
            "end_timestamp": "00:37:13,717",
            "id": 194,
            "speaker": "Speaker 2",
            "start_timestamp": "00:37:02,426"
        },
        {
            "dialogue": "Then we went back to the data and looked for examples. Oh, okay. So it's a back and forth process.",
            "end_timestamp": "00:37:20,042",
            "id": 195,
            "speaker": "Speaker 1",
            "start_timestamp": "00:37:14,538"
        },
        {
            "dialogue": "Right. Yeah, that constant back and forth, which is what this is exploring.",
            "end_timestamp": "00:37:24,585",
            "id": 196,
            "speaker": "Speaker 2",
            "start_timestamp": "00:37:20,222"
        },
        {
            "dialogue": "So you've built up the themes from the ground up.",
            "end_timestamp": "00:37:27,767",
            "id": 197,
            "speaker": "Speaker 1",
            "start_timestamp": "00:37:25,946"
        },
        {
            "dialogue": "That's what we did. Yeah.",
            "end_timestamp": "00:37:28,887",
            "id": 198,
            "speaker": "Speaker 2",
            "start_timestamp": "00:37:28,067"
        },
        {
            "dialogue": "Grounded themes. You build themes from the ground up. So what we did is instead of deciding what the, we didn't know what the themes were because all we got was feedback from the students during the pandemic of using an online system. Right. With lots of",
            "end_timestamp": "00:37:42,896",
            "id": 199,
            "speaker": "Speaker 0",
            "start_timestamp": "00:37:28,907"
        },
        {
            "dialogue": "directed",
            "end_timestamp": "00:37:44,144",
            "id": 200,
            "speaker": "Speaker 2",
            "start_timestamp": "00:37:43,604"
        },
        {
            "dialogue": "and open-ended questions and then particularly from the open-ended",
            "end_timestamp": "00:37:49,126",
            "id": 201,
            "speaker": "Speaker 0",
            "start_timestamp": "00:37:44,164"
        },
        {
            "dialogue": "questions we encouraged them to type their answers and we got long answers and then from those very long answers we then put them all together",
            "end_timestamp": "00:38:00,329",
            "id": 202,
            "speaker": "Speaker 2",
            "start_timestamp": "00:37:49,166"
        },
        {
            "dialogue": "in one huge text file and then we went through it and we tried to pull out different common themes, like motivation, for example,",
            "end_timestamp": "00:38:10,324",
            "id": 203,
            "speaker": "Speaker 0",
            "start_timestamp": "00:38:00,349"
        },
        {
            "dialogue": "maybe",
            "end_timestamp": "00:38:10,865",
            "id": 204,
            "speaker": "Speaker 2",
            "start_timestamp": "00:38:10,364"
        },
        {
            "dialogue": "one motivation was grading, and students were motivated",
            "end_timestamp": "00:38:14,032",
            "id": 205,
            "speaker": "Speaker 0",
            "start_timestamp": "00:38:10,945"
        },
        {
            "dialogue": "by the grade that they wanted. Yeah, assessments.",
            "end_timestamp": "00:38:18,201",
            "id": 206,
            "speaker": "Speaker 2",
            "start_timestamp": "00:38:14,112"
        },
        {
            "dialogue": "There was a lot of mention about students were concerned about their grade.",
            "end_timestamp": "00:38:23,025",
            "id": 207,
            "speaker": "Speaker 0",
            "start_timestamp": "00:38:18,281"
        },
        {
            "dialogue": "So that came up quite a lot. So, you know, excluding this reference to a formalized achievement metrics such as course grade or GPA score. That was mentioned a lot because they were very worried about being online and how it would affect their GPA. So that was a common theme right across this group. That was a theme, and we looked for examples that fit with that theme.",
            "end_timestamp": "00:38:46,860",
            "id": 208,
            "speaker": "Speaker 2",
            "start_timestamp": "00:38:23,925"
        },
        {
            "dialogue": "In the end, we came up with five themes, or six themes.",
            "end_timestamp": "00:38:50,902",
            "id": 209,
            "speaker": "Speaker 0",
            "start_timestamp": "00:38:47,921"
        },
        {
            "dialogue": "Not five, that's four.",
            "end_timestamp": "00:38:55,564",
            "id": 210,
            "speaker": "Speaker 2",
            "start_timestamp": "00:38:52,042"
        },
        {
            "dialogue": "Okay, we cut it down to four. But I think if you want to have a look at the way we developed it, the analytical framework, that might help you think about how you're going to explain your your process. It might help you, I think it might.",
            "end_timestamp": "00:39:13,823",
            "id": 211,
            "speaker": "Speaker 0",
            "start_timestamp": "00:38:55,604"
        },
        {
            "dialogue": "About this, you mentioned you involved six PhD students? This was just the three of us. When I was in Singapore, before I came to Japan, we did research on, I was a teacher trainer, so what can I do? We'd get our students, which are BA pre-service teachers, and in the practicum, they would go out to schools and teach, practice. So, the schools we would go to is that we'd take video cameras and we could videotape the teachers teaching the kids, and the kids, you know, everything.",
            "end_timestamp": "00:39:52,240",
            "id": 212,
            "speaker": "Speaker 2",
            "start_timestamp": "00:39:15,704"
        },
        {
            "dialogue": "So everything was captured, professional mics hanging from the ceiling, good cameras, and then good audio pickups. Then they come back. and then those PhD students, they were doing a PhD in education. And they all had different theses to work on. But generally, their job, their paid job, was to transcribe and then basically Either A, they come up with their own coding scheme or B, they would use a Ministry of Education standardised coding scheme.",
            "end_timestamp": "00:40:34,899",
            "id": 213,
            "speaker": "Speaker 0",
            "start_timestamp": "00:39:52,300"
        },
        {
            "dialogue": "we prefer that they come up with their own coding scheme because they then did a lot more thematic analysis. If they use the standardised Ministry of Education coding scheme, then there's not much thinking going on, they're just looking for examples. Whereas to deep dive into the data, it's better for the student to come up with their own coding themes from the data. So when they're initially coding the data, it's up to them on how they interpret it at first?",
            "end_timestamp": "00:41:09,825",
            "id": 214,
            "speaker": "Speaker 2",
            "start_timestamp": "00:40:36,947"
        },
        {
            "dialogue": "It's up to them as they're going through it. See, when you're watching teachers teach, you may see things like, OK, maybe there's, say, three parts to a lesson.",
            "end_timestamp": "00:41:23,259",
            "id": 215,
            "speaker": "Speaker 0",
            "start_timestamp": "00:41:10,366"
        },
        {
            "dialogue": "There'll be a performance practice presentation.",
            "end_timestamp": "00:41:26,643",
            "id": 216,
            "speaker": "Speaker 2",
            "start_timestamp": "00:41:23,319"
        },
        {
            "dialogue": "There'll be a presentation.",
            "end_timestamp": "00:41:27,684",
            "id": 217,
            "speaker": "Speaker 0",
            "start_timestamp": "00:41:26,663"
        },
        {
            "dialogue": "the kids are practising something, then you've got performance, where the students then are performing to the teacher or to other students to display what they've learnt.",
            "end_timestamp": "00:41:43,522",
            "id": 218,
            "speaker": "Speaker 2",
            "start_timestamp": "00:41:30,917"
        },
        {
            "dialogue": "So you've got presentation, practice, performance.",
            "end_timestamp": "00:41:46,683",
            "id": 219,
            "speaker": "Speaker 0",
            "start_timestamp": "00:41:43,822"
        },
        {
            "dialogue": "And within those three parts of a lesson, things will be happening where the teacher may be presenting you to the PowerPoint, giving information, The teacher may ask a student a question.",
            "end_timestamp": "00:42:01,604",
            "id": 220,
            "speaker": "Speaker 2",
            "start_timestamp": "00:41:46,763"
        },
        {
            "dialogue": "The teacher may say, how many?",
            "end_timestamp": "00:42:05,426",
            "id": 221,
            "speaker": "Speaker 0",
            "start_timestamp": "00:42:01,624"
        },
        {
            "dialogue": "So we get group interaction.",
            "end_timestamp": "00:42:07,367",
            "id": 222,
            "speaker": "Speaker 2",
            "start_timestamp": "00:42:05,666"
        },
        {
            "dialogue": "One to one, what do you say? Or Jimmy, what do you say?",
            "end_timestamp": "00:42:11,369",
            "id": 223,
            "speaker": "Speaker 0",
            "start_timestamp": "00:42:08,088"
        },
        {
            "dialogue": "Jane, what do you think?",
            "end_timestamp": "00:42:12,690",
            "id": 224,
            "speaker": "Speaker 2",
            "start_timestamp": "00:42:11,549"
        },
        {
            "dialogue": "So it's one to one. What question? Is that right? What's the answer? Give me the answer. So you've got different, asks a question, demands an answer, makes a statement, what's the answer, give me an answer. It's very different. That's the way of teaching. Yeah, so you've got all these different ways of interacting with the kids as a presenter. Then you've got practice, what the students when they're practicing.",
            "end_timestamp": "00:42:42,394",
            "id": 225,
            "speaker": "Speaker 0",
            "start_timestamp": "00:42:13,010"
        },
        {
            "dialogue": "In the closed practice, maybe it's a worksheet that the kids are working on together or on their own. What's going on there? So lots and lots of things happening that the teachers can write little codes for in a lesson. And that's it.",
            "end_timestamp": "00:42:58,300",
            "id": 226,
            "speaker": "Speaker 2",
            "start_timestamp": "00:42:43,274"
        },
        {
            "dialogue": "And then they've determined from watching the video you know, the different codes and different actions. Then they get the transcript and they see how the transcript would fit these, and if they've got like twenty or thirty, can they narrow it down to say five or six?",
            "end_timestamp": "00:43:13,161",
            "id": 227,
            "speaker": "Speaker 0",
            "start_timestamp": "00:42:58,561"
        },
        {
            "dialogue": "So that's what coding does, we narrowed it down to four. But you can start off with a lot. So you could start off by looking at your transcripts and coming up with, let's say you've got forty answers, you could potentially have forty different codes.",
            "end_timestamp": "00:43:31,841",
            "id": 228,
            "speaker": "Speaker 2",
            "start_timestamp": "00:43:15,383"
        },
        {
            "dialogue": "But then you think away a bit. This answer, this answer, this answer is quite similar to a particular theme about, and then you could decide what that theme is.",
            "end_timestamp": "00:43:42,508",
            "id": 229,
            "speaker": "Speaker 0",
            "start_timestamp": "00:43:32,422"
        },
        {
            "dialogue": "And you say, OK, so that's one of my codes, those sorts, we could go there.",
            "end_timestamp": "00:43:46,911",
            "id": 230,
            "speaker": "Speaker 2",
            "start_timestamp": "00:43:42,528"
        },
        {
            "dialogue": "But what's he saying? What's he saying?",
            "end_timestamp": "00:43:48,532",
            "id": 231,
            "speaker": "Speaker 0",
            "start_timestamp": "00:43:46,991"
        },
        {
            "dialogue": "That's quite similar. What's that?",
            "end_timestamp": "00:43:51,774",
            "id": 232,
            "speaker": "Speaker 2",
            "start_timestamp": "00:43:49,432"
        },
        {
            "dialogue": "Is there a set number of times you have to define your themes?",
            "end_timestamp": "00:44:00,442",
            "id": 233,
            "speaker": "Speaker 1",
            "start_timestamp": "00:43:55,758"
        },
        {
            "dialogue": "I remember when I did this with... First of all, it was myself and Michiko.",
            "end_timestamp": "00:44:08,408",
            "id": 234,
            "speaker": "Speaker 0",
            "start_timestamp": "00:44:01,983"
        },
        {
            "dialogue": "We did it together. We did it.",
            "end_timestamp": "00:44:09,830",
            "id": 235,
            "speaker": "Speaker 2",
            "start_timestamp": "00:44:08,448"
        },
        {
            "dialogue": "We went through it three times.",
            "end_timestamp": "00:44:12,572",
            "id": 236,
            "speaker": "Speaker 0",
            "start_timestamp": "00:44:11,571"
        },
        {
            "dialogue": "And we were quite happy. Then we brought in our third researcher, which was the first author, Damien. He came in, then. Then he coded it his way and compared his...",
            "end_timestamp": "00:44:26,537",
            "id": 237,
            "speaker": "Speaker 2",
            "start_timestamp": "00:44:15,751"
        },
        {
            "dialogue": "So me and Richard compared with ourselves.",
            "end_timestamp": "00:44:28,378",
            "id": 238,
            "speaker": "Speaker 0",
            "start_timestamp": "00:44:26,817"
        },
        {
            "dialogue": "We did that three times, because we had too many. We wanted to narrow it down. We got it down to five.",
            "end_timestamp": "00:44:35,141",
            "id": 239,
            "speaker": "Speaker 2",
            "start_timestamp": "00:44:28,418"
        },
        {
            "dialogue": "Damien came in. He went through it. He came up with four themes. When we all three of us came together then, so that would be the one, two, seven, two, let's say we went through it. Let's say we went through the old text three or four times, we ended up with four themes. There's no hard and fast rule. and you've got to do it with at least one other person.",
            "end_timestamp": "00:45:02,943",
            "id": 240,
            "speaker": "Speaker 0",
            "start_timestamp": "00:44:35,702"
        },
        {
            "dialogue": "Oh, so a minimum of two people? You've got to have a minimum of two people, yeah, because you need that inter-reliability rate, because you can't depend on yourself, because then you're introducing bias.",
            "end_timestamp": "00:45:14,825",
            "id": 241,
            "speaker": "Speaker 2",
            "start_timestamp": "00:45:03,823"
        },
        {
            "dialogue": "Yeah, that's true. Every time I go back to the transcripts, I always come up with different codes and different themes each time.",
            "end_timestamp": "00:45:22,946",
            "id": 242,
            "speaker": "Speaker 1",
            "start_timestamp": "00:45:15,165"
        },
        {
            "dialogue": "But when you do it many times, you'll end up...",
            "end_timestamp": "00:45:25,427",
            "id": 243,
            "speaker": "Speaker 0",
            "start_timestamp": "00:45:23,826"
        },
        {
            "dialogue": "confirmatory bias.",
            "end_timestamp": "00:45:30,832",
            "id": 244,
            "speaker": "Speaker 2",
            "start_timestamp": "00:45:29,512"
        },
        {
            "dialogue": "In other words, you might be going back to something, and your bias might be confirming your original answer. But if you get somebody else looking at it, they say, what are you talking about?",
            "end_timestamp": "00:45:42,021",
            "id": 245,
            "speaker": "Speaker 0",
            "start_timestamp": "00:45:30,933"
        },
        {
            "dialogue": "That's not it. What's this?",
            "end_timestamp": "00:45:43,042",
            "id": 246,
            "speaker": "Speaker 2",
            "start_timestamp": "00:45:42,041"
        },
        {
            "dialogue": "And then you look at it three times, you then have this confirmatory bias, that you're confirming what you already think, you need to bring in a second person to overcome that.",
            "end_timestamp": "00:45:58,281",
            "id": 247,
            "speaker": "Speaker 0",
            "start_timestamp": "00:45:44,162"
        },
        {
            "dialogue": "So you need somebody else to, ideally, I don't know if you have time, but ideally you need another person to go through the text, to go through the process that you're going through. and then you come together and match them together, which is why, I don't know if you're doing this on your own, which is why it's really important to work together.",
            "end_timestamp": "00:46:20,430",
            "id": 248,
            "speaker": "Speaker 2",
            "start_timestamp": "00:46:00,542"
        },
        {
            "dialogue": "Ideally would it be like another PhD student? It'd be somebody working in the same area as you. You need somebody who's familiar with industrial design and design. And certainly another PhD student, absolutely. You need somebody of your level.",
            "end_timestamp": "00:46:45,660",
            "id": 249,
            "speaker": "Speaker 0",
            "start_timestamp": "00:46:22,172"
        },
        {
            "dialogue": "Or maybe somebody just finishing their Masters.",
            "end_timestamp": "00:46:51,882",
            "id": 250,
            "speaker": "Speaker 2",
            "start_timestamp": "00:46:48,621"
        },
        {
            "dialogue": "Would it be strange if we ask another faculty member?",
            "end_timestamp": "00:46:57,663",
            "id": 251,
            "speaker": "Speaker 1",
            "start_timestamp": "00:46:51,922"
        },
        {
            "dialogue": "Because I don't know any PhD students right now who are experts in this field. no but i wouldn't. i wouldn't bring",
            "end_timestamp": "00:47:06,470",
            "id": 252,
            "speaker": "Speaker 2",
            "start_timestamp": "00:46:57,703"
        },
        {
            "dialogue": "a faculty member into it because then",
            "end_timestamp": "00:47:08,594",
            "id": 253,
            "speaker": "Speaker 0",
            "start_timestamp": "00:47:06,530"
        },
        {
            "dialogue": "you've got the",
            "end_timestamp": "00:47:09,155",
            "id": 254,
            "speaker": "Speaker 2",
            "start_timestamp": "00:47:08,614"
        },
        {
            "dialogue": "You've got the hierarchical structure then, because then you can't disagree. Yeah, that's true.",
            "end_timestamp": "00:47:16,393",
            "id": 255,
            "speaker": "Speaker 1",
            "start_timestamp": "00:47:11,330"
        },
        {
            "dialogue": "You then have authority to bias. The authority will trump what you think. You can't argue about this. That is true. You need to find a friend.",
            "end_timestamp": "00:47:32,162",
            "id": 256,
            "speaker": "Speaker 2",
            "start_timestamp": "00:47:17,934"
        },
        {
            "dialogue": "A friend who's working in in design, user interface design, designer products, industrial design, product design. Somebody who's preferably an academic rather than a general designer from outside the industry, because they don't have the same thinking process. As an academic, you might be a designer, but you've got your academic head on for this.",
            "end_timestamp": "00:47:58,468",
            "id": 257,
            "speaker": "Speaker 0",
            "start_timestamp": "00:47:32,182"
        },
        {
            "dialogue": "And that's how you've got to approach it. So you've got preferably a lot of fellow If you've got time to do it.",
            "end_timestamp": "00:48:15,988",
            "id": 258,
            "speaker": "Speaker 2",
            "start_timestamp": "00:47:59,188"
        },
        {
            "dialogue": "I'm not saying it's a bad paper. I think it's a great paper. But I think if you've got time to enhance it, you could make it into a much better paper.",
            "end_timestamp": "00:48:23,610",
            "id": 259,
            "speaker": "Speaker 0",
            "start_timestamp": "00:48:16,148"
        },
        {
            "dialogue": "Thank you. Thank you for your comments. They're actually really awesome.",
            "end_timestamp": "00:48:26,910",
            "id": 260,
            "speaker": "Speaker 2",
            "start_timestamp": "00:48:24,050"
        },
        {
            "dialogue": "Two things I want to bring up. I've got to go. We've got ten minutes. You didn't reference, I'm not surprised anymore, but you know about this book?",
            "end_timestamp": "00:48:38,622",
            "id": 261,
            "speaker": "Speaker 0",
            "start_timestamp": "00:48:27,310"
        },
        {
            "dialogue": "Don Norman? I think I did. You did, yeah, because when you talk about the design process, there was no mention of the double diamond. I'm a big fan of the double diamond design process. Yeah.",
            "end_timestamp": "00:48:55,132",
            "id": 262,
            "speaker": "Speaker 2",
            "start_timestamp": "00:48:39,542"
        },
        {
            "dialogue": "The divergence.",
            "end_timestamp": "00:48:56,373",
            "id": 263,
            "speaker": "Speaker 1",
            "start_timestamp": "00:48:55,552"
        },
        {
            "dialogue": "Yeah, divergence converges, yeah. I didn't check your references but I'll be familiar with that.",
            "end_timestamp": "00:49:02,616",
            "id": 264,
            "speaker": "Speaker 2",
            "start_timestamp": "00:48:56,493"
        },
        {
            "dialogue": "The other one you said something about, you said something. either it's problematic or it's never been done before, you know when you're interviewing people about their design and interactions, that was kind of a limitation, people's design problems and challenges. and I'm surprised because If you were my student, you're not, but if you were my student, okay, I'd give you this book, and I'd say, take a look at all these UX, computer, software, and industrial product designers. These are interviews with lots and lots of people, okay, very short about their projects, and then here they talk about the challenges. And if you were my student, as part of your background, I'd get you to go through this, and for each one, I'd get you to tell me... Larry Tesla, Doug Engelbart, he invented the mouse.",
            "end_timestamp": "00:50:14,728",
            "id": 265,
            "speaker": "Speaker 0",
            "start_timestamp": "00:49:03,056"
        },
        {
            "dialogue": "Yeah. And I think also the Ethernet board.",
            "end_timestamp": "00:50:18,151",
            "id": 266,
            "speaker": "Speaker 2",
            "start_timestamp": "00:50:15,209"
        },
        {
            "dialogue": "McCain, oh yeah, the mouse.",
            "end_timestamp": "00:50:20,813",
            "id": 267,
            "speaker": "Speaker 0",
            "start_timestamp": "00:50:18,732"
        },
        {
            "dialogue": "Okay, what were his challenges?",
            "end_timestamp": "00:50:22,395",
            "id": 268,
            "speaker": "Speaker 2",
            "start_timestamp": "00:50:20,833"
        },
        {
            "dialogue": "Next slide. Bill Atkinson, he invented the Macintosh computer. What were his challenges? These are the famous people.",
            "end_timestamp": "00:50:34,805",
            "id": 269,
            "speaker": "Speaker 0",
            "start_timestamp": "00:50:24,316"
        },
        {
            "dialogue": "The Palm, the Palm pilot there, the Palm PDA.",
            "end_timestamp": "00:50:37,207",
            "id": 270,
            "speaker": "Speaker 2",
            "start_timestamp": "00:50:34,845"
        },
        {
            "dialogue": "What were their challenges?",
            "end_timestamp": "00:50:39,788",
            "id": 271,
            "speaker": "Speaker 0",
            "start_timestamp": "00:50:38,908"
        },
        {
            "dialogue": "So I get them to go through all these people, all these chapters, and just write down what challenges they had.",
            "end_timestamp": "00:50:47,251",
            "id": 272,
            "speaker": "Speaker 2",
            "start_timestamp": "00:50:39,968"
        },
        {
            "dialogue": "And I think that might help you provide a wider context to the challenges beyond the six, seven people that you interviewed. Because my guess is, my intuition, is that the challenges that your participants commented upon were probably commented upon in the seventies by these people who invented the mouse and the desktop and the Mac in the seventies, eighties and nineties. Because at the end of the day, the product design today The problems are probably no different to the problems that were designed thirty years ago. So, I'm not saying do it, I'm saying if you want",
            "end_timestamp": "00:51:31,873",
            "id": 273,
            "speaker": "Speaker 0",
            "start_timestamp": "00:50:47,271"
        },
        {
            "dialogue": "to, not for this, but if you want to, you know,",
            "end_timestamp": "00:51:34,393",
            "id": 274,
            "speaker": "Speaker 2",
            "start_timestamp": "00:51:31,913"
        },
        {
            "dialogue": "you're doing your doctorate, I think as part of your doctorate, to step away",
            "end_timestamp": "00:51:39,454",
            "id": 275,
            "speaker": "Speaker 0",
            "start_timestamp": "00:51:34,413"
        },
        {
            "dialogue": "and to look further afield,",
            "end_timestamp": "00:51:41,595",
            "id": 276,
            "speaker": "Speaker 2",
            "start_timestamp": "00:51:39,554"
        },
        {
            "dialogue": "I would suggest there needs to be a section in your paper, in your project, that introduces problems that have been",
            "end_timestamp": "00:51:51,865",
            "id": 277,
            "speaker": "Speaker 0",
            "start_timestamp": "00:51:42,555"
        },
        {
            "dialogue": "recognized by designers from overseas and what they are. Would it help if I also cite that textbook in this?",
            "end_timestamp": "00:52:04,091",
            "id": 278,
            "speaker": "Speaker 2",
            "start_timestamp": "00:51:51,925"
        },
        {
            "dialogue": "Well, I think what you'd have to do, I would say, Not for what you've done there, no, because I think you're being, there you're very specific about what you're doing. I'd say this is like a pilot study. I think this is an excellent pilot study, but for, it's a pilot study, but for your real research project, you need to widen the scope of your awareness of the literature and the problems beyond the seven students, the seven participants. I would suggest you need to go through something like this, you know you could search the internet but look it's all in one book, it's all there. So this is not for this, this is for your, like I said if I were your supervisor I would ask you to do that for your PhD writing.",
            "end_timestamp": "00:52:58,775",
            "id": 279,
            "speaker": "Speaker 0",
            "start_timestamp": "00:52:04,891"
        },
        {
            "dialogue": "There would have to be a section that would essentially be this.",
            "end_timestamp": "00:53:02,419",
            "id": 280,
            "speaker": "Speaker 2",
            "start_timestamp": "00:52:59,096"
        },
        {
            "dialogue": "Yeah, to get the bigger picture.",
            "end_timestamp": "00:53:05,891",
            "id": 281,
            "speaker": "Speaker 1",
            "start_timestamp": "00:53:03,649"
        },
        {
            "dialogue": "To get the bigger picture, yeah. Because when you get the bigger picture, this may put this into context. Or it may say that there are similarities, or they may say there are differences. And if there are differences, I think there's only two Japanese people in here. All these are mostly American, yeah? There's one guy, Japanese, Hiroshi Ishii, Maeda.",
            "end_timestamp": "00:53:33,314",
            "id": 282,
            "speaker": "Speaker 0",
            "start_timestamp": "00:53:06,252"
        },
        {
            "dialogue": "No, Maeda's not Japanese. Maeda's Japanese, but he's American Japanese. There's a guy who worked on the Apple company, Sakai.",
            "end_timestamp": "00:53:41,136",
            "id": 283,
            "speaker": "Speaker 2",
            "start_timestamp": "00:53:33,714"
        },
        {
            "dialogue": "Yeah, there's a few Japanese in it. Takeshi Natsuno.",
            "end_timestamp": "00:53:44,477",
            "id": 284,
            "speaker": "Speaker 0",
            "start_timestamp": "00:53:41,436"
        },
        {
            "dialogue": "There's quite a few Japanese in it. Oh, I didn't realize.",
            "end_timestamp": "00:53:46,318",
            "id": 285,
            "speaker": "Speaker 2",
            "start_timestamp": "00:53:44,497"
        },
        {
            "dialogue": "But I know on the Apple project in the '' the nineties, there was a couple of Japanese who bought it. What are the problems there? Could the problem be based on Filipino and one Japanese person's experience? Are these problems unique to the Filipinos? That's what I might say. You might say, OK, you've got more on Filipinos, so therefore it's not an international problem. It's a problem with designers in the Philippines, which is not true, I know. But the fact that you've only interviewed six Filipinos and one Japanese makes it kind of like, well, it's not a worldwide problem, is it? Doesn't sound like it. It sounds like it's just a Filipino-Japanese problem. Which is the criticism of all Western research, because the Western research comes out of America, therefore it's an American problem.",
            "end_timestamp": "00:54:43,307",
            "id": 286,
            "speaker": "Speaker 0",
            "start_timestamp": "00:53:46,758"
        },
        {
            "dialogue": "What's it going to do with us in Asia?",
            "end_timestamp": "00:54:44,629",
            "id": 287,
            "speaker": "Speaker 2",
            "start_timestamp": "00:54:43,347"
        },
        {
            "dialogue": "So if you want to generalise it more, then take something like this, which is multi-national, and come up with problems which then say, well actually the problems that these six Filipinos and one Japanese have are actually quite similar to the problems that all these multi-nationals have as well.",
            "end_timestamp": "00:55:03,978",
            "id": 288,
            "speaker": "Speaker 0",
            "start_timestamp": "00:54:46,692"
        },
        {
            "dialogue": "So their problems are not unique to the Philippines and Japan. I think what you're trying to say is that this could be a way to contribute to the challenges in a way that we're trying to address problems that are in Asia, outside the Western area? What you're doing is you're contextualizing.",
            "end_timestamp": "00:55:34,563",
            "id": 289,
            "speaker": "Speaker 2",
            "start_timestamp": "00:55:04,738"
        },
        {
            "dialogue": "You've got the problems which you've identified, which are applicable not only to designers in Asia and Japan, but applicable to designers worldwide, including Singapore, Malaysia, which are also part of Asia, but also America, Europe, Australia, and Africa. For example, which is why I think if you put it then in a broader context, this would provide that broader context. By connecting it to that. If there is a connection, yes, by connecting that, because there may not be a connection. After doing this, you might find that these problems are unique to Filipinos only.",
            "end_timestamp": "00:56:10,803",
            "id": 290,
            "speaker": "Speaker 0",
            "start_timestamp": "00:55:35,044"
        },
        {
            "dialogue": "Yes, that's true. At the moment, they are.",
            "end_timestamp": "00:56:13,465",
            "id": 291,
            "speaker": "Speaker 2",
            "start_timestamp": "00:56:11,184"
        },
        {
            "dialogue": "They are unique to those seven people, because you've only transcribed interviews from seven people. So they're not unique to me from England because I wasn't interviewed.",
            "end_timestamp": "00:56:27,753",
            "id": 292,
            "speaker": "Speaker 0",
            "start_timestamp": "00:56:14,786"
        },
        {
            "dialogue": "So how are you going to put that now into a more generalized context? What we have to do is either interview people from around the world, which is possible using the internet and creating Google Forms and contacting designers overseas and asking them to fill out your form. Yeah, that's possible. Get their nationality, get their gender, I guess. And, or, you know, take it from information that's readily available.",
            "end_timestamp": "00:56:57,455",
            "id": 293,
            "speaker": "Speaker 2",
            "start_timestamp": "00:56:27,873"
        },
        {
            "dialogue": "This book is in the library, I believe. This is mine, but this book is in the Farm Library. Do you have a phone?",
            "end_timestamp": "00:57:09,894",
            "id": 294,
            "speaker": "Speaker 0",
            "start_timestamp": "00:57:01,778"
        },
        {
            "dialogue": "You can take a picture of me if you want. Actually, I think I have a copy of that.",
            "end_timestamp": "00:57:15,037",
            "id": 295,
            "speaker": "Speaker 2",
            "start_timestamp": "00:57:09,914"
        },
        {
            "dialogue": "Yeah, it's quite famous, you know. These two are my two design bibles, you know.",
            "end_timestamp": "00:57:21,901",
            "id": 296,
            "speaker": "Speaker 0",
            "start_timestamp": "00:57:15,097"
        },
        {
            "dialogue": "Yeah. All right, got it. OK.",
            "end_timestamp": "00:57:25,082",
            "id": 297,
            "speaker": "Speaker 2",
            "start_timestamp": "00:57:21,941"
        },
        {
            "dialogue": "OK? Yeah. Great. It's two-thirty, I've got to go. I hope that was helpful for you. Like I say, I'm not being critical. I think it's really good. What I'm trying to do is give you information to make it much better.",
            "end_timestamp": "00:57:41,842",
            "id": 298,
            "speaker": "Speaker 0",
            "start_timestamp": "00:57:25,503"
        },
        {
            "dialogue": "Thank you, thank you. It was actually really helpful, especially with describing how you did the coding. Yeah, this is stuff that your supervisor should be telling you, but maybe they're not familiar with that.",
            "end_timestamp": "00:57:57,395",
            "id": 299,
            "speaker": "Speaker 2",
            "start_timestamp": "00:57:41,862"
        },
        {
            "dialogue": "which is why I printed that paper for you. But yeah, come back any time. Book another session, or if you want to chat to Kudo Sensei or Damien Rivers. I want to get a different perspective, because they are in different backgrounds to me. Please do so.",
            "end_timestamp": "00:58:16,638",
            "id": 300,
            "speaker": "Speaker 0",
            "start_timestamp": "00:57:58,342"
        },
        {
            "dialogue": "I'll book another session when you want to do this again. Yeah, got it.",
            "end_timestamp": "00:58:21,322",
            "id": 301,
            "speaker": "Speaker 2",
            "start_timestamp": "00:58:16,878"
        },
        {
            "dialogue": "Thank you very much. That's OK. Great. I enjoyed that.  ",
            "end_timestamp": "00:58:23,043",
            "id": 302,
            "speaker": "Speaker 0",
            "start_timestamp": "00:58:21,342"
        }
    ]
};
	// let feedback_list=[];
	let feedback_list= [
    {
        "id":1,
        "dialogue_id": 36,
        "done": false,
        "quote": "First of all, I think this is a very, very well-written paper, very logical, follows in terms of the way you conducted the process of this evaluation, what the limitations are, are some of the finer details of the project.",
        "speaker": "Speaker 0",
        "task": null,
        "type": "positive",
        "excerpt_reference": {
            "dialogue": "That is true. OK, so first of all, I will say, I made a comment here. <mark class=\"positive\" style=\"background-color:lightgreen;\">First of all, I think this is a very, very well-written paper, very logical, follows in terms of the way you conducted the process of this evaluation, what the limitations are, are some of the finer details of the project.</mark>",
            "end_timestamp": "00:06:44,556",
            "id": 36,
            "speaker": "Speaker 0",
            "start_timestamp": "00:06:12,364"
        }
    },
    {
        "id":2,
        "dialogue_id": 37,
        "done": false,
        "quote": "Your writing is actually very good, very logical, very, very good.",
        "speaker": "Speaker 2",
        "task": null,
        "type": "positive",
        "excerpt_reference": {
            "dialogue": "Not your writing. <mark class=\"positive\" style=\"background-color:lightgreen;\">Your writing is actually very good, very logical, very, very good.</mark>",
            "end_timestamp": "00:06:50,058",
            "id": 37,
            "speaker": "Speaker 2",
            "start_timestamp": "00:06:44,696"
        }
    },
    {
        "id":3,
        "dialogue_id": 38,
        "done": false,
        "quote": "I want to point out some points to you with some questions that you may be able to answer to make this a better paper.",
        "speaker": "Speaker 0",
        "task": null,
        "type": "critical",
        "excerpt_reference": {
            "dialogue": "So <mark class=\"critical\" style=\"background-color:lightcoral;\">I want to point out some points to you with some questions that you may be able to answer to make this a better paper.</mark>",
            "end_timestamp": "00:06:57,340",
            "id": 38,
            "speaker": "Speaker 0",
            "start_timestamp": "00:06:50,538"
        }
    },
    {
        "id":4,
        "dialogue_id": 41,
        "done": false,
        "quote": "I wouldn't put in a word like tedious, because it means then, well if it's tedious, don't do it.",
        "speaker": "Speaker 0",
        "task": null,
        "type": "critical",
        "excerpt_reference": {
            "dialogue": "But with a PDF, it's a bit problematic to do that, even though I've got Adobe Pro, Acrobat Pro, so I did it by pencil. So I tried to read my writing. a few, starting off with the very first line, okay, <mark class=\"critical\" style=\"background-color:lightcoral;\">I wouldn't put in a word like tedious, because it means then, well if it's tedious, don't do it.</mark>",
            "end_timestamp": "00:07:42,117",
            "id": 41,
            "speaker": "Speaker 2",
            "start_timestamp": "00:07:14,053"
        }
    },
    {
        "id":5,
        "dialogue_id": 42,
        "done": false,
        "quote": "If you think your job, or if you think a design life cycle is tedious, then maybe you're not the person to do it.",
        "speaker": "Speaker 0",
        "task": null,
        "type": "critical",
        "excerpt_reference": {
            "dialogue": "<mark class=\"critical\" style=\"background-color:lightcoral;\">If you think your job, or if you think a design life cycle is tedious, then maybe you're not the person to do it.</mark>",
            "end_timestamp": "00:07:52,113",
            "id": 42,
            "speaker": "Speaker 0",
            "start_timestamp": "00:07:43,798"
        }
    },
    {
        "id":6,
        "dialogue_id": 52,
        "done": false,
        "quote": "So why not say the product meets technical and safety specifications?",
        "speaker": "Speaker 0",
        "task": null,
        "type": "critical",
        "excerpt_reference": {
            "dialogue": "So carry loads and maybe specific guides are probably technical and safety specifications. So why not change that to that? Because it's kind of not in context with what you're saying before<mark class=\"critical\" style=\"background-color:lightcoral;\">So why not say the product meets technical and safety specifications?</mark>safety specifications. So why not change that to that? Because it's kind of not in context with what you're saying before.",
            "end_timestamp": "00:10:09,650",
            "id": 52,
            "speaker": "Speaker 0",
            "start_timestamp": "00:09:54,838"
        }
    },
    {
        "id":7,
        "dialogue_id": 54,
        "done": false,
        "quote": "So this is why I'm saying, you know, your writing is very, very good. Then you've got this word, out of expertise, knowledge, generalized. Generalized knowledge. Because, you know, if you've got expert knowledge and general knowledge and no knowledge. So this would be generalized knowledge. Because that person's not an expert, they've just got general knowledge.",
        "speaker": "Speaker 0",
        "task": null,
        "type": "critical",
        "excerpt_reference": {
            "dialogue": "Yeah, you're kind of being generalized there and specific there, suddenly. So if you make it generalized, you've probably got that phrase there. <mark class=\"critical\" style=\"background-color:lightcoral;\">So this is why I'm saying, you know, your writing is very, very good. Then you've got this word, out of expertise, knowledge, generalized. Generalized knowledge. Because, you know, if you've got expert knowledge and general knowledge and no knowledge. So this would be generalized knowledge. Because that person's not an expert, they've just got general knowledge.</mark>",
            "end_timestamp": "00:10:50,046",
            "id": 54,
            "speaker": "Speaker 0",
            "start_timestamp": "00:10:12,813"
        }
    },
    {
        "id":8,
        "dialogue_id": 64,
        "done": false,
        "quote": "So you come to me and go to your friends, yeah? So... Again, you then switch to... Ah, wait a minute. Okay, you've got the word... I've just changed the language a bit to make it a bit better. You've got verifying them, just say subsequent verification. Right, right. Just makes it sound better, okay? You've got stakeholders, then you've got users. So I put a question mark there.",
        "speaker": "Speaker 0",
        "task": null,
        "type": "critical",
        "excerpt_reference": {
            "dialogue": "<mark class=\"critical\" style=\"background-color:lightcoral;\">So you come to me and go to your friends, yeah? So... Again, you then switch to... Ah, wait a minute. Okay, you've got the word... I've just changed the language a bit to make it a bit better. You've got verifying them, just say subsequent verification. Right, right. Just makes it sound better, okay? You've got stakeholders, then you've got users. So I put a question mark there.</mark>",
            "end_timestamp": "00:14:14,028",
            "id": 64,
            "speaker": "Speaker 0",
            "start_timestamp": "00:13:42,661"
        }
    },
    {
        "id":9,
        "dialogue_id": 101,
        "done": false,
        "quote": "So when I read the rest of the paper, I'm looking for the answers to these two questions. That's all. And then you've got, You've got goals and aims. Again, asking for, requesting, same thing. I'm not sure. I'm sure I know what to say anymore.",
        "speaker": "Speaker 0",
        "task": null,
        "type": "critical",
        "excerpt_reference": {
            "dialogue": "You see what I mean? As a reader, I shouldn't do that. You've got to make it clear, one aim there, one aim there. <mark class=\"critical\" style=\"background-color:lightcoral;\">So when I read the rest of the paper, I'm looking for the answers to these two questions. That's all. And then you've got, You've got goals and aims. Again, asking for, requesting, same thing. I'm not sure. I'm sure I know what to say anymore.</mark>",
            "end_timestamp": "00:19:16,189",
            "id": 101,
            "speaker": "Speaker 0",
            "start_timestamp": "00:18:41,722"
        }
    },
    {
        "id":10,
        "dialogue_id": 118,
        "done": false,
        "quote": "So it's quite important to define. grounded theory is. It does two things. One, it tells the reader what it is, because the reader might not know. And two, it demonstrates that you know what it is as the writer. So just one sentence, grounded theory is, and the benefits of grounded theory are. So in other words, why grounded theory?",
        "speaker": "Speaker 0",
        "task": null,
        "type": "critical",
        "excerpt_reference": {
            "dialogue": "<mark class=\"critical\" style=\"background-color:lightcoral;\">So it's quite important to define. grounded theory is. It does two things. One, it tells the reader what it is, because the reader might not know. And two, it demonstrates that you know what it is as the writer. So just one sentence, grounded theory is, and the benefits of grounded theory are. So in other words, why grounded theory?</mark>",
            "end_timestamp": "00:21:31,036",
            "id": 118,
            "speaker": "Speaker 0",
            "start_timestamp": "00:21:05,791"
        }
    },
    {
        "id":11,
        "dialogue_id": 143,
        "done": false,
        "quote": "So you need to explain that before you move on to the results, because without that foundation of coding then everything else is unreliable. Even though when I read your scripts, it made sense and I can understand why you did it, but at the same time, when I read your conclusion and transcripts that support your conclusion, somebody in the audience may put their hand up and say that's bias. You may be biased. In other words, you are cherry picking. You are picking out information to suit your outcome. Whereas what you should be doing is looking at the information and from the information determine that outcome. But what you could be accused of here is that the outcome has already been decided by you subconsciously, but you've kind of looked for the transcripts to match that. I'm not saying you did that, but that's what you could be accused of. It's not a big accusation, of course, but it's just that somebody may take issue with that. So you don't have to change anything there. I think what you need to do is just justify how you've done this thematic analysis. Even if you keep everything else the same, that's fine. But when you do it, you may change.",
        "speaker": "Speaker 0",
        "task": null,
        "type": "critical",
        "excerpt_reference": {
            "dialogue": "So, we've done it, myself and two colleagues here have done it, we did it two years ago during the pandemic, and we called it thematic analysis, which is explain that process. so you can use our paper as an example of the process of coding and how we came up, because we did something similar. <mark class=\"critical\" style=\"background-color:lightcoral;\">So you need to explain that before you move on to the results, because without that foundation of coding then everything else is unreliable. Even though when I read your scripts, it made sense and I can understand why you did it, but at the same time, when I read your conclusion and transcripts that support your conclusion, somebody in the audience may put their hand up and say that's bias. You may be biased. In other words, you are cherry picking. You are picking out information to suit your outcome. Whereas what you should be doing is looking at the information and from the information determine that outcome. But what you could be accused of here is that the outcome has already been decided by you subconsciously, but you've kind of looked for the transcripts to match that. I'm not saying you did that, but that's what you could be accused of. It's not a big accusation, of course, but it's just that somebody may take issue with that. So you don't have to change anything there. I think what you need to do is just justify how you've done this thematic analysis. Even if you keep everything else the same, that's fine. But when you do it, you may change.</mark>",
            "end_timestamp": "00:26:58,041",
            "id": 143,
            "speaker": "Speaker 0",
            "start_timestamp": "00:25:03,509"
        }
    },
    {
        "id":12,
        "dialogue_id": 144,
        "done": false,
        "quote": "I don't think you'll change, because I think your discussion is actually very focused and very good.",
        "speaker": "Speaker 2",
        "task": null,
        "type": "positive",
        "excerpt_reference": {
            "dialogue": "<mark class=\"positive\" style=\"background-color:lightgreen;\">I don't think you'll change, because I think your discussion is actually very focused and very good.</mark>",
            "end_timestamp": "00:27:02,125",
            "id": 144,
            "speaker": "Speaker 2",
            "start_timestamp": "00:26:58,081"
        }
    },
    {
        "id":13,
        "dialogue_id": 149,
        "done": false,
        "quote": "Yeah, and then, okay, your results. you know, your discussion, it's all very good, sorry, the overview of the results is all very good, and then when it came to the discussion I think this is what you've got to decide yourself.",
        "speaker": "Speaker 0",
        "task": null,
        "type": "positive",
        "excerpt_reference": {
            "dialogue": "you know, your discussion, it's all very good, sorry, the overview of the results is all very good, and then when it came to the discussion I think this is what you've got to decide yourself<mark class=\"positive\" style=\"background-color:lightgreen;\">Yeah, and then, okay, your results. you know, your discussion, it's all very good, sorry, the overview of the results is all very good, and then when it came to the discussion I think this is what you've got to decide yourself.</mark>",
            "end_timestamp": "00:28:08,795",
            "id": 149,
            "speaker": "Speaker 0",
            "start_timestamp": "00:27:54,744"
        }
    },
    {   
        "id":14,
        "dialogue_id": 150,
        "done": false,
        "quote": "In your discussion you said the aim of the study. But in the previous section there were two aims. So I actually personally, I like the fact that you've got it written down as one aim. You've connected the two into one. I like that. And I think it makes it more focused.",
        "speaker": "Speaker 0",
        "task": null,
        "type": "positive",
        "excerpt_reference": {
            "dialogue": "<mark class=\"positive\" style=\"background-color:lightgreen;\">In your discussion you said the aim of the study. But in the previous section there were two aims. So I actually personally, I like the fact that you've got it written down as one aim. You've connected the two into one. I like that. And I think it makes it more focused.</mark>",
            "end_timestamp": "00:28:28,774",
            "id": 150,
            "speaker": "Speaker 2",
            "start_timestamp": "00:28:09,015"
        }
    },
    {   
        "id":15,
        "dialogue_id": 259,
        "done": false,
        "quote": "I'm not saying it's a bad paper. I think it's a great paper. But I think if you've got time to enhance it, you could make it into a much better paper.",
        "speaker": "Speaker 0",
        "task": null,
        "type": "positive",
        "excerpt_reference": {
            "dialogue": "<mark class=\"positive\" style=\"background-color:lightgreen;\">I'm not saying it's a bad paper. I think it's a great paper. But I think if you've got time to enhance it, you could make it into a much better paper.</mark>",
            "end_timestamp": "00:48:23,610",
            "id": 259,
            "speaker": "Speaker 0",
            "start_timestamp": "00:48:16,148"
        }
    },
    {   
        "id":16,
        "dialogue_id": 279,
        "done": false,
        "quote": "I think this is an excellent pilot study, but for, it's a pilot study, but for your real research project, you need to widen the scope of your awareness of the literature and the problems beyond the seven students, the seven participants.",
        "speaker": "Speaker 0",
        "task": null,
        "type": "critical",
        "excerpt_reference": {
            "dialogue": "Well, I think what you'd have to do, I would say, Not for what you've done there, no, because I think you're being, there you're very specific about what you're doing. I'd say this is like a pilot study. <mark class=\"critical\" style=\"background-color:lightcoral;\">I think this is an excellent pilot study, but for, it's a pilot study, but for your real research project, you need to widen the scope of your awareness of the literature and the problems beyond the seven students, the seven participants.</mark> I would suggest you need to go through something like this, you know you could search the internet but look it's all in one book, it's all there. So this is not for this, this is for your, like I said if I were your supervisor I would ask you to do that for your PhD writing.",
            "end_timestamp": "00:52:58,775",
            "id": 279,
            "speaker": "Speaker 0",
            "start_timestamp": "00:52:04,891"
        }
    },
    {
        "id":17,
        "dialogue_id": 298,
        "done": false,
        "quote": "What I'm trying to do is give you information to make it much better.",
        "speaker": "Speaker 0",
        "task": null,
        "type": "critical",
        "excerpt_reference": {
            "dialogue": "OK? Yeah. Great. It's two-thirty, I've got to go. I hope that was helpful for you. Like I say, I'm not being critical. I think it's really good. <mark class=\"critical\" style=\"background-color:lightcoral;\">What I'm trying to do is give you information to make it much better.</mark>",
            "end_timestamp": "00:57:41,842",
            "id": 298,
            "speaker": "Speaker 0",
            "start_timestamp": "00:57:25,503"
        }
    }
];
	

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

