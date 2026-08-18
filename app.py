import streamlit as st
from datetime import date, datetime, timedelta, timezone
from supabase import create_client, Client

# --------------------------------------------------
# GRUNDEINSTELLUNGEN
# --------------------------------------------------

st.set_page_config(
    page_title="Mission 365",
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
        --bg: #08111f;
        --card: rgba(17, 29, 48, 0.86);
        --card-2: rgba(22, 37, 61, 0.82);
        --line: rgba(148, 163, 184, 0.16);
        --text: #f8fafc;
        --muted: #94a3b8;
        --green: #22c55e;
        --yellow: #f59e0b;
        --red: #ef4444;
        --blue: #38bdf8;
        --purple: #a78bfa;
    }

    .stApp {
        background:
            radial-gradient(circle at 15% 0%, rgba(56, 189, 248, 0.10), transparent 26rem),
            radial-gradient(circle at 100% 10%, rgba(167, 139, 250, 0.10), transparent 24rem),
            var(--bg);
        color: var(--text);
    }

    .block-container {
        max-width: 1180px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3, h4, p, label, span {
        color: var(--text);
    }

    div[data-testid="stWidgetLabel"] p {
        color: #cbd5e1 !important;
        font-weight: 600;
    }

    .mission-header {
        padding: 0.2rem 0 1rem 0;
    }

    .mission-kicker {
        color: var(--blue);
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }

    .mission-title {
        font-size: clamp(2.1rem, 6vw, 4rem);
        line-height: 1;
        font-weight: 900;
        letter-spacing: -0.04em;
        margin: 0;
    }

    .mission-subtitle {
        color: var(--muted);
        font-size: 1rem;
        margin-top: 0.55rem;
    }

    .hero-card {
        background: linear-gradient(135deg, rgba(18, 35, 58, 0.96), rgba(11, 23, 40, 0.96));
        border: 1px solid var(--line);
        border-radius: 24px;
        padding: 1.3rem 1.4rem;
        margin: 0.25rem 0 1.1rem 0;
        box-shadow: 0 18px 50px rgba(0, 0, 0, 0.22);
    }

    .hero-row {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        gap: 1rem;
        flex-wrap: wrap;
    }

    .hero-label {
        color: var(--muted);
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.11em;
        text-transform: uppercase;
    }

    .hero-score {
        font-size: clamp(2.8rem, 8vw, 5.5rem);
        font-weight: 900;
        line-height: 0.95;
        letter-spacing: -0.06em;
        margin-top: 0.3rem;
    }

    .hero-score span {
        color: var(--muted);
        font-size: 0.32em;
        font-weight: 700;
        letter-spacing: 0;
    }

    .hero-status {
        color: #dbeafe;
        font-size: 1rem;
        font-weight: 700;
        text-align: right;
    }

    .hero-meta {
        color: var(--muted);
        margin-top: 0.3rem;
        font-size: 0.9rem;
        text-align: right;
    }

    .section-title {
        font-size: 1.1rem;
        font-weight: 800;
        margin: 0.25rem 0 0.65rem 0;
    }

    .week-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(115px, 1fr));
        gap: 0.7rem;
        margin-top: 0.7rem;
        margin-bottom: 1rem;
    }

    .day-card {
        border-radius: 18px;
        border: 1px solid var(--line);
        padding: 0.9rem;
        min-height: 112px;
        background: var(--card);
    }

    .day-good {
        background: linear-gradient(145deg, rgba(34, 197, 94, 0.18), rgba(17, 29, 48, 0.92));
        border-color: rgba(34, 197, 94, 0.35);
    }

    .day-mid {
        background: linear-gradient(145deg, rgba(245, 158, 11, 0.16), rgba(17, 29, 48, 0.92));
        border-color: rgba(245, 158, 11, 0.35);
    }

    .day-low {
        background: linear-gradient(145deg, rgba(239, 68, 68, 0.15), rgba(17, 29, 48, 0.92));
        border-color: rgba(239, 68, 68, 0.30);
    }

    .day-empty {
        background: rgba(15, 23, 42, 0.52);
        opacity: 0.82;
    }

    .day-name {
        color: var(--muted);
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 0.1em;
    }

    .day-score {
        font-size: 1.65rem;
        font-weight: 900;
        margin: 0.25rem 0 0.2rem 0;
    }

    .day-detail {
        color: #cbd5e1;
        font-size: 0.78rem;
    }

    div[data-testid="stMetric"] {
        background: rgba(17, 29, 48, 0.72);
        border-color: var(--line) !important;
        border-radius: 18px;
        padding: 0.25rem 0.35rem;
    }

    div[data-testid="stMetricValue"] {
        font-weight: 900;
        letter-spacing: -0.03em;
    }

    div.stButton > button[kind="primary"] {
        border-radius: 14px;
        font-weight: 800;
        min-height: 3rem;
    }

    div[data-testid="stCheckbox"] {
        padding: 0.15rem 0;
    }

    .habit-row {
        padding: 0.2rem 0 0.55rem 0;
    }

    .mini-note {
        color: var(--muted);
        font-size: 0.82rem;
    }

    @media (max-width: 700px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 1rem;
        }

        .hero-status,
        .hero-meta {
            text-align: left;
        }

        .week-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
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
        <div class="mission-kicker">Daily Performance System</div>
        <div class="mission-title">🎯 MISSION 365</div>
        <div class="mission-subtitle">
            Training • Ernährung • Gesundheit • Lernen • Trading
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

    daily_fields = [
        ("calorie_deficit", "🔥 Kaloriendefizit eingehalten"),
        ("fixed_meals", "🍽️ Feste Mahlzeiten eingehalten"),
        ("no_snacks", "🚫 Keine unnötigen Snacks"),
        ("no_calorie_drinks", "🥤 Keine Kalorien getrunken"),
        ("no_alcohol", "🍺 Kein Alkohol"),
        ("movement_30", "🚶 30 Minuten Spaziergang / Bewegung"),
        ("protein_goal", "🥩 Proteinziel erreicht"),
        ("sleep_goal", "😴 Schlafziel erreicht"),
        ("reading_30", "📚 30 Minuten gelesen"),
        ("trading_30", "📈 30 Minuten Trading / Trading lernen"),
    ]

    daily_values = {}

    check_col1, check_col2 = st.columns(2, gap="large")

    for index, (field, label) in enumerate(daily_fields):
        target_col = check_col1 if index % 2 == 0 else check_col2
        with target_col:
            daily_values[field] = st.checkbox(
                label,
                value=default_value(field),
                key=f"{datum}_{field}",
            )

    st.markdown('<div class="section-title">💪 Training</div>', unsafe_allow_html=True)

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
        st.metric("Mission Score", f"{mission_score}/100", border=True)
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
with hero_placeholder.container():
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-row">
                <div>
                    <div class="hero-label">Mission Score · {datum.strftime("%d.%m.%Y")}</div>
                    <div class="hero-score">{mission_score}<span>/100</span></div>
                </div>
                <div>
                    <div class="hero-status">{status_for_score(progress)}</div>
                    <div class="hero-meta">{schicht} · {training}</div>
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
            score_text = f"{score_pct}%"
        else:
            css_class = "day-empty"
            dot = "⚪"
            detail = "Noch kein Eintrag"
            score_text = "–"

        if current_date > today:
            css_class = "day-empty"
            dot = "⚪"
            detail = "Noch offen"
            score_text = "–"

        week_cards.append(
            f"""
            <div class="day-card {css_class}">
                <div class="day-name">{weekdays[index]} · {current_date.strftime("%d.%m.")}</div>
                <div class="day-score">{dot} {score_text}</div>
                <div class="day-detail">{detail}</div>
            </div>
            """
        )

    st.markdown(
        '<div class="week-grid">' + "".join(week_cards) + "</div>",
        unsafe_allow_html=True,
    )

    st.caption("🟢 ab 80 % · 🟡 50–79 % · 🔴 unter 50 % · ⚪ noch kein Eintrag")

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

st.caption("MISSION 365 · Konsequenz heute. Fortschritt morgen.")
