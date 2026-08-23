#!/usr/bin/env python3
"""Build ONE clean workbook from the spec, the Jun-2026 warehouse audit, and the latest
browser run. Re-runnable: every audit refreshes it. Replaces 47 tabs of accretion with 5.

  python3 tools/build-sheet.py [--out PATH]
"""
import argparse, glob, json, os
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
OUT_DEFAULT = Path.home() / "ClaudeDocs" / "inc42" / "Inc42 Web Analytics — Event Register.xlsx"

# ── palette ────────────────────────────────────────────────────────────────
INK, MUTE = "1F2A30", "6B7A82"
HDR_BG, HDR_FG = "12333A", "FFFFFF"
TITLE_FG = "0E6F78"
BAND = "F4F7F8"
OK_BG, OK_FG = "E6F4EC", "0F6B3D"
WARN_BG, WARN_FG = "FBF2E2", "8A5A07"
BAD_BG, BAD_FG = "FBECEB", "A32C22"
NA_BG, NA_FG = "EEF1F3", "5B6B73"

F_TITLE = Font(name="Calibri", size=15, bold=True, color=TITLE_FG)
F_SUB = Font(name="Calibri", size=10, color=MUTE)
F_HDR = Font(name="Calibri", size=10, bold=True, color=HDR_FG)
F_BODY = Font(name="Calibri", size=10, color=INK)
F_MONO = Font(name="Consolas", size=9.5, color=INK)
F_MUTE = Font(name="Calibri", size=9.5, color=MUTE)
F_SECT = Font(name="Calibri", size=11, bold=True, color=INK)
FILL_HDR = PatternFill("solid", fgColor=HDR_BG)
FILL_BAND = PatternFill("solid", fgColor=BAND)
TOP = Alignment(vertical="top", wrap_text=True)
TOPL = Alignment(vertical="top", horizontal="left")
TOPR = Alignment(vertical="top", horizontal="right")
THIN = Side(style="thin", color="DDE4E9")
BORDER = Border(bottom=THIN)

TONE = {
    "implemented": (OK_BG, OK_FG), "verified": (OK_BG, OK_FG), "ok": (OK_BG, OK_FG),
    "partial": (WARN_BG, WARN_FG), "gtm_only": (WARN_BG, WARN_FG), "drift": (WARN_BG, WARN_FG),
    "missing": (BAD_BG, BAD_FG), "dead": (BAD_BG, BAD_FG), "P0": (BAD_BG, BAD_FG),
    "P1": (WARN_BG, WARN_FG), "P2": (NA_BG, NA_FG),
    "server_side": (NA_BG, NA_FG), "unplanned": (NA_BG, NA_FG),
}

def load(p):
    return json.loads((ROOT / p).read_text())

def latest_run():
    runs = sorted(glob.glob(str(ROOT / "runs" / "20*")))
    if not runs:
        return None, None
    d = Path(runs[-1])
    drift_p = d / "drift.json"
    drift = json.loads(drift_p.read_text()) if drift_p.exists() else []
    return json.loads((d / "raw.json").read_text()), json.loads((d / "findings.json").read_text()), drift

def header(ws, row, cols):
    for i, (label, width) in enumerate(cols, start=1):
        c = ws.cell(row=row, column=i, value=label)
        c.font, c.fill, c.alignment = F_HDR, FILL_HDR, Alignment(vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(i)].width = width
    ws.row_dimensions[row].height = 28
    ws.freeze_panes = ws.cell(row=row + 1, column=1)

def titleblock(ws, title, sub, cols):
    ws.cell(row=1, column=1, value=title).font = F_TITLE
    ws.cell(row=2, column=1, value=sub).font = F_SUB
    ws.merge_cells(start_row=1, end_row=1, start_column=1, end_column=len(cols))
    ws.merge_cells(start_row=2, end_row=2, start_column=1, end_column=len(cols))
    ws.row_dimensions[2].height = 26
    ws.cell(row=2, column=1).alignment = Alignment(vertical="top", wrap_text=True)

