# Product & Data Weekly

- Wispr meeting id: 1b0b6785-7732-4c9b-800f-48d8dd3ea3bb
- Start: 2026-09-07 18:14 IST (12:44Z) · End: 18:55 IST
- Attendees (calendar): Ashish Sharma, Prapti Rastogi, Ranjith M, Utkarsh Agarwal (organizer)
- Share link: https://notes.wisprflow.ai/shared/RfVfAWrzO_CNoDncsE8toJ7p--KhptrNor8RpV3oVwo
- Archived from Wispr Flow via MCP on 2026-09-08. Transcript is verbatim ASR output; speaker labels are Wispr's and are sometimes mis-assigned.

## Wispr summary
Debated whether QIA should require activation and how activation works across the multi-product (app, data labs, in42) setup, plus quick alignments on design strokes, Slack event, and the Mohangez deadline.

### QIA & Activation Definition
- Funnel ideally: identification → activation → actives; actives should only come from activated users
- Activation is product-specific; no single in42-wide activation yet, treat products separately for now
- QIA name retained, but definition updated: user must be activated on at least one surface to count
    - Backfill baseline will be higher than forward numbers since activation state unknown historically
- Infotude lacks an activation metric; needs one defined (tentative: 2+ articles, pending analysis)

### Unified Workspace & Events
- Approach: new combined workspace receiving only qualified action events; individual properties continue as-is
    - Open issue: stitching across anonymous → identified users, especially cross-surface journeys
- Volume events (e.g. page views) still flow to warehouse for engagement score calc

### Design & Logistics
- Proceed with stroke variant as primary across website; test gradient variant for PDF separately
- Mohangez closure deadline in 2 days; contact unresponsive, will escalate via email thread
- Azure portal access still blocked; try direct signup at portal.azure.com

### Next Steps
- (Speaker 1) Create Slack channel with Prakash, Akshay, Speaker 2, and self for app design overlaps
- (Speaker 2) Update stroke primary variant across website assets, then tackle PDF
- (Speaker 2) Create grid mapping QIA / activated / active user combinations
- (Speaker 2) Double-check edge cases for QIA requiring activation
- (Speaker 2) Sync with Prathi on how engagement score / page view events are implemented
- (Speaker 2) Run analysis to validate Infotude activation definition (2+ articles) via retention correlation
- (Speaker 2) Follow up with Mohangez contact; initiate email thread if no reply tonight
- (Speaker 2) Attend Slack product launch Thursday at Aerocity, 4:30–8:30

### Decisions Made
- QIA keeps its name but definition requires user to be activated on at least one surface
- Activation stays product-specific until in42 matures into a unified product
- Onboarding communication for cross-product users (e.g. app-activated visiting data labs web) will be tweaked to reflect existing QIA status
- Combined workspace receives only qualified action events; volume events stay in individual properties

