# 📊 ASEP Metrics Dashboard

A Streamlit web application for calculating and visualizing **Alternative Student Educator Preparation (ASEP)** program metrics — built for tracking educator preparation program performance across multiple indicators (certification exams, principal perceptions, student growth, field supervision, teacher surveys) and rolling them up into a final **ASEP Index Score**.

---

## 🧭 Table of Contents

- [Background](#-background)
- [Overview](#-overview)
- [Pages](#-pages)
- [Datasets Required](#-datasets-required)
- [Getting Started](#-getting-started)
  - [🪟 Windows Setup](#-windows-setup)
  - [🍎 macOS Setup](#-macos-setup)
- [How to Use the App](#-how-to-use-the-app)
- [Data Security](#-data-security)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Contributing / Feedback](#-contributing--feedback)
- [I2I Workgroup Members](#-i2i-workgroup-members)
- [Contact](#-contact)
- [Credits](#-credits)

---

## 📖 Background

The ASEP Data Dashboard was developed in support of the [UT System's ElevateTXed initiative](https://elevatetxed.utsystem.edu/). It was envisioned and collaboratively designed by the I2I Data Workgroup (members below). The primary goal of this project is to enhance the capacity of educator preparation programs (EPPs) to use data for continuous improvement, informed decision-making, and alignment with state accountability metrics.

This software allows users to securely upload raw data files from multiple TEA sources — including I2I, ECOS, ResultsAnalyzer, and others — and automatically convert those files into EPP-specific dashboards in alignment with the [24-25 Texas Accountability System for Educator Preparation Manual](https://tea.texas.gov/educators/preparation-and-continuing-education/consumer-information-about-educator-preparation-programs/24-25-asep-manual.pdf). The intent of this dashboard is to aggregate these disparate data sources into a unified environment, directly aligned with ASEP standards, using real-time, student-level data. Our hope is that this tool will enable EPPs to monitor progress on accountability benchmarks and serve as an early warning system to identify areas of strength and risk.

---

## 📖 Overview

This dashboard automates the process of calculating ASEP compliance metrics for an Educator Preparation Program (EPP). Instead of manually combining reports from **I2I**, **ECOS**, **ResultsAnalyzer**, and **TEA Program Provider Resources**, users upload the raw exports directly, and the app:

1. Auto-detects and renames uploaded files based on their structure.
2. Merges and cleans the data per chapter/indicator.
3. Calculates each ASEP indicator (1a, 1b, 2, 3, 4a, 4b, 5).
4. Produces a weighted, demographic-broken-down **ASEP Index Score** with a visual gauge.

---

## 🗂️ Pages

| Page | Description |
|---|---|
| **📁 Data Management** | Upload raw dataset files. The app detects and renames each file automatically so the rest of the dashboard can recognize it. Includes a downloadable PDF guide and renamed-file download option. |
| **📊 Dashboard** | Tabbed view (Chapter 3–8) showing calculated metrics for each ASEP indicator, culminating in the combined ASEP Index Score in Chapter 8. |
| **ℹ️ About Us** | Background on the project, data security info, the I2I Workgroup, and a step-by-step navigation guide. |
| **💬 Feedback** | Embedded Microsoft Forms widget for reporting bugs, requesting features, or submitting general feedback. |

> The app opens on the **About Us** page by default so new users see the navigation guide first.

---

## 📋 Datasets Required

| Dataset | Source |
|---|---|
| **Educator Details** | I2I → EPP Employment and Retention → Educator Details |
| **Exam Roster** | ResultsAnalyzer → Texas Examinee Data → Examinee Roster |
| **Principal Perception** | I2I → EPP Perception Surveys → New Teacher Perceptions by Candidate (View by Academic Year) |
| **Student Growth** | I2I → EPP Student Growth → Average Student Growth by Candidate |
| **Observation** | ECOS → EPP → ASEP → Observations Report |
| **Finishers** | ECOS → ASEP → Maint Finishers |
| **Exit Survey** | TEA Program Provider Resources → Accountability System Data → Exit Survey Data |
| **New Teacher Survey** | I2I → EPP Perception Surveys → New Teacher Perceptions by Candidate |

**Which chapters need which files:**

| Chapter | Required Datasets |
|---|---|
| Chapter 3 | Exam Roster + Educator Details |
| Chapter 4 | Principal Perception + Educator Details |
| Chapter 5 | Educator Details + Student Growth |
| Chapter 6 | Observation + Finishers + Exit Survey |
| Chapter 7 | Educator Details + New Teacher Survey |
| Chapter 8 | All datasets |

> ⚠️ **Note:** The Principal Perception dataset and New Teacher Survey dataset come from the *same* I2I report and look identical when exported. Rename them manually before uploading:
> - Principal Perception → `principal_perceptions`
> - New Teacher Survey → `teacher_perceptions`

---

## 🚀 Getting Started

Pick the guide for your operating system below. Each guide assumes **no prior coding experience** — just copy and paste each command into your terminal (one at a time) and press Enter.

---

### 🪟 Windows Setup

**To open a terminal:** Press `Windows key`, type `Command Prompt` (or `PowerShell`), and hit Enter.

#### Step 1: Check if Python is Already Installed

```bash
python --version
```

**✅ If Python IS installed** — you'll see something like `Python 3.11.4`. Skip to Step 2.

**❌ If Python is NOT installed** — you'll see an error like `'python' is not recognized`:
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Click **Download Python** (it auto-detects Windows)
3. Run the installer — **important:** check the box that says **"Add Python to PATH"** before clicking Install
4. Once finished, close and reopen your terminal, then run `python --version` again to confirm

#### Step 2: Check if Git is Already Installed

```bash
git --version
```

**✅ If Git IS installed** — skip to Step 3.

**❌ If Git is NOT installed:**
1. Go to [git-scm.com/download/win](https://git-scm.com/download/win)
2. Download and run the installer, clicking **Next** through the default options
3. Close and reopen your terminal, then run `git --version` again to confirm

#### Step 3: Download the Project

```bash
git clone https://github.com/takshb21/asep_dashboard.git
cd asep_dashboard
```

#### Step 4: Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

✅ You'll know it worked when you see `(venv)` appear at the start of the line.

#### Step 5: Install Required Packages

```bash
pip install -r requirements.txt
```

Let it run until it returns to a normal prompt (may take a minute or two).

#### Step 6: Build the Desktop App

```bash
streamlit-desktop-app build app.py --name MyDashboard --pyinstaller-options --onefile --noconfirm --add-data "images;images" --add-data "utils\dataset_download_info.pdf;utils" --add-data "%VIRTUAL_ENV%\Lib\site-packages\streamlit_theme\frontend\dist;streamlit_theme\frontend\dist" --collect-submodules=utils --hidden-import=enable_downloads --hidden-import=utils.certificate_chart --hidden-import=utils.chapter_3_calculations --hidden-import=utils.chapter_4_calculations --hidden-import=utils.chapter_5_calculations --hidden-import=utils.chapter_6_calculations --hidden-import=utils.chapter_7_calculations --hidden-import=utils.data_management --hidden-import=utils.gauge
```

This can take several minutes — let it run until the prompt returns.

#### Step 7: Open the App

1. Open File Explorer and go into the `asep_dashboard` folder, then the new `dist` folder
2. Double-click **MyDashboard.exe**
3. If Windows shows a "Windows protected your PC" warning, click **More info** → **Run anyway**

#### Running It Again Later

```bash
cd asep_dashboard
venv\Scripts\activate
```

Then launch the app from the `dist` folder as normal.

---

### 🍎 macOS Setup

**To open Terminal:** Press `Cmd + Space`, type `Terminal`, and hit Enter.

#### Step 1: Check if Python is Already Installed

```bash
python3 --version
```

**✅ If Python IS installed** — you'll see something like `Python 3.11.4`. Skip to Step 2.

**❌ If Python is NOT installed** — you'll see an error like `command not found: python3`:
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Click the yellow **Download Python** button (it auto-detects macOS)
3. Open the downloaded `.pkg` file and click through the installer (Continue → Continue → Agree → Install)
4. Enter your Mac password if asked
5. Close and reopen Terminal, then run `python3 --version` again to confirm

#### Step 2: Check if Git is Already Installed

```bash
git --version
```

**✅ If Git IS installed** — skip to Step 3.

**❌ If Git is NOT installed:**
A popup will appear asking to install "Command Line Developer Tools." Click **Install**, agree to the terms, and wait a few minutes. Then run `git --version` again to confirm.

#### Step 3: Download the Project

```bash
git clone https://github.com/takshb21/asep_dashboard.git
cd asep_dashboard
```

#### Step 4: Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

✅ You'll know it worked when you see `(venv)` appear at the start of the line.

#### Step 5: Install Required Packages

```bash
pip install -r requirements.txt
```

Let it run until it returns to a normal prompt (may take a minute or two).

#### Step 6: Build the Desktop App

```bash
streamlit-desktop-app build app.py --name MyDashboard --pyinstaller-options --onefile --noconfirm --add-data "images:images" --add-data "utils/dataset_download_info.pdf:utils" --add-data "$VIRTUAL_ENV/lib/python3.*/site-packages/streamlit_theme/frontend/dist:streamlit_theme/frontend/dist" --collect-submodules=utils --hidden-import=enable_downloads --hidden-import=utils.certificate_chart --hidden-import=utils.chapter_3_calculations --hidden-import=utils.chapter_4_calculations --hidden-import=utils.chapter_5_calculations --hidden-import=utils.chapter_6_calculations --hidden-import=utils.chapter_7_calculations --hidden-import=utils.data_management --hidden-import=utils.gauge
```

This can take several minutes — let it run until the prompt returns.

#### Step 7: Open the App

1. In Terminal, type `open dist` and press Enter to open the `dist` folder in Finder
2. Double-click **MyDashboard**
3. If macOS blocks it ("unidentified developer"): **right-click** (or Control-click) **MyDashboard** → **Open** → **Open** again in the popup. You only need to do this once.

#### Running It Again Later

```bash
cd asep_dashboard
source venv/bin/activate
```

Then launch the app from the `dist` folder as normal.

---

## 🧭 How to Use the App

1. **Go to Data Management** — Upload the required Excel/CSV files for the chapters you need.
2. **Rename before uploading if prompted** — Some files look identical when exported and must be renamed manually first.
3. **Confirm the files were recognized** — The page shows an arrow (➡️) mapping your original file name to the renamed name the app uses internally.
4. **Go to Dashboard** — Each Chapter tab auto-populates once its required datasets are uploaded. A tab showing a warning means a file is still missing.
5. **Check Chapter 8** — View the combined, weighted ASEP Index Score with a color-coded gauge (🟢 ≥85%, 🟡 80–85%, 🔴 <80%).
6. **Use Feedback** — Report issues or request changes anytime through the built-in form.

---

## 🔒 Data Security

When running the desktop version of this application, data files will never leave your hard drive. The software is designed to run entirely locally so that private student information never leaves the environment from which it was originally downloaded. The software neither operates nor stores data in any environment other than where you originally downloaded the files.

If you are unable to run the desktop version, we have developed a [Streamlit](https://asepdashboard-kqt5fwct9wzlnxgqnf2qsb.streamlit.app/) site that allows users to access the tool from a browser. Streamlit is [SOC 2 Type 1 compliant](https://discuss.streamlit.io/t/streamlit-cloud-is-now-soc-2-type-1-compliant/20850), and more information on their security practices is available [here](https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/trust-and-security).

---

## 🗄️ Project Structure

```
.
.
├── app.py                          # Main Streamlit app (navigation, pages, ASEP score calculation)
├── enable_downloads.py             # Configures PyWebView to allow file downloads in the desktop window
├── utils/
│   ├── data_management.py          # File upload, renaming, and download helpers
│   ├── chapter_3_calculations.py   # Indicator 1a/1b: exam pass rate calculations
│   ├── chapter_4_calculations.py   # Indicator 2: principal perception survey calculations
│   ├── chapter_5_calculations.py   # Indicator 3: student growth calculations
│   ├── chapter_6_calculations.py   # Indicator 4a/4b: field supervision calculations
│   ├── chapter_7_calculations.py   # Indicator 5: new teacher survey calculations
│   └── dataset_download_info.pdf   # Step-by-step dataset download guide
├── images/
│   ├── black_company_logo.png      # Light theme logo
│   └── white_company_logo.png      # Dark theme logo
└── requirements.txt
```

---

## 💬 Contributing / Feedback

Found a bug or have a feature request? Use the **Feedback** page inside the app, or open an issue in this repository.

---

## 👥 I2I Workgroup Members

The workgroup was initiated by the UT System's ElevateTXed initiative and has evolved to include participants from multiple institutions and systems, reflecting its broader statewide scope:

- **Taksh Beladiya** — Graduate Research Assistant, The University of Texas System
- **Kevin Badgett** — Dean, College of Education, Sul Ross State University
- **Michelle Lowry** — Senior Software Developer/Analyst, UTeach, The University of Texas at Austin
- **Michael Marder** — Executive Director, UTeach Natural Sciences, The University of Texas at Austin
- **Jeremy Martin** — Senior Research & Policy Analyst, The University of Texas System
- **Emma Savage-Davis** — Dean, College of Education and Human Development, TAMU-San Antonio
- **Robin Kapavik** — Associate Dean, College of Education and Human Development, TAMU-San Antonio

---

## ✉️ Contact

For questions or comments, please contact Jeremy Martin at [jemartin@utsystem.edu](mailto:jemartin@utsystem.edu).

For source code and pull requests, please visit Taksh Beladiya's GitHub page at [github.com/takshb21/asep_dashboard](https://github.com/takshb21/asep_dashboard).

---

## 🎓 Credits

**Special thanks** to the **University of Texas at Arlington** for their partnership and support in making this project possible.