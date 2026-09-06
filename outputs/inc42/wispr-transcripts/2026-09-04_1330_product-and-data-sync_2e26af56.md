# Product & Data Sync

- Wispr meeting id: 2e26af56-99eb-468a-88d1-1310f756a434
- Start: 2026-09-04 13:30 IST (08:00Z) · End: 14:00 IST
- Attendees (calendar): Ashish Sharma, Prapti Rastogi, Ranjith M, Utkarsh Agarwal (organizer)
- Share link: https://notes.wisprflow.ai/shared/0qW-XD3k6pMyAVMPydoXKcUmWfruS0Rz8Om9Ay1rDVI
- Archived from Wispr Flow via MCP on 2026-09-06, before notetaker access was removed. Transcript is verbatim ASR output; speaker labels are Wispr's and are sometimes mis-assigned.

## Wispr summary

Team sync covering warehouse enrichment, agentic playbooks, server/GCP consolidation, event audit, and QIA measurement. Ranjith to drive QIA instrumentation, Azure credits outreach, and app design/logic docs.

### Warehouse Enrichment & Onboarding Fields
- Email split: 36% work, 64% personal; enrichment via LinkedIn where present, else name + company
- Apollo to be used, but personal-email coverage limited; company name likely improves enrichment rate
- Prapti Rastogi to identify which field combinations most boost enrichment, to inform onboarding trade-offs

### Agentic Playbooks & Bootstrap Enrichment
- Social playbooks in final testing; evals built per 42 use cases across verticals
- Bootstrap enrichment scaling from 10k to ~60k companies; optimizing API calls to avoid blocks

### Server, GCP & Event Audit
- Phase 1 server work done; Phase 2 auto-scaling + cost optimization being scoped by vendor
- GCP remaining: BigQuery instance and Slack meeting app; forecast ~72,000
- Ranjith shared audit sheet of events (not firing, duplicates, missing properties); Ashish Sharma reviewing before fixes

### QIA Metric & App Design
- Lock measurability, baseline, and dependencies of QIA before deciding ownership; measure both QIA 7 and QIA 30
- App designs (explore article, dark mode) expected by Monday; team aiming Wednesday delivery

### Azure Credits
- LinkedIn outreach via Varun and Ranjith yielding no positive response so far
- Square Ops may offer additional discount if billing routed through them; reserved-instance style options to explore

### Next Steps
- (Utkarsh Agarwal) Run monthly SEO/data labs analysis this weekend once doc updates land
- (Utkarsh Agarwal) Figure out Azure owner/billing permissions to grant Ranjith access
- (Ashish Sharma) Review Ranjith's event audit sheet and kick off fixes with team
- (Ashish Sharma) Deploy pending frontend FAQs/tests for data labs SEO
- (Ashish Sharma) Raise Azure support thread for startup credits, mark Utkarsh Agarwal and Ranjith
- (Prapti Rastogi) Share cap table / valuation in-app blog ideations with Utkarsh Agarwal
- (Prapti Rastogi) Brief Ranjith on which data points most improve enrichment accuracy
- (Ranjith M) Share QIA qualification profile list and initiate Mayank contact for mowing age discussion

### Decisions Made
- Measure both QIA 7 and QIA 30, then decide ownership
- Prioritize QIA instrumentation and measurability before assigning ownership

## Transcript