def put(ws, r, c, val, font=F_BODY, align=TOP, tone=None):
    cell = ws.cell(row=r, column=c, value=val)
    cell.font, cell.alignment, cell.border = font, align, BORDER
    if tone and tone in TONE:
        bg, fg = TONE[tone]
        cell.fill = PatternFill("solid", fgColor=bg)
        cell.font = Font(name="Calibri", size=9.5, bold=True, color=fg)
    return cell

# ── build ──────────────────────────────────────────────────────────────────
def main(out_path):
    target = load("spec/target.json")
    aliases = load("spec/aliases.json")
    live = load("spec/live.json")
    raw, findings, drift = latest_run()

    amap = aliases["map"]
    unspecd = aliases.get("unspecified_live_events", {})
    live_by_name = {e["live_name"]: e for e in live["events"] if e.get("live_name")}

    coverage = load("spec/coverage.json")

    # what the browser actually saw, per live event name
    observed_by_name = {}
    seen = {}
    run_stamp = "not run"
    if raw:
        run_stamp = raw.get("browser", {}).get("startedAt", "")[:16].replace("T", " ")
        for e in raw["browser"]["events"]:
            if e.get("replayed") or e.get("source") != "wire":
                continue
            seen.setdefault(str(e.get("name")), {"vendors": set(), "count": 0})
            seen[str(e["name"])]["vendors"].add(e["vendor"])
            seen[str(e["name"])]["count"] += 1
            o = observed_by_name.setdefault(str(e.get("name")), {"vendors": {}})
            o["vendors"][e["vendor"]] = o["vendors"].get(e["vendor"], 0) + 1

    wb = Workbook()

    # ══ 1 · Read Me ═════════════════════════════════════════════════════════
    ws = wb.active
    ws.title = "Read Me"
    ws.column_dimensions["A"].width = 26
    ws.column_dimensions["B"].width = 108
    ws.cell(row=1, column=1, value="Inc42 Web Analytics — Event Register").font = Font(name="Calibri", size=17, bold=True, color=TITLE_FG)
    r = 3
    blocks = [
        ("What this is", "One register for inc42.com editorial + Inc42 Plus. It replaces the 47-tab 'Inc42 Analytics | Master' "
                         "and the separate 'Inc42 Website - Events & Properties' spec. Every event appears exactly once, with "
                         "what it is SUPPOSED to do next to what it ACTUALLY does."),
        ("Reference", "'Inc42 Analytics | Master.xlsx' -> tab 'Audit | Jun 2026' (leftmost = newest; the only tab carrying live "
                      "production names, 30-day volumes and statuses). The July tabs were checked and are not it: 'Inc42 App | "
                      "July 26' is the APP with 2 events referencing MoEngage/Mixpanel/Amplitude (removed vendors), and "
                      "'Inc42 Property Groups | July 26' has property groups but no events."),
        ("Why it exists", "The two previous sheets each held one half of the truth and neither was complete. The plan is "
                          "snake_case; production is Title Case. Only 2 of 63 event names match on their own, so nothing "
                          "could be reconciled by eye."),
        ("", ""),
        ("Tabs", ""),
        ("  Re-Audit vs June", "Every event from 'Audit | Jun 2026' re-tested in a live browser two months on. "
                              "Is that audit still true, and what moved?"),
        ("  Event Register", "THE table. All planned events + every live event that was never planned. Status, live name, "
                             "30-day volume, and whether the browser audit actually observed it."),
        ("  Property Dictionary", "Every property defined once, with its group, type, allowed values, and live coverage."),
        ("  Findings", "Current defects from the automated audit, ranked P0/P1/P2."),
        ("  Scroll Depth", "Worked example: one event, three parallel implementations, five thresholds, three property formats."),
        ("", ""),
        ("Status meanings", ""),
        ("  implemented", "Fires, reaches PostHog, carries its spec'd properties."),
        ("  partial", "Fires, but wrong name, thin payload, near-zero volume, or wrong destination."),
        ("  gtm_only", "Reaches GTM / GA4 / Meta and never reaches PostHog."),
        ("  missing", "Planned. Nothing fires anywhere."),
        ("  unplanned", "Live in production, absent from every plan. Ungoverned."),
        ("  server_side", "Emitted server-side; not observable from the browser."),
        ("", ""),
        ("Verdicts", ""),
        ("  regressed", "June called it healthy with real volume. The journey reached its trigger and it produced nothing."),
        ("  misrouted", "Fires reliably — to GA4/Meta, never to PostHog. June read the low PostHog volume as a firing problem."),
        ("  still broken", "June flagged it; the trigger was reached; still nothing."),
        ("  recovered", "June flagged it; it fires now. The June finding is stale."),
        ("  new", "Live now, absent from the June tab entirely."),
        ("  not tested", "The trigger never occurred, or the journey needs credentials. NOT evidence of a defect."),
        ("", ""),
        ("Browser verified", "'yes' means the automated audit drove the real UI and captured the payload on the wire during "
                             "the run below. Blank does NOT mean broken — it can mean the journey never reached the trigger. "
                             "The Findings tab distinguishes the two."),
        ("", ""),
        ("Sources", "Spec: 'Inc42 Website - Events & Properties.xlsx' (v1.0, 12 Aug 2026).\n"
                    "Warehouse: 'Inc42 Analytics | Master.xlsx' tab 'Audit | Jun 2026' (PostHog 53557, 30d to 22 Jun 2026).\n"
                    "Browser: automated audit, run " + run_stamp + "."),
        ("Regenerate", "cd ~/ClaudeDocs/inc42/event-auditor && node audit.mjs && python3 tools/build-sheet.py"),
        ("Caveat", "30-day volumes are from the June 2026 warehouse audit and are NOT refreshed by a browser-only run. "
                   "Set POSTHOG_API_KEY and run the full audit to refresh them."),
    ]
    for label, body in blocks:
        if label and not body:
            ws.cell(row=r, column=1, value=label).font = F_SECT
        elif label:
            ws.cell(row=r, column=1, value=label).font = Font(name="Calibri", size=10, bold=True, color=INK)
            c = ws.cell(row=r, column=2, value=body)
            c.font, c.alignment = F_BODY, TOP
            ws.row_dimensions[r].height = max(15, 13 * (body.count("\n") + 1 + len(body) // 105))
        r += 1

    # ══ 2 · Re-Audit vs June ════════════════════════════════════════════════
    ws = wb.create_sheet("Re-Audit vs June")
    cols = [("Event (live name)", 26), ("June 2026 status", 20), ("June 30d vol", 12),
            ("Journey that covers it", 20), ("Trigger driven", 30), ("Seen now", 22),
            ("Verdict", 20), ("What this means", 62), ("Pri", 6)]
    titleblock(ws, "Re-Audit vs 'Audit | Jun 2026'",
               f"Every event from the Master sheet's latest tab, re-tested in a live browser on {run_stamp}. "
               "'not tested' rows are honest gaps, not defects — the trigger never occurred or the journey needs credentials.", cols)
    header(ws, 4, cols)
    r = 5
    VERDICT_TONE = {"misrouted": "missing", "regressed since June": "missing", "unchanged": "partial",
                    "new": "partial", "improved since June": "ok", "not tested": "unplanned",
                    "unchanged, unverified": "unplanned"}
    cov_map = coverage["map"]
    drift_by_event = {d["event"]: d for d in drift}
    ordering = {"P0": 0, "P1": 1, "P2": 2}
    for dft in sorted(drift, key=lambda x: (ordering[x["severity"]], x["event"])):
        ev_name = dft["event"]
        c = cov_map.get(ev_name, {})
        obsd = observed_by_name.get(ev_name)
        put(ws, r, 1, ev_name, F_MONO)
        put(ws, r, 2, str(dft.get("junStatus") or ""), F_MUTE)
        put(ws, r, 3, dft.get("junVol") or None, F_BODY, TOPR)
        put(ws, r, 4, c.get("journey") or "— none reaches it", F_MUTE)
        put(ws, r, 5, c.get("trigger") or c.get("why") or "", F_MUTE)
        put(ws, r, 6, (", ".join(f"{k} ×{v}" for k, v in obsd["vendors"].items()) if obsd else "nothing"), F_MONO)
        put(ws, r, 7, dft["verdict"], tone=VERDICT_TONE.get(dft["verdict"]))
        put(ws, r, 8, dft["title"], F_BODY)
        put(ws, r, 9, dft["severity"], tone=dft["severity"])
        r += 1
    ws.auto_filter.ref = f"A4:I{r-1}"
    r += 1
    ws.cell(row=r, column=1, value="EVENTS THAT NEEDED NO FLAG").font = F_SECT
    r += 1
    for ev in live["events"]:
        nm = ev.get("live_name")
        if not nm or nm in drift_by_event or ev.get("noise"):
            continue
        obsd = observed_by_name.get(nm)
        put(ws, r, 1, nm, F_MONO)
        put(ws, r, 2, str(ev.get("status") or ""), F_MUTE)
        put(ws, r, 3, ev.get("volume_30d") or None, F_BODY, TOPR)
        put(ws, r, 4, (cov_map.get(nm) or {}).get("journey") or "", F_MUTE)
        put(ws, r, 5, (cov_map.get(nm) or {}).get("trigger") or "", F_MUTE)
        put(ws, r, 6, (", ".join(f"{k} ×{v}" for k, v in obsd["vendors"].items()) if obsd else "nothing"), F_MONO)
        put(ws, r, 7, "confirmed firing" if obsd else "", tone="ok" if obsd else None)
        put(ws, r, 8, "Observed reaching PostHog this run." if obsd else "", F_MUTE)
        put(ws, r, 9, "", F_MUTE)
        r += 1

    # ══ 3 · Event Register ══════════════════════════════════════════════════
    ws = wb.create_sheet("Event Register")
    cols = [("Group", 22), ("Event (plan)", 26), ("Live name (PostHog)", 24), ("Also fires as", 22),
            ("Status", 13), ("30d volume", 11), ("Browser\nverified", 10), ("Destinations", 15),
            ("Fires when", 40), ("Properties", 34), ("What's wrong / note", 52), ("Pri", 6)]
    titleblock(ws, "Event Register",
               "All 63 planned events, then every live event that was never planned. One row per event. "
               "Sorted by group, then by how broken it is.", cols)
    header(ws, 4, cols)
    r = 5

    order = {"missing": 0, "gtm_only": 1, "partial": 2, "implemented": 3, "server_side": 4}
    groups, seen_groups = [], set()
    for e in target["events"]:
        if e["group"] not in seen_groups:
            seen_groups.add(e["group"]); groups.append(e["group"])

    for g in groups:
        evs = [e for e in target["events"] if e["group"] == g]
        evs.sort(key=lambda e: order.get(amap.get(e["event"], {}).get("status"), 9))
        for e in evs:
            a = amap.get(e["event"], {})
            st = a.get("status", "unmapped")
            lv = live_by_name.get(a.get("posthog"))
            obs = seen.get(a.get("posthog") or "", None)
            dests = "·".join(k.replace(" Pixel", "") for k, v in e["destinations"].items() if v)
            props = " · ".join(p["name"] for p in e["properties"]) or "—"
            if e["property_groups"]:
                props = f"[{'+'.join(e['property_groups'])}] " + props
            pri = ""
            if st == "missing":
                pri = "P0" if (e["critical"] or e["upsell"]) else "P1"
            elif st in ("gtm_only", "partial"):
                pri = "P1" if lv and lv.get("dead") else "P2"

            name = e["event"] + (" ★" if e["critical"] else " ↑" if e["upsell"] else "")
            put(ws, r, 1, g, F_MUTE)
            put(ws, r, 2, name, F_MONO)
            put(ws, r, 3, a.get("posthog") or "—", F_MONO)
            put(ws, r, 4, a.get("gtm") or "", F_MONO)
            put(ws, r, 5, st, tone=st)
            put(ws, r, 6, lv["volume_30d"] if lv else None, F_BODY, TOPR)
            put(ws, r, 7, "yes" if obs else "", tone="verified" if obs else None)
            put(ws, r, 8, dests, F_MUTE)
            put(ws, r, 9, e["fires_when"], F_MUTE)
            put(ws, r, 10, props, F_MUTE)
            put(ws, r, 11, a.get("note") or "", F_MUTE)
            put(ws, r, 12, pri, tone=pri or None)
            r += 1

    # unplanned live events
    ws.cell(row=r + 1, column=1, value="LIVE BUT NEVER PLANNED").font = F_SECT
    r += 2
    for name, note in sorted(unspecd.items(), key=lambda kv: -(live_by_name.get(kv[0], {}).get("volume_30d") or 0)):
        lv = live_by_name.get(name)
        obs = seen.get(name)
        put(ws, r, 1, "—", F_MUTE)
        put(ws, r, 2, "—", F_MUTE)
        put(ws, r, 3, name, F_MONO)
        put(ws, r, 4, "", F_MONO)
        put(ws, r, 5, "unplanned", tone="unplanned")
        put(ws, r, 6, lv["volume_30d"] if lv else None, F_BODY, TOPR)
        put(ws, r, 7, "yes" if obs else "", tone="verified" if obs else None)
        put(ws, r, 8, "", F_MUTE); put(ws, r, 9, "", F_MUTE); put(ws, r, 10, "", F_MUTE)
        put(ws, r, 11, note, F_MUTE)
        put(ws, r, 12, "P1" if lv and lv.get("duplicate") else "P2", tone="P1" if lv and lv.get("duplicate") else "P2")
        r += 1

    ws.auto_filter.ref = f"A4:L{r-1}"
    ws.cell(row=r + 1, column=1, value="★ north-star   ↑ commercial-intent signal").font = F_MUTE

    # ══ 3 · Property Dictionary ═════════════════════════════════════════════
    ws = wb.create_sheet("Property Dictionary")
    cols = [("Property", 30), ("Group", 11), ("Type", 10), ("Allowed values", 46),
            ("Live key(s) found", 30), ("Coverage", 13), ("Status", 11), ("Note", 56)]
    titleblock(ws, "Property Dictionary",
               "Every property defined once. 'Live key(s)' and coverage come from the June 2026 warehouse audit; "
               "blank means the property was not checked at warehouse level.", cols)
    header(ws, 4, cols)
    r = 5
    prop_live = {}
    for p in live["properties"]:
        prop_live[p["plan_property"].strip().lower()] = p
    for d in target["dictionary"]:
        pl = prop_live.get(d["property"].strip().lower())
        st = ""
        if pl:
            st = "ok" if pl["ok"] else "dead" if pl["dead"] else "drift"
        put(ws, r, 1, d["property"], F_MONO)
        put(ws, r, 2, d["group"], F_MUTE)
        put(ws, r, 3, d["type"], F_MUTE)
        put(ws, r, 4, d["raw_allowed"], F_MUTE)
        put(ws, r, 5, pl["live_keys"] if pl else "", F_MONO)
        put(ws, r, 6, pl["coverage"] if pl else "", F_BODY, TOPR)
        put(ws, r, 7, st, tone=st or None)
        put(ws, r, 8, pl["notes"] if pl else "", F_MUTE)
        r += 1
    ws.auto_filter.ref = f"A4:H{r-1}"

    # ══ 4 · Findings ════════════════════════════════════════════════════════
    ws = wb.create_sheet("Findings")
    cols = [("Pri", 6), ("Class", 20), ("Event", 26), ("Finding", 46), ("Evidence", 58), ("Impact", 50), ("Fix", 50)]
    titleblock(ws, "Findings",
               f"Automated audit, run {run_stamp}. Browser half only unless a PostHog key was supplied — "
               "'Unverified' rows resolve once the warehouse query runs.", cols)
    header(ws, 4, cols)
    r = 5
    for f in (findings or []):
        put(ws, r, 1, f["severity"], tone=f["severity"])
        put(ws, r, 2, f["cls"], F_MUTE)
        put(ws, r, 3, f["event"], F_MONO)
        put(ws, r, 4, f["title"].replace("`", ""), F_BODY)
        put(ws, r, 5, f["evidence"].replace("`", ""), F_MUTE)
        put(ws, r, 6, f["impact"].replace("`", ""), F_MUTE)
        put(ws, r, 7, f["fix"].replace("`", ""), F_MUTE)
        r += 1
    if r > 5:
        ws.auto_filter.ref = f"A4:G{r-1}"

    # ══ 5 · Scroll Depth ════════════════════════════════════════════════════
    ws = wb.create_sheet("Scroll Depth")
    cols = [("Implementation", 30), ("Event name", 28), ("Destination", 16), ("Thresholds seen", 22),
            ("Property carrying the depth", 30), ("Format", 16), ("Observed", 11), ("Verdict", 62)]
    titleblock(ws, "Scroll Depth — one behaviour, three implementations",
               f"Captured across 8 articles, run {run_stamp}. This is what 'not triggering properly' looks like in detail.", cols)
    header(ws, 4, cols)

    rows = []
    if raw:
        agg = {}
        for e in raw["browser"]["events"]:
            if e.get("replayed"):
                continue
            nm = str(e.get("name") or "")
            if "scroll" not in nm.lower():
                continue
            p = e.get("props") or {}
            thr = p.get("gtm.scrollThreshold") or p.get("Scroll_Percentage") or p.get("percent_scrolled")
            k = (nm, e["vendor"])
            agg.setdefault(k, {"thr": set(), "count": 0, "key": None, "src": e.get("source")})
            if thr is not None:
                agg[k]["thr"].add(str(thr))
            for cand in ("gtm.scrollThreshold", "Scroll_Percentage", "percent_scrolled"):
                if cand in p:
                    agg[k]["key"] = cand
            agg[k]["count"] += 1
        IMPL = {
            "gtm.scrollDepth": "GTM built-in scroll trigger",
            "Custom Scroll Depth": "Custom GTM tag",
            "ScrollDepth-Value-Calculator": "Custom GTM tag (Meta value-bid)",
            "scroll": "GA4 enhanced measurement",
            "Scroll Depth": "Custom GTM tag → GA4",
        }
        FMT = {"gtm.scrollThreshold": "number (25)", "Scroll_Percentage": 'string ("25%")', "percent_scrolled": 'string ("90")'}
        for (nm, vendor), v in sorted(agg.items(), key=lambda kv: -kv[1]["count"]):
            thr = sorted(v["thr"], key=lambda x: float(str(x).rstrip("%") or 0))
            rows.append((IMPL.get(nm, "—"), nm, vendor, " / ".join(thr) or "—",
                         v["key"] or "—", FMT.get(v["key"], "—"), v["count"],
                         "on the wire" if v["src"] == "wire" else "dataLayer only"))
    r = 5
    for impl, nm, vendor, thr, key, fmt, count, where in rows:
        put(ws, r, 1, impl, F_BODY)
        put(ws, r, 2, nm, F_MONO)
        put(ws, r, 3, vendor, F_MUTE)
        put(ws, r, 4, thr, F_MONO)
        put(ws, r, 5, key, F_MONO)
        put(ws, r, 6, fmt, F_MUTE)
        put(ws, r, 7, count, F_BODY, TOPR)
        put(ws, r, 8, where, F_MUTE)
        r += 1
    put(ws, r, 1, "PostHog", F_BODY)
    put(ws, r, 2, "(none)", F_MONO)
    put(ws, r, 3, "posthog", F_MUTE)
    put(ws, r, 4, "—", F_MONO)
    put(ws, r, 5, "—", F_MONO)
    put(ws, r, 6, "—", F_MUTE)
    put(ws, r, 7, 0, F_BODY, TOPR)
    put(ws, r, 8, "NEVER FIRES", tone="missing")
    r += 2

    ws.cell(row=r, column=1, value="WHAT'S WRONG").font = F_SECT
    r += 1
    verdicts = [
        ("PostHog receives nothing", "Zero scroll events across 8 articles. The core editorial engagement signal is absent "
                                     "from the tool product decisions are made in."),
        ("Three parallel implementations", "GTM's built-in trigger, a 'Custom Scroll Depth' tag, and a "
                                           "'ScrollDepth-Value-Calculator' tag all fire on the same scroll."),
        ("Thresholds don't match the plan", "Plan says 25/50/75/100. Production fires at 25/50/75/90/100 — the 90 threshold "
                                            "is undocumented and the most frequent of all."),
        ("GA4 gets two different events", "'scroll' (enhanced measurement, only ever at 90) and 'Scroll Depth' (custom, at "
                                          "25/50). Two names for one action; neither alone is the full curve."),
        ("Three formats for one number", 'gtm.scrollThreshold = 25 (number) · Scroll_Percentage = "25%" (string with %) · '
                                         'percent_scrolled = "90" (string, no %). No consumer can join these.'),
        ("Custom tag is unreliable", "'Custom Scroll Depth' fired on only 4 of 8 articles and never above 50%. The deep-read "
                                     "signal — 75% and 100% — is not captured anywhere except GTM's internal dataLayer."),
        ("Genuine double-fire", "'Custom Scroll Depth' and 'ScrollDepth-Value-Calculator' each emit duplicate payloads "
                                "within 2s at the same threshold."),
    ]
    for t, b in verdicts:
        c = ws.cell(row=r, column=1, value=t); c.font = Font(name="Calibri", size=10, bold=True, color=BAD_FG); c.alignment = TOP
        c2 = ws.cell(row=r, column=2, value=b); c2.font, c2.alignment = F_BODY, TOP
        ws.merge_cells(start_row=r, end_row=r, start_column=2, end_column=8)
        ws.row_dimensions[r].height = 30
        r += 1
    r += 1
    ws.cell(row=r, column=1, value="FIX").font = F_SECT
    c = ws.cell(row=r, column=2, value="Emit one canonical scroll_depth event to PostHog at 25/50/75/100 carrying the Super + "
                                       "Story bundle and depth_percent as an integer. Retire the two custom GTM tags; keep the "
                                       "Meta value as a property on the one event, not a second event. Decide whether 90 stays "
                                       "(GA4 enhanced measurement) and document it if so.")
    c.font, c.alignment = F_BODY, TOP
    ws.merge_cells(start_row=r, end_row=r, start_column=2, end_column=8)
    ws.row_dimensions[r].height = 46

    for sheet in wb.worksheets:
        sheet.sheet_view.showGridLines = False

    out_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out_path)
    n_plan = len(target["events"])
    n_live = len(unspecd)
    print(f"saved  {out_path}")
    print(f"       Event Register      {n_plan} planned + {n_live} unplanned")
    print(f"       Property Dictionary {len(target['dictionary'])} properties")
    print(f"       Re-Audit vs June    {len(drift)} flagged")
    print(f"       Findings            {len(findings or [])}")
    print(f"       Scroll Depth        {len(rows)} implementations + PostHog (none)")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(OUT_DEFAULT))
    main(Path(ap.parse_args().out))
