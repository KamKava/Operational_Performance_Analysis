import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# OPERATIONAL PROJECT — SYNTHETIC DATA GENERATOR
# ============================================================

np.random.seed(42)

OUT = Path("data/raw")
OUT.mkdir(exist_ok=True)

# ------------------------------------------------------------
# MASTER DATA
# ------------------------------------------------------------

dates = pd.date_range("2026-01-01", "2026-06-30", freq="D")

regions = [
    "Scotland",
    "North East",
    "North West",
    "Midlands",
    "South West",
    "South East",
    "Wales"
]

teams = [
    "Workplace Services",
    "Facilities Response",
    "Estates Support",
    "Workplace Projects"
]

region_info = {
    "Scotland": {
        "area": "North",
        "office": "Edinburgh",
        "lead": "Regional Lead A"
    },
    "North East": {
        "area": "North",
        "office": "Newcastle",
        "lead": "Regional Lead B"
    },
    "North West": {
        "area": "North",
        "office": "Manchester",
        "lead": "Regional Lead C"
    },
    "Midlands": {
        "area": "Central",
        "office": "Birmingham",
        "lead": "Regional Lead D"
    },
    "South West": {
        "area": "South",
        "office": "Bristol",
        "lead": "Regional Lead E"
    },
    "South East": {
        "area": "South",
        "office": "Worthing",
        "lead": "Regional Lead F"
    },
    "Wales": {
        "area": "Wales",
        "office": "Cardiff",
        "lead": "Regional Lead G"
    }
}

# ============================================================
# 1. STAFFING / CAPACITY DATA
# ============================================================

staff_rows = []
staff_id = 2001

for region in regions:
    for team in teams:

        # Give each region/team a relatively stable staffing level
        base_headcount = np.random.randint(8, 22)

        for month in pd.date_range("2026-01-01", "2026-06-01", freq="MS"):

            # Small monthly staffing variation
            headcount = max(
                5,
                base_headcount + np.random.choice([-1, 0, 0, 0, 1])
            )

            working_days = len(
                pd.bdate_range(
                    month,
                    month + pd.offsets.MonthEnd(0)
                )
            )

            hours_per_day = 7.4

            available_hours = (
                headcount *
                working_days *
                hours_per_day
            )

            absence_hours = round(
                available_hours *
                np.random.uniform(0.03, 0.10),
                1
            )

            training_hours = round(
                available_hours *
                np.random.uniform(0.01, 0.05),
                1
            )

            productive_hours = round(
                max(
                    0,
                    available_hours -
                    absence_hours -
                    training_hours
                ) *
                np.random.uniform(0.72, 0.88),
                1
            )

            utilisation = round(
                productive_hours /
                max(available_hours, 1),
                3
            )

            staff_rows.append([
                f"STAFF-{staff_id}",
                month.date(),
                region,
                team,
                headcount,
                working_days,
                round(available_hours, 1),
                absence_hours,
                training_hours,
                productive_hours,
                utilisation
            ])

            staff_id += 1

staffing = pd.DataFrame(
    staff_rows,
    columns=[
        "Staff_Record_ID",
        "Month",
        "Region",
        "Team",
        "Headcount",
        "Working_Days",
        "Available_Hours",
        "Absence_Hours",
        "Training_Hours",
        "Productive_Hours",
        "Staff_Utilisation"
    ]
)

# ============================================================
# 2. INCIDENT DATA
# ============================================================

incident_types = [
    "System outage",
    "Supplier delay",
    "Staffing shortage",
    "Data quality issue",
    "Building issue",
    "Process failure",
    "Customer escalation",
    "Health & safety issue"
]

severity_levels = [
    "Low",
    "Medium",
    "High",
    "Critical"
]

statuses = [
    "Closed",
    "Closed",
    "Closed",
    "Open",
    "In Progress"
]

incident_rows = []

for i in range(1, 601):

    date = np.random.choice(dates)

    region = np.random.choice(
        regions,
        p=[
            0.15,
            0.12,
            0.16,
            0.16,
            0.12,
            0.18,
            0.11
        ]
    )

    team = np.random.choice(teams)

    severity = np.random.choice(
        severity_levels,
        p=[
            0.45,
            0.35,
            0.16,
            0.04
        ]
    )

    incident_type = np.random.choice(incident_types)

    status = np.random.choice(statuses)

    # High/Critical incidents take longer
    severity_multiplier = {
        "Low": 0.7,
        "Medium": 1.0,
        "High": 1.7,
        "Critical": 2.8
    }[severity]

    response_hours = round(
        (np.random.exponential(5) + 0.5)
        * severity_multiplier,
        1
    )

    resolution_hours = round(
        response_hours +
        np.random.exponential(18) *
        severity_multiplier,
        1
    )

    if status == "Closed":
        lesson = np.random.choice([
            "Process updated",
            "Training required",
            "Supplier action",
            "No further action",
            "Documentation updated"
        ])
    else:
        lesson = ""

    incident_rows.append([
        f"INC-{i:05d}",
        pd.Timestamp(date).date(),
        region,
        team,
        incident_type,
        severity,
        status,
        response_hours,
        resolution_hours,
        lesson
    ])

