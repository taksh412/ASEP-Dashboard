import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# exam_roaster_sub_name = exam_data['Exam Name'].unique().tolist()

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


def merge_chapter_3_data(exam_data, emp_data):
    data = emp_data.sort_values(by=['TEA ID', 'Employment Date'], ascending=False)

    # 3. Drop duplicates, keeping only the 'last' occurrence for each TEA ID
    data = data.drop_duplicates(subset='TEA ID', keep='first')

    # Optional: Reset the index for a clean dataframe
    emp_data = data.reset_index(drop=True)

    merge_data = emp_data.merge(
        exam_data.rename(columns={'TEAID': 'TEA ID'}), 
        on='TEA ID', 
        how='inner'
    )

   
    return merge_data



def get_first_attempts_data(merge_data):

    # Step 1: Ensure the Exam Date is in datetime format so it sorts correctly
    merge_data['Exam Date'] = pd.to_datetime(merge_data['Exam Date'])

    # Step 2: Sort by TEA ID, Exam Name, and Exam Date (Ascending = True for earliest first)
    sorted_data_chronological = merge_data.sort_values(
        by=['TEA ID', 'Exam Name', 'Exam Date'], 
        ascending=True
    )

    # Step 3: Group by TEA ID and Exam Name, then take the first 2 rows for each group
    first_two_attempts = sorted_data_chronological.groupby(['TEA ID', 'Exam Name']).head(2)

    return first_two_attempts

def group_size_calculate(df):
    return df['TEA ID'].nunique()

def indicator_1a_data(first_two_attempt_data, year_filter):

    test_view = first_two_attempt_data[first_two_attempt_data['Exam Name'].isin(indicator_1a_pedagogy)]
    combined_df = pd.DataFrame()
    year_taken = []

    for i in range(3):
        year_data = test_view[test_view['Exam Date'].dt.year == (year_filter - i)]
        combined_df = pd.concat([combined_df, year_data])
        year_taken.append(year_filter-i)
        if group_size_calculate(combined_df) >= 10:
            break
    
    return combined_df, year_taken

def indicator_1a_data_last_3_year_data(first_two_attempt_data, year_filter):
    test_view = first_two_attempt_data[first_two_attempt_data['Exam Name'].isin(indicator_1a_pedagogy)]
    first_year_df = test_view[test_view['Exam Date'].dt.year == (year_filter)]
    second_year_df = test_view[test_view['Exam Date'].dt.year == (year_filter - 1)]
    third_year_df = test_view[test_view['Exam Date'].dt.year == (year_filter - 2)]

    return first_year_df, second_year_df, third_year_df

def calculate_asep_indicator_1a_calculation(df, tea_id_col='TEA ID', exam_name_col='Exam Name', 
                                exam_date_col='Exam Date', status_col='P/F Status'):
    
    # Chronologically number each attempt (1, 2, 3...) per candidate per exam
    df['Attempt'] = df.groupby([tea_id_col, exam_name_col]).cumcount() + 1
    
    passed_1st_or_2nd = 0  # Numerator
    total_tracked_attempts = 0  # Denominator
    
    # Evaluate the first two attempts for each unique candidate-exam combination
    for (_, _), group in df.groupby([tea_id_col, exam_name_col]):
        # Extract the 1st and 2nd attempts
        attempt_1 = group[group['Attempt'] == 1]
        attempt_2 = group[group['Attempt'] == 2]
        
        if attempt_1.empty:
            continue
            
        status_1 = attempt_1[status_col].values[0]
        
        # Rule 1: If passed on the first attempt, count it in both numerator and denominator
        if status_1 == 'P':
            passed_1st_or_2nd += 1
            total_tracked_attempts += 1
            
        # Rule 2: If failed on the first attempt, look for a second attempt
        elif status_1 == 'F':
            if not attempt_2.empty:
                status_2 = attempt_2[status_col].values[0]
                total_tracked_attempts += 1  # Denominator includes all 2nd attempts
                
                if status_2 == 'P':
                    passed_1st_or_2nd += 1  # Numerator includes 2nd attempt passes
            # Note: If no second attempt exists, the record is excluded entirely from both.

    # Calculate final percentage rounded to the nearest whole number
    if total_tracked_attempts == 0:
        final_percentage = 0
    else:
        final_percentage = round((passed_1st_or_2nd / total_tracked_attempts) * 100)

    return {
        "Passed on 1st or 2nd Attempt (Numerator)": passed_1st_or_2nd,
        "Total Counted Attempts (Denominator)": total_tracked_attempts,
        "Indicator 1a Pass Rate (%)": final_percentage,
        "year_taken": df['Exam Date'].dt.year.unique()
    }


