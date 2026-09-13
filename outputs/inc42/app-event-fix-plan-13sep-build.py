import html
N=15
S=[]
def title(t): S.append(('title',[t]))
def sec(t): S.append(('sec',[t]))
def hdr(*c): S.append(('hdr',list(c)))
def row(*c): S.append(('row',list(c)))
def blank(): S.append(('blank',[]))
Y='✓'; X='✗'

title('App Event Fix Plan (13 Sep 2026)')
row('What this is','The full plan to fix app event tracking for the new design: what to fix, what to add, which properties, which person properties, and where each event is sent.')
row('Where to change','The INC42 app (Android and iOS), in the code that sends events to PostHog and Customer.io.')
row('Checked against','Live PostHog, Inc42 App project, 13 Sep 2026, last 30 days unless stated. Customer.io figures from the 12 Sep full audit.')
row('How to read the spec','One row per event. "Event properties" lists each field as  name : what it holds : allowed values : required or not. ADD = new field, FIX = field exists but is wrong, KEEP = no change.')
blank()

sec('1. What we agreed')
hdr('#','Decision','What it means for tracking')
row('1','Fix existing events first, then add new events','Step 1 below is fixes only. New events start at Step 2.')
row('2','Bottom nav is Brief / Article / Company. There is no Explore screen.','explore_viewed is retired. The word "explore" is removed from every source value.')
row('3','One view event for the Article page and one for the Company page. The tab is a field.','article_home_viewed and company_home_viewed. Switching tabs fires the same event with a new tab value.')
row('4','The landing page of Article and Company has many sections, like Explore had','New event section_viewed, with page_type = article_home or company_home.')
row('5','We need to know which card was seen, and whether it was in the Brief or on the Article page','card_viewed gets source_type (brief, article_home, company_home). Story open is tracked with the same field.')
blank()

sec('2. What live PostHog shows today (the facts this plan is built on)')
hdr('#','Fact','Number','Why it matters')
row('1','card_viewed only fires inside the Brief today','16,621 of 16,697 events are in sessions where a brief was opened. Highest position is 9.','Once Article and Company cards also fire card_viewed, every Brief card chart must filter to source_type = brief, or its numbers jump.')
row('2','card_viewed has no edition_date and card_type is always "story"','edition_date on 0 events. card_type = story on all 16,697.','Brief drop-off per edition cannot be measured today.')
row('3','explore_viewed already records a tab, but the live tab names differ from Figma','Articles: latest 4,819 · deals 344 · financials 163 · startup_stories 97 · in-depth 88 · trends 71 · news 23. Companies: all 2,673 · recently_funded 542 · just_launched 187 · ipo_bound 129 · early_fundraisers 99 · soonicorns 99 · unicorns 88 · watchlist 48 · profitable_startups 8.','Figma shows News, In-Depth, Markets, Financials, Startups, D2C, Newsletter and All, Recently funded, Just launched, Early rounds, Profitable, Unicorns, Sectors. The final list must come from the build.')
row('4','"explore" is used as a source value in five events','article_opened 1,126 · brief_page_opened 665 · company_profile_viewed 606 · sector_landing_viewed 90 · story_saved 68','All five must switch to article_home or company_home in the same release.')
row('5','No event carries a theme; is_registered is already on every event','theme on 0 of 91,138 events. is_registered on 91,138 of 91,138.','Add theme. Do not add a separate auth_state field, it would repeat is_registered.')
row('6','push_opened does not exist','0 events','Opens from notifications cannot be counted.')
row('7','Person properties are not being saved for many users','watchlist_count on 59 of 119 people who added to watchlist (90 days). push_types_enabled on 7 of 827 people who allowed push (90 days).','Any new person property will hit the same problem until this is fixed.')
row('8','Most people are on old app versions','People who opened the app in the last 7 days: 1.0.0 = 393 · 1.0.1 = 244 · 1.0.2 = 23','New events reach only people who update. Old events keep arriving from old versions for weeks.')
row('9','Customer.io receives many events that are not on its approved list','card_viewed, explore_viewed, brief_page_opened, profile_section_viewed, scroll_depth each 3,000+ in 30 days (12 Sep audit). 76% of Customer.io volume is not approved.','If forwarding is "send everything", every new event in this plan will also flood Customer.io.')
row('10','watchlist_viewed tab is mostly empty','entity_tab empty on 1,512 of 2,118 events (71%)','Watchlist tab usage cannot be split.')
row('11','Some planned events have never fired','rating_prompt_shown 0 · share_initiated 0 · decode 0','Build them under the existing names. Do not invent new names for the same thing.')
blank()

