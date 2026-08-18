
import streamlit as st
from datetime import date, datetime, timedelta, timezone
from supabase import create_client, Client

# --------------------------------------------------
# GRUNDEINSTELLUNGEN
# --------------------------------------------------

st.set_page_config(
    page_title="Stani Performance",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------
# SUPABASE
# --------------------------------------------------

@st.cache_resource
def init_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase: Client = init_supabase()

# --------------------------------------------------
# DESIGN
# --------------------------------------------------

st.markdown(
    """
    <style>
    :root {
        --bg: #07101d;
        --bg-soft: #0a1526;
        --card: rgba(15, 28, 47, 0.88);
        --card-strong: rgba(18, 34, 57, 0.96);
        --line: rgba(148, 163, 184, 0.14);
        --line-strong: rgba(148, 163, 184, 0.22);
        --text: #f8fafc;
        --muted: #94a3b8;
        --green: #34d399;
        --green-soft: rgba(52, 211, 153, 0.14);
        --yellow: #fbbf24;
        --red: #fb7185;
        --blue: #38bdf8;
        --purple: #a78bfa;
    }

    .stApp {
        background:
            radial-gradient(circle at 12% -10%, rgba(56, 189, 248, 0.13), transparent 28rem),
            radial-gradient(circle at 96% 4%, rgba(167, 139, 250, 0.11), transparent 26rem),
            linear-gradient(180deg, #081322 0%, var(--bg) 45%, #060d18 100%);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: rgba(7, 16, 29, 0.70);
        backdrop-filter: blur(14px);
    }

    .block-container {
        max-width: 1180px;
        padding-top: 1.35rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3, h4, p, label, span {
        color: var(--text);
    }

    /* Header */
    .mission-header {
        padding: 0.15rem 0 1.05rem 0;
    }

    .mission-kicker {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        color: #bae6fd;
        background: rgba(56, 189, 248, 0.10);
        border: 1px solid rgba(56, 189, 248, 0.18);
        border-radius: 999px;
        padding: 0.34rem 0.68rem;
        font-size: 0.72rem;
        font-weight: 850;
        letter-spacing: 0.11em;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
    }

    .mission-title {
        font-size: clamp(2.2rem, 6vw, 4.25rem);
        line-height: 0.98;
        font-weight: 950;
        letter-spacing: -0.055em;
        margin: 0;
    }

    .mission-subtitle {
        color: var(--muted);
        font-size: 1rem;
        margin-top: 0.62rem;
    }

    /* Hero */
    .hero-card {
        position: relative;
        overflow: hidden;
        background:
            radial-gradient(circle at 88% 18%, rgba(56, 189, 248, 0.16), transparent 14rem),
            linear-gradient(135deg, rgba(19, 38, 64, 0.98), rgba(9, 21, 37, 0.98));
        border: 1px solid var(--line-strong);
        border-radius: 28px;
        padding: 1.35rem 1.45rem;
        margin: 0.35rem 0 1.15rem 0;
        box-shadow: 0 22px 60px rgba(0, 0, 0, 0.26);
    }

    .hero-card:before {
        content: "";
        position: absolute;
        width: 220px;
        height: 220px;
        border-radius: 50%;
        background: rgba(167, 139, 250, 0.10);
        filter: blur(12px);
        right: -90px;
        bottom: -120px;
    }

    .hero-row {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1.4rem;
        flex-wrap: wrap;
        z-index: 1;
    }

    .hero-copy {
        flex: 1 1 360px;
    }

    .hero-label {
        color: #93c5fd;
        font-size: 0.76rem;
        font-weight: 850;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    .hero-status {
        font-size: clamp(1.25rem, 3vw, 1.7rem);
        font-weight: 900;
        margin-top: 0.42rem;
        letter-spacing: -0.02em;
    }

    .hero-meta {
        color: var(--muted);
        margin-top: 0.45rem;
        font-size: 0.9rem;
    }

    .hero-chips {
        display: flex;
        gap: 0.45rem;
        flex-wrap: wrap;
        margin-top: 0.85rem;
    }

    .hero-chip {
        color: #dbeafe;
        background: rgba(148, 163, 184, 0.10);
        border: 1px solid rgba(148, 163, 184, 0.14);
        border-radius: 999px;
        padding: 0.34rem 0.64rem;
        font-size: 0.78rem;
        font-weight: 750;
    }

    .score-ring {
        --score: 0;
        width: 132px;
        height: 132px;
        border-radius: 50%;
        display: grid;
        place-items: center;
        flex: 0 0 132px;
        background:
            radial-gradient(circle at center, #0b1829 57%, transparent 58%),
            conic-gradient(var(--green) calc(var(--score) * 1%), rgba(148, 163, 184, 0.13) 0);
        box-shadow:
            inset 0 0 0 1px rgba(148, 163, 184, 0.10),
            0 18px 34px rgba(0, 0, 0, 0.24);
    }

    .score-value {
        text-align: center;
        font-size: 2.15rem;
        line-height: 0.95;
        font-weight: 950;
        letter-spacing: -0.055em;
    }

    .score-value small {
        display: block;
        color: var(--muted);
        font-size: 0.68rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-top: 0.3rem;
        font-weight: 800;
    }

    /* Abschnittsüberschriften */
    .section-title {
        font-size: 1.05rem;
        font-weight: 900;
        margin: 0.35rem 0 0.72rem 0;
        letter-spacing: -0.01em;
    }

    .section-note {
        color: var(--muted);
        font-size: 0.82rem;
        margin-top: -0.45rem;
        margin-bottom: 0.75rem;
    }

    /* Tabs als moderne Pillen */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.45rem;
        background: rgba(15, 28, 47, 0.60);
        border: 1px solid var(--line);
        padding: 0.35rem;
        border-radius: 16px;
        margin-bottom: 0.9rem;
    }

    .stTabs [data-baseweb="tab"] {
        height: 2.65rem;
        padding: 0 1rem;
        border-radius: 12px;
        color: var(--muted);
        font-weight: 800;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(56, 189, 248, 0.11);
        color: #e0f2fe !important;
    }

    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }

    /* Inputs dunkel */
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        background: rgba(15, 28, 47, 0.92) !important;
        border-color: var(--line-strong) !important;
        border-radius: 14px !important;
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="select"] span {
        color: var(--text) !important;
    }

    div[data-testid="stWidgetLabel"] p {
        color: #cbd5e1 !important;
        font-weight: 750;
    }

    /* Checkboxen als Karten */
    div[data-testid="stCheckbox"] {
        background: rgba(15, 28, 47, 0.60);
        border: 1px solid rgba(148, 163, 184, 0.10);
        border-radius: 14px;
        padding: 0.48rem 0.62rem;
        margin-bottom: 0.46rem;
        transition: transform 0.16s ease, border-color 0.16s ease, background 0.16s ease;
    }

    div[data-testid="stCheckbox"]:hover {
        transform: translateY(-1px);
        background: rgba(18, 34, 57, 0.88);
        border-color: rgba(56, 189, 248, 0.24);
    }

    /* Container / Metrics */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: var(--line) !important;
        background: linear-gradient(180deg, rgba(15, 28, 47, 0.72), rgba(9, 20, 35, 0.62));
        border-radius: 20px !important;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(180deg, rgba(18, 34, 57, 0.80), rgba(12, 24, 41, 0.80));
        border: 1px solid var(--line) !important;
        border-radius: 18px;
        padding: 0.55rem 0.7rem;
        min-height: 104px;
    }

    div[data-testid="stMetricLabel"] {
        color: var(--muted) !important;
        font-weight: 750;
    }

    div[data-testid="stMetricValue"] {
        font-weight: 950;
        letter-spacing: -0.045em;
    }

    /* Button */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #0ea5e9, #22c55e);
        border: 0;
        border-radius: 15px;
        font-weight: 900;
        min-height: 3.1rem;
        box-shadow: 0 12px 28px rgba(14, 165, 233, 0.16);
    }

    div.stButton > button[kind="primary"]:hover {
        filter: brightness(1.06);
        transform: translateY(-1px);
    }

    /* Progress */
    div[data-testid="stProgress"] > div > div {
        background: rgba(148, 163, 184, 0.12);
        border-radius: 999px;
    }

    div[data-testid="stProgress"] > div > div > div > div {
        background: linear-gradient(90deg, #38bdf8, #34d399);
        border-radius: 999px;
    }

    /* Wochenkalender */
    .week-grid {
        display: grid;
        grid-template-columns: repeat(7, minmax(0, 1fr));
        gap: 0.62rem;
        margin-top: 0.7rem;
        margin-bottom: 0.95rem;
    }

    .day-card {
        position: relative;
        overflow: hidden;
        border-radius: 18px;
        border: 1px solid var(--line);
        padding: 0.85rem;
        min-height: 126px;
        background: rgba(15, 28, 47, 0.72);
    }

    .day-card:after {
        content: "";
        position: absolute;
        left: 0;
        right: 0;
        bottom: 0;
        height: 3px;
        background: rgba(148, 163, 184, 0.15);
    }

    .day-good {
        background: linear-gradient(145deg, rgba(52, 211, 153, 0.16), rgba(15, 28, 47, 0.88));
        border-color: rgba(52, 211, 153, 0.28);
    }

    .day-good:after { background: var(--green); }

    .day-mid {
        background: linear-gradient(145deg, rgba(251, 191, 36, 0.14), rgba(15, 28, 47, 0.88));
        border-color: rgba(251, 191, 36, 0.26);
    }

    .day-mid:after { background: var(--yellow); }

    .day-low {
        background: linear-gradient(145deg, rgba(251, 113, 133, 0.13), rgba(15, 28, 47, 0.88));
        border-color: rgba(251, 113, 133, 0.24);
    }

    .day-low:after { background: var(--red); }

    .day-empty {
        background: rgba(15, 23, 42, 0.46);
        opacity: 0.78;
    }

    .day-today {
        outline: 2px solid rgba(56, 189, 248, 0.55);
        outline-offset: 2px;
    }

    .day-name {
        color: var(--muted);
        font-size: 0.70rem;
        font-weight: 900;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .day-score {
        font-size: 1.5rem;
        font-weight: 950;
        margin: 0.28rem 0 0.34rem 0;
        letter-spacing: -0.035em;
    }

    .day-detail {
        color: #cbd5e1;
        font-size: 0.72rem;
        line-height: 1.35;
    }

    .day-subdetail {
        color: var(--muted);
        font-size: 0.68rem;
        margin-top: 0.18rem;
    }

    /* Radio */
    div[data-testid="stRadio"] > div {
        gap: 0.45rem;
    }

    div[data-testid="stRadio"] label {
        background: rgba(15, 28, 47, 0.65);
        border: 1px solid var(--line);
        border-radius: 999px;
        padding: 0.30rem 0.55rem;
    }

    /* Alerts */
    div[data-testid="stAlert"] {
        border-radius: 16px;
    }

    @media (max-width: 950px) {
        .week-grid {
            grid-template-columns: repeat(4, minmax(0, 1fr));
        }
    }

    @media (max-width: 700px) {
        .block-container {
            padding-left: 0.85rem;
            padding-right: 0.85rem;
            padding-top: 0.9rem;
        }

        .hero-card {
            padding: 1.15rem;
            border-radius: 22px;
        }

        .score-ring {
            width: 112px;
            height: 112px;
            flex-basis: 112px;
        }

        .score-value {
            font-size: 1.85rem;
        }

        .week-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        div[data-testid="stMetric"] {
            min-height: 92px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# TRAININGSPLAN
# --------------------------------------------------

trainingsplan = {
    "Training A": [
        ("Klimmzüge Obergriff", "4 × 5–8"),
        ("Dips", "4 × 6–10"),
        ("Bulgarian Split Squats", "4 × 8–12 / Bein"),
        ("Ring Rows", "3 × 8–15"),
        ("Rumänisches Kreuzheben", "3 × 8–12"),
        ("Ring Curls", "3 × 10–15"),
        ("Hängendes Knie-/Beinheben", "3 × 10–15"),
    ],
    "Training B": [
        ("Chin-ups Untergriff", "4 × 6–10"),
        ("Schulterdrücken Hantel/SZ", "4 × 6–10"),
        ("Goblet Squats / Weste", "4 × 10–15"),
        ("Liegestütze", "3 × 8–15"),
        ("Ring Archer Rows", "3 × 6–10 / Seite"),
        ("Seitheben mit Hanteln", "3 × 12–20"),
        ("Ring Triceps Extensions", "3 × 10–15"),
    ],
    "Training C": [
        ("Dips", "3 × 6–10"),
        ("Enge Klimmzüge Obergriff", "3 × 6–10"),
        ("Reverse Lunges", "4 × 8–12 / Bein"),
        ("Normale Ring Rows", "3 × 8–12"),
        ("Pike Push-ups", "3 × 6–12"),
        ("Rumänisches Kreuzheben SZ", "3 × 8–12"),
        ("SZ-Curls / Hammer Curls", "3 × 8–12"),
    ],
}

# --------------------------------------------------
# DATENBANK
# --------------------------------------------------

def load_day(selected_date):
    response = (
        supabase
        .table("daily_tracker")
        .select("*")
        .eq("date", str(selected_date))
        .execute()
    )
    return response.data[0] if response.data else None


def save_day(data):
    (
        supabase
        .table("daily_tracker")
        .upsert(data)
        .execute()
    )


def load_all_days():
    response = (
        supabase
        .table("daily_tracker")
        .select("*")
        .order("date")
        .execute()
    )
    return response.data or []


# --------------------------------------------------
# SCORE / STATISTIK-HILFEN
# --------------------------------------------------

habit_fields = [
    "calorie_deficit",
    "fixed_meals",
    "no_snacks",
    "no_calorie_drinks",
    "no_alcohol",
    "movement_30",
    "protein_goal",
    "sleep_goal",
    "reading_30",
    "trading_30",
]

exercise_fields = [f"exercise_{i}" for i in range(1, 8)]


def calculate_score(day):
    completed = sum(bool(day.get(field, False)) for field in habit_fields)
    total = len(habit_fields)

    if day.get("training_day", "Ruhetag") != "Ruhetag":
        completed += sum(bool(day.get(field, False)) for field in exercise_fields)
        total += len(exercise_fields)

    return completed / total if total else 0


def average_score(days):
    return (
        sum(calculate_score(day) for day in days) / len(days)
        if days
        else 0
    )


def count_training(days):
    return sum(
        1
        for day in days
        if day.get("training_day", "Ruhetag") != "Ruhetag"
    )


def calculate_streak(days, minimum_score=0.80):
    if not days:
        return 0, 0

    success_by_date = {
        date.fromisoformat(day["date"]): calculate_score(day) >= minimum_score
        for day in days
    }

    longest = 0
    running = 0
    previous_date = None

    for current_date in sorted(success_by_date):
        successful = success_by_date[current_date]

        if successful and (
            previous_date is None
            or current_date == previous_date + timedelta(days=1)
        ):
            running += 1
        elif successful:
            running = 1
        else:
            running = 0

        longest = max(longest, running)
        previous_date = current_date

    current = 0
    check_date = date.today()

    while success_by_date.get(check_date, False):
        current += 1
        check_date -= timedelta(days=1)

    return current, longest


def status_for_score(score):
    if score >= 1:
        return "🏆 Perfekter Tag"
    if score >= 0.80:
        return "🔥 Stark unterwegs"
    if score >= 0.50:
        return "💪 Gute Basis"
    return "🎯 Dranbleiben"


def short_training_name(training_day):
    mapping = {
        "Training A": "💪 A",
        "Training B": "💪 B",
        "Training C": "💪 C",
        "Ruhetag": "🌙 Ruhe",
    }
    return mapping.get(training_day, "—")


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="mission-header">
        <div class="mission-kicker">● STANI · PERSONAL PERFORMANCE SYSTEM</div>
        <div class="mission-title">⚡ STANI PERFORMANCE</div>
        <div class="mission-subtitle">
            Konstanz • Fokus • Fortschritt · Training • Ernährung • Gesundheit • Lernen • Trading
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

hero_placeholder = st.empty()

# --------------------------------------------------
# DATUM / SCHICHT
# --------------------------------------------------

top1, top2 = st.columns(2, gap="medium")

with top1:
    datum = st.date_input("📅 Datum", value=date.today())

saved = load_day(datum)

shift_options = ["Frühschicht", "Spätschicht", "Nachtschicht", "Frei"]
training_options = ["Ruhetag", "Training A", "Training B", "Training C"]

default_shift = saved.get("shift", "Frühschicht") if saved else "Frühschicht"
if default_shift not in shift_options:
    default_shift = "Frühschicht"

default_training = saved.get("training_day", "Ruhetag") if saved else "Ruhetag"
if default_training not in training_options:
    default_training = "Ruhetag"

with top2:
    schicht = st.selectbox(
        "🏭 Meine Schicht",
        shift_options,
        index=shift_options.index(default_shift),
        key=f"{datum}_shift",
    )

if saved:
    st.caption("💾 Für dieses Datum gibt es bereits einen gespeicherten Eintrag.")
else:
    st.caption("✨ Neuer Tag – deine Änderungen werden erst mit „Tag speichern“ dauerhaft.")

# --------------------------------------------------
# TABS
# --------------------------------------------------

tab_daily, tab_progress = st.tabs(["✅ Tagesmission", "📊 Fortschritt"])

# --------------------------------------------------
# TAB 1: TAGESMISSION
# --------------------------------------------------

with tab_daily:
    st.markdown('<div class="section-title">🏆 Tages-Check</div>', unsafe_allow_html=True)

    def default_value(field):
        return bool(saved.get(field, False)) if saved else False

    daily_values = {}

    nutrition_fields = [
        ("calorie_deficit", "🔥 Kaloriendefizit"),
        ("fixed_meals", "🍽️ Feste Mahlzeiten"),
        ("no_snacks", "🚫 Keine unnötigen Snacks"),
        ("no_calorie_drinks", "🥤 Keine Kalorien getrunken"),
        ("no_alcohol", "🍺 Kein Alkohol"),
        ("protein_goal", "🥩 Proteinziel"),
    ]

    health_fields = [
        ("movement_30", "🚶 30 Minuten Bewegung"),
        ("sleep_goal", "😴 Schlafziel"),
    ]

    growth_fields = [
        ("reading_30", "📚 30 Minuten gelesen"),
        ("trading_30", "📈 30 Minuten Trading"),
    ]

    daily_col1, daily_col2, daily_col3 = st.columns([1.35, 1, 1], gap="medium")

    with daily_col1:
        with st.container(border=True):
            st.markdown("#### 🥗 Ernährung")
            st.caption("Die Basis für Fettverlust & Muskelaufbau")
            for field, label in nutrition_fields:
                daily_values[field] = st.checkbox(
                    label,
                    value=default_value(field),
                    key=f"{datum}_{field}",
                )

    with daily_col2:
        with st.container(border=True):
            st.markdown("#### ❤️ Gesundheit")
            st.caption("Bewegung & Regeneration")
            for field, label in health_fields:
                daily_values[field] = st.checkbox(
                    label,
                    value=default_value(field),
                    key=f"{datum}_{field}",
                )

    with daily_col3:
        with st.container(border=True):
            st.markdown("#### 🚀 Wachstum")
            st.caption("Jeden Tag ein Stück weiter")
            for field, label in growth_fields:
                daily_values[field] = st.checkbox(
                    label,
                    value=default_value(field),
                    key=f"{datum}_{field}",
                )

    st.markdown('<div class="section-title">💪 Training</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-note">Wähle deinen Trainingstag – ein Ruhetag senkt deinen Performance Score nicht.</div>', unsafe_allow_html=True)

    training = st.radio(
        "Was steht heute an?",
        training_options,
        index=training_options.index(default_training),
        horizontal=True,
        key=f"{datum}_training",
    )

    training_values = []

    if training != "Ruhetag":
        with st.container(border=True):
            st.markdown(f"#### {training}")

            for index, (exercise, reps) in enumerate(trainingsplan[training]):
                field = f"exercise_{index + 1}"
                old_value = (
                    bool(saved.get(field, False))
                    if saved and saved.get("training_day") == training
                    else False
                )

                ex_col1, ex_col2 = st.columns([4, 1], vertical_alignment="center")
                with ex_col1:
                    done = st.checkbox(
                        exercise,
                        value=old_value,
                        key=f"{datum}_{training}_{field}",
                    )
                with ex_col2:
                    st.markdown(f"**{reps}**")

                training_values.append(done)
    else:
        st.info("🌙 Ruhetag – Training wird heute nicht negativ in deinen Score eingerechnet.")
        training_values = [False] * 7

    completed_daily = sum(daily_values.values())
    total_daily = len(daily_values)

    if training != "Ruhetag":
        completed_training = sum(training_values)
        total_training = len(training_values)
    else:
        completed_training = 0
        total_training = 0

    completed_total = completed_daily + completed_training
    total_tasks = total_daily + total_training
    progress = completed_total / total_tasks if total_tasks else 0
    mission_score = round(progress * 100)

    st.markdown('<div class="section-title">⚡ Dein Tagesstand</div>', unsafe_allow_html=True)

    score_col1, score_col2, score_col3 = st.columns(3, gap="medium")
    with score_col1:
        st.metric("Performance Score", f"{mission_score}/100", border=True)
    with score_col2:
        st.metric("Erledigt", f"{completed_total}/{total_tasks}", border=True)
    with score_col3:
        st.metric("Status", status_for_score(progress), border=True)

    st.progress(progress)

    if st.button(
        "💾 TAG SPEICHERN",
        type="primary",
        width="stretch",
    ):
        data = {
            "date": str(datum),
            "shift": schicht,
            "training_day": training,
            "calorie_deficit": daily_values["calorie_deficit"],
            "fixed_meals": daily_values["fixed_meals"],
            "no_snacks": daily_values["no_snacks"],
            "no_calorie_drinks": daily_values["no_calorie_drinks"],
            "no_alcohol": daily_values["no_alcohol"],
            "movement_30": daily_values["movement_30"],
            "protein_goal": daily_values["protein_goal"],
            "sleep_goal": daily_values["sleep_goal"],
            "reading_30": daily_values["reading_30"],
            "trading_30": daily_values["trading_30"],
            "exercise_1": training_values[0],
            "exercise_2": training_values[1],
            "exercise_3": training_values[2],
            "exercise_4": training_values[3],
            "exercise_5": training_values[4],
            "exercise_6": training_values[5],
            "exercise_7": training_values[6],
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

        try:
            save_day(data)
            st.success("✅ Tag dauerhaft gespeichert.")
            st.rerun()
        except Exception as exc:
            st.error("Speichern fehlgeschlagen.")
            st.exception(exc)

# Hero wird nach der Score-Berechnung oben an seinem Platz gerendert.
remaining_tasks = max(total_tasks - completed_total, 0)
remaining_text = "Alles geschafft – Tag komplett!" if remaining_tasks == 0 else f"{remaining_tasks} Aufgaben noch offen"

with hero_placeholder.container():
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-row">
                <div class="hero-copy">
                    <div class="hero-label">Performance Score · {datum.strftime("%d.%m.%Y")}</div>
                    <div class="hero-status">{status_for_score(progress)}</div>
                    <div class="hero-meta">{remaining_text}</div>
                    <div class="hero-chips">
                        <span class="hero-chip">🏭 {schicht}</span>
                        <span class="hero-chip">{short_training_name(training)} {training if training != "Ruhetag" else ""}</span>
                        <span class="hero-chip">✅ {completed_total}/{total_tasks} erledigt</span>
                    </div>
                </div>
                <div class="score-ring" style="--score:{mission_score};">
                    <div class="score-value">{mission_score}<small>von 100</small></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# TAB 2: FORTSCHRITT
# --------------------------------------------------

with tab_progress:
    all_days = load_all_days()
    today = date.today()

    start_week = today - timedelta(days=today.weekday())
    end_week = start_week + timedelta(days=6)
    start_month = today.replace(day=1)
    start_year = today.replace(month=1, day=1)

    def days_between(start_date, end_date):
        return [
            day
            for day in all_days
            if start_date <= date.fromisoformat(day["date"]) <= end_date
        ]

    week_days = days_between(start_week, today)
    month_days = days_between(start_month, today)
    year_days = days_between(start_year, today)

    week_score = average_score(week_days)
    month_score = average_score(month_days)
    year_score = average_score(year_days)

    st.markdown('<div class="section-title">📈 Überblick</div>', unsafe_allow_html=True)

    stat1, stat2, stat3 = st.columns(3, gap="medium")
    with stat1:
        st.metric("Diese Woche", f"{week_score:.0%}", border=True)
    with stat2:
        st.metric("Dieser Monat", f"{month_score:.0%}", border=True)
    with stat3:
        st.metric("Dieses Jahr", f"{year_score:.0%}", border=True)

    # --------------------------------------------------
    # WOCHENKALENDER
    # --------------------------------------------------

    st.markdown('<div class="section-title">🗓️ Deine Woche</div>', unsafe_allow_html=True)

    weekdays = ["MO", "DI", "MI", "DO", "FR", "SA", "SO"]
    saved_by_date = {
        date.fromisoformat(day["date"]): day
        for day in all_days
    }

    week_cards = []

    for index in range(7):
        current_date = start_week + timedelta(days=index)
        day = saved_by_date.get(current_date)

        if day:
            day_score = calculate_score(day)
            score_pct = round(day_score * 100)

            if day_score >= 0.80:
                css_class = "day-good"
                dot = "🟢"
            elif day_score >= 0.50:
                css_class = "day-mid"
                dot = "🟡"
            else:
                css_class = "day-low"
                dot = "🔴"

            detail = short_training_name(day.get("training_day", "Ruhetag"))
            subdetail = f"🏭 {day.get('shift', '—')}"
            score_text = f"{score_pct}%"
        else:
            css_class = "day-empty"
            dot = "⚪"
            detail = "Noch kein Eintrag"
            subdetail = "—"
            score_text = "–"

        if current_date > today:
            css_class = "day-empty"
            dot = "⚪"
            detail = "Noch offen"
            subdetail = "—"
            score_text = "–"

        if current_date == today:
            css_class += " day-today"

        week_cards.append(
            f'<div class="day-card {css_class}">'
            f'<div class="day-name">{weekdays[index]} · {current_date.strftime("%d.%m.")}</div>'
            f'<div class="day-score">{dot} {score_text}</div>'
            f'<div class="day-detail">{detail}</div>'
            f'<div class="day-subdetail">{subdetail}</div>'
            f'</div>'
        )

    week_html = '<div class="week-grid">' + "".join(week_cards) + '</div>'

    st.markdown(
        week_html,
        unsafe_allow_html=True,
    )

    st.caption("🟢 ab 80 % · 🟡 50–79 % · 🔴 unter 50 % · ⚪ kein Eintrag · blauer Rand = heute")

    # --------------------------------------------------
    # KONSTANZ
    # --------------------------------------------------

    current_streak, longest_streak = calculate_streak(all_days)

    st.markdown('<div class="section-title">🔥 Konstanz</div>', unsafe_allow_html=True)

    streak1, streak2, streak3 = st.columns(3, gap="medium")
    with streak1:
        st.metric("Aktuelle 80%-Streak", f"{current_streak} Tage", border=True)
    with streak2:
        st.metric("Längste 80%-Streak", f"{longest_streak} Tage", border=True)
    with streak3:
        st.metric("Gespeicherte Tage", len(all_days), border=True)

    # --------------------------------------------------
    # TRAINING
    # --------------------------------------------------

    st.markdown('<div class="section-title">💪 Training</div>', unsafe_allow_html=True)

    train1, train2, train3 = st.columns(3, gap="medium")
    with train1:
        st.metric("Diese Woche", count_training(week_days), border=True)
    with train2:
        st.metric("Dieser Monat", count_training(month_days), border=True)
    with train3:
        st.metric("Dieses Jahr", count_training(year_days), border=True)

    # --------------------------------------------------
    # GEWOHNHEITEN IM MONAT
    # --------------------------------------------------

    st.markdown('<div class="section-title">🎯 Gewohnheiten diesen Monat</div>', unsafe_allow_html=True)

    habit_labels = {
        "calorie_deficit": "🔥 Kaloriendefizit",
        "fixed_meals": "🍽️ Feste Mahlzeiten",
        "no_snacks": "🚫 Keine unnötigen Snacks",
        "no_calorie_drinks": "🥤 Keine Kalorien getrunken",
        "no_alcohol": "🍺 Kein Alkohol",
        "movement_30": "🚶 30 Min. Bewegung",
        "protein_goal": "🥩 Proteinziel",
        "sleep_goal": "😴 Schlafziel",
        "reading_30": "📚 30 Min. Lesen",
        "trading_30": "📈 30 Min. Trading",
    }

    for field, label in habit_labels.items():
        completed = sum(bool(day.get(field, False)) for day in month_days)
        total = len(month_days)
        percentage = completed / total if total else 0

        row1, row2 = st.columns([5, 1], vertical_alignment="center")
        with row1:
            st.write(f"**{label}**")
            st.progress(percentage)
        with row2:
            st.write(f"**{completed}/{total}**")

    # --------------------------------------------------
    # MONATSFAZIT
    # --------------------------------------------------

    st.markdown('<div class="section-title">🧠 Monatsfazit</div>', unsafe_allow_html=True)

    if not month_days:
        st.info("🌱 Noch keine gespeicherten Tage in diesem Monat.")
    elif month_score >= 0.90:
        st.success("🏆 Überragende Konstanz – diesen Rhythmus beibehalten.")
    elif month_score >= 0.80:
        st.success("🔥 Sehr starker Monat. Du bist klar auf Kurs.")
    elif month_score >= 0.70:
        st.info("💪 Solider Monat. Kleine Verbesserungen bringen dich Richtung 80 %.")
    elif month_score >= 0.50:
        st.info("🎯 Gute Basis – konzentriere dich auf die Gewohnheiten mit der niedrigsten Quote.")
    else:
        st.info("🌱 Jeder gespeicherte Tag zählt. Ziel ist zunächst Konstanz, nicht Perfektion.")

st.caption("STANI PERFORMANCE · Konstanz heute. Fortschritt morgen.")
