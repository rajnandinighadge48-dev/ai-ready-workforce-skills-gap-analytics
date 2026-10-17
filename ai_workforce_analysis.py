from pathlib import Path
import pandas as pd

# AI Ready Workforce and Skills Gap Analytics
print("=" * 55)
print(" AI READY WORKFORCE AND SKILLS GAP ANALYTICS")
print("=" * 55)

# Find project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Find Dataset folder
DATASET_FOLDER = BASE_DIR / "Dataset"

print("\nChecking Dataset folder...")

if not DATASET_FOLDER.exists():
    print("ERROR: Dataset folder not found.")
else:
    print("Dataset folder found!")

    # Find Excel files automatically
    excel_files = list(DATASET_FOLDER.glob("*.xlsx"))

    if not excel_files:
        print("ERROR: No Excel file found in Dataset folder.")

    else:
        DATA_FILE = excel_files[0]

        print("\nExcel file found:", DATA_FILE.name)

        try:
            df = pd.read_excel(DATA_FILE)

            print("\nExcel file opened successfully!")
            print("\nFirst 5 rows:")
            print(df.head().to_string(index=False))

            print("\nDataset Shape:")
            print("Rows:", df.shape[0])
            print("Columns:", df.shape[1])

            print("\nColumn Names:")
            print(df.columns.tolist())

        except Exception as e:
            print("\nError opening Excel file:")
            print(e)

print("\n" + "=" * 55)
print("PYTHON DATA CHECK COMPLETED")
print("=" * 55)

# ============================================================
# PROJECT: AI READY WORKFORCE AND SKILLS GAP ANALYTICS
# TOOL: PYTHON, PANDAS, MATPLOTLIB, OPENPYXL
# ============================================================

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

# ------------------------------------------------------------
# 1. PROJECT PATHS
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_FOLDER = BASE_DIR / "Dataset"
PYTHON_FOLDER = Path(__file__).resolve().parent
OUTPUT_FOLDER = PYTHON_FOLDER / "output"
CHART_FOLDER = OUTPUT_FOLDER / "charts"

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
CHART_FOLDER.mkdir(parents=True, exist_ok=True)

print("=" * 65)
print("AI READY WORKFORCE AND SKILLS GAP ANALYTICS")
print("=" * 65)

# ------------------------------------------------------------
# 2. FIND EXCEL DATASET AUTOMATICALLY
# ------------------------------------------------------------

if not DATASET_FOLDER.exists():
    raise FileNotFoundError(
        f"Dataset folder not found: {DATASET_FOLDER}\n"
        "Check whether Dataset is inside the main project folder."
    )

excel_files = [
    file for file in DATASET_FOLDER.glob("*.xlsx")
    if not file.name.startswith("~$")
]

if not excel_files:
    excel_files = [
        file for file in DATASET_FOLDER.glob("*.xls")
        if not file.name.startswith("~$")
    ]

if not excel_files:
    raise FileNotFoundError(
        "No Excel dataset found inside the Dataset folder."
    )

DATA_FILE = excel_files[0]

print("\nDataset file:", DATA_FILE.name)

# ------------------------------------------------------------
# 3. LOAD RAW DATA
# ------------------------------------------------------------

excel_file = pd.ExcelFile(DATA_FILE)

print("\nAvailable Excel sheets:")
for sheet in excel_file.sheet_names:
    print("-", sheet)

# Prefer Raw_Data if available.
# Otherwise, use the first worksheet.

matching_sheets = {
    sheet.strip().lower(): sheet
    for sheet in excel_file.sheet_names
}

if "raw_data" in matching_sheets:
    SHEET_NAME = matching_sheets["raw_data"]
else:
    SHEET_NAME = excel_file.sheet_names[0]

df = pd.read_excel(
    DATA_FILE,
    sheet_name=SHEET_NAME
)

if df.empty:
    raise ValueError(
        "The selected worksheet contains no data."
    )

print("\nWorksheet selected:", SHEET_NAME)
print("Original rows:", len(df))
print("Original columns:", len(df.columns))

# ------------------------------------------------------------
# 4. CLEAN COLUMN NAMES
# ------------------------------------------------------------

df.columns = (
    df.columns.astype(str)
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)

# Remove completely empty rows and columns.