sec('3. Where each event is sent')
hdr('Destination','Send when','From this plan')
row('PostHog','Always. Every event in this plan.','All rows')
row('Customer.io','Only if a message, campaign or segment uses it','push_opened, notification_settings_changed, watchlist_entity_added / _removed (already approved). None of the new view, section, card, drawer, filter or state events.')
row('Firebase','Only install and conversion events used for ads and store reporting','None')
row('Singular / SKAN','Only the agreed conversion steps','None')
row('Before Step 2 ships','Change Customer.io forwarding from "send everything" to an approved list','Otherwise every new event below reaches Customer.io automatically (see fact 9)')
blank()

sec('4. Event spec')
hdr('Step','Change','Event','Fires when','Event property groups','Event properties (name : holds : allowed values : required)','Person property to update','Identify call','PostHog','Customer.io','Firebase','Singular / SKAN','What it answers','Done when (test)','Notes and nuances')

S.append(('sub',['STEP 1: FIX EVENTS THAT ALREADY EXIST']))
row('1','Fix','card_viewed','A card becomes visible. Today: Brief cards only.','Super + Story',
'ADD source_type : where the card is : brief (Step 1). article_home, company_home added in Step 2 : required\nADD edition_date : date of the edition : e.g. 2026-09-13 : required when source_type = brief\nFIX card_type : kind of card : story | company | stock | sector | edition : required\nKEEP position : number, 1 = first card : required\nKEEP story_id : required for story cards\nKEEP is_boosted, boost_reason : Brief only',
'None','No',Y,X+' stop (arrives today, not approved)',X,X,'Brief card drop-off per edition','On a test phone, every card_viewed from the new build shows source_type = brief and an edition_date',
'Old events have no source_type. Brief charts should filter "source_type = brief OR source_type is not set" so history is kept.')
row('1','Fix','brief_page_opened','Brief page shown, or the edition day is switched','Super',
'FIX is_edition_switch : was the day switched : true | false : required (on 1,025 of 10,620 today)\nFIX source : where the user came from : organic | push | deeplink | watchlist | article_home | company_home | profile | streak : required\nKEEP edition_date, is_today',
'None','No',Y,X+' stop',X,X,'Which past days are opened; where Brief visits come from','Switch day on a test phone: one event, is_edition_switch = true, edition_date = the picked day',
'Live source has "explore" 665 (replace), "brief" 1,508 and "tab" 9. Ask the developer what "brief" and "tab" mean before mapping them.')
row('1','Fix','article_opened','Full article reading screen opens','Super + Story',
'FIX source : brief_card | article_home | company_home | article_reader | company_profile | sector_page | watchlist | search | push | deeplink : required ("explore" 1,126 today)\nADD source_section : section the story was in : e.g. top_stories : required when source is article_home or company_home\nADD source_tab : tab the user was on : required when source is article_home or company_home\nKEEP story_id, position',
'None','No',Y,X+' stop (2,779 arrive today, not approved)',X,X,'Which surface and which section drive reading','Open a story from Article home on a test phone: source = article_home with section and tab filled',
'See open decision 1: story_opened may be the same tap as this event.')
row('1','Fix','company_profile_viewed','A company profile opens','Super',
'FIX source : company_home | article_home | article_reader | sector_page | directory | search | watchlist | stock_watch : required ("explore" 606; "companies" 50 and "companies_directory" 13 mean the same place, merge into directory)\nFIX company_name : always send (on 329 of 4,538 profile_section_viewed events only)\nKEEP company_id, is_tracked',
'None','No',Y,X,X,X,'Where company profile visits come from','Open a profile from Directory and from Stock Watch: source = directory / stock_watch','company_id must be the same ID Stock Watch uses.')
row('1','Fix','sector_landing_viewed','A sector page opens','Super','FIX source : article_home | company_home | card_tag | article_reader | watchlist : required ("explore" 90 and "unknown" 20 today)\nKEEP sector, sub_tab','None','No',Y,X,X,X,'Where sector visits come from','No event with source = unknown or explore from the new build','Find which entry point sends "unknown".')
row('1','Fix','story_saved / story_unsaved','User saves or unsaves a story','Super + Story','FIX source : same list as article_opened ("explore" 68 today)\nKEEP story_id, position','None','No',Y,Y+' approved (story_unsaved loses 47.8% today)',X,X,'Where saves happen','Save from Article home: source = article_home','')
row('1','Fix','story_shared','Share completed on a story','Super + Story','FIX source : one value for the reading screen: article_reader ("article" 1 and "article_reader" 150 today)\nFIX channel : whatsapp | linkedin | x | email | copy_link | other : required (wrong today per App - Events tab)','None','No',Y,X,X,X,'Which stories get shared and where','Share to WhatsApp on a test phone: channel = whatsapp','Replaced by entity_shared in Step 4. Send both until old versions fade.')
row('1','Fix','profile_section_viewed','A section on a company profile comes into view','Super','FIX section : add overview | investments | acquisitions to today\'s funding | financial_overview | key_people | corporate_activity | recent_activity : required\nFIX company_name : always send\nKEEP company_id','None','No',Y,X+' stop (3,000+ arrive today)',X,X,'Which profile sections are read','Tap each of the 5 profile tabs: one event each with the right section','')
row('1','Fix','watchlist_viewed','Watchlist tab shown or its tab switched','Super','FIX entity_tab : articles | companies | sectors : required (empty on 71% today; rename "industry" to "sector" to match watchlist_entity_added)\nKEEP sub_tab, tracked_count','None','No',Y,X+' stop',X,X,'Which watchlist tab is used','Open each of the 3 tabs: entity_tab filled every time','')
row('1','Fix','search_initiated','Search box tapped','Super','FIX surface : brief_header | article_home | company_home | directory : required (only "explore" today, 421 of 421)\nKEEP search_scope','None','No',Y,X,X,X,'Where people start searching','Tap search on each of the 4 screens: correct surface','')
row('1','Fix','notification_settings_changed','Any push setting changed','Super','FIX setting : master | daily_brief | watchlist_alerts | delivery_time : required\nFIX new_value : true | false, or a time like 07:00 for delivery_time : required','push_opt_in (for master)\npush_types_enabled (list of switched-on types)','Yes, person update',Y,Y+' approved (44.3% lost today)',X,X,'Who turns push off, and at what time people want the brief','Turn master off on a test phone: event arrives in PostHog and Customer.io; person shows push_opt_in = false','push_types_enabled is saved for 7 of 827 people who allowed push. Fix the person update, including for signed-out users.')
row('1','Fix','watchlist_entity_added / _removed','Company or sector added or removed','Super','KEEP entity_type, entity_id, entity_name, watchlist_size_before\nFIX entity_name : also send on sector add (empty today per App - Events tab)','watchlist_count\ntracked_sector_count','Yes, person update',Y,Y+' approved',X,Y+' (added only, already agreed)','Watchlist size for digest eligibility','Add a company on a test phone: person watchlist_count goes up by 1 in PostHog and Customer.io','watchlist_count is saved for 59 of 119 people who added (90 days).')
row('1','Build','push_opened','User taps a push notification, with the app closed, in background or open','Super','push_type : morning_brief | watchlist_digest | breaking | nudge | winback : required\nmessage_id : Customer.io delivery ID : required\ndestination_screen : screen the push opens : required\napp_state : killed | background | foreground : required','None','No',Y,Y+' approved',X,X,'How many opens come from push, per push type','Send a test push, app fully closed, on Android and iOS: exactly one push_opened, and app_opened shows source = push','0 events today. Timing with app_opened is set in attribution/03-implementation-handoff.md. Test on Xiaomi / Oppo / Vivo, which kill background apps.')

