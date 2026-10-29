import pandas as pd
import streamlit as st
from streamlit_theme import st_theme

import plotly.express as px
import plotly.graph_objects as go


# ─────────────────────────────────────────────
# THEME TOKENS (shared across all chapters)
# ─────────────────────────────────────────────
BG_MAIN      = "rgba(0,0,0,0)"   # fully transparent — let the real page show through
BG_CARD      = "rgba(0,0,0,0)"   # was a hardcoded dark card bg — now transparent
BG_SURFACE   = "rgba(0,0,0,0)"   # was a hardcoded lighter surface — now transparent
BORDER       = "rgba(128,128,128,0.4)"
ACCENT_BLUE  = "#58A6FF"
ACCENT_TEAL  = "#3BCEAC"
ACCENT_AMBER = "#F0B429"
TEXT_PRIMARY = "var(--text-color)"
TEXT_MUTED   = "var(--text-color)"
GRID_COLOR   = "rgba(128,128,128,0.25)"

# Gauge / traffic light — unchanged, these are semantic (pass/fail), not theme colors
GREEN  = "#2EA043"
YELLOW = "#F0B429"
RED    = "#F85149"

FONT_FAMILY = "Montserrat, sans-serif"

def merge_both_df(principle_preception_df, educator_detail_df):
    # Find columns in the second DF that already exist in the first (excluding 'TEA ID')
    cols_to_drop = educator_detail_df.columns.intersection(principle_preception_df.columns).drop('TEA ID')
    
    # Merge while excluding those columns from the second DF
    return principle_preception_df.merge(
        educator_detail_df.drop(columns=cols_to_drop), 
        on='TEA ID', 
        how='inner'
    )

# ─────────────────────────────────────────────
# BASE PLOTLY LAYOUT (dark)
# ─────────────────────────────────────────────
def base_layout(title: str, xtitle: str = "", ytitle: str = "") -> dict:
    return dict(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(family=FONT_FAMILY, size=17, color=TEXT_PRIMARY),
            x=0.03,
        ),
        xaxis=dict(
            title=dict(text=f"<b>{xtitle}</b>", font=dict(family=FONT_FAMILY, size=12, color=TEXT_MUTED)),
            tickfont=dict(family=FONT_FAMILY, size=11, color=TEXT_MUTED),
            gridcolor=GRID_COLOR,
            linecolor=BORDER,
            showgrid=True,
            zeroline=False,
        ),
        yaxis=dict(
            title=dict(text=f"<b>{ytitle}</b>", font=dict(family=FONT_FAMILY, size=12, color=TEXT_MUTED)),
            tickfont=dict(family=FONT_FAMILY, size=11, color=TEXT_MUTED),
            gridcolor=GRID_COLOR,
            linecolor=BORDER,
            showgrid=True,
            zeroline=False,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=BG_CARD,
        font=dict(family=FONT_FAMILY, color=TEXT_PRIMARY),
        margin=dict(l=60, r=30, t=70, b=60),
        hoverlabel=dict(
            bgcolor=BG_SURFACE,
            font_color=TEXT_PRIMARY,
            font_family=FONT_FAMILY,
            bordercolor=BORDER,
        ),
    )

# ─────────────────────────────────────────────
# BASE PLOTLY LAYOUT (dark)
# ─────────────────────────────────────────────
def base_layout(title: str, xtitle: str = "", ytitle: str = "") -> dict:
    return dict(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(family=FONT_FAMILY, size=17, color=TEXT_PRIMARY),
            x=0.03,
        ),
        xaxis=dict(
            title=dict(text=f"<b>{xtitle}</b>", font=dict(family=FONT_FAMILY, size=12, color=TEXT_MUTED)),
            tickfont=dict(family=FONT_FAMILY, size=11, color=TEXT_MUTED),
            gridcolor=GRID_COLOR,
            linecolor=BORDER,
            showgrid=True,
            zeroline=False,
        ),
        yaxis=dict(
            title=dict(text=f"<b>{ytitle}</b>", font=dict(family=FONT_FAMILY, size=12, color=TEXT_MUTED)),
            tickfont=dict(family=FONT_FAMILY, size=11, color=TEXT_MUTED),
            gridcolor=GRID_COLOR,
            linecolor=BORDER,
            showgrid=True,
            zeroline=False,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=BG_CARD,
        font=dict(family=FONT_FAMILY, color=TEXT_PRIMARY),
        margin=dict(l=60, r=30, t=70, b=60),
        hoverlabel=dict(
            bgcolor=BG_SURFACE,
            font_color=TEXT_PRIMARY,
            font_family=FONT_FAMILY,
            bordercolor=BORDER,
        ),
    )