df = df.dropna(how="all")
df = df.dropna(axis=1, how="all")

# Trim spaces from text values.

for column in df.select_dtypes(include=["object"]).columns:
    df[column] = df[column].map(
        lambda value: value.strip()
        if isinstance(value, str)
        else value
    )

# ------------------------------------------------------------
# 5. DATA QUALITY ANALYSIS
# ------------------------------------------------------------

original_row_count = len(df)

duplicate_count = int(df.duplicated().sum())

missing_values = df.isna().sum()

missing_summary = pd.DataFrame({
    "Column": df.columns,
    "Missing_Values": missing_values.values,
    "Missing_Percentage": (
        missing_values.values / max(len(df), 1) * 100
    ).round(2)
})

# Remove exact duplicate rows.

df = df.drop_duplicates().copy()

print("\n" + "-" * 65)
print("DATA QUALITY ANALYSIS")
print("-" * 65)

print("Rows before duplicate removal:", original_row_count)
print("Duplicate rows removed:", duplicate_count)
print("Rows after duplicate removal:", len(df))
print("Total missing cells:", int(df.isna().sum().sum()))

# ------------------------------------------------------------
# 6. IDENTIFY NUMERIC COLUMNS
# ------------------------------------------------------------

for column in df.columns:
    if df[column].dtype == "object":
        cleaned_values = (
            df[column].astype(str)
            .str.strip()
            .str.replace(",", "", regex=False)
        )

        converted = pd.to_numeric(
            cleaned_values,
            errors="coerce"
        )

        non_empty = df[column].notna().sum()

        if non_empty > 0:
            conversion_rate = (
                converted.notna().sum() / non_empty
            )

            if conversion_rate >= 0.85:
                df[column] = converted

numeric_columns = df.select_dtypes(
    include="number"
).columns.tolist()

categorical_columns = df.select_dtypes(
    include=["object", "category", "bool"]
).columns.tolist()

# ------------------------------------------------------------
# 7. IDENTIFY IMPORTANT WORKFORCE COLUMNS
# ------------------------------------------------------------

def find_column(keywords):
    """
    Find a column using case-insensitive keyword matching.
    Returns None if no suitable column is found.
    """

    for column in df.columns:
        normalized = (
            column.lower()
            .replace("_", " ")
            .replace("-", " ")
        )

        if any(
            keyword.lower() in normalized
            for keyword in keywords
        ):
            return column

    return None


department_col = find_column(["department"])

job_role_col = find_column(["job role", "job title"])

gender_col = find_column(["gender"])

skill_gap_col = find_column(["skill gap level"])

future_role_col = find_column(["future role interest"])

employee_id_col = find_column([
    "employee id",
    "candidate id",
    "staff id",
    "worker id"
])

# ------------------------------------------------------------
# 8. BUILD DATA QUALITY REPORT
# ------------------------------------------------------------

quality_report = pd.DataFrame({
    "Metric": [
        "Dataset File",
        "Worksheet",
        "Rows After Cleaning",
        "Number of Columns",
        "Duplicate Rows Removed",
        "Missing Cells Remaining",
        "Numeric Columns",
        "Categorical Columns"
    ],
    "Value": [
        DATA_FILE.name,
        SHEET_NAME,
        len(df),
        len(df.columns),
        duplicate_count,
        int(df.isna().sum().sum()),
        len(numeric_columns),
        len(categorical_columns)
    ]
})

# ------------------------------------------------------------
# 9. NUMERIC SUMMARY
# ------------------------------------------------------------

if numeric_columns:
    numeric_summary = df[numeric_columns].describe().T

    numeric_summary = numeric_summary.reset_index()

    numeric_summary = numeric_summary.rename(
        columns={"index": "Metric"}
    )

    numeric_summary = numeric_summary.round(2)

else:
    numeric_summary = pd.DataFrame({
        "Message": ["No numeric columns were identified."]
    })

# ------------------------------------------------------------
# 10. IDENTIFY SKILLS AND READINESS SCORES
# ------------------------------------------------------------

def normalize_name(column):
    return (
        column.lower()
        .replace("_", " ")
        .replace("-", " ")
        .strip()
    )


