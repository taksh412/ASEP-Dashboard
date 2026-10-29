import streamlit as st
import enable_downloads
import pandas as pd
import plotly.graph_objects as go
from utils.data_management import show_old_new_file, process_and_rename_file
from utils.chapter_4_calculations import principal_perceptions, calculate_asep_chapter_4
from utils.chapter_5_calculations import student_growth, chapter_5_calculation
from utils.chapter_3_calculations import exam_pass_rate, calculate_asep_indicator_1a, calculate_asep_indicator_1b
from utils.chapter_6_calculations import field_supervision, chapter_4a_calculation, chapter_4b_calculation 
from utils.chapter_7_calculations import new_teacher

import plotly.express as px
import plotly.graph_objects as go
from streamlit_theme import st_theme
import base64
from streamlit_theme import st_theme
import os
import sys


# ─────────────────────────────────────────────
# DARK THEME DESIGN TOKENS
# ─────────────────────────────────────────────
BG_MAIN      = "#0D1117"   # page background
BG_CARD      = "#161B22"   # chart / card background
BG_SURFACE   = "#1C2333"   # slightly lighter surface
BORDER       = "#30363D"   # subtle border
ACCENT_BLUE  = "#58A6FF"   # bright blue for lines/accents
ACCENT_TEAL  = "#3BCEAC"   # teal for pass/positive
ACCENT_AMBER = "#F0B429"   # amber for secondary line
# TEXT_PRIMARY = "#E6EDF3"   # main text
# TEXT_MUTED   = "#FFFFFF"   # captions / axis labels
TEXT_PRIMARY = "var(--text-color)"
TEXT_MUTED   = "var(--text-color)"
GRID_COLOR   = "#21262D"   # chart gridlines

# Gauge / traffic light
GREEN  = "#2EA043"         # satisfactory  0 – 1.8
YELLOW = "#F0B429"         # developing    1.8 – 2.0
RED    = "#F85149"         # poor          2.0 – 2.5

FONT_FAMILY = "Montserrat, sans-serif"


# ─────────────────────────────────────────────
# INJECT DARK CSS
# ─────────────────────────────────────────────
DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');

/* ── root background ── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stHeader"], [data-testid="stSidebar"] {
    background-color: #0D1117 !important;
    color: #E6EDF3 !important;
    font-family: 'Montserrat', sans-serif !important;
}

/* sidebar */
[data-testid="stSidebar"] {
    background-color: #161B22 !important;
    border-right: 1px solid #30363D;
}