S.append(('sub',['STEP 2: ARTICLE AND COMPANY PAGES, SECTIONS, STORIES, CARDS']))
row('2','New','article_home_viewed','Article page becomes visible: nav bar tap, tab tap, Back from an article, app reopened on this page, or a deep link','Super',
'tab : fixed code of the tab, not the label : final list from the build (Figma: news | in_depth | markets | financials | startups | d2c | newsletter) : required\nprevious_tab : tab before the switch : required when trigger = tab_tap\ntrigger : what made it visible : nav_tap | tab_tap | back | app_resume | deeplink : required\nsource : previous screen : brief | company_home | article_reader | company_profile | watchlist | profile | push | deeplink : required',
'None','No',Y,X,X,X,'Which Article tabs are used, and where visits come from','Tap each tab on a test phone: one event each, correct tab. Back from an article: trigger = back','Replaces explore_viewed with sub_tab = articles (5,605 in 30 days). Use underscores in codes (live uses "in-depth" with a hyphen).')
row('2','New','company_home_viewed','Company page becomes visible (same triggers as above)','Super',
'tab : final list from the build (Figma: all | recently_funded | just_launched | early_rounds | profitable | unicorns | sectors) : required\nprevious_tab : required when trigger = tab_tap\ntrigger : nav_tap | tab_tap | back | app_resume | deeplink : required\nsource : same list as article_home_viewed : required\nfilters_count : number of active filters : required',
'None','No',Y,X,X,X,'Which Company tabs are used','Same test as article_home_viewed','Replaces explore_viewed with sub_tab = companies (3,873 in 30 days). Live has ipo_bound, early_fundraisers, soonicorns, watchlist tabs that are not in Figma: confirm which survive.')
row('2','New','section_viewed','A section on the Article or Company landing page is at least half on screen for 1 second. Once per section per visit.','Super',
'page_type : article_home | company_home : required\ntab : tab the section is under : required\nsection_name : fixed code : e.g. top_stories | in_depth | markets | financials | stock_watch | recently_funded | directory_strip : required\nsection_position : 1 = top section : required\nitem_count : cards in the section : required',
'None','No',Y,X,X,X,'How far down people scroll, which sections are seen','Scroll to the bottom on a test phone: one event per section. Scrolling back up sends nothing new.','Rough volume: 9,478 page views x 4 to 6 sections = about 38,000 to 57,000 a month, which is 2 to 3 times card_viewed. Confirm PostHog billing, or limit to once per section per session.')
row('2','Extend','card_viewed','Cards on the Article and Company landing pages also fire it','Super + Story',
'ADD source_type values : article_home | company_home\nADD section_name : required when not brief\nADD tab : required when not brief\nADD company_id : required for company cards\nKEEP same visibility rule as section_viewed (half on screen, 1 second, once per visit)',
'None','No',Y,X,X,X,'Which cards are seen on each page','Scroll Article home on a test phone: card_viewed with source_type = article_home, section_name and tab filled','Volume will rise sharply. Update every Brief card insight to filter source_type = brief in the same release.')
row('2','New (decision needed)','story_opened','User opens a story. Exact tap to be confirmed (see open decision 1).','Super + Story',
'source_type : brief | article_home | company_home : required\nstory_id : required\nposition : required\ncard_type : required\nsection_name, tab : required when not brief',
'None','No',Y,X,X,X,'Which card type and which surface lead to a story open','Open a story from the Brief and from Article home: source_type differs','article_opened already fires on the tap that opens the full article (source brief_card 860, explore 1,126). If story_opened is the same tap, extend article_opened instead, or every open is counted twice.')
row('2','Retire','explore_viewed','Keep sending until few people are on old versions, then stop','Super','KEEP as is','None','No',Y+' (for now)',X+' stop now (2,999+ arrive, not approved)',X,X,'Keeps old charts working during the switch','For people on the new build: explore_viewed count roughly equals article_home_viewed + company_home_viewed','Do not stop on release day. Most users are on 1.0.0 (fact 8).')