def calculate_asep_indicator_1a(first_two_attempt_data_1a_data, year_filter, pass_standard):
    # st.table(first_two_attempt_data_1a_data[first_two_attempt_data_1a_data['Exam Date'].dt.year == (year_filter)])
    first_year_df, second_year_df, third_year_df = indicator_1a_data_last_3_year_data(first_two_attempt_data_1a_data, year_filter=year_filter)    
    first_score, second_score, third_score = calculate_asep_indicator_1a_calculation(first_year_df), calculate_asep_indicator_1a_calculation(second_year_df), calculate_asep_indicator_1a_calculation(third_year_df)

    if (len(first_year_df) == 0 and len(second_year_df) == 0 and len(third_year_df) == 0) or (len(first_year_df) + len(second_year_df) + len(third_year_df) < 10):
        return len(first_year_df)
    elif first_score['Indicator 1a Pass Rate (%)'] >= pass_standard:
        return 1
    elif second_score['Indicator 1a Pass Rate (%)'] >= pass_standard or third_score['Indicator 1a Pass Rate (%)'] >= pass_standard:
        return 0
    else:
        return -1

def indicator_1b_data_last_3_year_data(first_two_attempt_data, year_filter):
    test_view = first_two_attempt_data[first_two_attempt_data['Exam Name'].isin(indicator_1b_content)]
    first_year_df = test_view[(test_view['Exam Date'] >= pd.Timestamp(year_filter - 1, 9, 1)) & (test_view['Exam Date'] <= pd.Timestamp(year_filter, 8, 31))]
    second_year_df = test_view[(test_view['Exam Date'] >= pd.Timestamp(year_filter, 9, 1)) & (test_view['Exam Date'] <= pd.Timestamp(year_filter+1, 8, 31))]
    third_year_df = test_view[(test_view['Exam Date'] >= pd.Timestamp(year_filter+1, 9, 1)) & (test_view['Exam Date'] <= pd.Timestamp(year_filter+2, 8, 31))]

    return first_year_df, second_year_df, third_year_df

def calculate_asep_indicator_1b(first_two_attempt_data_1b_data, year_filter, pass_standard):
    # st.table(first_two_attempt_data_1a_data[first_two_attempt_data_1a_data['Exam Date'].dt.year == (year_filter)])
    first_year_df, second_year_df, third_year_df = indicator_1b_data_last_3_year_data(first_two_attempt_data_1b_data, year_filter=year_filter)    
    first_score, second_score, third_score = calculate_asep_indicator_1b_calculation(first_year_df), calculate_asep_indicator_1b_calculation(second_year_df), calculate_asep_indicator_1b_calculation(third_year_df)

    if (len(first_year_df) == 0 and len(second_year_df) == 0 and len(third_year_df) == 0) or (len(first_year_df) + len(second_year_df) + len(third_year_df) < 10):
        return len(first_year_df)
    elif first_score['Indicator 1b Pass Rate (%)'] >= pass_standard:
        return 1
    elif second_score['Indicator 1b Pass Rate (%)'] >= pass_standard or third_score['Indicator 1b Pass Rate (%)'] >= pass_standard:
        return 0
    else:
        return -1