def is_score_column(column):
    """
    Identify score columns using their names.
    Excludes unrelated numeric measures such as Age and Experience.
    """

    name = normalize_name(column)

    score_keywords = [
        "score",
        "rating",
        "learning agility",
        "technical skills",
        "productivity",
        "goal achievement",
        "job satisfaction",
        "performance",
        "ai readiness"
    ]

    return any(
        keyword in name
        for keyword in score_keywords
    )


score_columns = [
    column for column in numeric_columns
    if is_score_column(column)
]

# ------------------------------------------------------------
# 11. CALCULATE AI READINESS SCORE
# ------------------------------------------------------------

readiness_keywords = [
    "technical skills",
    "learning agility",
    "productivity",
    "goal achievement",
    "tools score",
    "ai readiness"
]

readiness_columns = []

for column in score_columns:
    name = normalize_name(column)

    if any(
        keyword in name
        for keyword in readiness_keywords
    ):
        readiness_columns.append(column)

# Use existing score columns if no specific readiness
# indicators are found.

if not readiness_columns:
    readiness_columns = score_columns.copy()

if readiness_columns:

    score_data = df[readiness_columns].copy()

    # A score is assumed to be out of 10 only when
    # the observed data supports that scale.

    for column in readiness_columns:

        values = score_data[column].dropna()

        if len(values) == 0:
            continue

        if values.min() >= 0 and values.max() <= 10:

            score_data[column] = (
                score_data[column] / 10 * 100
            )

        elif values.min() >= 0 and values.max() <= 100:

            score_data[column] = score_data[column]

        else:

            minimum = values.min()
            maximum = values.max()

            if maximum > minimum:
                score_data[column] = (
                    (score_data[column] - minimum)
                    / (maximum - minimum)
                    * 100
                )
            else:
                score_data[column] = 100.0

    df["AI_Readiness_Score"] = (
        score_data.mean(axis=1)
    ).round(2)

    def readiness_category(score):

        if pd.isna(score):
            return "Insufficient Data"

        if score >= 75:
            return "High Readiness"

        elif score >= 50:
            return "Moderate Readiness"

        return "Needs Development"

    df["AI_Readiness_Category"] = (
        df["AI_Readiness_Score"]
        .apply(readiness_category)
    )

    readiness_summary = (
        df["AI_Readiness_Category"]
        .value_counts(dropna=False)
        .rename_axis("Readiness_Category")
        .reset_index(name="Count")
    )

    average_readiness = round(
        df["AI_Readiness_Score"].mean(), 2
    )

else:

    df["AI_Readiness_Score"] = pd.NA

    df["AI_Readiness_Category"] = "Insufficient Data"

    readiness_summary = pd.DataFrame({
        "Readiness_Category": ["Insufficient Data"],
        "Count": [len(df)]
    })

    average_readiness = None

print("\n" + "-" * 65)
print("AI READINESS ANALYSIS")
print("-" * 65)

print("Readiness indicators:", readiness_columns)

if average_readiness is not None:
    print("Average AI Readiness Score:", average_readiness)
else:
    print("No suitable readiness score columns were found.")

# Note: This is a transparent, rule-based score,
# not a trained machine-learning prediction.

# ------------------------------------------------------------
# 12. DEPARTMENT-WISE WORKFORCE ANALYSIS
# ------------------------------------------------------------

if department_col:

    department_summary = (
        df.groupby(department_col, dropna=False)
        .size()
        .reset_index(name="Employee_Count")
    )

    department_summary = department_summary.sort_values(
        "Employee_Count",
        ascending=False
    )

    if "AI_Readiness_Score" in df.columns:

        department_readiness = (
            df.groupby(department_col, dropna=False)
            ["AI_Readiness_Score"]
            .mean()
            .reset_index()
        )

        department_readiness = (
            department_readiness.rename(
                columns={
                    "AI_Readiness_Score":
                    "Average_AI_Readiness_Score"
                }
            )
        )

        department_summary = department_summary.merge(
            department_readiness,
            on=department_col,
            how="left"
        )

        department_summary[
            "Average_AI_Readiness_Score"
        ] = department_summary[
            "Average_AI_Readiness_Score"
        ].round(2)

else:

    department_summary = pd.DataFrame({
        "Message": [
            "Department column was not found."
        ]
    })

