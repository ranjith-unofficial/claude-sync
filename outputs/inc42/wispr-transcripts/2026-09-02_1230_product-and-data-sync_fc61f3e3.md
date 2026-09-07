# Product & Data Sync

- Wispr meeting id: fc61f3e3-643c-412f-a59a-0385cf4e46ab
- Start: 2026-09-02 12:30 IST (07:00Z) · End: 13:00 IST
- Attendees (calendar): Ashish Sharma, Prapti Rastogi, Ranjith M, Utkarsh Agarwal (organizer)
- Share link: https://notes.wisprflow.ai/shared/wlZ1q5l_KDmUhlhbL55SewhRr-t1t6u7oVDRCu-FgaU
- Archived from Wispr Flow via MCP on 2026-09-08. Transcript is verbatim ASR output; speaker labels are Wispr's and are sometimes mis-assigned.

## Wispr summary
Team reviewed the MOP status: dunning/winback went live and is in testing, analytics user-property unification is the next focus, and QIA definition needs locking. Sprint planning and documentation to close this week.

### Dunning & Events Status
- Dunning and winback went live yesterday; Ranjith M testing with Bhavik and Anmol
- Winback creates a ₹10 order solely for mandate registration when user cancels externally
- Payment-related events fully implemented across renewal journey and states

### Analytics Unification (One Inc42)
- Priority: audit existing events work correctly, then streamline user properties across Inc42, data labs, app
- Events not being modified (backfill gap risk); only user properties unified for warehouse/reverse ETL
    - Adding/removing events is a later, additional requirement
- Analytics work must consolidate and close within one week

### QIA Definition
- Students clearly excluded; service providers debatable given volume and paying-audience potential
- Seniority definition tricky: flat 'senior manager+' vs company-type-weighted (e.g. analysts valuable for DL)
- Ranjith M to sync with Prapti Rastogi, loop in Ashish Sharma, close definition in coming days

### Warehouse & Other Workstreams
- Prapti Rastogi progressing on external enrichment, reverse ETL SOW, Ask Query Q&A tests, Bootstrap Companies enrichment
- Server-side phase-2 optimization: Inc42 auto scale-up and VM merging kicking off today
- Cap-table dataset opens valuation and investor ticket-size unlocks; explore app use cases first

### Next Steps
- (Utkarsh Agarwal) Review the reorganized MOP in parallel while sprint plan is drafted
- (Utkarsh Agarwal) Hand over Inc42 base documentation so team can pick it up
- (Ashish Sharma) Add dunning/data-library documentation to PRD and share for review
- (Ashish Sharma) Kick off server-side phase-2: Inc42 auto scale-up and VM merging
- (Ranjith M) Close events documentation today and share audit-validated user-properties doc
- (Ranjith M) Draft high-level sprint plan, review with Prapti Rastogi and Ashish Sharma, then share with Utkarsh Agarwal
- (Ranjith M) Finalize two screen designs with Satya and share
- (Prapti Rastogi) Evaluate QIA definitions against internal use cases and flag needed changes