/* main content wrapper */
[data-testid="block-container"] { background-color: #0D1117 !important; }

/* ── typography ── */
h1, h2, h3, h4, h5, h6,
.stMarkdown p, .stCaption,
[data-testid="stMetricLabel"],
[data-testid="stMetricValue"],
[data-testid="stMetricDelta"] {
    color: var(--text-color) !important;
    font-family: 'Montserrat', sans-serif !important;
}

.stCaption { color: var(--text-color) !important; }

/* ── metric cards ── */
[data-testid="metric-container"] {
    background-color: #161B22 !important;
    border: 1px solid #30363D !important;
    border-radius: 10px !important;
    padding: 16px !important;
}
[data-testid="stMetricLabel"] { font-weight: 600 !important; }

/* ── divider ── */
hr { border-color: #30363D !important; }

/* ── tabs ── */
[data-baseweb="tab-list"] { background-color: #161B22 !important; border-bottom: 1px solid #30363D; }
[data-baseweb="tab"] { color: #8B949E !important; font-family: 'Montserrat', sans-serif !important; }
[aria-selected="true"] { color: #58A6FF !important; border-bottom: 2px solid #58A6FF !important; }

/* ── selectbox / multiselect ── */
[data-baseweb="select"] > div {
    background-color: #161B22 !important;
    border: 1px solid #30363D !important;
    color: var(--text-color) !important;
    font-family: 'Montserrat', sans-serif !important;
}

/* ── buttons ── */
.stDownloadButton > button, .stButton > button {
    background-color: #1F6FEB !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 600 !important;
}
.stDownloadButton > button:hover, .stButton > button:hover {
    background-color: #388BFD !important;
}

/* ── file uploader ── */
[data-testid="stFileUploader"] {
    background-color: #161B22 !important;
    border: 1px dashed #30363D !important;
    border-radius: 8px !important;
}

/* ── info / success / warning boxes ── */
[data-testid="stAlert"] { border-radius: 8px !important; }

/* plotly chart transparent bg */
.js-plotly-plot .plotly { background: transparent !important; }
</style>
"""

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
def sidebar_data():
    uploaded_files = st.sidebar.file_uploader(
        "Upload data", accept_multiple_files=True, label_visibility="visible"
    )
    st.session_state.uploaded_files = uploaded_files




def Data_Management():
    st.title("📁 Data Management")

    st.warning(
        "⚠️ **Rename before uploading:** The **Principal Perception Dataset** and the "
        "**New Teacher Survey Dataset** come from the *same* I2I report (New Teacher Perceptions "
        "by Candidate), so the downloaded files look identical. Please rename them manually before "
        "uploading, or the app won't be able to tell them apart:\n\n"
        "- **Principal Perception Dataset** → rename to **principal_perceptions**\n"
        "- **New Teacher Survey Dataset** → rename to **teacher_perceptions**"
    )

    with st.expander("📋 What datasets do I need? (click to expand)", expanded=True):
        st.markdown("""
Each dataset comes from a different report in **I2I**, **ECOS**, or **ResultsAnalyzer**. Here's where each one comes from, and which chapters need it.

| Dataset | Where to get it from |
|---|---|
| **Educator Details** | I2I → EPP Employment and Retention → Educator Details |
| **Exam Roster** | ResultsAnalyzer → Texas Examinee Data → Examinee Roster |
| **Principal Perception** | I2I → EPP Perception Surveys → New Teacher Perceptions by Candidate (View by Academic Year) |
| **Student Growth** | I2I → EPP Student Growth → Average Student Growth by Candidate |
| **Observation** | ECOS → EPP → ASEP → Observations Report (Academic Year 2025-26) |
| **Finishers** | ECOS → ASEP → Maint Finishers |
| **New Teacher Survey** | I2I → EPP Perception Surveys → New Teacher Perceptions by Candidate |

**Dataset requirement for each chapter**
- **Chapter 3** — Exam Roster + Educator Details
- **Chapter 4** — Principal Perception + Educator Details
- **Chapter 5** — Educator Details + Student Growth
- **Chapter 6** — Observation + Finishers
- **Chapter 7** — Educator Details + New Teacher Survey
- **Chapter 8** — All datasets
        """)


    # ── PDF: Detailed dataset download guide ──
    pdf_path = get_asset_path("utils/dataset_download_info.pdf")
    try:
        with open(pdf_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
        st.download_button(
            label="📄 Download Full Dataset Download Guide (PDF)",
            data=pdf_bytes,
            file_name="dataset_download_info.pdf",
            mime="application/pdf",
        )
        st.caption("Step-by-step instructions with screenshots for downloading each dataset from I2I, ECOS, and ResultsAnalyzer.")
    except FileNotFoundError:
        st.warning(f"⚠️ Reference guide not found at `{pdf_path}`. Please add `dataset_download_info.pdf` to that folder.")


    st.markdown("---")
    st.subheader("1️⃣ Upload Your Files")
    st.caption(
        "Upload your files below. The app automatically detects and renames each one so the "
        "dashboard can recognize it — the ➡️ arrow shows the original name on the left and the "
        "**renamed file name** on the right."
    )
    show_old_new_file()

    # st.markdown("---")
    # st.subheader("2️⃣ Download Renamed Files")
    # st.caption(
    #     "Use the button below to download your file with its corrected/renamed filename — "
    #     "click it to save the renamed file to your computer."
    # )
    # download_new_file()








indicator_1a_pedagogy = [
    "PPR EC-12",
    "PPR EC-4",
    "PPR 8-12",
    "PPR EC-6",
    "PPR 4-8"
]

indicator_1b_content = [
    "Physical Education EC-12",
    "Principal",
    "Core Sub EC-6 Science",
    "Core Sub EC-6 Soc Studies",
    "Core Sub EC-6 ELAR/STR",
    "Core Sub EC-6 Math",
    "Core Sub EC-6 FA/Hlth/PE",
    "ESL Supp",
    "Generalist EC-4",
    "History 8-12",
    "Generalist EC-6",
    "Mathematics 7-12",
    "Music EC-12",
    "Generalist 4-8",
    "ELAR/Soc Studies 4-8",
    "ELAR 7-12",
    "Art All Level",
    "Reading Specialist",
    "Core Sub EC-6 ELAR",
    "BTLPT - Spanish",
    "Science of Teaching Reading",
    "Bilingual Education Supp",
    "Science 4-8",
    "History 7-12",
    "TOPT-Spanish",
    "Bilingual Generalist EC-4",
    "Special Education EC-12",
    "School Counselor",
    "Social Studies 7-12",
    "Bilingual Generalist EC-6",
    "SPED SP EC-12",
    "Superintendent",
    "ESL/Generalist EC-6",
    "Art EC-12",
    "ELAR 8-12",
    "Mathematics/Science 4-8",
    "Life Science 8-12",
    "Physics/Math 7-12",
    "Mathematics 8-12",
    "Science 7-12",
    "Superintendent Parts I-II",
    "TX PACT: ELAR 4-8",
    "Life Science 7-12",
    "PHYSICAL EDUCATION EC-12",
    "Special Education Supp",
    "Principal Pilot",
    "TX PACT: EAS (Subtest III: Math)",
    "TX PACT: EAS (Subtest II: Writing)",
    "TX PACT: EAS (Subtest I Reading)",
    "Chemistry 7-12",
    "TX PACT: Music EC-12",
    "TX PACT: Social Studies 7-12",
    "Spanish 6-12",
    "TX PACT: ELAR 7-12",
    "TX PACT: Mathematics 4-8",
    "Social Studies 4-8",
    "LOTE-Spanish EC-12",
    "Speech 7-12",
    "Master Reading Teacher",
    "Speech 8-12",
    "ELAR 4-8",
    "Journalism 8-12",
    "TX PACT: Health EC 12",
    "Theatre EC-12",
    "TX PACT: Art EC-12",
    "Mathematics 4-8",
    "Social Studies 8-12",
    "Physical Science 8-12",
    "Master Tech Teacher EC-12",
    "TX PACT: Theatre EC-12",
    "Core Sub 4-8 Soc Studies",
    "Core Sub 4-8 Science",
    "Core Sub 4-8 ELAR",
    "Core Sub 4-8 Math",
    "Chemistry 8-12",
    "Physical Science 6-12",
    "TX PACT: History 7-12",
    "Science 8-12",
    "TX PACT: Physics 7-12",
    "TX PACT: Mathematics 7-12",
    "TX PACT: Life Science 7-12",
    "Gifted and Talented Supp",
    "TX PACT: Science 4-8",
    "TOPT-French",
    "French 6-12",
    "TX PACT: LOTE Spanish EC-12",
    "TX PACT: Physical Ed EC-12",
    "LOTE-French EC-12",
    "German 6-12",
    "TX PACT: Core Subjects 4-8",
    "TX PACT: Computer Science 8-12",
    "TX PACT: Chemistry 7–12",
    "TX PACT: Speech 7-12"
]

        







def asep_index_score(first_two_attempt_data_1a_data, first_two_attempt_data_1b_data, principal_dataset, teacher_survey_dataset, student_growth_data, field_supervision_dataset, exit_survey_dataset):
    st.title('Chapter 8 – Determination of ASEP Index Score')
    st.write(' ')

    indicator_4b_year_options = exit_survey_dataset['Data Year'].unique().tolist()
    indicator_4b_university_options = sorted(exit_survey_dataset['org_name'].unique().tolist())

    if "chapter_8_indicator_4b_year_selected" not in st.session_state:
        st.session_state.chapter_8_indicator_4b_year_selected = indicator_4b_year_options
    if "chapter_8_indicator_4b_university_selected" not in st.session_state:
        st.session_state.chapter_8_indicator_4b_university_selected = indicator_4b_university_options

    
    # ── Filters ──
    st.subheader("🔍 Filter Options:")
    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        year_filter = st.selectbox(
            "Year Filter",
            options=list(range(2016, 2027)),
            key="chapter_8_year_select",
        )
        st.session_state.chapter_8_indicator_4b_year_selected = year_filter

    with filter_col2:
        indicator_4b_university_selected = st.selectbox(
            "Indicator 4b University Options",
            options=indicator_4b_university_options,
            key="chapter_8_indicator_4b_university_selected_key",
        )
        st.session_state.chapter_8_indicator_4b_university_selected = indicator_4b_university_selected

    if year_filter:
        year_str = f"{st.session_state.chapter_8_indicator_4b_year_selected - 1}-{st.session_state.chapter_8_indicator_4b_year_selected}"
        exit_survey_dataset = exit_survey_dataset[exit_survey_dataset["Data Year"] == year_str]
    if indicator_4b_university_selected:
        exit_survey_dataset = exit_survey_dataset[exit_survey_dataset["org_name"] == st.session_state.chapter_8_indicator_4b_university_selected]

    # st.write(len(exit_survey_dataset))


    columns = [
        "ASEP Measure",
        "All",
        "Female",
        "Male",
        "African American",
        "Hispanic / Latino",
        "Other",
        "White"
    ]
    asep_df = pd.DataFrame(columns=columns)

    # ── Indicator weights ──
    indicator_1a_weight = 4
    indicator_1b_weight = 2
    indicator_2_weight = 1
    indicator_3_weight = 3
    indicator_4a_weight = 3
    indicator_4b_weight = 3
    indicator_5_weight = 2

    # ── Demographic group weights ──
    demo_weight_all = 6
    demo_weight_female = 1
    demo_weight_male = 1
    demo_weight_african_american = 1
    demo_weight_hispanic_latino = 1
    demo_weight_other = 1
    demo_weight_white = 1

    def weighted(value, *weights):
        """
        Multiply value by all given weights, but ONLY if value is a real number.
        If value is blank / None / NaN / empty string / non-numeric, return the
        literal string "<blank>" so pandas doesn't silently convert it to NaN
        when stored in a numeric column.
        """
        if value is None:
            return "<blank>"
        if isinstance(value, str):
            if value.strip() == "" or value.strip().lower() in ("<blank>", "nan", "none", "n/a"):
                return "<blank>"
        try:
            num = float(value)
        except (ValueError, TypeError):
            return "<blank>"
        if pd.isna(num):
            return "<blank>"
        result = num
        for w in weights:
            result *= w
        return result

    # For Chapter3: indicator 1a
    asep_df.loc[len(asep_df)] = [
        "1a: Certification examination results for pedagogy tests ",
        weighted(calculate_asep_indicator_1a(first_two_attempt_data_1a_data, year_filter, 85), indicator_1a_weight, demo_weight_all),
        weighted(calculate_asep_indicator_1a(first_two_attempt_data_1a_data[first_two_attempt_data_1a_data['Gender'] == 'Female'], year_filter, 85), indicator_1a_weight, demo_weight_female),
        weighted(calculate_asep_indicator_1a(first_two_attempt_data_1a_data[first_two_attempt_data_1a_data['Gender'] == 'Male'], year_filter, 85), indicator_1a_weight, demo_weight_male),
        weighted(calculate_asep_indicator_1a(first_two_attempt_data_1a_data[first_two_attempt_data_1a_data['Race/Ethnicity'] == 'Black - African American'], year_filter, 85), indicator_1a_weight, demo_weight_african_american),
        weighted(calculate_asep_indicator_1a(first_two_attempt_data_1a_data[first_two_attempt_data_1a_data['Race/Ethnicity'] == 'Hispanic - Latino'], year_filter, 85), indicator_1a_weight, demo_weight_hispanic_latino),
        weighted(calculate_asep_indicator_1a(first_two_attempt_data_1a_data[~first_two_attempt_data_1a_data['Race/Ethnicity'].isin(['Black - African American', 'Hispanic - Latino', 'White'])], year_filter, 85), indicator_1a_weight, demo_weight_other),
        weighted(calculate_asep_indicator_1a(first_two_attempt_data_1a_data[first_two_attempt_data_1a_data['Race/Ethnicity'] == 'White'], year_filter, 85), indicator_1a_weight, demo_weight_white)
    ]

    # For Chapter3: indicator 1b
    asep_df.loc[len(asep_df)] = [
        "1b: Certification examination results for content pedagogy tests ",
        weighted(calculate_asep_indicator_1b(first_two_attempt_data_1b_data, year_filter, 80), indicator_1b_weight, demo_weight_all),
        weighted(calculate_asep_indicator_1b(first_two_attempt_data_1b_data[first_two_attempt_data_1b_data['Gender'] == 'Female'], year_filter, 80), indicator_1b_weight, demo_weight_female),
        weighted(calculate_asep_indicator_1b(first_two_attempt_data_1b_data[first_two_attempt_data_1b_data['Gender'] == 'Male'], year_filter, 80), indicator_1b_weight, demo_weight_male),
        weighted(calculate_asep_indicator_1b(first_two_attempt_data_1b_data[first_two_attempt_data_1b_data['Race/Ethnicity'] == 'Black - African American'], year_filter, 80), indicator_1b_weight, demo_weight_african_american),
        weighted(calculate_asep_indicator_1b(first_two_attempt_data_1b_data[first_two_attempt_data_1b_data['Race/Ethnicity'] == 'Hispanic - Latino'], year_filter, 80), indicator_1b_weight, demo_weight_hispanic_latino),
        weighted(calculate_asep_indicator_1b(first_two_attempt_data_1b_data[~first_two_attempt_data_1b_data['Race/Ethnicity'].isin(['Black - African American', 'Hispanic - Latino', 'White'])], year_filter, 80), indicator_1b_weight, demo_weight_other),
        weighted(calculate_asep_indicator_1b(first_two_attempt_data_1b_data[first_two_attempt_data_1b_data['Race/Ethnicity'] == 'White'], year_filter, 80), indicator_1b_weight, demo_weight_white)
    ]

    # For Chapter 4: Principal survey
    asep_df.loc[len(asep_df)] = [
        "2: Principal survey ",
        weighted(calculate_asep_chapter_4(principal_dataset, year_filter, 70), indicator_2_weight, demo_weight_all),
        weighted(calculate_asep_chapter_4(principal_dataset[principal_dataset['Gender'] == 'Female'], year_filter, 70), indicator_2_weight, demo_weight_female),
        weighted(calculate_asep_chapter_4(principal_dataset[principal_dataset['Gender'] == 'Male'], year_filter, 70), indicator_2_weight, demo_weight_male),
        weighted(calculate_asep_chapter_4(principal_dataset[principal_dataset['Race/Ethnicity'] == 'Black - African American'], year_filter, 70), indicator_2_weight, demo_weight_african_american),
        weighted(calculate_asep_chapter_4(principal_dataset[principal_dataset['Race/Ethnicity'] == 'Hispanic - Latino'], year_filter, 70), indicator_2_weight, demo_weight_hispanic_latino),
        weighted(calculate_asep_chapter_4(principal_dataset[~principal_dataset['Race/Ethnicity'].isin(['Black - African American', 'Hispanic - Latino', 'White'])], year_filter, 70), indicator_2_weight, demo_weight_other),
        weighted(calculate_asep_chapter_4(principal_dataset[principal_dataset['Race/Ethnicity'] == 'White'], year_filter, 70), indicator_2_weight, demo_weight_white)
    ]

    # For Chapter 5: student growth
    if year_filter == 2025 or year_filter == 2026:
        growth_score_percentage = 60
    elif year_filter == 2027:
        growth_score_percentage = 65
    else:
        growth_score_percentage = 70

    asep_df.loc[len(asep_df)] = [
        "3: Improvement in student achievement of students taught by beginning teachers ",
        weighted(chapter_5_calculation(student_growth_data, year_filter, growth_score_percentage), indicator_3_weight, demo_weight_all),
        weighted(chapter_5_calculation(student_growth_data[student_growth_data['Gender_x'] == 'Female'], year_filter, growth_score_percentage), indicator_3_weight, demo_weight_female),
        weighted(chapter_5_calculation(student_growth_data[student_growth_data['Gender_x'] == 'Male'], year_filter, growth_score_percentage), indicator_3_weight, demo_weight_male),
        weighted(chapter_5_calculation(student_growth_data[student_growth_data['Race/Ethnicity'] == 'Black - African American'], year_filter, growth_score_percentage), indicator_3_weight, demo_weight_african_american),
        weighted(chapter_5_calculation(student_growth_data[student_growth_data['Race/Ethnicity'] == 'Hispanic - Latino'], year_filter, growth_score_percentage), indicator_3_weight, demo_weight_hispanic_latino),
        weighted(chapter_5_calculation(student_growth_data[~student_growth_data['Race/Ethnicity'].isin(['Black - African American', 'Hispanic - Latino', 'White'])], year_filter, growth_score_percentage), indicator_3_weight, demo_weight_other),
        weighted(chapter_5_calculation(student_growth_data[student_growth_data['Race/Ethnicity'] == 'White'], year_filter, growth_score_percentage), indicator_3_weight, demo_weight_white),
    ]

    # For Chapter 6: Indicator 4a
    indicator_4a_percentage = 95
    asep_df.loc[len(asep_df)] = [
        "4a: Frequency and duration of field observations ",
        weighted(chapter_4a_calculation(field_supervision_dataset, year_filter, indicator_4a_percentage), indicator_4a_weight, demo_weight_all),
        weighted(chapter_4a_calculation(field_supervision_dataset[field_supervision_dataset['Gender'] == 'F'], year_filter, indicator_4a_percentage), indicator_4a_weight, demo_weight_female),
        weighted(chapter_4a_calculation(field_supervision_dataset[field_supervision_dataset['Gender'] == 'M'], year_filter, indicator_4a_percentage), indicator_4a_weight, demo_weight_male),
        weighted(chapter_4a_calculation(field_supervision_dataset[field_supervision_dataset['Ethnicity'] == 'Black/African Amer'], year_filter, indicator_4a_percentage), indicator_4a_weight, demo_weight_african_american),
        weighted(chapter_4a_calculation(field_supervision_dataset[field_supervision_dataset['Ethnicity'] == 'Hispanic/Latino'], year_filter, indicator_4a_percentage), indicator_4a_weight, demo_weight_hispanic_latino),
        weighted(chapter_4a_calculation(field_supervision_dataset[~field_supervision_dataset['Ethnicity'].isin(['Black/African Amer', 'Hispanic/Latino', 'White'])], year_filter, indicator_4a_percentage), indicator_4a_weight, demo_weight_other),
        weighted(chapter_4a_calculation(field_supervision_dataset[field_supervision_dataset['Ethnicity'] == 'White'], year_filter, indicator_4a_percentage), indicator_4a_weight, demo_weight_white)
    ]

    # For Chapter 6: Indicator 4b
    # HERE PROBLEM IS ALL OPTION I GET <blind> SEE WHY
    indicator_4b_percentage = 90
    asep_df.loc[len(asep_df)] = [
        "4b: Quality of field supervision ",
        weighted(chapter_4b_calculation(exit_survey_dataset, year_filter, indicator_4b_percentage), indicator_4b_weight, demo_weight_all),
        weighted(chapter_4b_calculation(exit_survey_dataset[exit_survey_dataset['gender_string'] == 'Female'], year_filter, indicator_4b_percentage), indicator_4b_weight, demo_weight_female),
        weighted(chapter_4b_calculation(exit_survey_dataset[exit_survey_dataset['gender_string'] == 'Male'], year_filter, indicator_4b_percentage), indicator_4b_weight, demo_weight_male),
        weighted(chapter_4b_calculation(exit_survey_dataset[exit_survey_dataset['ethnicity_string'] == 'African American'], year_filter, indicator_4b_percentage), indicator_4b_weight, demo_weight_african_american),
        weighted(chapter_4b_calculation(exit_survey_dataset[exit_survey_dataset['ethnicity_string'] == 'Hispanic'], year_filter, indicator_4b_percentage), indicator_4b_weight, demo_weight_hispanic_latino),
        weighted(chapter_4b_calculation(exit_survey_dataset[~exit_survey_dataset['ethnicity_string'].isin(['African American', 'Hispanic', 'White'])], year_filter, indicator_4b_percentage), indicator_4b_weight, demo_weight_other),
        weighted(chapter_4b_calculation(exit_survey_dataset[exit_survey_dataset['ethnicity_string'] == 'White'], year_filter, indicator_4b_percentage), indicator_4b_weight, demo_weight_white)
    ]

    # For Chapter 7a: Teacher survey
    asep_df.loc[len(asep_df)] = [
        "5: Teacher Survey ",
        weighted(calculate_asep_chapter_4(teacher_survey_dataset, year_filter, 70), indicator_5_weight, demo_weight_all),
        weighted(calculate_asep_chapter_4(teacher_survey_dataset[teacher_survey_dataset['Gender'] == 'Female'], year_filter, 70), indicator_5_weight, demo_weight_female),
        weighted(calculate_asep_chapter_4(teacher_survey_dataset[teacher_survey_dataset['Gender'] == 'Male'], year_filter, 70), indicator_5_weight, demo_weight_male),
        weighted(calculate_asep_chapter_4(teacher_survey_dataset[teacher_survey_dataset['Race/Ethnicity'] == 'Black - African American'], year_filter, 70), indicator_5_weight, demo_weight_african_american),
        weighted(calculate_asep_chapter_4(teacher_survey_dataset[teacher_survey_dataset['Race/Ethnicity'] == 'Hispanic - Latino'], year_filter, 70), indicator_5_weight, demo_weight_hispanic_latino),
        weighted(calculate_asep_chapter_4(teacher_survey_dataset[~teacher_survey_dataset['Race/Ethnicity'].isin(['Black - African American', 'Hispanic - Latino', 'White'])], year_filter, 70), indicator_5_weight, demo_weight_other),
        weighted(calculate_asep_chapter_4(teacher_survey_dataset[teacher_survey_dataset['Race/Ethnicity'] == 'White'], year_filter, 70), indicator_5_weight, demo_weight_white)
    ]

    # Safety net: replace any leftover NaN with visible "<blank>" text before display
    asep_df = asep_df.fillna("<blank>")
    st.markdown(asep_df.to_html(index=False), unsafe_allow_html=True)

    # ── Total ASEP Index Score ──
    # Sum every numeric cell across the WHOLE table (all demographic columns, all chapter rows).
    # Blank / None / NaN / non-numeric cells are simply skipped, not treated as 0-that-gets-multiplied.
    # ── Total ASEP Index Score ──
    value_columns = ["All", "Female", "Male", "African American", "Hispanic / Latino", "Other", "White"]
    total_asep_score = pd.to_numeric(
        asep_df[value_columns].stack(), errors='coerce'
    ).sum()

    st.write(f"**Total ASEP Index Score (sum of all table values):** {total_asep_score}")
    asep_index_score_value = round((total_asep_score / 182)*100, 2)
    st.write(f"**ASEP Index Score:** {asep_index_score_value}")

    # ══════════════════════════════════════════
    # ASEP Index Score Gauge (Ch.5 style theme)
    # ══════════════════════════════════════════
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("ASEP Index Score")
        st.caption(
            "🟢 Green = 85% or more  |  🟡 Yellow = 80% to less than 85%  |  🔴 Red = Below 80%. "
            f"(Current ASEP Index Score: {asep_index_score_value}%)"
        )

        if asep_index_score_value >= 85:
            gauge_color = GREEN
        elif asep_index_score_value >= 80:
            gauge_color = YELLOW
        else:
            gauge_color = RED

        theme = st_theme(key="theme_chapter_8")
        is_light = theme and theme.get("base") == "light"

        gauge_fill_color   = "#FFFFFF" if is_light else "#000000"   # white fill in light theme
        gauge_border_color = "#000000" if is_light else "#FFFFFF"   # black border in light theme

        fig_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=asep_index_score_value,
                number=dict(
                    font=dict(size=52, color=gauge_border_color),
                    suffix="%",
                ),
                domain={"x": [0, 1], "y": [0, 1]},
                gauge={
                    "axis": {
                        "range": [0, 100],
                        "tickwidth": 1,
                        "tickcolor": gauge_border_color,
                        "tickfont": {"color": gauge_border_color},
                    },
                    "bar": {"color": gauge_color},
                    "bgcolor": gauge_fill_color,
                    "borderwidth": 2,
                    "bordercolor": gauge_border_color,
                    "steps": [
                        {"range": [0, 80],   "color": gauge_fill_color},
                        {"range": [80, 85],  "color": gauge_fill_color},
                        {"range": [85, 100], "color": gauge_fill_color},
                    ],
                },
            )
        )
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            height=300,
            margin=dict(l=0, r=0, t=30, b=10),  # Removes side margins pushing it off-center
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

# ─────────────────────────────────────────────
# STUDENT GROWTH TAB
# ─────────────────────────────────────────────
def student_growth_tab(df):
    st.subheader("📚 Indicator 3: Student Growth")
    


# ─────────────────────────────────────────────
# EXAM PASS RATE TAB
# ─────────────────────────────────────────────
def exam_pass_rate_tab(df):
    st.subheader("🏆 Indicator 1: Certification Exam Pass Rates")
    

def Feedback():
    import streamlit as st
    import streamlit.components.v1 as components

    st.set_page_config(layout="wide")

    # st.title("📬 Submit Dashboard Feedback")
    # st.markdown("""
    # Please use the form below to report any **errors**, suggest **changes**, or request future **updates**. 
    # Your input helps improve the local dashboard experience!
    # """)

    # 1. Increased the iframe height property to 1200px
    ms_form_iframe = """
    <iframe src="https://forms.cloud.microsoft/Pages/ResponsePage.aspx?id=X505YZwk0ESyca3Ch_Mj_8Qon6bq6RdOvMeTNsPMoKRUMEtZRE85U05NTlFQNzZCVzI3Rjk3VVRXSy4u&embed=true" 
        width="100%" 
            height="1200px" 
            frameborder="0" 
            marginwidth="0" 
            marginheight="0" 
            style="border: none; max-width:100%; min-height: 1200px; background: transparent;" 
            allowfullscreen 
            webkitallowfullscreen 
            mozallowfullscreen 
            msallowfullscreen>
        </iframe>
    """

    col1, col2, col3 = st.columns([1, 4, 1])

    with col2:
        # 2. CRUCIAL: Increased the Streamlit component container height to 1250px 
        # to perfectly match the iframe and prevent clipping.
        components.html(ms_form_iframe, height=1250, scrolling=True)

# ─────────────────────────────────────────────
# DASHBOARD PAGE
# ─────────────────────────────────────────────
def Dashboard():
    st.title("📊 ASEP Metrics Dashboard")
    st.caption(
        "Alternative Student Educator Preparation (ASEP) program metrics"
    )

    if not st.session_state.get("uploaded_files"):
        st.warning("Please upload Excel files in the Data Management page first.")
        return

    data = {
        "principal_perception": None,
        "educator_details": None,
        "student_growth": None,
        "new_teacher_survey": None,
        "exam_roaster": None,
        "observation_data": None,
        "main_finisher_data": None,
        "exit_survey_data": None
    }

    NAME_TO_KEY = {
        "principal_perceptions": "principal_perception",
        "educator_details_with_emp_start_date": "educator_details",
        "academic_year_average_student_growth_by_candidate": "student_growth",
        "teacher_perceptions": "new_teacher_survey",
        "exam_roaster_data": "exam_roaster",
        "observation_df": "observation_data",
        "main_finisher_data": "main_finisher_data",
        "exit_survey_dataset": "exit_survey_data"
    }

    # 1. Process every uploaded file once, group results by output name
    grouped = {}
    for uploaded_file in st.session_state.uploaded_files:
        new_name, df = process_and_rename_file(uploaded_file)
        grouped.setdefault(new_name, []).append(df)

    # 2. Concat any name that has multiple files behind it (e.g. multi-year
    #    Finisher files), otherwise just use the single df
    for new_name, dfs in grouped.items():
        key = NAME_TO_KEY.get(new_name)
        if key is None:
            continue  # unrecognized schema, skip
        merged_df = pd.concat(dfs, ignore_index=True) if len(dfs) > 1 else dfs[0]
        data[key] = merged_df

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["Chapter 3", "Chapter 4", "Chapter 5", "Chapter 6", "Chapter 7", "Chapter 8"]
    )
    first_two_attempt_data_1a_data = None 
    first_two_attempt_data_1b_data = None
    principal_dataset = None
    teacher_survey_dataset = None
    student_growth_data = None
    field_supervision_dataset = None
    exit_survey_dataset = None
    
    with tab1:
        if data["exam_roaster"] is not None and data['educator_details'] is not None:
            first_two_attempt_data_1a_data, first_two_attempt_data_1b_data, _ = exam_pass_rate(data["exam_roaster"], data["educator_details"])
        else:
            if data["exam_roaster"] is not None:
                st.info("⚠️ Please upload a Educator Details file first.")
            elif data['educator_details'] is not None:
                st.info("⚠️ Please upload a Examinee Roster file first.")

    with tab2:
        if data["principal_perception"] is not None and data['educator_details'] is not None:
            principal_dataset = principal_perceptions(data["principal_perception"], data["educator_details"])
        else:
            if data["principal_perception"] is not None:
                st.info("⚠️ Please upload a Educator Details file first.")
            elif data['educator_details'] is not None:
                st.info("⚠️ Please upload a Principal Perceptions file first.")

    with tab3:
        if data["educator_details"] is not None and data['student_growth'] is not None:
            student_growth_data = student_growth(data["educator_details"], data["student_growth"])
        else:
            if data["educator_details"] is not None:
                st.info("⚠️ Please upload a Student Growth file first.")
            elif data['student_growth'] is not None:
                st.info("⚠️ Please upload a Educator Details file first.")

    with tab4:
        if data['observation_data'] is not None and data['main_finisher_data'] is not None and data['exit_survey_data'] is not None:
            field_supervision_dataset, exit_survey_dataset = field_supervision(data['observation_data'], data['main_finisher_data'], data['exit_survey_data'])
        else:
            if data['observation_data'] is None:
                st.info("⚠️ Please upload an Observations Data file first.")
            if data['main_finisher_data'] is None:
                st.info("⚠️ Please upload a Main Finisher file first.")
            if data['exit_survey_data'] is None:
                st.info("⚠️ Please upload an Exit Survey file first.")

    with tab5:
        if data["new_teacher_survey"] is not None and data['educator_details'] is not None:
            teacher_survey_dataset = new_teacher(data["new_teacher_survey"], data["educator_details"])
        else:
            if data["new_teacher_survey"] is not None:
                st.info("⚠️ Please upload a Educator Details file first.")
            elif data['educator_details'] is not None:
                st.info("⚠️ Please upload a New Teacher Survey file first.")

    with tab6:
        if first_two_attempt_data_1a_data is not None and first_two_attempt_data_1b_data is not None and principal_dataset is not None and teacher_survey_dataset is not None and student_growth_data is not None and field_supervision_dataset is not None and exit_survey_dataset is not None:
            asep_index_score(first_two_attempt_data_1a_data, first_two_attempt_data_1b_data, principal_dataset, teacher_survey_dataset, student_growth_data, field_supervision_dataset, exit_survey_dataset)
        else:
            st.info("⚠️ Please ensure the required files are uploaded to populate this tab.")



def get_asset_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller temporary extraction directory
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def About_us():
    theme = st_theme()
    is_light = theme and theme.get("base") == "light"

    logo_filename = (
        "images/black_company_logo.png"
        if is_light
        else "images/white_company_logo.png"
    )

    # Dynamically resolve path whether frozen or in dev mode
    logo_path = get_asset_path(logo_filename)

    with open(logo_path, "rb") as img_file:
        logo_base64 = base64.b64encode(img_file.read()).decode()

    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/png;base64,{logo_base64}" width="300">
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ---------------- Background ----------------
    st.markdown(
        """
        <h4>📖 Background</h4>
        <p style="line-height: 1.7; font-size: 17px; color: var(--text-color);">
            The ASEP Data Dashboard was developed in support of the
            <a href="https://elevatetxed.utsystem.edu/" target="_blank">UT System's ElevateTXed initiative</a>.
            The ASEP Data Dashboard was envisioned and collaboratively designed by the
            I2I Data Workgroup (members below). The primary goal of this project is to enhance
            the capacity of educator preparation programs (EPPs) to use data for continuous
            improvement, informed decision-making, and alignment with state accountability metrics.
        </p>
        <p style="line-height: 1.7; font-size: 17px; color: var(--text-color);">
            This software will allow users to securely upload raw data files from multiple TEA
            sources, including I2I, ECOS, ResultsAnalyzer, and others, and automatically convert
            those files into EPP-specific dashboards in alignment with the
            <a href="https://tea.texas.gov/educators/preparation-and-continuing-education/consumer-information-about-educator-preparation-programs/24-25-asep-manual.pdf" target="_blank">
            24-25 Texas Accountability System for Educator Preparation Manual</a>.
            The intent of this dashboard is to aggregate these disparate data sources into a
            unified environment, directly aligned with ASEP standards, using real-time,
            student-level data. Our hope is that this tool will enable EPPs to monitor progress
            on accountability benchmarks and serve as an early warning system to identify areas
            of strength and risk.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ---------------- Data Security ----------------
    st.markdown(
        """
        <div style="background-color: #262730; padding: 20px; border-radius: 10px; border: 1px solid var(--text-color);">
            <h4 style="color: #ffffff;">🔒 Data Security</h4>
            <p style="color: #dddddd; font-size: 17px; line-height: 1.7;">
                When running the desktop version of this application, data files will never leave
                your hard drive. The software is designed to run entirely locally so that private
                student information never leaves the environment from which it was originally
                downloaded. The software neither operates nor stores data in any environment other
                than where you originally downloaded the files.
            </p>
            
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ---------------- I2I Workgroup Members ----------------
    st.markdown(
        """
        <h4>👥 I2I Workgroup Members</h4>
        <p style="line-height: 1.7; font-size: 17px; color: var(--text-color);">
            The workgroup was initiated by the UT System's ElevateTXed initiative and has evolved
            to include participants from multiple institutions and systems, reflecting its
            broader statewide scope:
        </p>
        <ul style="line-height: 1.9; font-size: 17px; color: var(--text-color);">
            <li><strong>Taksh Beladiya</strong> — Graduate Research Assistant, The University of Texas System</li>
            <li><strong>Kevin Badgett</strong> — Dean, College of Education, Sul Ross State University</li>
            <li><strong>Michelle Lowry</strong> — Senior Software Developer/Analyst, UTeach, The University of Texas at Austin</li>
            <li><strong>Michael Marder</strong> — Executive Director, UTeach Natural Sciences, The University of Texas at Austin</li>
            <li><strong>Jeremy Martin</strong> — Senior Research & Policy Analyst, The University of Texas System</li>
            <li><strong>Emma Savage-Davis</strong> — Dean, College of Education and Human Development, TAMU-San Antonio</li>
            <li><strong>Robin Kapavik</strong> — Associate Dean, College of Education and Human Development, TAMU-San Antonio</li>
        </ul>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ---------------- Contact ----------------
    st.markdown(
        """
        <h4>✉️ Contact</h4>
        <p style="line-height: 1.7; font-size: 17px; color: var(--text-color);">
            For questions or comments, please contact Jeremy Martin at
            <a href="mailto:jemartin@utsystem.edu">jemartin@utsystem.edu</a>.
        </p>
        <p style="line-height: 1.7; font-size: 17px; color: var(--text-color);">
            For source code and pull requests, please visit Taksh Beladiya's GitHub page at
            <a href="https://github.com/takshb21/asep_dashboard" target="_blank">github.com/takshb21/asep_dashboard</a>.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

        # ---------------- Next Steps ----------------
    st.markdown("<h4>➡️ Next Steps</h4>", unsafe_allow_html=True)

    nav_flow_css = """
    <style>
    .nav-flow {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: center;
        gap: 8px;
        margin: 20px 0;
    }
    .nav-step {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.3);
        border-radius: 10px;
        padding: 16px 18px;
        width: 300px;
        min-height: 130px;
        text-align: center;
    }
    .nav-step .step-icon {
        font-size: 30px;
        margin-bottom: 6px;
    }
    .nav-step .step-title {
        color: #58A6FF;
        font-weight: 700;
        font-size: 20px;
        margin-bottom: 6px;
    }
    .nav-step .step-desc {
        color: var(--text-color);
        font-size: 17px;
        line-height: 1.4;
    }
    .nav-arrow {
        font-size: 28px;
        color: #F0B429;
        font-weight: bold;
    }
    </style>
    """

    nav_flow_html = """
    <div class="nav-flow">
        <div class="nav-step">
            <div class="step-icon">📁</div>
            <div class="step-title">1. Data Management</div>
            <div class="step-desc">On your left, click "Data Management." Upload your Excel/CSV files there, and rename any files if prompted.</div>
        </div>
        <div class="nav-arrow">➡️</div>
        <div class="nav-step">
            <div class="step-icon">✅</div>
            <div class="step-title">2. Confirm Files</div>
            <div class="step-desc">Check the ➡️ arrow list to confirm your files were renamed correctly.</div>
        </div>
        <div class="nav-arrow">➡️</div>
        <div class="nav-step">
            <div class="step-icon">📊</div>
            <div class="step-title">3. Dashboard</div>
            <div class="step-desc">Open each Chapter tab — it auto-fills once the right files are uploaded.</div>
        </div>
        <div class="nav-arrow">➡️</div>
        <div class="nav-step">
            <div class="step-icon">🏆</div>
            <div class="step-title">4. Chapter 8 Score</div>
            <div class="step-desc">View the final combined ASEP Index Score.</div>
        </div>
        <div class="nav-arrow">➡️</div>
        <div class="nav-step">
            <div class="step-icon">💬</div>
            <div class="step-title">5. Feedback</div>
            <div class="step-desc">Report issues or request changes anytime.</div>
        </div>
    </div>
    """

    st.markdown(nav_flow_css, unsafe_allow_html=True)
    st.markdown(nav_flow_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="ASEP Metrics Dashboard",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    
    sidebar_data()

    pages = [st.Page(About_us, title="About Us", default=True),
        st.Page(Data_Management, title="Data Management"),
        st.Page(Dashboard, title="Dashboard"),  
        st.Page(Feedback, title="Feedback"),
    ]
    pg = st.navigation(pages)
    pg.run()


main()