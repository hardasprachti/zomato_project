import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from src.filter import parse_input, filter_restaurants, serialize_restaurants
from src.prompt_builder import SYSTEM_PROMPT, build_user_prompt
from src.llm_client import get_recommendation

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FoodAI — AI Restaurant Discovery",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS — Deep Midnight Glass & Neural Ember Design System
# ─────────────────────────────────────────────────────────────────────────────
DESIGN_CSS = """
<style>
/* ── Google Fonts ─────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

/* ── Design Tokens ───────────────────────────────────────────────────────── */
:root {
    --bg:              #131318;
    --surface:         #131318;
    --surface-dim:     #0e0e13;
    --surface-low:     #1b1b20;
    --surface-mid:     #1f1f25;
    --surface-high:    #2a292f;
    --surface-highest: #35343a;
    --surface-bright:  #39383e;
    --on-surface:      #e4e1e9;
    --on-surface-var:  #e1bfb5;
    --outline:         #a98a80;
    --outline-var:     #594139;
    --primary:         #ffb59d;
    --primary-c:       #ff6b35;
    --on-primary:      #5d1900;
    --secondary:       #ddb7ff;
    --secondary-c:     #6f00be;
    --on-secondary-c:  #d6a9ff;
    --tertiary:        #4ae176;
    --tertiary-c:      #00b150;
    --error:           #ffb4ab;
    --error-c:         #93000a;
    --font-body:       'Inter', sans-serif;
    --font-code:       'JetBrains Mono', monospace;
    --radius-sm:       0.25rem;
    --radius-md:       0.5rem;
    --radius-lg:       1rem;
    --radius-xl:       1.5rem;
    --radius-full:     9999px;
}

/* ── Reset & Base ─────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: var(--font-body) !important;
    background-color: var(--bg) !important;
    color: var(--on-surface) !important;
}
.stApp {
    background: var(--bg) !important;
    background-image:
        radial-gradient(circle at 80% 10%, rgba(110,0,190,0.12) 0%, transparent 45%),
        radial-gradient(circle at 10% 60%, rgba(255,107,53,0.08) 0%, transparent 40%) !important;
    min-height: 100vh;
}

/* ── Hide Streamlit chrome ───────────────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Top gradient accent bar ─────────────────────────────────────────────── */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--primary-c), var(--secondary), var(--primary-c));
    z-index: 9999;
}

/* ── Sidebar ─────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--surface-dim) 0%, var(--surface-mid) 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stSidebar"] * { color: var(--on-surface) !important; }
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stSlider > div { background: transparent !important; }

/* ── Sidebar section headers ─────────────────────────────────────────────── */
.sidebar-section-header {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--outline) !important;
    margin: 1rem 0 0.5rem 0;
}

/* ── Pill filter buttons ─────────────────────────────────────────────────── */
.pill-btn {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 5px 14px;
    border-radius: var(--radius-full);
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.04);
    color: var(--outline);
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: var(--font-body);
}
.pill-btn:hover { background: rgba(255,255,255,0.08); color: var(--on-surface); }
.pill-btn.active {
    background: rgba(255,107,53,0.15);
    border-color: var(--primary-c);
    color: var(--primary-c);
    box-shadow: 0 0 12px rgba(255,107,53,0.2);
}

/* ── Inputs ──────────────────────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: var(--radius-full) !important;
    color: var(--on-surface) !important;
    font-family: var(--font-body) !important;
    font-size: 16px !important;
    padding: 12px 20px !important;
    backdrop-filter: blur(16px);
    transition: border-color 0.2s, box-shadow 0.2s;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--primary-c) !important;
    box-shadow: 0 0 0 3px rgba(255,107,53,0.15), 0 0 24px rgba(255,107,53,0.15) !important;
}
.stTextArea > div > div > textarea { border-radius: var(--radius-lg) !important; }
input::placeholder, textarea::placeholder { color: var(--outline) !important; }

/* ── Select boxes ────────────────────────────────────────────────────────── */
.stSelectbox > div > div {
    background: var(--surface-high) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: var(--radius-full) !important;
    color: var(--on-surface) !important;
}
.stSelectbox [data-baseweb="select"] { background: transparent !important; }

/* ── Select slider ───────────────────────────────────────────────────────── */
.stSelectSlider > div { color: var(--on-surface) !important; }
.stSelectSlider [data-baseweb="slider"] { background: var(--surface-high) !important; }

/* ── Sliders ─────────────────────────────────────────────────────────────── */
.stSlider [data-baseweb="slider"] > div:first-child { background: var(--surface-bright) !important; }
.stSlider [data-baseweb="slider"] > div:nth-child(2) { background: linear-gradient(90deg, var(--primary-c), var(--secondary)) !important; }
.stSlider [data-baseweb="thumb"] {
    background: var(--primary) !important;
    border-color: var(--surface-mid) !important;
    box-shadow: 0 0 12px rgba(255,107,53,0.4) !important;
}

/* ── Buttons ─────────────────────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, var(--primary-c), #f59e0b) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius-full) !important;
    font-family: var(--font-body) !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    letter-spacing: 0.02em !important;
    padding: 10px 28px !important;
    box-shadow: 0 4px 24px rgba(255,107,53,0.35) !important;
    transition: all 0.2s ease !important;
    width: 100%;
}
.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 8px 32px rgba(255,107,53,0.55) !important;
}
.stButton > button:active { transform: scale(0.98) !important; }

/* ── Multiselect ─────────────────────────────────────────────────────────── */
.stMultiSelect > div > div {
    background: var(--surface-mid) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: var(--radius-lg) !important;
}
[data-baseweb="tag"] {
    background: rgba(255,107,53,0.15) !important;
    border: 1px solid var(--primary-c) !important;
    color: var(--primary-c) !important;
    border-radius: var(--radius-full) !important;
}

/* ── Checkboxes ──────────────────────────────────────────────────────────── */
.stCheckbox > label > div:first-child {
    background: rgba(255,255,255,0.06) !important;
    border-color: rgba(255,255,255,0.2) !important;
    border-radius: var(--radius-sm) !important;
}
.stCheckbox > label > div[data-checked="true"]:first-child {
    background: var(--primary-c) !important;
    border-color: var(--primary-c) !important;
}

/* ── Expander ────────────────────────────────────────────────────────────── */
.stExpander > details {
    background: var(--surface-low) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: var(--radius-lg) !important;
    border-left: 3px solid var(--secondary) !important;
}
.stExpander summary { color: var(--on-surface) !important; font-weight: 600 !important; }

/* ── Spinner ─────────────────────────────────────────────────────────────── */
.stSpinner > div { border-top-color: var(--primary-c) !important; }
[data-testid="stSpinner"] { color: var(--secondary) !important; }

/* ── Info / warning / error / success boxes ──────────────────────────────── */
.stAlert { border-radius: var(--radius-lg) !important; }
.stSuccess { background: rgba(34,197,94,0.1) !important; border-color: #22c55e !important; color: var(--on-surface) !important; }
.stError   { background: rgba(239,68,68,0.1) !important;  border-color: #ef4444 !important; color: var(--on-surface) !important; }
.stWarning { background: rgba(245,158,11,0.1) !important; border-color: #f59e0b !important; color: var(--on-surface) !important; }
.stInfo    { background: rgba(168,85,247,0.1) !important; border-color: #a855f7 !important; color: var(--on-surface) !important; }

/* ── DataFrames ──────────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] { border-radius: var(--radius-lg) !important; overflow: hidden; }
[data-testid="stDataFrame"] thead tr th { background: var(--surface-high) !important; color: var(--primary-c) !important; font-weight: 700 !important; }
[data-testid="stDataFrame"] tbody tr:nth-child(even) { background: var(--surface-low) !important; }
[data-testid="stDataFrame"] tbody tr:hover { background: rgba(255,107,53,0.06) !important; }

/* ── Custom component classes ────────────────────────────────────────────── */
.foodai-navbar {
    background: rgba(14,14,19,0.85);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255,255,255,0.06);
    padding: 1rem 2rem;
    border-radius: 0 0 1rem 1rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.foodai-logo {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--on-surface);
}
.foodai-logo span { color: var(--primary-c); }
.powered-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--surface-low);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: var(--radius-full);
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--on-surface-var);
}
.nav-links {
    display: flex;
    gap: 4px;
    align-items: center;
}
.nav-link {
    padding: 6px 14px;
    border-radius: var(--radius-full);
    font-size: 13px;
    font-weight: 600;
    color: var(--outline);
    text-decoration: none;
    transition: all 0.15s ease;
}
.nav-link.active {
    background: var(--surface-high);
    color: var(--primary);
}

/* ── Hero Search Area ────────────────────────────────────────────────────── */
.hero-section {
    max-width: 860px;
    margin: 0 auto 2rem auto;
    text-align: center;
}
.ai-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(110,0,190,0.15);
    border: 1px solid rgba(168,85,247,0.3);
    border-radius: var(--radius-full);
    padding: 5px 16px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--secondary);
    margin-bottom: 1rem;
}
.hero-title {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.15;
    margin-bottom: 0.5rem;
    background: linear-gradient(135deg, var(--on-surface) 0%, var(--primary-c) 60%, var(--secondary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-subtitle {
    font-size: 15px;
    color: var(--outline);
    margin-bottom: 1.5rem;
}
.search-container {
    position: relative;
    background: rgba(14,14,19,0.9);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: var(--radius-full);
    padding: 4px 4px 4px 16px;
    backdrop-filter: blur(20px);
    box-shadow: 0 0 0 1px rgba(255,107,53,0.2), 0 20px 60px rgba(0,0,0,0.6);
    display: flex;
    align-items: center;
    gap: 8px;
}
.quick-cuisine-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-top: 1rem;
}
.cuisine-chip {
    padding: 5px 14px;
    border-radius: var(--radius-full);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    background: var(--surface-high);
    border: 1px solid rgba(255,255,255,0.06);
    color: var(--outline);
    cursor: pointer;
    transition: all 0.15s;
}
.cuisine-chip.hot {
    background: rgba(255,107,53,0.12);
    border-color: rgba(255,107,53,0.3);
    color: var(--primary-c);
}

/* ── Prompt Preview Card ─────────────────────────────────────────────────── */
.prompt-card {
    background: var(--surface-low);
    border: 1px solid rgba(255,255,255,0.06);
    border-left: 3px solid var(--secondary);
    border-radius: var(--radius-lg);
    padding: 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 0 24px rgba(168,85,247,0.08);
}
.prompt-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.75rem;
}
.prompt-card-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--on-surface);
    display: flex;
    align-items: center;
    gap: 8px;
}
.prompt-badge {
    font-size: 11px;
    font-weight: 700;
    background: rgba(110,0,190,0.3);
    border: 1px solid rgba(168,85,247,0.3);
    color: var(--on-secondary-c);
    border-radius: var(--radius-full);
    padding: 2px 10px;
}
.code-block {
    background: var(--surface-dim);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: var(--radius-md);
    padding: 0.75rem;
    font-family: var(--font-code);
    font-size: 12px;
    line-height: 1.6;
    overflow-x: auto;
    color: var(--on-surface);
}
.code-keyword { color: var(--primary-c); font-weight: 600; }
.code-value   { color: var(--tertiary); }
.code-param   { color: var(--secondary); }
.code-comment { color: var(--outline); }
.prompt-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 0.5rem;
    padding-top: 0.5rem;
    border-top: 1px solid rgba(255,255,255,0.05);
}
.token-count {
    font-family: var(--font-code);
    font-size: 11px;
    color: var(--outline);
    display: flex;
    align-items: center;
    gap: 6px;
}
.token-dot { width:8px; height:8px; border-radius:50%; background:var(--tertiary); display:inline-block; }

/* ── Results Header ──────────────────────────────────────────────────────── */
.results-header {
    background: var(--surface-mid);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: var(--radius-lg);
    padding: 0.75rem 1.25rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
}
.results-count {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 17px;
    font-weight: 700;
    letter-spacing: -0.01em;
}
.live-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: var(--tertiary);
    box-shadow: 0 0 10px var(--tertiary);
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
}
.results-meta { font-size: 13px; color: var(--outline); }

/* ── Restaurant Card ─────────────────────────────────────────────────────── */
.restaurant-card {
    background: var(--surface-low);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: var(--radius-lg);
    overflow: hidden;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
    position: relative;
}
.restaurant-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 40px rgba(255,107,53,0.2);
    border-color: rgba(255,107,53,0.3);
}
.card-image-container {
    position: relative;
    height: 170px;
    overflow: hidden;
    background: var(--surface-high);
}
.card-image-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 56px;
    background: linear-gradient(135deg, var(--surface-high), var(--surface-dim));
}
.card-gradient-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, var(--surface-low) 0%, transparent 60%, rgba(0,0,0,0.3) 100%);
}
.card-match-badge {
    position: absolute;
    top: 10px;
    left: 10px;
    background: rgba(10,10,15,0.8);
    backdrop-filter: blur(8px);
    border-radius: var(--radius-full);
    padding: 3px 10px;
    font-family: var(--font-code);
    font-size: 12px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 4px;
}
.match-high   { color: var(--tertiary); }
.match-medium { color: var(--secondary); }
.match-low    { color: var(--primary); }
.card-delivery-badge {
    position: absolute;
    bottom: 8px;
    left: 10px;
    background: rgba(10,10,15,0.8);
    backdrop-filter: blur(8px);
    border-radius: var(--radius-sm);
    padding: 2px 8px;
    font-size: 12px;
    font-weight: 600;
    color: var(--on-surface);
    display: flex;
    align-items: center;
    gap: 4px;
}
.card-heart {
    position: absolute;
    top: 10px;
    right: 10px;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: rgba(10,10,15,0.75);
    backdrop-filter: blur(8px);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    cursor: pointer;
    transition: transform 0.2s;
}
.card-heart:hover { transform: scale(1.2); }
.card-body {
    padding: 1rem;
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 0.5rem;
}
.card-title-row {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 8px;
}
.card-title {
    font-size: 17px;
    font-weight: 700;
    letter-spacing: -0.01em;
    color: var(--on-surface);
    line-height: 1.3;
}
.card-rating {
    display: inline-flex;
    align-items: center;
    gap: 3px;
    background: rgba(74,225,118,0.12);
    color: var(--tertiary);
    font-size: 13px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: var(--radius-sm);
    white-space: nowrap;
    flex-shrink: 0;
}
.card-meta {
    font-size: 13px;
    color: var(--outline);
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
}
.card-meta-sep { opacity: 0.5; }
.card-tags { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 4px; }
.card-tag {
    background: var(--surface-high);
    color: var(--on-surface-var);
    font-size: 11px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: var(--radius-sm);
}
.card-tag.ai { background: rgba(110,0,190,0.15); border: 1px solid rgba(168,85,247,0.25); color: var(--on-secondary-c); }
.card-tag.match { background: rgba(255,107,53,0.12); border: 1px solid rgba(255,107,53,0.2); color: var(--primary-c); }
.ai-reason {
    background: var(--surface-mid);
    border-radius: var(--radius-md);
    padding: 8px 10px;
    margin-top: 4px;
    display: flex;
    gap: 8px;
    align-items: flex-start;
}
.ai-reason-icon { color: var(--secondary); font-size: 15px; flex-shrink: 0; margin-top: 1px; }
.ai-reason-text { font-size: 12px; color: var(--on-surface-var); line-height: 1.5; }
.ai-reason-label { color: var(--on-secondary-c); font-weight: 700; }
.card-view-btn {
    margin-top: 8px;
    width: 100%;
    padding: 7px;
    border-radius: var(--radius-full);
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    color: var(--on-surface-var);
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s;
    text-align: center;
}
.card-view-btn:hover { background: rgba(255,255,255,0.08); color: var(--on-surface); }

/* ── AI Response Panel ───────────────────────────────────────────────────── */
.ai-response-panel {
    background: var(--surface-low);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    box-shadow: 0 0 40px rgba(168,85,247,0.08);
    position: relative;
    overflow: hidden;
    margin-top: 1rem;
}
.ai-response-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, var(--secondary), var(--primary-c));
    border-radius: 4px 0 0 4px;
}
.ai-response-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
}
.ai-response-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 17px;
    font-weight: 700;
    color: var(--on-surface);
}
.ai-response-title .icon { color: var(--secondary); font-size: 22px; }
.ai-feedback-row {
    display: flex;
    align-items: center;
    gap: 8px;
}
.feedback-btn {
    width: 32px; height: 32px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.08);
    background: var(--surface-mid);
    color: var(--outline);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 17px;
    transition: all 0.15s;
}
.feedback-btn:hover.up   { color: var(--tertiary); border-color: var(--tertiary); background: rgba(74,225,118,0.1); }
.feedback-btn:hover.down { color: var(--error);    border-color: var(--error);    background: rgba(255,180,171,0.1); }
.regen-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--surface-high);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: var(--radius-full);
    color: var(--secondary);
    font-size: 13px;
    font-weight: 700;
    padding: 5px 14px;
    cursor: pointer;
    transition: all 0.15s;
}
.regen-btn:hover { background: var(--surface-highest); }
.ai-response-content {
    background: rgba(14,14,19,0.6);
    border-radius: var(--radius-md);
    padding: 1rem 1.25rem;
    font-size: 14px;
    line-height: 1.75;
    color: var(--on-surface);
}
.ai-response-content strong { color: var(--primary-c); }
.ai-response-content em     { color: var(--on-surface-var); }

/* ── Loading overlay ─────────────────────────────────────────────────────── */
.loading-overlay {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem;
    gap: 1rem;
}
.loading-ring {
    width: 64px; height: 64px;
    border-radius: 50%;
    border: 3px solid rgba(255,255,255,0.08);
    border-top-color: var(--primary-c);
    border-right-color: var(--secondary);
    animation: spin 1s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.loading-text {
    font-size: 15px;
    font-weight: 600;
    color: var(--secondary);
}

/* ── Skeleton shimmer card ───────────────────────────────────────────────── */
.skeleton-card {
    background: var(--surface-low);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: var(--radius-lg);
    overflow: hidden;
    animation: shimmer-pulse 1.8s ease-in-out infinite;
}
@keyframes shimmer-pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.55; }
}
.skeleton-img  { height: 170px; background: var(--surface-highest); }
.skeleton-body { padding: 1rem; display: flex; flex-direction: column; gap: 10px; }
.skeleton-line {
    height: 12px;
    border-radius: var(--radius-full);
    background: var(--surface-high);
}
.skeleton-line.w-3-4 { width: 75%; }
.skeleton-line.w-1-2 { width: 50%; }
.skeleton-line.w-1-3 { width: 33%; }
.skeleton-line.tall  { height: 40px; border-radius: var(--radius-md); }

/* ── Toast ───────────────────────────────────────────────────────────────── */
.toast-container {
    position: fixed;
    bottom: 24px;
    right: 24px;
    z-index: 9998;
    max-width: 360px;
    width: 100%;
}
.toast {
    background: rgba(14,14,19,0.92);
    backdrop-filter: blur(20px);
    border-radius: var(--radius-xl);
    padding: 1rem 1.25rem;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 20px 60px rgba(0,0,0,0.8);
    display: flex;
    flex-direction: column;
    gap: 8px;
    animation: slide-up 0.3s ease;
}
@keyframes slide-up {
    from { transform: translateY(20px); opacity: 0; }
    to   { transform: translateY(0);    opacity: 1; }
}
.toast-row { display: flex; align-items: center; gap: 12px; }
.toast-icon {
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}
.toast-icon.success { background: rgba(34,197,94,0.2);  color: var(--tertiary); }
.toast-icon.error   { background: rgba(239,68,68,0.2);  color: var(--error);    }
.toast-title  { font-size: 14px; font-weight: 700; color: var(--on-surface); }
.toast-body   { font-size: 12px; color: var(--outline); }
.toast-progress {
    height: 3px;
    border-radius: var(--radius-full);
    background: var(--surface-highest);
    overflow: hidden;
}
.toast-progress-bar {
    height: 100%;
    border-radius: var(--radius-full);
    background: linear-gradient(90deg, var(--tertiary), var(--primary-c));
    animation: shrink 4s linear forwards;
}
@keyframes shrink { from { width: 100%; } to { width: 0%; } }

/* ── Sidebar adornments ──────────────────────────────────────────────────── */
.sidebar-logo-area {
    padding: 0.5rem 0 1rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 1rem;
}
.sidebar-history-chip {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: var(--surface-high);
    border-radius: var(--radius-full);
    padding: 4px 10px;
    font-size: 12px;
    color: var(--on-surface-var);
    cursor: pointer;
    margin: 2px;
    border: 1px solid rgba(255,255,255,0.06);
    transition: all 0.15s;
}
.sidebar-history-chip:hover { color: var(--on-surface); background: var(--surface-highest); }

/* ── Divider ─────────────────────────────────────────────────────────────── */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    margin: 1rem 0;
}

/* ── Markdown in response ────────────────────────────────────────────────── */
.ai-markdown h1, .ai-markdown h2, .ai-markdown h3 {
    color: var(--on-surface);
    font-weight: 700;
    letter-spacing: -0.015em;
    margin-top: 1rem;
}
.ai-markdown ul { padding-left: 1.5rem; }
.ai-markdown li::marker { color: var(--primary-c); }
.ai-markdown strong { color: var(--primary-c); }
.ai-markdown em { color: var(--on-surface-var); font-style: italic; }
.ai-markdown code {
    background: var(--surface-dim);
    border-radius: var(--radius-sm);
    padding: 1px 6px;
    font-family: var(--font-code);
    font-size: 12px;
    color: var(--secondary);
}
</style>
"""