S.append(('sub',['STEP 3: DIRECTORY AND STOCK WATCH (ship in the same release as these screens)']))
row('3','New','directory_viewed','Company Directory (browse all) screen shown','Super','source : company_home | search | deeplink : required\nresult_count : companies shown : required\nfilters_count : required','None','No',Y,X,X,X,'How many people open the full directory','Open Directory from "Browse all": one event, source = company_home','No view event exists for this screen today.')
row('3','New','filter_changed','A filter is applied, removed, reset or cleared','Super','action : apply | remove | reset | clear_all : required\nsurface : directory | company_home : required\nfilter_group : sector | stage | funding | location | other groups from the build : required unless reset or clear_all\nfilter_value : fixed code of the value : required unless reset or clear_all\nactive_filter_count : required\nresult_count : companies after the change : required','None','No',Y,X,X,X,'Which filters people use, and whether filtering leads to a profile view','Apply Sector = Fintech on a test phone: filter_group = sector, filter_value = fintech, result_count filled','Send codes, not labels. Fire on apply, not on each checkbox inside the drawer.')
row('3','New','sort_changed','Sort order changed','Super','surface : directory : required\nsort_field : total_funding | latest_round | name | others from the build : required\nsort_direction : asc | desc : required\nresult_count : required','None','No',Y,X,X,X,'Which sort people use','Change sort on a test phone: one event','')
row('3','New','stock_row_tapped','A row in Stock Watch is tapped','Super','list_type : gainers | losers | recently_listed : required\ncompany_id : same ID as company_profile_viewed : required\nposition : required\nchange_pct : price change shown : required','None','No',Y,X,X,X,'Is Stock Watch used, and does it lead to profiles','Tap row 3 in Top gainers: list_type = gainers, position = 3, and the next company_profile_viewed has the same company_id','Blocked until the Stock Watch data source is confirmed (open decision 5).')

