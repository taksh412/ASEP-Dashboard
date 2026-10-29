# ─────────────────────────────────────────────
# FILE PROCESSING
# ─────────────────────────────────────────────
import os
import re
import io
import pandas as pd
import streamlit as st

# ─────────────────────────────────────────────
# FINISHER FILE DETECTION + READING
# ─────────────────────────────────────────────
FINISHER_COLUMNS = [
    'TEA ID',
    'SSN',
    'First Name',
    'Middle Name',
    'Last Name',
    'Cert Code',
    'Cert Description',
    'Program Type',
    'Gender',
    'Ethnicity',
    'Status',
]


def is_finisher_file(uploaded_file) -> bool:
    """Peek at the file's real header row (row 3, i.e. skiprows=2) to see
    if it matches the SBEC ASEP Finisher schema."""
    uploaded_file.seek(0)
    try:
        if uploaded_file.name.lower().endswith('.csv'):
            df_check = pd.read_csv(uploaded_file, skiprows=2, nrows=0)
        else:
            df_check = pd.read_excel(uploaded_file, skiprows=2, nrows=0, engine='calamine')
    except Exception:
        uploaded_file.seek(0)
        return False
    uploaded_file.seek(0)
    cols_check = sorted([str(c).strip() for c in df_check.columns])
    return cols_check == sorted(FINISHER_COLUMNS)


def read_finisher_file(uploaded_file) -> pd.DataFrame:
    """Extracts 'Data year' from row 1 and parses the table starting after
    the header row (skiprows=2)."""
    is_csv = uploaded_file.name.lower().endswith('.csv')

    # 1. Extract the year from the first cell of row 1
    uploaded_file.seek(0)
    if is_csv:
        header_text_df = pd.read_csv(uploaded_file, nrows=1, header=None)
    else:
        header_text_df = pd.read_excel(uploaded_file, nrows=1, header=None, engine='calamine')

    first_cell_value = str(header_text_df.iloc[0, 0])
    year_match = re.search(r'(\d{4})', first_cell_value, re.IGNORECASE)
    data_year = int(year_match.group(1)) if year_match else None

    # 2. Read the actual table (headers on row 3 -> skiprows=2)
    uploaded_file.seek(0)
    if is_csv:
        df = pd.read_csv(uploaded_file, skiprows=2)
    else:
        df = pd.read_excel(uploaded_file, skiprows=2, engine='calamine')

    df.columns = [str(col).strip() for col in df.columns]

    if 'TEA ID' in df.columns:
        df = df[df['TEA ID'].notna()].copy()

    # 3. Tag each row with its source year
    df['Data year'] = data_year
    return df


def extract_exit_survey_year(filename: str) -> str:
    """Extracts the academic school year from an exit survey filename."""
    name = filename.lower().rsplit(".", 1)[0]
    name = re.sub(r"[_\s]+", "-", name)

    # 1. Special case: "...2021-to-post..." style files -> 2020-2021
    post_match = re.search(r"(\d{4})-to-post", name)
    if post_match:
        end_year = int(post_match.group(1))
        start_year = end_year - 1
        return f"{start_year}-{end_year}"

    # 2. General case: "...-21-22" / "...-24-25" style files
    range_match = re.search(r"(\d{2})-(\d{2})(?:-|$)", name[::-1])
    if range_match:
        end_yy = range_match.group(1)[::-1]
        start_yy = range_match.group(2)[::-1]
        start_year = 2000 + int(start_yy)
        end_year = 2000 + int(end_yy)
        return f"{start_year}-{end_year}"

    return None