def indicator_1b_data(first_two_attempt_data, year_filter, exam_name_filter):

    if exam_name_filter!="All":
        first_two_attempt_data = first_two_attempt_data[first_two_attempt_data['Exam Name'] == exam_name_filter]

    # test_view = first_two_attempt_data[first_two_attempt_data['Exam Name'].isin(indicator_1b_content)]
    combined_df = pd.DataFrame()
    year_taken = []

    for i in range(3):
        year = year_filter - i
        start_date = pd.Timestamp(year - 1, 9, 1)   # Sep 1 of previous year
        end_date = pd.Timestamp(year, 8, 31)         # Aug 31 of selected year

        year_data = first_two_attempt_data[
            (first_two_attempt_data['Exam Date'] >= start_date) &
            (first_two_attempt_data['Exam Date'] <= end_date)
        ]
        # year_data = first_two_attempt_data[first_two_attempt_data['Exam Date'].dt.year == (year_filter - i)]
        combined_df = pd.concat([combined_df, year_data])
        year_taken.append(year_filter-i)
        if group_size_calculate(combined_df) >= 10:
            break
    
    return combined_df, year_taken

def calculate_asep_indicator_1b_calculation(df):
    """
    Calculates the ASEP Indicator 1b pass rate metrics based on chronological attempts.
    Expected DataFrame columns: ['TEA ID', 'Exam Name', 'Exam Date', 'P/F Status']
    """
    # Handle edge case where the filtered dataframe might be empty
    if df.empty:
        return {
            "Number of Tests Passed": 0,
            "Number of Tests Completed": 0,
            "Indicator 1b Pass Rate (%)": 0.0
        }

    # # 1. Ensure Exam Date is a datetime object for proper chronological sorting
    # df = df.copy()
    # df['Exam Date'] = pd.to_datetime(df['Exam Date'])
    
    # # 2. Sort the data chronologically for each individual and exam type
    # df = df.sort_values(by=['TEA ID', 'Exam Name', 'Exam Date'])
    
    # 3. Assign attempt numbers (1, 2, 3, etc.) within each group
    df['Attempt'] = df.groupby(['TEA ID', 'Exam Name']).cumcount() + 1
    
    # 4. Isolate first and second attempts based on the sorted order
    first_attempts = df[df['Attempt'] == 1].set_index(['TEA ID', 'Exam Name'])
    second_attempts = df[df['Attempt'] == 2].set_index(['TEA ID', 'Exam Name'])
    
    # 5. Join them together to evaluate the ASEP conditions side-by-side
    combined = first_attempts.join(second_attempts, lsuffix='_1', rsuffix='_2')
    
    # Rule 1: Passed on the 1st attempt
    passed_first = combined['P/F Status_1'] == 'P'
    
    # Rule 2 & 3: Failed on the 1st attempt AND took a 2nd attempt
    failed_first = combined['P/F Status_1'] == 'F'
    took_second = combined['P/F Status_2'].notna()
    
    passed_second = failed_first & took_second & (combined['P/F Status_2'] == 'P')
    failed_second = failed_first & took_second & (combined['P/F Status_2'] == 'F')
    
    # 6. Calculate Totals
    # Total Passes = Passes on Attempt 1 + Passes on Attempt 2
    total_passed = passed_first.sum() + passed_second.sum()
    
    # Total Completed = Total Passes + Fails on Attempt 2
    # (Note: Individuals who failed the 1st attempt and lack a 2nd attempt evaluate to False 
    # across all these variables, naturally excluding them from the denominator).
    total_completed = total_passed + failed_second.sum()
    
    # 7. Calculate Pass Rate
    if total_completed > 0:
        pass_rate = round((total_passed / total_completed) * 100, 2)
    else:
        pass_rate = 0.0
        
    return {
        "Number of Tests Passed": int(total_passed),
        "Number of Tests Completed": int(total_completed),
        "Indicator 1b Pass Rate (%)": float(pass_rate)
    }