incidents = pd.DataFrame(
    incident_rows,
    columns=[
        "Incident_ID",
        "Date",
        "Region",
        "Team",
        "Incident_Type",
        "Severity",
        "Status",
        "Response_Time_Hours",
        "Resolution_Time_Hours",
        "Lesson_or_Action"
    ]
)

# ============================================================
# 3. OPERATIONAL PERFORMANCE DATA
# ============================================================

# Create lookup from staffing data
staff_lookup = staffing.set_index(
    ["Month", "Region", "Team"]
)

# Keep track of backlog by region/team
backlog_tracker = {}

operations_rows = []
record_id = 100001

for date in dates:

    # Weekends have fewer operational records
    if date.weekday() >= 5 and np.random.rand() < 0.75:
        continue

    month = pd.Timestamp(date).replace(day=1)

    for region in regions:

        for team in teams:

            key = (month.date(), region, team)

            staff = staff_lookup.loc[key]

            headcount = staff["Headcount"]
            utilisation = staff["Staff_Utilisation"]

            # ------------------------------------------------
            # Opening backlog
            # ------------------------------------------------

            previous_key = (region, team)

            opening_backlog = backlog_tracker.get(
                previous_key,
                np.random.randint(3, 15)
            )

            # ------------------------------------------------
            # Incoming demand
            # ------------------------------------------------

            base_demand = np.random.normal(42, 9)

            # South East deliberately receives higher demand
            if region == "South East":
                base_demand *= 1.12

            # Workplace Projects receives slightly lower volume
            if team == "Workplace Projects":
                base_demand *= 0.72

            # ------------------------------------------------
            # Incident pressure
            # ------------------------------------------------

            daily_incidents = incidents[
                (incidents["Date"] == date.date()) &
                (incidents["Region"] == region) &
                (incidents["Team"] == team)
            ]

            incident_count = len(daily_incidents)

            high_incidents = len(
                daily_incidents[
                    daily_incidents["Severity"].isin(
                        ["High", "Critical"]
                    )
                ]
            )

            incident_pressure = (
                incident_count * 0.025 +
                high_incidents * 0.07
            )

            requests_received = max(
                5,
                int(base_demand *
                    np.random.uniform(0.85, 1.15))
            )

            # ------------------------------------------------
            # Available capacity
            # ------------------------------------------------

            # Capacity is influenced by staffing utilisation
            capacity_factor = (
                0.82 +
                utilisation * 0.35
            )

            # Incidents reduce effective capacity
            capacity_factor *= max(
                0.70,
                1 - incident_pressure
            )

            # ------------------------------------------------
            # Total workload
            # ------------------------------------------------

            total_workload = (
                opening_backlog +
                requests_received
            )

            theoretical_capacity = (
                headcount *
                np.random.uniform(2.2, 3.0) *
                capacity_factor
            )

            requests_completed = min(
                total_workload,
                max(
                    0,
                    int(theoretical_capacity)
                )
            )

            closing_backlog = (
                total_workload -
                requests_completed
            )

            # ------------------------------------------------
            # Operational KPIs
            # ------------------------------------------------

            average_completion_days = round(
                np.clip(
                    1.5 +
                    (closing_backlog * 0.08) +
                    incident_pressure * 5 +
                    np.random.normal(0, 0.35),
                    0.5,
                    8.0
                ),
                1
            )

            sla_compliance = round(
                np.clip(
                    0.97 -
                    (closing_backlog * 0.006) -
                    incident_pressure -
                    np.random.normal(0, 0.025),
                    0.60,
                    1.00
                ),
                3
            )

            quality_pass_rate = round(
                np.clip(
                    0.985 -
                    (incident_pressure * 0.3) -
                    np.random.normal(0, 0.018),
                    0.82,
                    1.00
                ),
                3
            )

            customer_satisfaction = round(
                np.clip(
                    4.55 -
                    (closing_backlog * 0.035) -
                    (incident_pressure * 2) +
                    np.random.normal(0, 0.18),
                    2.5,
                    5.0
                ),
                1
            )

            # Completion rate
            completion_rate = round(
                requests_completed /
                max(total_workload, 1),
                3
            )

            operations_rows.append([
                f"OPS-{record_id}",
                date.date(),
                region,
                team,
                opening_backlog,
                requests_received,
                total_workload,
                requests_completed,
                closing_backlog,
                incident_count,
                high_incidents,
                average_completion_days,
                sla_compliance,
                quality_pass_rate,
                customer_satisfaction,
                utilisation,
                completion_rate
            ])

            record_id += 1

            backlog_tracker[previous_key] = closing_backlog