## Transcript
Ranjith M: Karnaapi.
Utkarsh Agarwal:  Karnauna? You're asking—
Ranjith M:  MOP, point of view से जो हमारे पास टास्क थे, उसमें हमारे पास main था "डनिंग सिस्टम" वाला पार्ट। तो वो डनिंग और विनबैक सब हमने लाइव कर दिया है कल। So उसपे हम टेस्टिंग वाला पार्ट हमने आज से स्टार्ट कर दिया है।
Ranjith M:  तो मैंने भाविक और अनमोल को इस चीज़ के लिए कर दिया। मैं भी पूरे फ्लोज़ टेस्ट कर रहा हूँ।
Ranjith M:  तो based upon that, हम— मतलब, इसको फिर आगे forward कर सकते हैं, जो भी हमें मेल्स और— मतलब, extra चीज़ें जो करनी थीं।
Utkarsh Agarwal:  समझ गया। एक बार उसका अगर जिस तरह से हमने implement किया, जैसे हम बात कर रहे थे, वो डेटा लाइब्रेरी, उसमें PRD में एक बार वो documentation उसकी भी add कर देना। एक बार मैं वो— मैं भी एक बार वो review कर लूँगा।
Utkarsh Agarwal:  वो add करके एक बार share कर देना, ताकि एक बार वो review कर लें।
Ranjith M:  ठीक है, उद्गश।
Utkarsh Agarwal:  डनिंग से भी हमारे coverage में I think दो-तीन points थे। उसमें अभी क्या-क्या चीज़ें cover हो गईं? डनिंग point of view से?
Ranjith M:  So, उत्कर्ष, basically हमने इसमें जो cover कर लिया है, एक तो डनिंग सिस्टम, जहाँ पे जो भी हमारा failure आएँगे, उसमें हम directly without any login— हम directly payment receive भी कर सकते हैं। So उनके links जो उनको मिलेंगे, जो events के through जा रहे हैं, उसमें directly वो user directly pay कर सकता है, without any login।
Utkarsh Agarwal:  और ये links जो generate हो रहे हैं, ये फिर अभी कहाँ store हो रहे हैं? कैसे हम उसको pass कर रहे हैं?
Ranjith M:  ये— ये उत्कर्ष, सारे payment links हैं। तो जो— जो भी हमारे order का payment link बनेगा, वही हमारे use होगा। अब इसमें जो एक वो condition है, winback वाली, जिसमें वो user cancel कर देता है externally, कोई mandate अपना, तो उस वाले case में हम एक random— एक— एक order बना रहे हैं, जिसको हम winback order कह रहे हैं।
Ranjith M:  उसमें वो 10 rupee का order है, जिसमें वो केवल mandate registration के लिए काम में आएगा।
Utkarsh Agarwal:  समझ गया।
Ranjith M:  And वो basically directly link बन जाएगा आपके subscription से। तो आपका जो भी mandate— mandate updation वाला part चलेगा, वो उसके through चलेगा।
Utkarsh Agarwal:  समझ गया।
Ranjith M:  So, उत्कर्ष, इसमें basically हमने जो हमारे दो से तीन use case थे, कि user हमारे पास renewals नहीं कर रहे हैं, and हमारे पास उनकी states नहीं आ रही हैं, हमें पता नहीं पड़ता है। तो उस वाले case में हम ये links भेज सकते हैं, जिससे directly हम payment receive कर लेंगे।
Utkarsh Agarwal:  समझ गया।
Ranjith M:  हाँ। And इसमें जो भी हमारे events regarding— हमारे implementation था, जो आपने— भाविक ने बनाया था, वो वाला part भी हमने implement कर दिया पूरा।
Utkarsh Agarwal:  समझ गया।
Ranjith M:  Yes.
Utkarsh Agarwal:  अभी events वाले में सिर्फ वो वाले थे?
Ranjith M:  सिर्फ payments वाले।
Utkarsh Agarwal:  अभी हुए हैं या सारे हुए?
Ranjith M:  नहीं, उत्कर्ष, वो उसमें सारे— basically हमने payments वाले जो आपने सारे states जो बनाई थीं, जो आपने, मैंने, और अनमोल ने discuss किया था।
Utkarsh Agarwal:  Right, right, वो वाले सारे हुए।
Ranjith M:  वो— वो सारा हो गया, yes। वो पूरा flow पूरा ready हो गया है, कि from starting a journey से लेके payment states, multiple states, उसके पर renewal में जितनी भी states manage होंगी, user props manage होंगे।
Utkarsh Agarwal:  समझ गया।
Ranjith M:  वो पूरा journey पूरा बन गया है।
Ranjith M:  Hello? I think—
Utkarsh Agarwal:  Hello? Sorry—
Ranjith M:  हाँ, उत्कर्ष।
Utkarsh Agarwal:  हाँ, उत्कर्ष। तो डनिंग वाले हमारे हो गए हैं, ये basic हमारा, और events ये वाले हमारे हो गए हैं। 
Utkarsh Agarwal: ठीक है। रंजीत, are you— मतलब, for these events, this is there in your master sheet also, right?
Ranjith M:  Right, right, right, उत्कर्ष।
Utkarsh Agarwal:  ठीक है। So उसका testing and status एक बार उसमें we can test and map it there कि हाँ, these are working। So that is one.
Utkarsh Agarwal:  And डनिंग वाला, okay, फिर आशीष, documentation एक बार add कर देना, वो भी फिर भाविक के साथ मिलके, रंजीत and आशीष, फिर एक बार test करके इन दोनों points को भी close करते हैं। फिर बचा हुआ हमारा जो analytics का जो बचे हुए points हैं, then that is something we have to map out next week, right?
Ranjith M:  Yes. हाँ, additional event and properties जो हमने बस हमने extra add करे। I think properties ही हैं जो हमें map करनी हैं extra।
Ashish Sharma:  Right। रंजीत, so अभी in context of this, अभी how are we approaching the analytics वाला point?
Ranjith M:  So right now, उत्कर्ष, if you remember, we were discussing that whatever the new events which are being introduced for data labs onboarding payment, these are the two new set of events which have been recently introduced. We'll try to unify that. That is the very first step, because it is already tested on data labs, so it can be replicated on Inc42.
Ranjith M:  Second, when I just talk about events, I have figured out there are a lot of mis-user properties which have been circulated differently for data labs and media, which could be unified.
Utkarsh Agarwal:  Right.
Ranjith M:  For which also I've created a documentation. These are more from implementation— I mean, implementation point of view, say. It can be picked up.
Ranjith M:  I'll share this document also right after this call. I will just— I've run the audit yesterday or night also, just to validate this, so that I can share the relevant one.
Ranjith M:  मुझे इसमें I have some confidence that these are the user properties which need to be combined. I'll share the document with everyone.
Ranjith M:  This is the two primary approach we will take for now, then followed by, once we have entire data, Prapti can take it up. And anyway, I believe she is already working on reverse ETL.
Ranjith M:  So as part of one Inc42, we can continue this.
Utkarsh Agarwal:  Got it. नहीं, तो ठीक है। So इसमें two parts।
Utkarsh Agarwal:  One is— one is the conversation we had, रंजीत, separately on the MOP में। The बाकी stuff we talked about, how do we organize them better।
Utkarsh Agarwal:  So one thing that we have to close today is that, if you remember, the one Inc42 thing that we discussed, one Inc42 data labs का scope we had simplified for this month, and how are we looking at all the buckets together, right?
Ranjith M:  Right.
Utkarsh Agarwal:  So can we finalize— duplicate that MOP sheet and let's finalize those changes and lock that today? One part is that. And second is, then in terms of the mapping for the next— like we were talking about the sprint mapping.
Utkarsh Agarwal:  So now, what are we prioritizing and in which order are we picking, you know, the analytics and the app? These two are the main big things that are happening in parallel.
Ranjith M:  Right, right, उत्कर्ष।
Utkarsh Agarwal:  So इसमें then we need to map out the timelines and the approach that we're taking for both of these things. Because analytics वाला part has been going on for almost one and a half months now, मतलब, in different forms and shapes. So now I think we need to finally consolidate and close it in the next one week at max.
Ranjith M:  हाँ। नहीं, वैसे it's consolidated, but you're talking about implementation also?
Utkarsh Agarwal:  हाँ, हाँ।
Ranjith M:  Yes. Okay, got it.
Utkarsh Agarwal:  मतलब, जो भी उसमें final changes agree करके, whatever has to be done across data labs and Inc42 both, and that along with the audit system. All of that we need to close now in the next one week, because it's been going on for a while, and the longer that it takes, the longer that the data correction also takes for it to happen.
Ranjith M:  हाँ, right। Here, are we also— okay, just to get more clarity, are we just trying to talk that whatever events are going to the respective platform, those are similar, and those are getting triggered properly? There are no duplicate events, there are no additional events, or there are no such thing happening?
Ranjith M:  This is one. Are we just talking about this, or are we also talking about either combining all those few certain events to one single workspace, or stitching them across every workspace?
Ranjith M:  Are we talking about this method?
Utkarsh Agarwal:  Not the latter. The first part only, but with the additional caveat of user properties being synonymous across all three.
Ranjith M:  Okay. Prapti, you have—
Utkarsh Agarwal:  Events we are not— events we are not changing, like we discussed, because modifying the events will create an issue of backfill का gap. Like, the historical data will be in a different event format, and the new format will be different. So we are retaining the same event format for Inc42, for data labs, for app.
Utkarsh Agarwal:  Nothing changes in the event and event properties. For user properties, that is the thing that we are streamlining across all three, because that is the only way the data warehouse will work correctly.
Utkarsh Agarwal:  If the— if the properties are the same, that is how everything will sync correctly across all three.
Ranjith M:  Got it.
Utkarsh Agarwal:  Right?
Ranjith M:  Yes.
Utkarsh Agarwal:  इसमें कोई doubts किसी के? या any other inputs? मतलब, कुछ miss कर रहा हूँ अगर?
Ranjith M:  नहीं, उत्कर्ष, makes sense। मतलब, हाँ, मतलब, user props वाले part पे, yes, हम align कर लेंगे इसमें। And unification— unified जो properties हैं, उनमें agreement कर लेंगे, yes।
Utkarsh Agarwal:  Because you— sprint properties point of view से, we just need to do the audit। कि—
Ranjith M:  Right, audit and make sure कि everything is working correctly and is implemented correctly। फिर उसके बाद, मतलब, additionally, अगर उसमें कुछ remove करना है, कोई events add करने हैं या remove करने हैं, वो— that's a additional point। But fundamentally, तो पहले अभी जो mapped है in the master analytics sheet, everything— वो उस point of view से, everything सही चल— is working correctly or not, that is the first objective।
Ranjith M:  Second is the user properties का streamlining across all three, so that they are synonymous and our data warehouse can work on top of that।
Utkarsh Agarwal:  Got it।
Ranjith M:  Third would be if we want to now add or remove any events from either of Inc42 or data labs।
Utkarsh Agarwal:  Got it।
Ranjith M:  Got it।
Utkarsh Agarwal:  Because addition removing will require our one Inc42 वाला approach कि हाँ, मतलब, additionally, we are doing some additional things, or we want some additional events or properties that we need. That is our additional requirement। But अभी what is already mapped, ensuring that user properties are correct, so that reverse ETL and data warehouse can work।
Utkarsh Agarwal:  These are the immediate objectives।
Ranjith M:  Right। हाँ। So I was supposed to close the document for events yesterday, but— उत्कर्ष, आपको तो पता है, we— now the developer is blocked on design।
Ranjith M:  So I thought I'll spend some more time with Satya in terms of getting the initial few drafts of design, so that developers are not blocked।
Utkarsh Agarwal:  Right।
Ranjith M:  So that is why the focus has been shifted— was shifted to design, slightly more on design। But right now, we have few drafts screen. I believe today we'll have almost finalized version we'll discuss with you.
Ranjith M:  But हाँ, that was the aim that it got slightly— I'd reprioritize events slightly so that now the— like, everything is blocked on design, so that is the only reason. But हाँ, तो we'll try to close it today, events part.
Ranjith M:  At least the high level of documentation and share it with you.
Utkarsh Agarwal:  Right। So उसका documentation and this MOP का mapping, मतलब, the bucket changes, and then based on that, once we've logged that, then the plan for at least next two weeks कि what are we picking। चाहे अभी detailed mapping can be done in one or two days, that's fine, but at least broad plan कि next two weeks में what all things are we covering in which order।
Utkarsh Agarwal:  Because multiple buckets चल रही हैं, and that now needs to be streamlined।
Ranjith M:  Got it।
Utkarsh Agarwal:  तो सब लोग multiple चीज़ों पे काम कर रहे हैं।
Ranjith M:  हाँ, that— that makes sense, उत्कर्ष। So I have created the MOP, and have had a high-level discussion with Prapti and Ashish। With Ashish को I had a little in-depth— detailed discussion.
Ranjith M:  Prapti को I had a very brief discussion, where I've created three buckets every— and I limited the bucket three of data labs only to retention and the dunking system which we discussed. Bucket one, bucket two is what we already discussed.
Ranjith M:  It's just structured in more— in a better way. But like you said, this— this anyways exists.
Ranjith M:  If we can— if you want to go through and discuss, that can also be done. If you want to discuss this, can— can be done.
Ranjith M:  Or if we want to discuss along with the weekly plans— I mean, or the sprint plan, we can do that also.
Utkarsh Agarwal:  हाँ, so go ahead with the sprint plan। I'll— I'll also parallelly go through this and see if there are any changes or anything that I want to add or remove. That we— I'll do parallelly।
Utkarsh Agarwal:  Meanwhile, go ahead with the— I think broadly, I think since the buckets are same, मतलब, we just reorganize from the existing MOP. So principally, that's fine.
Utkarsh Agarwal:  Go ahead with the making the weekly plan so that we can do that in parallel. Meanwhile, I'll go through this, then we'll sit and close both together.
Ranjith M:  Got it। Done, उत्कर्ष।
Utkarsh Agarwal:  ठीक है। We'll— let's aim to close all of it today only।
Ranjith M:  All of this one is event documentation. Second is MOP closure। I mean, MOP closure also includes sprint close— I mean, sprint planning।
Utkarsh Agarwal:  Right।
Ranjith M:  हाँ। So I'll create a high-level sprint planning. I'll discuss with Prapti and Ashish and see if— if— if planning is correct, then I'll share it with you, then we can take a final call।
Utkarsh Agarwal:  ठीक है। Done।
Ranjith M:  हाँ। ठीक है, done है।
Utkarsh Agarwal:  ठीक है। So this is that। हाँ, फिर आशीष, और कोई points अभी?
Ranjith M:  नहीं, उत्कर्ष। बाकी का तो ये points नहीं हैं। So बाकी का जो phase two वाला जो optimization on the server side का एक part है, वो वाला part मैं start करवा दूँगा।
Ranjith M:  आज मैं call server team के साथ call है, जिसमें हम Inc42 auto scale up वाला part and जो other सारे और VMs को merging वाला part था, उसपे मैं activity start करवाऊँगा।
Utkarsh Agarwal:  Right।
Ranjith M:  Yes.
Utkarsh Agarwal:  समझ गया। ठीक है, ये एक और हो गया। और कुछ हमारा बचा नहीं।
Utkarsh Agarwal:  I think basically यही points थे हमारे। 
Utkarsh Agarwal: ठीक है। Inc42 वाला, मुझे बस एक बार वो documentation handover करनी है। फिर वहाँ से हम उसको pick कर सकते हैं।
Ranjith M:  हाँ, exactly।
Utkarsh Agarwal:  Base तो I think अब वो stabilize हो गया है। अब बाकी उसके बाद का roadmap, फिर हम बाद में अलग से एक बार discuss कर सकते हैं। अभी priority पे नहीं है वो।
Utkarsh Agarwal:  But हाँ, उसके आगे हम रंजीत और तुम्हारे साथ एक बार बैठ के, फिर पहले अभी core MOP lock— मतलब, अभी sprint plans lock हो जाएँ, उसके बाद फिर देखते हैं कि उसके बाद अगर कहीं space है और priority के point of view से एक बार देखना पड़ेगा कि उसपे अभी हम और कितना काम कर रहे हैं या नहीं कर रहे हैं। But हाँ, अभी के लिए base stabilization हो चुका है उसका।
Utkarsh Agarwal:  वापस जो भी issues थे, mostly सारे हो गए हैं। कुछ अगर छोटा-मोटा होगा तो at max हो।
Utkarsh Agarwal:  बाकी improvement तो फिर वो एक अलग discussion है, वो अलग से।
Ranjith M:  Exactly। Yes।
Utkarsh Agarwal:  ठीक है। ठीक है। 
Utkarsh Agarwal: ठीक है, next फिर Prapti। Blockers या कोई immediate points?
Prapti Rastogi:  उत्कर्ष, blockers warehouse point of view से था मेरा एक point। तो अभी warehouse point of view से, एक तो मैं external enrichment plan कर रही हूँ, और दूसरा reverse ETL की planning हमारी throughout, मतलब अभी month में कैसी रहेगी, उसका मैं एक बार ये broader SOW बना रही हूँ। इसके अलावा मेरा ना एक QIA पे question था, उत्कर्ष, कि अभी are we taking company type also in QIA?
Utkarsh Agarwal:  Yes।
Prapti Rastogi:  उत्कर्ष, इसमें मतलब एक broader question था कि मतलब for example हम कह रहे हैं कि service providers and students हम exclude कर रहे हैं QIA में से। तो अगर मैं data labs की बात करूँ या app की बात करूँ, तो does it make sense कि हम वहाँ से उनको exclude करें, इस— मतलब इस user type को?
Utkarsh Agarwal:  नहीं। Service providers I would agree is a debatable point। Students not।
Utkarsh Agarwal:  Students तो definitely exclude होने चाहिए। Service provider is the— is the point जहाँ पर वो थोड़ा सा debatable हो जाता है, क्योंकि while technically वो हमारी in— readership point of view से वैसे core नहीं है, but at the same time है भी।
Utkarsh Agarwal:  क्योंकि उसका volume अच्छा खासा है। And जैसे अभी मैं app का data भी देख रहा था, तो I think decent volume अभी other persona choose कर रहा है।
Utkarsh Agarwal:  और most likely जो अभी initial— मतलब उसका enrichment एक बार देख सकते हैं कि अगर उसका— अब वैसे तो personal emails हैं, पर उसको अभी one time enrich करके देख सकते हैं behavior app के analysis के लिए भी। But उसमें उनका user behavior point of view से engagement levels भी काफी अच्छे हैं, the other persona के।
Utkarsh Agarwal:  And तो वो— वो service provider becomes the tricky point, जो हम maybe include कर सकते हैं। क्योंकि वो— वो— वो हम एक बार मिलके debate करके उसको lock कर सकते हैं।
Utkarsh Agarwal:  क्योंकि service provider में वो benefit है कि हाँ, वो हमारा— technically वो audience है भी, क्योंकि वो हमें पड़ती है startups ढूँढने के लिए। वो technically paying audience भी बनेगी, अगर कोई membership या subscription आता है।
Utkarsh Agarwal:  And technically वो sponsor और वो वाली चीज़ें भी करती है events में और IPs में।
Prapti Rastogi:  Correct। Correct।
Ranjith M:  तो इसलिए मुझे भी ये doubt था। दूसरा, उत्कर्ष, एक seniority पे भी मुझे लग रहा है। For example, अब जैसे अगर मैं DL के lens से बात करूँ, उत्कर्ष, तो there are a lot of analyst वाले लोग, जो काफी अच्छा quotient, मतलब, use करता है जो हमारा DL।
Ranjith M:  वो ये analyst level के people भी होते हैं। तो क्या हमें, मतलब, DL specific अलग QIA या फिर, मतलब, मैं वैसे सोच रही थी कि अगर— अगर मैं broader sense में QIA को देख रही हूँ, तो फिर मेरे ये जो analyst level people हैं, वो are not for DL and all।
Ranjith M:  तो ये तो exclude हो जाते हैं उसमें से। But जो कि मेरे लिए एक अच्छी audience है, अगर मैं DL के perspective से बात करूँ।
Ranjith M:  But अगर मैं events के perspective से बात करूँ, तो नहीं है।
Ranjith M:  Right।
Utkarsh Agarwal:  तो उसमें तभी वो company type का usability was the use case। कि अभी flat definition simpler रखने के लिए senior manager and above— for example, अगर मैं company type का weightage नहीं लाता हूँ, तो senior manager and above flat works to some extent। Company type के basis पे then we can have different seniority levels, depending on कि अगर वो investor है, तो उसमें seniority levels का requirement changes।
Utkarsh Agarwal:  But non-investor है तो अलग है। तो ये अभी definition level पे ये है।
Utkarsh Agarwal:  अब इसको practical level पे हम इसको actually implement— जो रंजीत was also flagging कि हाँ, मतलब, in terms of complication, this will become a little complicated। तो अब इसको— इस definition को realistic कैसे करें, और ये जो caveats हम edge cases की बात कर रहे हैं, उसको कैसे और realistic करें।
Utkarsh Agarwal:  That is just a point that is open। वो उसपे हम ये सारे एक बार edge cases and caveats एक बार देख के, उसके basis पे अगर definition में कुछ tweak करना है या इसका एक और version बनाना है, that we can do।
Utkarsh Agarwal:  कि अगले दो-तीन दिन में if we are able to narrow this down and lock that definition again।
Prapti Rastogi:  ठीक है। ठीक है, उत्कर्ष। अभी ना मैंने warehouse level पे ये तीनों— IA30, QIA30, and QIA30 core— ये तीनों निकाल लिए हैं।
Prapti Rastogi:  Now what I will do is एक बार थोड़ा सा हमारे internal use cases के हिसाब से भी थोड़ा सा इसको देख लेती हूँ मैं कि कैसे align कर रहा है ये। And on the basis of that, अगर मुझे लगता है कि कोई definition में changes required है या हम कुछ और broader sense में ले सकते हैं, तो वो मैं एक बार आपके साथ share करती हूँ।
Utkarsh Agarwal:  Correct। क्योंकि एक तो ये backend level पे एक चीज़ हो गया, और दूसरा product level पे practical implementation की— frontend level पे हमें इतना या तो चीज़ें मांगनी पड़ेंगी या हमें अलग तरीके से enrichments करने पड़ेंगे। तो वो एक practical trade-off भी हमें देखना पड़ेगा।
Utkarsh Agarwal:  तो balance the definition।
Ranjith M:  हाँ। So what I will do is I'll sync with Prapti in this case, उत्कर्ष। We'll try to get some definition.
Ranjith M:  We'll onboard Ashish also on this, then we'll come back to you. We'll try to close in coming very soon।
Utkarsh Agarwal:  हाँ, we will close the definition।
Ranjith M:  We will close the definition। We say already MOP is— it is not a blocker। It's just that— it's just the count will change।
Ranjith M:  For example, if you are targeting, let's say, 20%, 30%। Just the percentage of number will change।
Ranjith M:  ऐसा लग रहा है nothing else is going to change। So anyway, weekly or— I mean, the sprint and MOPs— anyways, it's already locked।
Ranjith M:  Sprint also I will just create। But again, QIA can be worked upon in coming days also।
Ranjith M:  Because of that।
Utkarsh Agarwal:  Correct।
Ranjith M:  Right।
Utkarsh Agarwal:  And it's important to lock the definition properly because while yes, nothing else changes, but then our goals and how we change it and all of that will have an impact। And our baseline— yeah, today we are at, for example, 10,000 and we need to get to 50,000। That chase and that practical use case of that chase will change।
Utkarsh Agarwal:  So hence we have to consciously agree on the definition।
Prapti Rastogi:  Correct।
Utkarsh Agarwal:  Right।
Prapti Rastogi:  ठीक है। ठीक है, उत्कर्ष। Broadly, ये तो warehouse पे था।
Prapti Rastogi:  दूसरा, उत्कर्ष, ask your query जो board बना रहे हैं, उसपे बस एक बार ये questions— Inc42 specific use cases के questions हम लोग test कर रहे हैं। हमने वो eval set and playbooks वाला method कर दिया है उसमें incorporate।
Prapti Rastogi:  Now just the questions Q&A एक बार try करके आपको final version submit करते हैं हम। I think, उत्कर्ष, बस I think कल तक में ये हो जाना चाहिए close।
Prapti Rastogi:  इसके अलावा, उत्कर्ष, Bootstrap Companies का जो हमारा enrichment वाला part है, जो हमें September MOP में close करना है, तो उसका kickoff start कर दिया है हमने अपने end से। To basically see कि अभी कितनी identified companies हम निकाल पा रहे हैं through other platforms।
Prapti Rastogi:  तो broadly, अभी यही तीन चीज़ों पे काम चल रहा है।
Utkarsh Agarwal:  समझ गया। Separate note पे— और एक हमारा वो MOP में वो add होना था, startup है, बस वो entity tag।
Prapti Rastogi:  वो मैं, उत्कर्ष, अभी add कर दे रही हूँ।
Utkarsh Agarwal:  Right। और एक और चीज़ मुझे याद आ रही थी, तो ठीक है, वो एक अलग discussion है। मतलब, just a note separately, वो roadmap planning में अलग से देख सकते हैं।
Utkarsh Agarwal:  अभी तो हम उसपे focus नहीं कर रहे, but data labs का जो हमने एक बार वो dataset की बात की थी ना, कि अब हमारे पास cap table है, तो उसके basis पे हम और क्या चीज़ें निकाल सकते हैं, वो एक point और है। मतलब, not that अभी हम उसमें कुछ implementation कर रहे हैं।
Utkarsh Agarwal:  तो product point of view से हमें backtrack करना पड़ेगा कि उसकी use case हम कहाँ पे उसको दिखा रहे हैं, specifically app या कहीं और में। क्योंकि cap table के basis पे now we have essentially options to unlock valuation and investor का individual ticket size also।
Utkarsh Agarwal:  And ऐसे एक-दो चीज़ें और निकल के आएँगी, जो हम filters point of view से पहले बात कर रहे थे। तो वो एक point है जो अलग से एक बार discuss कर सकते हैं।
Utkarsh Agarwal:  मतलब, या तो रंजीत एक बार देखती है ना कि कहीं use case अभी बहुत strong है, तो उसको consider करेंगे। नहीं तो ठीक है, उसको अभी note करके बाद में revisit कर सकते हैं।
Prapti Rastogi:  ठीक है। ठीक है। उत्कर्ष, इसको मैं अभी DL point of view से सोचूँ या app के point of view से?
Prapti Rastogi:  या both?
Utkarsh Agarwal:  पहले app point of view से।
Prapti Rastogi:  पहले app। ठीक है। 
Prapti Rastogi: ठीक है, ठीक है, उत्कर्ष। एक बारी मैं ये कर लेती हूँ। And दूसरा— ठीक है, I think ये app वाले point of view से मैं एक बारी ये कुछ datasets evaluate कर लेती हूँ।
Prapti Rastogi:  और एक ये MOP में add कर दूँगी मैं company classification वाला point।
Utkarsh Agarwal:  Right। क्योंकि app पे I think data labs का basic usage तो आ रहा है। तो पहले app point of view से एक बारी देख सकते हैं कि और वहाँ पे हम data point of view से— क्योंकि सिर्फ data points ही अभी हम functionality नहीं change कर रहे।
Utkarsh Agarwal:  But data point of view से हम अगर और कुछ value उसमें value create कर सकते हैं, that is the lens that we can look at it from।
Prapti Rastogi:  ठीक है, उत्कर्ष। ये मैं आपके साथ share करती हूँ। और रंजीत, आपके साथ भी share करती हूँ।
Prapti Rastogi:  एक बारी discuss कर लेंगे इसपे।
Utkarsh Agarwal:  ठीक है ना।
Ranjith M:  Done।
Utkarsh Agarwal:  हाँ, रंजीत, any other points?
Ranjith M:  No, उत्कर्ष, I'm good। वैसे design तो— we'll try to get the design for at least finalize the screen design for two screens at least। Then we'll close all the documentation what we just discussed on this call।
Ranjith M:  I believe nothing else for now।
Utkarsh Agarwal:  ठीक है। And app का— also now, after this, let's create a weekly dashboard of sorts, where we tracking the key metrics and key performances। And start reporting on that also weekly।
Ranjith M:  QIA।
Utkarsh Agarwal:  Hmm?
Ranjith M:  Hello? For app or for QIA?
Utkarsh Agarwal:  App first, QIA after we lock the definition।
Ranjith M:  Got it। Done।
Utkarsh Agarwal:  Done, उत्कर्ष।
Ranjith M:  Perfect।
Utkarsh Agarwal:  ठीक है। Done। Okay।
Ranjith M:  Cool.
Utkarsh Agarwal:  Thank you।