def get_asep_consolidated_data(merged_df):
    """
        Consolidates data per teacher:
        - Keeps the EARLIEST (oldest) Employment Date.
    """
    merged_df['Employment Date'] = pd.to_datetime(merged_df['Employment Date'], dayfirst=True)

    # 2. Sort the dataframe by TEA ID and then by date (ascending)
    # This puts the most recent date at the bottom for each ID
    df1_sorted = merged_df.sort_values(by=['TEA ID', 'Employment Date'], ascending=False)

    # 3. Drop duplicates, keeping only the 'last' occurrence for each TEA ID
    df_latest = df1_sorted.drop_duplicates(subset='TEA ID', keep='last')

    # Optional: Reset the index for a clean dataframe
    df_latest = df_latest.reset_index(drop=True)

    return df_latest

def chapter_4_chart(df, key_suffix="chapter_4"):
    

    MET_COLOR     = "#1B8720"   # green  – score >= 50
    MISSED_COLOR  = "#FF1708"   # red    – score <  50
    # TARGET        = 50

    # ── Chapter 5–style binary threshold ────────────────────────────────
    TARGET_C4 = 2.0
    MET_COLOR_C4    = MET_COLOR    # reuse the same green used in Ch.5
    MISSED_COLOR_C4 = MISSED_COLOR # reuse the same red used in Ch.5

    

    def _c4_color(v):
        return MET_COLOR_C4 if v >= TARGET_C4 else MISSED_COLOR_C4

    def _c4_bar_colors(series):
        return [_c4_color(v) for v in series]

    # ══════════════════════════════════════════
    # CHART 1 — Radar Chart (dark theme, line/fill green/red based on avg)
    # ══════════════════════════════════════════
    st.markdown("---")
    st.subheader("📊 Domain Performance Overview")
    st.caption(
        "🟢 Green = Overall average ≥ 2.0 (Satisfactory)  |  🔴 Red = Below 2.0. "
        "Radar chart comparing average scores across six principal appraisal domains."
    )

    categories = [
        "Planning",
        "Instruction",
        "Learning Environment",
        "Professional Practices and Responsibilities",
        "Students with Disabilities",
        "English Language Learners",
    ]
    values = [df[c].mean() for c in categories]
    radar_avg = sum(values) / len(values)
    radar_color = _c4_color(radar_avg)
    radar_fill = "rgba(46,204,113,0.15)" if radar_avg >= TARGET_C4 else "rgba(231,76,60,0.15)"

    fig_radar = go.Figure()
    fig_radar.add_trace(
        go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            name="Appraisal Score",
            line=dict(color=radar_color, width=2.5),
            fillcolor=radar_fill,
            hovertemplate="<b>%{theta}</b><br>Score: %{r:.2f}<extra></extra>",
        )
    )
    fig_radar.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",   # was "black" — invisible/wrong in light theme
            radialaxis=dict(
                visible=True,
                range=[0, max(values) + 0.4],
                tickfont=dict(size=10, family=FONT_FAMILY, color=TEXT_MUTED),
                gridcolor=GRID_COLOR,
                linecolor=BORDER,
            ),
            angularaxis=dict(
                tickfont=dict(size=11, family=FONT_FAMILY, color=TEXT_PRIMARY),
                linecolor=BORDER,
            ),
        ),
        showlegend=False,
        title=dict(
            text="<b>Principal Appraisal — Domain Performance Overview</b>",
            font=dict(family=FONT_FAMILY, size=17, color=TEXT_PRIMARY),
            x=0.03,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT_FAMILY, color=TEXT_PRIMARY),
        margin=dict(t=80, b=40),
        height=480,
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # ══════════════════════════════════════════
    # CHART 2 — Bar Chart (UNCHANGED — kept as original traffic-light style)
    # ══════════════════════════════════════════
    st.markdown("---")
    st.subheader("📈 Average Overall Score by Certification Grade Level")
    st.caption(
        "Bars are color-coded by performance band: "
        "🔴 Needs Improvement (< 1.8)  🟡 Developing (1.8 – 2.0) 🟢 Satisfactory  (≥ 2.0). "
        "Dashed lines mark the band boundaries."
    )

    grade_df = (
        df.groupby("Certification Area Grade Level")["Overall"]
        .mean()
        .reset_index()
        .sort_values("Overall")
    )
    grade_df.columns = ["Grade Level", "Average Score"]

    def score_color(v):
        if v >= 2.0:
            return GREEN
        elif v >= 1.8:
            return YELLOW
        else:
            return RED

    bar_colors = [score_color(v) for v in grade_df["Average Score"]]

    fig_bar = go.Figure(
        go.Bar(
            x=grade_df["Grade Level"],
            y=grade_df["Average Score"],
            marker=dict(
                color=bar_colors,
                opacity=0.9,
            ),
            text=grade_df["Average Score"].round(2),
            textposition="outside",
            textfont=dict(family=FONT_FAMILY, size=11, color=TEXT_PRIMARY),
            hovertemplate="<b>%{x}</b><br>Avg Score: %{y:.2f}<extra></extra>",
        )
    )
    layout_bar = base_layout(
        "Average Appraisal Score by Certification Grade Level",
        xtitle="Certification Grade Level",
        ytitle="Average Overall Score",
    )
    layout_bar["yaxis"]["range"] = [0, grade_df["Average Score"].max() + 0.45]

    fig_bar.add_hline(
        y=1.8,
        line=dict(color=RED, dash="dash", width=1.8),
        annotation_text="",
        annotation_position="top left",
        annotation_font=dict(family=FONT_FAMILY, size=10, color=RED),
    )
    fig_bar.add_hline(
        y=2.0,
        line=dict(color=YELLOW, dash="dash", width=1.8),
        annotation_text="",
        annotation_position="top right",
        annotation_font=dict(family=FONT_FAMILY, size=10, color=YELLOW),
    )
    fig_bar.update_layout(**layout_bar, height=430)
    st.plotly_chart(fig_bar, use_container_width=True)

    # ══════════════════════════════════════════
    # CHART 3 — Gauge (Ch.5 binary theme) + Donut (ORIGINAL dark theme, UNCHANGED)
    # ══════════════════════════════════════════
    st.markdown("---")
    overall_avg = round(df["Overall"].mean(), 2)

    # Shared theme detection for both charts below
    theme =  st_theme(key=f"theme_{key_suffix}")
    is_light = theme and theme.get("base") == "light"
    donut_text_color   = "#000000" if is_light else "#FFFFFF"
    donut_border_color = "#000000" if is_light else "#FFFFFF"

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Principal Survey Pass Rate")
        survey_data = chapter_4_survey_summary(df)
        total_valid_surveys, surveys_meeting_standard = survey_data['total_valid_surveys'], survey_data['surveys_meeting_standard']
        if total_valid_surveys > 0:
            pct_meeting_standard = round((surveys_meeting_standard / total_valid_surveys) * 100, 2)
        else:
            pct_meeting_standard = 0

        st.caption(
            "🟢 Green = 70% or more surveys meeting standard (Overall ≥ 2.0)  |  "
            "🔴 Red = Below 70%. "
            f"({surveys_meeting_standard} of {total_valid_surveys} surveys met standard)"
        )

        gauge_color = GREEN if pct_meeting_standard >= 70 else RED

        gauge_fill_color   = "#FFFFFF" if is_light else "#000000"
        gauge_border_color = "#000000" if is_light else "#FFFFFF"

        fig_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=pct_meeting_standard,
                number=dict(
                    font=dict(size=52, color=TEXT_PRIMARY),
                    suffix="%",
                ),
                domain={"x": [0, 1], "y": [0, 1]},
                gauge={
                    "axis": {
                        "range": [0, 100],
                        "tickwidth": 1,
                        "tickcolor": gauge_border_color,
                        "tickfont": {"color": TEXT_PRIMARY},
                    },
                    "bar": {"color": gauge_color},
                    "bgcolor": gauge_fill_color,
                    "borderwidth": 2,
                    "bordercolor": gauge_border_color,
                    "steps": [
                        {"range": [0, 70],   "color": gauge_fill_color},
                        {"range": [70, 100], "color": gauge_fill_color},
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

    with col2:
        st.subheader("🥧 Score Distribution by Race / Ethnicity")
        st.caption(
            "Donut chart showing average principal appraisal scores proportionally "
            "by demographic group. Hover over each slice for exact values. "
            "The center displays the overall cohort average."
        )

        ethnicity_df = (
            df.groupby("Race/Ethnicity")["Overall"].mean().round(2).reset_index()
        )
        palette = [
            ACCENT_BLUE, ACCENT_TEAL, "#F63228", ACCENT_AMBER,
            "#BC8CFF", "#FF7B72", "#56D364",
        ]

        fig_donut = go.Figure(
            go.Pie(
                labels=ethnicity_df["Race/Ethnicity"],
                values=ethnicity_df["Overall"],
                hole=0.48,
                marker=dict(
                    colors=palette[: len(ethnicity_df)],
                    line=dict(color=donut_border_color, width=2),
                ),
                textinfo="label+percent",
                textfont=dict(family=FONT_FAMILY, size=11, color=donut_text_color),
                hovertemplate=(
                    "<b>%{label}</b><br>Avg Score: %{value:.2f}<br>Share: %{percent}<extra></extra>"
                ),
            )
        )
        fig_donut.update_layout(
            title=dict(
                text="<b>Avg Appraisal Score by Race / Ethnicity</b>",
                font=dict(family=FONT_FAMILY, size=15, color=TEXT_PRIMARY),
                x=0.03,
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family=FONT_FAMILY, color=TEXT_PRIMARY),
            legend=dict(
                orientation="v",
                font=dict(family=FONT_FAMILY, size=10, color=TEXT_MUTED),
                bgcolor="rgba(0,0,0,0)",
            ),
            annotations=[
                dict(
                    text=f"<b>{overall_avg}</b><br><span style='font-size:11px'>Overall</span>",
                    x=0.5, y=0.5,
                    font=dict(size=18, family=FONT_FAMILY, color=donut_text_color),
                    showarrow=False,
                )
            ],
            height=400,
            margin=dict(t=60, b=20, l=10, r=10),
        )
        st.plotly_chart(fig_donut, use_container_width=True)


def specific_year_data(df, selected_year):
    target_emp_date = pd.Timestamp(year=selected_year - 1, month=9, day=1)

    final_ready_df = df[df['Employment Date'] == target_emp_date].reset_index(drop=True)

    return final_ready_df

def verify_certificate(df):
    df = df[df['Certification Type'].isin(['Standard', 'Intern','Probationary', 'Enhanced Standared'])]
    return df

def missing_required_sections(df):
    target_columns = [
        'Planning', 
        'Instruction', 
        'Learning Environment', 
        'Professional Practices and Responsibilities'
    ]

    # Drop rows where any of these columns have NaN/None
    return df.dropna(subset=target_columns)

def remove_duplicates(df):
    """If a Teacher work in multiple campus in same time it will give score of highest one also use this after merging both the dataset"""
    df['Employment Year'] = df['Employment Date'].dt.year

    merged_cleaned = df.sort_values(
        by=['TEA ID', 'Employment Year', 'Overall'], 
        ascending=[True, True, False]
    ).drop_duplicates(
        subset=['TEA ID', 'Employment Year'], 
        keep='first'
    )
    return merged_cleaned

# ─────────────────────────────────────────────
# PRINCIPAL PERCEPTIONS TAB
# ─────────────────────────────────────────────
# @st.cache_data
def prepare_chapter_4(principal_df, educator_df):
    merged = merge_both_df(principal_df, educator_df)
    merged = get_asep_consolidated_data(merged)
    merged = verify_certificate(merged)
    merged = missing_required_sections(merged)
    merged = remove_duplicates(merged)
    return merged


def chapter_4_group_aggregration(filtered_copy_df, current_year):
    aggregated_dfs = []
    total_records = 0  # now represents UNIQUE TEA ID count, not row count
    years_checked = 0
    combined_df = pd.DataFrame(columns=filtered_copy_df.columns)

    # Keep aggregating while unique TEA ID group size is <= 10, up to 3 years back
    while total_records <= 10 and years_checked < 3:
        year_df = specific_year_data(filtered_copy_df, current_year)

        if not year_df.empty:
            aggregated_dfs.append(year_df)
            combined_df = pd.concat(aggregated_dfs, ignore_index=True)
            total_records = combined_df['TEA ID'].nunique()  

        current_year -= 1
        years_checked += 1

    if aggregated_dfs:
        filtered_copy_df = pd.concat(aggregated_dfs, ignore_index=True)
    else:
        filtered_copy_df = pd.DataFrame(columns=filtered_copy_df.columns)

    return filtered_copy_df, total_records

def chapter_4_last_3_year_data(filtered_copy_df, current_year):
    first_year_df = specific_year_data(filtered_copy_df, current_year)
    second_year_df = specific_year_data(filtered_copy_df, current_year-1)
    third_year_df = specific_year_data(filtered_copy_df, current_year-2)

    return first_year_df, second_year_df, third_year_df

def calculate_asep_chapter_4(principal_dataset, year_filter, pass_standard):
    first_year_df, second_year_df, third_year_df = chapter_4_last_3_year_data(principal_dataset, year_filter)

    # st.write(len(first_year_df))
    # st.write(len(second_year_df))
    # st.write(len(third_year_df))
    first_score, second_score, third_score = chapter_4_survey_summary(first_year_df, False), chapter_4_survey_summary(second_year_df, False), chapter_4_survey_summary(third_year_df, False)

    if (len(first_year_df) == 0 and len(second_year_df) == 0 and len(third_year_df) == 0) or (len(first_year_df) + len(second_year_df) + len(third_year_df) < 10):
        return len(first_year_df)
    elif first_score['overall_score'] >= pass_standard:
        return 1
    elif second_score['overall_score'] >= pass_standard or third_score['overall_score'] >= pass_standard:
        return 0
    else:
        return -1




def chapter_4_survey_summary(df, small_group_aggregration=True):
    total_valid_surveys = df['TEA ID'].nunique()
    surveys_meeting_standard = df[df['Overall'] >= 2.00]['TEA ID'].nunique()
    # No data / small group exception
    if small_group_aggregration == True:
        if total_valid_surveys == 0 or total_valid_surveys < 10:
            return {
                "total_valid_surveys": total_valid_surveys,
                "surveys_meeting_standard": surveys_meeting_standard,
                "overall_score": 0,
            }
    else:
        if total_valid_surveys == 0:
                    return {
                        "total_valid_surveys": total_valid_surveys,
                        "surveys_meeting_standard": surveys_meeting_standard,
                        "overall_score": 0,
                    }
        
    # Calculate percentage meeting standard
    overall_score = round(
        (surveys_meeting_standard / total_valid_surveys) * 100,
        2
    )

    return {
        "total_valid_surveys": total_valid_surveys,
        "surveys_meeting_standard": surveys_meeting_standard,
        "overall_score": overall_score,
    }


def principal_perceptions(principal_perception_df, educator_details_df):

    st.title('Chapter 4 – Appraisal of First-Year Teachers by Administrators (Principal Survey)')
    st.write(' ')

    # 1. Handle the initial session state before preprocessing
    merged = prepare_chapter_4(principal_perception_df, educator_details_df)

    available_cohort_options = sorted(merged["Admission Cohort"].unique().astype(int).tolist())
    available_employment_options = sorted(merged['Employment Date'].dt.year.astype(int).unique().tolist())

    if "chapter_4_cohort_filter" not in st.session_state:
        st.session_state.chapter_4_cohort_filter = available_cohort_options  # Or [2019, 2020, 2021] depending on your default target
        
    if "chapter_4_gender_filter" not in st.session_state:
        st.session_state.chapter_4_gender_filter = "All"

    if "chapter_4_employment_date" not in st.session_state:
        st.session_state.chapter_4_employment_date = available_employment_options


    # # ── Filters ──
    st.subheader("🔍 Filter Options: Principal Survey (ASEP Accountability Indicator 2)")
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        gender_selected = st.selectbox(
            "Gender",
            options=["All"] + sorted(merged["Gender"].unique().tolist()),
            key="chapter_4_gender_select",
        )
        st.session_state.chapter_4_gender_filter = gender_selected

    with filter_col2:
        employment_date_selected = st.selectbox(
            "Employment Date",
            options=available_employment_options,
            # default=st.session_state.chapter_4_employment_date,
            key="chapter_4_emp_date_select"
        )

        if employment_date_selected != st.session_state.chapter_4_employment_date:
            st.session_state.chapter_4_employment_date = employment_date_selected
            

    filtered_copy_df = merged.copy()
    if gender_selected != "All":
        filtered_copy_df = filtered_copy_df[filtered_copy_df["Gender"] == gender_selected]


    filtered_copy_df, total_records = chapter_4_group_aggregration(filtered_copy_df, employment_date_selected)
    # if years_checked > 1 and total_records > 0:
    st.info(
        f"ℹ️ **Small Group Aggregation Applied:** Initial cohort was under 10. "
        f"Total evaluation sample size: **{total_records}**."
    )

    if total_records != 0:
        chapter_4_chart(filtered_copy_df, key_suffix="chapter_4")
    else:
        st.info('Select Other Year No Record Found')

    return merged