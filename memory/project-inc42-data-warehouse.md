---
name: project-inc42-data-warehouse
description: "INC42's unified BigQuery data warehouse (8 sources → Bronze/Silver/Gold) — live since Apr 2026, powers contact_360/company_360 and Customer.io reverse ETL"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1414dfae-c80e-4314-8abb-3b8f31460628
---

INC42 runs a production data warehouse (repo: `github.com/Prapti-art/inc42-data-warehouse`, private) unifying 8 source systems — Gravity Forms, Tally, Inc42 DB, Customer.io, WooCommerce, HubSpot, Datalabs DB, Moengage — into BigQuery via a Bronze (raw, 48 tables) → PySpark identity/company resolution → Silver (30+ clean dbt models) → quality gate → Gold (star schema) pipeline, orchestrated by Airflow.

**Why it matters:** it's the backbone for identity resolution (one `unified_contact_id` per real person across 7+ systems), company enrichment (Datalabs-powered, 75K companies), and the engagement/segmentation data that feeds Customer.io campaigns via reverse ETL (shipped Jun 16–19 2026).

**Scale as of Apr 2026 status snapshot:** 25.3M Bronze rows, 328K unified contacts (`contact_360`, 80+ cols), 75K companies (`company_360`). Infra cost ~$23/month (BigQuery+GCS+Airflow VM+Streamlit dashboard VM).

**Key mechanisms:**
- `net_ltv` rolls up **4 order surfaces** (WooCommerce main, WooCommerce events42, D2CX WooCommerce, D2CX direct Razorpay) with dedup between WC and Razorpay.
- RFV engagement scoring on `contact_360`: separate paid/nonpaid/combined scores with exponential recency decay, tiered hot/engaged/passive/dormant — paid weighted 2x. `moengage_ltv`/`moengage_*` are separate app-side figures, NOT part of `net_ltv` or the RFV scores.
- `silver.events` (added May 2026) unions free registrations + paid tickets, dedupes, tracks per-year loyalty (`years_as_paid_attendee`).
- Join key for gold facts is `contact_key` (INT64 surrogate), not the Silver `unified_contact_id` UUID.

**Relevant cross-link:** [[project-inc42-content-personalization]] notes 86% of articles have no sector, killing sector-based content personalization — but `company_360` here DOES carry Datalabs-sourced sector enrichment per contact's company, which is a different (company-level, not article-level) signal worth considering if sector personalization is revisited.

**Still open (as of the doc's last update):** HubSpot ingestion deferred, Looker Studio dashboards for leadership not yet built, Google OAuth for the Streamlit dashboard needs a subdomain (data.inc42.com).

**How to apply:** when discussing INC42 personalization, lifecycle marketing, Customer.io segmentation, or revenue/LTV reporting, this warehouse is the source of truth — check `contact_360`/`company_360` semantics (esp. net_ltv vs moengage_ltv, and the paid/nonpaid RFV split) before proposing new metrics, to avoid redefining something that already exists.
