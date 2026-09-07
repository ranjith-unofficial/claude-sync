# App UI Redesign Discussion

- Wispr meeting id: 2233a7e7-019b-4e7c-8121-a9345389e900
- Start: 2026-09-07 18:57 IST (13:27Z) · End: 20:21 IST
- Attendees (calendar): (not listed in Wispr)
- Share link: https://notes.wisprflow.ai/shared/k869WCco8davBiYW672f3VgrBtAxTzPNgQ-_rWUqbOY
- Archived from Wispr Flow via MCP on 2026-09-08. Transcript is verbatim ASR output; speaker labels are Wispr's and are sometimes mis-assigned.

## Wispr summary
Design review of the in42 app redesign: font/color direction, splitting Explore into separate News and Companies tabs, moving Watchlist under Profile, and locking a timeline for Sept 15 marketing launch.

### Content & Card Details
- Hero card description: pick first summary bullet instead of article's first line, to avoid incomplete cut-off text
- Tags should look like tags (familiarity); try a version without tag styling to keep card focused
- Long tag names (e.g. 'Advanced Hardware and Technology', 'Media and Entertainment') need shorter display names
- Article page needs readability fixes: line-height and paragraph spacing too large

### Color & Font Direction
- in42 logo red is the baseline; narrow down to a single primary red swatch tested across screens
    - Akshay's morning point: gradient exists but no defined primary red
- Font direction (serif + sans-serif combo) agreed; test edge cases with real content variations
- Reduce depth/3D effect on toggle pill to match flatter background

### Information Architecture
- Explore split into two bottom tabs: News and Companies (4 tabs total)
    - Article and company consumption patterns are fundamentally different
- Watchlist merged into Profile (only ~15% usage); Streak stays top-level for now (~20-25% usage)
- Companies page uses sectional layout (recently funded, just launched, etc.) with 'browse all' filter page
- Search prominence to increase on Companies page; stays global, not a separate bottom tab

### Timeline & Delivery
- Design completion target: 9th EOD; dev completion 11th; submission Fri/Sat; marketing launch 15th
- Page order: news home, companies home, article detail, company profile, then brief last
- Company profile page: UI update only this round, UX revamp deferred to v3
- Web-view idea for company detail page rejected (breaks native interaction, aesthetics mismatch)

### Next Steps
- (Speaker 1) Simulate hero card with real article content to test incomplete-line edge cases
- (Speaker 1) Build standard screen template to test red shades across displays and pick primary swatch
- (Speaker 1) Propose 2-3 shorter naming variations for long sector tags (hardware technology, media)
- (Speaker 1) Deliver designs sequentially: article page first (tomorrow), then news home, companies home, company profile, brief last
- (Speaker 1) Fix article page readability: line-height, paragraph spacing, summary size
- (Speaker 2) Re-share information hierarchy document covering news, companies, tags, and onboarding
- (Speaker 2) Submit app build Friday EOD / Saturday morning; test one day before submission

### Decisions Made
- Explore tab replaced by separate News and Companies bottom tabs (4 tabs total)
- Watchlist merged into Profile; Profile moves to bottom bar as last tab
- in42 logo red becomes the baseline primary red
- Hero card description sourced from summary's first bullet, not article's first line
- Company profile page: UI-only update this round, UX revamp pushed to v3
- Skip web-view approach for company detail page