def process_and_rename_file(uploaded_file):
    """Processes a SINGLE uploaded file, assigns proper column schemas and metadata."""
    index_name = [
        "Field Supervisor Last Name",
        "Field Supervisor First Name",
        "Assignment Begin Date",
        "Candidate TEA ID",
        "Candidate Last Name",
        "Candidate First Name",
        "Visit Date",
        "Duration Hours",
        "Comments",
        "Field Supervisor TEA ID",
        "Assignment Type",
        "Experience Model",
        "Assignment End Date",
        "Observation Setting",
    ]

    uploaded_file.seek(0)

    # 0. Finisher files check
    if is_finisher_file(uploaded_file):
        df = read_finisher_file(uploaded_file)
        new_name = "main_finisher_data"
        return new_name, df

    # Read file content based on extension
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file, skiprows=10)
        df.columns = index_name
    else:
        df = pd.read_excel(uploaded_file, skipfooter=2, engine="calamine")

    # Standardize column whitespace
    df.columns = [str(col).strip() for col in df.columns]
    cols = sorted(df.columns)

    # 1. Manual Collisions
    if "principal_perceptions" in uploaded_file.name.lower():
        new_name = "principal_perceptions"
    elif "teacher_perceptions" in uploaded_file.name.lower():
        new_name = "teacher_perceptions"

    # 2. Exit Survey Handling
    elif "exit-survey" in uploaded_file.name.lower() or (
        "county_org_cd" in [c.lower() for c in df.columns]
    ):
        new_name = "exit_survey_dataset"

        # Standardize column casing ('Gender' -> 'gender', 'Ethnicity' -> 'ethnicity')
        df.columns = [
            col.lower() if col.lower() in ["gender", "ethnicity"] else col
            for col in df.columns
        ]

        # Extract and assign Data Year
        data_year = extract_exit_survey_year(uploaded_file.name)
        if data_year is None:
            st.warning(
                f"Couldn't parse a Data Year from filename: {uploaded_file.name}"
            )

        df["Data Year"] = data_year
        return new_name, df

    # 3. Other Data Schemas
    elif cols == sorted(
        [
            "TEA ID",
            "Employment Date",
            "Certification Type",
            "Name",
            "Race/Ethnicity",
            "Gender",
            "Certification Date",
            "Position",
            "District",
            "Campus",
            "Title I Designation",
            "Certification Grade Level",
            "Certification Subject Area",
            "Teaching Grade Level",
            "Teaching Subject Area",
        ]
    ):
        new_name = "educator_details_with_emp_start_date"

    elif cols == sorted(
        [
            "TEA ID",
            "First Name",
            "Last Name",
            "Finisher Year",
            "Gender",
            "Race/ Ethnicity",
            "Certification Area Grade Level",
            "Year of Teaching",
            "Data Year",
            "Overall Student Growth Score",
            "Mathematics Student Growth Score",
            "Mathematics N",
            "English/ Reading Student Growth Score",
            "English/ Reading N",
        ]
    ):
        new_name = "academic_year_average_student_growth_by_candidate"

    elif cols == sorted(
        [
            "Examinee Name",
            "TEAID",
            "Exam Name",
            "Exam Code",
            "Exam Version",
            "Exam Date",
            "P/F Status",
            "Reporting Type",
            "Score Report Finder",
        ]
    ):
        new_name = "exam_roaster_data"

    elif cols == sorted(index_name):
        new_name = "observation_df"

    # Fallback
    else:
        new_name = uploaded_file.name

    return new_name, df


# ─────────────────────────────────────────────
# GROUPING / MERGING LOGIC
# ─────────────────────────────────────────────
def get_grouped_dataframes():
    """Processes all uploaded files, groups them by output dataset name,
    and cleanly concatenates multi-year uploads without duplicate reads."""
    uploaded_files = st.session_state.get("uploaded_files", [])
    grouped = {}

    for uploaded_file in uploaded_files:
        new_name, df = process_and_rename_file(uploaded_file)
        grouped.setdefault(new_name, []).append(df)

    merged = {}
    for name, dfs in grouped.items():
        merged[name] = pd.concat(dfs, ignore_index=True) if len(dfs) > 1 else dfs[0]

    return merged


# ─────────────────────────────────────────────
# DATA MANAGEMENT PAGE
# ─────────────────────────────────────────────
def show_old_new_file():
    uploaded_files = st.session_state.get("uploaded_files", [])
    if not uploaded_files:
        st.write("Upload your Files First")
    else:
        for uploaded_file in uploaded_files:
            new_name, _ = process_and_rename_file(uploaded_file)
            col1, col2, col3 = st.columns([4, 1, 4])
            with col1:
                st.info(f"{uploaded_file.name}")
            with col2:
                st.markdown(
                    "<h2 style='text-align:center;margin-top:-10px;color:#E6EDF3;'>→</h2>",
                    unsafe_allow_html=True,
                )
            with col3:
                st.success(f"{new_name}")


def download_new_file():
    uploaded_files = st.session_state.get("uploaded_files", [])
    if uploaded_files:
        st.subheader("Download file")
        grouped = get_grouped_dataframes()  # Cleanly merges same-name files (e.g. Exit Survey years, Finisher years)
        for idx, (new_name, df) in enumerate(grouped.items()):
            buffer = io.BytesIO()
            file_name = new_name if new_name.endswith(('.csv', '.xlsx')) else f"{new_name}.csv"
            if file_name.endswith(".csv"):
                csv_data = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label=f"Download {file_name}",
                    data=csv_data,
                    file_name=file_name,
                    mime="text/csv",
                    key=f"dl_{idx}_{file_name}",
                )
            else:
                with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                    df.to_excel(writer, index=False, sheet_name="Sheet1")
                st.download_button(
                    label=f"Download {file_name}",
                    data=buffer.getvalue(),
                    file_name=file_name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"dl_{idx}_{file_name}",
                )