S.append(('sub',['STEP 4: COMMON ACTIONS']))
row('4','New','drawer_opened','A bottom sheet opens','Super','drawer : filters | tldr | funding_rounds | key_people | corporate_activity | recent_activity | edit_role | edit_topics | edit_sectors | edit_profile | streak_faqs | sign_in : required\nsurface : screen it opened on : required\nentity_type, entity_id : required when the drawer is about a company, story or sector','None','No',Y,X,X,X,'Which drawers are used','Open each drawer once: one event each','')
row('4','New','drawer_dismissed','A bottom sheet closes','Super','drawer : same list : required\nmethod : cta | cancel | swipe | backdrop | not_now : required\nseconds_open : required','None','No',Y,X,X,X,'Where people abandon (for example Edit topics cancelled, Sign in "Not now")','Close the Sign in sheet with "Not now": method = not_now','')
row('4','New','item_expanded','A card or row is expanded or collapsed','Super','surface : required\nentity_type : directory_card | company_chips | company_description | faq_row : required\nentity_id : required when about a company\naction : expand | collapse : required','None','No',Y,X,X,X,'Is hidden detail worth showing','Tap "View more" on a Directory card: action = expand','Keep summary_expanded (2,462 in 30 days) for the TL;DR. Do not move TL;DR into this event.')
row('4','New','list_opened','"View all" tapped','Super','surface : required\ntarget_list : funding_rounds | investors | recently_funded | others from the build : required\nitem_count : required','None','No',Y,X,X,X,'Which full lists people want','Tap "View all 25 funding rounds": target_list = funding_rounds, item_count = 25','')
row('4','New','entity_shared','Share completed on a story, company or sector','Super','entity_type : story | company | sector : required\nentity_id : required\nchannel : same list as story_shared : required\nsource : required\nshare_id : unique ID also put in the shared link : required','None','No',Y,X,X,X,'What gets shared, and which shares bring people back','Share a company on a test phone: entity_type = company, and the shared link carries the share_id','Send story_shared as well until old versions fade. share_id lets an inbound click be matched to the share (story_shared has none today).')
row('4','Build','rating_prompt_shown','"Enjoyed today\'s brief?" sheet appears','Super','trigger : brief_end | streak_day_7 | third_completion : required\nbrief_position : card number when shown : required when trigger = brief_end','None','No',Y,X,X,X,'How often the rating ask is shown','Finish a brief on a test phone: event with trigger = brief_end','Already in App - Events with this name, 0 events ever. Build under the same name.')
row('4','New','rating_prompt_actioned','User answers the rating sheet','Super','trigger : required\naction : rate | later | dismiss : required','rating_prompt_last_action\nrating_prompt_last_at','Yes, person update',Y,X,X,X,'How many people agree to rate','Tap "Maybe later": action = later; person shows rating_prompt_last_action = later','Person properties only needed if re-asking is decided from the server. Skip if the app remembers it on the phone.')
row('4','New super property','theme (on every event)','Set when the app starts and whenever the theme changes','Super','theme : light | dark | system : required on every event','theme','Yes, person update',Y,X,X,X,'How many people use dark mode','Switch to dark on a test phone: the next event carries theme = dark','Do not add auth_state. is_registered already sits on every event.')

