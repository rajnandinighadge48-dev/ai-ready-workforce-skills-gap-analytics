
-- ============================================================
-- PROJECT: AI-READY WORKFORCE & SKILLS GAP ANALYTICS
-- Database: ai_workforce_analytics
-- Confirmed table: ai_workforce
-- Dataset: 21 columns
-- MySQL Workbench
-- ============================================================

USE `ai_workforce_analytics`;


-- QUERY 1: Verify table and record count
SELECT COUNT(*) AS Total_Records
FROM `ai_workforce`;


-- QUERY 2: Preview dataset
SELECT *
FROM `ai_workforce`
LIMIT 10;


-- QUERY 3: Data quality overview
SELECT
    COUNT(*) AS Total_Rows,
    COUNT(DISTINCT `ï»¿Employee_ID`) AS Unique_Employee_IDs,
    SUM(`ï»¿Employee_ID` IS NULL OR TRIM(`ï»¿Employee_ID`) = '') AS Missing_Employee_IDs,
    SUM(`Department` IS NULL OR TRIM(`Department`) = '') AS Missing_Departments,
    SUM(`Job_Role` IS NULL OR TRIM(`Job_Role`) = '') AS Missing_Job_Roles,
    SUM(`AI_Readiness_Score_10` IS NULL) AS Missing_AI_Readiness_Scores
FROM `ai_workforce`;


-- QUERY 4: Find duplicate employee IDs
SELECT
    `ï»¿Employee_ID`,
    COUNT(*) AS Duplicate_Count
FROM `ai_workforce`
GROUP BY `ï»¿Employee_ID`
HAVING COUNT(*) > 1
ORDER BY Duplicate_Count DESC;


-- QUERY 5: Overall workforce KPIs
SELECT
    COUNT(*) AS Total_Employees,
    ROUND(AVG(`Age`), 2) AS Average_Age,
    ROUND(AVG(`Experience_ Years`), 2) AS Average_Experience_Years,
    ROUND(AVG(`Performance_Rating_10`), 2) AS Average_Performance,
    ROUND(AVG(`Job_Satisfaction_10`), 2) AS Average_Job_Satisfaction,
    ROUND(AVG(`Productivity_Score_10`), 2) AS Average_Productivity,
    ROUND(AVG(`Engagement_Score_10`), 2) AS Average_Engagement,
    ROUND(AVG(`AI_Readiness_Score_10`), 2) AS Average_AI_Readiness
FROM `ai_workforce`;


-- QUERY 6: Department-wise workforce analysis
SELECT
    `Department`,
    COUNT(*) AS Employee_Count,
    ROUND(AVG(`AI_Readiness_Score_10`), 2) AS Average_AI_Readiness,
    ROUND(AVG(`Technical_Skills_Score_10`), 2) AS Average_Technical_Skills,
    ROUND(AVG(`AI_Tools_Score_10`), 2) AS Average_AI_Tools,
    ROUND(AVG(`Performance_Rating_10`), 2) AS Average_Performance,
    ROUND(AVG(`Training_Hours`), 2) AS Average_Training_Hours
FROM `ai_workforce`
GROUP BY `Department`
ORDER BY Average_AI_Readiness DESC;


-- QUERY 7: Skills gap distribution
SELECT
    `Skill_Gap_Level`,
    COUNT(*) AS Employee_Count,
    ROUND(
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM `ai_workforce`),
        2
    ) AS Workforce_Percentage
FROM `ai_workforce`
GROUP BY `Skill_Gap_Level`
ORDER BY Employee_Count DESC;


-- QUERY 8: High-priority skills gap employees
SELECT
    `ï»¿Employee_ID`,
    `Department`,
    `Job_Role`,
    `AI_Tools_Score_10`,
    `Technical_Skills_Score_10`,
    `Learning_Agility_10`,
    `AI_Readiness_Score_10`,
    `Skill_Gap_Level`
FROM `ai_workforce`
WHERE LOWER(TRIM(`Skill_Gap_Level`)) = 'high'
ORDER BY
    `AI_Readiness_Score_10` ASC,
    `Technical_Skills_Score_10` ASC;


-- QUERY 9: Department-wise high skills gap percentage
SELECT
    `Department`,
    COUNT(*) AS Total_Employees,
    SUM(
        CASE
            WHEN LOWER(TRIM(`Skill_Gap_Level`)) = 'high'
            THEN 1 ELSE 0
        END
    ) AS High_Skill_Gap_Employees,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN LOWER(TRIM(`Skill_Gap_Level`)) = 'high'
                THEN 1 ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS High_Skill_Gap_Percentage,
    ROUND(AVG(`AI_Readiness_Score_10`), 2) AS Average_AI_Readiness
FROM `ai_workforce`
GROUP BY `Department`
ORDER BY High_Skill_Gap_Percentage DESC;


-- QUERY 10: AI readiness categories
SELECT
    CASE
        WHEN `AI_Readiness_Score_10` >= 8 THEN 'High Readiness'
        WHEN `AI_Readiness_Score_10` >= 5 THEN 'Moderate Readiness'
        ELSE 'Low Readiness'
    END AS Readiness_Category,
    COUNT(*) AS Employee_Count,
    ROUND(AVG(`AI_Readiness_Score_10`), 2) AS Average_Readiness
FROM `ai_workforce`
WHERE `AI_Readiness_Score_10` IS NOT NULL
GROUP BY Readiness_Category
ORDER BY Average_Readiness DESC;


