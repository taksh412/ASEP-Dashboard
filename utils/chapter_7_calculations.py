import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils.chapter_4_calculations import merge_both_df, get_asep_consolidated_data, verify_certificate, missing_required_sections, remove_duplicates, chapter_4_chart, specific_year_data, chapter_4_group_aggregration

# @st.cache_data
def prepare_chapter_7(new_teacher_survey_df, educator_df):
    merged = merge_both_df(new_teacher_survey_df, educator_df)
    merged = get_asep_consolidated_data(merged)
    merged = verify_certificate(merged)
    merged = missing_required_sections(merged)
    merged = remove_duplicates(merged)
    return merged


def new_teacher(new_teacher_survey_df, educator_details_df):
    st.title('Chapter 7 – Evaluation of Educator Preparation Programs by Teachers (Teacher Survey)')
    st.write(' ')
    merged = prepare_chapter_7(new_teacher_survey_df, educator_details_df)

    available_cohort_options = sorted(merged["Admission Cohort"].unique().astype(int).tolist())
    available_employment_options = sorted(merged['Employment Date'].dt.year.astype(int).unique().tolist())

    if "chapter_7_cohort_filter" not in st.session_state:
        st.session_state.chapter_7_cohort_filter = available_cohort_options  # Or [2019, 2020, 2021] depending on your default target
        
    if "chapter_7_gender_filter" not in st.session_state:
        st.session_state.chapter_7_gender_filter = "All"

    if "chapter_7_employment_date" not in st.session_state:
        st.session_state.chapter_7_employment_date = available_employment_options


    # # ── Filters ──
    st.subheader("🔍 Filter Options: Teacher Survey (ASEP Accountability Indicator 5) ")
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        gender_selected = st.selectbox(
            "Gender",
            options=["All"] + sorted(merged["Gender"].unique().tolist()),
            key="chapter_7_gender_select",
        )
        st.session_state.chapter_7_gender_filter = gender_selected

    with filter_col2:
        admission_cohort = st.multiselect(
            "Admission Cohort Year",
            options=available_cohort_options,
            default=st.session_state.chapter_7_cohort_filter,
            key="chapter_7_cohort_select",
        )
        
        # If the user changes selection, trigger a rerun so the preprocessor runs with new years
        if admission_cohort != st.session_state.chapter_7_cohort_filter:
            st.session_state.chapter_7_cohort_filter = admission_cohort
            # st.rerun()

    with filter_col3:
        employment_date_selected = st.selectbox(
            "Employment Date",
            options=available_employment_options,
            # default=st.session_state.chapter_7_employment_date,
            key="chapter_7_emp_date_select"
        )

        if employment_date_selected != st.session_state.chapter_7_employment_date:
            st.session_state.chapter_7_employment_date = employment_date_selected

    filtered_copy_df = merged.copy()
    if gender_selected != "All":
        filtered_copy_df = filtered_copy_df[filtered_copy_df["Gender"] == gender_selected]
    if admission_cohort:
        filtered_copy_df = filtered_copy_df[filtered_copy_df["Admission Cohort"].isin(admission_cohort)]
    filtered_copy_df = specific_year_data(filtered_copy_df, st.session_state.chapter_7_employment_date)


    filtered_copy_df, total_records = chapter_4_group_aggregration(filtered_copy_df, employment_date_selected)
    # if years_checked > 1 and total_records > 0:
    st.info(
        f"ℹ️ **Small Group Aggregation Applied:** Initial cohort was under 10. "
        f"Total evaluation sample size: **{total_records}**."
    )

    # st.write('len of filtered data is ', len(filtered_copy_df))
    if total_records != 0:
        chapter_4_chart(filtered_copy_df, key_suffix="chapter_7")
    else:
        st.info('Select Other Year No Record Found')

    return merged