
import streamlit as st
import pandas as pd
import joblib
import sklearn
import sys

print("PYTHON:", sys.version)
print("SCIKIT-LEARN:", sklearn.__version__)

st.set_page_config(
    page_title="EcoPulse Iași",
    page_icon="🌿",
    layout="centered"
)

@st.cache_resource
def load_model():
    return joblib.load("ecopulse_model_compressed.joblib")

model = load_model()

st.title("🌿 EcoPulse Iași")
st.subheader("Înțelege impactul emisiilor vehiculului tău")

st.write(
    "Introdu caracteristicile mașinii pentru a estima "
    "emisiile sale de CO₂ la țeava de eșapament."
)

st.info(
    "Această estimare se bazează pe date standardizate "
    "despre vehicule. Nu reprezintă o măsurătoare a "
    "calității aerului din Iași."
)

with st.form("vehicle_form"):
    year = st.number_input(
        "Anul modelului",
        min_value=1980,
        max_value=2027,
        value=2020,
        step=1
    )

    displ = st.number_input(
        "Cilindreea motorului (litri)",
        min_value=0.0,
        max_value=10.0,
        value=2.0,
        step=0.1
    )

    cylinders = st.number_input(
        "Numărul de cilindri",
        min_value=0,
        max_value=16,
        value=4,
        step=1
    )

    comb08 = st.number_input(
        "Consum combinat (MPG)",
        min_value=1,
        max_value=150,
        value=30,
        step=1,
        help="MPG înseamnă mile per galon american."
    )

    distance = st.number_input(
        "Distanța parcursă (km)",
        min_value=1.0,
        max_value=2000.0,
        value=10.0,
        step=1.0
    )

    submitted = st.form_submit_button(
        "Estimează emisiile"
    )

if submitted:
    vehicle = pd.DataFrame([{
        "year": year,
        "displ": displ,
        "cylinders": cylinders,
        "comb08": comb08
    }])

    emission_rate = float(model.predict(vehicle)[0])
    emission_rate = max(0, emission_rate)

    emissions_per_km = emission_rate / 1.609344
    trip_emissions = emissions_per_km * distance

    st.divider()
    st.subheader("Rezultatul estimării")

    col1, col2 = st.columns(2)

    col1.metric(
        "Emisii estimate",
        f"{emissions_per_km:.1f} g CO₂/km"
    )

    col2.metric(
        "Pentru distanța introdusă",
        f"{trip_emissions:.1f} g CO₂"
    )

    st.caption(
        "Rezultatul este o estimare a emisiilor vehiculului, "
        "nu o măsurătoare directă. Precizia depinde de "
        "datele de antrenare și de caracteristicile introduse."
    )

st.divider()
st.caption("EcoPulse Iași | Prototip educațional pentru hackathon")

