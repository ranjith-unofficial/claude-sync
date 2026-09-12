# Cohort parity — brief_completed & sign_in_completed

**Audited:** 2026-09-12 17:18 IST  
**PH:** Inc42 App `146258` · **CIO:** Inc42 App `224949`  
**Method:** HogQL sample of persons with email who fired the event in last 30d → per-email CIO profile lookup → `GET /logs?internal_id=&type=event&name=` (activity logs, ~30d retention).

## brief_completed cohort (n=25)

| # | email (redacted in summary) | CIO profile? | CIO event `brief_completed` | CIO attr `last_brief_completed_at` |
|---|----------------------------|--------------|-----------------------------|------------------------------------|
| 1 | pabandeepswain@zohomail.in | **NO** | n/a | n/a |
| 2 | pranav@clarcai.com | Y | Y (15) | Y |
| 3 | dubey.anand082@gmail.com | Y | Y (1) | Y |
| 4 | shatayubhatnagar98@gmail.com | Y | Y (16) | Y |
| 5 | sudsingh32@gmail.com | Y | Y (3) | Y |
| 6 | saketh.research@gmail.com | Y | Y (1) | Y |
| 7 | onehabitus@gmail.com | Y | Y (2) | Y |
| 8 | 9chr8g2b96@privaterelay.appleid.com | Y | Y (1) | Y |
| 9 | saubhagyakukrety1999@gmail.com | Y | Y (3) | Y |
| 10 | arnabds179@gmail.com | Y | Y (2) | Y |
| 11 | nehalk482@gmail.com | Y | **NO (0)** | **Y** (attr without event) |
| 12 | hartej23196@gmail.com | Y | Y (7) | Y |
| 13 | skk360951@gmail.com | Y | Y (2) | Y (stale vs PH same-day complete) |
| 14 | **lalitarorac9@gmail.com** | Y | **NO (0)** | **NO** |
| 15 | utkarsh@inc42.com | Y | Y (14) | Y |
| 16 | animesh.kumar@inc42.com | Y | Y (48) | Y |
| 17 | nitin.tripathi@gmail.com | Y | Y (5) | Y |
| 18 | anidhya5105r@gmail.com | Y | Y (1) | Y |
| 19 | vamsik.namala@gmail.com | Y | Y (4) | Y |
| 20 | ashishu001@gmail.com | Y | Y (15) | Y |
| 21 | info@plusvalueindia.com | Y | Y (1) | Y |
| 22 | amieshverma@gmail.com | Y | Y (1) | Y |
| 23 | kavicharlaraviteja@gmail.com | Y | Y (7) | Y |
| 24 | rahim.tester@gmail.com | Y | Y (8) | Y |
| 25 | saniyamohan14@gmail.com | Y | Y (2) | Y |

### Gap rates — brief_completed

| Definition | Rate |
|------------|------|
| PH event but **no CIO profile** | **1/25 = 4%** (pabandeepswain) |
| PH event but **no CIO event** (incl. no profile) | **3/25 = 12%** (pabandeep + lalit + nehalk) |
| Profile found but **no CIO event** | **2/24 = 8.3%** (lalit + nehalk) |
| Profile found, **attr set but event missing** | **1/24 = 4.2%** (nehalk) |

**Parity (CIO event present | PH sample):** **22/25 = 88%**

## sign_in_completed cohort (n=15)

| # | email | CIO profile? | CIO event `sign_in_completed` |
|---|-------|--------------|-------------------------------|
| 1 | harshbagaria27@gmail.com | Y | Y (7) |
| 2 | pabandeepswain@zohomail.in | **NO** | n/a |
| 3 | pranav@clarcai.com | Y | Y (5) |
| 4 | arihantkhivasara02@gmail.com | Y | Y (1) |
| 5 | sudsingh32@gmail.com | Y | Y (4) |
| 6 | sinha.satyam045@gmail.com | Y | Y (1) |
| 7 | ranveeriitjee1@gmail.com | Y | Y (2) |
| 8 | saketh.research@gmail.com | Y | Y (1) |
| 9 | chiragbgupta@gmail.com | Y | Y (3) |
| 10 | onehabitus@gmail.com | Y | Y (3) |
| 11 | varun.sja@gmail.com | Y | Y (9) |
| 12 | ashishsri87@gmail.com | Y | Y (5) |
| 13 | hardik.bagdai95@gmail.com | Y | Y (2) |
| 14 | sangame.parshwa@gmail.com | Y | Y (6) |
| 15 | chetasndholakia2023@gmail.com | Y | Y (1) |

### Gap rates — sign_in_completed

| Definition | Rate |
|------------|------|
| PH event but **no CIO profile** | **1/15 = 6.7%** |
| PH event but **no CIO event** (incl. no profile) | **1/15 = 6.7%** |
| Profile found but **no CIO event** | **0/14 = 0%** in this sample |

**Caveat:** Exhibit A (`lalitarorac9`) is **outside** this top-15 window and **does** miss `sign_in_completed` on CIO. Sample gap understates intermittent auth-event drops.

## Cross-cutting observations

1. Workspace-wide CIO `logs?name=brief_completed` returns many **anonymous UUID** customer ids in `filter_matches` — consistent with events firing **before identify**.
2. `nehalk482`: person attrs updated (`last_brief_completed_at`) **without** track event — matches Aug 29 note “no setPersonProperties” / partial identify path.
3. `lalitarorac9`: identify completed (`209480`) **before** `brief_completed` in PH, yet CIO still missing both terminal events → not only pre-identify timing.
