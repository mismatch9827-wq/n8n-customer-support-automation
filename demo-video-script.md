# Demo Video Script (about 7–8 minutes)

## 0:00–0:40 — Introduction

“This is my AI Customer Support Automation Platform. It solves the delays and inconsistent prioritization that happen when support tickets are manually categorized and assigned. The solution uses a Streamlit portal and five modular n8n workflows connected to Google Sheets, OpenAI, Gmail, and Slack.”

Show the architecture diagram, then the Streamlit home screen.

## 0:40–1:40 — Submit a ticket

“The first tab is where a customer creates a ticket. I will enter a name and email, choose Technical issue, and describe that the production dashboard is unavailable for all users. The app generates a unique ticket ID and posts the ticket JSON to the n8n webhook.”

Submit the form. Point to the successful confirmation. Briefly show `app.py`'s webhook configuration and explain that the real n8n production URL is stored in `.env`, not in source code.

## 1:40–2:35 — Ingestion workflow and ticket register

Open n8n Workflow 1.

“The ticket webhook starts the collection workflow. The code node normalizes the request and adds a timestamp and initial status. The Google Sheets node appends the ticket to the Tickets register, and Gmail sends an immediate acknowledgment.”

Show the new Google Sheets row and then the inbox acknowledgment. State the ticket ID aloud.

## 2:35–3:40 — AI classification and priority

Open Workflow 2 and its latest execution.

“A new spreadsheet row triggers the AI triage workflow. I provide OpenAI with the category hint and customer description. It must return JSON only: category, priority, team, and rationale. This incident is classified as Critical because the production dashboard is unavailable.”

Show the OpenAI output and the updated columns in Sheets. Mention the model is an assistant to support operations and rules define the critical threshold.

## 3:40–4:40 — Routing and escalation

Open Workflow 3.

“The routing workflow uses a Switch node. Critical tickets notify the incident channel in Slack, while categorized tickets are forwarded to the appropriate team through Gmail. This reduces the time between identifying an urgent issue and putting it in front of the right people.”

Show Slack alert and the forwarding email. Highlight ticket ID, priority, and description.

## 4:40–5:40 — SLA monitoring

Open Workflow 4 and set/show a test ticket that is Open and older than 24 hours.

“Every day at 9 AM, the SLA workflow reads the Tickets register and filters tickets that are still Open, Triaged, or In Progress after 24 hours. It builds a concise manager digest and sends it to Slack.”

Execute manually for the demo. Show the Slack digest. Explain that this is an escalation safety net.

## 5:40–6:45 — Feedback and sentiment

Return to Streamlit Feedback tab.

“After closure, the customer can submit a rating and comments. I will submit a low rating with feedback about slow updates.”

Submit. Open Workflow 5 execution and show the feedback sheet row.

“OpenAI returns a sentiment and theme, while a low score can be marked action required. The workflow logs the result, waits briefly, and sends a thank-you email.”

## 6:45–7:30 — Status, results, and conclusion

Show the status tab and explain it calls the optional small lookup webhook, which reads the ticket register by ID or email.

“The platform delivers consistent registration, AI-assisted prioritization, rapid critical escalation, SLA visibility, and a feedback loop. The five core workflows contain 25 nodes and can be extended by replacing Google Sheets with a production database, adding deduplication, and ingesting email, chatbot, and social sources. Thank you.”
