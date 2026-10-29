tea_dashboard_validation_chart = {
    # =========================================================================
    # SUPPLEMENTAL CREDENTIALS (Can cross-apply to ALL GRADE LEVELS)
    # =========================================================================
    "Supplemental": {
        "Bilingual Education": {
            "ALL GRADE LEVELS": ["Foreign Language", "Self-Contained", "Other"],
            "PRE-KINDERGARTEN": ["Self-Contained", "English Language Arts"],
            "KINDERGARTEN": ["Self-Contained", "English Language Arts"],
            "KINDERGARTEN/ELEMENTARY (K-6)": ["Self-Contained", "English Language Arts", "Mathematics", "Science", "Social Studies"]
        },
        "Special Education": {
            "ALL GRADE LEVELS": ["Special Education", "Self-Contained", "Non-Classroom Role"],
            "MIDDLE SCHOOL (GRADES 6 - 8)": ["Special Education", "Self-Contained"],
            "GRADES 9-12": ["Special Education", "Self-Contained", "Career & Technology Education"]
        }
    },

    # =========================================================================
    # EARLY CHILDHOOD TO ELEMENTARY (EC-6)
    # =========================================================================
    "Grades EC-6": {
        "General Elementary (Self-Contained)": {
            "EARLY EDUCATION": ["Self-Contained", "Other"],
            "PRE-KINDERGARTEN": ["Self-Contained"],
            "KINDERGARTEN": ["Self-Contained"],
            "KINDERGARTEN/ELEMENTARY (K-6)": ["Self-Contained", "English Language Arts", "Mathematics", "Science", "Social Studies"],
            "FIRST GRADE": ["Self-Contained"], "SECOND GRADE": ["Self-Contained"], "THIRD GRADE": ["Self-Contained"], 
            "FOURTH GRADE": ["Self-Contained"], "FIFTH GRADE": ["Self-Contained"], "SIXTH GRADE": ["Self-Contained"]
        },
        "English Language Arts": {
            "KINDERGARTEN/ELEMENTARY (K-6)": ["English Language Arts"],
            "SIXTH GRADE": ["English Language Arts"],
            "MIDDLE SCHOOL (GRADES 6 - 8)": ["English Language Arts"]  # Grade 6 overlap
        },
        "Mathematics": {
            "KINDERGARTEN/ELEMENTARY (K-6)": ["Mathematics"],
            "SIXTH GRADE": ["Mathematics"]
        },
        "Science": {
            "KINDERGARTEN/ELEMENTARY (K-6)": ["Science"],
            "SIXTH GRADE": ["Science"]
        },
        "Social Studies": {
            "KINDERGARTEN/ELEMENTARY (K-6)": ["Social Studies"],
            "SIXTH GRADE": ["Social Studies"]
        },
        "Bilingual Education": {
            "PRE-KINDERGARTEN": ["Self-Contained"],
            "KINDERGARTEN": ["Self-Contained"],
            "KINDERGARTEN/ELEMENTARY (K-6)": ["Self-Contained", "English Language Arts"]
        }
    },

    # =========================================================================
    # MIDDLE SCHOOL BAND (4-8)
    # =========================================================================
    "Grades 4-8": {
        "General Elementary (Self-Contained)": {
            "FOURTH GRADE": ["Self-Contained"],
            "FIFTH GRADE": ["Self-Contained"],
            "KINDERGARTEN/ELEMENTARY (K-6)": ["Self-Contained"]  # Validates the 4-5 elementary range
        },
        "English Language Arts": {
            "FOURTH GRADE": ["English Language Arts"], "FIFTH GRADE": ["English Language Arts"], "SIXTH GRADE": ["English Language Arts"],
            "SEVENTH GRADE": ["English Language Arts"], "EIGHTH GRADE": ["English Language Arts"],
            "MIDDLE SCHOOL (GRADES 6 - 8)": ["English Language Arts"]
        },
        "Mathematics": {
            "FOURTH GRADE": ["Mathematics"], "FIFTH GRADE": ["Mathematics"], "SIXTH GRADE": ["Mathematics"],
            "SEVENTH GRADE": ["Mathematics"], "EIGHTH GRADE": ["Mathematics"],
            "MIDDLE SCHOOL (GRADES 6 - 8)": ["Mathematics"]
        },
        "Science": {
            "FOURTH GRADE": ["Science"], "FIFTH GRADE": ["Science"], "SIXTH GRADE": ["Science"],
            "SEVENTH GRADE": ["Science"], "EIGHTH GRADE": ["Science"],
            "MIDDLE SCHOOL (GRADES 6 - 8)": ["Science"]
        },
        "Social Studies": {
            "FOURTH GRADE": ["Social Studies"], "FIFTH GRADE": ["Social Studies"], "SIXTH GRADE": ["Social Studies"],
            "SEVENTH GRADE": ["Social Studies"], "EIGHTH GRADE": ["Social Studies"],
            "MIDDLE SCHOOL (GRADES 6 - 8)": ["Social Studies"]
        }
    },

    # =========================================================================
    # HIGH SCHOOL & SECONDARY BANDS (6-12 & 7-12)
    # =========================================================================
    "Grades 6-12": {
        "English Language Arts": {
            "SIXTH GRADE": ["English Language Arts"], "SEVENTH GRADE": ["English Language Arts"], "EIGHTH GRADE": ["English Language Arts"],
            "MIDDLE SCHOOL (GRADES 6 - 8)": ["English Language Arts"],
            "GRADES 9-12": ["English Language Arts"]
        },
        "Social Studies": {
            "SIXTH GRADE": ["Social Studies"], "SEVENTH GRADE": ["Social Studies"], "EIGHTH GRADE": ["Social Studies"],
            "MIDDLE SCHOOL (GRADES 6 - 8)": ["Socsial Studies"],
            "GRADES 9-12": ["Social Studies"]
        }
    },

    "Grades 7-12": {
        "Social Studies": {
            "SEVENTH GRADE": ["Social Studies"],
            "EIGHTH GRADE": ["Social Studies"],
            "MIDDLE SCHOOL (GRADES 6 - 8)": ["Social Studies"],
            "GRADES 9-12": ["Social Studies"]
        },
        "English Language Arts": {
            "SEVENTH GRADE": ["English Language Arts"],
            "EIGHTH GRADE": ["English Language Arts"],
            "MIDDLE SCHOOL (GRADES 6 - 8)": ["English Language Arts"],
            "GRADES 9-12": ["English Language Arts"]
        },
        "Mathematics": {
            "SEVENTH GRADE": ["Mathematics"], "EIGHTH GRADE": ["Mathematics"],
            "MIDDLE SCHOOL (GRADES 6 - 8)": ["Mathematics"],
            "GRADES 9-12": ["Mathematics"]
        },
        "Science": {
            "SEVENTH GRADE": ["Science"], "EIGHTH GRADE": ["Science"],
            "MIDDLE SCHOOL (GRADES 6 - 8)": ["Science"],
            "GRADES 9-12": ["Science"]
        },
        # THE KINDERGARTEN CROSSOVER EXCEPTION
        "Bilingual Education": {
            "PRE-KINDERGARTEN": ["Foreign Language"],
            "KINDERGARTEN": ["Foreign Language"],
            "KINDERGARTEN/ELEMENTARY (K-6)": ["Foreign Language"],
            "GRADES 9-12": ["Foreign Language"]
        }
    },

    # =========================================================================
    # ALL-LEVEL SYSTEM-WIDE CREDENTIALS (EC-12)
    # =========================================================================
    "Grades EC-12": {
        "Special Education": {
            "ALL GRADE LEVELS": ["Special Education"],
            "EARLY EDUCATION": ["Special Education"], "PRE-KINDERGARTEN": ["Special Education"], "KINDERGARTEN": ["Special Education"],
            "KINDERGARTEN/ELEMENTARY (K-6)": ["Special Education", "Self-Contained"],
            "MIDDLE SCHOOL (GRADES 6 - 8)": ["Special Education"],
            "GRADES 9-12": ["Special Education"],
            "NOT APPLICABLE": ["Non-Classroom Role"]
        },
        "Fine Arts": {
            "KINDERGARTEN/ELEMENTARY (K-6)": ["Fine Arts"],
            "MIDDLE SCHOOL (GRADES 6 - 8)": ["Fine Arts"],
            "GRADES 9-12": ["Fine Arts"]
        },
        "Health & Physical Education": {
            "KINDERGARTEN/ELEMENTARY (K-6)": ["Physical Ed. & Health"],
            "MIDDLE SCHOOL (GRADES 6 - 8)": ["Physical Ed. & Health"],
            "GRADES 9-12": ["Physical Ed. & Health"]
        }
    }
}


import pandas as pd

def filter_valid_assignments(df):
    # 1. Ensure the required columns exist in the input dataframe
    required_cols = [
        "Certification Grade Level", 
        "Certification Subject Area", 
        "Teaching Grade Level", 
        "Teaching Subject Area"
    ]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column in DataFrame: '{col}'")
            
    # 2. Flatten the nested validation dictionary into a list of tuples
    flat_records = []
    for cert_grade, cert_subjects in tea_dashboard_validation_chart.items():
        for cert_subject, teach_grades in cert_subjects.items():
            for teach_grade, teach_subjects in teach_grades.items():
                for teach_sub in teach_subjects:
                    flat_records.append({
                        "Certification Grade Level": cert_grade,
                        "Certification Subject Area": cert_subject,
                        "Teaching Grade Level": teach_grade,
                        "Teaching Subject Area": teach_sub
                    })
                    
    # 3. Create a master reference DataFrame of valid combinations
    ref_df = pd.DataFrame(flat_records)
    
    # 4. Use an inner join to filter the original dataframe down to matches only
    valid_df = df.merge(ref_df, on=required_cols, how="inner")
    
    return valid_df