operations = pd.DataFrame(
    operations_rows,
    columns=[
        "Record_ID",
        "Date",
        "Region",
        "Team",
        "Opening_Backlog",
        "Requests_Received",
        "Total_Workload",
        "Requests_Completed",
        "Closing_Backlog",
        "Incident_Count",
        "High_Critical_Incidents",
        "Average_Completion_Days",
        "SLA_Compliance",
        "Quality_Pass_Rate",
        "Customer_Satisfaction",
        "Staff_Utilisation",
        "Completion_Rate"
    ]
)

# ============================================================
# 4. KPI TARGETS
# ============================================================

targets = pd.DataFrame([
    [
        "Completion Rate",
        "Completion_Rate",
        0.95,
        "Minimum 95% of available workload completed"
    ],
    [
        "SLA Compliance",
        "SLA_Compliance",
        0.92,
        "Target percentage completed within SLA"
    ],
    [
        "Quality Pass Rate",
        "Quality_Pass_Rate",
        0.95,
        "Target percentage passing quality checks"
    ],
    [
        "Customer Satisfaction",
        "Customer_Satisfaction",
        4.20,
        "Target average customer satisfaction score"
    ],
    [
        "Staff Utilisation",
        "Staff_Utilisation",
        0.75,
        "Target productive utilisation"
    ],
    [
        "Average Completion Days",
        "Average_Completion_Days",
        3.00,
        "Maximum preferred average completion time"
    ],
    [
        "Closing Backlog",
        "Closing_Backlog",
        10,
        "Preferred maximum daily closing backlog"
    ]
], columns=[
    "KPI_Name",
    "Source_Field",
    "Target_Value",
    "Target_Description"
])

# ============================================================
# 5. REGIONAL REFERENCE DATA
# ============================================================

region_reference = pd.DataFrame([
    [
        region,
        region_info[region]["area"],
        region_info[region]["office"],
        region_info[region]["lead"]
    ]
    for region in regions
], columns=[
    "Region",
    "Area",
    "Primary_Office",
    "Regional_Lead"
])

# ============================================================
# 6. ACTION / LESSONS LOG
# ============================================================

action_types = [
    "Process improvement",
    "Training",
    "Documentation",
    "Supplier management",
    "System improvement",
    "Resource review"
]

action_statuses = [
    "Not Started",
    "In Progress",
    "Complete",
    "Overdue"
]

action_rows = []

for i in range(1, 151):

    incident = incidents.sample(1).iloc[0]

    action_rows.append([
        f"ACT-{i:04d}",
        incident["Incident_ID"],
        incident["Date"],
        incident["Region"],
        incident["Team"],
        np.random.choice(action_types),
        np.random.choice(action_statuses),
        np.random.choice([
            "Review process",
            "Update guidance",
            "Deliver refresher training",
            "Review supplier SLA",
            "Investigate system issue",
            "Assess staffing requirement"
        ])
    ])

actions = pd.DataFrame(
    action_rows,
    columns=[
        "Action_ID",
        "Incident_ID",
        "Date_Raised",
        "Region",
        "Team",
        "Action_Type",
        "Status",
        "Action_Description"
    ]
)

# ============================================================
# 7. INTENTIONAL DATA QUALITY PROBLEMS
# ============================================================

# Operational data
operations.loc[15, "Region"] = " Scotland "
operations.loc[120, "Team"] = "Facilities  Response"
operations.loc[350, "Customer_Satisfaction"] = np.nan
operations.loc[620, "SLA_Compliance"] = np.nan
operations.loc[900, "Team"] = "Workplace services"
operations.loc[1100, "Region"] = "North  West"

# Incident data
incidents.loc[8, "Severity"] = " high "
incidents.loc[27, "Region"] = "North  West"
incidents.loc[102, "Status"] = "In progress"
incidents.loc[205, "Incident_Type"] = "System  outage"
incidents.loc[300, "Status"] = np.nan