S.append(('sub',['STEP 5: SCREEN STATE']))
row('5','New','screen_refreshed','User pulls to refresh, taps refresh, or the app refreshes on its own','Super','screen : required\nmethod : pull | button | auto : required\nresult : fresh | no_change | error : required\nnew_item_count : required\ncontent_age_sec : age of the content before refresh : required','None','No',Y,X,X,X,'Do people refresh because content is stale','Pull to refresh on Brief: one event with result filled','')
row('5','New','empty_state_shown','A screen shows "nothing here"','Super','screen : required\nreason : no_saved_items | no_results | filters_too_narrow | offline : required','None','No',Y,X,X,X,'How often people hit empty screens','Open an empty watchlist: reason = no_saved_items','')
row('5','Extend','error_shown','A user-facing error is shown (fires today, 471 in 30 days)','Super','KEEP error_type, surface\nADD is_retryable : true | false : required\nADD attempt : 1 for first failure : required','None','No',Y,X,X,X,'Which failures can be recovered','Airplane mode, open a screen: error_shown with is_retryable filled','Use this instead of a new content_load_failed event.')
row('5','New','retry_tapped','User taps retry after an error','Super','screen : required\nerror_type : required\nattempt : required','None','No',Y,X,X,X,'Do retries work','Tap retry twice: attempt = 1 then 2','')
row('5','New','network_state_changed','Phone goes offline or comes back online','Super','state : online | offline : required\nscreen : required','None','No',Y,X,X,X,'How much reading happens offline','Toggle airplane mode: one event each way','Fire only on a change, not on every connection check.')
row('5','Do not build','session_end','n/a','n/a','n/a','n/a','n/a',X,X,X,X,'n/a','n/a','PostHog already puts a session ID on every event.')
blank()

sec('5. Person properties')
hdr('Property','Holds','Set by','Today','Used for','PostHog','Customer.io')
row('theme','light | dark | system','App start and theme change','Not present','Dark mode usage',Y,X)
row('watchlist_count','Number of tracked items','watchlist_entity_added / _removed','On 59 of 119 people who added (90 days)','Digest eligibility, upsell',Y,Y+' (fix)')
row('tracked_sector_count','Number of tracked sectors','watchlist_entity_added / _removed','Partly set','Digest eligibility',Y,Y+' (fix)')
row('push_opt_in','true | false','notification_settings_changed (master), push permission events','Set on 1,334 people','Send eligibility',Y,Y)
row('push_types_enabled','List of push types switched on','notification_settings_changed','On 7 of 827 people who allowed push (90 days)','Which pushes to send',Y,Y+' (fix)')
row('rating_prompt_last_action / rating_prompt_last_at','Last answer and time','rating_prompt_actioned','Not present','Not re-asking too soon (only if decided on the server)',Y,X)
row('No person property for page, section or card views','','','','These are behaviour. PostHog groups of users can be built from the events. Add a person property only when Customer.io must target on it.','','')
blank()

