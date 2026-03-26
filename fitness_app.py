import streamlit as st
import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FitCoach Pro",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main theme */
    [data-testid="stAppViewContainer"] { background: #0f0f0f; }
    [data-testid="stSidebar"] { background: #1a1a1a; border-right: 1px solid #2a2a2a; }
    h1, h2, h3 { color: #f5f5f5; }
    p, label, .stMarkdown { color: #c0c0c0; }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: #1e1e1e;
        border: 1px solid #2e2e2e;
        border-radius: 12px;
        padding: 16px;
    }
    [data-testid="stMetricValue"] { color: #e8ff47 !important; font-size: 2rem !important; }
    [data-testid="stMetricLabel"] { color: #888 !important; }

    /* Buttons */
    .stButton > button {
        background: #e8ff47;
        color: #0f0f0f;
        border: none;
        border-radius: 8px;
        font-weight: 700;
        padding: 0.5rem 1.5rem;
        transition: all 0.2s;
    }
    .stButton > button:hover { background: #d4eb2e; transform: translateY(-1px); }

    /* Progress bars */
    .stProgress > div > div { background: #e8ff47; border-radius: 4px; }

    /* Section cards */
    .card {
        background: #1e1e1e;
        border: 1px solid #2e2e2e;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
    }
    .highlight { color: #e8ff47; font-weight: 700; }
    .badge {
        display: inline-block;
        background: #e8ff47;
        color: #0f0f0f;
        border-radius: 20px;
        padding: 2px 12px;
        font-size: 0.75rem;
        font-weight: 700;
        margin: 2px;
    }
    hr { border-color: #2a2a2a; }
</style>
""", unsafe_allow_html=True)

# ── Session state defaults ────────────────────────────────────────────────────
defaults = {
    "workouts_done": 0,
    "calories_burned": 0,
    "water_glasses": 0,
    "streak": 4,
    "log": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💪 FitCoach Pro")
    st.markdown("---")

    name = st.text_input("Your name", value="Athlete")
    goal = st.selectbox("🎯 Primary goal", [
        "Lose weight", "Build muscle", "Improve endurance",
        "Increase flexibility", "General fitness"
    ])
    fitness_level = st.select_slider(
        "Fitness level",
        options=["Beginner", "Intermediate", "Advanced", "Elite"],
        value="Intermediate"
    )
    age = st.number_input("Age", min_value=13, max_value=90, value=25)
    weight_kg = st.number_input("Weight (kg)", min_value=30, max_value=250, value=75)
    height_cm = st.number_input("Height (cm)", min_value=100, max_value=250, value=175)

    st.markdown("---")
    page = st.radio("Navigate", [
        "🏠 Dashboard", "🏋️ Workout Planner",
        "🥗 Nutrition", "📊 Progress", "💬 Coach Chat"
    ])

# ── BMI Calc ──────────────────────────────────────────────────────────────────
bmi = weight_kg / ((height_cm / 100) ** 2)
bmi_label = (
    "Underweight" if bmi < 18.5 else
    "Normal weight" if bmi < 25 else
    "Overweight" if bmi < 30 else "Obese"
)

# ── TDEE Calc ─────────────────────────────────────────────────────────────────
bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
activity_factors = {"Beginner": 1.375, "Intermediate": 1.55, "Advanced": 1.725, "Elite": 1.9}
tdee = int(bmr * activity_factors[fitness_level])

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ═════════════════════════════════════════════════════════════════════════════
if page == "🏠 Dashboard":
    st.markdown(f"# 👋 Welcome back, {name}!")
    st.markdown(f"**{datetime.date.today().strftime('%A, %B %d %Y')}** · Goal: `{goal}`")
    st.markdown("---")

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔥 Workouts Done", st.session_state.workouts_done, "+1 today")
    c2.metric("⚡ Calories Burned", f"{st.session_state.calories_burned} kcal")
    c3.metric("💧 Water Intake", f"{st.session_state.water_glasses} glasses")
    c4.metric("🏅 Day Streak", f"{st.session_state.streak} days", "+1")

    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 📅 Today's Plan")
        st.markdown(f'<div class="card">', unsafe_allow_html=True)

        workouts = {
            "Lose weight":          [("🏃 Cardio HIIT", 30, 300), ("🧘 Yoga cool-down", 15, 80)],
            "Build muscle":         [("🏋️ Upper body strength", 45, 350), ("💪 Core finisher", 15, 120)],
            "Improve endurance":    [("🚴 Zone 2 cycling", 50, 400), ("🏊 Easy swim", 20, 150)],
            "Increase flexibility": [("🧘 Dynamic stretching", 20, 60), ("🏃 Light jog", 25, 200)],
            "General fitness":      [("🏋️ Full-body circuit", 40, 320), ("🚶 Brisk walk", 20, 120)],
        }
        plan = workouts[goal]
        total_cal = sum(c for _, _, c in plan)

        for workout, mins, cal in plan:
            done = st.checkbox(f"{workout} — {mins} min · ~{cal} kcal", key=workout)
            if done:
                st.session_state.calories_burned = cal
                st.session_state.workouts_done = 1

        st.markdown(f"**Total estimated burn: <span class='highlight'>{total_cal} kcal</span>**", unsafe_allow_html=True)
        if st.button("✅ Log Workout"):
            st.session_state.workouts_done += 1
            st.session_state.calories_burned += total_cal
            st.session_state.log.append({
                "date": str(datetime.date.today()),
                "workout": goal,
                "calories": total_cal
            })
            st.success("Workout logged! Great job 💪")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("### 💧 Water Tracker")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        target = 8
        current = st.session_state.water_glasses
        pct = min(int((current / target) * 100), 100)
        st.markdown(f"**{current} / {target} glasses**")
        st.progress(pct / 100)
        if st.button("+ Add a glass"):
            st.session_state.water_glasses = min(st.session_state.water_glasses + 1, target)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("### 📐 Body Stats")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"**BMI:** <span class='highlight'>{bmi:.1f}</span> — {bmi_label}", unsafe_allow_html=True)
        st.markdown(f"**TDEE:** <span class='highlight'>{tdee} kcal/day</span>", unsafe_allow_html=True)
        st.markdown(f"**Level:** <span class='highlight'>{fitness_level}</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: WORKOUT PLANNER
# ═════════════════════════════════════════════════════════════════════════════
elif page == "🏋️ Workout Planner":
    st.markdown("# 🏋️ Workout Planner")
    st.markdown("Build a custom workout session.")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        duration = st.slider("Session duration (min)", 15, 90, 45, 5)
        intensity = st.select_slider("Intensity", ["Light", "Moderate", "Hard", "All-out"], value="Moderate")
        focus = st.multiselect("Muscle focus", [
            "Chest", "Back", "Shoulders", "Arms",
            "Core", "Legs", "Full body", "Cardio"
        ], default=["Full body"])

    with col2:
        equipment = st.multiselect("Available equipment", [
            "Barbell", "Dumbbells", "Resistance bands",
            "Pull-up bar", "Kettlebell", "Bodyweight only", "Machines"
        ], default=["Dumbbells", "Bodyweight only"])
        rest_time = st.slider("Rest between sets (sec)", 30, 120, 60, 15)

    if st.button("🎲 Generate My Workout"):
        st.markdown("---")
        st.markdown("### Your Custom Workout")

        exercises = {
            "Chest":      [("Push-ups", "3×15"), ("Dumbbell press", "4×10"), ("Chest fly", "3×12")],
            "Back":       [("Pull-ups", "3×8"), ("Bent-over row", "4×10"), ("Lat pulldown", "3×12")],
            "Shoulders":  [("Overhead press", "4×10"), ("Lateral raises", "3×15"), ("Front raises", "3×12")],
            "Arms":       [("Bicep curl", "3×12"), ("Tricep dip", "3×15"), ("Hammer curl", "3×10")],
            "Core":       [("Plank", "3×45s"), ("Russian twist", "3×20"), ("Leg raise", "3×15")],
            "Legs":       [("Squat", "4×12"), ("Lunges", "3×10/leg"), ("Calf raise", "3×20")],
            "Full body":  [("Burpee", "3×10"), ("Thruster", "4×8"), ("Mountain climber", "3×20")],
            "Cardio":     [("Jump rope", "3×2min"), ("Box jump", "3×10"), ("Sprint intervals", "5×30s")],
        }

        cols = st.columns(2)
        for i, group in enumerate(focus if focus else ["Full body"]):
            ex_list = exercises.get(group, exercises["Full body"])
            with cols[i % 2]:
                st.markdown(f'<div class="card"><b class="highlight">{group}</b><br><br>', unsafe_allow_html=True)
                for ex, sets in ex_list:
                    st.markdown(f"• **{ex}** — {sets} · {rest_time}s rest")
                st.markdown('</div>', unsafe_allow_html=True)

        est_cal = int(duration * (5 if intensity == "Light" else 8 if intensity == "Moderate" else 11 if intensity == "Hard" else 14))
        st.info(f"⏱ Estimated duration: **{duration} min** · 🔥 ~**{est_cal} kcal** burned")

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: NUTRITION
# ═════════════════════════════════════════════════════════════════════════════
elif page == "🥗 Nutrition":
    st.markdown("# 🥗 Nutrition Guide")
    st.markdown("---")

    goal_macros = {
        "Lose weight":          {"Protein": 40, "Carbs": 30, "Fat": 30},
        "Build muscle":         {"Protein": 35, "Carbs": 45, "Fat": 20},
        "Improve endurance":    {"Protein": 25, "Carbs": 55, "Fat": 20},
        "Increase flexibility": {"Protein": 30, "Carbs": 40, "Fat": 30},
        "General fitness":      {"Protein": 30, "Carbs": 40, "Fat": 30},
    }
    macros = goal_macros[goal]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎯 Your Daily Targets")
        st.markdown(f'<div class="card">', unsafe_allow_html=True)
        deficit = {"Lose weight": -500, "Build muscle": +300}.get(goal, 0)
        target_cal = tdee + deficit
        st.markdown(f"**Daily calories:** <span class='highlight'>{target_cal} kcal</span>", unsafe_allow_html=True)
        st.markdown(f"**TDEE (maintenance):** {tdee} kcal")
        if deficit != 0:
            st.markdown(f"**Adjustment:** {'−' if deficit < 0 else '+'}{abs(deficit)} kcal ({goal})")
        st.markdown("---")
        for macro, pct in macros.items():
            grams = int(target_cal * pct / 100 / (4 if macro != "Fat" else 9))
            st.markdown(f"**{macro}:** {pct}% → ~{grams}g/day")
            st.progress(pct / 100)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("### 🍽️ Meal Ideas")
        meals = {
            "Lose weight": {
                "Breakfast": "Greek yogurt + berries + flaxseeds",
                "Lunch":     "Grilled chicken salad + olive oil",
                "Dinner":    "Baked salmon + steamed broccoli + quinoa",
                "Snack":     "Apple + almond butter",
            },
            "Build muscle": {
                "Breakfast": "Eggs + oats + banana + protein shake",
                "Lunch":     "Rice + chicken breast + avocado",
                "Dinner":    "Lean beef + sweet potato + spinach",
                "Snack":     "Cottage cheese + walnuts",
            },
        }
        day_meals = meals.get(goal, meals["Lose weight"])
        st.markdown('<div class="card">', unsafe_allow_html=True)
        for meal, food in day_meals.items():
            st.markdown(f"**{meal}:** {food}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 🍱 Calorie Logger")
    food_input = st.text_input("Add food item")
    food_cal = st.number_input("Calories", min_value=0, max_value=2000, value=0)
    if st.button("Log food"):
        if food_input:
            st.success(f"✅ Logged: {food_input} — {food_cal} kcal")

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: PROGRESS
# ═════════════════════════════════════════════════════════════════════════════
elif page == "📊 Progress":
    st.markdown("# 📊 Progress Tracker")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Workouts", st.session_state.workouts_done)
    col2.metric("Calories Burned", f"{st.session_state.calories_burned} kcal")
    col3.metric("Day Streak", f"{st.session_state.streak} 🔥")

    st.markdown("### Weekly Goal Progress")
    weekly_goals = {
        "Workouts (target: 5)": min(st.session_state.workouts_done / 5, 1.0),
        "Cardio minutes (target: 150 min)": 0.6,
        "Water intake (target: 56 glasses/week)": min(st.session_state.water_glasses / 56, 1.0),
        "Calories burned (target: 2500 kcal)": min(st.session_state.calories_burned / 2500, 1.0),
    }
    for label, val in weekly_goals.items():
        st.markdown(f"**{label}** — {int(val*100)}%")
        st.progress(val)

    st.markdown("### 🏅 Achievements")
    badges = []
    if st.session_state.workouts_done >= 1: badges.append("First Workout!")
    if st.session_state.streak >= 3: badges.append("3-Day Streak")
    if st.session_state.streak >= 7: badges.append("Week Warrior")
    if st.session_state.water_glasses >= 8: badges.append("Hydration Hero")
    if not badges: badges.append("Complete your first workout to earn badges!")
    badge_html = " ".join(f'<span class="badge">{b}</span>' for b in badges)
    st.markdown(badge_html, unsafe_allow_html=True)

    if st.session_state.log:
        st.markdown("### 📋 Workout Log")
        for entry in reversed(st.session_state.log[-5:]):
            st.markdown(f"• **{entry['date']}** — {entry['workout']} · {entry['calories']} kcal")

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: COACH CHAT
# ═════════════════════════════════════════════════════════════════════════════
elif page == "💬 Coach Chat":
    st.markdown("# 💬 Ask Your AI Coach")
    st.markdown("Get personalised advice based on your profile.")
    st.markdown("---")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": f"Hey {name}! 👋 I'm your FitCoach AI. I know your goal is **{goal}** and you're at **{fitness_level}** level. Ask me anything about workouts, nutrition, or recovery!"}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    quick = st.pills("Quick questions", [
        "What should I eat post-workout?",
        "How many rest days do I need?",
        "How do I avoid plateaus?",
        "Best exercises for my goal?",
    ], selection_mode="single")

    prompt = st.chat_input("Ask your coach...") or quick

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Simple rule-based responses
        p = prompt.lower()
        if "eat" in p or "food" in p or "nutrition" in p or "post-workout" in p:
            reply = f"For **{goal}**, post-workout nutrition is key! Aim for a **protein + carb combo within 30–60 min** — e.g. chicken + rice, or a protein shake with a banana. Your daily protein target is ~{int(weight_kg * 1.8)}g."
        elif "rest" in p or "recovery" in p:
            reply = f"As a **{fitness_level}** athlete targeting **{goal}**, aim for **{2 if fitness_level in ['Beginner','Intermediate'] else 1}–2 rest days per week**. Sleep 7–9 hours. Active recovery (walks, stretching) on off days is great."
        elif "plateau" in p:
            reply = "Plateaus are normal! Try: **progressive overload** (add 5% weight/week), **change rep ranges**, add a **deload week** every 4–6 weeks, or switch up your exercise selection entirely."
        elif "exercise" in p or "workout" in p or "best" in p:
            recs = {
                "Lose weight":       "HIIT cardio, compound lifts (squats, deadlifts), circuit training",
                "Build muscle":      "Progressive overload with barbell compounds — squat, bench, deadlift, overhead press",
                "Improve endurance": "Zone 2 cardio, tempo runs, interval training, swim/bike combos",
                "General fitness":   "Full-body circuits 3–4x/week with a mix of cardio and strength",
            }
            reply = f"For **{goal}** at **{fitness_level}** level, I recommend: {recs.get(goal, 'a balanced mix of cardio and strength training')}."
        else:
            reply = f"Great question! As a **{fitness_level}** working on **{goal}**, consistency is your superpower. Stay on your plan, track your progress, and don't skip recovery. You've got this, {name}! 💪"

        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
