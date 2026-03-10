import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.patches import Rectangle
import numpy as np
from io import BytesIO
st.set_page_config(
    page_title="STEVE HAMENI | Scouting Database",     page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ─── TEAM COLORS ───
TEAM_COLORS = {
    "AFC Telford United":"#1a237e","AFC Totton":"#d32f2f","Aldershot Town":"#e400     "Alfreton Town":"#e4002b","Altrincham":"#e4002b","Bath City":"#333333",
    "Bedford Town":"#1565c0","Boreham Wood":"#333333","Boston United":"#f57f17",     "Brackley Town":"#e4002b","Braintree Town":"#f57f17","Buxton":"#1565c0",
    "Carlisle United":"#1565c0","Chelmsford City":"#880e4f","Chesham United":"#88     "Chester":"#1565c0","Chippenham Town":"#1565c0","Chorley":"#333333",
    "Curzon Ashton":"#1565c0","Dagenham & Redbridge":"#e4002b","Darlington 1883":     "Dorking Wanderers":"#e4002b","Dover Athletic":"#333333","Eastbourne Borough"     "Eastleigh":"#1565c0","Ebbsfleet United":"#e4002b","Enfield Town":"#1565c0",     "Farnborough":"#e4002b","Forest Green Rovers":"#2e7d32","Fylde":"#e4002b",
    "Gateshead":"#1565c0","Halifax Town":"#1565c0","Hampton & Richmond":"#e4002b"     "Hartlepool United":"#1565c0","Hemel Hempstead Town":"#e4002b","Hereford FC":     "Hornchurch":"#e4002b","Horsham":"#f57f17","Kidderminster Harriers":"#e4002b"
    "King's Lynn Town":"#1565c0","Leamington":"#f57f17","Macclesfield Town":"#156     "Maidenhead United":"#333333","Maidstone United":"#f57f17","Marine":"#1565c0"     "Merthyr Town":"#2e7d32","Morecambe":"#e4002b","Oxford City":"#1565c0",
    "Peterborough Sports":"#1565c0","Radcliffe FC":"#333333","Rochdale":"#1565c0"     "Salisbury":"#e4002b","Scarborough Athletic":"#e4002b","Scunthorpe United":"#     "Slough Town":"#f57f17","Solihull Moors":"#f57f17","South Shields":"#2e7d32",     "Southend United":"#1565c0","Southport":"#f57f17","Spennymoor Town":"#333333"     "Sutton United":"#f57f17","Tamworth":"#e4002b","Tonbridge Angels":"#1565c0",     "Torquay United":"#f57f17","Truro City":"#333333","Wealdstone":"#1565c0",
    "Weston-super-Mare":"#2e7d32","Woking":"#e4002b","Worksop Town":"#f57f17",
    "Worthing":"#e4002b","Yeovil Town":"#2e7d32","York City":"#e4002b",
}
# ─── POSITION METRICS ───
POS_METRICS = {
    "Attacker": {
        "bars": [
            ("Non-penalty goals per 90","Non-Pen Goals/90"),
            ("npxG per 90","npxG/90"),
            ("Goal conversion, %","Goal Conversion %"),
            ("Shots per 90","Shots/90"),
            ("Touches in box per 90","Touches in Box/90"),
            ("xA per 90","xA/90"),
            ("Assists per 90","Assists/90"),
            ("Shot assists per 90","Shot Assists/90"),
            ("Successful dribbles, %","Dribble Success %"),
            ("Progressive runs per 90","Progressive Runs/90"),
            ("Accelerations per 90","Accelerations/90"),
            ("Fouls suffered per 90","Fouls Suffered/90"),
        ],
        "scatters": [
            ("Non-penalty goals per 90","npxG per 90","GOAL OUTPUT vs xG"),
            ("Successful dribbles, %","Progressive runs per 90","DRIBBLING & PROG             ("xA per 90","Assists per 90","CREATION & ASSISTS"),
            ("Shots per 90","Touches in box per 90","SHOTS & BOX PRESENCE"),
        ]
    },
    "Midfielder": {
        "bars": [
            ("Progressive passes per 90","Progressive Passes/90"),
            ("Passes per 90","Passes/90"),
            ("Accurate passes, %","Pass Accuracy %"),
            ("Smart passes per 90","Smart Passes/90"),
            ("xA per 90","xA/90"),
            ("Assists per 90","Assists/90"),
            ("pAdj Tkl+Int per 90","pAdj Tackles+Int/90"),
            ("Successful defensive actions per 90","Def. Actions/90"),
            ("PAdj Interceptions","pAdj Interceptions"),
            ("Successful dribbles, %","Dribble Success %"),
            ("Non-penalty goals per 90","Non-Pen Goals/90"),
            ("Accelerations per 90","Accelerations/90"),
        ],
        "scatters": [
            ("Progressive passes per 90","Passes per 90","PASSING & PROGRESSION")             ("pAdj Tkl+Int per 90","Successful defensive actions per 90","DEFENSI             ("xA per 90","Assists per 90","CREATION"),
            ("Successful dribbles, %","Accelerations per 90","CARRYING & PACE"),         ]
    },
    "Defender": {
        "bars": [
            ("pAdj Tkl+Int per 90","pAdj Tackles+Int/90"),
            ("PAdj Interceptions","pAdj Interceptions"),
            ("Shots blocked per 90","Shots Blocked/90"),
            ("Successful defensive actions per 90","Def. Actions/90"),
            ("PAdj Sliding tackles","pAdj Sliding Tackles"),
            ("Aerial duels won, %","Aerial Duel Win %"),
            ("Aerial duels won per 90","Aerial Duels Won/90"),
            ("Passes per 90","Passes/90"),
            ("Accurate passes, %","Pass Accuracy %"),
            ("Progressive passes per 90","Progressive Passes/90"),
            ("Smart passes per 90","Smart Passes/90"),
            ("Accurate long passes, %","Long Pass Accuracy %"),
        ],
        "scatters": [
            ("pAdj Tkl+Int per 90","PAdj Interceptions","TACKLING & INTERCEPTIONS             ("Passes per 90","Accurate passes, %","PASSING VOLUME & ACCURACY"),             ("Progressive passes per 90","Smart passes per 90","BALL PROGRESSION"             ("Aerial duels won, %","Aerial duels won per 90","AERIAL DOMINANCE"),         ]
    },
    "Goalkeeper": {
        "bars": [
            ("Save rate, %","Save Rate %"),
            ("Goals prevented %","Goals Prevented %"),
            ("Conceded goals per 90","Conceded Goals/90"),
            ("Prevented goals per 90","Prevented Goals/90"),
            ("Shots against per 90","Shots Against/90"),
            ("Exits per 90","Exits/90"),
            ("Passes per 90","Passes/90"),
            ("Accurate passes, %","Pass Accuracy %"),
            ("Accurate long passes, %","Long Pass Accuracy %"),
            ("Accurate short / medium passes, %","Short Pass Accuracy"),
        ],
        "scatters": [
            ("Save rate, %","Goals prevented %","SHOT STOPPING"),
            ("Passes per 90","Accurate passes, %","DISTRIBUTION"),
            ("Exits per 90","Conceded goals per 90","SWEEPING & GOALS CONCEDED"),         ]
    }
}
BG = '#1a1a1a'
GRID_DARK = '#2e2e2e'
BAR_BG = '#282828'
TEXT_WHITE = '#ffffff'
TEXT_LIGHT = '#e0e0e0'
def get_bar_color(p):
    if p >= 90: return '#00ff87'     if p >= 80: return '#22c55e'     if p >= 70: return '#84cc16'     if p >= 60: return '#eab308'     if p >= 50: return '#f59e0b'     if p >= 40: return '#f97316'     if p >= 30: return '#ef4444'     return '#dc2626'
def get_accent(team):
    return TEAM_COLORS.get(team, '#e4002b')
@st.cache_data
def load_data():
    df = pd.read_csv("all_players.csv")
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce').fillna(0).astype(int)     return df
def compute_percentile(player_val, series):
    valid = series.dropna()
    if len(valid) == 0 or pd.isna(player_val):
        return None
    return (valid <= player_val).sum() / len(valid) * 100
def draw_page1(player, comp_df, accent):
    pos_group = player['pos_group']
    metrics = POS_METRICS.get(pos_group, {}).get("bars", [])     if not metrics:
        return None
    data = []
    for col, label in metrics:
        if col in comp_df.columns and pd.notna(player.get(col)):
            pct = compute_percentile(player[col], comp_df[col])
            if pct is not None:
                data.append({"label": label, "pct": pct, "val": player[col]})
    if not data:
        return None
fig = plt.figure(figsize=(10, 14), facecolor=BG)
# Header
ax_h = fig.add_axes([0.05, 0.94, 0.9, 0.05])
ax_h.set_xlim(0, 1); ax_h.set_ylim(0, 1); ax_h.axis('off')
t = ax_h.text(0.5, 0.6, player['Player'].upper(), fontsize=36, fontweight='90
                  color=TEXT_WHITE, va='center', ha='center', family='sans-serif'     t.set_path_effects([path_effects.withStroke(linewidth=3, foreground=BG)])
    ax_h.text(0.5, 0.0, f"{player['Position']}  •  {player['Team']}  •  {player['               fontsize=10, fontweight='700', color=accent, va='center', ha='cente
# Placeholders
    for pos_rect, label_text in [([0.08, 0.78, 0.22, 0.13], 'PLAYER\nPHOTO'), ([0         ax = fig.add_axes(pos_rect)
        ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off'); ax.set_facecolor(GRID         ax.add_patch(Rectangle((0,0),1,1, facecolor=GRID_DARK, edgecolor=accent,         ax.text(0.5, 0.5, label_text, ha='center', va='center', fontsize=11, font
# Title
    ax_t = fig.add_axes([0.05, 0.73, 0.9, 0.03])
    ax_t.set_xlim(0,1); ax_t.set_ylim(0,1); ax_t.axis('off')
    tt = ax_t.text(0.5, 0.5, f'PERCENTILE PROFILE — vs {player["league_clean"]} {                    ha='center', va='center', fontsize=13, color=accent, fontweigh     tt.set_path_effects([path_effects.withStroke(linewidth=2, foreground=BG)])
# Bars
    ax_bars = fig.add_axes([0.05, 0.36, 0.9, 0.35])
    ax_bars.set_xlim(-10, 110); ax_bars.set_ylim(-1, len(data)); ax_bars.axis('of     bar_h = 0.65
    for i, row in enumerate(data):
        y = len(data) - 1 - i
        p = row['pct']
        color = get_bar_color(p)
        ax_bars.barh(y, 100, bar_h, color=BAR_BG, edgecolor=GRID_DARK, linewidth=         for gl in [25, 50, 75]:
            ax_bars.plot([gl,gl],[y-bar_h/2, y+bar_h/2], color=GRID_DARK, linewid         ax_bars.barh(y, p, bar_h, color=color, edgecolor=color, linewidth=1.5, zo         mt = ax_bars.text(-1.5, y, row['label'], ha='right', va='center', fontsiz         mt.set_path_effects([path_effects.withStroke(linewidth=2, foreground=BG)]         bbox_p = dict(boxstyle='round,pad=0.3', facecolor=GRID_DARK, edgecolor=co         ax_bars.text(2, y, f"{row['val']:.2f}", ha='left', va='center', fontsize=         pl = ax_bars.text(p+2, y, f"{p:.0f}%", ha='left', va='center', fontsize=9         pl.set_path_effects([path_effects.withStroke(linewidth=2, foreground=BG)]
# Scatter plots (3 on page 1)
    scatters = POS_METRICS.get(pos_group, {}).get("scatters", [])[:3]     scatter_positions = [
        [0.08, 0.18, 0.38, 0.14],
        [0.56, 0.18, 0.38, 0.14],
        [0.32, 0.02, 0.38, 0.14],
    ]
    for idx, (x_col, y_col, title) in enumerate(scatters):
        if idx >= len(scatter_positions): break
        if x_col not in comp_df.columns or y_col not in comp_df.columns: continue         ax = fig.add_axes(scatter_positions[idx]); ax.set_facecolor(GRID_DARK)
        mask = comp_df[x_col].notna() & comp_df[y_col].notna()
        ax.scatter(comp_df.loc[mask, x_col], comp_df.loc[mask, y_col], s=50, alph         if pd.notna(player.get(x_col)) and pd.notna(player.get(y_col)):
            ax.scatter(player[x_col], player[y_col], s=220, color=accent, edgecol         ax.axvline(comp_df[x_col].mean(), color=TEXT_LIGHT, linestyle='--', linew         ax.axhline(comp_df[y_col].mean(), color=TEXT_LIGHT, linestyle='--', linew         xl = x_col.replace('per 90','/90').replace('Successful dribbles, %','Drib         yl = y_col.replace('per 90','/90').replace('Successful defensive actions'         ax.set_xlabel(xl, fontsize=8, fontweight='700', color=TEXT_LIGHT)
        ax.set_ylabel(yl, fontsize=8, fontweight='700', color=TEXT_LIGHT)
        ax.set_title(title, fontsize=10, fontweight='800', color=accent, pad=6)         ax.tick_params(labelsize=6, colors=TEXT_LIGHT)
        for spine in ['top','right']: ax.spines[spine].set_visible(False)
        for spine in ['left','bottom']: ax.spines[spine].set_color('#444')
        ax.grid(True, alpha=0.15, color='#444', linewidth=0.8)
# Footer
ax_f = fig.add_axes([0.05, 0.155, 0.9, 0.015])
ax_f.set_xlim(0,1); ax_f.set_ylim(0,1); ax_f.axis('off')
ax_f.text(0.5, 0.5, '© STEVE HAMENI ANALYTICS', fontsize=9, fontweight='800',
return fig
def draw_page2(player, comp_df, accent):
    pos_group = player['pos_group']
    scatters = POS_METRICS.get(pos_group, {}).get("scatters", [])     if not scatters:
        return None
fig = plt.figure(figsize=(10, 14), facecolor=BG)
# Header
    ax_h = fig.add_axes([0.05, 0.94, 0.9, 0.05])
    ax_h.set_xlim(0,1); ax_h.set_ylim(0,1); ax_h.axis('off')
    t = ax_h.text(0.5, 0.6, player['Player'].upper(), fontsize=36, fontweight='90                   color=TEXT_WHITE, va='center', ha='center')
    t.set_path_effects([path_effects.withStroke(linewidth=3, foreground=BG)])
    ax_h.text(0.5, 0.0, f"IN-DEPTH ANALYSIS  •  {player['league_clean']} 25/26",               fontsize=10, fontweight='700', color=accent, va='center', ha='cente
# 4 scatter plots (or 3 for GK)
    if len(scatters) == 4:
        positions = [
            [0.08, 0.70, 0.40, 0.20],             [0.56, 0.70, 0.40, 0.20],             [0.08, 0.42, 0.40, 0.20],             [0.56, 0.42, 0.40, 0.20],         ]
    else:
        positions = [
            [0.08, 0.65, 0.40, 0.25],             [0.56, 0.65, 0.40, 0.25],             [0.32, 0.35, 0.40, 0.25],         ]
    for idx, (x_col, y_col, title) in enumerate(scatters):
        if idx >= len(positions): break
        if x_col not in comp_df.columns or y_col not in comp_df.columns: continue         ax = fig.add_axes(positions[idx]); ax.set_facecolor(GRID_DARK)
        mask = comp_df[x_col].notna() & comp_df[y_col].notna()
        ax.scatter(comp_df.loc[mask, x_col], comp_df.loc[mask, y_col], s=60, alph         if pd.notna(player.get(x_col)) and pd.notna(player.get(y_col)):
            ax.scatter(player[x_col], player[y_col], s=250, color=accent, edgecol         ax.axvline(comp_df[x_col].mean(), color=TEXT_LIGHT, linestyle='--', linew         ax.axhline(comp_df[y_col].mean(), color=TEXT_LIGHT, linestyle='--', linew         xl = x_col.replace('per 90','/90').replace('Successful dribbles, %','Drib         yl = y_col.replace('per 90','/90').replace('Successful defensive actions'         ax.set_xlabel(xl, fontsize=9, fontweight='700', color=TEXT_LIGHT)
        ax.set_ylabel(yl, fontsize=9, fontweight='700', color=TEXT_LIGHT)
        ax.set_title(title, fontsize=12, fontweight='800', color=accent, pad=8)         ax.tick_params(labelsize=7, colors=TEXT_LIGHT)
        for spine in ['top','right']: ax.spines[spine].set_visible(False)
        for spine in ['left','bottom']: ax.spines[spine].set_color('#444')
        ax.grid(True, alpha=0.15, color='#444', linewidth=0.8)
# Personal details box
y_box = 0.08 if len(scatters) == 4 else 0.05
h_box = 0.28 if len(scatters) == 4 else 0.25
ax_det = fig.add_axes([0.15, y_box, 0.7, h_box])
ax_det.set_xlim(0,1); ax_det.set_ylim(0,1); ax_det.axis('off'); ax_det.set_fa ax_det.add_patch(Rectangle((0,0),1,1, facecolor=GRID_DARK, edgecolor=accent, ax_det.text(0.5, 0.92, 'PERSONAL DETAILS', fontsize=12, fontweight='800', col
details_left = f"Age: {player['Age']}\nNationality: {player.get('Birth countr details_right = f"Club: {player['Team']}\nLeague: {player['league_clean']}\nT ax_det.text(0.08, 0.72, details_left, fontsize=10, fontweight='600', color=TE ax_det.text(0.55, 0.72, details_right, fontsize=10, fontweight='600', color=T
sig_bbox = dict(boxstyle='round,pad=0.35', facecolor=BG, edgecolor=accent, li ax_det.text(0.5, 0.08, '© STEVE HAMENI', fontsize=9, fontweight='900', color=
return fig
def fig_to_bytes(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=200, bbox_inches='tight', facecolor=BG, ed     plt.close(fig)
    buf.seek(0)
    return buf.getvalue()
# ─── CUSTOM CSS ───
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;600;700
.stApp { background-color: #0a0a0a; } section[data-testid="stSidebar"] { background-color: #111111; } section[data-testid="stSidebar"] .stMarkdown p, section[data-testid="stSidebar"] .stMarkdown label, section[data-testid="stSidebar"] label { color: #cccccc !important; }
    .brand-header {
        font-family: 'Oswald', sans-serif;         font-size: 28px;
        font-weight: 900;
        letter-spacing: 4px;
        text-transform: uppercase;
        color: #ffffff;
        text-align: center;
        padding: 16px 0 4px;
    }
    .brand-header span { color: #e4002b; }     .brand-sub {
        text-align: center;
        font-size: 11px;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #888;
        margin-bottom: 20px;
    }
    .player-card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 8px;
        cursor: pointer;
        transition: all 0.15s;
    }
    .player-card:hover { background: #222; border-color: #444; }
    .player-name {
        font-family: 'Oswald', sans-serif;
        font-size: 16px;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        color: #fff;
    }
    .player-meta { color: #888; font-size: 12px; margin-top: 3px; }
    .pos-badge {
        display: inline-block;
        background: #2a2a2a;
        padding: 1px 8px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-right: 6px;
    }
    .download-btn {
        text-align: center;
        margin: 10px 0;
    }
    div[data-testid="stImage"] { display: flex; justify-content: center; } </style>
""", unsafe_allow_html=True)
# ─── LOAD DATA ───
df = load_data()
# ─── SIDEBAR ───
with st.sidebar:
    st.markdown('<div class="brand-header">STEVE <span>HAMENI</span></div>', unsa     st.markdown('<div class="brand-sub">Scouting Database · NL & NL N/S 25/26</di
league = st.selectbox("League", ["All"] + sorted(df['league_clean'].unique(). pos_group = st.selectbox("Position", ["All"] + sorted(df['pos_group'].unique(
    filtered = df.copy()
    if league != "All":
        filtered = filtered[filtered['league_clean'] == league]     if pos_group != "All":
        filtered = filtered[filtered['pos_group'] == pos_group]
team = st.selectbox("Team", ["All"] + sorted(filtered['Team'].unique().tolist if team != "All":
filtered = filtered[filtered['Team'] == team]
    search = st.text_input("Search player", "")
    if search:
        filtered = filtered[filtered['Player'].str.contains(search, case=False, n
st.markdown(f"**{len(filtered)}** players")
# ─── MAIN ───
if 'selected_id' not in st.session_state:     st.session_state.selected_id = None
# Player list
col_list, col_visual = st.columns([1, 2])
with col_list:
    st.markdown(f"#####  Players ({len(filtered)})")
    for idx, row in filtered.head(200).iterrows():
        accent = get_accent(row['Team'])
        pos_short = row['pos_group'][:3].upper()
        if st.button(
            f"**{row['Player']}** — {row['Team']} · {pos_short} · Age {row['Age']             key=f"player_{idx}",
            use_container_width=True
        ):
            st.session_state.selected_id = idx
with col_visual:
    if st.session_state.selected_id is not None and st.session_state.selected_id         player = df.loc[st.session_state.selected_id]
        accent = get_accent(player['Team'])
# Get comparison pool
comp = df[(df['pos_group'] == player['pos_group']) & (df['league_clean'] 
st.markdown(f"### {player['Player']} — {player['Team']}")
# Draw Page 1
        fig1 = draw_page1(player, comp, accent)
        if fig1:
            img1 = fig_to_bytes(fig1)
            st.image(img1, use_container_width=True)
            st.download_button(" Download Page 1", img1, f"{player['Player'].re
# Draw Page 2
fig2 = draw_page2(player, comp, accent) if fig2:
            img2 = fig_to_bytes(fig2)
            st.image(img2, use_container_width=True)
            st.download_button(" Download Page 2", img2, f"{player['Player'].re     else:
        st.markdown("""
        <div style="text-align:center;padding:100px 20px;color:#555">
            <div style="font-size:48px;opacity:0.3"></div>
            <p style="font-size:14px;letter-spacing:2px;text-transform:uppercase;                 Select a player to view their scouting report
            </p>
        </div>
        """, unsafe_allow_html=True)