# ─────────────────────────────────────────────
# DARK THEME DESIGN TOKENS
# ─────────────────────────────────────────────
# ══════════════════════════════════════════════════════════
# THEME VARIABLES — Dark Theme (shared across all chapters)
# ══════════════════════════════════════════════════════════

BG_MAIN      = "rgba(0,0,0,0)"   # fully transparent — let the real page show through
BG_SURFACE   = "rgba(0,0,0,0)"   # fully transparent — no card box, no border

TEXT_PRIMARY = "var(--text-color)"
TEXT_MUTED   = "var(--text-color)"

GRID_COLOR   = "rgba(128,128,128,0.25)"   # translucent gray — visible on both light & dark
BORDER       = "rgba(128,128,128,0.4)"

FONT_FAMILY  = "Segoe UI, Helvetica, Arial, sans-serif"

ACCENT_BLUE  = "#58A6FF"
ACCENT_TEAL  = "#39D2C0"
ACCENT_AMBER = "#F0B429"

MET_COLOR    = "#1B8720"
MISSED_COLOR = "#FF1708"
GREEN, RED   = MET_COLOR, MISSED_COLOR
YELLOW       = "#F1C40F"

PASS_RATE_TARGET_1A = 85
PASS_RATE_TARGET_1B = 75


def render_indicator_1a_charts(indi_1a_result: dict, combined_df_1a: pd.DataFrame):
    """
    Renders 3 charts for Indicator 1a (Target: Pass Rate ≥ 85%):
      1. KPI metric cards
      2. Attempts by Exam Name — stacked pass/fail bar
      3. Pass rate by Race/Ethnicity — 🟢 ≥85% / 🔴 <85%
    """
    passed = indi_1a_result["Passed on 1st or 2nd Attempt (Numerator)"]
    total  = indi_1a_result["Total Counted Attempts (Denominator)"]
    rate   = indi_1a_result["Indicator 1a Pass Rate (%)"]
    failed = total - passed

    # ── KPI row ──────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    c1.metric("Passed (Numerator)",     passed)
    c2.metric("Total Attempts (Denom)", total)
    c3.metric("Pass Rate", f"{rate:.1f}%", delta=f"{rate - PASS_RATE_TARGET_1A:+.1f} pts vs 85% target")

    col1, col2, col3 = st.columns(3)

    # ── Chart 1: Pass vs Fail donut ───────────────────────────
    with col1:
        st.caption("🟢 Passed  |  🔴 Failed")
        donut = go.Figure(go.Pie(
            labels=["Passed", "Failed"],
            values=[passed, failed],
            hole=0.65,
            marker=dict(colors=[MET_COLOR, MISSED_COLOR], line=dict(color=BG_MAIN, width=2)),
            textinfo="label+percent",
            textfont=dict(family=FONT_FAMILY, size=11, color="black"),
            hovertemplate="%{label}: %{value}<extra></extra>",
        ))
        donut.update_layout(
            title=dict(text="Pass vs Fail Breakdown", font=dict(family=FONT_FAMILY, color=TEXT_PRIMARY)),
            showlegend=True,
            legend=dict(font=dict(family=FONT_FAMILY, size=10, color=TEXT_MUTED), bgcolor="rgba(0,0,0,0)"),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family=FONT_FAMILY, color=TEXT_PRIMARY),
            height=320,
            margin=dict(t=40, b=20, l=20, r=20),
        )
        st.plotly_chart(donut, use_container_width=True)

    # ── Chart 2: Attempts by Exam Name ───────────────────────
    with col2:
        st.caption("Passed vs Failed attempts per exam")
        exam_counts = (
            combined_df_1a.groupby(["Exam Name", "P/F Status"])
            .size()
            .unstack(fill_value=0)
            .rename(columns={"P": "Passed", "F": "Failed"})
            .reset_index()
        )

        bar_exam = go.Figure()
        if "Passed" in exam_counts.columns:
            bar_exam.add_trace(go.Bar(
                name="Passed", x=exam_counts["Passed"], y=exam_counts["Exam Name"],
                orientation="h", marker=dict(color=MET_COLOR, line=dict(color=BG_MAIN, width=1)),
            ))
        if "Failed" in exam_counts.columns:
            bar_exam.add_trace(go.Bar(
                name="Failed", x=exam_counts["Failed"], y=exam_counts["Exam Name"],
                orientation="h", marker=dict(color=MISSED_COLOR, line=dict(color=BG_MAIN, width=1)),
            ))
        bar_exam.update_layout(
            title=dict(text="Attempts by Exam Name", font=dict(family=FONT_FAMILY, color=TEXT_PRIMARY)),
            barmode="group",
            height=max(280, len(exam_counts) * 44 + 80),
            margin=dict(t=40, b=20, l=20, r=20),
            xaxis=dict(title="Count", tickfont=dict(family=FONT_FAMILY, color=TEXT_MUTED), gridcolor=GRID_COLOR, linecolor=BORDER),
            yaxis=dict(title="", tickfont=dict(family=FONT_FAMILY, color=TEXT_MUTED), linecolor=BORDER),
            legend=dict(orientation="h", y=1.08, font=dict(family=FONT_FAMILY, color=TEXT_MUTED), bgcolor="rgba(0,0,0,0)"),
            paper_bgcolor=BG_SURFACE,
            plot_bgcolor=BG_SURFACE,
            font=dict(family=FONT_FAMILY, color=TEXT_PRIMARY),
        )
        st.plotly_chart(bar_exam, use_container_width=True)

    # ── Chart 3: Pass rate by Race/Ethnicity ─────────────────
    with col3:
        st.caption("🟢 Green = ≥ 85% pass rate  |  🔴 Red = below 85%")
        race_group = combined_df_1a.groupby("Race/Ethnicity")["P/F Status"].apply(
            lambda s: round((s == "P").sum() / len(s) * 100, 1)
        ).reset_index(name="Pass Rate (%)")

        race_colors = [
            MET_COLOR if v >= PASS_RATE_TARGET_1A else MISSED_COLOR
            for v in race_group["Pass Rate (%)"]
        ]

        bar_race = go.Figure(go.Bar(
            x=race_group["Race/Ethnicity"],
            y=race_group["Pass Rate (%)"],
            marker=dict(color=race_colors, line=dict(color=BG_MAIN, width=1.5)),
            text=race_group["Pass Rate (%)"].astype(str) + "%",
            textposition="outside",
            textfont=dict(family=FONT_FAMILY, color=TEXT_PRIMARY),
            hovertemplate="%{x}: %{y}%<extra></extra>",
        ))
        bar_race.add_hline(
            y=PASS_RATE_TARGET_1A,
            line=dict(color="black", dash="dash", width=1.8),
            annotation_text="Target: 85%",
            annotation_font=dict(family=FONT_FAMILY, size=10, color=TEXT_MUTED),
        )
        bar_race.update_layout(
            title=dict(text="Pass Rate by Race / Ethnicity", font=dict(family=FONT_FAMILY, color=TEXT_PRIMARY)),
            height=300,
            margin=dict(t=40, b=20, l=20, r=20),
            yaxis=dict(range=[0, 110], ticksuffix="%", tickfont=dict(family=FONT_FAMILY, color=TEXT_MUTED), gridcolor=GRID_COLOR, linecolor=BORDER),
            xaxis=dict(title="", tickfont=dict(family=FONT_FAMILY, color=TEXT_MUTED), linecolor=BORDER),
            paper_bgcolor=BG_SURFACE,
            plot_bgcolor=BG_SURFACE,
            font=dict(family=FONT_FAMILY, color=TEXT_PRIMARY),
        )
        st.plotly_chart(bar_race, use_container_width=True)