Prapti Rastogi: Quickly. Uh, so first, on the warehouse front, अभी हम enrichment वाली activity plan कर रहे हैं, जिसमें— अभी तो basically मैंने bifurcation निकाला है कि personal versus work emails कितने हैं। तो we have, um, 36% work and 64% personal.
Prapti Rastogi:  तो अभी, भाई, उसके around I'm planning कि on the basis of what other data points we can enrich, and कौन सा third-party tool use करके हम इसका enrichment better plan कर सकते हैं। तो उसी के around अभी चल रहा है।
Prapti Rastogi:  इसके अलावा कुछ— today I'll be starting the entity-type classification as well. And Utkarsh, अभी Bootstrap companies का enrichment is going on.
Prapti Rastogi:  अभी उसमें हम थोड़ा optimization कर रहे हैं, because since अभी हम काफी heavy extraction करेंगे। क्योंकि अभी last time तो हमने total 10k निकाली थी, and अभी इसमें हमारे plan में almost 60k companies हैं।
Prapti Rastogi:  तो we need to plan कि हम कितनी API calls कर रहे हैं। तो थोड़ा उसमें optimization चल रहा है, so that we don't get blocked.
Prapti Rastogi:  तो एक ये वाला part है। और दूसरा, Utkarsh, आपने जो मुझे cap table and valuation पे in-app के लिए बोला था, वो मैंने उसका एक blog बनाया है।
Prapti Rastogi:  तो उसमें अभी मैंने 3-4 ही, मतलब, ideations सोचे हैं कि who owns this company, valuation trajectory दिखा सकते हैं, या founder dilution curve दिखा सकते हैं। तो उसके around ही मैंने कुछ-कुछ ideas सोचे हैं।
Prapti Rastogi:  तो एक बारी वो मैं share करती हूँ आपके साथ।
Utkarsh Agarwal:  समझ गया।
Prapti Rastogi:  हाँ जी।
Utkarsh Agarwal:  इसमें जो ये 60k वाला था, वो कौन से वाले point था?
Prapti Rastogi:  Uh, Utkarsh, जो Bootstrap company का हम enrichment कर रहे हैं ना, sorry, enrichment से मेरा मतलब था data completeness।
Utkarsh Agarwal:  समझ गया।
Prapti Rastogi:  हाँ जी।
Utkarsh Agarwal:  Got it. Got it. 
Utkarsh Agarwal: ठीक है। And जो ये warehouse में enrichment का अभी हम approach देख रहे हैं, वो हम किस तरह से देख रहे हैं?
Prapti Rastogi:  Utkarsh, अभी तो मैंने यही करा है कि अभी तो मैंने bifurcation निकाला है कि work emails and personal. अब personal में भी जितनों में LinkedIns हैं, तो LinkedIn के via enrichment हो जाएगा उनका। जिसमें LinkedIn नहीं है, सिर्फ company name present है, तो उसके लिए फिर हम एक अलग route लेंगे।
Prapti Rastogi:  उनका LinkedIn identify करने की कोशिश करेंगे via their primary, मतलब, their name and their company name। तो उसी के basis पे अभी मैं multiple permutations and combinations बना रही हूँ कि हम कैसे-कैसे identify कर सकते हैं user को, and then creating that whole loop of enrichment।
Utkarsh Agarwal:  Makes sense. Just one point here, Prapti—
Prapti Rastogi:  हाँ जी, बिल्कुल।
Utkarsh Agarwal:  There's an Apollo tool which I mentioned. So—
Prapti Rastogi:  Apollo ना?
Ranjith M:  हाँ। उसमें there are multiple ways you can do enrichment. Either by sending email id, I mean work email, or second is either sharing their name, email id, and company name.
Ranjith M:  It will give you the LinkedIn profile, it will give you the— all the other details. It could be one of the easiest ways, because they also have the APIs and everything, which is—
Utkarsh Agarwal:  Apollo, but actually, Ranjith, Apollo पे personal email ids का coverage बहुत small रहता है। I've been using Apollo from a very long time. Good idea.
Prapti Rastogi:  But उसमें—
Utkarsh Agarwal:  But using the company name, I think इसका enrichment rate थोड़ा better होगा, is what I'm—
Prapti Rastogi:  हाँ, हाँ, हाँ। तो उसपे भी, उसको, मतलब, Apollo तो I will use only। Apollo I've been using earlier also।
Prapti Rastogi:  Apollo तो आएगा ही इस loop में। बाकी एक बारी और देख सकते हैं कि कैसे उसको utilize कर सकते हैं।
Prapti Rastogi:  हाँ। इसमें एक चीज़ और, Prapti, वो हम एक बार Ranjith के context में एक बार ले सकते
Utkarsh Agarwal:  हैं कि क्या data points help in overall enrichment। मतलब, for example, अगर हमारे पास name and, मतलब, personal email id है, और उसके साथ अगर hypothetically अगर company name मिल जाता है, तो हमारा वो कितना accuracy बढ़ जाती है enrichment की, person without। So basically जो भी combination of fields हैं, जिससे हमारी enrichment capabilities और बढ़ जाती हैं, that will help us define the onboarding में हम क्या trade-offs लें, in terms of fields to optimize for।
Utkarsh Agarwal:  Got it, Utkarsh। हाँ, मैं इस, मतलब, इसके हिसाब से मैं एक बारी Ranjith को बता दूँगी कि कौन से data points हमारे लिए truly valuable होंगे, in terms of कि हम आगे भी onboarding में क्या कर सकते हैं।
Utkarsh Agarwal:  I got your point। Right, right.
Utkarsh Agarwal:  Makes sense. 
Utkarsh Agarwal: ठीक है। ठीक है। और कोई points यहाँ पे?
Prapti Rastogi:  नहीं, Utkarsh, अभी broadly यही, मतलब, यही तीन-चार चीज़ों पे ही काम चल रहा है। एक बारी मैं आपके साथ share करती हूँ, once these things are logged।
Utkarsh Agarwal:  समझ गया। ठीक है। 
Utkarsh Agarwal: ठीक है। And social वाला जो अपना था, वो भी हमारा final, वो playbooks वाला part चल रहा है?
Prapti Rastogi:  हाँ, Utkarsh, बस final playbooks ही चल रहा है। कल भी एक-दो चीज़ें अभी optimize कराई हैं। I think by today, भाई, Tanuj was saying कि बस उसका final version बन ही गया है।
Prapti Rastogi:  तो बस अब मुझे एक final test और करना है, फिर आपको देंगे। तो वही चल रहा है उसपे।
Utkarsh Agarwal:  अभी उसमें approach कैसे ले रहे हैं, वही मतलब कि उसके evals बना के उसको optimize करके?
Prapti Rastogi:  हाँ, exactly, Utkarsh। Evals बना के, and playbooks को और stronger करके, वैसे ही कर रहे हैं।
Utkarsh Agarwal:  Right, right। वो, वही, वो generally agentic में यही वो है challenge कि हाँ, कोई आपको specific use cases के around ही playbooks बना के उसको evals करने पड़ेंगे, अगर generalized agent भी कर रहे हैं। क्योंकि multi-purpose general agent बहुत ही मुश्किल से quality दे पाता है।
Prapti Rastogi:  Exactly, Utkarsh। वो हम अपने use case के हिसाब से ना, around different verticals, in 42 use cases के हिसाब से ही उसको हम break down करके वैसे ही eval set prepare कर रहे हैं।
Utkarsh Agarwal:  Makes sense. ठीक है। Makes sense. 
Utkarsh Agarwal: ठीक है। और कोई points?
Prapti Rastogi:  नहीं, Utkarsh, अभी यही है।
Utkarsh Agarwal:  समझ गया। ठीक है, Ashish।
Utkarsh Agarwal:  हाँ जी, Utkarsh। So Utkarsh, मतलब, हमारा dummy system तो हमने deploy कर दिया था।
Utkarsh Agarwal:  So उसपे अभी testing हमारा चल रहा है। So basic testing
Ashish Sharma:  तो हमने, I think, कल तक wrap up कर लिया था। And everything is working as expected। I think कुछ हमारे जो multiple flows वाला part था, वो अभी still pending में है, because वो multiple delays, मतलब, renewals के time पे ही वो समझ में आएगा वो वाला part।
Ashish Sharma:  तो वो team एक बार test कर रही है। तो उसके basis पे सब कुछ अगर ठीक चलता है, तो I think, because उसमें loop in है, तो वो wrap up हो जाएगा वहाँ पे।
Utkarsh Agarwal:  समझ गया।
Ashish Sharma:  And फिर Utkarsh, इसके बाद जो हमारा events और ये सारी चीज़ें fixes करने वाला part था, तो Ranjith ने अपनी sheet भेज दी है, जिसमें सारे अभी audit sheet, जिसमें अभी events कैसे चल रहे हैं, क्या-क्या issues आ रहे हैं, तो वो मैं एक बार review कर रहा हूँ। And उसके basis पे अब मैं ये fixes वाला part start करवा दूँगा team में। समझ गया।
Ashish Sharma:  Got it. 
Ashish Sharma: ठीक है। Got it. And इसमें हमारा, ठीक है, and वो document जो हम बना रहे थे, इसका analysis— हाँ, हाँ, sorry।
Utkarsh Agarwal:  Yes. वो एक बार—
Ashish Sharma:  So Utkarsh, वो वाला मैंने बना दिया है। And I think मैंने update भी कर दिया है। मैं एक बार आपको ping करता हूँ link का।
Ashish Sharma:  समझ गया। 
Ashish Sharma: ठीक है। हाँ, ताकि वो review करके फिर वो close कर सकें। फिर उसके बाद।
Ashish Sharma:  Yes.
Utkarsh Agarwal:  ठीक है। ठीक है। और कोई points अभी इसमें हमारे?
Ashish Sharma:  नहीं, Utkarsh। I think अभी यही वाले points हैं। बाकी की तो अब buckets pick करनी हैं सारी।
Utkarsh Agarwal:  समझ गया। और हमारे SEO वाले points में data labs वाले जो पुराने थे, उसमें और कोई points हमारा अभी कहीं रह गए?
Ashish Sharma:  नहीं, Utkarsh। वो frontend, मतलब, basically सबका हो गया है। अब मैं basically frontend में pick करवाना start करवा कर दूँगा।
Ashish Sharma:  मतलब, people FAQs सारे बन गए हैं। वो test भी सारे बन गए हैं।
Ashish Sharma:  उसको मुझे deploy करवाना है। I think वही pending था बस।
Utkarsh Agarwal:  समझ गया। Got it. 
Utkarsh Agarwal: ठीक है। तो एक बार वो करके, फिर एक बार उस doc में एक बार updates जो हमने बात की थी, Prapti और Ashish, एक बार वो कर लो। तो उसके basis पे मैं फिर एक इस weekend पे एक बार monthly उसका analysis एक बार फिर से run कर लेंगे, ताकि क्या अब status है, और वो हमारा एक बार इस month के लिए अगर कुछ उसमें से pick करना है या नहीं करना है, वो चलो Ranjith के साथ plan कर लेंगे।
Utkarsh Agarwal:  But हाँ, at least status पूरा आ जाएगा, फिर accordingly roadmap में incorporate करेंगे, या तो इस month या अगले month। 
Utkarsh Agarwal: ठीक है, Utkarsh। वही बोल रहे हैं। मैं एक बार update करता हूँ उसको। 
Utkarsh Agarwal: ठीक है। ठीक है। I think हाँ, four points ये थे।
Utkarsh Agarwal:  बाकी server वाले में हमारा सब कुछ हो गया या कुछ रह गया?
Ashish Sharma:  हाँ, Utkarsh। वो server वाले में हमारा phase one वाला पूरा part हमारा बन गया है। So मेरी कल उनसे call हुई थी phase two के regarding, जिसमें हमारा auto scaling वाला part और cost थोड़ी सी और optimize करने का part था।
Ashish Sharma:  तो उसके regarding वो एक बार evaluate कर रहे हैं, हमारा in part two में क्या वो auto scaling वाला part अभी कर सकते हैं कि नहीं। तो वो वाला part, Utkarsh, अभी एक बार मुझे I think वो इस weekend, मतलब, next week बताएंगे।
Ashish Sharma:  और कितना time लग सकता है। तो वो उसके basis पे फिर, Utkarsh, phase two decide करेंगे, कितना हो सकता है उसमें।
Ashish Sharma:  लेकिन हमारा जो अभी तक जितना part था, वो पूरा part हमने कर लिया था।
Utkarsh Agarwal:  समझ गया।
Ashish Sharma:  अब वो consolidation वाला जो part था, वो वाला part हमें करना है। जिसमें मेरी applications जो थीं, और जितना, मतलब, हमारी जो applications चलती हैं, आपका वाला server मालूम पड़ गया था। And जो हमारे वाले servers हैं।
Ashish Sharma:  और अगर कोई और server चल रहा है, वो मुझे एक बार activate start करना है।
Utkarsh Agarwal:  समझ गया। Got it। तो अभी हमारा उसमें और इसका अभी GCP का कुछ और बचा है क्या?
Ashish Sharma:  नहीं, Utkarsh। GCP का नहीं बचा है। I think केवल अब हमारा जो बचा है, वो केवल हमारा अब वो BigQuery वाला ही instance बचा हुआ है।
Ashish Sharma:  And एक Slack application, जो हमारी meeting वाली थी। समझ गया।
Ashish Sharma:  हाँ, फिर वो consolidation के साथ-साथ फिर उसको भी हम move कर लेंगे। Yes, yes।
Ashish Sharma:  समझ गया। 
Ashish Sharma: ठीक है। हाँ, I think अब forecasted जो इसका अभी रहा है GCP में, वो अभी 72,
Utkarsh Agarwal: 000 का forecast आ रहा है। तो हाँ, I think वो उसी range में रहेगा। तो ये सारा, I think, अब GCP का ही primary बचा है, right?
Ashish Sharma:  Yes. मतलब BigQuery वाले part में mainly।
Utkarsh Agarwal:  हाँ, sorry, BigQuery वाला। Sorry।
Ashish Sharma:  Yes.
Utkarsh Agarwal:  समझ गया। ठीक है। तो अभी GCP में, ठीक है, वो चलो cost optimization, उसका बाद में आते हैं।
Utkarsh Agarwal:  वो बाद में solve करेंगे। 
Utkarsh Agarwal: ठीक है, समझ गया। ठीक है, done। हाँ, Ranjith।
Ranjith M:  हाँ। So Utkarsh, like we discussed in the last call, हमारा three main objective था: weekly plan close करना है, weekly the sprint plan, second is user properties का documentation, third is event properties। These three things are done and have given in the group, I mean shared on the group.
Ranjith M:  Yesterday we discussed about user properties, I mean when we discussed individually, but I've completed the event and event properties also. Yesterday we discussed the user properties.
Ranjith M:  Today I'll just give a context, then we can discuss individually अगर if there requires। So we have different, in this sheet we have different tabs of app events, event properties, data labs, event, event properties, and media events and event properties.
Ranjith M:  So now coming back to the audit sheet which I've created, which is this particular tab. So this tab has across for all the project: app, data labs, and media.
Ranjith M:  इसमें क्या-क्या है? All the events which are not firing, उसमें these are the events which are not fired.
Ranjith M:  These are the events which are firing multiple times or duplicate events. And these are the events which are firing correctly.
Ranjith M:  And there are, these are the events उसमें there are few properties missing. So similarly it goes for, and let's say these are the events which are getting triggered, but these are not part of the sheet, the master sheet which I've collated.
Ranjith M:  So this is for app. So then goes for data labs, then again followed by media.
Ranjith M:  This is the sheet which I've created. Again, I'm not getting into detail in the interest of time.
Utkarsh Agarwal:  Right, right.
Ranjith M:  But again, concluding that, this is done. Probably if anyone has any point, we can discuss on top of it. This is one.
Ranjith M:  Second, myself, Ashish, had a discussion on QIA yesterday. We, there is agreement and disagreement.
Ranjith M:  I believe Utkarsh, I've discussed with you briefly yesterday, but again, just for a context, we agreed that QIA, this is the metric that we should be chasing, but how do we chase it? For example, QIA is what, QIA is what gonna benefit company or this is the business metric that everyone should be chasing.
Ranjith M:  But how each bucket or how each team is contributing to final metric. That's when what we decided is, I'll try to make it, I'll try to split it, QIA.
Utkarsh Agarwal:  उसमें, उसमें, उसमें how does, I would recommend, like, what we discussed yesterday I remember, but उसमें one layer I would want to add is, like, we were discussing, one is IA, second is QIA, and third is QIA core. So अभी के लिए, before who chases what and how do we influence it, से पहले, one layer further before we should go is, first measuring this and setting a baseline and seeing what affects it, and how is it affected, how is it measured, and what parts are subjective. Like,
Utkarsh Agarwal:  for example, if we need company type along with the designation to be able to say whether it's QIA or not, if that is too complicated to measure, is there an easier way to do it? So first lock the measurability and how easy is it to define, how much is it dependent on enrichment, what are the other dependencies of it. Then we can come to whether we chase IA or QIA or which part do we chase and how do we influence it.
Utkarsh Agarwal:  But first, quantifying the metric properly, making it measurable and easy to track, and seeing if there are any other gaps or challenges that we missed in terms of measurability and implementation. That first we need to log.
Utkarsh Agarwal:  Because if it's not easily measurable or it takes a lot of enrichment and some parts are not enrichable and there are a lot of dependencies, then the metric is no longer anyways useful.
Ranjith M:  Right.
Utkarsh Agarwal:  So first solve for instrumentation and measurability and any other such dependencies. Then we define how do we, who chases what or whose metric is what.
Ranjith M:  हाँ, right. So, हाँ। So just to add on few things, we did discussed all of these things.
Ranjith M:  So, and what we ended up, what we ended up is that the qualification criteria, that rather than, one second, I'm just, ठीक है।
Ranjith M:  So what we just, what we discussed yesterday is that obviously what to chase and how to chase, and also what you also just mentioned. Like, is this the right metric to chase?
Ranjith M:  And is this the right qualification benchmark? Because we had a different controversy point is, let's say, is the company type even needed?
Ranjith M:  Or when we talk about seniority, so are we only considering senior manager or, let's say, VP and above? Is these are the right metrics?
Ranjith M:  We did discuss that. I have the list of profiles which, as per me, should be the ideal qualification metric for us to consider this is a qualified active.
Ranjith M:  And how easily do we get the data is also something I have the data with me. Right after this call, I'll share this.
Ranjith M:  Probably we can conclude the discussion in the chat as well. But मेरे पास, I have curated the list of whatever you just mentioned.
Ranjith M:  So who should be the ideal audience? How do we chase and why do we agree or why do we disagree upon?
Ranjith M:  So I've created this. I can, I'll share this right after this, probably in 2:15, 2:30 type, I'll share it.
Ranjith M:  Probably we can agree, agree on the group. If there is a lot of disagreement, we can, everyone can get on a quick call and close this.
Utkarsh Agarwal:  ठीक है।
Ranjith M:  That is one. Second, we also agreed on, again, this is again coming back to part of instrumentation, which is, we agreed on QIA for 7 days.
Utkarsh Agarwal:  हाँ, मतलब, that is QIA 7 versus QIA 30, either we can have measured for both, and then we can decide who is chasing what, both that we can see.
Ranjith M:  हाँ, done. These are the two things. But like I said, I'll share the documentation which, which whatever I just said is already in part of the document.
Ranjith M:  Again, we can discuss on top of it. That is one update.
Ranjith M:  Now coming back, I'll just open my document. So I'll try to initiate the mowing age का discussion today, Utkarsh.
Ranjith M:  I got the contact details of Mayank. I have his number with me.
Ranjith M:  I'll call him. I'll, before that, I'll take a few more context.
Ranjith M:  I'll go through, I've gone through, but very briefly I've gone through. I'll get more context.
Ranjith M:  I'll have, I'll have an initial discussion with him. Then I'll discuss with you what are the next step as per me.
Ranjith M:  Then we can conclude on this. That is one.
Ranjith M:  Second is, in the document I've mentioned to close the performance-related search, search bar performance-related. So there are, so I'll try to scope, scope out the work, like what to be included, what not to be included.
Ranjith M:  I'll try to close the documentation for this as well. This is second.
Ranjith M:  Third is, if you remember the notification which we, which we discussed that if we can prioritize this week. So when it comes to notification, I have the logic with me.
Ranjith M:  But I was, I also checked my high level, but I was animated to check what is the feasibility of it and how do we consume the, can he pass the dynamic message in the notification? Can he consume the notification का message from the event property or not?
Ranjith M:  So that is something I've asked him to check. If there is any response, I'll let you know.
Ranjith M:  If not, I'll check myself and get some clarity today itself. So these are the things which I'll try to close today.
Utkarsh Agarwal:  Got it.
Ranjith M:  हाँ, I'm done. If there is anything else missing, let me know or I think I'm good. Best.
Utkarsh Agarwal:  App में अभी status?
Ranjith M:  हाँ, when it comes to app, Rithvik has started the explore article page का design, and I've scheduled the design for article page also. Rest, I have, I've just on my, I'll just share my screen. One second.
Ranjith M:  I have started creating a Asana tickets for all the tasks which are related to design and development. I've asked Satya to update the timeline also.
Ranjith M:  So mostly all the design we can expect by Monday, Monday, including the dark mode also. That is the estimate which I got from Satya for all the, what are the pages that we discussed and on top of the dark mode.
Ranjith M:  That is something that we are aiming to close so that develop, anyways developer is not, not blocked right now. Rithvik has sufficient pages to work upon.
Ranjith M:  And we'll, again, like I said, we are aiming for Wednesday as a team. If there is any changes or deviation, I'll let you know.
Ranjith M:  I've shared you a Figma file also. If requires, we can discuss in detail.
Ranjith M:  If not, we can connect separately.
Utkarsh Agarwal:  Oh, हाँ, we can, we can sit in office in some time on the designs एक बार, any feedbacks that are required on that, that we can discuss separately in office. Part one. Part two, one other thing for the app is, maybe in the app का master sheet, the filters and the logics and the pills that are there in terms of, like, in one the explore का articles and companies वाला part, those logics and use cases is one other part that we can better define.
Utkarsh Agarwal:  So that if there is something that we are missing, that can be covered there.
Ranjith M:  Got it. So I got a, and the priority order of, in which order we show it also. Got it.
Ranjith M:  So I got a revised logic. Prapti has shared that revised logic with me.
Ranjith M:  And the results are making sense. What I'll do is I'll share the, I'm also talking about the pill, especially for company section in the expert page.
Ranjith M:  So I'll share the document with you. And again, we can, once you're gone through the document, we can discuss to refine it further if there are any changes.
Ranjith M:  Or I'll also add as part of the document for more clarity.
Utkarsh Agarwal:  Got it.
Ranjith M:  Yes.
Ranjith M:  That's it from my side.
Utkarsh Agarwal:  ठीक है, makes sense. Any other points किसी का on this?
Ranjith M:  Not on this, Utkarsh, but just one thing. On the server side, so credits वाला part अभी हम नहीं मिल रहा है ना, तो मैं एक बार.
Utkarsh Agarwal:  Ranjith, any updates on the credits वाला part?
Ranjith M:  Varun also reached out to few folks, and I myself have also reached out to few folks on LinkedIn. But so far, no positive response. I'm just trying to, I was thinking to reach out to my second connection, via, I mean, via my first connection to the person so that to see if we can do something else.
Ranjith M:  I've reached out to few people today also. Again, I'm not having too much of expectation or a positive, I'm not expecting a positive response also for now.
Ranjith M:  But again, I'm just trying to see if, just get a better response if possible.
Utkarsh Agarwal:  हाँ, ये थोड़ा important है। This is, इसमें, Azure के portal पे, Ashish, is there any option to reach out?
Ranjith M:  Utkarsh, बस वो उनका support वाला thread है, and उसके through मैं try कर सकता हूँ, if that is possible.
Utkarsh Agarwal:  हाँ, वो भी try कर लो, कि वहाँ पे raise करके, कि हाँ, मतलब ये startup program वाले से हमें connect करना है, हमारे credits के context में, further discussion चाहिए। तो वहाँ पे भी thread एक बार कर लेते हैं। उसमें हम दोनों को भी mark कर लेना, ताकि accordingly हम उसको वो कर पाएँ।
Ranjith M:  Oh, I can do, I can do, I can take this up.
Utkarsh Agarwal:  हाँ।
Ranjith M:  तो, Utkarsh, help me with the access of Azure. I can initiate.
Utkarsh Agarwal:  Let me see how, how to do that. इसके permissions are? हाँ, permissions मुझे आज तक समझ में नहीं आया, कैसे देते हैं इसमें।
Utkarsh Agarwal:  इसमें scale dynamics, sorry, on a different note, ये scale dynamics वाले के पास जो access है, वो मैं हटा दूँ ना?
Ranjith M:  हाँ, Utkarsh, उसका remove कर सकते हैं ऐसे।
Ashish Sharma:  ठीक है, उसको तो मैं disable कर ही देता हूँ। फिर कैसे access देना है, वो देखना पड़ेगा। 
Ashish Sharma: ठीक है, let me figure out कैसे। Ashish, तुम्हारे पास भी admin है ना शायद, या नहीं है तुम्हारे पास?
Ranjith M:  Utkarsh, मेरे पास admin तो है, आपने मुझे दिया था। But due to some reason, पता नहीं, मैं किसी को, मतलब वैसा owner type का access दे नहीं पाता हूँ।
Utkarsh Agarwal:  समझ गया।
Ranjith M:  मतलब वो, मतलब billing का access मैं दे नहीं पाऊँगा, I think, उस वाले part में।
Utkarsh Agarwal:  ठीक है, वो मैं try करता हूँ।
Ranjith M:  ठीक है। So Utkarsh, me को बस, बस एक चीज़ जानना था, कि क्या मैं conversation initiate करवा लूँ, कि billing हमें जो आगे करवानी है, वो हमारे account के through होगी या Square Ops के through होगी? And Square Ops team was saying कि अगर वो उनके through billing होगी, then वो हमें additional discounts provide कर देंगे।
Utkarsh Agarwal:  ठीक है, एक बार बात करके देख लूँ। मतलब समझ लेते हैं, सारी details ले लेते हैं और process समझ लेते हैं, कि क्या कहानी है, ताकि accordingly हम उसके base पे एक बार देख पाएँ।
Ranjith M:  ठीक है, एक बार मैं उनसे estimate मँगा लेता हूँ, कि आप हमें कितना discount provide करोगे, as per जो अब, just because आपको पूरा context है कि हमारा कितना costing अभी है, क्योंकि अभी पूरा हमने close ही किया। And उसके basis पे, अभी हमारी कितनी billing होगी, and आप उसमें कितना discount दोगे हमें।
Utkarsh Agarwal:  Right. And इसमें एक और चीज़, वो भी check करते हैं, कि इसमें, जैसे AWS में वो हुआ करता था ना, reserved instances versus pod instances।
Ranjith M:  हाँ, yes.
Utkarsh Agarwal:  वैसा, वैसा कुछ भी है क्या यहाँ पे?
Ranjith M:  एक बार मैं पूछ लेता हूँ, Utkarsh, इस वाले part में। मतलब reserved instance, यानी कि, मतलब, मतलब वो services जो हम use नहीं कर रहे।
Utkarsh Agarwal:  नहीं, reserved instances का concept AWS पे जो होता था, उसमें ये होता था कि by default सब कुछ pod instances या मतलब normal आपके servers हो गए। Reserved instances में आप ये commitment दे देते हैं कि हाँ, हम मतलब 6 महीना या साल भर हम ये वाला server type का या ये level का server हम use करेंगे। And hence वो और discounted rates आपको दे देते हैं।
Ranjith M:  Got it. मैं एक बार पूछ लेता हूँ, Utkarsh, इस वाले part को।
Utkarsh Agarwal:  हाँ, तो वो वाला भी अगर यहाँ पे optimization का कोई scope हो, तो वो भी देख सकते हैं।
Ranjith M:  ठीक है, okay।
Utkarsh Agarwal:  And इसमें और कोई तरीका, अगर हम इसको fast track करें। Varun वाले में अभी क्या बात हुई थी उसमें, Ranjith?
Ranjith M:  He also reached out to few people on LinkedIn, but they're saying, either they're not part of the organization or they're moved to a different team and getting very difficult to get the contacts of startup team, especially. Then I still told them to reach out to few people via different connections and see if at least we get some idea क्या मिलेगा, नहीं मिलेगा। Or if, if, if it, if I, if we can get, how soon we can get.
Ranjith M:  I've asked them to get, but I'll, anyways I've asked them two days back also, I'll follow up with them again today to get some conclusion so that it becomes a closed thread.
Utkarsh Agarwal:  Right. ठीक है। And हाँ, भाई, I've sent you an invite.
Utkarsh Agarwal:  Let's see if that works on, on the, this thing, Azure का portal. See, on your email you might have gotten it.
Utkarsh Agarwal:  Check that and see if that's working.
Ranjith M:  So far not, but हाँ, let me check as in when I received.
Utkarsh Agarwal:  ठीक है। Any other points फिर?
Ranjith M:  Good.
Utkarsh Agarwal:  ठीक है, done done. Okay, thanks again.
Ranjith M:  Thank you.
Utkarsh Agarwal:  Thank you.