## Transcript
Speaker 1: When you're acquiring the user—
Speaker 2:  You want to—
Speaker 1:  That is when you want to activate them.
Speaker 2:  Ha.
Speaker 1:  That is a one-time thing. This active vala— sorry, ha, this active vala 10 qualifying actions—
Speaker 2:  Ha.
Speaker 1:  —is for the population overall that exists in your identified pool, or not even— not necessarily identified also. Engage— this is a metric for engage. What we call engagement.
Speaker 2:  Ha.
Speaker 1:  Engage users— के लिए these qualifying actions—
Speaker 2:  Then that becomes a repeat rate of engaged users. नहीं, that becomes— नहीं, that becomes a repeat rate of—
Speaker 1:  Engagement metric.
Speaker 2:  Ha, of QIA. But QIA— ideally it should be qualified, identified, people have activated. When I say activated— activation— irrespective of people coming through different journey, if they've done few active— any either of the steps that we decided.
Speaker 2:  That is also an activation, nah. We are defining activation if they did any of the activity.
Speaker 2:  Not a random activity— the activity which we specified.
Speaker 1:  Mm-hm.
Speaker 2:  So that is activation, nah.
Speaker 1:  Activation is product-specific and only at new acquisition.
Speaker 2:  Ha, ha, 100%. But anyways, you— you'll also have to define— once your acquisition is done, you'll have to define activation.
Speaker 1:  Mm-hm.
Speaker 2:  Anyways, current— the actives that you have listed. Those are product-specific in a way. In a way it is a product-specific.
Speaker 2:  Then that becomes your activated user also.
Speaker 1:  Mm-hm.
Speaker 2:  That becomes your activation, essentially.
Speaker 1:  Right. Abhi— both are correlated but are not equal.
Speaker 2:  Okay, let's talk about activation. Only activation.
Speaker 1:  Mm-hm.
Speaker 2:  If someone signed up, which means we are acquired.
Speaker 1:  It's all about ac— activation and the relation with QIA. Let's say cap as the scope. Now tell me.
Speaker 2:  How—
Speaker 1:  How— how are they saying?
Speaker 2:  Ha, ठीक है. So now, in this case, people have completed the brief. We are considering those an activated user.
Speaker 2:  Activate— is that activation done for that particular user?
Speaker 1:  After signup, they— they complete the brief, yes.
Speaker 2:  It is activation.
Speaker 1:  After signup, within the first 7 days.
Speaker 2:  Ha, within first 7 days. This is one. Uh, are you not considering people who are going through few articles at depth?
Speaker 1:  Not in activation.
Speaker 2:  But you'll— you'll— but you'll consider them as actives. Now, in website, you'll have one activation.
Speaker 1:  Right.
Speaker 2:  It could be going through two articles. Or it could be search also. It could be, uh—
Speaker 1:  Like in data labs, the activation metric that we last week decided was at least two advanced searches.
Speaker 2:  Ha. But not necessarily. As soon as we have asked in for the same to help them reduce the search.
Speaker 1:  अब वो तो अभी बाद में आया. मतलब, last when— without asking for when it was being considered, then the last activation definition that we set for data labs was.
Speaker 2:  Ha.
Speaker 1:  At least two advanced searches done.
Speaker 2:  Ha.
Speaker 1:  तो उसका वो है.
Speaker 2:  Ha. No, सर— सर, definition है is called identified activation.
Speaker 1:  Right.
Speaker 2:  Ha. Again, we are— what we are trying to chase within 7 days is activation end of the day. Actives is we are chasing after 7 days.
Speaker 1:  Mm-hm.
Speaker 2:  तो QIA within 7 days as a term is not making sense, nah. If you define A as a active— actives.
Speaker 1:  Like for example, um, um, for example, if someone's Northstar is DAU, for example, activation may or may not have happened, but DAU can still happen.
Speaker 2:  नहीं, DAU— in the DAU, you want user to complete your goal, nah. That is what you'll— you'll chase for. DAU is just not opening the app.
Speaker 2:  They'll have to perform the activity which we are tend to. So that is— in a way, it's an activation criteria.
Speaker 2:  So you'll bring user to app. Article is again a secondary.
Speaker 2:  But you'll— you'll keep bringing user to the app to complete the brief end of the day.
Speaker 1:  Mm-hm.
Speaker 2:  That— तो in a way, it cannot happen, nah, what you just said.
Speaker 1:  For example, if there is a user who is signed up to the app.
Speaker 2:  Who signed up to the app.
Speaker 1:  Did not— well, used the brief but never completed a brief.
Speaker 2:  Ha.
Speaker 1:  But uses the app daily to search companies on retail apps in— in the app.
Speaker 2:  Ha. What do you consider as actives? What do you consider as an activated user?
Speaker 1:  नहीं.
Speaker 2:  You won't consider as activated user. But the finally— it break, nah. There's a lot of— now, there is a lot of discrepancy in this itself.
Speaker 1:  Mm-hm.
Speaker 2:  So ideally, active user— those— ideally, those people have experienced the activation. But there is a lot of bigger disconnect happening here. But again, तो what you're saying is an extreme case.
Speaker 1:  Then we'll have to eventually change the activation definition.
Speaker 2:  In— eventually we'll have to change the activation definition.
Speaker 1:  Because right now we are somewhere in the middle. When I say somewhere in the middle, because we're trying to apply things retro— retrospectively also to the existing user base. Now, existing user base may or may not have done the activation which we defined later.
Speaker 2:  नहीं, I'm just try— talking about what we are doing moving forward. That is the only thing which I'm— I'm not considering.
Speaker 1:  Existing.
Speaker 2:  Ha. Existing— existing— I can get them back different ways. But again, I'm only talking about the time that we're going to implement this.
Speaker 1:  Right.
Speaker 2:  So it should be identification, activation, then actives. It cannot be other.
Speaker 1:  Point of view. Yes. From a finally point of view, yes.
Speaker 2:  But.
Speaker 1:  Ha.
Speaker 2:  Your only challenge is. Then they should not— actives then should not ever come back. Uh, if— if.
Speaker 1:  But how do you manage that?
Speaker 2:  Ha, I'll tell you. I'll tell you. If— if it is going ulta, which is activation is less, users are high, then we are not chasing the right metric.
Speaker 1:  Then the activation definition is wrong.
Speaker 2:  Ha.
Speaker 1:  Agreed.
Speaker 2:  Which is— then it is wrong.
Speaker 1:  Agreed.
Speaker 2:  So ideally.
Speaker 1:  But इसमें just one caveat additional.
Speaker 2:  Ha.
Speaker 1:  How do you handle this on a multi-product?
Speaker 2:  Ha.
Speaker 1:  They might have activated on data.
Speaker 2:  Data labs.
Speaker 1:  Ha. But are active on the app.
Speaker 2:  Ha.
Speaker 1:  And did not complete activation here.
Speaker 2:  See, okay. As an in42 user.
Speaker 1:  So in this case, are they activated in any one place but are active in some other place?
Speaker 2:  Ha.
Speaker 1:  Do we count them as activated here also?
Speaker 2:  So now, it depends on— for an example, uh, let's say I'll— I'll talk about this. Uh, I am active— I'm— I'm an activated user on app, which means I've completed at least one brief in any— within certain window. Now I'm coming to data labs.
Speaker 2:  Now, what we need to do is, I'll treat for now as a separate product. Now I want to give them more— uh, it's an activated user still.
Speaker 2:  But I want to give more nudges to get them activated. Again, my act— my intention is not to become an activated user.
Speaker 2:  Whenever an activation defines, so that they understand the product. Whatever it makes me for them to understand a product or experience a product, that I'll call it as a— that, okay, that they— that person has understood the product.
Speaker 2:  But activation ultimately, as a one in42, at least they know one thing about that particular product. Other set of product, for an example, uh, data labs, media.
Speaker 1:  It will be— I— fair. Direction-wise, you're saying fair. But I think one caveat for now, what I want to add here is, they'll be have a much more concrete version of one in42.
Speaker 2:  Ha.
Speaker 1:  Till then, we can keep these two as separate.
Speaker 2:  I was about to— I thought you— I know you'll go to there. You'll say.
Speaker 1:  QIA has to be separate and activation has to be separate for now.
Speaker 2:  Ha.
Speaker 1:  Because.
Speaker 2:  Now, then.
Speaker 1:  Because from an individual product perspective, तो for example, he's activated and active on the app, then he goes to data labs.
Speaker 2:  Talking about data labs website or company section?
Speaker 1:  Uh, website.
Speaker 2:  Ha. ठीक है.
Speaker 1:  Then he goes to data labs, does not get activated.
Speaker 1:  But data labs has a— for now, till it's treated as a separate product. From its goal perspective, it wasn't— the user wasn't activated.
Speaker 2:  It's a new user. For data labs, it's a new user.
Speaker 1:  So for them, it's not activated. And for them else, the user did not understand the product.
Speaker 2:  Ha. Ha, which— which also same which I said.
Speaker 1:  अभी right now, I'm— in a larger horizon, yes, the funnel should work like that. In an ideal case also, funnel should work like that. That is how— that's why it's called a funnel.
Speaker 2:  Ha.
Speaker 1:  But since it's a multi-product approach.
Speaker 2:  As long as we are not chasing the wrong numbers.
Speaker 1:  Since it's a multi-product approach, that is why— for now, that is why I said both statements can be true, but right now they don't have to be.
Speaker 2:  Ha.
Speaker 1:  Interconnected. That QIA has to be a— a— a activated user only.
Speaker 2:  Ha, but in a way.
Speaker 1:  Or you can say QIA is activated user anywhere. At least one of the surfaces, the user is activated.
Speaker 2:  Ha.
Speaker 1:  That can be, for the time being, the definition.
Speaker 2:  Ha.
Speaker 1:  Eventually, that has to evolve.
Speaker 2:  Ha. Now, the communication— if someone is going to experience the second product, the— not the one which is activated, the second product, now the first intention of the marketing of the product should be, how do we make sure that they experience that product? Which becomes the activation.
Speaker 2:  Again, we are not explicitly saying activation because it, again, takes another— different discussion, because it, again, confuses when we discuss with the— in general with people. But our aim is to— for if someone is experienced opening data labs, our aim is to focus on certain products.
Speaker 1:  Mm-hm.
Speaker 2:  That becomes our ultimate goal.
Speaker 1:  Mm-hm.
Speaker 2:  But as a one in42, we are treating as a activated user.
Speaker 1:  Fair. For now, yes. उसमें अपने फर्दर नुआंसेस लिखता हूँ.
Speaker 1:  मतलब, फॉर एग्जांपल, इफ वी आर डिज़ाइनिंग.
Speaker 2:  मुझे ऐसा लग रहा है.
Speaker 1:  द ऑनबोर्डिंग कम्युनिकेशन.
Speaker 2:  सेम.
Speaker 1:  इन द सेम सिनेरियो, डेटा लैब्स में. एंड मतलब, एक्टिवेटेड एंड एक्टिव ऑन ऐप. नाउ ही गोज़ टू डेटा लैब्स वेब.
Speaker 2:  तो वी डोंट आस्क फॉर ऑनबोर्डिंग.
Speaker 1:  ऑनबोर्डिंग नहीं किया. बट कम्युनिकेशन पॉइंट ऑफ व्यू से, आई थिंक दैट सेगमेंट वी हैव. कि हाँ, दे आर ऑलरेडी.
Speaker 2:  दे आर.
Speaker 1:  अ QIA user और अ.
Speaker 2:  हाँ.
Speaker 1:  फ्रेश यूज़र.
Speaker 2:  हाँ.
Speaker 1:  एंड अकॉर्डिंग्ली, द कम्युनिकेशन विल हैव टू बी ट्वीक्ड.
Speaker 2:  स्लाइटली.
Speaker 1:  अकॉर्डिंग्ली.
Speaker 2:  हाँ.
Speaker 1:  ठीक है. फेयर.
Speaker 2:  हाँ, दिस इज़ द कंक्लूजन व्हिच आई वांट टू गेट. बिकॉज़ आई वांट— again, I also don't want to drag this conversation. I believe there will be changes which will come.
Speaker 2:  एंड आई डोंट थिंक देयर इज़ एनी डाउट ऑफ दिस क्वेश्चन कमिंग अगेन.
Speaker 1:  हाँ.
Speaker 2:  बट एटलीस्ट, वी विल लॉग दिस डेफिनेशन.
Speaker 1:  नहीं, तभी QIA में— दैट्स व्हाई अभी एक्टिवेशन— दैट्स व्हाई आई हैडंट पर्पसली पुट इट. बिकॉज़ QIA राइट नाउ मेजरिंग द बेसलाइन फॉर इट बेस्ड ऑन, uh, existing डेटा वेयरहाउस डेटा. बिकॉज़ देयर, यू डोंट नो वेदर द यूज़र वाज़ इवन एक्टिवेटेड ऑर नॉट.
Speaker 1:  द ओनली थिंग यू कैन नो इज़ वेदर दे आर.
Speaker 2:  कर सकते हैं, ना. तो बैकफुट डेटा तो है. देन आई विल शो व्हाट प्राथिया शेयर्ड मी.
Speaker 2:  इसे थोड़ा पुराना डेटा है. इट्स लिटिल ओल्डर.
Speaker 2:  बट.
Speaker 1:  यूनिफाइड वर्कस्पेस वाला पॉइंट, जिसमें ओपन लिखा है इन द एमओएम.
Speaker 2:  हाँ.
Speaker 1:  वो हमने अभी के लिए कंक्लूड तो कर लिया था. वी हैड ऑलरेडी टेकन अ डिसीजन ऑन दिस.
Speaker 2:  व्हेन डिड वी?
Speaker 1:  वी डिस्कस्ड, ना, इन द लास्ट मंडे का मीटिंग.
Speaker 2:  हाँ, एंड इट वाज़ स्टिल अ ओपन पॉइंटर.
Speaker 1:  नहीं, द डिसीजन इन द प्रोडक्ट मीटिंग, नॉट इन द टीम लीड मीटिंग.
Speaker 2:  हाँ, हाँ, सेम मीटिंग.
Speaker 1:  नो, नो. ऑन दैट, वी डिस्कस्ड, uh, वी क्रिएट अ न्यू कंबाइंड प्रॉपर्टी एंड ओनली सेंड की इवेंट्स, व्हिच आर द क्वालिफाइड एक्शन इवेंट्स, इंटू इट फॉर नाउ टू बिगिन विथ. नॉट द वॉल्यूम इवेंट्स.
Speaker 2:  नो, बट दैट वाज़ नेवर कंक्लूडेड.
Speaker 1:  तो दैट वाज़ द कंक्लूजन.
Speaker 2:  नहीं.
Speaker 1:  हाँ.
Speaker 2:  नहीं, नहीं.
Speaker 1:  आई हैव इट रिकॉर्डेड.
Speaker 2:  नहीं, आई आल्सो— आई आल्सो— व्हाट आई डिड इज़, व्हेन बिफोर मी क्रिएटिंग दिस डॉक्यूमेंट, uh, इट गॉन थ्रू ऑल माय मीटिंग्स.
Speaker 1:  हाँ.
Speaker 2:  ओबवियसली, मोस्ट मेजॉरिटी ऑफ़ देयर पार्ट. तो उसमें वी— वी वर सपोज़ टू कम बैक विथ व्हाट आर द अप्रोचेस. वी वर नेवर कंक्लूडेड दिस.
Speaker 1:  ऑन द QIA डेफिनेशन.
Speaker 2:  नहीं, नहीं.
Speaker 1:  नहीं, नहीं, नहीं. इवेंट्स. एंड टॉक.
Speaker 1:  इवेंट्स वाज़— दैट डिस्कशन वाज़ अ वीक बिफोर दैट. जस्ट लास्ट वीक वाले में तो वी कंक्लूडेड दिस.
Speaker 1:  दिस वाज़ माय ओनली स्टेटमेंट कि— बिकॉज़ द थ्री ऑफ़ यू वर सिटिंग हियर एंड वी हैड— यू हैड आस्क्ड द सेम थिंग. वी हैड कंक्लूडेड कि क्रिएट अ न्यू कंबाइंड वर्कस्पेस एंड ओनली सेंड QI— द क्वालिफाइड एक्शन.
Speaker 2:  क्वालिफाइड एक्शन. नहीं.
Speaker 1:  बिकॉज़ द वॉल्यूम विल नॉट बी टू मच. ठीक है, अभी नहीं. अगर इफ दैट वाज़ स्टिल अ कंफ्यूजन, डू दिस.
Speaker 1:  लेट्स गो अहेड विथ दिस. उसमें स्टिचिंग कैसे हो रही है, वाज़ द ओपन पॉइंट.
Speaker 2:  नहीं, अगर इफ यू आर एबल टू सॉल्व द स्टिचिंग एज अ प्रॉब्लम, तो ऐसे करते हैं, ना. ऐसे कर लेते हैं. व्हाई डू डू वी सॉल्व टू डिफरेंट प्रॉब्लम्स?
Speaker 2:  आई मीन, प्रॉब्लम इज़ एक ही है.
Speaker 1:  नहीं, नहीं. उस— इन दिस अप्रोच, दैट आई सेड, सेंड ओनली क्वालिफाइड एक्शंस टू दैट कॉमन प्रॉपर्टी.
Speaker 2:  हाँ.
Speaker 1:  उसमें द ओपन पॉइंट, एस पर मी, दैट वाज़ लेफ्ट, वाज़ हाउ आर वी स्टिचिंग. जिसमें वो एसडीके वाली बात भी हुई थी कि हाँ, दे और— नहीं, वो एसडीके वाली बात यहाँ पे नहीं हुई थी. वो दूसरा कॉम्बिनेशन था.
Speaker 1:  बट हाँ, स्टिचिंग कैसे होगी, दैट वाज़ द पॉइंट.
Speaker 2:  नहीं, अ— अ— एक्टिवेशन, क्वालिफिकेशन.
Speaker 2:  बट इज़— डोंट यू थिंक इट बिकम्स लिटिल लेस एफिशिएंट इफ वी ओनली सेंड क्वालिफाइड आइडेंटिफाइड एक्ट— अ— क्वालिफाइड इवेंट्स जो है, इफ वी आर सेंडिंग ओनली टू दोज़ रेस— अ सेपरेट वर्कस्पेस. फॉर एन एग्जांपल, फॉर पीपल आर— लेट्स से देयर इज़ अ यूज़र, अनोनिमस यूज़र, हैव गॉन थ्रू थ्री आर्टिकल्स और डिड सर्टेन सर्च, बट नॉट लॉग इन.
Speaker 2:  आई वांट टू शो द सर्टेन, uh, मॉडल एक्स ओनली टू देम. नाउ, इट बिकम्स अ यूज़र.
Speaker 2:  इट बिकम्स अनएक्टिवेटेड यूज़र.
Speaker 1:  नहीं, दिस इज़ जस्ट अ पायलट. दिस इज़ नॉट यूज़फुल.
Speaker 2:  हाँ.
Speaker 1:  दिस इज़—
Speaker 2:  नहीं, बट एक ही करते हैं, ना. बिकॉज़ एनीवेज, आई हैव डन मोर टू फिक्स एवरीथिंग प्रॉपर्ली.
Speaker 1:  नहीं, नहीं, वो तो वैसे भी चलेगा. द इंडिविजुअल प्रॉपर्टीज़ विल स्टिल रिमेन. ऑन टॉप ऑफ दैट, एज अ डेस्टिनेशन, वी ऐड अनदर कॉमन प्रॉपर्टी, इन व्हिच रिस्पेक्टिव क्वालिफाइंग एक्शंस फॉर ईच ऑफ़ द थ्री प्रोडक्ट्स आर आल्सो सेंट टू द—
Speaker 2:  बट हाउ वुड— हाउ वुड द यूटिलाइज़ेशन ऑफ़ दैट गोना लुक लाइक?
Speaker 1:  उसमें— दैट इज़ हाउ वी टेस्ट द स्टिचिंग, वेदर स्टिचिंग एंड एवरीथिंग इज़ वर्किंग करेक्टली, एंड वेदर देयर इज़ अ ओवरलैप बिटवीन पीपल अक्रॉस प्रॉपर्टीज़.
Speaker 2:  वो तो एनीवेज होगा, ना.
Speaker 1:  स्टिचिंग नहीं अभी सॉल्व हो रही, ना.
Speaker 2:  स्टिचिंग वैसे भी, हाँ, एनोनिमस में.
Speaker 1:  एनोनिमस में.
Speaker 2:  आई नो. नहीं, इवन इन दिस—
Speaker 1:  एनोनिमस में भी जाएगा, ना. इन दिस अप्रोच, वी गेट अ सेंस ऑफ व्हाट हैपेंस इन एनोनिमस.
Speaker 2:  नहीं, आई हैव वन क्वेश्चन. फॉर एन एग्जांपल, यू आर एन यूज़र. यू ओपनड इन42 वेब.
Speaker 1:  हम्म.
Speaker 2:  अ— यू डिड द ओपन थ्री फोर आर्टिकल.
Speaker 1:  हम्म.
Speaker 2:  यू केम टू ऐप.
Speaker 1:  हम्म.
Speaker 2:  यू लॉगड इन एन ऑनबोर्डिंग. आइडियली, यू आर एन एक्टिवेटेड यूज़र.
Speaker 1:  हम्म.
Speaker 2:  बट तो द करंट सेटअप में, द वन व्हिच यू आर सेइंग विल नॉट वर्क.
Speaker 1:  यस.
Speaker 1:  आई थिंक स्ट्रोक वाला प्राइमरी है, ना. इसमें थोड़ा वो क्रिएट भी लग रहा है.
Speaker 2:  ग्रेडिएंट की वजह से?
Speaker 1:  हाँ.
Speaker 2:  समझ में नहीं आ रहा. इसमें भी स्ट्रोक के समझ में आ रहा है. तो अभी ये दो वेरिएशंस अभी ट्राई करें.
Speaker 1:  ठीक है.
Speaker 2:  मेजरली यही दोनों यूज़ होंगे.
Speaker 1:  ठीक है.
Speaker 2:  तो मैं आगे प्रोसीड करूँ ये हर जगह पे चेंज.
Speaker 1:  राइट.
Speaker 2:  ये हम कई बहुत— अ— डीप कर दो. डीप प्राइवेटाइज. क्योंकि—
Speaker 1:  हाँ, प्राइमरी वही है. अगर कहीं जरूरत पड़े और जहाँ पे वो फिट नहीं आता, तभी ये यूज़ करो.
Speaker 2:  ठीक है. मुझे लग रहा है जो हम पीडीएफ बनाया, ना, इसमें आई डोंट थिंक स्ट्रोक फिट होगे. एक बार मैं ट्राई करूँगा.
Speaker 2:  अभी बस खाली वेबसाइट वगैरह में.
Speaker 1:  जहाँ पे एप्लीकेशन में डाउट आ रहा है, वहाँ पे अगर मैं एक चैनल बना के देता हूँ, टू सी डिज़ाइन्स का, प्रकाश के साथ, उसमें अक्षय वगैरह को भी डाल देता हूँ.
Speaker 2:  ठीक है.
Speaker 1:  ताकि वहीं पे अब ये जो भी ओवरलैप्स आ रहे हैं, वहाँ पे फिर वो टच करते जाएँ.
Speaker 2:  ठीक है. थैंक यू. अभी के लिए फिर मैं वेबसाइट, ये सब के लिए, जहाँ पे प्राइमरी यूज़ होगा, वो सारे मैंने अपडेट करूँगा.
Speaker 1:  ठीक है.
Speaker 2:  देन पीडीएफ पे आएगा.
Speaker 1:  ठीक है. चैनल तुम ही बना दो. मैं पहुँच नहीं पाऊँगा.
Speaker 2:  ठीक है.
Speaker 1:  प्रकाश, अक्षय, तुम और मैं.
Speaker 2:  ठीक है.
Speaker 1:  हम्म.
Speaker 2:  हम्म. सो व्हाट आई एम सेइंग इज़, अस्यूम यू आर सेंडिंग अ क्वालिफाइड इवेंट्स टू वन सिंगल वर्कस्पेस.
Speaker 1:  हम्म.
Speaker 2:  अस्यूम देयर इज़ अ यूज़र हु हैव ब्राउज़्ड इन42 वेबसाइट आर्टिकल्स एंड लेटर डाउनलोड द ऐप एंड डिडन ऑनबोर्डिंग एंड कंप्लीटेड द साइन अप बाय गिविंग द डिटेल्स. आइडियली, इट इज़ एन एक्टिवेटेड यूज़र एज वेल. बट इन द वर्कस्पेस, इन द अप्रोच व्हिच यू सेड, इट विल नॉट सैटिस्फाई दिस.
Speaker 1:  व्हाट विल नॉट सैटिस्फाई?
Speaker 2:  हाउ वुड यू टेल दिस इज़ एन एक्टिवेटेड यूज़र? बिकॉज़ व्हाइल ही डिडन एक्टिवेशन, एट द टाइम ही वाज़ अ नॉन लॉगिन यूज़र. इन दिस इंस्टेंस, वी वुड हैव नॉट सेंड दिस इवेंट टू द वर्कस्पेस.
Speaker 1:  हम्म.
Speaker 2:  लेटर ही डाउनलोड एंड कंप्लीटेड द ऑनबोर्डिंग. वी वुड हैव सेंड दिस इवेंट.
Speaker 1:  नहीं, बट आई हैड आइडेंटिफाइड इवेंट्स आल्सो.
Speaker 2:  हाँ?
Speaker 1:  आई हैड आइडेंटिफाइंग इवेंट्स आल्सो.
Speaker 2:  वैसे फिर सारा है, ना.
Speaker 1:  आइडेंटिफाइड, आइडेंटिफाइड.
Speaker 2:  आइडेंटिफायर.
Speaker 1:  हाँ, ओनली द वन इवेंट्स दैट रिक्वायर आइडेंटिफिकेशन. लाइक लॉगिन, रजिस्टर.
Speaker 2:  नहीं, एक्टिवेशन और आइडेंटिफिकेशन.
Speaker 1:  आइडेंटिफिकेशन.
Speaker 2:  नहीं. सी, लेट्स से यू डिड अ स्क्रॉल इन इन42 वेबसाइट. यू— देन यू क्लोज़्ड इट.
Speaker 2:  यू केम टू ऐप. यू डिड लॉगिन एंड कंप्लीटेड ऑनबोर्डिंग.
Speaker 2:  सो यू आर अ क्वालिफाइड यूज़र.
Speaker 1:  हम्म.
Speaker 2:  बट इन दिस केस, आई विल सेंड ओनली टू इवेंट्स, व्हिच इज़ ऑनबोर्डिंग कंप्लीटेड, साइन अप कंप्लीटेड, टू द न्यू वर्कस्पेस.
Speaker 1:  ठीक है. इसपे वी कैन कम बैक. बट इज़ नॉट अ क्रिटिकल पॉइंट टू सॉल्व अभी.
Speaker 2:  हाँ.
Speaker 1:  अभी तो इंडिविजुअल तो कर ही रहे हैं.
Speaker 2:  हाँ, वैसे वो तो—
Speaker 1:  बिकॉज़ लास्ट मीटिंग वी वर डिस्कसिंग, कैन वी डू द यूनिफाइड वाला थिंग आल्सो? सो दैट— देन दिस वाज़ द अप्रोच आइडेंटिफाइड.
Speaker 2:  हाँ.
Speaker 1:  कि वी कैन डू समथिंग लाइक दिस, बट दिस इज़ नॉट नेसेसरी राइट नाउ.
Speaker 2:  नहीं, बस करना पड़ेगा, ना.
Speaker 1:  क्यों?
Speaker 2:  क्योंकि देन हाउ वुड इट अक्रॉस प्रमोटेड?
Speaker 1:  वो तो डेटा वेयरहाउस से रिवर्स हीटेड.
Speaker 2:  हाँ, नहीं होगा, ना. देन वी हैव टू स्टार्ट कंज़्यूमिंग ऑल द स्क्रॉल्ड अप इवेंट्स.
Speaker 1:  नहीं, नहीं, वो तो इंडिविजुअल प्रॉपर्टीज़.
Speaker 2:  ओके.
Speaker 1:  वुड बी सेंडिंग थिंग्स टू वेयरहाउस?
Speaker 2:  इंडिविजुअल प्रॉपर्टीज़ ऑफ?
Speaker 1:  ईच ऑफ़ द थ्री सरफेसेस.
Speaker 2:  ऑल द इवेंट्स वी आर सेंडिंग टू.
Speaker 1:  हाँ, हाँ.
Speaker 2:  नहीं, ऑल इवेंट्स आर आल्सो गोइंग. एनालिटिक इवेंट्स आर ऑल गोइंग. ओके.
Speaker 2:  ओके. नहीं, जितना व्हाटएवर द डिस्कशन व्हिच आई हैड विथ प्राथी टू द एक्सटेंट, दोज़ आर क्वालिफाइंग इवेंट्स फॉर नाउ एंड आदर सेट ऑफ इवेंट्स.
Speaker 2:  हाई वॉल्यूम इवेंट्स जितना मैंने—
Speaker 1:  वो कॉमन प्रॉपर्टी की बात हो रही है. इसमें, अ— अ— डेटा वेयरहाउस में तो ऑल इवेंट्स गो. और शुड गो.
Speaker 2:  हाँ, शुड गो. आई अग्री. बट इट इज़ नॉट हैपनिंग.
Speaker 2:  और इट्स— एटलीस्ट इट्स नॉट पार्ट ऑफ़ द प्लान.
Speaker 1:  नहीं, इट इज़ हैपनिंग. अभी फॉर एग्जांपल, टू कैलकुलेट द एंगेजमेंट स्कोर, दे आर फैक्टरिंग द पेज व्यूज़. टू कैल— टू फैक्टर इन द पेज व्यूज़, दे नीड द पेज व्यू इवेंट्स.
Speaker 2:  नहीं, दे कैन—
Speaker 1:  व्हिच इज़ द मोस्ट हाईएस्ट वॉल्यूम इवेंट.
Speaker 2:  हाँ. नहीं, इट कैन बी एक्सट्रैक्टेड फ्रॉम— अ— व्हेनएवर दिस सपोज़ टू हैपन, इट कैन बी आल्सो एक्सट्रैक्टेड फ्रॉम ईदर ऑफ़ दोज़ प्लेटफॉर्म. कैन बी कैलकुलेटेड इज़ व्हाट आई एम सेइंग.
Speaker 2:  व्हाट आई विल डू इज़ आई विल सिंक विथ प्राथी एंड अंडरस्टैंड हाउ एक्सैक्टली इट इज़ बीन इम्प्लीमेंटेड इन—
Speaker 1:  पर यूसीएस क्या है? मतलब फाइनली, अभी हम व्हाट आर वी ट्राइंग टू सॉल्व एट द एंड ऑफ़ इट, वहाँ से रिवर्स करते हैं.
Speaker 2:  हाँ. व्हाट वी आर ट्राइंग टू सॉल्व इज़, इफ पीपल आर डिड वन थिंग एट वन प्लेटफॉर्म, डूइंग अदर थिंग एट अदर प्लेटफॉर्म, हाउ डू वी कॉल इट एज एक्टिवेटेड?
Speaker 1:  एक्टिवेटेड इज़ प्रोडक्ट-स्पेसिफिक ओनली. दैट्स व्हाट आई सेड, ना अभी.
Speaker 2:  एक्टिवेटेड इज़ प्रोडक्ट-स्पेसिफिक. 100% अग्रीड.
Speaker 1:  QIA फॉर नाउ इज़—
Speaker 2:  क्वालिफाइड, आइडेंटिफाइड.
Speaker 1:  एक्टिव्स.
Speaker 2:  एक्ट— एक्टिवेशन्स.
Speaker 1:  एक्टिव्स.
Speaker 2:  देन हियर, व्हेर आर यू कंसीडरिंग एक्टिवेशन इन दैट?
Speaker 1:  देन इन द QIA7, फॉर एग्जांपल, क्वालिफाइड, आइडेंटिफाइड एक्टिव्स मे हैव द यूज़र्स हु आर आइडेंटिफाइड एंड क्वालिफाइड हैव डन वन ऑफ़ द क्वालिफाइंग एक्शन्स इन द लास्ट सेवन डेज. दैट इज़ QIA7.
Speaker 2:  हाँ. बट नाउ यू आर— यू आर स्किपिंग ऑल द—
Speaker 1:  इर्रेस्पेक्टिव ऑफ़ एक्टिवेशन.
Speaker 2:  हाँ, बट यू आर कंप्लीटली स्किपिंग द एक्टिवेशन पार्ट.
Speaker 1:  फॉर नाउ.
Speaker 2:  हाँ, बट वो— दैट इज़ नॉट हाउ इट शुड वर्क, ना. एक्टिवेशन इज़ समथिंग व्हेन यू मेक पीपल एक्सपीरियंस योर प्रोडक्ट. दैट्स व्हेन दे एक्सपीरियंस द प्रोडक्ट.
Speaker 2:  बट नाउ, इफ यू आर सिंपली चेसिंग QIA नॉट रादर एन एक्टिवेशन, फिर वो टेक्निकली और प्रोडक्ट वाइज़ और इन जनरल आल्सो, इट्स— इट गोज़ अगेंस्ट व्हाट वी आर चेसिंग वर्सेस व्हाट वी आर गोइंग टू गेट.
Speaker 1:  हम्म.
Speaker 2:  सी, इफ यू आर— सी, अ— इफ आई से पीपल आर कमिंग टू आर ऐप रीडिंग न्यूज़, इज़ दैट व्हाट वी इवेंचुअली वांट टू फोकस ऑन? नो.
Speaker 1:  नहीं, हाइपोथेटिकली, इफ फॉर एग्जांपल अ डिफरेंट प्रोडक्ट लाइन—
Speaker 2:  हाँ.
Speaker 1:  हैड नॉट स्टार एज पेइंग यूज़र्स और नंबर ऑफ़ ट्रांजैक्शन्स, लाइक फॉर अ ई-कॉमर्स वेबसाइट. जब ई-कॉमर्स स्ट्रीम स्लाइटली डिफरेंट, बट ठीक है. सो अ कंज्यूमर ऐप व्हिच हैज़ पेड मोर.
Speaker 1:  व्हाट इफ द यूज़र कम्स, डज़ नॉट एक्टिवेट, बट पेज, एंड योर नॉट स्टार वाज़ पेमेंट? वुड यू स्टिल काउंट देम इन योर नॉट स्टार?
Speaker 2:  नहीं, मतलब लेस लाइकली है, ना. द यूज़र वुड हैव गॉन थ्रू एटलीस्ट वन ऑफ़ द एक्टिवेशन मेट्रिक, एंड देन— दैट्स व्हेन अ परचेस हैपेंस. सी, परचेस हैपेंस ओनली व्हेन यू अंडरस्टैंड द वैल्यू ऑफ़— नहीं, नहीं, मोस्टली.
Speaker 2:  एटलीस्ट द— नहीं, दैट— दैट्स अ रेयर केस, ना. नहीं, सी, पीपल वुड नॉट पे बिफोर एक्सपीरियंसिंग द प्रोडक्ट.
Speaker 2:  नाउ, एक्सपीरियंसिंग द प्रोडक्ट बिकम्स अ एक्टिवेशन फॉर देम.
Speaker 1:  हाँ.
Speaker 2:  दैट— दैट्स व्हेन दे गेट द पेमेंट. तो टेक्निकली और एसेंशियली, विदाउट एक्टिवेशन, दे वुड नॉट रीच पेमेंट. अनलेस अंटिल— आई— समवन एक्सप्लीट सेइंग, इसका एक्सेस, इसका— अ— बाय चैट जीपीटी, बाय एक्स वाई जे.
Speaker 2:  दैट वुड नॉट हैपन. इधर—
Speaker 1:  इट कैन हैपन.
Speaker 2:  हाँ, इट कैन. दैट्स व्हाट आई एम गोइंग टू से.
Speaker 1:  फॉर एग्जांपल, इफ आई—
Speaker 2:  फॉर एग्जांपल, लाइक अ प्रोडक्ट लाइक लवरेबल, फॉर एग्जांपल, व्हिच हैज़ अ क्रेडिट बेस सिस्टम, एंड दे हैव अ फ्री प्लान आल्सो.
Speaker 1:  हाँ.
Speaker 2:  एंड पीपल कैन डू इट ऑन द फ्री प्लान आल्सो.
Speaker 1:  हाँ.
Speaker 2:  राइट? एंड देयर एक्टिवेशन— टेक्निकली, देयर एक्टिवेशन मेट्रिक वुड बी कि हाँ, पीपल साइन अप, एंड देन दे ट्राई द फ्री प्रोडक्ट, एंड स्पेंड एक्स नंबर ऑफ़ क्रेडिट्स टू क्रिएट एक्स वाई जेड.
Speaker 1:  हाँ.
Speaker 2:  एंड देन दे आर काउंटेड एज एक्टिव—
Speaker 1:  हाँ.
Speaker 2:  एक्टिवेटेड.
Speaker 1:  हाँ.
Speaker 2:  बट इफ समवन जस्ट गोज़ टू लवरेबल का होम पेज एंड जस्ट बाय्स अ सब्सक्रिप्शन.
Speaker 1:  बट दैट इज़ वेरी— नहीं, दैट इज़ वेरी लेस लाइकली, ना, प्रकाश.
Speaker 2:  बट एज़ दैट काउंटेड इन द नॉट स्टार ऑफ़ पेइंग सब्सक्राइबर्स, समवन—
Speaker 1:  सी, नहीं, ओके.
Speaker 2:  अ— दैट— दैट— इन दिस यूज़ केस, इट इज़ नॉट काउंटेड एज एक्टिवेशन. बट इफ यू लुक एट द—
Speaker 1:  सेम थिंग फॉर डेटा लैब्स. डेटा लैब्स हैज़ अ होम पेज. होम पेज में देयर इज़ प्राइसिंग.
Speaker 2:  हाँ.
Speaker 1:  एंड यू कैन डायरेक्टली परचेस आल्सो. यू कैन साइन अप, डू द व्हाटएवर एक्टिवेशन, एंड देन अपग्रेड.
Speaker 2:  हाँ.
Speaker 1:  और आई कैन जस्ट डायरेक्टली साइन अप फ्रॉम— फ्रॉम डेटा लैब्स का होम पेज आल्सो.
Speaker 2:  हाँ. नाउ, साइनिंग अप कुड बी योर एक्टिवेशन. सी, साइनिंग— एक्टिवेशन कुड बी डिफरेंट.
Speaker 2:  सी, फॉर एग्जांपल, साइनिंग अप कुड नॉट बी एक्टिवेशन. बट साइनिंग अप फॉर योर ट्रायल कुड बी— कुड बी एन एक्टिवेशन मेट्रिक.
Speaker 1:  कांट.
Speaker 2:  हाँ.
Speaker 1:  दैट्स व्हाट एक्सपीरियंस इन द प्रोडक्ट.
Speaker 2:  हाँ.
Speaker 1:  डूइंग दैट कोर एक्शन इज़ द एक्टिवेशन, ना.
Speaker 2:  डूइंग द कोर एक्शन इज़—
Speaker 1:  लाइक इन द एनआरकेस इन डेटा लैब्स, इट्स—
Speaker 2:  इदर व्यूइंग और आस्किंग फॉर डेटा और सम— सम सर्च, व्हिच इज़ हैपनिंग. हाँ.
Speaker 1:  एक्टिवेशन का प्राइमरी कोरिलेशन इज़ रिटेंशन. मोर देन एनीथिंग एल्स.
Speaker 2:  नहीं.
Speaker 1:  लाइक, द वे— लाइक, इफ यू रिसर्च ऑन इट, व्हेन डिफाइनिंग एक्टिवेशन, एंड सपोज़ देयर इज़ नो हार्ड एक्टिवेशन डेफिनेशन.
Speaker 2:  हाँ.
Speaker 1:  यू कैन हैव डिफरेंट एक्शन्स एंड डिफरेंट—
Speaker 2:  अगेन, इट्स अप टू यू प्रोडक्ट एंड हाउ यू एंड अप डिफाइनिंग फ्यू थिंग्स.
Speaker 1:  राइट. सो उसमें, फॉर एग्जांपल, इफ यू डिफाइन फोर-फाइव डिफरेंट वेज़ ऑफ़ एक्टिवेशन, यू कैन मेजर ऑल ऑफ़ दैट. बट द वे टू डिसाइड व्हिच वन टू चूज़ आउट ऑफ़ फोर और फाइव ऑप्शन्स, दैट— इज़ द कोरिलेशन विथ रिटेंशन एट द एंड ऑफ़ द डे.
Speaker 1:  व्हिच ऑफ द एक्टिवेशन— लाइक, वी डिड दैट सेम एनालिसिस फॉर डेटा लैब्स आल्सो.
Speaker 2:  ओके.
Speaker 1:  व्हिच ऑफ द एक्टिवेशन डेफिनेशन्स हैव द बेस्ट कोरिलेशन?
Speaker 2:  विथ—
Speaker 1:  रिटेंशन.
Speaker 2:  हाँ. बट अगेन, दैट इज़ अगेन लीड्स टू पेमेंट.
Speaker 1:  मे लीड, हाँ.
Speaker 2:  नहीं, इवेंचुअल गोल तो वही है, ना, दैट इट लीड्स टू पेमेंट.
Speaker 1:  ठीक है.
Speaker 2:  बट अगेन, इट बाइल्स ऑन टू दैट.
Speaker 1:  हम्म. इट्स अ प्रॉब्लम सेट टू डे, दैट वेदर—
Speaker 2:  एक्टिवेशन— इट शुड बी एक्टिवेशन फॉलोड बाय एक्टिव्स. इट कैन नॉट बी अदरवाइज़.
Speaker 1:  एक्टिवेशन इज़ वन सेपरेट गोल. बट आई गेट योर—
Speaker 2:  नहीं, यू हैव टू चेस एक्टिव्स वन ओनली फॉर पीपल हैव एक्टिवेटेड. इज़ व्हाट आई एम ट्राइंग टू से.
Speaker 2:  इट शुड नॉट बी अदरवाइज़, इज़ व्हाट आई एम ट्राइंग टू कन्वै.
Speaker 1:  ठीक है. अभी के लिए, इफ वी टेक दैट, देन व्हाट चेंजेस?
Speaker 2:  एक्टिवेशन, देन QIA. सॉरी, देन इट विल बी क्यू— क्वालिफिकेशन आइडेंटिफाइड एक्टिवेशन. देन वी विल हैव अ— देन वी विल हैव अ एक्टिव्स, लाइक व्हाट इज़ द रिपीटेड, व्हाट इज़ द एंगेजमेंट रेट.
Speaker 2:  दैट बिकम्स द अदर मेट्रिक टू बी चेस्ड.
Speaker 1:  एक्टिवेशन इज़ नॉट व्हाट आई एम चेसिंग. आई एम चेसिंग—
Speaker 2:  एक्टिव्स.
Speaker 1:  QIA इज़ एक्टिव.
Speaker 2:  और QIA— ए— ए—
Speaker 1:  हाँ, मतलब, दैट— कमिंग बैक टू द सेम वीकली एंगेज्ड आइडेंटिफाइड यूज़र्स. लाइक, प्रीवियस नॉट स्टार वाज़ डब्ल्यूईआईयू.
Speaker 2:  वीकली एंगेज्ड—
Speaker 1:  आइडेंटिफाइड एक्टिव— अ— यूज़र्स.
Speaker 2:  आइडेंटिफाइड यूज़र्स. बट स्टिल, दिस डज़न्ट कवर्स द एक्टिवेशन.
Speaker 1:  वीकली एंगेज्ड आइडेंटिफाइड यूज़र्स. वीकली— नहीं, वी—
Speaker 2:  डब्ल्यूईआईए.
Speaker 1:  वीकली एंगेज्ड एक्टिवेटेड— अ— हाँ, डब्ल्यूईएयू.
Speaker 2:  वीकली एंगेज्ड एक्टिव यूज़र्स.
Speaker 1:  एक्टिवेटेड यूज़र्स.
Speaker 2:  एक्टिवेटेड यूज़र्स.
Speaker 1:  दैट वाज़ माय प्रीवियस वन.
Speaker 2:  बट दिस इज़ आल्सो—
Speaker 1:  इट्स द सेम QIA7 एंड डब्ल्यू— वीकली एंगेज्ड एक्टिवेटेड यूज़र्स इज़ द सेम थिंग, देन. आफ्टर योर चेंज ऑफ़ एक्टिव, ऐडिंग द एक्टिवेटेड.
Speaker 2:  हाँ.
Speaker 1:  बैक टू द सेम नॉट स्टार.
Speaker 2:  अ— बट एनी रीजन वी ड्रॉप्ड इन बिटवीन? और इज़ इट लाइक, नॉट चेसिंग?
Speaker 1:  नहीं, वी— वी हैडेंट इम्प्लीमेंटेड इट ओनली प्रॉपर्ली, बिकॉज़ दैट वाज़ द लास्ट डेफिनेशन बिफोर द वन इनफॉर्मेटिव डिस्कशन. थ्री मंथ्स अगो, दैट आई मेड लास्ट. बट वी हैडेंट इम्प्लीमेंटेड इट.
Speaker 2:  अच्छा.
Speaker 1:  एज़ अ मेट्रिक टू चेस.
Speaker 2:  अच्छा.
Speaker 1:  वी वर सपोज़्ड टू, बट वी वांट— वी हैडेंट येट.
Speaker 2:  अच्छा. वीकली एंगेज्ड एक्टिवेटेड यूज़र.
Speaker 1:  ठीक है, वो फॉरगेट दैट. डज़न्ट मैटर. QIA पे ही रहते हैं.
Speaker 1:  लेट्स कीप इट द सेम.
Speaker 2:  हाँ.
Speaker 1:  सिंस वी इंट्रोड्यूस्ड इट, लेट्स कीप टू दैट. अगर अगेन—
Speaker 2:  नहीं, दैट बिकम्स टू मच टू इंटरनली ओनली. हाँ. सो.
Speaker 1:  एनी अदर एज केसेस इन दिस? और एनी अदर डाउट साइड ऑफ़ दिस?
Speaker 2:  नहीं, यही मेजर है. इट शुड स्टार्ट फ्रॉम एक्टिवेशन, फॉलोड बाय द अदर सेट ऑफ़ थिंग्स. और इट कुड बी— व्हाइल आई एम थिंकिंग अलाउड, एनीवेज, राइट नाउ, वी मेड आवर ऐप सो एडिटोरियल फ्रेंड.
Speaker 2:  तो पीपल कमिंग एंड रीडिंग अ न्यूज़ कुड बी अ—
Speaker 1:  इज़ दैट अ साइन ऑफ़ रिटेंशन? लाइक, आई डोंट माइंड चेंजिंग द एक्टिवेशन डेफिनेशन. गिव मी द नंबर फॉर रिटेंशन.
Speaker 2:  नहीं, वैसे—
Speaker 1:  कोरिलेशन विथ रिटेंशन.
Speaker 2:  नहीं, पीपल हु आर कमिंग टू एक्सप्लोर पेज आर एंगेजिंग मोर. एंगेजमेंट ज्यादा है, बिकॉज़ देयर आर टू मेनी थिंग्स टू एंगेज, एंड पीपल आर कमिंग बैक.
Speaker 1:  एंगेजमेंट आल्सो देयर. रिटेंशन हैयरली.
Speaker 2:  हाँ.
Speaker 1:  रिटेंशन हैयरली.
Speaker 2:  रिटेंशन सेम— सिमिलर है, बट एक्सप्लोर पेज थोड़ा ज्यादा है.
Speaker 1:  रिटेंशन.
Speaker 2:  रिटेंशन, हाँ, थोड़ा सा ज्यादा है, लाइक 5-2%, 5% टाइप्स.
Speaker 1:  देन यू हैव टू— देन द ब्रीफ कॉन्सेप्ट विल हैव टू बी डीप प्रायोरिटीज.
Speaker 2:  नहीं, सी, इट्स अबाउट हाउ डू वी— राइट नाउ, इट इज़— आई एम नॉट एबल टू वॉच ऑन इट, बिकॉज़ ऑफ़ द फैक्ट दैट इट इज़ नॉट बीन कन्वेड इन द वे. व्हिच इज़ व्हाई आई एम नॉट डीप—
Speaker 1:  आई गेट इट.
Speaker 2:  हाँ. प्रॉबब्ली, व्हाट वी कैन डू इज़ प्रॉबब्ली— अ— आई विल—
Speaker 1:  नहीं, ठीक है. सो QIA— सी, एक बार जस्ट टेक एनी अदर एज केसेस और पोटेंशियल इश्यूज़ ऑफ़ एक्टिव बीइंग— मतलब, QIA हैविंग एक्टिवेटेड ओनली यूज़र्स. नाउ, जस्ट वॉन्ट चेंज द नेम.
Speaker 2:  हाँ.
Speaker 1:  जस्ट डिफाइन इट कि हाँ, दे आर एक्टिवेटेड ऑलरेडी, एंड ओनली देन विल दे बी काउंटेड इन QIA.
Speaker 2:  हाँ. आई विल ट्राइ टू क्लोज़ दिस लॉजिक. इफ रिक्वायर्ड.
Speaker 1:  पर इसका एज केस अगर और कोई इश्यूज़ है, वो एक बार डबल चेक कर लेना.
Speaker 2:  हाँ. एंड हाउ वी आर गोइंग टू एनेबल मार्केटिंग टीम बाय यूनिफाइंग इज़ आल्सो समथिंग आई विल— अ— कंसिडर. एनीवेज, इंडिविजुअल प्रॉपर्टीज़ इवेंट्स, इट इज़ गेटिंग फिक्स्ड.
Speaker 2:  देयर इज़ नो डाउट इन दैट. हाउ डू वी यूनिफाई वर्कस्पेस?
Speaker 2:  ओबी—
Speaker 1:  उसमें अभी जो एनवायरमेंट वाले पॉइंट में एक्टिवेशन डेफिनेशन इज़ ओपन, मैं यही वाला पॉइंट था। कि QIA में एक्टिवेशन है या नहीं है, दैट्स द—
Speaker 2:  नहीं, नहीं, नहीं. एक्टिव— नहीं, इन जनरल, एक्टिवेशन क्या होगा?
Speaker 1:  ओह.
Speaker 2:  क्या होगा?
Speaker 1:  किसका?
Speaker 2:  इन जनरल. 1942. सो अभी—
Speaker 1:  1942, हाँ. 1942 एक्टिवेशन इज़ हार्ड. अभी वो उसका आंसर किसी के पास नहीं है.
Speaker 2:  हाँ, किसी के पास नहीं है. सो व्हिच इज़ व्हाई आई मेंशंड नेथियम दैट इट शुड बी प्रोडक्ट-स्पेसिफिक एक्टिवेशन, बिकॉज़ आवर एंटायर इकोसिस्टम इज़ नॉट बिल्ट इन द सच अ वे, एटलीस्ट नाउ. इवेंचुअली, वी आर हेडिंग टू द डायरेक्शन.
Speaker 2:  सो इट हैज़ टू बी प्रोडक्ट-स्पेसिफिक. सो उसका पॉइंट है कि वी विल हैव वन मेट्रिक, व्हिच इज़ 1942.
Speaker 2:  पीपल हैव रेड थ्री और मोर आर्टिकल्स. टू व्हिच द कॉन्ट्राडिक्शन पॉइंट वाज़, आर वी गोइंग टू डिसरेगार्ड फॉर पीपल हु आर यूज़िंग डेटा लैब्स, और डिसरेगार्ड पीपल हु आर कंप्लीटिंग द ब्रीफ.
Speaker 2:  दैट्स व्हेन आई हैड अ कॉन्ट्राडिक्टर पॉइंट. सो आई थॉट ऑफ़ लेट हिम कम बैक विथ हिज़ ओपिनियन.
Speaker 1:  इंडिविजुअल होना चाहिए. अभी तो वी गिव इट.
Speaker 2:  हाँ. बिकॉज़—
Speaker 1:  बिकॉज़ इंडिविजुअल एक्विज़िशन सरफेस इज़ देयर. बिकॉज़ कैंपेन विल नॉट बी कि कम टू 1942 एंड कम इन एनी पार्ट.
Speaker 2:  हाँ. इट विल बी प्रोडक्ट-स्पेसिफिक.
Speaker 1:  प्रोडक्ट-स्पेसिफिक, फॉर नाउ. टिल द टाइम वी—
Speaker 2:  मैच्योर आवर प्रोडक्ट इन सच अ वे, दैट इट्स— इट्स वन.
Speaker 1:  अभी तो इंडिविजुअल एक्टिवेशन है, एंड इन्फोट्यूड डज़ नॉट हैव अ एक्टिवेशन मेट्रिक.
Speaker 2:  एज़ अ मेट्रिक, हाँ.
Speaker 1:  एज़ अ फ्लो.
Speaker 2:  आई नो.
Speaker 1:  इन्फोट्यूड का वी हैव टू क्रिएट समथिंग.
Speaker 2:  हाँ. सो आई पुट ऑल दिस थॉट्स इन हिज़ माइंड, फॉर हिम टू कम बैक. आई डोंट वांट टू गिव एनी इमीडिएट आंसर्स, तो लेट हिम कम बैक.
Speaker 2:  बट दैट—
Speaker 1:  इंडिविजुअल.
Speaker 2:  हाँ, आईडियली तो इंडिविजुअली, बट हाँ.
Speaker 1:  तो इंडिविजुअली होगा.
Speaker 2:  हाँ. बट एक्टिवेशन और एक्टिव्स इज़ समथिंग— इफ रिक्वायर्ड, आई विल डू सम प्रॉबब्ली फॉर नेक्स्ट टू आवर्स.
Speaker 1:  उस एज केसेस चेक कर लो. आई एम फाइन विथ QIA बीइंग ओनली फॉर एक्टिव्स. इट रिड्यूसेस—
Speaker 2:  एक्टिवेशन.
Speaker 1:  हाँ, इट रिड्यूसेस योर बेंचमार्क अ लिटिल लोअर. बेसलाइन अ लिटिल लोअर.
Speaker 2:  नहीं, नहीं, इट रिड्यूसेस लोअर, बट इट— नहीं, नहीं. इट— हाँ, इट रिड्यूसेस लोअर, बट द एफर्ट इज़ मच हायर राइट नाउ.
Speaker 1:  नहीं, बिकॉज़ योर बैकफिल्ड में यू विल नॉट गेट एक्यूरेटली वेदर दे आर एक्टिवेटेड ऑर नॉट. योर बिगेस्ट चैलेंज शुड बी दैट.
Speaker 2:  हाँ.
Speaker 1:  एंड बैकफिल्ड के बेसिस पे, योर बेसलाइन नंबर विल बी हाई.
Speaker 2:  हाँ.
Speaker 1:  एंड योर अपकमिंग एक्विज़िशन नंबर्स विल बी लोअर.
Speaker 2:  बैकडेट में आई विल—
Speaker 1:  बिकॉज़ बैकडेट में, फॉर एग्जांपल, टुडे, हाइपोथेटिकली, इफ आई से देयर आर 20,000 QIAs, अ— देन इफ— इफ द बेसलाइन नंबर इज़ हायर, से 20,000.
Speaker 2:  बट यू विल लुक एट— नहीं, उसका—
Speaker 1:  एंड देन आई से, लेट्स रीच 50,000. वर्सेस— बिकॉज़ वी कुड एक्यूरेटली से वेदर दे वर एक्टिवेटेड और प्रॉपर्ली और नॉट.
Speaker 2:  बट, हाँ.
Speaker 1:  बट, एंड गोइंग फॉरवर्ड, योर एक्टिवेशन इज़ एट अ सर्टेन रेट ओनली, ऑफ व्हिच यू हैव टू रिटेन पीपल.
Speaker 2:  हाँ.
Speaker 1:  सो दैट एडिशन विल बिकम हार्डर.
Speaker 2:  हाँ. वो तो होगा. दैट बिकम्स इवन मोर चैलेंजिंग ऑफ हाउ डू वी गो अबाउट इट.
Speaker 2:  बट इसमें— अ—
Speaker 1:  बट गोल सेटिंग कैन स्टिल बी डन. ठीक है, चलेगा. बेसलाइन कैन स्टिल बी देयर.
Speaker 1:  बेसलाइन कैन स्टिल बी हायर. गोल सेटिंग विल हैव टू बी डन इन सच अ वे.
Speaker 2:  नहीं, ऐसे कहते हैं ना, इवेंट टू सिंपलीफाई दिस.
Speaker 1:  बेंचमार्क इट फ्रॉम एक्टिवेशन.
Speaker 2:  हाँ.
Speaker 1:  अभी ऑनगोइंग लास्ट एक महीने में, या नेक्स्ट वन मंथ में, फॉर एग्जांपल, वंस योर इवेंट्स आर आल्सो फ्लेम्स. देन यू सेट द बेसलाइन ऑफ़ टारगेट नंबर.
Speaker 2:  नहीं, बट ऐसे करते हैं ना, लेट्स मेक अप हैव अ प्रॉपर फंड, रादर देन दिस एंटायर कॉम्प्लिकेशन. अवेयरनेस, एक्विज़िशन, एक्टिवेशन. और री-डिफाइनिंग द फंड, लेट्स से, अवेयरनेस, एक्विज़िशन.
Speaker 2:  अ— इसमें ऑनबोर्डिंग कंप्लीटेड, देन एक्टिवेशन.
Speaker 1:  वही तो है. डिफरेंस क्या है?
Speaker 2:  नहीं, इट्स अ कं— कॉम्बिनेशन ऑफ़ एवरीथिंग. नाउ, एक्ट— नाउ, एक्टिव्स और एक्टिवेशन.
Speaker 1:  हम्म.
Speaker 2:  सो दैट— QIA इज़ एक्टिव और एक्टिवेशन राइट नाउ.
Speaker 1:  एक्टिवेटेड यूज़र्स का ही QIA है, लाइक यू सेड.
Speaker 2:  हाँ, फिर ठीक है. हाँ, इफ—
Speaker 1:  वो चेंज नहीं, वो उसमें चेंज नहीं करते.
Speaker 2:  नहीं, यू मेंशन ए इज़ एक्टिव्स. आई एम सेइंग एक्टिवेटेड यूज़र.
Speaker 1:  नाम इज़ एक्टिव्स ओनली. डेफिनेशन में अंडरस्टुड है कि एक्टिवेटेड यूज़र्स का ही एक्टिव्स है.
Speaker 2:  हाँ, फिर ठीक है.
Speaker 1:  वो डिफाइन कर लो. बट नेम इज़ स्टिल एक्टिव्स ओनली.
Speaker 2:  हाँ, फिर ठीक है. एज़ लॉन्ग एज़ वी आर मेंटेनिंग दैट नोमेनक्लेचर, देन इट मेक्स—
Speaker 1:  यू कैन से कि हाँ, दे आर एक्टिवेटेड इन वन ऑफ़ द सरफेसेस, एंड ओनली देन दे विल बी कंप्लीटेड इन QIA.
Speaker 2:  हाँ. देन दिस मेक सेंस. इट हैज़—
Speaker 1:  देन यू विल हैव टू क्रिएट वन मोर मेट्रिक.
Speaker 2:  व्हिच इज़ हाउ मेनी इज़—
Speaker 1:  ओनली QIA.
Speaker 2:  हाँ, ओनली QIA.
Speaker 1:  ओनली QIA.
Speaker 2:  ओनली QIA. फर्स्ट वन इज़ ओनली आईए.
Speaker 1:  वो तो है ही. वो तो ऑलरेडी था. बट नाउ देयर इज़ अ QIA आल्सो.
Speaker 1:  हु क्वालिफाइड एंड आइडेंटिफाइड, बट आर नॉट एक्टिवेटेड.
Speaker 2:  बट आर एक्टिव्स.
Speaker 1:  बट आर एक्टिव्स.
Speaker 2:  नहीं, नहीं, इफ देयर— ओके.
Speaker 1:  एंड देन देयर इज़ QIA ओनली, व्हिच हु नॉट एक्टिवेटेड एंड नॉट एक्टिव, बट आर QIA.
Speaker 2:  हाँ, बट आर QIA. हाँ, वो तो ऑब्वियस है, वो तो हो जाएगा. हाँ.
Speaker 2:  नहीं, दैट्स हाउ इंटरेस्टिंग इज़ द प्रॉब्लम टू सॉल्व आल्सो, ना. तो मुझे हो जाएगा.
Speaker 1:  तो फिर ये सारे ग्रिड बनानी पड़ेगी.
Speaker 2:  हाँ. हाउ— व्हाट डू वी कॉल हाउ— वो तो ग्रिड आई विल क्रिएट इट राइट नाउ, ओनली. क्लोज़ इट.
Speaker 2:  इफ रिक्वायर्ड, एक बार वी कैन कनेक्ट अगेन ओवर अ कॉल, वर्चुअली और—
Speaker 1:  का एक्टिवेशन इज़ क्लियर. आपका एक्टिवेशन फॉर नाउ इज़ क्लियर. इन्फोट्यूड डज़ नॉट हैव एन एक्टिवेशन डेफिनेशन, व्हिच यू विल हैव टू सेट.
Speaker 2:  हाँ, टू और मोर आर्टिकल्स फॉर नाउ, और आई विल ट्राइ टू क्रिएट फ्यू थिंग्स, तो उसमें भी—
Speaker 1:  हाँ, वो एक बार एनालिसिस करके देखना. बट टू और मोर तो नहीं हो सकता आर्टिकल.
Speaker 2:  आई विल कम बैक विथ— यू सेइंग इट इज़ हायर और लेसर.
Speaker 1:  मतलब—
Speaker 2:  और इट्स नॉट—
Speaker 1:  दे हैव टू साइन अप. और दे हैव टू गिव देयर— मतलब, दे हैव टू बी आइडेंटिफाइड फर्स्ट.
Speaker 2:  हाँ.
Speaker 1:  उसके बाद टू और मोर इज़ नॉट. टू और मोर आफ्टर आइडेंटिफिकेशन.
Speaker 2:  हाँ, वैसे—
Speaker 1:  नॉट बिफोर.
Speaker 2:  वैसे हो जाएगा, ना.
Speaker 1:  आइडेंटिफाई पहले होना पड़ेगा. उसके बाद टू और मोर.
Speaker 2:  नहीं, नॉट नेसेसरी, ना.
Speaker 1:  सो तुम्हारा बेस विल बी वेरी हाई.
Speaker 2:  नहीं, नहीं, इट कुड बी उल्टा इज़ व्हाट आई एम सेइंग. एक्टिवेटेड, देन आइडेंटिफाइड. देयर इज़ नो रॉन्ग इन इज़ व्हाट आई एम सेइंग.
Speaker 2:  आज— आई एम नॉट ओनली टॉकिंग अबाउट एक्टिवेटेड यूज़र्स. इफ प्रोवाइडेड एक्टिवेशन— वैसे, हमारा एवरेज तो 67% स्क्रॉल डेप्थ है.
Speaker 1:  यू ओनली सेड ना कि द फंड हैज़ टू वर्क इन वन वे.
Speaker 2:  हाँ.
Speaker 1:  फंड हैज़ टू वर्क इन वन वे. तो दे हैव टू फर्स्ट साइन अप. डेटा लैब्स में भी दे हैव टू फर्स्ट साइन अप.
Speaker 1:  ऐप में आल्सो दे हैव टू फर्स्ट साइन अप. आर यू कंसीडरिंग पीपल हु आर— हु आर नॉट साइंड अप इन द ब्रीफ कंप्लीशन?
Speaker 2:  बट—
Speaker 1:  एक्टिवेशन डेफिनेशन.
Speaker 2:  ब्रीफ कंप्लीशन इन द ऐप, इफ दे आर नॉट साइंड इन—
Speaker 1:  इज़ एक्टिवेशन इन— इन द ऐप? हाँ, ऐप में तो है एक्चुअली. बोथ आर ऑप्शंस आर देयर.
Speaker 2:  नहीं, इट देयर— नहीं, देयर आर— हाँ, बट देयर आर एन एक्टिवेटेड यूज़र, ना.
Speaker 1:  दे कैन बी एक्टिवेटेड विदाउट साइनिंग अप.
Speaker 2:  हाँ.
Speaker 1:  बट ऐप इज़ अ डिफरेंट यूज़ केस. ऐप ऑलरेडी दे हैव पुट इन द एफर्ट ऑन डाउनलोडिंग द ऐप.
Speaker 2:  हाँ. बट वेबसाइट में तो इतना नहीं है. दे कम फ्रॉम एनी— एनी अदर—
Speaker 1:  राइट.
Speaker 2:  10 डिफरेंट सोर्सेस.
Speaker 1:  राइट. वेबसाइट— ऐप में दे ऑलरेडी पुट इन द एफर्ट ऑन—
Speaker 2:  ऑन डाउनलोडिंग, हाँ.
Speaker 1:  दैट इज़ ऑलरेडी अ कमिटमेंट इनफ.
Speaker 2:  हाँ.
Speaker 1:  वेबसाइट हैज़ नो कमिटमेंट. वेबसाइट विल रिक्वायर अ हायर बेंचमार्क.
Speaker 2:  सो बिकॉज़, वैसे, ट्रैफिक वैसे ज्यादा है.
Speaker 1:  राइट.
Speaker 2:  हाँ. सो व्हाट आई विल डू इज़, आई विल ट्राइ टू क्रिएट अ ग्रिड, एंड वी विल ट्राइ टू क्लोज़ इट टुडे. फ्रॉम माय साइड तो आई विल क्लोज़ इट.
Speaker 2:  इफ रिक्वायर्ड, वी कैन गेट ऑन— गो ओवर अ कॉल, अगर— इफ यू आर अवेलेबल ड्यूरिंग द— राइट. तो एक बार क्लोज़ करते हैं.
Speaker 2:  फिर कुछ और पॉइंट्स हैं फ्रॉम योर साइड?
Speaker 1:  नहीं, वो मुझे तो तुम्हारे यहाँ—
Speaker 2:  नहीं, मुझे तो सिर्फ डिज़ाइन के लेके आया. अ— वैसे, यू हैड अ जेन्युइन चैटल डिस्कशन विथ सत्या?
Speaker 1:  नहीं.
Speaker 2:  अच्छा.
Speaker 1:  अभी है?
Speaker 2:  हाँ, सत्या है.
Speaker 1:  अभी तो नहीं.
Speaker 2:  कुछ आपको इन्फॉर्म करना था. कल फर्स्ट हाफ में ना, मैं शूट पे जा रहा हूँ. शान सर का लैब्स का शूट है.
Speaker 2:  ही नीड्स अ लिटिल हेल्प. तो आई वास लाइक कि ठीक है, मैं चलता हूँ.
Speaker 2:  करने को, करने को वो कह रहे हैं कि बस वहाँ पे और कोई शूट के लिए होता नहीं है. प्लस, अगर कुछ सामने हम दो लोग हो सके तो थोड़ा बेटर हो सकता है.
Speaker 2:  प्लस, थोड़ा अगर बता सके तो. तो आई वास लाइक, ठीक है, मैं चलता हूँ.
Speaker 2:  दो घंटे, तीन घंटे जीते हैं. उसको 11-12 बजे के आसपास जाके 2 बजे तक वापस आ जाऊँगा.
Speaker 1:  ठीक है.
Speaker 2:  तो प्रीवियस वाला वर्क जो है, वो तो अलाइन करेंगे, बेसलाइन बेसलाइन पर.
Speaker 1:  अरे यार, अभी तो इसी केस में डीएफपी—
Speaker 2:  हाँ, उसकी तो अब सारी चीज़ें अलाइन हो गई हैं. डीड्यूसी रिट्रीट का, बिकॉज़ मैंने फास्ट इन अ प्रोसेस करा दिया था. अब उसकी 8-9 वीडियोस बन गई हैं, जो रेडी हो के आ चुकी हैं.
Speaker 2:  तो अब उसके अवेयरनेस ऐड्स, वो सेम, वो स्टार्ट करा रहे हैं.
Speaker 1:  नए लोगो.
Speaker 2:  करा दिया.
Speaker 1:  नए— नए लोगो इनकॉरपोरेट कर रहे हैं.
Speaker 2:  इन द एंड स्क्रीन रहता है, राइट. वो कराना है.
Speaker 1:  वेबसाइट पे पहले चेंजेस और फिर सारे एसेट्स.
Speaker 2:  हाँ, वो सारा कल मॉर्निंग में मैक्सिमम सब टर्म हो जाएगा. वो सारा कुछ.
Speaker 1:  हाँ.
Speaker 2:  दिस रिमाइंड्स मी वन मोर थिंग. आई गॉट अ इनवाइट फॉर स्लैक, फॉर— दे आर होस्टिंग देयर समिट— नॉट समिट, द प्रोडक्ट लॉन्च इन एरोसिटी.
Speaker 1:  ओके.
Speaker 2:  हाँ, फोर्थ— अ— थर्सडे, 4:30 टू 8:30, फॉर आवर इवेंट. सो आई थॉट ऑफ जॉइनिंग— अ—
Speaker 1:  वर्चुअल और ओनली फिजिकल.
Speaker 2:  हाँ.
Speaker 1:  स्लैक इज़ डूइंग सम व्हाट— व्हाट प्रोडक्ट लॉन्च?
Speaker 2:  देयर ओन प्रोडक्ट लॉन्चेस, कुछ. एवरी— एवरी—
Speaker 1:  इफ इट्स यूज़फुल, देन गो. इफ इट्स नॉट, देन स्किप. इफ इट्स यूज़फुल, देन गो.
Speaker 1:  नॉट एन इशू.
Speaker 2:  हाँ. मुझे ऐसे थोड़ा— सी व्हाट्स हैपनिंग टाइप. बट ठीक है.
Speaker 1:  हाँ, आई कैन गो.
Speaker 2:  उसमें— अ— अ— गौरव रिमाइंडेड मी दैट टू— वी आर लेफ्ट विथ टू डेज़ फॉर मोहंगेज का क्लोज़र.
Speaker 1:  टू डेज़ क्यों? ओह, द डेडलाइन.
Speaker 2:  हाँ, डेडलाइन.
Speaker 1:  उससे बात हुई?
Speaker 2:  आई हैव ट्राइड कॉलिंग हिम. अ— डजंट एंड अप डिस्कसिंग. आई मीन, ही डिडंट आंसर द कॉल.
Speaker 2:  ही सेड ही विल कॉल मी बैक.
Speaker 1:  व्हाट्सएप कर दिया?
Speaker 2:  कर दिया मैंने. देन आई थॉट आई विल एटलीस्ट इनिशियल द थ्रेड, सेइंग देट आई ट्राइड कॉलिंग यू. एटलीस्ट टू कन्— सो दैट इट्स रिकॉर्ड ऑन रिकॉर्ड.
Speaker 2:  आई विल जस्ट वेट फॉर हिम टुनाइट. इफ— इफ देयर इज़ नो रिप्लाई, एटलीस्ट इनिशियल द न्यू ईमेल थ्रेड, सेइंग दैट आई ट्राइड रीचिंग यू.
Speaker 2:  लेट मी नो व्हेनएवर टू डिस्कस और समथिंग. हाँ.
Speaker 2:  सो दिस इज़ व्हाट—
Speaker 1:  उसके बाद अभी नहीं मिला ना कुछ?
Speaker 2:  नहीं मिला. आई कॉल्ड वन ऑफ द गाय फ्रॉम माय प्रीवियस ऑर्डर. आई गॉट— आई गॉट अ कॉन्टैक्ट.
Speaker 2:  ही सेड, राइट नाउ इट इज़ वेरी डिफिकल्ट फॉर हिम टू हेल्प. बट मैंने सोचा कुछ कर लो.
Speaker 1:  अ— अ— पोर्टल का एक्सेस मिल गया था?
Speaker 2:  नहीं.
Speaker 1:  पोर्टल का तो आई डिड—
Speaker 2:  नहीं, आई— आई हैव नॉट गॉट मेल आल्सो.
Speaker 1:  डायरेक्टली ट्राइ साइनिंग अप. portal.azure.com.
Speaker 2:  वैसे— ठीक है.
Speaker 1:  हाँ, उसको— मतलब, दैट इज़ व्हाई इट्स वेरी वियर्ड एंड कॉम्प्लिकेटेड.
Speaker 2:  मतलब, इट टेक्स— आई डोंट नो. इट्स नॉट क्लियर व्हाट— हाउ— व्हाट इज़ द राइट प्रोसेस फॉर इट. इट्स वेरी— एंड वेरी कॉम्प्लिकेटेड.
Speaker 1:  ठीक है, इससे पहले ये करें. अ— एक बार ये तो इनके साथ— ऐप डिज़ाइन पे एक बार बैठ के ही जाते हैं ना.
Speaker 2:  हाँ.
Speaker 1:  स्टूडेंट आल्सो.
Speaker 2:  शुड आई कम देयर?
Speaker 1:  जाओ.
Speaker 2:  हाँ, सो दिस इज़ द इनवाइट, व्हिच आई गॉट.
Speaker 2:  इसने बोला देयर आर लॉट ऑफ प्रोडक्ट मैनेजर्स कमिंग इन. तो इसको— हाँ, कैन गो लेट.
Speaker 1:  डेली में एवरीथिंग इज़ एनीवेज लेट.
Speaker 2:  हाँ.
Speaker 1:  गो बाय स्तर.
Speaker 2:  हाँ.
Speaker 1:  मेनली इज़ एनीवेज लेट.
Speaker 2:  वैसे, हाँ, द इनिशियल सेट ऑफ थिंग्स आर नॉट दैट मच. 6, 6:30, 7 आल्सो. 7 तो थोड़ा एंड हो गया, बट हाँ, 6, आई बिलीव, समवेयर. 
Speaker 2: ठीक है.
Speaker 2:  इश अक्षय— अक्षय इज़ आल्सो कमिंग?
Speaker 1:  इट्स नॉट— बट मे बी माइट अपॉन.
Speaker 2:  अच्छा. ओ, यू मीन टू पिंग हिम और लेट?
Speaker 1:  हाँ.
Speaker 2:  एक मिनट, गेट हिज फोन नंबर.