def render_indicator_1b_charts(
    indi_1b_result: dict,
    sample_size: int,
    certificate_1b_cert_result: dict,
):
    """
    Renders 3 charts for Indicator 1b (Target: Pass Rate ≥ 75%):
      1. KPI metric cards
      2. Pass vs Fail donut
      3. Tests passed vs failed by certificate — grouped bar
      4. Pass rate by certificate area — 🟢 ≥75% / 🔴 <75%
    """
    passed    = indi_1b_result["Number of Tests Passed"]
    completed = indi_1b_result["Number of Tests Completed"]
    rate      = indi_1b_result["Indicator 1b Pass Rate (%)"]
    failed    = completed - passed

    # ── KPI row ──────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    c1.metric("Tests Passed (Numerator)",      passed)
    c2.metric("Tests Completed (Denominator)", completed)
    c3.metric("Pass Rate", f"{rate:.1f}%", delta=f"{rate - PASS_RATE_TARGET_1B:+.1f} pts vs 75% target")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption("🟢 Passed  |  🔴 Failed")
        donut = go.Figure(go.Pie(
            labels=["Passed", "Failed"],
            values=[passed, max(failed, 0)],
            hole=0.65,
            marker=dict(colors=[MET_COLOR, MISSED_COLOR], line=dict(color=BG_MAIN, width=2)),
            textinfo="label+percent",
            textfont=dict(family=FONT_FAMILY, size=11, color="black"),
            hovertemplate="%{label}: %{value}<extra></extra>",
        ))
        donut.update_layout(
            title=dict(text="Pass vs Fail Breakdown", font=dict(family=FONT_FAMILY, color=TEXT_PRIMARY)),
            showlegend=True,
            legend=dict(font=dict(family=FONT_FAMILY, size=10, color=TEXT_MUTED), bgcolor="rgba(0,0,0,0)"),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family=FONT_FAMILY, color=TEXT_PRIMARY),
            height=320,
            margin=dict(t=40, b=20, l=20, r=20),
        )
        st.plotly_chart(donut, use_container_width=True)

    with col2:
        st.caption("Passed vs Failed tests per certificate area")
        certs        = list(certificate_1b_cert_result.keys())
        cert_passed  = [certificate_1b_cert_result[k]["Number of Tests Passed"]    for k in certs]
        cert_complet = [certificate_1b_cert_result[k]["Number of Tests Completed"] for k in certs]
        cert_failed  = [c - p for c, p in zip(cert_complet, cert_passed)]

        bar_cert = go.Figure()
        bar_cert.add_trace(go.Bar(
            name="Passed",
            x=cert_passed,
            y=certs,
            orientation="h",
            marker=dict(color=MET_COLOR, line=dict(color=BG_MAIN, width=1)),
            hovertemplate="%{y}: %{x} passed<extra></extra>",
        ))
        bar_cert.add_trace(go.Bar(
            name="Failed",
            x=cert_failed,
            y=certs,
            orientation="h",
            marker=dict(color=MISSED_COLOR, line=dict(color=BG_MAIN, width=1)),
            hovertemplate="%{y}: %{x} failed<extra></extra>",
        ))
        bar_cert.update_layout(
            title=dict(text="Attempts by Certificate Area", font=dict(family=FONT_FAMILY, color=TEXT_PRIMARY)),
            barmode="group",
            height=max(280, len(certs) * 44 + 80),
            margin=dict(t=40, b=20, l=20, r=20),
            xaxis=dict(title="Count", tickfont=dict(family=FONT_FAMILY, color=TEXT_MUTED), gridcolor=GRID_COLOR, linecolor=BORDER),
            yaxis=dict(title="", tickfont=dict(family=FONT_FAMILY, color=TEXT_MUTED), linecolor=BORDER),
            legend=dict(orientation="h", y=1.08, font=dict(family=FONT_FAMILY, color=TEXT_MUTED), bgcolor="rgba(0,0,0,0)"),
            paper_bgcolor=BG_SURFACE,
            plot_bgcolor=BG_SURFACE,
            font=dict(family=FONT_FAMILY, color=TEXT_PRIMARY),
        )
        st.plotly_chart(bar_cert, use_container_width=True)

    with col3:
        st.caption("🟢 Green = ≥ 75% pass rate  |  🔴 Red = below 75%")
        cert_rates = [certificate_1b_cert_result[k]["Indicator 1b Pass Rate (%)"] for k in certs]

        rate_colors = [
            MET_COLOR if r >= PASS_RATE_TARGET_1B else MISSED_COLOR
            for r in cert_rates
        ]

        bar_rate = go.Figure(go.Bar(
            x=certs,
            y=cert_rates,
            marker=dict(color=rate_colors, line=dict(color=BG_MAIN, width=1.5)),
            text=[f"{r}%" for r in cert_rates],
            textposition="outside",
            textfont=dict(family=FONT_FAMILY, color=TEXT_PRIMARY),
            hovertemplate="%{x}: %{y}%<extra></extra>",
        ))
        bar_rate.add_hline(
            y=PASS_RATE_TARGET_1B,
            line=dict(color="black", dash="dash", width=1.8),
            annotation_text="Target: 75%",
            annotation_font=dict(family=FONT_FAMILY, size=10, color=TEXT_MUTED),
        )
        bar_rate.update_layout(
            title=dict(text="Pass Rate by Certificate Area", font=dict(family=FONT_FAMILY, color=TEXT_PRIMARY)),
            height=300,
            margin=dict(t=40, b=20, l=20, r=20),
            yaxis=dict(range=[0, 110], ticksuffix="%", tickfont=dict(family=FONT_FAMILY, color=TEXT_MUTED), gridcolor=GRID_COLOR, linecolor=BORDER),
            xaxis=dict(title="", tickfont=dict(family=FONT_FAMILY, color=TEXT_MUTED), linecolor=BORDER),
            paper_bgcolor=BG_SURFACE,
            plot_bgcolor=BG_SURFACE,
            font=dict(family=FONT_FAMILY, color=TEXT_PRIMARY),
        )
        st.plotly_chart(bar_rate, use_container_width=True)

