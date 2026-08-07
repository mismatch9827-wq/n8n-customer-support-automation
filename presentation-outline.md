# Presentation Outline — AI Customer Support Automation Platform

## Slide 1 — Title
- AI Customer Support Automation Platform
- Assignment 5 final capstone
- Name, course, date

**Speaker note:** Introduce the project as a modular support operation that turns a customer request into a trackable, AI-prioritized workflow.

## Slide 2 — The business problem
- Requests arrive through many channels and are manually processed
- Delays, inconsistent urgency decisions, duplicate effort, and missed follow-ups
- Customer satisfaction drops as volume grows

**Speaker note:** Emphasize that the operational bottleneck is not only ticket volume; it is decision-making and coordination.

## Slide 3 — Goals and success metrics
- Automate registration, triage, routing, notifications, SLA tracking, and feedback
- Reduce first-response and resolution time
- Track SLA breaches, CSAT, sentiment, and recurring issue themes

**Speaker note:** Describe these as measurable outcomes rather than just technical features.

## Slide 4 — Solution architecture
- Streamlit portal → n8n → Google Sheets / OpenAI / Gmail / Slack
- Event-driven workflows with a scheduled daily audit
- Google Sheets is the transparent ticket register for the capstone

**Speaker note:** Use the architecture diagram from the README. Explain that n8n isolates integrations from the UI.

## Slide 5 — Customer portal
- Three tabs: submit ticket, check status, submit feedback
- Generates a unique ticket ID
- Handles connection, timeout, and HTTP errors gracefully

**Speaker note:** Show the live Streamlit application and explain that all forms send JSON to webhooks.

## Slide 6 — Workflow 1: collection and registration
- Webhook → normalize/timestamp → Google Sheets append → Gmail acknowledgment
- Every request starts with an open ticket and a customer confirmation

**Speaker note:** Show one submitted form, then the row and email it creates.

## Slide 7 — Workflow 2: AI classification and triage
- Google Sheets trigger → OpenAI → JSON parser → critical check → Sheets update
- AI returns category, priority, team, and short rationale
- Critical includes outage, security, data loss, or production blockage

**Speaker note:** Mention that JSON-only output makes the downstream automation deterministic.

## Slide 8 — Workflow 3: smart routing and escalation
- Switch routes by priority/category
- Critical tickets create an immediate Slack alert
- Team receives a Gmail assignment with ticket context

**Speaker note:** Show a critical incident example in Slack. The key value is faster human intervention, not fully autonomous resolution.

## Slide 9 — Workflows 4 and 5: SLA and feedback loop
- Daily 9 AM audit flags open tickets older than 24 hours
- Feedback is sentiment-scored and stored for service improvement
- Manager digest makes backlog risk visible

**Speaker note:** Explain the closed-loop process: operational data drives both immediate action and longer-term improvement.

## Slide 10 — Results, controls, and scalability
- Expected: consistent first response, fewer missed SLAs, prioritized queue
- Controls: OAuth credentials, least privilege, no secrets in code, human escalation
- Scale path: replace Sheets with database/queue, add deduplication and knowledge base retrieval

**Speaker note:** Be candid that Google Sheets is suitable for a capstone/small operation; database and queue are the production evolution.

## Slide 11 — Conclusion and Q&A
- Five workflows, 25 nodes, one customer-facing portal
- AI assists decisions; humans retain ownership of sensitive cases
- Questions

**Speaker note:** Finish with the business outcome: reliable support at growing volume.