# ------------------------------------------------------------
# 13. JOB ROLE ANALYSIS
# ------------------------------------------------------------

if job_role_col:

    job_role_summary = (
        df.groupby(job_role_col, dropna=False)
        .size()
        .reset_index(name="Employee_Count")
    )

    job_role_summary = job_role_summary.sort_values(
        "Employee_Count",
        ascending=False
    )

else:

    job_role_summary = pd.DataFrame({
        "Message": ["Job Role column was not found."]
    })

# ------------------------------------------------------------
# 14. SKILLS GAP ANALYSIS
# ------------------------------------------------------------

if skill_gap_col:

    skills_gap_summary = (
        df[skill_gap_col]
        .fillna("Unknown")
        .astype(str)
        .value_counts()
        .rename_axis("Skill_Gap_Level")
        .reset_index(name="Employee_Count")
    )

else:

    skills_gap_summary = pd.DataFrame({
        "Message": [
            "Skill Gap Level column was not found."
        ]
    })

# ------------------------------------------------------------
# 15. TRAINING NEEDS ANALYSIS
# ------------------------------------------------------------

training_hours_col = find_column([
    "training hours",
    "training hour"
])

if training_hours_col:

    df[training_hours_col] = pd.to_numeric(
        df[training_hours_col],
        errors="coerce"
    )

    training_summary = pd.DataFrame({
        "Metric": [
            "Average Training Hours",
            "Minimum Training Hours",
            "Maximum Training Hours",
            "Employees with Zero Training Hours",
            "Employees with Missing Training Hours"
        ],
        "Value": [
            round(df[training_hours_col].mean(), 2),
            df[training_hours_col].min(),
            df[training_hours_col].max(),
            int((df[training_hours_col] == 0).sum()),
            int(df[training_hours_col].isna().sum())
        ]
    })

else:

    training_summary = pd.DataFrame({
        "Message": [
            "Training Hours column was not found."
        ]
    })

# ------------------------------------------------------------
# 16. CATEGORICAL SUMMARIES
# ------------------------------------------------------------

category_summaries = []

for column in categorical_columns:

    counts = (
        df[column]
        .fillna("Missing")
        .astype(str)
        .value_counts()
        .rename_axis("Category")
        .reset_index(name="Count")
    )

    counts.insert(0, "Column", column)

    category_summaries.append(counts)

if category_summaries:

    category_summary = pd.concat(
        category_summaries,
        ignore_index=True
    )

else:

    category_summary = pd.DataFrame({
        "Message": [
            "No categorical columns were identified."
        ]
    })

# ------------------------------------------------------------
# 17. CREATE CHARTS
# ------------------------------------------------------------

plt.close("all")

# Chart 1: Department Workforce Distribution