# @st.cache_data
def prepare_chapter_3(exam_roaster_data, educator_details_data):
    merge_data = merge_chapter_3_data(exam_roaster_data, educator_details_data)
    first_two_attempt_data = get_first_attempts_data(merge_data=merge_data)
    return first_two_attempt_data

def exam_pass_rate(exam_roaster_data, educator_details_data):

    st.title('Chapter 3 – Certification Exam Pass Rate')
    st.write(' ')
    first_two_attempt_data = prepare_chapter_3(exam_roaster_data, educator_details_data)

    # Indicator 1a
    first_two_attempt_data_1a_data = first_two_attempt_data[first_two_attempt_data['Exam Name'].isin(indicator_1a_pedagogy)]

    available_year_filter_1a = sorted(first_two_attempt_data_1a_data['Exam Date'].dt.year.unique().astype(int).tolist())
    # available_exam_names_1a = sorted(first_two_attempt_data_1a_data['Exam Name'].unique().tolist())

    if "chapter_3_year_filter_1a" not in st.session_state:
        st.session_state.chapter_3_year_filter_1a = available_year_filter_1a[-1]

    if "chapter_3_exam_name" not in st.session_state:
        st.session_state.chapter_3_exam_name = "All"

    # # ── Filters ──
    st.subheader("🔍 Filter Options for Indicator 1a: Percent of Individuals Passing Pedagogy Tests")
    filter_1a_col1, filter_1a_col2, filter_1a_col3 = st.columns(3)

    with filter_1a_col1:
        exam_year = st.selectbox(
            "Exam Year",
            options=available_year_filter_1a,
            key="chapter_3_exam_year_1a",
        )
        
        # If the user changes selection, trigger a rerun so the preprocessor runs with new years
        if exam_year != st.session_state.chapter_3_year_filter_1a:
            st.session_state.chapter_3_year_filter_1a = exam_year

    with filter_1a_col2:
        exam_name = st.selectbox(
            "Exam Name",
            options=["All"] + indicator_1a_pedagogy,
            key="chapter_3_exam_name_filter_1a",
        )
        st.session_state.chapter_3_exam_name = exam_name
        # If the user changes selection, trigger a rerun so the preprocessor runs with new years
        # if exam_name != st.session_state.chapter_3_exam_name:
        #     st.session_state.chapter_3_exam_name = exam_name

    # st.write(st.session_state.chapter_3_year_filter_1a)
    combined_df_1a, year_taken_1a = indicator_1a_data(first_two_attempt_data_1a_data, year_filter=st.session_state.chapter_3_year_filter_1a)

    # st.write(indicator_1a_data(first_two_attempt_data_1a_data, year_filter=2023, no_of_year=1))

    if st.session_state.chapter_3_exam_name != "All":
        combined_df_1a = combined_df_1a[combined_df_1a['Exam Name'] == st.session_state.chapter_3_exam_name]

    indi_1a_result = calculate_asep_indicator_1a_calculation(combined_df_1a)
    
    render_indicator_1a_charts(indi_1a_result, combined_df_1a)

    st.markdown("---")
    # indicator 1b
    first_two_attempt_data_1b_data = first_two_attempt_data[first_two_attempt_data['Exam Name'].isin(indicator_1b_content)]

    available_year_filter_1b = sorted(first_two_attempt_data_1b_data['Exam Date'].dt.year.unique().astype(int).tolist())

    if "chapter_3_year_filter_1b" not in st.session_state:
        st.session_state.chapter_3_year_filter_1b = available_year_filter_1b[-1]
    
    if "chapter_3_exam_name_1b" not in st.session_state:
        st.session_state.chapter_3_exam_name_1b = "All"

    st.subheader("🔍 Filter Options for Indicator 1b: Percent of Individuals Passing Content Pedagogy Tests")
    filter_1b_col1, filter_1b_col2, filter_1b_col3 = st.columns(3)

    with filter_1b_col1:
        exam_year_1b = st.selectbox(
            "Exam Year",
            options=available_year_filter_1a,
            key="chapter_3_exam_year_1b",
        )
        
        # If the user changes selection, trigger a rerun so the preprocessor runs with new years
        if exam_year_1b != st.session_state.chapter_3_year_filter_1b:
            st.session_state.chapter_3_year_filter_1b = exam_year_1b

    with filter_1b_col2:
        exam_name_1b = st.selectbox(
            "Exam Name",
            options=["All"] + indicator_1b_content,
            key="chapter_3_exam_name_filter_1b",
        )
        st.session_state.chapter_3_exam_name_1b = exam_name_1b

    # st.write('Indicator 1b data')
    combined_df_1b, year_taken = indicator_1b_data(first_two_attempt_data_1b_data, year_filter=st.session_state.chapter_3_year_filter_1b, exam_name_filter=st.session_state.chapter_3_exam_name_1b)
    
    
    indi_1b_result = calculate_asep_indicator_1b_calculation(combined_df_1b)
    

    all_unique_result=combined_df_1b['Certification Grade Level'].unique().tolist()
    certificate_1b_cert_result = {}


    for i in all_unique_result:
        retrieved_data = combined_df_1b[combined_df_1b['Certification Grade Level'] == i]
        indi_1b_certification_result = calculate_asep_indicator_1b_calculation(retrieved_data)
        certificate_1b_cert_result[i] = indi_1b_certification_result


    render_indicator_1b_charts(indi_1b_result, len(combined_df_1b), certificate_1b_cert_result)

    return first_two_attempt_data_1a_data, first_two_attempt_data_1b_data, year_taken_1a