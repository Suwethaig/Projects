-- Verification query with CTE to identify and tag duplicate records
-- The CTE 'DuplicateRecords' uses ROW_NUMBER() to tag duplicates based on JourneyID, CustomerID, and ProductID
-- Records with RowNum > 1 are considered duplicates

WITH DuplicateRecords AS (
    SELECT 
        JourneyID,
        CustomerID,
        ProductID,
        VisitDate,
        Stage,
        Action, 
        Duration,
        ROW_NUMBER() OVER (
            PARTITION BY JourneyID, CustomerID, ProductID
            ORDER BY JourneyID
        ) AS RowNum
    FROM 
        dbo.customer_journey
)
SELECT *
FROM 
    DuplicateRecords
WHERE 
    RowNum > 1
ORDER BY 
    JourneyID;


-- Replace NULL values in Duration to avg duration of the day
-- Create uniform values for Stage
-- Remove duplicate rows

SELECT 
    JourneyID,
    CustomerID,
    ProductID,
    VisitDate,
    Stage,
    Action,
    COALESCE(Duration, avg_duration) AS Duration
FROM (
    SELECT
        JourneyID,
        CustomerID,
        ProductID,
        VisitDate,
        UPPER(Stage) AS Stage,
        Action,
		Duration,
        AVG(Duration) OVER (PARTITION BY VisitDate) AS avg_duration,
        ROW_NUMBER() OVER (
            PARTITION BY JourneyID, CustomerID, ProductID
            ORDER BY JourneyID
        ) AS RowNum
    FROM 
        dbo.customer_journey
) AS subquery
WHERE 
    RowNum = 1;