-- QUERY 11: Training hours and AI readiness
SELECT
    CASE
        WHEN `Training_Hours` < 5 THEN 'Low Training: Under 5 Hours'
        WHEN `Training_Hours` < 10 THEN 'Medium Training: 5-9 Hours'
        ELSE 'High Training: 10+ Hours'
    END AS Training_Category,
    COUNT(*) AS Employee_Count,
    ROUND(AVG(`AI_Readiness_Score_10`), 2) AS Average_AI_Readiness,
    ROUND(AVG(`Technical_Skills_Score_10`), 2) AS Average_Technical_Skills,
    ROUND(AVG(`AI_Tools_Score_10`), 2) AS Average_AI_Tools
FROM `ai_workforce`
GROUP BY Training_Category
ORDER BY Average_AI_Readiness DESC;


-- QUERY 12: Future role interest analysis
SELECT
    `Future_Role_Interest`,
    COUNT(*) AS Interested_Employees,
    ROUND(AVG(`AI_Readiness_Score_10`), 2) AS Average_AI_Readiness,
    ROUND(AVG(`Technical_Skills_Score_10`), 2) AS Average_Technical_Skills
FROM `ai_workforce`
GROUP BY `Future_Role_Interest`
ORDER BY Interested_Employees DESC;


-- QUERY 13: Department and skills gap matrix
SELECT
    `Department`,
    `Skill_Gap_Level`,
    COUNT(*) AS Employee_Count,
    ROUND(AVG(`AI_Readiness_Score_10`), 2) AS Average_AI_Readiness
FROM `ai_workforce`
GROUP BY `Department`, `Skill_Gap_Level`
ORDER BY `Department`, Employee_Count DESC;


-- QUERY 14: Monthly salary analysis
-- Handles ₹ symbol, commas and spaces in text salary values
SELECT
    `Department`,
    COUNT(*) AS Employee_Count,
    ROUND(
        AVG(
            CAST(
                NULLIF(
                    REPLACE(
                        REPLACE(
                            REPLACE(TRIM(`Monthly_Salary`), '₹', ''),
                            ',', ''
                        ),
                        ' ', ''
                    ),
                    ''
                ) AS DECIMAL(12,2)
            )
        ),
        2
    ) AS Average_Monthly_Salary,
    ROUND(AVG(`AI_Readiness_Score_10`), 2) AS Average_AI_Readiness
FROM `ai_workforce`
GROUP BY `Department`
ORDER BY Average_Monthly_Salary DESC;


-- QUERY 15: Rank departments by AI readiness
SELECT
    `Department`,
    COUNT(*) AS Employee_Count,
    ROUND(AVG(`AI_Readiness_Score_10`), 2) AS Average_AI_Readiness,
    DENSE_RANK() OVER (
        ORDER BY AVG(`AI_Readiness_Score_10`) DESC
    ) AS Readiness_Rank
FROM `ai_workforce`
GROUP BY `Department`
ORDER BY Readiness_Rank;


-- QUERY 16: Employee-level training recommendations
SELECT
    `ï»¿Employee_ID`,
    `Department`,
    `Job_Role`,
    `Skill_Gap_Level`,
    `AI_Readiness_Score_10`,
    `Technical_Skills_Score_10`,
    `AI_Tools_Score_10`,
    `Learning_Agility_10`,
    CASE
        WHEN LOWER(TRIM(`Skill_Gap_Level`)) = 'high'
             AND `Learning_Agility_10` >= 7
            THEN 'Priority 1 - Targeted AI Training'
        WHEN LOWER(TRIM(`Skill_Gap_Level`)) = 'high'
            THEN 'Priority 2 - Foundational Skills Training'
        WHEN LOWER(TRIM(`Skill_Gap_Level`)) = 'medium'
            THEN 'Priority 3 - Skills Development'
        WHEN LOWER(TRIM(`Skill_Gap_Level`)) = 'low'
            THEN 'Maintain and Advance Skills'
        ELSE 'Review Skill Gap Classification'
    END AS Recommended_Action
FROM `ai_workforce`
ORDER BY
    CASE
        WHEN LOWER(TRIM(`Skill_Gap_Level`)) = 'high' THEN 1
        WHEN LOWER(TRIM(`Skill_Gap_Level`)) = 'medium' THEN 2
        WHEN LOWER(TRIM(`Skill_Gap_Level`)) = 'low' THEN 3
        ELSE 4
    END,
    `AI_Readiness_Score_10` ASC;


-- QUERY 17: Performance and engagement by department
SELECT
    `Department`,
    COUNT(*) AS Employee_Count,
    ROUND(AVG(`Performance_Rating_10`), 2) AS Average_Performance,
    ROUND(AVG(`Productivity_Score_10`), 2) AS Average_Productivity,
    ROUND(AVG(`Goal_Achievement_10`), 2) AS Average_Goal_Achievement,
    ROUND(AVG(`Engagement_Score_10`), 2) AS Average_Engagement,
    ROUND(AVG(`Job_Satisfaction_10`), 2) AS Average_Job_Satisfaction
FROM `ai_workforce`
GROUP BY `Department`
ORDER BY Average_Performance DESC;


-- QUERY 18: Compare AI tools and technical skills
SELECT
    `Department`,
    ROUND(AVG(`AI_Tools_Score_10`), 2) AS Average_AI_Tools_Score,
    ROUND(AVG(`Technical_Skills_Score_10`), 2) AS Average_Technical_Skills,
    ROUND(
        AVG(`AI_Tools_Score_10`) -
        AVG(`Technical_Skills_Score_10`),
        2
    ) AS AI_Tools_Skill_Difference,
    ROUND(AVG(`AI_Readiness_Score_10`), 2) AS Average_AI_Readiness
FROM `ai_workforce`
GROUP BY `Department`
ORDER BY Average_AI_Readiness DESC;