if department_col:

    chart_data = (
        df[department_col]
        .fillna("Unknown")
        .astype(str)
        .value_counts()
    )

    if not chart_data.empty:

        plt.figure(figsize=(10, 6))

        chart_data.plot(kind="bar")

        plt.title("Workforce Distribution by Department")
        plt.xlabel("Department")
        plt.ylabel("Number of Employees")

        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        plt.savefig(
            CHART_FOLDER / "01_department_distribution.png",
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

# Chart 2: AI Readiness Distribution

if "AI_Readiness_Category" in df.columns:

    chart_data = (
        df["AI_Readiness_Category"]
        .value_counts()
    )

    if not chart_data.empty:

        plt.figure(figsize=(8, 6))

        chart_data.plot(kind="bar")

        plt.title("AI Readiness Distribution")
        plt.xlabel("Readiness Category")
        plt.ylabel("Number of Employees")

        plt.xticks(rotation=25, ha="right")
        plt.tight_layout()

        plt.savefig(
            CHART_FOLDER / "02_ai_readiness_distribution.png",
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

# Chart 3: Skills Gap Distribution

if skill_gap_col:

    chart_data = (
        df[skill_gap_col]
        .fillna("Unknown")
        .astype(str)
        .value_counts()
    )

    if not chart_data.empty:

        plt.figure(figsize=(8, 6))

        chart_data.plot(kind="bar")

        plt.title("Workforce Skills Gap Distribution")
        plt.xlabel("Skill Gap Level")
        plt.ylabel("Number of Employees")

        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()

        plt.savefig(
            CHART_FOLDER / "03_skills_gap_distribution.png",
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

# Chart 4: Average Score Indicators

if readiness_columns:

    average_scores = (
        df[readiness_columns]
        .mean()
        .sort_values(ascending=False)
    )

    if not average_scores.empty:

        plt.figure(figsize=(10, 6))

        average_scores.plot(kind="bar")

        plt.title("Average Workforce Readiness Indicators")
        plt.xlabel("Score Indicator")
        plt.ylabel("Average Score (Normalized to 0-100)")

        plt.xticks(rotation=35, ha="right")
        plt.tight_layout()

        plt.savefig(
            CHART_FOLDER / "04_readiness_indicators.png",
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

# ------------------------------------------------------------
# 18. CREATE FINAL EXCEL REPORT
# ------------------------------------------------------------

REPORT_FILE = (
    OUTPUT_FOLDER
    / "AI_Ready_Workforce_Professional_Report.xlsx"
)

with pd.ExcelWriter(
    REPORT_FILE,
    engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        sheet_name="Data_Cleaned",
        index=False
    )

    quality_report.to_excel(
        writer,
        sheet_name="Data_Quality",
        index=False
    )

    missing_summary.to_excel(
        writer,
        sheet_name="Missing_Values",
        index=False
    )

    numeric_summary.to_excel(
        writer,
        sheet_name="Numeric_Summary",
        index=False
    )

    category_summary.to_excel(
        writer,
        sheet_name="Category_Summary",
        index=False
    )

    department_summary.to_excel(
        writer,
        sheet_name="Department_Analysis",
        index=False
    )

    job_role_summary.to_excel(
        writer,
        sheet_name="Job_Role_Analysis",
        index=False
    )

    skills_gap_summary.to_excel(
        writer,
        sheet_name="Skills_Gap_Analysis",
        index=False
    )

    readiness_summary.to_excel(
        writer,
        sheet_name="AI_Readiness",
        index=False
    )

    training_summary.to_excel(
        writer,
        sheet_name="Training_Analysis",
        index=False
    )

# ------------------------------------------------------------
# 19. FORMAT THE EXCEL REPORT
# ------------------------------------------------------------

from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

from openpyxl import load_workbook

workbook = load_workbook(REPORT_FILE)

for worksheet in workbook.worksheets:

    worksheet.freeze_panes = "A2"

    worksheet.auto_filter.ref = worksheet.dimensions

    for cell in worksheet[1]:

        cell.font = Font(
            bold=True,
            color="FFFFFF"
        )

        cell.fill = PatternFill(
            fill_type="solid",
            fgColor="17365D"
        )

        cell.alignment = Alignment(
            horizontal="center",
            vertical="center",
            wrap_text=True
        )

    worksheet.row_dimensions[1].height = 30

    for column_cells in worksheet.columns:

        max_length = 0

        column_letter = get_column_letter(
            column_cells[0].column
        )

        for cell in column_cells:

            cell.alignment = Alignment(
                vertical="center",
                wrap_text=True
            )

            if cell.value is not None:

                max_length = max(
                    max_length,
                    len(str(cell.value))
                )

        worksheet.column_dimensions[
            column_letter
        ].width = min(max(max_length + 3, 12), 35)

workbook.save(REPORT_FILE)

# ------------------------------------------------------------
# 20. FINAL PROJECT SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 65)
print("PROJECT EXECUTION COMPLETED")
print("=" * 65)

print("\nFINAL RESULTS")

print("Total Employees / Records:", len(df))
print("Total Columns:", len(df.columns))
print("Duplicate Rows Removed:", duplicate_count)
print("Missing Cells Remaining:", int(df.isna().sum().sum()))

if average_readiness is not None:

    print(
        "Average AI Readiness Score:",
        average_readiness
    )

print("\nREPORT SAVED AT:")
print(REPORT_FILE)

print("\nCHARTS SAVED AT:")
print(CHART_FOLDER)

print("\nGENERATED CHART FILES:")

for chart in sorted(CHART_FOLDER.glob("*.png")):
    print("-", chart.name)

print("\n" + "=" * 65)
print("AI WORKFORCE ANALYSIS FINISHED SUCCESSFULLY")
print("=" * 65)