st.markdown(DESIGN_CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# NAVBAR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="foodai-navbar">
    <div class="foodai-logo">Food<span>AI</span></div>
    <div class="nav-links">
        <a href="#" class="nav-link active">Discover</a>
        <a href="#" class="nav-link">AI Curations</a>
        <a href="#" class="nav-link">Near Me</a>
        <a href="#" class="nav-link">Trending</a>
    </div>
    <div class="powered-badge">
        ✦ Powered by Gemini
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        return pd.read_csv("data/restaurants.csv")
    except FileNotFoundError:
        return None

@st.cache_data
def get_locations(df):
    locs = sorted(df['location'].dropna().str.title().unique().tolist())
    return ["(All Locations)"] + locs

@st.cache_data
def get_cuisines(df):
    cuisines = set()
    for row in df['cuisines'].dropna():
        for c in row.split(','):
            cuisines.add(c.strip().title())
    return sorted(cuisines)

df = load_data()

if df is None:
    st.markdown("""
    <div style="text-align:center;padding:3rem;">
        <div style="font-size:48px;margin-bottom:1rem;">⚠️</div>
        <div style="font-size:18px;font-weight:700;color:#ef4444;margin-bottom:0.5rem;">Dataset not found</div>
        <div style="font-size:14px;color:#a98a80;">Run <code>python src/ingest.py</code> first to load restaurant data.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

locations = get_locations(df)
all_cuisines = get_cuisines(df)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
if "results"       not in st.session_state: st.session_state.results       = None
if "ai_response"   not in st.session_state: st.session_state.ai_response   = None
if "user_prompt"   not in st.session_state: st.session_state.user_prompt   = None
if "user_prefs"    not in st.session_state: st.session_state.user_prefs    = None
if "show_toast"    not in st.session_state: st.session_state.show_toast    = False
if "toast_type"    not in st.session_state: st.session_state.toast_type    = "success"
if "toast_msg"     not in st.session_state: st.session_state.toast_msg     = ""
if "saved_cards"   not in st.session_state: st.session_state.saved_cards   = set()
if "regen_trigger" not in st.session_state: st.session_state.regen_trigger = 0

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — NEURAL FILTERS
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Sidebar header
    st.markdown("""
    <div class="sidebar-logo-area">
        <div style="font-size:18px;font-weight:800;letter-spacing:-0.02em;">
            Food<span style="color:#ff6b35;">AI</span>
            <span style="font-size:11px;font-weight:700;color:#a98a80;letter-spacing:0.08em;
                         text-transform:uppercase;margin-left:8px;">Filters</span>
        </div>
        <div style="font-size:12px;color:#a98a80;margin-top:4px;">Neural preference matching</div>
    </div>
    """, unsafe_allow_html=True)

    # Recent queries
    st.markdown('<div class="sidebar-section-header">Recent Taste Queries</div>', unsafe_allow_html=True)
    recent_queries = ["Spicy biryani < ₹300", "Vegan brunch", "Rooftop Italian"]
    st.markdown(
        " ".join([
            f'<span class="sidebar-history-chip">🕐 {q}</span>'
            for q in recent_queries
        ]),
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Location
    st.markdown('<div class="sidebar-section-header">📍 Location</div>', unsafe_allow_html=True)
    location_choice = st.selectbox("", locations, label_visibility="collapsed")

    # Cuisine multi-select
    st.markdown('<div class="sidebar-section-header">🍴 Cuisine Match</div>', unsafe_allow_html=True)
    cuisine_choices = st.multiselect(
        "",
        options=all_cuisines,
        default=[],
        placeholder="Select cuisines (blank = any)",
        label_visibility="collapsed"
    )

    # Budget
    st.markdown('<div class="sidebar-section-header">💰 Budget Range (₹ for two)</div>', unsafe_allow_html=True)
    budget_range = st.slider("", min_value=0, max_value=2000, value=(0, 1000), step=50, label_visibility="collapsed")
    st.markdown(
        f'<div style="text-align:center;font-family:var(--font-code, monospace);'
        f'font-size:13px;font-weight:700;color:#ff6b35;margin-top:-8px;">'
        f'₹{budget_range[0]} — ₹{budget_range[1]}</div>',
        unsafe_allow_html=True
    )

    # Minimum rating
    st.markdown('<div class="sidebar-section-header">⭐ Minimum Rating</div>', unsafe_allow_html=True)
    min_rating = st.slider("", 0.0, 5.0, 3.5, step=0.1, label_visibility="collapsed")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Dining options
    st.markdown('<div class="sidebar-section-header">🍽️ Dining Options</div>', unsafe_allow_html=True)
    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1: delivery = st.checkbox("Delivery", value=True)
    with col_d2: dine_in  = st.checkbox("Dine-in")
    with col_d3: takeaway = st.checkbox("Takeaway")

    # Dietary alignment
    st.markdown('<div class="sidebar-section-header">🌿 Dietary</div>', unsafe_allow_html=True)
    col_v1, col_v2 = st.columns(2)
    with col_v1: pure_veg = st.checkbox("Pure Veg")
    with col_v2: halal    = st.checkbox("Halal")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Extra preferences
    st.markdown('<div class="sidebar-section-header">💬 Extra Preferences</div>', unsafe_allow_html=True)
    extras = st.text_area(
        "",
        placeholder="e.g. rooftop, family-friendly, live music, parking...",
        label_visibility="collapsed",
        height=80
    )

    # Submit
    submit = st.button("✦ Find My Restaurants", use_container_width=True)

    # Dataset note
    st.markdown("""
    <div style="margin-top:1rem;padding:0.75rem;background:rgba(255,255,255,0.03);
                border-radius:0.5rem;border:1px solid rgba(255,255,255,0.05);">
        <div style="font-size:11px;color:#a98a80;font-weight:600;text-transform:uppercase;
                    letter-spacing:0.06em;">ℹ️ Dataset Info</div>
        <div style="font-size:12px;color:#71717a;margin-top:4px;">
            Covers Bangalore restaurants from Zomato dataset.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN CONTENT AREA
# ─────────────────────────────────────────────────────────────────────────────

# ── Hero Search Section ───────────────────────────────────────────────────────
st.markdown("""
<div class="hero-section" style="text-align:center;max-width:800px;margin:0 auto 2rem auto;">
    <div class="ai-pill">✦ Multimodal Taste Synthesizer v2.4</div>
    <div class="hero-title">Discover Your Perfect<br>Culinary Match</div>
    <div class="hero-subtitle">Describe any craving in plain language — our AI handles the rest</div>
    <div class="quick-cuisine-chips">
        <span class="cuisine-chip hot">🔥 Biryani</span>
        <span class="cuisine-chip">South Indian</span>
        <span class="cuisine-chip">Artisan Cafe</span>
        <span class="cuisine-chip">Late Night</span>
        <span class="cuisine-chip">Rooftop Dining</span>
        <span class="cuisine-chip">Vegan &amp; Healthy</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# QUERY PROCESSING
# ─────────────────────────────────────────────────────────────────────────────
if submit:
    location_query = "" if location_choice == "(All Locations)" else location_choice.lower()
    cuisine_query  = ", ".join(c.lower() for c in cuisine_choices) if cuisine_choices else ""

    # Build budget label from slider
    mid_budget = (budget_range[0] + budget_range[1]) / 2
    if mid_budget <= 500:
        budget_label = "low"
    elif mid_budget <= 1500:
        budget_label = "medium"
    else:
        budget_label = "high"

    # Use raw numeric range instead of label-based range
    user_prefs = {
        "location":     location_query,
        "cuisine":      cuisine_query,
        "cost_min":     budget_range[0],
        "cost_max":     budget_range[1],
        "min_rating":   min_rating,
        "extras":       extras.strip(),
        "budget_label": f"₹{budget_range[0]}–₹{budget_range[1]} for two",
    }

    filtered = filter_restaurants(df, user_prefs)
    st.session_state.user_prefs = user_prefs
    st.session_state.results = filtered
    st.session_state.ai_response = None   # reset for new search

    if not filtered.empty:
        st.session_state.user_prompt = build_user_prompt(user_prefs, serialize_restaurants(filtered))

        loading_placeholder = st.empty()
        with st.spinner(""):
            loading_placeholder.markdown("""
            <div class="loading-overlay">
                <div class="loading-ring"></div>
                <div class="loading-text">🤖 Consulting AI for the best picks...</div>
            </div>
            """, unsafe_allow_html=True)
            try:
                response = get_recommendation(SYSTEM_PROMPT, st.session_state.user_prompt)
                st.session_state.ai_response = response
                st.session_state.show_toast = True
                st.session_state.toast_type = "success"
                n = len(filtered)
                st.session_state.toast_msg = f"Analyzed {n} restaurants • AI recommendation ready"
            except Exception as e:
                st.session_state.show_toast = True
                st.session_state.toast_type = "error"
                st.session_state.toast_msg = str(e)
        loading_placeholder.empty()
    else:
        st.session_state.show_toast = True
        st.session_state.toast_type = "error"
        st.session_state.toast_msg = "No restaurants found — try adjusting filters"

# ─────────────────────────────────────────────────────────────────────────────
# PROMPT PREVIEW (AI Prompt Display)
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.user_prompt:
    up = st.session_state.user_prefs
    cuisine_display = up.get("cuisine", "any") or "any"
    location_display = up.get("location", "all") or "all"
    budget_display = up.get("budget_label", "any")
    rating_display = up.get("min_rating", 0)
    extras_display = up.get("extras", "None") or "None"

    prompt_html = f"""
    <div class="prompt-card">
        <div class="prompt-card-header">
            <div class="prompt-card-title">
                <span>⬡</span> Gemini Prompt Preview
            </div>
            <span class="prompt-badge">Active</span>
        </div>
        <div class="code-block">
<span class="code-comment">// SYSTEM: AI Restaurant Recommendation Engine</span><br>
<span class="code-keyword">SELECT</span> <span class="code-param">restaurants</span><br>
<span class="code-keyword">WHERE</span> cuisine <span class="code-keyword">IN</span> [<span class="code-value">'{cuisine_display}'</span>]<br>
<span class="code-keyword">AND</span> price_for_two <span class="code-keyword">BETWEEN</span> <span class="code-value">{up.get('cost_min',0)}</span> <span class="code-keyword">AND</span> <span class="code-value">{up.get('cost_max',9999)}</span><br>
<span class="code-keyword">AND</span> rating <span class="code-keyword">&gt;=</span> <span class="code-value">{rating_display}</span><br>
<span class="code-keyword">AND</span> location <span class="code-keyword">=</span> <span class="code-value">'{location_display}'</span><br>
<span class="code-param">REASON_BY_EMBEDDINGS</span>(intent=<span class="code-value">"{extras_display}"</span>)
        </div>
        <div class="prompt-footer">
            <div class="token-count">
                <span class="token-dot"></span> Prompt ready • Filters applied
            </div>
        </div>
    </div>
    """
    with st.expander("🤖 AI Prompt Preview", expanded=False):
        st.markdown(prompt_html, unsafe_allow_html=True)
        st.code(st.session_state.user_prompt, language="text")

# ─────────────────────────────────────────────────────────────────────────────
# AI RESPONSE PANEL
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.ai_response:
    # Regen button callback
    def _regen():
        if st.session_state.user_prompt:
            try:
                response = get_recommendation(SYSTEM_PROMPT, st.session_state.user_prompt)
                st.session_state.ai_response = response
                st.session_state.regen_trigger += 1
            except Exception as e:
                st.error(f"Regeneration failed: {e}")

    st.markdown("""
    <div class="ai-response-panel">
        <div class="ai-response-header">
            <div class="ai-response-title">
                <span class="icon">✦</span>
                Gemini Culinary Insight &amp; Recommendation Summary
            </div>
            <div class="ai-feedback-row">
                <span class="feedback-btn up" title="Helpful">👍</span>
                <span class="feedback-btn down" title="Not helpful">👎</span>
            </div>
        </div>
        <div class="ai-response-content ai-markdown">
    """, unsafe_allow_html=True)

    st.markdown(st.session_state.ai_response)

    st.markdown("</div></div>", unsafe_allow_html=True)

    col_regen, _ = st.columns([1, 4])
    with col_regen:
        if st.button("↻ Regenerate", key="regen_btn"):
            _regen()
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# RESULTS HEADER + CARD GRID
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.results is not None:
    filtered = st.session_state.results

    if filtered.empty:
        st.markdown("""
        <div style="text-align:center;padding:3rem;background:var(--surface-low, #1b1b20);
                    border-radius:1rem;border:1px dashed rgba(255,255,255,0.08);margin-top:1rem;">
            <div style="font-size:48px;margin-bottom:1rem;">🔍</div>
            <div style="font-size:18px;font-weight:700;color:#f4f4f5;margin-bottom:0.5rem;">
                No matches found
            </div>
            <div style="font-size:14px;color:#a98a80;">
                Try lowering minimum rating, broadening cuisine, or selecting 'All Locations'.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        n = len(filtered)

        # Results header
        st.markdown(f"""
        <div class="results-header">
            <div class="results-count">
                <span class="live-dot"></span>
                Found {n} AI-curated spot{"s" if n != 1 else ""}
                <span class="results-meta">• Ranked by rating &amp; relevance</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Sort options
        sort_col, _ = st.columns([2, 5])
        with sort_col:
            sort_by = st.selectbox(
                "Sort by",
                ["Rating (High → Low)", "Price (Low → High)", "Price (High → Low)", "Most Reviews"],
                label_visibility="visible"
            )

        if sort_by == "Rating (High → Low)":
            filtered = filtered.sort_values("aggregate_rating", ascending=False)
        elif sort_by == "Price (Low → High)":
            filtered = filtered.sort_values("cost", ascending=True)
        elif sort_by == "Price (High → Low)":
            filtered = filtered.sort_values("cost", ascending=False)
        elif sort_by == "Most Reviews":
            filtered = filtered.sort_values("votes", ascending=False)

        filtered = filtered.reset_index(drop=True)

        # ── Card Grid ─────────────────────────────────────────────────────────
        FOOD_EMOJIS = ["🍛", "🍜", "🍕", "🥘", "🍱", "🌮", "🍲", "🥗", "🍣", "🥩"]

        # AI reasons (short sentences)
        AI_REASONS = [
            "Top-rated in your area with outstanding flavor profiles.",
            "Exceptional value-to-quality ratio — highly recommended.",
            "Fan favourite for your preferred cuisine style.",
            "Perfect match for your budget and craving profile.",
            "Consistently high ratings with fast delivery.",
            "Popular choice among regulars — great atmosphere.",
            "Known for authentic recipes and generous portions.",
            "Premium dining experience within your price range.",
            "Strong community ratings and fresh ingredients.",
            "Ideal for your specified dining preferences.",
        ]

        cols_per_row = 3
        rows = [
            filtered.iloc[i:i+cols_per_row]
            for i in range(0, len(filtered), cols_per_row)
        ]

        for row_df in rows:
            cols = st.columns(cols_per_row)
            for col, (_, row) in zip(cols, row_df.iterrows()):
                with col:
                    idx = row.name
                    emoji = FOOD_EMOJIS[idx % len(FOOD_EMOJIS)]
                    rating = float(row.get("aggregate_rating", 0))
                    cost = int(row.get("cost", 0))
                    votes = int(row.get("votes", 0))
                    name = str(row.get("name", "Restaurant"))
                    location_ = str(row.get("location", ""))
                    cuisines_ = str(row.get("cuisines", ""))
                    rest_type = str(row.get("rest_type", ""))

                    # Compute mock match score
                    match_score = min(99, max(65, int(rating * 20 + (100 - idx * 3))))
                    if match_score >= 90:
                        match_class, match_icon = "match-high", "⚡"
                    elif match_score >= 80:
                        match_class, match_icon = "match-medium", "✦"
                    else:
                        match_class, match_icon = "match-low", "○"

                    # Heart
                    is_saved = idx in st.session_state.saved_cards
                    heart = "❤️" if is_saved else "🤍"

                    # Cuisine tags (first 3)
                    cuisine_tags = [c.strip() for c in cuisines_.split(",") if c.strip()][:3]
                    tags_html = "".join(
                        f'<span class="card-tag">{t}</span>'
                        for t in cuisine_tags
                    )
                    if rest_type and rest_type != "nan":
                        tags_html += f'<span class="card-tag ai">{rest_type.split(",")[0].strip()}</span>'

                    ai_reason = AI_REASONS[idx % len(AI_REASONS)]

                    card_html = f"""
<div class="restaurant-card">
    <div class="card-image-container">
        <div class="card-image-placeholder">{emoji}</div>
        <div class="card-gradient-overlay"></div>
        <div class="card-match-badge">
            <span class="{match_class}">{match_icon} {match_score}% Match</span>
        </div>
        <div class="card-heart">{heart}</div>
        <div class="card-delivery-badge">⏱ ~25 min • {location_[:15]}</div>
    </div>
    <div class="card-body">
        <div>
            <div class="card-title-row">
                <div class="card-title">{name}</div>
                <div class="card-rating">{'⭐' if rating >= 4.0 else '☆'} {rating:.1f}</div>
            </div>
            <div class="card-meta">
                <span>₹{cost} for two</span>
                <span class="card-meta-sep">•</span>
                <span>{votes:,}+ reviews</span>
            </div>
            <div class="card-tags">{tags_html}</div>
        </div>
        <div class="ai-reason">
            <span class="ai-reason-icon">✦</span>
            <div class="ai-reason-text">
                <span class="ai-reason-label">AI Pick: </span>{ai_reason}
            </div>
        </div>
        <div class="card-view-btn">View Details →</div>
    </div>
</div>
"""
                    st.markdown(card_html, unsafe_allow_html=True)

                    # Save button
                    btn_label = "💔 Unsave" if is_saved else "🤍 Save"
                    if st.button(btn_label, key=f"save_{idx}_{name[:10]}"):
                        if is_saved:
                            st.session_state.saved_cards.discard(idx)
                        else:
                            st.session_state.saved_cards.add(idx)
                        st.rerun()

        # ── Full dataset expander ──────────────────────────────────────────────
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        with st.expander("📋 View full matched restaurant database", expanded=False):
            display_cols = [c for c in ['name', 'location', 'cuisines', 'cost', 'aggregate_rating', 'votes', 'rest_type'] if c in filtered.columns]
            st.dataframe(filtered[display_cols], use_container_width=True, height=280)

# ─────────────────────────────────────────────────────────────────────────────
# EMPTY STATE (no search yet)
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.results is None:
    st.markdown("""
    <div style="text-align:center;padding:4rem 2rem;opacity:0.6;">
        <div style="font-size:56px;margin-bottom:1.5rem;">🍽️</div>
        <div style="font-size:20px;font-weight:700;color:#f4f4f5;margin-bottom:0.5rem;">
            Set your preferences and find your next meal
        </div>
        <div style="font-size:14px;color:#a98a80;">
            Use the filter panel on the left to describe your perfect dining experience.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TOAST NOTIFICATION
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.show_toast:
    t_type  = st.session_state.toast_type
    t_msg   = st.session_state.toast_msg
    t_icon  = "✓" if t_type == "success" else "✕"
    t_title = "Analysis Complete" if t_type == "success" else "Something went wrong"

    st.markdown(f"""
    <div class="toast-container">
        <div class="toast">
            <div class="toast-row">
                <div class="toast-icon {t_type}">{t_icon}</div>
                <div>
                    <div class="toast-title">{t_title}</div>
                    <div class="toast-body">{t_msg}</div>
                </div>
            </div>
            <div class="toast-progress">
                <div class="toast-progress-bar"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Auto-clear after one render cycle
    st.session_state.show_toast = False
