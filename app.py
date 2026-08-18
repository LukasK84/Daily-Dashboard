import streamlit as st
from datetime import date, datetime
from supabase import create_client, Client

# --------------------------------------------------
# GRUNDEINSTELLUNGEN
# --------------------------------------------------

st.set_page_config(
    page_title="Joe's Daily Dashboard",
    page_icon="💪",
    layout="wide"
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
    color: white !important;
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
    font-size: 2rem;
    font-weight: 800;
}

.small-text {
    color: #9ca3af;
    font-size: 0.85rem;
}

/* Labels besser lesbar */
label, p, span {
    color: #e5e7eb;
}

/* Radio- und Selectbox-Beschriftung */
div[data-testid="stWidgetLabel"] p {
    color: #d1d5db !important;
}

/* Progressbar */
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
# DATENBANK-FUNKTIONEN
# --------------------------------------------------

def load_day(selected_date):

    response = (
        supabase
        .table("daily_tracker")
        .select("*")
        .eq("date", str(selected_date))
        .execute()
    )

    if response.data:
        return response.data[0]

    return None


def save_day(data):

    supabase \
        .table("daily_tracker") \
        .upsert(data) \
        .execute()


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
# DATUM
# --------------------------------------------------

datum = st.date_input(
    "📅 Datum",
    value=date.today()
)

saved = load_day(datum)


# --------------------------------------------------
# STANDARDWERTE
# --------------------------------------------------

if saved:

    default_shift = saved["shift"]
    default_training = saved["training_day"]

else:

    default_shift = "Frühschicht"
    default_training = "Ruhetag"


shift_options = [
    "Frühschicht",
    "Spätschicht",
    "Nachtschicht",
    "Frei"
]

training_options = [
    "Ruhetag",
    "Training A",
    "Training B",
    "Training C"
]


# --------------------------------------------------
# SCHICHT
# --------------------------------------------------

col1, col2 = st.columns([1, 1])

with col1:

    schicht = st.selectbox(
        "🏭 Meine Schicht",
        shift_options,
        index=shift_options.index(default_shift)
    )

with col2:

    if saved:
        st.success("💾 Dieser Tag ist gespeichert")
    else:
        st.info("🆕 Neuer Tag")


st.divider()


# --------------------------------------------------
# DAILY CHECK
# --------------------------------------------------

st.subheader("🏆 Mein Tages-Check")


def default_value(field):
    if saved:
        return bool(saved.get(field, False))
    return False


daily_fields = [
    ("calorie_deficit", "Kaloriendefizit eingehalten"),
    ("fixed_meals", "Feste Mahlzeiten eingehalten"),
    ("no_snacks", "Keine unnötigen Snacks"),
    ("no_calorie_drinks", "Keine Kalorien getrunken"),
    ("movement_30", "30 Minuten Spaziergang / Bewegung"),
    ("protein_goal", "Proteinziel erreicht"),
    ("sleep_goal", "Schlafziel erreicht"),
    ("reading_30", "30 Minuten gelesen"),
    ("trading_30", "30 Minuten Trading / Trading lernen"),
]

daily_values = {}

col1, col2 = st.columns(2)

for index, (field, label) in enumerate(daily_fields):

    column = col1 if index % 2 == 0 else col2

    with column:

        daily_values[field] = st.checkbox(
            label,
            value=default_value(field),
            key=f"{datum}_{field}"
        )


# --------------------------------------------------
# TRAINING
# --------------------------------------------------

st.divider()

st.subheader("💪 Mein Training")

training = st.radio(
    "Was steht heute an?",
    training_options,
    index=training_options.index(default_training),
    horizontal=True,
    key=f"{datum}_training"
)


training_values = []

if training != "Ruhetag":

    st.markdown(f"### {training}")

    exercises = trainingsplan[training]

    for index, (exercise, reps) in enumerate(exercises):

        col1, col2 = st.columns([4, 1])

        field = f"exercise_{index + 1}"

        old_value = False

        if saved and saved["training_day"] == training:
            old_value = bool(saved.get(field, False))

        with col1:

            done = st.checkbox(
                exercise,
                value=old_value,
                key=f"{datum}_{training}_{field}"
            )

        with col2:

            st.markdown(f"**{reps}**")

        training_values.append(done)

else:

    st.info("😌 Heute ist Regeneration angesagt.")

    training_values = [False] * 7


# --------------------------------------------------
# FORTSCHRITT
# --------------------------------------------------

st.divider()

st.subheader("📊 Tagesfortschritt")

completed_daily = sum(daily_values.values())
total_daily = len(daily_values)

if training != "Ruhetag":

    completed_training = sum(training_values)
    total_training = 7

else:

    completed_training = 0
    total_training = 0


completed_total = completed_daily + completed_training
total_tasks = total_daily + total_training

progress = completed_total / total_tasks if total_tasks else 0


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
        status = "🏆 Perfekt!"
    elif progress >= 0.8:
        status = "🔥 Stark!"
    elif progress >= 0.5:
        status = "💪 Weiter!"
    else:
        status = "🎯 Dranbleiben"

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
# SPEICHERN
# --------------------------------------------------

st.divider()

if st.button(
    "💾 TAG SPEICHERN",
    type="primary",
    use_container_width=True
):

    data = {

        "date": str(datum),

        "shift": schicht,
        "training_day": training,

        "calorie_deficit": daily_values["calorie_deficit"],
        "fixed_meals": daily_values["fixed_meals"],
        "no_snacks": daily_values["no_snacks"],
        "no_calorie_drinks": daily_values["no_calorie_drinks"],
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

        "updated_at": datetime.utcnow().isoformat()
    }

    try:

        save_day(data)

        st.success(
            "✅ Tag dauerhaft gespeichert!"
        )

        st.rerun()

    except Exception as e:

        st.error(
            "Speichern fehlgeschlagen."
        )

        st.exception(e)


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
        "🎯 Nicht Perfektion entscheidet, sondern Konstanz."
    )


st.caption(
    "Konsequenz heute. Fortschritt morgen."
)
