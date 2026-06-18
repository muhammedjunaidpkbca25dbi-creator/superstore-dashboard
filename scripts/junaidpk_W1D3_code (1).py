import streamlit as st

st.title("🏥 BMI Calculator")
st.markdown("---")

# User Inputs
name = st.text_input("Name")
age = st.number_input("Age", 10, 100, 25)
sex = st.radio("Gender", ["Male", "Female"], horizontal=True)
weight = st.slider("Weight (kg)", 30, 150, 70)
height = st.slider("Height (cm)", 100, 220, 170)

# BMI Calculation
bmi = weight / ((height / 100) ** 2)

st.header("BMI Result")

st.metric("BMI", f"{bmi:.1f}")

# BMI Classification
if bmi < 18.5:
    st.warning("Underweight | Health Risk: Moderate")
elif bmi < 25:
    st.success("Normal Weight | Health Risk: Low")
elif bmi < 30:
    st.warning("Overweight | Health Risk: Elevated")
else:
    st.error("Obese | Health Risk: High")

# Activity Level
st.header("Daily Calorie Need")

activity = st.selectbox(
    "Activity Level",
    [
        "Sedentary",
        "Lightly active",
        "Moderately active",
        "Very active",
        "Extra active"
    ]
)

multipliers = {
    "Sedentary": 1.2,
    "Lightly active": 1.375,
    "Moderately active": 1.55,
    "Very active": 1.725,
    "Extra active": 1.9
}

# BMR
if sex == "Male":
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
else:
    bmr = 10 * weight + 6.25 * height - 5 * age - 161

calories = bmr * multipliers[activity]

st.metric("Daily Calories", f"{round(calories)} kcal")

# Ideal Weight (Robinson Formula)
st.header("Ideal Weight Range")

if sex == "Male":
    ideal = 52 + 1.9 * ((height / 2.54) - 60)
else:
    ideal = 49 + 1.7 * ((height / 2.54) - 60)

low = ideal * 0.9
high = ideal * 1.1

col1, col2 = st.columns(2)

with col1:
    st.metric("Minimum", f"{low:.1f} kg")

with col2:
    st.metric("Maximum", f"{high:.1f} kg")

# Summary
if st.button("Show My Summary"):
    st.subheader("Summary")
    st.write(f"👤 Name: {name}")
    st.write(f"🎂 Age: {age}")
    st.write(f"⚧ Gender: {sex}")
    st.write(f"📏 Height: {height} cm")
    st.write(f"⚖ Weight: {weight} kg")
    st.write(f"📊 BMI: {bmi:.1f}")
    st.write(f"🔥 Daily Calories: {round(calories)} kcal")
    st.write(f"🎯 Ideal Weight Range: {low:.1f} - {high:.1f} kg")

    