## Transcript
Speaker 1: Uh, one second, you in?
Speaker 2:  तो मेरी अक्षय से मॉर्निंग में बात हुई, तो हम लोग थोड़े से, uh, atomic level पे ही—like पहले फॉन्ट फाइनलाइज़, कलर फाइनलाइज़ कर रहे हैं। तो, तो जो कुछ कलर्स थे, वो तो मैंने वहाँ से पिक कर लिए थे, जो already हमारे पास ब्रांड एक्सटेंशन में थे। बाकी मैंने, uh, फॉन्ट चेंज किया था इसमें।
Speaker 1:  समझ गया।
Speaker 2:  फॉन्ट की readability तो better है।
Speaker 1:  हाँ। इसमें हमारे ये वाला description अभी exist नहीं करता।
Speaker 2:  अभी आता तो है। हीरो पे आता ही है। हीरो कार्ड, जो वेबसाइट है।
Speaker 1:  वो कहाँ से पासवर्ड होगा? क्योंकि अब तो हमारे पास सिर्फ summary है, जो 3 bullet points की है।
Speaker 2:  कल ही तो देख रहा था मैं। हाँ, आ रहा है ना, हीरो कार्ड पे।
Speaker 1:  नहीं तो content—ओह, ये article का first line ही pick हो रही है।
Speaker 2:  अच्छा। हाँ, I think वैसे ही look करता है, I think।
Speaker 1:  बाकी लोग भी यही कर रहे हैं। वही, first line ही pick हो रही है।
Speaker 2:  हम्म।
Speaker 1:  इसको real content की तरह एक बार simulate करके देखना पड़ेगा, क्योंकि incomplete lines आएँगी।
Speaker 2:  हाँ।
Speaker 1:  वो एक challenge आएगा।
Speaker 2:  Incomplete lines मतलब डॉट डॉट? मतलब, that is what the thing is, ना? वो डॉट डॉट आए तो उसमें—
Speaker 1:  They open for—
Speaker 2:  हाँ, वही होता है ना, read more वाला।
Speaker 1:  हाँ, यहाँ पे भी। यहाँ पे भी है। नहीं, read more—read more people।
Speaker 2:  हाँ, मतलब अगर कोई पढ़ रहा है तो it's like a stop। वैसा हो गया ना। वही होना चाहिए, complete नहीं होना चाहिए तब।
Speaker 1:  ये cases देखने पड़ेंगे।
Speaker 2:  एक सेकंड।
Speaker 1:  ये एक edge case है।
Speaker 2:  नहीं, content में है।
Speaker 1:  ये copy नहीं है। It's not a section. ये content है।
Speaker 2:  ओह। ओके।
Speaker 1:  When they update the same article—
Speaker 2:  Developing stories में कभी-कभी ये होता है।
Speaker 1:  हम्म। ये एक edge case है इसमें।
Speaker 2:  सत्य ऐसे करते हैं। हमारा अभी summary में 3 points आते हैं। एक point उसमें, उसमें—
Speaker 1:  तो वो तो family की hierarchy में ही built-in हो सकता है ना। उसमें तो we don't need another।
Speaker 2:  हाँ, या फिर summary का first point भी pick कर सकते हैं। That is a safe way। हाँ, summary का first point pick कर सकते हैं, logic point of view से।
Speaker 2:  I think that will work।
Speaker 1:  Because इसमें कुछ भी हो सकता है।
Speaker 2:  Hmm।
Speaker 1:  And summary का point at least automatically capped language to some extent।
Speaker 2:  हाँ।
Speaker 1:  Maybe—
Speaker 2:  नहीं, you are not looking— नहीं, you are looking at this summary, but I am talking about the white matters, what it matters।
Speaker 1:  वो अलग है? वही book तो यही है।
Speaker 2:  नहीं, नहीं।
Speaker 1:  उसका content अलग है?
Speaker 2:  हाँ। एक मिनट, अब बताओ।
Speaker 1:  But फिर वो यहाँ पे क्यों नहीं load हुआ?
Speaker 2:  हाँ।
Speaker 1:  नहीं, नहीं। हाँ, नहीं, वो तो— it is not developed here. It's not updated here.
Speaker 1:  एक बार I will open this।
Speaker 2:  This is part of that options वाला cleanup we were talking about in the morning. We have to start doing this cleanup। The editor will be filling— जितना article है, उतना time they have to fill in tagging and adding these variations for all of our systems।
Speaker 2:  I think।
Speaker 1:  उनके पास already 20 options— 20 things हैं that they already fill for every article।
Speaker 2:  It's आज का article है ये।
Speaker 1:  हाँ।
Speaker 2:  एक मिनट, just— can you just scroll to top?
Speaker 2:  नहीं, thankfully same है। But I was not anticipating this, but हाँ, somehow it is same।
Speaker 1:  Same है?
Speaker 2:  हाँ, no paperwork। एक मिनट।
Speaker 1:  तो अपने आप में सब जबरदस्ती white matters डाल रहे हैं या— hopefully the content is same, but—
Speaker 2:  नहीं, it is relatable also। I was randomly going through few other articles, so it makes sense।
Speaker 1:  ठीक है।
Speaker 2:  तो यहाँ पे भी वो changes eventually करेंगे। ठीक है।
Speaker 1:  हाँ।
Speaker 2:  But again, coming back, we can pick it from the summary।
Speaker 1:  We can pick the first summary point।
Speaker 2:  हाँ।
Speaker 1:  ठीक है, तो वो हो जाएगा। Then we are back to— then we can continue on this। Uh, tag style में एक चीज़ देख सकते हैं।
Speaker 1:  If you want to keep the roundness, या we want to keep it— this also clean। Just simple।
Speaker 1:  No tag का वो।
Speaker 2:  नहीं, वो फिर वही था कि—
Speaker 1:  Capability?
Speaker 2:  हाँ, capability।
Speaker 1:  Now the problem is, you'll— you'll end up having—
Speaker 2:  From a familiarity perspective, tags should look like tags।
Speaker 1:  Hmm।
Speaker 2:  हाँ, otherwise—
Speaker 1:  There is a cleanness here. But I get it।
Speaker 2:  हाँ, मतलब वो— वो देख सकते हैं यार। मतलब, वो है ना। We'll have to make it very evident कि वो एक tag है, तो फिर—
Speaker 1:  But do people even click?
Speaker 2:  Either way। अभी भी अगर नहीं click हो रहा है, and usability वैसे भी अगर ज्यादा है— use case नहीं है ज्यादा।
Speaker 1:  हम्म।
Speaker 2:  तो then it doesn't matter।
Speaker 1:  Makes sense।
Speaker 2:  एक— actually इसमें ना, there is— I mean, for your context also— इसमें there is a technology— hardware technology and consumer— कुछ।
Speaker 1:  हाँ, समझ गया। बड़ा वाला।
Speaker 2:  फिर तो—
Speaker 1:  हाँ, मैंने वो—
Speaker 2:  हाँ, वैसे— and it gets braved। तो you'll have to consider how do we incorporate that design also। When two line comes up।
Speaker 1:  Hmm। I think—
Speaker 2:  It becomes—
Speaker 1:  अच्छा लग रहा है। You minus this color।
Speaker 2:  मैं experiment कर रहा हूँ, sectional wise color put करके, art बना के।
Speaker 1:  कलर match कर रहा है। वैसे मेरा ऐसा नहीं कि कलर में कुछ issue है। Nothing is wrong with the color।
Speaker 1:  Only challenge is, ET is exactly this। जैसे ये देखिए, ET आ जाता है।
Speaker 2:  ये वाला?
Speaker 1:  हाँ।
Speaker 2:  ओके।
Speaker 1:  ET भी यही करता है। इसके—
Speaker 2:  मतलब section वैसे बना के, या फिर—
Speaker 1:  उनका भी यही सबसे common है।
Speaker 2:  ओके। मैं सोच रहा हूँ कि सबका ही वैसे common है।
Speaker 1:  Business standard का भी यही है वैसे तो।
Speaker 2:  You're talking about this section? Something like this। यही है?
Speaker 2:  अच्छा, the usage।
Speaker 1:  अच्छा।
Speaker 2:  हम्म।
Speaker 1:  हाँ।
Speaker 2:  मतलब, as of now, मेरे दिमाग में वो ET का है, but maybe of different—
Speaker 1:  But that is the immediate shade you go जब आपका primary वो रहता है।
Speaker 2:  Business standard पूरा का पूरा यही है।
Speaker 1:  As far as I remember।
Speaker 2:  Change कर लिया होगा, पता नहीं।
Speaker 1:  अब हटा।
Speaker 2:  हाँ।
Speaker 1:  ये।
Speaker 2:  That's peach।
Speaker 1:  It is a little pinkish, slightly।
Speaker 2:  हाँ, slightly more।
Speaker 1:  But वो थोड़ा सा वैसा आता है ना, अगर वो— अगर वो इतना different नहीं है, तब तो वो same ही रहता है। It's like—
Speaker 2:  Right। तो यहाँ पे ये common है। Ken का भी है, but Ken इस तरह से नहीं।
Speaker 1:  नहीं, Ken का इतना नहीं होगा।
Speaker 2:  Ken का वो वाला color है।
Speaker 1:  उनका तो हाँ, background ही—
Speaker 2:  उनका font थोड़ा similar है।
Speaker 1:  हाँ, तो ये— ये वाले की वजह से अपने आप balance अलग आ जाता है।
Speaker 2:  हाँ, फिर वो वैसे भी cards बनाते हैं ना।
Speaker 1:  हाँ।
Speaker 2:  White डालते थे cards के अंदर।
Speaker 1:  उनका हाँ, ये inverted।
Speaker 2:  इस तरीके से थोड़ा—
Speaker 1:  हाँ, ये invert कर रखा है।
Speaker 2:  ओके।
Speaker 1:  नया है।
Speaker 2:  पूरा section ही नया है।
Speaker 1:  This is the recommendation engine वाला approach that people are now trying।
Speaker 2:  हाँ।
Speaker 1:  पूरा— पूरा page नहीं personalize कर रहे, but section ही।
Speaker 2:  Somewhat of the section।
Speaker 1:  Yes, maybe।
Speaker 2:  But हाँ, ET वाला भी overlap देखना होगा।
Speaker 1:  मेरे दिमाग में सबसे पहले ET की याद आया था।
Speaker 2:  ठीक है।
Speaker 1:  ये देख के।
Speaker 2:  मतलब, वैसे— वैसे हम ये peach color use करते हैं।
Speaker 1:  हाँ।
Speaker 2:  Editorial में already use करते हैं। But for example, इस structure में जब आया, तो मेरे दिमाग में सबसे पहले ET आया। उसको board table।
Speaker 1:  Sorry, sorry।
Speaker 2:  I think interesting मतलब वो रहेगा कि we can use the color, but अगर हम उसका एक usage rule change कर दें ना, then it will be— वो work कर जाएगा।
Speaker 1:  तो I think primary swatch figure out करते हैं।
Speaker 1:  Step one।
Speaker 2:  But हाँ, directionally I think I like जिस तरह भी जा रहा है।
Speaker 1:  ऊपर जाना तो— uh— like on the top। हाँ। So why have we gone with the boxier panels now?
Speaker 2:  Hmm।
Speaker 1:  Like—
Speaker 2:  हाँ, देखा।
Speaker 1:  Rather than rounded ones।
Speaker 2:  अभी भी rounded तो है हल्का सा। Rounded— roundness का amount change हुआ है।
Speaker 1:  हाँ।
Speaker 2:  But—
Speaker 1:  हाँ, मतलब—
Speaker 2:  The directional— like because— like उसमें तो I think these are a lot more comfortable to view।
Speaker 1:  Hmm।
Speaker 2:  And how the toggle also feels।
Speaker 1:  ये वाला roundness— ये वाला roundness same है ना?
Speaker 2:  नहीं।
Speaker 1:  या ये इससे भी कम है?
Speaker 2:  More or less similar, but doesn't matter।
Speaker 1:  वो I think scale ही—
Speaker 2:  हाँ।
Speaker 1:  I think— I think component level change तो मतलब we'll explore, right?
Speaker 2:  हम्म।
Speaker 1:  मतलब different variations तो like— it's always वही है।
Speaker 2:  Because the softness of the previous version—
Speaker 1:  हाँ।
Speaker 2:  That— I think I like a little bit of that।
Speaker 1:  जैसे ये वाला है ना, वही। I get it।
Speaker 1:  मतलब वो उसकी—
Speaker 2:  क्योंकि app POV से—
Speaker 1:  Approachability इसकी better है। This feels less like a toggle and there, but ये मुझे— मुझे भी ये भी थोड़ा odd लग रहा था। We have to find something in between।
Speaker 2:  Maybe—
Speaker 1:  Not completely—
Speaker 2:  ये वाला थोड़ा वो करो ना, zoom करके।
Speaker 1:  हाँ, वो उसके reason से odd लग रहा है क्या?
Speaker 2:  हाँ, because—
Speaker 1:  वो actually इसका depth की वजह से और उसका—
Speaker 2:  Color थोड़ा flat कर दें।
Speaker 1:  Depth का— हाँ, depth की वजह से लग रहा है।
Speaker 2:  थोड़ा 3D जो उसका वो उठा हुआ—
Speaker 1:  मतलब कोई भी effects आ रहा है, वो हम थोड़ा reduce कर दें।
Speaker 2:  वो effect की वजह से शायद ज्यादा—
Speaker 1:  हाँ, वो उसी की वजह से।
Speaker 2:  उसी की वजह से आता है। वो odd तो लग रहा था।
Speaker 1:  उसका जो original component था, उसके original component में जो article था—
Speaker 2:  Flat design था वो थोड़ा।
Speaker 1:  हाँ, वो तो flat था। But इसके बाद जब मैंने इसी पे जो design किया था, अभी आप देख रहे होगे, उसके background में depth है, but जो pill है, उसमें कोई depth नहीं है। Ideally तो pill में भी depth होना चाहिए था।
Speaker 2:  Right।
Speaker 1:  तो हम pill में depth remove किया, but वहाँ depth remove। तो वो वैसा आया, I think।
Speaker 2:  This versus this— I like this।
Speaker 1:  Yes।
Speaker 2:  Cleaner।
Speaker 1:  Cleaner।
Speaker 2:  हाँ, हाँ।
Speaker 1:  वो— वो ठीक है।
Speaker 2:  वैसे in42 exclusive ऐसे random tags हैं और like something behind the reason।
Speaker 1:  Being a different color versus black।
Speaker 2:  नहीं, in42—
Speaker 1:  ये exist करता है। This tag exists।
Speaker 2:  In42 exists।
Speaker 1:  हाँ।
Speaker 2:  Exist करता है। वो अभी यहाँ randomly डाला होगा, वो अलग बात है, but हाँ, exist करता है।
Speaker 1:  हाँ, नहीं, in general।
Speaker 2:  अच्छा, ठीक है। Are we using in42?
Speaker 1:  नहीं, वो अभी— हाँ, उसका prominence eventually कोई technology build कर सकते हो, उसको लाने का। It just exists. But—
Speaker 2:  ठीक है। in42 exclusive में क्या-क्या आता है? Exactly articles?
Speaker 2:  मतलब article।
Speaker 1:  Newsroom ने exclusive break दी। जो हमारी first—
Speaker 2:  Section C होना चाहिए, बट— मतलब—
Speaker 1:  नहीं, what is the frequency of that? Which idea है उसका?
Speaker 2:  Frequency।
Speaker 1:  Quantum wise।
Speaker 2:  बहुत ज्यादा नहीं होगा, मतलब—
Speaker 1:  Out of 100 articles which we would have published, what would be the percentage?
Speaker 2:  नहीं, but फिर यहाँ पे question ये है कि frequency किस हिसाब से है? Like अगर month—
Speaker 1:  70% above 5%, lower than 10%।
Speaker 2:  नहीं, फिर तो we can skip this।
Speaker 1:  हाँ।
Speaker 2:  और gap कितना रहता है? Like अगर एक month को पकड़ो तो कैसा रहता है? कुछ?
Speaker 2:  फिर तो खत्म ही हो गया ना। 6 महीने पहले का news बोल के नहीं दिखाओगे।
Speaker 1:  नहीं, हर महीने होगा।
Speaker 2:  अच्छा।
Speaker 1:  पर किस frequency पे होगा is not a guarantee। Monthly होगा। Monthly is a volume।
Speaker 1:  ये—
Speaker 2:  10%, 5, 10%।
Speaker 1:  हाँ, 5 to 10% हर month होगा। But कितना consistently होगा is the debate।
Speaker 2:  हाँ, मतलब अगर कहीं-कहीं ऐसा तो होता है ना, package करके भी कर सकते हो। Monthly, weekly। अगर वो frequency match हो रहा है तो।
Speaker 2:  वहाँ पे package देखकर हो गया तो।
Speaker 1:  Yes. It becomes to package when it's very inconsistent। अगर pattern है कुछ।
Speaker 1:  Let's say weekly twice, thrice।
Speaker 2:  कभी तो बोला monthly।
Speaker 1:  हाँ।
Speaker 2:  अगर—
Speaker 1:  ये part देखना पड़ेगा। ये बस— ये मुझे— ये नीचे लगा। थोड़ा bland लगा मुझे ये।
Speaker 1:  हमारा header कैसे— का styling कैसे हम देख रहे हैं content में, और उसमें क्या-क्या हमने communicate करना है। Is that in42 का logo is one contender if we are showing anywhere here?
Speaker 1:  Part one, part two— वो जो greeting वाला part है, "Good morning" या whatever, क्या वो फिर से आ रहा है या नहीं आ रहा है? या वो पहले ऊपर आ रहा है और when we start scrolling तो वो फिर गायब या बिल्कुल ही minimal हो जाए?
Speaker 1:  वो वाले aspects भी to consider।
Speaker 2:  पहले तो हर जगह दिख रहा था in42 का logo।
Speaker 1:  हाँ।
Speaker 2:  वो आने—
Speaker 1:  नहीं, नहीं, नहीं। in42 का logo नहीं। in42 का logo अभी भी नहीं है।
Speaker 2:  नहीं, but this will be interesting कि अगर आप explore के place पे in42 का logo डालना चाहोगे कहीं। It could be interesting then।
Speaker 1:  In subtema है।
Speaker 2:  Wow।
Speaker 1:  Tab— वो change कर रहा हूँ मैं।
Speaker 2:  Wow।
Speaker 1:  तो tab change करो ना।
Speaker 2:  नहीं, नहीं, नहीं।
Speaker 1:  नहीं तो नीचे वाला।
Speaker 2:  नीचे वाला।
Speaker 1:  Okay, इसमें market जैसा आ गया।
Speaker 2:  इसमें क्यों नहीं?
Speaker 1:  हाँ, मतलब वही— वही main चीज़ है कि वो किस तरीके से—
Speaker 2:  पर phone पे—
Speaker 1:  तो ठीक है। मतलब एक जगह place करना वो थोड़ा है कि—
Speaker 2:  उनके यहाँ ऊपर भी है newer करके।
Speaker 1:  उनका तो fixed है। हमेशा है।
Speaker 2:  हाँ, change करो ना। Tab change करो।
Speaker 1:  बात क्यों?
Speaker 2:  App नहीं बदलते।
Speaker 1:  हाँ, क्योंकि— क्योंकि आप within— within एक page के sub-tab में change करोगे तो likely कि वो constant रहेगा। The moment आप bottom tab में change कर रहे हो, the page is changing।
Speaker 2:  Right।
Speaker 1:  वो चीज़ है ना, फिर वहाँ पे। वो— वो देखना important है कि वहाँ change हुआ है कि नहीं।
Speaker 2:  सब में ऐसा क्यों हो रहा है? Media में भी यही है। Home पे है, पर बाकी किसी भी tab में नहीं है।
Speaker 1:  Mostly।
Speaker 2:  पहली बार notice कर रहा हूँ।
Speaker 1:  ET भी ऐसे है।
Speaker 1:  Same।
Speaker 2:  कभी—
Speaker 1:  हाँ।
Speaker 2:  See, you have in home page as you— when you go। इसमें नहीं है, but यहाँ पे है।
Speaker 1:  Newer page में भी यही है। ये वाले scrolls में है सब में। इन वाले sections में।
Speaker 2:  हाँ।
Speaker 1:  Watch में तो चलो power meter भी आ जाता है। इसमें भी नहीं है।
Speaker 2:  इसमें भी नहीं है।
Speaker 1:  ठीक है। I think home page is a—
Speaker 2:  Home page and articles पे— articles पे क्या?
Speaker 1:  नहीं, only on home page में। At least जितना अभी देखा और—
Speaker 2:  Article में भी नहीं है।
Speaker 1:  InKB में भी नहीं है।
Speaker 2:  Article पे भी नहीं है।
Speaker 1:  Newer to call you down।
Speaker 2:  Subscribe करना।
Speaker 1:  हाँ। और किसी के article page पे भी नहीं है।
Speaker 2:  हाँ, article page में तो होगा ही नहीं। Article तो मतलब फिर भी एक sub-page की तरह है।
Speaker 1:  Sub-page आ गया ना।
Speaker 2:  Navigation पे नहीं। Navigation end page है वो।
Speaker 1:  हाँ।
Speaker 2:  ये हमारा एक use case बस उसमें आता है। Screenshots।
Speaker 1:  बहुत अच्छा।
Speaker 2:  मतलब वो— वो एक तरह का feature भी inbuilt है ना?
Speaker 1:  Stories share screenshot ना। और detecting the screenshot।
Speaker 2:  Detecting screenshot and giving them a custom screenshot। Which inshorts and everyone also does।
Speaker 1:  नहीं, नहीं, we are not doing it।
Speaker 2:  आगे v3 के लिए डालिए।
Speaker 1:  हाँ, डाल दिया मैंने। Especially for story cards sharing। Brief card sharing।
Speaker 2:  ठीक है। तो हाँ, मतलब home और इसकी तरफ लोगों का देखना ही पड़ेगा। And— हाँ, वो उसमें actually difference ये है कि लोगों का home ये है।
Speaker 2:  हमारा home brief है। इसलिए वो hierarchical difference आया।
Speaker 2:  क्योंकि जैसे अब आप बाकी सब tabs में जाना शुरू करते हो, वहाँ पे जरूरत नहीं पड़ती है। But first पे वो रख रहे हैं।
Speaker 2:  हमारे case में ये इसलिए disconnect आ रहा है क्योंकि in our way ये different form of home है हमारा। This is content point of view से।
Speaker 2:  इसलिए वो एक और disconnect feel हो रहा है। क्योंकि अब यहाँ पे भी अगर in42 आता है तो explore कैसे communicate करोगे, वो अपने आप में एक challenge आ जाता है।
Speaker 2:  पर जरूरत नहीं है। वैसे in42 के अंदर articles and companies हैं, तो हमारे पास already एक hierarchy यहाँ बनी हुई है इस page के अंदर।
Speaker 2:  So it can still work under explore।
Speaker 1:  फिर से repeat करने का बोला।
Speaker 2:  ये कह रहा हूँ, hierarchy यहाँ already बनी हुई है।
Speaker 1:  हाँ।
Speaker 2:  तो जब आप ये page खोलते हो, तो अगर explore ना भी आए और सिर्फ in42 आए, तो भी shit चल जाएगी।
Speaker 2:  दोनों तो नहीं आ सकता। In42 and explore दोनों तो नहीं आ सकता।
Speaker 2:  वो there's no scenario that happens।
Speaker 1:  अच्छा, क्या point है। in42 place करना तो जरूरी है। हाँ।
Speaker 2:  Font ये same है, बस weight change किया है।
Speaker 1:  हाँ, weight change किया है।
Speaker 2:  मतलब left and right बोल रहा है या फिर उसी same page पे?
Speaker 1:  Left and right।
Speaker 2:  नहीं, ये font अलग है।
Speaker 1:  अलग? ये कौन सा?
Speaker 2:  Fonts इस। Fonts इस।
Speaker 1:  It's slightly more textural than play fair। Play fair इतना readable नहीं feel होता।
Speaker 2:  हाँ, मतलब बहुत ज्यादा sharp है। हल्का sharpness है इसमें, लेकिन थोड़ा smoothness ज्यादा है।
Speaker 1:  Yeah।
Speaker 2:  F बहुत अलग है।
Speaker 1:  हाँ।
Speaker 2:  थोड़ा सा fancy है।
Speaker 1:  पर जो हम उसमें use कर रहे हैं, वो कौन सा है? Editorial में articles में? Charts में?
Speaker 2:  वो था Adverts Case Demo।
Speaker 1:  हाँ।
Speaker 2:  वो थोड़ा सा—
Speaker 1:  वो तो और भी ज्यादा—
Speaker 2:  Fancy है।
Speaker 1:  खतरनाक।
Speaker 2:  बहुत narrow भी हो जाता है वो।
Speaker 1:  हाँ।
Speaker 2:  बहुत छोटा है।
Speaker 1:  इधर articles में भी वो change करना पड़ेगा। Multi जगह placement font का करके देखना पड़ेगा। So—
Speaker 2:  I think you have some articles with the font। You have the articles with the font which you are mentioning। कुछ draft screens हैं।
Speaker 1:  Article में?
Speaker 2:  हाँ।
Speaker 1:  In article जो charts होते हैं हमारे—
Speaker 2:  Charts की बात कर रहे हैं।
Speaker 1:  In article charts में जो font है, वो अलग है। वो वही reference से हमने start किया था कल। वो वाला reference use करके। 
Speaker 1: ठीक है, direction wise coming out right। Sections का अब हम creation कैसे देख रहे हैं, मतलब this is also a nice way, but ये sectoral है। हाँ, ठीक है, sectoral भी हो सकता है, sectional भी हो सकता है।
Speaker 1:  क्योंकि अब तुम्हारा एक— which is a data and a user product statement level। These sections versus the sectoral sections।
Speaker 2:  हाँ।
Speaker 1:  Is a debate।
Speaker 2:  Okay. People are using sectors।
Speaker 1:  People are using sectors।
Speaker 2:  हाँ।
Speaker 1:  एक मिनट।
Speaker 2:  These sections no।
Speaker 1:  No।
Speaker 2:  एक मिनट लेते हैं।
Speaker 1:  एक मिनट, एक मिनट।
Speaker 2:  Sectoral में बहुत—
Speaker 1:  कुछ भी length जा सकती है इनकी। एक scroll के अंदर तो बहुत मुश्किल है।
Speaker 2:  वो तो हम transform कर देंगे।
Speaker 1:  सब हो जाएगा।
Speaker 2:  Display name change कर दो। Unfortunately, हम इतने लंबे रखते नहीं थे, पर वो डेटा लैब्स की वजह से इतने बड़े वाले आए हैं। क्योंकि वो सारे sectors अब डेटा लैब्स से full होते हैं।
Speaker 2:  डेटा लैब्स में तो फिर 450 sectors हैं। इसलिए इतना volume।
Speaker 1:  Infinite scroll।
Speaker 2:  इसलिए इतना volume exist करता है। नहीं, आपके case में तो I think we kept only 8 sectors in the onboarding, and यहाँ पे discovery भी within level C only at the opening up। But 8 also— also too many।
Speaker 2:  नहीं, नहीं, 8 is still fine. 8 से ज्यादा— मतलब 10 के ऊपर जाते ही फिर it becomes too much।
Speaker 1:  हाँ।
Speaker 2:  And hierarchy wise when we are showing both। For example, we show in depth also and sectors also in the same hierarchy level।
Speaker 1:  No. Should not be।
Speaker 2:  So मुझे ऐसा— again—
Speaker 1:  एक different—
Speaker 2:  एक— क्या बोलते हो उसको? एक अलग category form है वो।
Speaker 1:  नहीं, नहीं, but दो level of hierarchy of categories नहीं create कर सकते, वो भी एक challenge होता है।
Speaker 2:  Too much हो जाता है user के लिए।
Speaker 1:  दो level नहीं, जैसे app पे तो definitely—
Speaker 2:  हाँ, initially मतलब लगता है कि चलो दिखा देते हैं, but समझ नहीं आता है।
Speaker 1:  वो हमें उसमें hardcore नहीं—
Speaker 2:  मतलब I think जैसे उस time बात की, the only thing—
Speaker 1:  नहीं, ऐसे think कर लो, which is again I am trying to— now this is a different problem statement altogether।
Speaker 2:  हाँ।
Speaker 1:  Assume explore as an article section।
Speaker 2:  Article section?
Speaker 1:  Rather than having articles inside explore।
Speaker 2:  Okay।
Speaker 1:  Article as a separate section। फिर उसमें you have general articles, then you have exclusives of— you have other contents of in42.
Speaker 2:  Company as a separate tab।
Speaker 1:  हाँ। For company as a separate tab। Essentially, everyone is doing the same।
Speaker 1:  Is it leading to a different problem— problem statement altogether? But मुझे ऐसा लग रहा है it becomes even more powerful।
Speaker 2:  It's like getting data labs into a bottom bar tab।
Speaker 1:  हाँ, and articles especially।
Speaker 2:  Companies रख लो।
Speaker 1:  Company।
Speaker 2:  I think yeah, that might actually work। Because उसको अलग से productize करके दिखाओगे तो फिर उसकी—
Speaker 1:  Because people come।
Speaker 2:  उसका weight भी बढ़ता है property का।
Speaker 1:  Actually, हम अभी recently बात कर रहे थे, the thing is कि जब हम explore के अंदर जैसे article और companies हैं, and the weight is coming, it's more like a sub-tabs की तरह आ रहा है। And problem क्या है कि the nature, the consumption of article और companies एकदम ही अलग है।
Speaker 2:  बिल्कुल।
Speaker 1:  हाँ, एकदम ही अलग है। The moment में उसपे click करोगे, it is a page, consumption ही change हो रही है। Universe ही different हो गया है।
Speaker 1:  तो इसी वजह से even we were thinking कि क्या वो tabs रखनी चाहिए।
Speaker 2:  But—
Speaker 1:  Now—
Speaker 2:  पहले idea ये था कि सब कुछ बहुत minimal हो। But minimal होता हुआ लग नहीं रहा। मुझे तो expansively होता हुआ जा रहा है।
Speaker 2:  So I will down into।
Speaker 1:  हाँ, ठीक है। तो—
Speaker 2:  But मैं फिर भी, फिर भी article के अंदर मैं अगर वो tab भी है even। But पता नहीं, मैं फिर भी multiple hierarchies तो मैं फिर भी इतना in नहीं हूँ उसके लिए। It has to be very—
Speaker 1:  Single hierarchy in each tab।
Speaker 2:  Very simple होना चाहिए।
Speaker 1:  Single hierarchy in each tab only।
Speaker 2:  हाँ।
Speaker 1:  क्योंकि app पे उससे ज्यादा कोई consume नहीं कर रहा।
Speaker 2:  हाँ, because too much—
Speaker 1:  Should be more focused on कि— कि exactly cards किस तरीके से आ रहे हैं। अब not— अब let's suppose मेरे पास 6 section हैं। It cannot be कि सारे 6 section में same ही format use हो रहा है।
Speaker 1:  Priority order की कोई चीज़ है उसमें। वो—
Speaker 2:  वो— वो इस level में अभी ऐसा— इस वाले iteration में शायद ना कर पाओ। Eventually फिर हम sectional building थोड़ा सा करना शुरू कर सकते हैं। जैसे for example, जैसे तुम्हारा अभी— वही वो hiera— ये वापस information hierarchy problem में जो सालों से different forms and shapes में करते हुए आए हैं।
Speaker 2:  But जैसे in42 markets है, उसका header and पूरा style थोड़ा अलग है। So then that can— that kind of approach we can slowly start taking in different sections.
Speaker 2:  And then your card styles and everything can also slightly change।
Speaker 1:  नहीं, ऐसे इस version में भी कर सकते हैं ना। नहीं, as in— नहीं, नहीं, नहीं। नहीं, नहीं, in— नहीं, नहीं, having— either one is editorial.
Speaker 1:  When I say editorial, only about all the latest news which we publish in certain—
Speaker 2:  नहीं, sections अलग हैं। UI सबका अलग है। ये नहीं कर रहे।
Speaker 1:  हाँ, नहीं, हाँ, different section होगा। Section होगा, but section का differentiation नहीं होगा अभी। मतलब in terms of style and level।
Speaker 2:  हाँ, come through।
Speaker 1:  हाँ।
Speaker 2:  ठीक है, वो— वो भी एक separate call है कि when does things start synonymizing on the website।
Speaker 1:  हाँ।
Speaker 2:  क्योंकि अब हम app में divergence की तरफ जा रहे हैं। Fundamental divergence की तरफ जा रहे हैं। इससे पहले ठीक है, फिर भी अलग था, पर वो तो some word derived।
Speaker 2:  अब हम fundamental एक direction pick कर रहे हैं। तो अब website पे भी आना शुरू होना पड़ेगा।
Speaker 1:  So I believe— I believe it's— it— it is getting us to certain conclusions, certain foundation। It can be easily replicated to a certain extent in website rather than again reinitiating from scratch।
Speaker 2:  हाँ, but at the same time we have to— ठीक है, अभी इतना overcomplicated नहीं। ठीक है, let's— अभी app focus। तो अभी हमने app focus किया था कि app में ही इतने changes हो पाते हैं।
Speaker 2:  Website जैसे ही pick करते हैं, चीज़ें बहुत slow हो जाती हैं changes करने में। 
Speaker 2: ठीक है, anyway, समझ में आया।
Speaker 1:  ठीक है, तो information hierarchy is something that we have to lock then। What are we showing here? Both for this and for the companies when a new tab।
Speaker 1:  उसमें both का information hierarchy we have to close।
Speaker 2:  No, वो तो— वो— उसका तो sorted है। Companies— company document भी भेजा है ना।
Speaker 1:  हाँ, एक बार फिर से सारा summarize कर देना। Every reduction देख लो।
Speaker 2:  हाँ, probably।
Speaker 1:  Right after this discussion we can quickly summarize।
Speaker 2:  ठीक है। ठीक है, done।
Speaker 1:  Now this company's— थोड़ा देख लेना।
Speaker 2:  Hm?
Speaker 1:  इसमें हम next steps में और कोई points? Dependencies? Font ये अब— मतलब, is there something else that we have to discuss on the font?
Speaker 1:  Is there some other thought process to be applied when we are changing the font? या अभी we don't make a such a big deal out of it and iterate and keep iterating and then one month down the line then we think कि अब हर जगह unify जब कर जाएंगे तब फिर से font की call ले सकते हैं, right?
Speaker 2:  ठीक है। Color लेकिन सबसे पहले fix करते हैं।
Speaker 1:  Color ठीक है। Color is still fine।
Speaker 2:  Color logic has to be fixed।
Speaker 1:  Color is still fine। Color तो अभी भी हमारा उसी range में है, but हाँ, primary patch।
Speaker 2:  Which we range narrow down करें।
Speaker 1:  Akshay का actually point बहुत सही था। मतलब इस तरह कि जब मैंने सुबह बात की थी तो gradient is there। तो अब gradient ठीक है, दिख सही रहा है, but अब कौन से colors को मैं in42 से identify करूँ?
Speaker 2:  इसी guideline में मैंने कोई primary वो color नहीं है लिखा हुआ है। वही तो था, मुझे याद है। I think there was a primary red defined somewhere।
Speaker 2:  सिर्फ gradient नहीं exist करता।
Speaker 1:  I found 6 reds when I was doing my assignment।
Speaker 2:  वही तो defined होगा।
Speaker 1:  मैंने खुद 3 red use किए जब मैं अपना assignment कर रहा था।
Speaker 2:  सत्य का assignment था app।
Speaker 1:  हाँ, मेरा सत्य।
Speaker 2:  5 years ago।
Speaker 1:  इस brand extension वाले में भी कोई primary red नहीं है।
Speaker 2:  Primary red नहीं है।
Speaker 1:  Even if there was, the gradient puts it all out of context because it goes from a very soft red to a very orangish kind of a red।
Speaker 2:  नहीं, ये जो हम इन सब में जो हम reds use करते हैं।
Speaker 1:  This is much brighter than what I thought।
Speaker 2:  हाँ, I get it।
Speaker 1:  Yes, now that you mentioned it.
Speaker 2:  Every red is different।
Speaker 1:  Yes।
Speaker 2:  ये तो चलो article है। Article की feature में।
Speaker 1:  एक swatch कर लेते हैं final।
Speaker 2:  हाँ।
Speaker 1:  Universal ही comfort मिलेगा सबको।
Speaker 2:  How do you decide a red shade?
Speaker 1:  Screen— एक standard screen template बना लेते हैं, उसमें अलग-अलग red use करके देखते हैं।
Speaker 2:  Then कहाँ-कहाँ use हो रहा है वो?
Speaker 1:  अलग-अलग displays पे check करके देखते हैं कौन सा best निकलती है।
Speaker 2:  क्योंकि social में कौन सा red use हो रहा है, वो सबसे ज्यादा perceived red होगा अभी।
Speaker 1:  हाँ, क्योंकि I think— I think the social में ये वाला— ये जो देख रहे हो ना, red— हाँ, क्योंकि ये तो भाई, मतलब मैं different screen में बता सकता हूँ कि बहुत brighter भी दिख सकता है। It will not work।
Speaker 2:  It's very— हाँ, interesting। तो screen पे इतना नहीं चलेगा। इसको soft करना पड़ेगा थोड़ा।
Speaker 1:  Social पे concentrate करें। I think social red is one।
Speaker 2:  Social पे वो एक band जाता है hero post में। तो वो एक तरह— एक accent color की तरह।
Speaker 1:  Texture।
Speaker 2:  हाँ, I know। But यहाँ पे hero color है।
Speaker 1:  ठीक है, अभी कहाँ-कहाँ red of different shades use हो रहा है, मतलब जो भी shade में use हो रहा है, वो पहले आपको relate करते हैं। जिसमें primarily एक social है जो matter करता है। in42 की website पे जो primary accent color use हो रहा है।
Speaker 2:  In42 पे बस gradient है।
Speaker 1:  नहीं, नहीं।
Speaker 2:  Of course।
Speaker 1:  Top— top— top जो band है, उसमें तो gradient ही है ना।
Speaker 2:  Gradient।
Speaker 1:  इसमें तो—
Speaker 2:  City पे gradient।
Speaker 1:  City पे gradient।
Speaker 2:  मतलब एक चीज़ अच्छा नहीं होती, मतलब एक चीज़ अच्छा है कि चलो gradient है तो हर जगह gradient है।
Speaker 1:  Actually, in42 की logo में जो red है, वो—
Speaker 2:  वो, वो।
Speaker 1:  That is the only thing that's constant।
Speaker 2:  वो वाला red।
Speaker 1:  एक second, in42 के logo में gradient नहीं है।
Speaker 2:  नहीं, नहीं।
Speaker 1:  नहीं, नहीं, नहीं।
Speaker 2:  In42 के logo में कभी gradient नहीं था।
Speaker 1:  एक second।
Speaker 2:  है, gradient।
Speaker 1:  नहीं है।
Speaker 2:  नहीं, नहीं, नहीं।
Speaker 1:  Gradient नहीं हो सकता। ये solid है।
Speaker 2:  एक second, कैसे?
Speaker 1:  नहीं, gradient नहीं है।
Speaker 2:  Gradient नहीं है।
Speaker 1:  नहीं।
Speaker 2:  नहीं।
Speaker 1:  मैं कैसा बना रहा था? ये वाला gradient कैसा है?
Speaker 2:  ये— ये— this is the only one that's constant। जो logo में red था, that was the primary red that we had।
Speaker 1:  I'm sure। एक second, यार, मैं अभी भी थोड़ा confuse हूँ। मुझे देखना पड़ेगा।
Speaker 2:  नहीं, नहीं, नहीं।
Speaker 1:  In42 का website खुलवाएँ एक बार। मेरे को— मेरे को क्यों लग रहा है कि gradient है?
Speaker 2:  नहीं, नहीं, वो 2k की वजह से।
Speaker 1:  हाँ, हो सकता है।
Speaker 2:  वो जो outlines जिस तरह से बनी हुई हैं, उसकी वजह से।
Speaker 1:  हाँ, so this was the original in42।
Speaker 2:  हाँ, तो एक article बना लो।
Speaker 1:  अब यहाँ से backtrack कर सकते हैं। मतलब अब इसको भी हम change कर रहे हैं, तो फिर यहाँ से— this becomes your base to—
Speaker 2:  Because NX is—
Speaker 1:  NX is the softer part of the red।
Speaker 2:  हाँ।
Speaker 1:  That— that works greatly for the app।
Speaker 2:  I get it।
Speaker 1:  तो ये red अब हमारा अभी for now—
Speaker 2:  उसको baseline में—
Speaker 1:  हाँ, उसको baseline की तरह treat करके now—
Speaker 2:  नहीं यार, मतलब—
Speaker 1:  अब in—
Speaker 2:  It's like—
Speaker 1:  Original iris logo देख लो।
Speaker 2:  इतना गलत मैं कैसे हो गया? मैं तो इतने टाइम से बना रहा हूँ।
Speaker 1:  हाँ, तो—
Speaker 2:  ये red— ये भी red है। This is a red। ये red होता है।
Speaker 2:  Yes. This is a softer red।
Speaker 1:  कहते हो ना मैंने पूरा insult किया था।
Speaker 2:  ये red भी अलग है। ये शायद literage का red है। Literage का भी red अलग है।
Speaker 1:  हाँ, अलग है।
Speaker 2:  ये वाला same है।
Speaker 1:  The left one look—
Speaker 2:  यहाँ पे है ना?
Speaker 1:  ऊपर वाला नीचे वाला।
Speaker 2:  काफी variation है।
Speaker 1:  कह रहा हूँ ना मैं, अलग है।
Speaker 2:  What do you—
Speaker 1:  See, again, I'm not—
Speaker 2:  Not able to get it।
Speaker 1:  Everywhere।
Speaker 2:  थोड़ा darkish, थोड़ा lightish, ऐसे? ऐसे?
Speaker 1:  अब देखना शुरू।
Speaker 2:  थोड़ा darkish, थोड़ा—
Speaker 1:  हाँ।
Speaker 2:  Then this—
Speaker 1:  This वाला part dark और ऊपर एकदम light।
Speaker 2:  Print में तो हमारा red वाला कम है।
Speaker 1:  क्योंकि यहाँ पे— देखो, यहाँ पे इतना नहीं है। मैं बता रहा हूँ, in42 में भी है। आप देख लेना, जो original file मंगवाओगे, उसके बाद वो भी—
Speaker 2:  नहीं, नहीं, solid है।
Speaker 1:  वो क्योंकि split हो रखा है 2, तो वो अलग लग सकता है। थोड़ा dark अलग लग रहा है।
Speaker 2:  उसमें दिख जाएगा।
Speaker 1:  होगा तो in42 logo।
Speaker 2:  ये तो सालों पहले वाला version ये भी exist करता था।
Speaker 1:  This was 10 years ago।
Speaker 2:  कहाँ?
Speaker 1:  ये कहाँ से आया?
Speaker 2:  This is the old data labs।
Speaker 1:  This is the data labs।
Speaker 2:  ठीक है, देखता हूँ। I'll get it।
Speaker 1:  तो अब next step क्या है? Summarize।
Speaker 2:  मैं तो red पे work करता हूँ।
Speaker 1:  ठीक है, तो तुम्हारा ये in42 logo का red is the baseline red। अब red का shade वहाँ पे हमें देखना है। That is one part।
Speaker 1:  Second is font। अभी ठीक है, let's go ahead with the font।
Speaker 1:  अभी ज्यादा font तो—
Speaker 2:  Fonts isn't enter है ना अभी?
Speaker 1:  हाँ, fonts is on। मैंने guys दिया है अभी।
Speaker 2:  Fonts तुम लोग अपने बीच में lock कर लो। Directionally हाँ, serif and sans serif का combination is obviously the direction that we want to take। तो वो एक part हो गया।
Speaker 2:  Edge cases real content की variations के साथ भी try करके देख लो। वैसे तो font wise तो covered है।
Speaker 2:  लंबे नाम, छोटे नाम, वो वाले cases हमें यहाँ देखने हैं।
Speaker 1:  Header, tags।
Speaker 2:  Tags को हाँ, without— ideally without वो एक बार try करके भी देख सकते हो। To keep everything focused on this। क्योंकि ये इकलौता अलग type का roundness है, compared to all other rounds।
Speaker 2:  मतलब radius, quarter radiuses। ये अलग से दिख रहा है।
Speaker 2:  More than even the rest। तो ये extra prominence हो रही है इसमें।
Speaker 2:  Information hierarchy। And we agreed to separate।
Speaker 2:  मतलब explore is not— now there is no explore anymore। There is—
Speaker 1:  There's no article company।
Speaker 2:  There's news।
Speaker 1:  There's news company।
Speaker 2:  In42 homepage? यहाँ पे?
Speaker 1:  Brief— नहीं, brief, news।
Speaker 2:  अच्छा, you're talking about logo।
Speaker 1:  हाँ, कि वहाँ पे explore की जगह logo place होगा ना।
Speaker 2:  अब तो मैं हर जगह हो सकता हूँ।
Speaker 1:  हाँ।
Speaker 2:  अच्छा, ऊपर बहुत ज्यादा space आ गया अभी।
Speaker 1:  अगर वो segmented है तो फिर तो ठीक है।
Speaker 2:  हाँ, we have 4 tabs now।
Speaker 1:  And bottom menu? अब हम change नहीं कर रहे bottom bar को fundamentally।
Speaker 2:  Glass वाला?
Speaker 1:  Already change हो चुका है ना shape।
Speaker 2:  Glass वाला।
Speaker 1:  Glass वाला नहीं, वो— मतलब thinner strip।
Speaker 2:  The floating strip।
Speaker 1:  Floating strip।
Speaker 2:  हाँ।
Speaker 1:  Instead of the full bottom।
Speaker 2:  तो I think already कर चुके।
Speaker 1:  वो तो already— हाँ, I was just about to say।
Speaker 2:  नहीं, live में नहीं है, but हाँ, जो अभी।
Speaker 1:  Design— design wise तो।
Speaker 2:  हाँ, थोड़ा change हो सकता है, देखता हूँ।
Speaker 1:  And then that will bring your question of your header में अब हम क्या रख रहे हैं और menu में नीचे bottom bar में क्या ले जा रहे हैं।
Speaker 2:  हाँ, ठीक है।
Speaker 1:  So अब already we are at 4 items now। नहीं, 3— 4।
Speaker 1:  हाँ, 4। Washlist का कोई usage है अभी?
Speaker 2:  नहीं, इतना नहीं है। Only 15% people are using।
Speaker 1:  Merge them into profile and—
Speaker 2:  I was about to say this।
Speaker 1:  And make the profile there।
Speaker 2:  Then people।
Speaker 1:  And profile को हम फिर और— मतलब वो profile— see, news apps में देखोगे तो everyone— almost everyone has done for you।
Speaker 2:  हाँ।
Speaker 1:  As the last tab। उसी में ही profile है, उसी में ही ये।
Speaker 2:  Watchlist, जो भी वही है।
Speaker 1:  सब कुछ वहाँ पे है।
Speaker 2:  Then let's— हम भी ऐसे करते हैं, for you। लिख के profile, everything goes under that। And top— eventually दो चीज़ें।
Speaker 2:  One is streak, second is search।
Speaker 1:  Streak page पे कोई पहुँच रहा है?
Speaker 2:  हाँ, लोग आ रहे हैं। 25, 20, 25— 25% people आ रहे हैं।
Speaker 1:  हाँ।
Speaker 2:  That's a big number।
Speaker 1:  20%।
Speaker 2:  Interesting।
Speaker 1:  Streak is an interesting concept। तो streak भी technically speaking profile के अंदर जाना चाहिए, but हाँ, उसकी फिर prominence खत्म हो जाएगी completely।
Speaker 2:  हाँ।
Speaker 1:  फिर कोई नहीं use करेगा। ठीक है, for now अभी streak रखते हैं। Streak का— but we'll have to eventually start gamifying it a little।
Speaker 2:  हाँ, once we— हाँ, once the— at least fundamentals started, then people start using, then streak can come into play।
Speaker 1:  Right। तब उसमें कुछ करना पड़ेगा।
Speaker 2:  हाँ।
Speaker 1:  अभी तो वो बस है for the sake of it।
Speaker 2:  हाँ।
Speaker 1:  ठीक है। So then हाँ, ये सारी things हमने बात कर ली। इसका balance हमें देखना है, ये roundness का।
Speaker 2:  वैसे तो अभी नहीं होगा ना ये। It comes with something else now।
Speaker 1:  क्या?
Speaker 2:  Article companies का।
Speaker 1:  हाँ, तो वो चाहिए।
Speaker 2:  हाँ, that becomes out of the question।
Speaker 1:  And इन दोनों में से we've decided this direction।
Speaker 2:  Structure में।
Speaker 1:  Now, इसमें I've not thought about it, should we keep our newsletter section as separate? When I say as a— another section in the same news page। Newsletter, AI shift।
Speaker 1:  Checkout— checkout और D2C वो तो थोड़ा specific हो गया। But markets— all these things।
Speaker 2:  वो जो information hierarchy है, that is what we need to know।
Speaker 1:  ठीक है।
Speaker 2:  I thought you were specific।
Speaker 1:  Newsletters for the sake of newsletters नहीं है, right?
Speaker 2:  हाँ, not as a topic, just saying in our discussion, should we keep it separate। I thought the news— the hierarchy which you're talking about, I thought inside article— I mean, inside news में।
Speaker 1:  This is the information।
Speaker 2:  हाँ, that could be development tags also। Not necessarily your markets, AI shift। Those need to be different।
Speaker 2:  I probably can discuss some further।
Speaker 1:  क्या हम यहाँ पे दिखा रहे हैं? Both यहाँ articles में भी और news में भी और companies में भी।
Speaker 2:  हाँ, ठीक है।
Speaker 1:  Both। And the filtering— हाँ, companies में filtering mechanism पे अभी कोई usage and plus कोई direction जो अभी नहीं है। That's another complicated thing।
Speaker 2:  नहीं, अभी जो existing चल रहे हैं, let it go। इसमें people are coming from company page, they are looking for, they are using search bar। उसमें at least 16-17%।
Speaker 1:  हाँ, क्योंकि ऊपर search जा रहा है।
Speaker 2:  नहीं, they are landing— eventually the— the— how people coming to the search, they are coming to companies, they are browsing few companies, and they are also tapping on search and searching few companies, through which we are getting no results अभी, unfortunately।
Speaker 1:  हाँ, वो तो challenge वाला issue है। But यहाँ के भी filters और यहाँ के भी जो changes होने थे, वो सारे भी— that also get away, ना?
Speaker 2:  हाँ।
Speaker 1:  वो—
Speaker 2:  नहीं, that— okay, I'll tell you, this is how it's going to look। If you just— these becomes your sections। Now these— this is how recently funded एक section है, एक का— फिर what is next?
Speaker 2:  It just launches your another section। That's— that's how it has been structured।
Speaker 1:  जैसे हम article— news के लिए भी sectional कर रहे हैं।
Speaker 2:  हाँ।
Speaker 1:  Discoverable and— and then—
Speaker 2:  हाँ, maybe वो— can you go to that screen?
Speaker 1:  Makes sense। Logically makes sense, but a sort thing।
Speaker 2:  नहीं, नहीं, सत्य— एक बार वो company page— obviously design तो change होगा, but this is how— can you click on सत्य's screen?
Speaker 1:  नहीं, पर मैं भी click करूँगा।
Speaker 2:  Once again, जैसे it gets followed on— auto followed on—
Speaker 1:  ये horizontal क्यों कर रहे हैं हमारे इस बार सब कुछ?
Speaker 2:  आप scroll ही नहीं कर पाते।
Speaker 1:  कैसे? किसी भी direction में scroll कर रहे हो, scroll तो करते ही हैं।
Speaker 2:  हाँ, ऐसे recently funded फिर—
Speaker 1:  By the way, this is dead, right? इसका क्या कर रहे हैं?
Speaker 2:  नहीं, नहीं, that is— that was never dead।
Speaker 1:  अभी तो हटाया था वो।
Speaker 2:  नहीं, that is— he's just want to visualize as a page, so—
Speaker 1:  This is another debatable point। Then again, two hierarchies are—
Speaker 2:  नहीं, एक ही hierarchy।
Speaker 1:  Hierarchy I know, but it's another thing। ठीक है, अभी आते हैं उस पे।
Speaker 2:  हाँ, if you just scroll further— और सत्य? हाँ, just launched। हाँ।
Speaker 1:  समझ गया।
Speaker 2:  Just launched। ऐसे further।
Speaker 1:  Something is off। मतलब logic wise I get it, what the sectional approach—
Speaker 2:  नहीं, उसमें— इसमें एक आता है ना, browse all the companies।
Speaker 1:  That is not hitting।
Speaker 2:  नहीं, नहीं, इसमें आता है browse all companies।
Speaker 1:  By the way, card में हम क्या information दिखा रहे हैं, that is also another point that we have to look।
Speaker 2:  हाँ, I— that is— I'll tell you।
Speaker 1:  हाँ, वो मैं रखूँगा। Just making a note for separate discussion। वो अलग से आ जाएंगे।
Speaker 1:  हाँ। मतलब, but this is—
Speaker 2:  नहीं, उसके बाद तो change करना पड़ेगा।
Speaker 1:  हाँ, change करना पड़ेगा, but— नहीं, what I'm trying to—
Speaker 2:  हाँ, बताओ।
Speaker 1:  Browse all companies तो ऊपर you have mentioned ना।
Speaker 2:  हाँ।
Speaker 1:  I'm trying to show that so that he understands। I mean, visualize the path।
Speaker 2:  हाँ, मतलब he's saying कि जो ऊपर आपके tabs दिख रहे हैं ना, like suppose आप अगर just launch पर click करते हो, automatically scroll down to just—
Speaker 1:  No, no, no. What I'm talking is— this is— this is one section। यहाँ पे, if you remember, यहाँ पे एक section है browse all companies करके।
Speaker 1:  यहाँ पे—
Speaker 2:  अच्छा, वो वाला।
Speaker 1:  हाँ, that design।
Speaker 2:  ठीक है, actually तुम्हें जाना है—
Speaker 1:  हाँ, यही है ना?
Speaker 2:  हाँ, यही। हाँ, इसके लिए।
Speaker 1:  Something like this। Obviously it's like raised this week। Browse all companies।
Speaker 1:  That opens up a generic page।
Speaker 2:  हाँ, makes sense। मतलब, this makes sense।
Speaker 1:  हाँ, that— उसमें filter होगा।
Speaker 2:  नहीं, but this is weird कि when I click on IP home, which will scroll to this।
Speaker 1:  हाँ।
Speaker 2:  वो थोड़ा सा टिक्की है। अभी usage— अभी तो already है।
Speaker 1:  नहीं, उनका मतलब tricky किस— किस sense में?
Speaker 2:  नहीं, मतलब वो UX point of view से कौन सा purpose? वो किस— मतलब, what is their use case? Different use cases different ways में।
Speaker 2:  जैसे data labs का जब— तो पूरी दुनिया अलग है। पर feed चल रही है या— नहीं, सब— view all companies पे क्या होगा?
Speaker 1:  Redirect to the company page जहाँ पे filter है।
Speaker 2:  Full search page with filter added।
Speaker 1:  Pre-applied filter। हाँ।
Speaker 2:  सोचो। Multiple— पर इसमें use cases बहुत सारे हैं। मतलब, user journeys बहुत सारी possible हैं।
Speaker 2:  Different use cases।
Speaker 1:  The idea is people coming to a company page without any idea। Just to see।
Speaker 2:  हाँ, एक second। उसमें important ये भी होना चाहिए कि हमारे पास data हो दिखाने के लिए। क्योंकि I think हमने जो sections lock किए, it's also based upon कि हमारे पास data भी है कि नहीं।
Speaker 2:  Even इसमें जो आप पहले वाला design देख रहे थे ना, उसमें आप जो भी data देख रहे हो ना, उसमें—
Speaker 1:  Will exist for sure।
Speaker 2:  वो तो real data ही है। That's the real data। And उसके जो data points हैं, वो भी सब real ही हैं।
Speaker 2:  Depend— हाँ।
Speaker 1:  What if sections are horizontal scroll?
Speaker 2:  वो तो कर सकता है। Horizontal scroll तो कर ही सकता है।
Speaker 1:  अब तो अलग करना है।
Speaker 2:  हाँ?
Speaker 1:  अब तो अलग करना है।
Speaker 2:  करना तो वैसे ही है ना। मतलब, वो तो फिर वो article चीज़ में भी तो वो तो दोनों UI ही match नहीं हो रहा ना।
Speaker 1:  हाँ।
Speaker 2:  नहीं, नहीं, नहीं, नहीं। I'm saying—
Speaker 1:  हाँ, taking article tabs।
Speaker 2:  Tabs तो अलग करना है।
Speaker 1:  Article companies।
Speaker 2:  हो रहा तो था यार।
Speaker 1:  हाँ?
Speaker 2:  When we last discussed, it eventually makes sense also। वो बन ही नहीं रहा था ना। साथ में ही नहीं आ रहा था वो।
Speaker 1:  Again, ठीक है। अब compare with the first draft। I'll say— I was thinking it should be right thought by data labs।
Speaker 1:  फिर तो वो specific हो गया।
Speaker 2:  कर सकते हैं। मतलब, देख सकते हो। बाद में देख सकते हो।
Speaker 1:  हाँ।
Speaker 2:  हाँ, यार, solve कर लेते हैं।
Speaker 1:  That is why I stopped making— stopped before only।
Speaker 2:  जैसे यार, मैं आज जिम जाना है यार। So far I have the motivation to go।
Speaker 2:  Last week I'm not— जैसे the last week was missed ही। I'm not missed one day।
Speaker 2:  I've never been to gym after office। If it is छुट्टी, I'll still go।
Speaker 2:  But after office तो I've never in my life। At least probably once twice।
Speaker 1:  सुबह— सुबह even I can go करना, सुबह बहुत भीड़ होता है यार। बहुत भीड़ होता है।
Speaker 2:  अच्छा।
Speaker 1:  See, अभी— अभी also I have a काम, like right after this meeting, अभी hierarchy discuss करना है और something which I've mentioned तो वो भी complete।
Speaker 2:  Hierarchy।
Speaker 1:  Hierarchy।
Speaker 2:  ओह।
Speaker 1:  वो भी वैसे करना है। अनुभूति was asking। But हाँ, वो भी करना है।
Speaker 1:  अभी काम करूँ? मुझे अभी— I've recently did this Grok bot।
Speaker 1:  So इसमें ऐसे बहुत सारा bot you can create। You give the one instruction to this bot and say that these are my in 42 tasks।
Speaker 1:  कर लो। Then this bot assigns the task to product manager।
Speaker 1:  So it creates its own agent and gets the task done।
Speaker 2:  Grok bot?
Speaker 1:  हाँ। वो थोड़ा interesting है। But the problem is token usage बहुत ज्यादा है।
Speaker 1:  It's extremely crazy।
Speaker 2:  Someone's figured out a way to use Grok bot plus your own cloud subscription।
Speaker 1:  हाँ, I'm just trying to figure out— नहीं, I was not aware, but I'm just trying to figure out if there is any balance which I can make out of it।
Speaker 2:  Use the open weight model integrated into this। Use the architecture of Grok with the tokens of open model।
Speaker 1:  Open model और— नहीं, open model में तो you'll have a lot of limitation। Or I should see how do I use the cloud subscription।
Speaker 2:  हाँ, वो भी है। वो किसी ने कर लिया already।
Speaker 1:  अच्छा।
Speaker 2:  There are some limitations within that approach, but people have done that।
Speaker 1:  हाँ, at least to a certain extent।
Speaker 2:  People have solved this already।
Speaker 1:  हाँ। इसमें— it because it is very effective। When I want to do certain tasks, it's super effective।
Speaker 1:  But the only problem is it's—
Speaker 2:  Why can't you do this in cloud code?
Speaker 1:  Hmm?
Speaker 2:  Why can't you do all of this in cloud code already?
Speaker 1:  इसमें for an example—
Speaker 2:  Same चीज़ बना लो। वो web version बना लो। उसमें ही different tasks।
Speaker 2:  उससे ज्यादा manage कर लो।
Speaker 1:  हाँ, फिर I cannot have a— I have a shared account ना, तो—
Speaker 2:  नहीं, cloud code में तो it doesn't matter if you have a shared account।
Speaker 1:  हाँ, you'll have— if you want to remote sessions, तो your— your context goes to on web also। One है। Second, there are—
Speaker 2:  आपका पूरा VM। VM। We'll have to make a larger VM।
Speaker 1:  हाँ।
Speaker 2:  Like my structure is VM। VM based। I have all of these desks।
Speaker 1:  Hmm।
Speaker 2:  And they can talk to each other।
Speaker 1:  हाँ।
Speaker 2:  They are— all of them are remote।
Speaker 1:  Sorry।
Speaker 2:  All of them are remote connections।
Speaker 1:  हाँ।
Speaker 2:  And all of them can talk to each other।
Speaker 1:  हाँ। But जो मेरा है—
Speaker 2:  Only one VM।
Speaker 1:  हाँ, but मेरा तो ऐसा नहीं है ना।
Speaker 2:  नहीं, वो तो VM पे setup करा लो ना। Same backup वाला।
Speaker 1:  हाँ, वही करना पड़ेगा। VM और data labs।
Speaker 2:  उसमें वो adds किए हैं। But if a lot of people are using the same VM, then you'll have to see because— मैंने तो memory management and सब कुछ management— this approach has killed the VM three-four times so far। Now I've created systems so that that does not happen।
Speaker 2:  But—
Speaker 1:  In this case, let's say you might— if you're even using VM in a account, then you will— you will have your GitHub and all the sources connected।
Speaker 2:  Doesn't matter। Cloud code is not shared।
Speaker 1:  Cloud code is not shared। नहीं, see, for an example, if I— if it is a— there are two sessions in cloud code में। Local and web sessions।
Speaker 2:  फिर भी शो बाद में करते हैं।
Speaker 1:  हाँ, फिर ठीक है।
Speaker 2:  Full conversation and etc. And then someone opens the AI वाला topic and— It can go for an hour or two easily।
Speaker 1:  हाँ।
Speaker 2:  Coming back। ठीक है।
Speaker 1:  But मुझे— let me know how do we set up। But coming back। हाँ, so this is how visualizing।
Speaker 1:  But card ways when comparatively बहुत change होगा। But इसमें जो भी data है, that data do exist in your previous design।
Speaker 2:  हाँ, previous design।
Speaker 1:  What— what other sort of data? We can discuss।
Speaker 2:  But whatever the data that we are trying to show।
Speaker 1:  Fallbacks and arrows can be created। जो हमने शायद Cardio में desktop पे किया है ना, fallback data points।
Speaker 2:  हाँ, but the thing is कि अगर मान लो कि आपका एक section dedicated है particular चीज़ के लिए, cannot— वो तो आप fallback पे design कर सकते हो ना। सारे card में सारे data points।
Speaker 1:  हाँ, वो— वो तो filter करना पड़ेगा। Then the section has to be created in such a way that this— for example, if it's this thing, then that value has to exist for it to happen।
Speaker 2:  वो तो check लगाना पड़ेगा। वो filter level पे check लगाना पड़ेगा। Logic level पे।
Speaker 2:  वो तो होना ही पड़ेगा। But otherwise, मतलब, for example, if lead investor is not available, for example, then उसकी जगह you're showing sector, for example।
Speaker 2:  That is what I mean by fallback। हमारा primary तो ये था इस case में, इस section के लिए।
Speaker 2:  But if lead is not available, then you would fall to show sector instead or whatever। जो भी logic है।
Speaker 1:  हाँ।
Speaker 2:  That is what I mean by that fallback।
Speaker 1:  हाँ। That is in consideration when we do implement।
Speaker 2:  इस page पे भी आएगा।
Speaker 1:  नहीं, नहीं, नहीं, नहीं।
Speaker 2:  वो बहुत— मैं इधर-उधर काम कर रहा था।
Speaker 1:  Cloud थोड़ा गड़बड़ कर दिया। But हाँ।
Speaker 2:  समझ गया। बाकी ठीक है।
Speaker 1:  This is what I'm exploring। Because people coming to a company page, they might not have any intention। So we are giving option more to explore।
Speaker 1:  अगर इसका कुछ exact चाहिए तो they can go ahead and do।
Speaker 2:  Behavior point of view से, do people use this first, or people scroll and then use this?
Speaker 1:  मुझे लग रहा है people use first। They scroll। Or probably browse all companies।
Speaker 1:  अब बताओ।
Speaker 2:  देखो, anyways—
Speaker 1:  It depends on how prominent we keep it।
Speaker 2:  नहीं, नहीं, मैं वही बता रहा हूँ कि the thing is कि this is not a filter। This is a navigation। Table of content। 
Speaker 2: ठीक है। अगर वो scroll भी करेगा, तो भी ठीक है। But let's say उसने click कर दिया, तो automatically he gets to know that he scrolled down to that section।
Speaker 2:  So वो behavior वही behavior है। Scrolling वाला behavior is the only behavior left in this page।
Speaker 2:  और कोई behavior है भी नहीं। अगर वो tabs पे भी click कर रहा है, तो वो scroll down हो के नीचे जा रहा है ना।
Speaker 2:  It's an evident behavior। कि मतलब, अच्छा, I'm okay, this is the— यही page में जो हो रहा है, वो हो रहा है।
Speaker 2:  So वो है।
Speaker 1:  अगर इस तरह से इसका architecture है, तो फिर इसमें तुम्हारा particle style, not the UI। Scroll sections, each section is one— वो— वो वाला approach चल जाएगी। Horizontal scroll, मतलब, this section being a horizontal scroll।
Speaker 1:  वो— that is less information overload। इसमें the information overload is too much।
Speaker 2:  हाँ, वो तो है, मतलब, वो तो—
Speaker 1:  Feed— feed वाले approach में it becomes too— too much information।
Speaker 2:  But number of sections भी थोड़े ज्यादा होने चाहिए। कुछ खत्म ना हो जाए।
Speaker 1:  हाँ। नहीं, वो तो बन जाएंगे।
Speaker 2:  नहीं, पाँच sectors हैं। वैसे वो वैसे ही बड़ा है।
Speaker 1:  पाँच?
Speaker 2:  पाँच sectors?
Speaker 1:  नहीं, पाँच sections।
Speaker 2:  Sections पे text।
Speaker 1:  नहीं, वैसे यूँ खत्म हो जाएंगे। से ही भी काटो, तो—
Speaker 2:  बन जाएंगे और बन जाएंगे।
Speaker 1:  हाँ, थोड़ा सा— थोड़ा मतलब, थोड़ा करना पड़ेगा। थोड़ा।
Speaker 2:  And then— चलो, वो आगे की बात है। But हाँ, in the section, orders is personalized to the user type। Persona type।
Speaker 1:  हाँ, that based on what people have seen।
Speaker 2:  नहीं, user type के basis पे भी।
Speaker 1:  नहीं, हाँ, फिर वो तो simple personalization हो गया।
Speaker 2:  हाँ।
Speaker 1:  वो ठीक है। But हाँ, we've written this as part of v3। So—
Speaker 2:  ये page का design क्या है? तो मेरा ये question follow on ये है। Browse all companies।
Speaker 1:  नहीं, it will be simple। Pills जो हमारा पहले का— something similar होगा।
Speaker 2:  Table based या non-table based?
Speaker 1:  Non-table based ही होगा। मतलब, industry।
Speaker 2:  हाँ, table।
Speaker 1:  Table तो नहीं। बिल्कुल नहीं। हाँ, but मतलब, उसमें भी बस एक ही question रहेगा कि data points दिखेंगे कि नहीं।
Speaker 2:  और कौन से? और कितने?
Speaker 1:  मुझे ऐसा लग रहा है—
Speaker 2:  But हाँ, it— it थोड़ा सा consistent भी होना पड़ेगा। मतलब, हर card में अलग-अलग नहीं दे सकता। Because—
Speaker 1:  हाँ, I was just about to say, हमारे पास तीन fixed हैं: location, date, phone। कुछ fixed है। We'll continue with that।
Speaker 1:  क्योंकि every has— it could be n number of— some data exist, some data will never exist। तो we'll have— these are the few things which will—
Speaker 2:  Overall variety of data points। For example, funding, revenue, profit।
Speaker 1:  Hmm।
Speaker 2:  Shareholding।
Speaker 1:  वैसे तो already exist है ना। Sections।
Speaker 2:  वो priority— I think universally सही है। But थोड़ा सा अगर आप वो condition भी लगा रहे हो कि अगर specific filter भी है, funding, high to come, ये सब जो भी जा रहा है, तो उसमें funding information नहीं दिख रहा। Let's suppose— या फिर ऐसा कोई filter है, but वो priority order में बहुत नीचे है।
Speaker 2:  But filter is added for particular thing, पर उसमें उसका data points नहीं दिख रहा। तो बस वो एक case है।
Speaker 1:  In that case, it becomes very weird।
Speaker 2:  हाँ।
Speaker 1:  And उसमें तब ज्यादा और weird हो जाएगा कि कुछ companies में दिख रहा है और कुछ companies में नहीं दिख रहा। तब तो और weird हो जाएगा। क्योंकि you give a hint कि अच्छा, ये दिख सकता है, but then बाकी companies में नहीं दिख रहा।
Speaker 2:  ठीक है। I think directional भी मिल गया है।
Speaker 1:  हाँ, which is why I'll say, let's go with जो minimum होगा, which is your date, location।
Speaker 2:  Seed point continue होगा ना।
Speaker 1:  नहीं, उद्देश्य— मतलब, वही मैं कह रहा हूँ। मतलब, ये वैसा नहीं होगा। मतलब, obviously आप ये imagine नहीं करोगे कि आप phone size, lens card etc.
Speaker 1:  पे लगा दोगे।
Speaker 2:  हाँ, raise the sweep ऐसा।
Speaker 1:  हाँ, it can be।
Speaker 2:  Raise the sweep ऐसा।
Speaker 1:  वैसा।
Speaker 2:  Obviously।
Speaker 1:  Lens card पे नहीं हो पाएगा। That I agree।
Speaker 2:  वो style—
Speaker 1:  अलग style।
Speaker 2:  वैसे arc कर रहा है। Arc is— पर उसका font थोड़ा सा और balanced है उसके लिए।
Speaker 1:  Arc।
Speaker 2:  The arc।
Speaker 1:  Arc web। The arc web।
Speaker 2:  Arc देखा नहीं तुमने अभी।
Speaker 1:  अच्छा, ये— ओह, भाई, बहुत टाइम हो गया इसको देखे हुए।
Speaker 2:  Data labs के time पे ये इसके कुछ section के लिए हमने एक बार देखा था।
Speaker 1:  But—
Speaker 2:  यहाँ पे ये use कर रहे हैं।
Speaker 1:  But आपको पता है—
Speaker 2:  थोड़ा balanced है।
Speaker 1:  नहीं, नहीं, नहीं, मैं आपको बताता हूँ। ये still बहुत ज्यादा work करेगा जब आपके number of sections कम हैं और data points कम हैं। This is more like a packaged section।
Speaker 1:  आपको—
Speaker 2:  ये section की बात नहीं कर रहा। मैं तो ये font की बात कर रहा हूँ। बस।
Speaker 1:  But आप ऐसे देखो ना। आप वो font देख रहे हो, but this font more or less looks like an heading। So थोड़ा उस तरीके से लग रहा है।
Speaker 1:  तो वो— मतलब, even जितना उनके पास information उस तरीके से— but honestly बोलता है कि मैं वो arc बना रहा होता तो मैं वो नहीं रखता। Headings तो रखता है explore companies में, but same repeat नहीं करता। 
Speaker 1: ठीक है।
Speaker 2:  दोनों करके एक बार देख लेना।
Speaker 1:  हाँ, करके देख लूँगा वो।
Speaker 2:  हाँ, पर हमारे वाले अभी ये वाले थोड़ा सा—
Speaker 1:  बड़ा हो जाता है। हल्का सा ज्यादा है।
Speaker 2:  But वो scale नहीं होगा। But याद रखना।
Speaker 1:  इसी वजह से हमारे जो दूसरे fonts हैं, inter, जो मैं use कर रहा हूँ, वही use होंगे।
Speaker 2:  समझ गया। ठीक है। और कोई points इसमें?
Speaker 2:  तो explore हमने break कर दिया। News and data labs companies।
Speaker 1:  News and companies।
Speaker 2:  And अब इसके अंदर क्या information रखी है, अलग से देखनी है। Font अभी के लिए हमने agree कर लिया। जो छोटे-मोटे nuances थे, हमने वो ऊपर का header के, वो हमने कर लिया।
Speaker 2:  Profile हम नीचे ला रहे हैं। और—
Speaker 1:  Watchlist also goes under।
Speaker 2:  Watchlist goes inside profile, not as a separate tab altogether।
Speaker 1:  ठीक है।
Speaker 2:  Whenever you do—
Speaker 1:  हाँ, ठीक है।
Speaker 2:  आप बोलो।
Speaker 1:  नहीं, I was about to say, whenever you design company page, make the search little more prominent।
Speaker 2:  Search तो वही रहेगा। अगर वो global search—
Speaker 1:  हाँ।
Speaker 2:  I was— then I realized।
Speaker 1:  ठीक है।
Speaker 2:  नहीं, हमारा वो वाला search वाला hierarchy वाला problem वापस आ गया। जो data labs में भी था। Global search versus company search, उसके अंदर।
Speaker 2:  पर ठीक है, यहाँ पे तो अभी global ही रहेगा। यहाँ पे company specific search के अंदर का search।
Speaker 1:  नहीं, इसका— when someone— अभी I'm not sure. I'm not able to visualize. But someone when opens company, can make the search even more prominent।
Speaker 2:  हाँ, but for some reason ना, मतलब, I think company— searching the company is a very strong behavior।
Speaker 1:  हाँ।
Speaker 2:  एक instinct आता ही है जब मैं देखता हूँ कि अच्छा, बहुत सारी कंपनियों में मेरे को वही देखना है।
Speaker 1:  हाँ, because paying—
Speaker 2:  चाहे वो specifically मुझे पता भी नहीं है कि उस company के अंदर मुझे exactly क्या data देखना है।
Speaker 1:  उसके लिए—
Speaker 2:  उसके लिए एक scenario जो मैं सोच रहा था, was— पर अब तुम्हारा bottom bar crowd होता जाएगा। Bottom bar message। If search is that important।
Speaker 1:  Bottom bar में? नहीं, इतना जरूरी नहीं है। Because इतना performance भी— there are performance gap।
Speaker 2:  उसके बाद।
Speaker 1:  उसके बाद।
Speaker 2:  No, let's go with the— it is global, but I'm not able to visualize।
Speaker 1:  नहीं, bottom bar में भी global ही है। It's still global। But once your search is fixed, then the search can be that prominent।
Speaker 1:  Because हाँ, search का use case तो आता है for companies, especially the second-tier companies।
Speaker 2:  हाँ, so can we add some more prominence when they especially land to company page?
Speaker 1:  तो अपने आप बढ़ जाएगा। जैसे profile section हटेगा ऊपर से। So then वहाँ पे बस streak and search बच जाएगा।
Speaker 2:  So prominence you can— having as a proper search bar versus a search icon।
Speaker 1:  बार में बना। But search bar होता नहीं है on desktop। मोबाइल में।
Speaker 2:  नहीं।
Speaker 1:  मुझे लगता है वो—
Speaker 2:  तो?
Speaker 1:  सोचो, मैंने आज तक search bar वैसे देखा है।
Speaker 1:  इन सबके जैसे ये है, इसमें इनका search यहाँ नीचे है। It means open the— इस type का page।
Speaker 2:  That's like opening a— tapping a search bar। It's a main search icon।
Speaker 1:  नहीं, वो तो bottom bar में है। जब— wait, that is what I mean by ये full page search वाला direction। Is when people do this।
Speaker 1:  इसमें भी medium also same thing। Search here।
Speaker 1:  And then you have वही। This is like the info to website में जो search है।
Speaker 2:  हाँ।
Speaker 1:  Exactly।
Speaker 2:  It opens up a new—
Speaker 1:  It opens—
Speaker 2:  It's not a page, but हाँ, अच्छा screen।
Speaker 1:  A screen। Like this। Not exactly this, but हाँ, this।
Speaker 1:  वही।
Speaker 2:  हाँ।
Speaker 1:  Behaviorally—
Speaker 2:  नहीं, but इसमें— हाँ, we need a lot of things। ये तो बहुत basic है।
Speaker 1:  हाँ, ये तो बहुत basic है। But हाँ, मतलब, that is what most of these kind of apps are doing। Invite decor।
Speaker 2:  वो क्यों? Primarily ये चीज़ नहीं।
Speaker 1:  Invite decor भी same है।
Speaker 1:  Bottom bar यहाँ। नहीं, sorry, इनका यहाँ पे।
Speaker 1:  नहीं, उद्देश्य— मतलब, मेरा point ही वही है। इसको— इसको थोड़ा इस तरीके से देखते हैं।
Speaker 1:  मतलब कि ये अभी नहीं change कर रहे। ये बाद में change करेंगे।
Speaker 1:  और जब इनका search improve हो जाएगा। अभी search में बहुत सारे issues हैं।
Speaker 2:  हाँ, but we'll make it prominent। Is what we will do। But we'll not keep as a global— I mean, as a separate dedicated page।
Speaker 1:  जैसे-जैसे, let's suppose, आप एक article की page ले ले। Sticker या किस तरीके से भी वो बना हुआ है। There is एक search behavior नहीं होगा।
Speaker 1:  You could थोड़ा search करके article कौन सा less है। But let's suppose, the moment आप एक company page पे पहुँच जाते हो, automatically the prominence of search increases।
Speaker 1:  क्योंकि लोग को चाहिए होता है search करने के लिए।
Speaker 2:  नहीं, article लोग नहीं search करेंगे। But if people are in the research zone, then yes, they will search for specific company या specific sector के around अगर कुछ ढूँढ रहे हैं।
Speaker 1:  हाँ, तो वही— वही वाली बात है कि अभी हम जो app का reference भी देख रहे हैं, पहले तो वो companies नहीं कर रहे। वो in general कर रहे हैं। तो obviously, in general, आपको एक—
Speaker 2:  Discovery built हो जाएगी।
Speaker 1:  कहीं ना कहीं ना तो आपको देना पड़ेगा कि okay, आप search कर लो। But there can be pages जो जिसमें तो भाई search behavior होगा। It cannot be कि आप वो सोचो कि वही एक icon से ही आप trigger करो search को।
Speaker 1:  तो वो थोड़ा सा वो है। मतलब, it cannot— हाँ।
Speaker 1:  क्योंकि जैसे simple सा है ना, अगर हम as a editor, मतलब, ये news apps को भी ना लेके हम Sugi भी पकड़ लें। जैसे let's suppose कि आप एक specific restaurant पे हो।
Speaker 1:  Restaurant के अंदर आप एक certain food item ढूँढ रहे हो। तो specific searches हैं अंदर।
Speaker 1:  कि अभी ये search कर सकते हैं।
Speaker 2:  Search for food search।
Speaker 1:  Just because कि list items हैं।
Speaker 2:  हाँ।
Speaker 1:  वो है।
Speaker 2:  I was just opening drive randomly यहाँ पे। I believe in there are— यहाँ पे।
Speaker 1:  Exactly, exactly।
Speaker 2:  Search in company labs।
Speaker 1:  हाँ, some kind of folders। 100 folders are there। जैसे Gmail में भी है।
Speaker 1:  अब आप search कर लो।
Speaker 2:  News में कम है।
Speaker 1:  नहीं, इसमें अगर— if I was just randomly opening Flipkart। इसमें भी उतना prominent है search। Search in minutes।
Speaker 2:  Flipkart में तो हो गई। E-commerce में तो हो गई। E-commerce में तो search।
Speaker 1:  नहीं, even let's say if it is—
Speaker 2:  But थोड़ा use case similar है। Finding something very specific। I want to— मेरे पास बहुत बड़ा एक वो है।
Speaker 1:  Funnel it out।
Speaker 2:  उसको करना है मेरे को। तो वही behavior वही है।
Speaker 1:  Exactly। E-commerce में तो वही है। E-commerce is always searchable।
Speaker 1:  अगर आप app use कर रहे हो Amazon की, तो Amazon में आप जाके कोई specific चीज़ ढूँढोगे। उसमें आप browse— feed नहीं browse करते।
Speaker 1:  Is very common.
Speaker 2:  If I open few others।
Speaker 1:  Blinkit is that balanced।
Speaker 2:  Blinkit में भी वैसे search है।
Speaker 1:  Search है, but हाँ, मतलब, उनका feed भी।
Speaker 2:  But interesting है कि कहाँ-कहाँ उनका search वो वाला है। एक सेकंड।
Speaker 1:  Blinkit में भी सबसे पहली चीज़ search ही है।
Speaker 2:  Search है। Zomato में भी सबसे पहले search।
Speaker 1:  पर हाँ, वो catalog नहीं है। क्योंकि उसमें तो लोग जो उसपे जा रहे हैं, they have a specific—
Speaker 2:  Intent to need for।
Speaker 1:  हाँ।
Speaker 2:  Some need।
Speaker 1:  बिल्कुल।
Speaker 2:  है। You cannot do। नहीं, एक मिनट।
Speaker 1:  In fact, WhatsApp में भी है। सबसे ऊपर search ही है। WhatsApp में भी।
Speaker 2:  हाँ।
Speaker 2:  Search है वैसे।
Speaker 1:  ठीक है। Anyways, और कोई points?
Speaker 2:  नहीं। I think। Unless until Satya has।
Speaker 1:  देखो, यहाँ पे ना, जैसे यहाँ पे भी main में search है। But यहाँ पे ये वाला search है। But वो intent यही है कि अब यहाँ पे वो intent change हो गया है।
Speaker 1:  When somebody is in—
Speaker 2:  तो ये तो browse mode में आ गया ना। Categories browse mode।
Speaker 1:  तो मैंने open— उसमें यहाँ पे देखते हैं कि lot of things at one place। अगर मेरे को specific search करना है, तो मैं वहाँ search नहीं करूँगा। तो वही वाली बात है।
Speaker 2:  So—
Speaker 1:  I think वो—
Speaker 2:  Prominence बढ़ाना है in the company section।
Speaker 1:  That's why रखना ही होता है।
Speaker 2:  हाँ।
Speaker 1:  अब वो क्या कह रहा था? कि मतलब कि अभी जब वो improve कर लेंगे।
Speaker 2:  Has a separate page for search।
Speaker 1:  Bottom bar।
Speaker 2:  Bottom something।
Speaker 1:  अगर उसमें हम उसमें performance और quality दे पाते।
Speaker 2:  Bottom bar मतलब ask।
Speaker 1:  नहीं, नहीं।
Speaker 2:  Actually, search could be combination of both। फिर वो अलग topic।
Speaker 1:  Literally the tab। अच्छा, वैसा।
Speaker 2:  ठीक है, वो separate कर।
Speaker 1:  See, assume this— this search bar to be नीचे।
Speaker 2:  मैं उसके लिए थोड़ा bounce नहीं करूँगा। मतलब, the make it global feels still। मतलब, वो थोड़ा lost हो जाएगा।
Speaker 1:  नहीं, globally तो है उसमें भी। उसमें भी globally है। जैसे इनका भी है।
Speaker 2:  मतलब, वो तो—
Speaker 1:  इनके पास ऐसे-ऐसे options थे, तो वो इसलिए उन्होंने ये डाला होगा। But हाँ, इनके में जैसे ये— search is like discover।
Speaker 2:  And some— like people are doing the same। But हाँ।
Speaker 1:  But वो अभी— अभी वो consideration नहीं है। वैसे भी अभी और चीज़ें भी हैं।
Speaker 2:  Different discussion for some other day।
Speaker 1:  क्योंकि ask भी एक consideration factor रहेगा। जो हमको combined search की एक time पे हमने बात की थी, वो भी एक possibility है। Ask वाले case में।
Speaker 2:  हाँ। If our exact search is not able to provide the results, it could fall back could be।
Speaker 1:  नहीं, नहीं, that's not a— that's a two-way thinking। उसमें last that we discussed— one idea that we discussed was combining the global search and ask। With default running as—
Speaker 2:  Ask?
Speaker 1:  Search।
Speaker 2:  Search?
Speaker 1:  With the fallback to ask।
Speaker 2:  हाँ, this is so—
Speaker 1:  But ask will also have its own entry point।
Speaker 2:  हाँ।
Speaker 1:  Then that becomes complicated।
Speaker 2:  ठीक है।
Speaker 1:  ठीक है।
Speaker 2:  We are finalizing on this. Whatever we just discussed। अभी explore page में can developer start?
Speaker 1:  कल कर सकता है।
Speaker 2:  कल कर सकता है ना। क्योंकि— at least if I— imagining from implementation point of view से।
Speaker 1:  ठीक है। Done?
Speaker 2:  हाँ।
Speaker 1:  ठीक है।
Speaker 1:  आइए एक बार information architecture एक बार अपना version एक बार share कर दो। I'll also review and edit or do whatever।
Speaker 2:  ठीक है। जैसे I've already shared you the document। एक बार you can go through and let me know।
Speaker 2:  But I'll re-share it again in case if that is missed।
Speaker 1:  एक मिनट।
Speaker 2:  एक— this is the data about— On basis which Satya has prepared the company card, the niche data। If it is recently funded, last round amount is what we are going to show। And इसका probability है 87%।
Speaker 2:  Of the data exists।
Speaker 1:  What is recent?
Speaker 2:  Recently funded।
Speaker 1:  By ranking by time?
Speaker 2:  हाँ, by time। And उसका amount— 87% of the case the value exists। Investor होगा।
Speaker 1:  Value exists या undisclosed you've excluded?
Speaker 2:  Values exist। Undisclosed is— undisclosed is not excluded। Not included in this।
Speaker 2:  There is 13% in this case might be undisclosed।
Speaker 1:  ठीक है। Undisclosed आते ही फिर वो—
Speaker 2:  हाँ, उसमें—
Speaker 1:  Does not count।
Speaker 2:  हाँ। See, the other 12% are real undisclosed deals।
Speaker 1:  पढ़ लिया।
Speaker 2:  हाँ, so just launch में जो भी है। So we have 85% or more prominence, which is why we are taking।
Speaker 1:  नहीं, नहीं, आप combine करके news वाले page का भी the sections that we are proposing। Same way company page का the sections that we are proposing। ये दोनों एक बार share कर दो।
Speaker 1:  Both we'll have to see। Tags हमारे हो गए।
Speaker 1:  Tags का भी इसमें add कर लो कि finally हमारे tags कौन-कौन से हैं या नहीं हैं। Onboarding में कौन-कौन से हैं।
Speaker 1:  Articles में कौन से हैं। Articles में अभी शायद कहीं-कहीं tertiary sector का tag आ रहा है, which should not happen।
Speaker 2:  हाँ, that is considered।
Speaker 1:  हाँ, तो वो tertiary नहीं आ सकता। It should stay on primary only।
Speaker 2:  हाँ, maximum secondary।
Speaker 1:  Primary only।
Speaker 2:  अच्छा, ठीक है। नहीं, ऊपर inside the articles।
Speaker 1:  ऊपर।
Speaker 2:  हाँ, ऊपर तो it's always be primary।
Speaker 1:  वो long वाले cases कैसे आ रहे हैं? Advanced hardware cannot be a primary। Or is it a primary?
Speaker 2:  हाँ। Because we are clubbed into— we clubbed hardware and few other thing to one ना। तो which is that is coming।
Speaker 1:  वो primary है। Advanced hardware primary।
Speaker 2:  नहीं, advanced hard— एक मिनट।
Speaker 1:  कोई तो बोल रहा था ना जो इस तरह का।
Speaker 2:  Hardware technology and—
Speaker 1:  कोई बोल रहा था वो। I think अक्षय बोल रहा था।
Speaker 2:  मैं नहीं बोल रहा। I was telling। Hardware technology।
Speaker 2:  Advanced hardware and technology and archives।
Speaker 1:  हाँ, that exists।
Speaker 2:  हाँ।
Speaker 1:  Media and entertainment is a long one and advanced hardware and technology is another long one।
Speaker 2:  हाँ।
Speaker 1:  This is— I think they are revamping this।
Speaker 2:  They?
Speaker 1:  Might revamp।
Speaker 2:  They— तो भाई, प्राप्ति?
Speaker 1:  प्राप्ति, प्राप्ति।
Speaker 2:  ठीक, ठीक है।
Speaker 1:  उसके MOP में point है ना वो? This one। Sector—
Speaker 2:  ठीक है।
Speaker 1:  Sector thesis। This one।
Speaker 2:  ठीक है।
Speaker 1:  Not revamping it, but updating it based on newer companies and things। जिसमें ये वाला sector तो definitely something that needs to be updated because a lot is happening here and in manufacturing।
Speaker 2:  A lot could be as a— individual standalone sections could also। हाँ, but ठीक है। तो वैसे वो already part of that, which is why it is coming up।
Speaker 1:  इसका फिर इनकी handling देखनी होगी। Then we have to watch cases। Media entertainment and advanced hardware and technology।
Speaker 1:  इनको कैसे handle कर रहे हैं। These are too long।
Speaker 1:  Way too long for showing it there।
Speaker 2:  इसका refresh action देख सकते हैं। I mean, just in app, if this is this, then show this। ऐसे कर सकते हैं अभी के लिए।
Speaker 2:  Which?
Speaker 1:  Hardware कर लो बस।
Speaker 2:  Hardware technology।
Speaker 1:  Maybe।
Speaker 2:  Hardware technology।
Speaker 1:  उसका एक— अभी के लिए naming convention अभी के लिए डाल दो। Then I'll also review and accordingly approve which one or if I can।
Speaker 2:  I'll give you two-three suggestions and you can freeze. Same, I'll try to— media and entertainment तो वैसे ही छोटा है। इसके ऊपर तो— but ठीक है।
Speaker 2:  We can keep it media। 
Speaker 2: ठीक है, I'll also come back with few variation। We can।
Speaker 1:  Enterprise services and media entertainment.
Speaker 2:  ये कहाँ है? Technology।
Speaker 1:  ये technology। मैं ऐसे ही बोल रहा हूँ।
Speaker 2:  अच्छा।
Speaker 1:  मैंने सोचा ये कहाँ है। दिख नहीं रहे मुझे।
Speaker 2:  ठीक है।
Speaker 1:  और कोई points?
Speaker 2:  नहीं, I'm good। But हाँ।
Speaker 1:  Explore कर रहा है। तुम्हारा pick। Explore is no longer explore।
Speaker 1:  News वाला page and the article। Article का implementation में अब क्या impact आएगा इसका?
Speaker 1:  कुछ नहीं।
Speaker 2:  नहीं, फिर—
Speaker 1:  Header तो change होगा ना हमारा main। और readability। एक और चीज़, मुझे app में भी readability में मजा नहीं आ रहा।
Speaker 2:  हाँ, क्योंकि गिल रहा है ना।
Speaker 1:  Article में और नहीं, spacing का भी कुछ issues है। Paragraph line— line— paragraph breaks में भी spacing is weird।
Speaker 2:  सही बात है।
Speaker 1:  ज्यादा spacing। And line height भी थोड़ी ज्यादा है। Line height भी ज्यादा है।
Speaker 1:  And paragraphs के बीच में भी spacing ज्यादा है।
Speaker 2:  हाँ, वैसे we need to revamp this page also now। ऐसे पूरा revamp करना है।
Speaker 1:  नहीं, मतलब इसमें— इसमें इतना नहीं लगेगा। इसमें तो hygiene हमें ensure करनी है। हाँ, ये रहा again advanced hardware।
Speaker 1:  Advanced hardware।
Speaker 1:  But हाँ। तो इसकी readability Android पे अलग है क्या?
Speaker 2:  नहीं, नहीं।
Speaker 1:  नहीं, नहीं, नहीं। मैं वही कह रहा हूँ कि मैंने—
Speaker 2:  मेरा design तो चेक करो।
Speaker 1:  मेरे ऊपर आया था।
Speaker 2:  Which— which article are you— have you opened?
Speaker 1:  Every article में यही है।
Speaker 2:  हाँ, यही है। इतना ही specific। I mean—
Speaker 1:  ये change करना है। Readability has to be—
Speaker 2:  हाँ।
Speaker 1:  And—
Speaker 2:  एक और—
Speaker 1:  ये एक और point था। Summary की size हमें change करना था।
Speaker 2:  That is taken care of। Summary size to be revamped। But हाँ, now how do we practically look at the timelines?
Speaker 2:  क्योंकि अब एक बार— again, I don't want to ask this question। आप एक बार—
Speaker 1:  Development time कितना है?
Speaker 2:  नहीं, इतना बड़ा नहीं होगा। Let's say if— if I give this article page। हो जाएगा कल।
Speaker 2:  वैसे basic तो बना है।
Speaker 1:  वैसे भी ये तो एक दिन में पूरा development सारा।
Speaker 2:  नहीं, नहीं, पूरा तो नहीं होगा। नहीं, जब— whenever page-wise page is getting ready, so is development also। By the time design is done, most likely to a certain extent, मुझे लग रहा है development भी हो जाएगा।
Speaker 1:  Brief को छोड़ के पहले सारे मेरे हिसाब से होंगे। वो सबसे पहले दे देते हैं। वो इसी order में— मतलब इसी style में extend होना है।
Speaker 1:  Information hierarchy is another dependency। उसके base पे ये I think lock हो सकता है।
Speaker 1:  तो brief को छोड़ के all other pages in order। Starting with news का home page, followed by companies का home page, followed by news article का individual page, followed by your profile।
Speaker 2:  नहीं, profile नहीं। Company detail page।
Speaker 1:  हाँ, company detail page।
Speaker 2:  Company explore page।
Speaker 1:  हाँ, ये दोनों। हाँ, and then finally brief।
Speaker 2:  Hmm.
Speaker 1:  That is the order।
Speaker 2:  हाँ। The way— again, फिर इसका पूरा event— event properties।
Speaker 1:  वो क्यों change होगा? Functionality तो same है। Oh, some pages— some events will, yes.
Speaker 1:  Update।
Speaker 2:  हो जाएगा। मेरा skill तो बन गया वैसे। So it should not be this complicated the way it happened last time।
Speaker 2:  But coming back— ऐसे।
Speaker 1:  The same— company event exists। The same articles वाला event exists।
Speaker 2:  नहीं, right now there are a lot of new things which have been introduced। अब inside news— inside news will have major tabs। Or there are some।
Speaker 1:  तो पहले थे। They existed earlier also। Try to inherit the existing events।
Speaker 2:  हाँ, now for example अभी story एक आ गया। That is new। We cannot use brief card।
Speaker 1:  Story— story is overall new thing। Story का तो मुझे information hierarchy point of view से चाहिए। If you are showing sectors in that tab, then वापस ऊपर story नहीं आ सकता।
Speaker 2:  हाँ, दोनों नहीं। दोनों exist नहीं कर सकते। अब कैसे करता है?
Speaker 2:  ऊपर sectors—
Speaker 1:  यहाँ पे sectors अगर आ गए, तो यहाँ पे भी sector नहीं आ सकता।
Speaker 2:  हाँ, मेरा ऐसे report भी।
Speaker 1:  हाँ, हाँ, वो तो— that's the common sense।
Speaker 2:  तो hierarchy में ये एक बहुत important question है। क्योंकि यहाँ— this is just brief का stories। This is actually a field।
Speaker 2:  Both are actually very different things।
Speaker 1:  हाँ। So whenever I've just got the result as I speak, तो people are using for filter section। They are using more development tabs।
Speaker 1:  So ऊपर sector करते हैं, नीचे tags करते हैं। That is essentially what we have designed।
Speaker 2:  Sort of, yes।
Speaker 1:  नहीं, that is what exactly it is in the article page। ठीक है, I think that brings us to a certain conclusion। हाँ, coming back, you were saying।
Speaker 1:  I'll share the— I'll first I'll share the draft with you for hierarchy में। क्योंकि my designs direction हमारा बन चुका है।
Speaker 1:  इसमें जो refinements होने हैं, वो explore article page, news— news page, home page पे। Article page भी अभी शुरू है या तुम पहले companies ही करोगे?
Speaker 2:  Companies कर लेते हैं।
Speaker 1:  ठीक। Main फिर वही। 
Speaker 1: ठीक है। Timeline क्या लग रही है तुम्हें?
Speaker 2:  It's a good company।
Speaker 1:  कितनी चीज़ें? Company है, उसके बाद company।
Speaker 2:  News home page, news—
Speaker 1:  Company profile page पे थोड़ा time लग सकता है मेरे को। क्योंकि उसमें बहुत सारी चीज़ें हैं। Sectional चीज़ें बहुत सारी हैं।
Speaker 1:  यहाँ पे तो card repetition है। वहाँ पे तो सारे— कंपनी, हाँ, थोड़ा time लग सकता है उसमें।
Speaker 1:  Company page पे।
Speaker 2:  ये तो company profile पे अभी इतना time नहीं spend करेंगे। UI updation करेंगे बस। UX अभी ना छेड़ें।
Speaker 2:  इस round में। V3 में pick करो।
Speaker 2:  एक option बोल। अभी UI updation— यहाँ पे UX थोड़ा change हो रहा है हमारा।
Speaker 2:  Company— ये वाला जो भी page है इसका, companies का home page। Company profile page पे इतना ना changes करें।
Speaker 2:  Information में changes करें, yes। Information hierarchy में यहाँ पे cards पे।
Speaker 2:  Card style and card— information hierarchy card के अंदर। That is fine.
Speaker 2:  Company profile page में बस UI update based on जो अभी ये नई design language आई है, बस वो करें। उसका UX अभी मत छेड़ो।
Speaker 2:  उसपे next iteration में आएंगे। Next version में।
Speaker 2:  क्योंकि वो— वो page छेड़ा तो फिर वो अपने आप में कहानी है। वो अभी नहीं छेड़ते।
Speaker 2:  So then our scope उसमें थोड़ा कम हो जाएगा हमारा। उसी में सबसे ज्यादा time लगेगा।
Speaker 2:  और फिर brief पे आना पड़ेगा। Brief को iteration में देखनी पड़ेगी।
Speaker 2:  उसमें थोड़ा time लगेगा।
Speaker 1:  Even अगर company page में अगर हम UI भी exact बिठा रहे, तो उसमें भी एक तरीके से लगेगा ना।
Speaker 2:  Company home page?
Speaker 1:  या company profile page?
Speaker 2:  Profile page।
Speaker 1:  अभी—
Speaker 2:  अब एक और चीज़ कर सकते हैं क्या? उत्कर्ष।
Speaker 1:  क्या follow करते हो? क्या याद है?
Speaker 2:  नहीं, अभी एक immediate thought है। We'll go with whatever page जो अभी है, we'll go। But can we make it as a web page?
Speaker 2:  Can we render it as a web page? Any development that we do, it can— it doesn't require any app update।
Speaker 1:  Web page नहीं। Web page has a lot of other challenges।
Speaker 2:  नहीं, it doesn't look like a web page। When you open ET, there are few pages that are web page, but it doesn't look like a web page।
Speaker 1:  पर वो native interaction नहीं मिलेगा ना तुम्हें?
Speaker 2:  नहीं, नहीं। Functionality probably Rithvik can say it better। मुझे ऐसा लग रहा है, at least he has shown few sample।
Speaker 2:  मुझे इतना— I don't feel this much of— ये इसका web view है।
Speaker 1:  ETA?
Speaker 2:  हाँ।
Speaker 1:  As a section?
Speaker 2:  हाँ।
Speaker 1:  तो ऐसे करते हैं फिर।
Speaker 2:  क्या होगा?
Speaker 1:  हाँ।
Speaker 2:  ठीक है। But can we think in that?
Speaker 1:  उससे क्या फायदा होगा? What does that help in?
Speaker 2:  It will help in— right now we can go with existing design।
Speaker 1:  And then change it।
Speaker 2:  Change it later without any app update। क्योंकि वैसे it becomes— अगर if for quick confirmation, I can call Rithvik।
Speaker 1:  तुम्हें देख लेना। UI update कितना है?
Speaker 2:  मेरे according to, हाँ। On 20 दिख रहा है। मुझे लग रहा है बहुत ज्यादा— बहुत ज्यादा होगा।
Speaker 1:  वो भी just कि— मतलब ना, देखो, letter font change कर दिया, नहीं work करेगा। मैं बस इतना कह रहा हूँ। थोड़ा आपको ऐसा दिखना पड़ेगा।
Speaker 2:  ऐसा re—
Speaker 1:  एक certain corner radius है, एक certain spacing है, वो थोड़ा work करता है।
Speaker 2:  थोड़ा तो लगेगा।
Speaker 1:  मतलब उसमें भी ऐसा है कि मतलब कि once एक चीज़ ऐसे figure out हो गया, तो हाँ, ये तो ऐसा-ऐसा होगा। फिर वो बन जाएगा। बस वही चीज़ है।
Speaker 2:  Which is why I'm just— can I call Rithvik just to get some time?
Speaker 1:  अभी?
Speaker 2:  हाँ, है।
Speaker 1:  इसलिए।
Speaker 2:  Timeline?
Speaker 1:  अभी तक एक बार आया है।
Speaker 2:  Development का shadow is— क्योंकि मुझे अभी इतने changes के साथ— तो हमें अभी— आज क्या है? Monday है ना। कितना time लगेगा?
Speaker 1:  आप बताओ।
Speaker 2:  हाँ। So Rithvik, the context of this discussion is, we are revamping the— okay, explore page is no more explore. We are having brief page, news, companies profile।
Speaker 2:  और for you। That is how the page is going to look like।
Speaker 1:  Four tabs।
Speaker 2:  Four— four different tabs is what we are going to have।
Speaker 1:  Okay. मतलब companies को explore से break out करके अलग tab ही दे दिया। And articles ही अब है तो explore page रहेगा, essentially।
Speaker 2:  ठीक है। And हमारा home है brief।
Speaker 1:  हाँ।
Speaker 2:  That still remains brief।
Speaker 1:  कुछ change नहीं हुआ।
Speaker 2:  हाँ। Now with that being said, अभी there are a lot of pages where every page almost has a redesign। कुछ-कुछ change हो रहा है।
Speaker 2:  While we are discussing this, we conclude that जो company page हमारा है, it becomes a longer— it could be a bigger change. Because right now it's look very basic।
Speaker 2:  So what— what my proposal was, can we make it a web version of it so that we can make a dynamic changes?
Speaker 1:  Well, that functionality— heavy driven— that heavy functionality can't be used in web view. From engineering point of view, if I'm to say, from tomorrow, like— so the initial is web view.
Speaker 2:  हाँ।
Speaker 1:  Right? Then you need to click on it, have some interactions. That would be entirely done on web.
Speaker 1:  Not on a lab— no app collection would be there।
Speaker 2:  नहीं, जैसे तुमने ये बोला ना, ET को AI।
Speaker 1:  So what does ET— what ET does is, it basically opens some features in that web view।
Speaker 2:  हाँ, let's say तुमने A बोला। For example, this is ETA।
Speaker 1:  ETA is web view। But this is—
Speaker 2:  This is for example।
Speaker 1:  But आप उसके interactions देखोगे ना, तो बहुत limiting सा page होगा ये। बस।
Speaker 2:  हाँ, वैसे हमारा—
Speaker 1:  हमारा पूरा page inerted page है। उसमें watchlist, ये सब। बहुत सारे features हैं।
Speaker 2:  नहीं, नहीं, I'm not— I'm talking about company detail page।
Speaker 1:  Company detail page?
Speaker 2:  I'm not talking about company listical page। I'm talking about the detail page which is this।
Speaker 1:  Individual company profile page?
Speaker 2:  हाँ, I'm talking about this particular page। Where we already have limited information। Obviously ये तो है, but हाँ।
Speaker 1:  We can consider this। मतलब हमारा agenda क्या solve हो रहा है? Time बच रहा है, इसलिए हम वो कर रहे हैं।
Speaker 2:  हाँ, time बच रहा है क्योंकि और बहुत सारा variation होगा। बहुत सारा चीज़—
Speaker 1:  Time बच रहा है in the sense कि वो बोल रहा है अभी existing वाले को web view में convert कर दिया। And फिर meanwhile वो अलग से changes कर लिए। पर हमारा app का timeline फिर बच गया design का।
Speaker 1:  अभी उसको छोड़िए।
Speaker 2:  वैसे, हाँ, the उत्कर्ष point was, this— this is not going to be one small change। It's like major revamp हो सकता है when we initiate this discussion।
Speaker 1:  UI point of view।
Speaker 2:  हाँ, UI point of view से। So in order to optimize that, that is where this discussion is came up। तो अगर whatever—
Speaker 1:  मतलब लगभग उसकी interactions check करनी पड़ेंगी जो उसकी company page पे already हैं। Company page पे हम web में अगर कुछ extra कर रहे होंगे ना, तो हमें app में— जैसे अगर web में हम export कर रहे हैं, या web में हम—
Speaker 2:  नहीं, वो तो नहीं करेंगे।
Speaker 1:  तो वही तो, वो हमें limit करना पड़ेगा ना कि if hosted from this app, then don't show this button। Web की further redirection है, वो हमें—
Speaker 2:  नहीं, वो तो फिर development में थोड़ा ज्यादा होगा, but design में थोड़ा कम होगा अभी। I mean, in terms of to start with।
Speaker 1:  दोनों तरफ वापस rebalance करके।
Speaker 2:  I'm just trying to understand।
Speaker 1:  I'm not agreeing कि हमें एक पूरा feature— मतलब क्योंकि ये एक ही detail page है। इसमें I can— मतलब if there is a timeline crunch, I can provide some extras। But हमें करना तरीके से ही चाहिए।
Speaker 1:  एक ही बार ही होना चाहिए। मतलब अगर कोई बहुत ही बढ़िया problem solve हो रही होती, तो हम कर भी लेते।
Speaker 1:  But इसमें हमको उसमें भी पूरा check करना पड़ेगा। Data lab existing platform पे checks लगाने पड़ेंगे।
Speaker 1:  What I'm seeing is anyways, अगर यहाँ design में time बच गया, तो वो development में बढ़ते जाएगा।
Speaker 2:  हाँ, वैसे।
Speaker 1:  शुरुआत वही है।
Speaker 2:  हाँ।
Speaker 1:  और फिर हमारी app—
Speaker 2:  और फिर हमारी app की aesthetics पूरी orange है। वहाँ से वो red आएगा, वो भी बिल्कुल stitched experience लगेगा, patchy लगेगा।
Speaker 1:  हाँ।
Speaker 2:  नहीं, existing— this existing version cannot be converted to web। वो तो एक—
Speaker 1:  नहीं, but what I'm saying is— what I'm saying is, can we have a new web version only for this?
Speaker 2:  उस problem का solve। वो भी तो बना रहे हैं।
Speaker 1:  नहीं, नहीं, वो— what I'm— नहीं, what you're trying to—
Speaker 2:  What I'm saying is that maybe that also adds to depth।
Speaker 1:  Basically, अगर हम ये problem solve कर रहे होते कि app में बनाने में बहुत time लगेगा, हमारे पास iOS की अलग टीम, Android की अलग टीम, तो हमने web view लगा दिया। क्योंकि ET में ये होता है, Android की अलग टीम है, iOS की अलग टीम है। और वो basically लगाते हैं starting में, कि check करने के लिए कि app में उसपे clicks आ भी रहे हैं या नहीं आ रहे, या फिर—
Speaker 2:  फिर उसको convert करेंगे।
Speaker 1:  और वो basically उन चीज़ों के लिए भी लगाते हैं। आज ये slot ETAI का है, कल को ये ETAI Bytes का होगा, यही same slot। तो उनके वो feature lab-based होते हैं वो।
Speaker 2:  पूरा web page।
Speaker 1:  ठीक है।
Speaker 2:  फिर तो नहीं।
Speaker 1:  मेरे हिसाब से web view तो—
Speaker 2:  Avoid करो फिर।
Speaker 1:  ठीक है।
Speaker 2:  हाँ, फिर तो अभी skip the web view part।
Speaker 1:  ठीक है।
Speaker 2:  हाँ।
Speaker 1:  Comment हो सकती है।
Speaker 2:  सी, ideal timeline तो हमारी original timeline तो ये थी कि हम Thursday को dev start कर लें। और sequentially भी अगर कर रहे हैं, तो launch timeline— जो marketing launch timeline है, वो अभी हमने 15 ली थी।
Speaker 1:  15, हाँ।
Speaker 2:  Which is one week from now। Eight days from now।
Speaker 1:  15 ली थी। तो dev time कितना है उससे attracted to design time?
Speaker 2:  फिर approval time।
Speaker 1:  हाँ।
Speaker 2:  दो दिन?
Speaker 1:  दो दिन में सारा हो जाएगा?
Speaker 2:  I'll try push करूँगा और क्या करूँगा।
Speaker 1:  ठीक है।
Speaker 2:  खुशी कर रहे हैं अपने सैटे को निकालने के लिए।
Speaker 1:  दो दिन मतलब 8th and 9th। 9th EOD तक या 10th तक?
Speaker 2:  आज कितना है?
Speaker 1:  7th।
Speaker 2:  7th।
Speaker 1:  हाँ।
Speaker 2:  9th EOD तक।
Speaker 1:  9th EOD।
Speaker 2:  9th EOD।
Speaker 1:  ठीक। Let's push।
Speaker 2:  हाँ।
Speaker 1:  You're included company pages is what I'm assuming।
Speaker 2:  हाँ, हाँ।
Speaker 1:  Article detailing बदलेगा।
Speaker 2:  हाँ।
Speaker 1:  सारे pages बदलेंगे। UI change हो रहा है। मतलब नया font change हो रहा है।
Speaker 1:  Font and colors change हो रहे हैं।
Speaker 2:  हम target ये करते हैं कि dev completion।
Speaker 1:  तो—
Speaker 2:  15th को marketing launch है।
Speaker 1:  नहीं, वैसे— when I talk about news page right now, तो वैसे design finalized है, but it's just the font and कुछ basic चीज़ finalized है, which you can start picking up।
Speaker 2:  बस 15th वाला हमारी completion— अगर 14th तक design हो जाए, मैं इस दिन एक दिन तो test करना चाहूँगा, इतनी देर से development—
Speaker 1:  नहीं, वो तो बोल रहे हैं ना, दो दिन में हो जाएगा।
Speaker 2:  नहीं, जब भी होए, बस एक दिन मेरे को testing के लिए चाहिए होगा, और मैं कुछ नहीं मांग रहा।
Speaker 1:  Dev की बात नहीं है।
Speaker 2:  हाँ, हाँ।
Speaker 1:  Dev की बात नहीं है।
Speaker 2:  Dev की— dev completion के बाद मेरे को एक दिन test के लिए चाहिए होगा, जिसमें मेरे को कोई issues मिले।
Speaker 1:  किसी के submission timeline factor in किए?
Speaker 2:  हाँ?
Speaker 1:  Submission—
Speaker 2:  हाँ, जैसे मैंने बोला ना, approval time।
Speaker 1:  24 to 48 hours।
Speaker 2:  वो भी additional।
Speaker 1:  See, I'm not too much bothered about Play Store। I'm least bothered about Play Store right now।
Speaker 2:  App Store is okay।
Speaker 1:  हाँ। App— Play Store में तो हम 3-4 घंटे में आ जाता है।
Speaker 2:  ठीक है।
Speaker 1:  But still, that is not bad।
Speaker 2:  अगर brief page में कोई content नहीं है, मतलब content change तो नहीं हो रहा।
Speaker 1:  Brief page पे तो अभी पहुँचेंगे ही।
Speaker 2:  पहुँचेंगे।
Speaker 1:  Brief page पे तो अभी छुआ ही नहीं है। अभी आखिरी में brief page का design होगा।
Speaker 2:  बस अगर ये हुआ ना कि उसमें backend related भी मेरे को dependencies जो भी आ सकती हैं, तो—
Speaker 1:  हाँ, बहुत आ जाएगा।
Speaker 2:  Brief में आएंगी। Brief में definitely आएगी।
Speaker 1:  नहीं, नहीं, company page में आएगा।
Speaker 2:  हाँ, सब में।
Speaker 1:  क्योंकि we have different data for different sections।
Speaker 2:  Development ना वो हो जाएगी कि मतलब process size हो जाएगी, कि मेरे को पहले process बुक करवानी पड़ेगी, then only I can move। उस contract पर I can move forward।
Speaker 1:  नहीं, Anmol को bandwidth है वैसे। He is working on even—
Speaker 2:  जो भी bandwidth वो लेगा, उस time तक तो मैं उस चीज़ पे—
Speaker 1:  हाँ, he will be blocked।
Speaker 2:  Sequential हो जाएगा।
Speaker 1:  Sequential हो जाएगा।
Speaker 2:  Sequential हो जाएगा। Parallelize नहीं हो पाएगा।
Speaker 1:  वो फिर— मैं तो कहूँगा कि अगर feed भी layout में design है ना, तो Anmol को कल से बनाना मतलब चालू कर लेते हैं, ताकि—
Speaker 2:  He is working on even formal piece।
Speaker 1:  वो एक-दो API I can try कि वो थोड़ा करवा दें।
Speaker 2:  ठीक है। So अभी just to summarize, 9th EOD is the design का timeline जो अभी aim कर रहे हैं। And launch— marketing launch is 15th।
Speaker 2:  Approval timeline अगर app store का भी ले रहे हैं, तो then the submission has to happen on Sunday को तो वो review करेंगे नहीं। Saturday को भी वो review करते हैं?
Speaker 2:  या Friday को—
Speaker 1:  Friday नहीं करते। करते हैं। They do।
Speaker 2:  Friday?
Speaker 1:  We got— we got one of our rejection on Saturday, so I'm assuming they are working.
Speaker 2:  Friday EOD या Saturday morning is when we will have to do the submission। So everything is to two days, essentially।
Speaker 1:  नहीं तो डेली एक दिन की हो जाएगी। मेरे को testing चाहिए होगी एक दिन की तो। 9th, 10th, 11th।
Speaker 2:  नहीं, sequential नहीं होगा ना। कल— 8th को— कल तुम्हें दो-तीन designs मिल जाएंगे। तो 9th को तुम वो pick कर सकते हो।
Speaker 2:  तो तुम्हारा 10th को तुम्हारा start नहीं हो रहा, तुम्हारा तो कल से ही start हो जाएगा। कल EOD से या कल EOD से तुम्हारा start हो जाएगा sequence।
Speaker 1:  कल first half में वैसे हो सकता है, at least for article page।
Speaker 2:  मैं अभी कर देता हूँ।
Speaker 1:  नहीं, नहीं, नहीं। अरे।
Speaker 2:  अभी कर लो।
Speaker 1:  अरे यार, अब structurally तो sorted है ना सब कुछ।
Speaker 2:  ठीक है। तो मैं इस दिन submission दे दूँगा।
Speaker 1:  ताकि 14th तक हमारे पास approval आ जाए।
Speaker 2:  11th को dev completion है। मतलब—
Speaker 1:  तो इसको बस छोटे-मोटे changes push करेंगे। 11th, 12th को— रंजीत, आपकी भी bandwidth चाहिए होगी मुझे testing के लिए। मतलब testing में आज वो नहीं कर पाऊँगा अकेला सब कुछ।
Speaker 2:  हाँ।
Speaker 1:  Android और iOS दोनों हैं।
Speaker 2:  हाँ, हो जाएगा।
Speaker 1:  That's it।
Speaker 2:  ठीक है।
Speaker 1:  चलते हैं।
Speaker 2:  Thank you।
