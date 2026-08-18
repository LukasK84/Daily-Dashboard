import streamlit as st
from datetime import date

# --------------------------------------------------
# GRUNDEINSTELLUNGEN
# --------------------------------------------------

st.set_page_config(
    page_title="Joe's Daily Dashboard",
    page_icon="💪",
    layout="wide"
)

# --------------------------------------------------
# DESIGN
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #0e1625;
    color: white;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1, h2, h3 {
    color: white;
}

.dashboard-title {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 0;
}

.dashboard-subtitle {
    color: #9ca3af;
    margin-bottom: 25px;
}

.card {
    background: #151f30;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #263449;
    margin-bottom: 15px;
}

.big-number {
    font-size: 2.1rem;
    font-weight: 800;
}

.small-text {
    color: #9ca3af;
    font-size: 0.9rem;
}

div[data-testid="stProgress"] > div > div > div > div {
    background-color: #34d399;
}

</style>
""", unsafe_allow_html=True)


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
    ]
}


# --------------------------------------------------
# KOPF
# --------------------------------------------------

st.markdown(
    '<div class="dashboard-title">💪 JOE\'S DAILY DASHBOARD</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Fitness • Ernährung • Lernen • Trading'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# TAG & SCHICHT
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    datum = st.date_input(
        "📅 Datum",
        value=date.today()
    )

with col2:
    schicht = st.selectbox(
        "🏭 Meine Schicht",
        [
            "Frühschicht",
            "Spätschicht",
            "Nachtschicht",
            "Frei"
        ]
    )


st.divider()


# --------------------------------------------------
# DAILY CHECK
# --------------------------------------------------

st.subheader("🏆 Mein Tages-Check")

daily_tasks = [
    "Kaloriendefizit eingehalten",
    "Feste Mahlzeiten eingehalten",
    "Keine unnötigen Snacks",
    "Keine Kalorien getrunken",
    "30 Minuten Spaziergang / Bewegung",
    "Proteinziel erreicht",
    "Schlafziel erreicht",
    "30 Minuten gelesen",
    "30 Minuten Trading / Trading lernen",
]

daily_results = []

col1, col2 = st.columns(2)

for index, task in enumerate(daily_tasks):

    column = col1 if index % 2 == 0 else col2

    with column:
        checked = st.checkbox(
            task,
            key=f"daily_{datum}_{index}"
        )

        daily_results.append(checked)


# --------------------------------------------------
# TRAINING
# --------------------------------------------------

st.divider()

st.subheader("💪 Mein Training")

training = st.radio(
    "Was steht heute an?",
    [
        "Ruhetag",
        "Training A",
        "Training B",
        "Training C"
    ],
    horizontal=True
)


training_results = []

if training != "Ruhetag":

    st.markdown(f"### {training}")

    exercises = trainingsplan[training]

    for index, (exercise, reps) in enumerate(exercises):

        col1, col2 = st.columns([4, 1])

        with col1:
            done = st.checkbox(
                exercise,
                key=f"{datum}_{training}_{index}"
            )

        with col2:
            st.markdown(f"**{reps}**")

        training_results.append(done)

else:

    st.info("😌 Heute ist Regeneration angesagt.")


# --------------------------------------------------
# TAGESFORTSCHRITT
# --------------------------------------------------

st.divider()

st.subheader("📊 Tagesfortschritt")

completed_daily = sum(daily_results)
total_daily = len(daily_results)

if training != "Ruhetag":

    completed_training = sum(training_results)
    total_training = len(training_results)

else:

    completed_training = 0
    total_training = 0


completed_total = completed_daily + completed_training
total_tasks = total_daily + total_training

if total_tasks > 0:
    progress = completed_total / total_tasks
else:
    progress = 0


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="card">
        <div class="small-text">ERLEDIGT</div>
        <div class="big-number">{completed_total}/{total_tasks}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="card">
        <div class="small-text">TAGESFORTSCHRITT</div>
        <div class="big-number">{progress:.0%}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:

    if progress == 1:
        status = "🏆 Perfekter Tag!"
    elif progress >= 0.8:
        status = "🔥 Stark!"
    elif progress >= 0.5:
        status = "💪 Weiter so!"
    else:
        status = "🎯 Dranbleiben!"

    st.markdown(
        f"""
        <div class="card">
        <div class="small-text">STATUS</div>
        <div class="big-number">{status}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.progress(progress)


# --------------------------------------------------
# MOTIVATION
# --------------------------------------------------

st.divider()

if progress == 1:

    st.success(
        "🏆 Alles erledigt – starker Tag!"
    )

elif progress >= 0.8:

    st.success(
        "🔥 Fast alles geschafft. Genau diese Konstanz zählt."
    )

elif progress >= 0.5:

    st.info(
        "💪 Mehr als die Hälfte geschafft – weiter dranbleiben."
    )

else:

    st.info(
        "🎯 Nicht Perfektion entscheidet, sondern dass du heute etwas machst."
    )


st.caption(
    "Konsequenz heute. Fortschritt morgen."
)