# Staffing data
staffing.loc[10, "Region"] = "Scotland "
staffing.loc[45, "Team"] = "Facilities  Response"
staffing.loc[80, "Headcount"] = np.nan

# Actions
actions.loc[12, "Status"] = " complete "
actions.loc[55, "Region"] = "South  East"
actions.loc[91, "Action_Type"] = np.nan

# ============================================================
# 8. SAVE CSV FILES
# ============================================================

files = {
    "01_operations_data.csv": operations,
    "02_kpi_targets.csv": targets,
    "03_staffing_capacity.csv": staffing,
    "04_incident_log.csv": incidents,
    "05_region_reference.csv": region_reference,
    "06_action_tracker.csv": actions
}

for filename, dataframe in files.items():

    dataframe.to_csv(
        OUT / filename,
        index=False
    )

# ============================================================
# 9. README
# ============================================================

readme = """
OPERATIONAL PROJECT — SYNTHETIC DATA GENERATOR
==============================================

Scenario
--------
You are supporting an Operational Excellence team responsible
for monitoring operational performance across multiple regions.

The dataset contains operational performance, staffing,
incidents, actions and regional reference information.

Files
-----

01_operations_data.csv
    Daily operational performance.

    Important relationships:
        Opening Backlog
        + Requests Received
        = Total Workload

        Total Workload
        - Requests Completed
        = Closing Backlog


02_kpi_targets.csv
    KPI definitions and target values.


03_staffing_capacity.csv
    Monthly staffing and capacity information.


04_incident_log.csv
    Operational incidents and their impact.


05_region_reference.csv
    Regional lookup/reference table.


06_action_tracker.csv
    Actions resulting from incidents and improvement activity.


Recommended Excel Tasks
-----------------------

DATA CLEANING
- Remove leading/trailing spaces.
- Standardise region names.
- Standardise team names.
- Standardise status/severity values.
- Deal with missing values.
- Check for duplicates.
- Validate numeric fields.


LOOKUPS
- XLOOKUP
- XMATCH
- INDEX/MATCH


LOGIC
- IF
- IFS
- SWITCH
- CHOOSE


AGGREGATION
- SUMIFS
- COUNTIFS
- AVERAGEIFS


DYNAMIC ARRAYS
- FILTER
- SORT
- SORTBY
- UNIQUE
- SEQUENCE


ADVANCED ANALYSIS
- LARGE
- SMALL
- RANK
- MEDIAN
- MODE
- AGGREGATE


PIVOTTABLES
Analyse:
- Region
- Team
- Month
- Incident type
- Incident severity
- Action status


DASHBOARD
Recommended KPIs:

- Completion Rate
- SLA Compliance
- Quality Pass Rate
- Customer Satisfaction
- Staff Utilisation
- Average Completion Days
- Closing Backlog
- Open Incidents
- High/Critical Incidents
- Overdue Actions


MANAGEMENT QUESTIONS
--------------------

1. Which regions are performing best?

2. Which regions have the largest backlog?

3. Is backlog increasing or decreasing?

4. Does higher staffing utilisation correspond with
   better or worse performance?

5. Which teams have the highest SLA failure rate?

6. Which incident types cause the greatest disruption?

7. Are high-severity incidents associated with poorer
   operational performance?

8. Which regions have the highest customer satisfaction?

9. Which actions are overdue?

10. Which KPIs are consistently below target?

11. Are there regions where apparently good SLA performance
    hides a growing backlog?

12. What three recommendations should be presented to
    senior management?


PORTFOLIO OUTPUT
----------------

The final Excel workbook should ideally contain:

1. Raw Data
2. Cleaned Data
3. Reference Tables
4. Calculations
5. KPI Analysis
6. PivotTables
7. Dashboard
8. Management Findings
9. Recommendations

The objective is not merely to demonstrate Excel formulas.

The objective is to demonstrate the ability to take messy
operational information, establish reliable metrics, identify
performance issues and communicate actionable insight.
"""

(OUT / "README.txt").write_text(
    readme,
    encoding="utf-8"
)

# ============================================================
# 10. SUMMARY
# ============================================================

print("=" * 40)
print("OPERATIONAL PROJECT DATASET CREATED")
print("=" * 40)

for filename, dataframe in files.items():
    print(
        f"{filename:<35} "
        f"{len(dataframe):>6,} rows × "
        f"{len(dataframe.columns):>2} columns"
    )

print()
print(f"Output folder: {OUT.resolve()}")