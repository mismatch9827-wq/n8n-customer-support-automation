"""Streamlit UI for the AI Customer Support Automation Platform."""
from __future__ import annotations

import os
import uuid
from html import escape
from datetime import datetime, timezone
from typing import Any

import requests
import streamlit as st
from dotenv import load_dotenv


load_dotenv()
st.set_page_config(page_title="SupportFlow AI", page_icon="🎧", layout="wide", initial_sidebar_state="expanded")

DEFAULT_BASE_URL = "https://your-n8n-instance/webhook"
N8N_BASE_URL = os.getenv("N8N_WEBHOOK_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
WEBHOOKS = {
    "ticket": os.getenv("N8N_TICKET_WEBHOOK_URL", f"{N8N_BASE_URL}/support-ticket"),
    "status": os.getenv("N8N_STATUS_WEBHOOK_URL", f"{N8N_BASE_URL}/ticket-status"),
    "feedback": os.getenv("N8N_FEEDBACK_WEBHOOK_URL", f"{N8N_BASE_URL}/ticket-feedback"),
}


def post_to_automation(url: str, payload: dict[str, Any]) -> tuple[bool, str, dict[str, Any] | None]:
    """Send JSON to n8n and return a safe, user-facing result."""
    if "your-n8n-instance" in url:
        return False, "Webhook URL is not configured. Update your .env file first.", None
    try:
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        try:
            return True, "", response.json()
        except ValueError:
            return True, "", None
    except requests.exceptions.Timeout:
        return False, "The automation service took too long to respond. Please try again.", None
    except requests.exceptions.ConnectionError:
        return False, "Could not connect to the automation service. Check the webhook URL and n8n status.", None
    except requests.exceptions.HTTPError as error:
        detail = error.response.text[:250] if error.response is not None else ""
        return False, f"The automation service returned an error ({error.response.status_code}). {detail}", None
    except requests.exceptions.RequestException as error:
        return False, f"Unable to submit your request: {error}", None


def get_response_value(response: dict[str, Any] | None, *keys: str) -> str | None:
    if not response:
        return None
    for key in keys:
        if response.get(key) is not None:
            return str(response[key])
    return None


def sidebar_endpoint_card(label: str, value: str) -> None:
    """Render an explicitly light endpoint display without Streamlit's dark code block."""
    st.markdown(
        f"<div class='endpoint-label'>{escape(label)}</div>"
        f"<div class='endpoint-card'>{escape(value)}</div>",
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <style>
    :root { --ink: #111827; --muted: #4b5563; --line: #dbe3ef; --indigo: #4f46e5; }
    .stApp { background: #f8fafc; color: var(--ink); }
    .block-container { max-width: 1180px; padding-top: 2.25rem; padding-bottom: 3rem; }
    h1, h2, h3, p, label, .stMarkdown, .stCaption { color: var(--ink); }
    [data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid var(--line); }
    [data-testid="stSidebar"] * { color: var(--ink); }
    [data-testid="stTabs"] [data-baseweb="tab-list"] { gap: 1.25rem; border-bottom: 1px solid var(--line); }
    [data-testid="stTabs"] button[role="tab"] { color: #4b5563; font-weight: 600; padding: .65rem .1rem; }
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] { color: var(--indigo); }
    [data-testid="stTabs"] [data-baseweb="tab-highlight"] { background-color: var(--indigo); }
    [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea,
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
        background: #ffffff !important; color: var(--ink) !important; border-color: #cbd5e1 !important;
    }
    input::placeholder, textarea::placeholder { color: #64748b !important; opacity: 1 !important; }
    [data-testid="stTextInput"] input:focus, [data-testid="stTextArea"] textarea:focus {
        border-color: var(--indigo) !important; box-shadow: 0 0 0 3px #e0e7ff !important;
    }
    [data-testid="stForm"] { border: 0; padding: 0; }
    [data-testid="stVerticalBlockBorderWrapper"] { background: #ffffff; border-color: var(--line) !important; border-radius: 14px; }
    .stButton > button, [data-testid="stFormSubmitButton"] > button {
        background: var(--indigo); color: #ffffff; border: 1px solid var(--indigo); border-radius: 8px;
        font-weight: 650; min-height: 2.7rem;
    }
    .stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
        background: #3730a3; border-color: #3730a3; color: #ffffff;
    }
    [data-testid="stAlert"] { border-radius: 10px; }
    .hero { background: #eef2ff; border: 1px solid #c7d2fe; border-radius: 16px; padding: 1.75rem 2rem; }
    .hero__eyebrow { color: #4338ca; font-size: .8rem; font-weight: 750; letter-spacing: .08em; text-transform: uppercase; margin-bottom: .45rem; }
    .hero h1 { color: #111827; font-size: clamp(2rem, 4vw, 2.8rem); line-height: 1.1; margin: 0; }
    .hero p { color: #374151; font-size: 1.05rem; margin: .65rem 0 0; }
    .card-kicker { color: #4f46e5; font-size: .78rem; font-weight: 750; letter-spacing: .07em; text-transform: uppercase; margin-bottom: .25rem; }
    .card-title { color: #111827; font-size: 1.35rem; font-weight: 700; margin: 0 0 .3rem; }
    .card-copy { color: #4b5563; margin: 0 0 1.35rem; }
    .status-chip { display: inline-block; background: #e0e7ff; color: #3730a3; border-radius: 999px; padding: .22rem .6rem; font-size: .8rem; font-weight: 700; }
    .endpoint-label { color: #374151; font-size: .88rem; font-weight: 650; margin: .8rem 0 .3rem; }
    .endpoint-card { background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; color: #1f2937;
                     font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: .78rem;
                     line-height: 1.45; overflow-wrap: anywhere; padding: .7rem .75rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### SupportFlow AI")
    st.caption("Automation control panel")
    st.divider()
    st.markdown("#### Administrator setup")
    configured = "your-n8n-instance" not in N8N_BASE_URL
    if configured:
        st.success("n8n base URL configured")
    else:
        st.warning("Webhook configuration is required")
    with st.expander("Webhook configuration", expanded=False):
        st.caption("Configure URLs through environment variables; they are shown here for verification only.")
        st.markdown(
            "<div class='endpoint-card'>"
            "N8N_WEBHOOK_BASE_URL=https://your-n8n-instance/webhook<br><br>"
            "Optional individual overrides:<br>"
            "N8N_TICKET_WEBHOOK_URL=...<br>"
            "N8N_STATUS_WEBHOOK_URL=...<br>"
            "N8N_FEEDBACK_WEBHOOK_URL=..."
            "</div>",
            unsafe_allow_html=True,
        )
    with st.expander("Active endpoints", expanded=False):
        for label, url in WEBHOOKS.items():
            sidebar_endpoint_card(label.title(), url)
    st.divider()
    st.info("Customer submissions are securely passed to your configured n8n workflows.")

st.markdown(
    """
    <section class="hero">
      <div class="hero__eyebrow">AI-Powered Customer Support</div>
      <h1>🎧 SupportFlow AI</h1>
      <p>Submit, track, and improve support requests through one intelligent service desk.</p>
    </section>
    """,
    unsafe_allow_html=True,
)
st.divider()

tab_ticket, tab_status, tab_feedback = st.tabs(
    ["Submit Support Ticket", "Check Ticket Status", "Submit Feedback"]
)

with tab_ticket:
    with st.container(border=True):
        st.markdown("<p class='card-kicker'>New request</p><h2 class='card-title'>Tell us how we can help</h2><p class='card-copy'>Provide a few details and our automation will register, prioritize, and route your request.</p>", unsafe_allow_html=True)
        with st.form("ticket_form", clear_on_submit=True):
            name_col, email_col = st.columns(2, gap="large")
            name = name_col.text_input("Full name *", max_chars=100, placeholder="Jane Doe")
            email = email_col.text_input("Email address *", placeholder="jane@example.com")
            category_col, reference_col = st.columns([2, 1], gap="large")
            category = category_col.selectbox("Issue category *", ["Technical issue", "Billing & account", "Feature request", "Access & login", "Other"])
            reference_col.markdown("<br><span class='status-chip'>Typical reply: under 24 hours</span>", unsafe_allow_html=True)
            description = st.text_area("Detailed description *", height=155, placeholder="Include error messages, affected product area, and steps already tried.")
            submitted = st.form_submit_button("Submit support ticket", type="primary", use_container_width=True)

    if submitted:
        if not name.strip() or not email.strip() or not description.strip():
            st.warning("Please complete all required fields before submitting.")
        elif "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            st.warning("Please enter a valid email address.")
        else:
            ticket_id = f"SUP-{uuid.uuid4().hex[:8].upper()}"
            payload = {
                "ticketId": ticket_id, "name": name.strip(), "email": email.strip().lower(),
                "category": category, "description": description.strip(), "status": "Open",
                "submittedAt": datetime.now(timezone.utc).isoformat(), "source": "Streamlit Web App",
            }
            with st.spinner("Creating your ticket and notifying the support team..."):
                success, message, response = post_to_automation(WEBHOOKS["ticket"], payload)
            if success:
                returned_id = get_response_value(response, "ticketId", "ticket_id") or ticket_id
                st.success(f"Ticket {returned_id} submitted successfully. An acknowledgment email is on its way.")
            else:
                st.error(message)

with tab_status:
    with st.container(border=True):
        st.markdown("<p class='card-kicker'>Ticket tracker</p><h2 class='card-title'>Check your ticket status</h2><p class='card-copy'>Use the ticket ID or the email address from your original request.</p>", unsafe_allow_html=True)
        with st.form("status_form"):
            input_col, action_col = st.columns([3, 1], gap="large")
            identifier = input_col.text_input("Ticket ID or email *", placeholder="SUP-1234ABCD or jane@example.com")
            action_col.markdown("<br>", unsafe_allow_html=True)
            status_submitted = action_col.form_submit_button("Check status", type="primary", use_container_width=True)
    if status_submitted:
        if not identifier.strip():
            st.warning("Enter a ticket ID or email address.")
        else:
            with st.spinner("Checking ticket status..."):
                success, message, response = post_to_automation(WEBHOOKS["status"], {"identifier": identifier.strip()})
            if not success:
                st.error(message)
            elif response:
                status = get_response_value(response, "status") or "No matching ticket found"
                st.info(f"**Status:** {status}")
                if response.get("ticketId"):
                    st.write(f"Ticket: `{response['ticketId']}`")
                if response.get("updatedAt"):
                    st.caption(f"Last updated: {response['updatedAt']}")
            else:
                st.warning("The status workflow returned no ticket data.")

with tab_feedback:
    with st.container(border=True):
        st.markdown("<p class='card-kicker'>Service improvement</p><h2 class='card-title'>Rate your support experience</h2><p class='card-copy'>Your feedback helps us recognize what is working and improve what is not.</p>", unsafe_allow_html=True)
        with st.form("feedback_form", clear_on_submit=True):
            ticket_col, rating_col = st.columns([2, 1], gap="large")
            ticket_id = ticket_col.text_input("Ticket ID *", placeholder="SUP-1234ABCD")
            rating = rating_col.radio("Rating *", [1, 2, 3, 4, 5], index=4, horizontal=True, format_func=lambda n: "★" * n + "☆" * (5 - n))
            comments = st.text_area("Comments", height=135, placeholder="What went well? What could we improve?")
            feedback_submitted = st.form_submit_button("Send feedback", type="primary", use_container_width=True)
    if feedback_submitted:
        if not ticket_id.strip():
            st.warning("Enter the ticket ID associated with this feedback.")
        else:
            payload = {"ticketId": ticket_id.strip().upper(), "rating": rating, "comments": comments.strip(), "submittedAt": datetime.now(timezone.utc).isoformat()}
            with st.spinner("Sending feedback..."):
                success, message, _ = post_to_automation(WEBHOOKS["feedback"], payload)
            if success:
                st.success("Thank you. Your feedback helps us improve our support service.")
            else:
                st.error(message)