sec('6. Nuances to handle')
hdr('#','Nuance','What to do')
row('1','Brief card numbers will jump when Article and Company cards start firing card_viewed','Before Step 2 ships, add the filter source_type = brief (or not set) to every Brief card chart and funnel.')
row('2','Most people are on old app versions (1.0.0: 393, 1.0.1: 244, 1.0.2: 23 in the last 7 days)','Use the update sheet (already built and tracked) to push the update. Keep old and new events side by side, and split charts by app_version during the switch.')
row('3','Live tab names do not match Figma','Get the final tab list from the build. Send fixed codes with underscores, never the on-screen label, so copy changes do not break charts.')
row('4','"View" can fire too often: re-renders, Back, reopening the app','Fire once each time the page becomes visible, and always send trigger so Back and reopen can be filtered out. Android and iOS must follow the same rule.')
row('5','Scroll-based events (section_viewed, card_viewed) can fire on fast scrolls','Half on screen for 1 second, once per visit. Same rule on both platforms.')
row('6','section_viewed may become the largest event (about 38,000 to 57,000 a month)','Confirm PostHog billing. If too high, send once per section per session.')
row('7','Customer.io forwarding sends events that are not approved (76% of its volume)','Switch to an approved list before Step 2, or all new events flood Customer.io.')
row('8','Person properties fail for many users, including signed-out users','Fix the person update in Step 1 before adding any new person property.')
row('9','Same tap counted twice: story_opened vs article_opened','Settle open decision 1 before building story_opened.')
row('10','Names that already exist in the plan but never fired (rating_prompt_shown, share_initiated)','Build under the existing names.')
row('11','Duplicate ideas: auth_state repeats is_registered; content_load_failed repeats error_shown','Do not add them. Use the existing fields.')
row('12','Stock Watch company ID','stock_row_tapped.company_id must match company_profile_viewed.company_id, or taps cannot be joined to profile visits.')
row('13','Personal data','Never put email, phone or name in an event property. They belong only in person properties set at sign-in.')
row('14','Old "explore" values in history','Charts that group by source need both old ("explore") and new (article_home, company_home) values until old versions fade.')
row('15','Testing','Test every row on one Android and one iOS phone using PostHog live events filtered to the test user, before marking Build status done in App - Events.')
blank()

sec('7. Open decisions')
hdr('#','Question','Why it matters','Recommendation')
row('1','Is story_opened a different tap from article_opened?','If both mean "opened the full article", one is enough. Otherwise every open is counted twice.','Extend article_opened with source_type, section and tab, unless story_opened means a different action in the Brief.')
row('2','Final tab codes for Article and Company pages','Live and Figma differ (fact 3). Every tab value depends on it.','Needs the build list.')
row('3','Push the update to old versions?','Only 23 of about 660 recent people are on 1.0.2.','Yes, use the update sheet once Steps 1 and 2 ship.')
row('4','section_viewed: every visit or once per session?','About 38,000 to 57,000 a month at every visit','Every visit, if PostHog billing allows.')
row('5','Stock Watch data: DataLabs or an outside provider?','company_id must match the company profile','Needs your answer.')
row('6','Who owns the Customer.io approved list?','Needed before Step 2','Needs an owner.')

out=['<meta charset="utf-8"><table>']
for k,c in S:
    c=c+['']*(N-len(c)); e=[html.escape(x).replace('\n','<br>') for x in c]
    if k=='title': out.append(f'<tr><td style="font-weight:bold;font-size:16pt">{e[0]}</td>'+'<td></td>'*(N-1)+'</tr>')
    elif k=='sec': out.append('<tr>'+''.join(f'<td style="font-weight:bold;background:#c9daf8">{x}</td>' for x in e)+'</tr>')
    elif k=='sub': out.append('<tr>'+''.join(f'<td style="font-weight:bold;background:#fff2cc">{x}</td>' for x in e)+'</tr>')
    elif k=='hdr': out.append('<tr>'+''.join(f'<td style="font-weight:bold;background:#efefef">{x}</td>' for x in e)+'</tr>')
    elif k=='blank': out.append('<tr>'+'<td></td>'*N+'</tr>')
    else: out.append('<tr>'+''.join(f'<td>{x}</td>' for x in e)+'</tr>')
out.append('</table>')
open('plan3.html','w').write('\n'.join(out))
print(len(S), 'rows')
import re
print('emdash', sum(x.count('—') for k,c in S for x in c))
# cells starting with = or + that sheets may parse
print([x for k,c in S for x in c if x[:1] in '=+-@'])
