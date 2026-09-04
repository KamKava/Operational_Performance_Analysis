
OPERATIONAL PROJECT — SYNTHETIC DATA GENERATOR
==============================================

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


Excel Tasks
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


DASHBOARD KPIs:

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

