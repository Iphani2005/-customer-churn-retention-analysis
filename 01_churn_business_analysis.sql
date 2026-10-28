-- Customer Churn and Revenue Retention Analysis
-- SQL Business Analysis Layer
-- Dataset: Cleaned Telco Customer Churn dataset
-- Purpose: Analyse churn patterns, revenue at risk and retention priorities

------------------------------------------------------------
-- 1. Overall Customer and Churn Summary
------------------------------------------------------------

SELECT
    COUNT(DISTINCT customerID) AS TotalCustomers,
    SUM(ChurnFlag) AS ChurnedCustomers,
    COUNT(DISTINCT customerID) - SUM(ChurnFlag) AS ActiveCustomers,
    CAST(SUM(ChurnFlag) AS FLOAT) / COUNT(DISTINCT customerID) AS ChurnRate
FROM telco_customer_churn_cleaned;


------------------------------------------------------------
-- 2. Overall Revenue at Risk
------------------------------------------------------------

SELECT
    SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges ELSE 0 END) AS MonthlyRevenueAtRisk,
    SUM(CASE WHEN ChurnFlag = 1 THEN EstimatedAnnualRevenue ELSE 0 END) AS EstimatedAnnualRevenueAtRisk,
    AVG(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges END) AS AverageMonthlyValueOfChurnedCustomers
FROM telco_customer_churn_cleaned;


------------------------------------------------------------
-- 3. Churn by Contract Type
------------------------------------------------------------

SELECT
    Contract,
    COUNT(DISTINCT customerID) AS Customers,
    SUM(ChurnFlag) AS ChurnedCustomers,
    CAST(SUM(ChurnFlag) AS FLOAT) / COUNT(DISTINCT customerID) AS ChurnRate,
    SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges ELSE 0 END) AS MonthlyRevenueAtRisk,
    SUM(CASE WHEN ChurnFlag = 1 THEN EstimatedAnnualRevenue ELSE 0 END) AS EstimatedAnnualRevenueAtRisk
FROM telco_customer_churn_cleaned
GROUP BY Contract
ORDER BY ChurnRate DESC;


------------------------------------------------------------
-- 4. Churn by Tenure Group
------------------------------------------------------------

SELECT
    TenureGroup,
    COUNT(DISTINCT customerID) AS Customers,
    SUM(ChurnFlag) AS ChurnedCustomers,
    CAST(SUM(ChurnFlag) AS FLOAT) / COUNT(DISTINCT customerID) AS ChurnRate,
    SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges ELSE 0 END) AS MonthlyRevenueAtRisk,
    SUM(CASE WHEN ChurnFlag = 1 THEN EstimatedAnnualRevenue ELSE 0 END) AS EstimatedAnnualRevenueAtRisk
FROM telco_customer_churn_cleaned
GROUP BY TenureGroup
ORDER BY
    CASE
        WHEN TenureGroup = 'New Customer' THEN 1
        WHEN TenureGroup = '0-12 Months' THEN 2
        WHEN TenureGroup = '13-24 Months' THEN 3
        WHEN TenureGroup = '25-48 Months' THEN 4
        WHEN TenureGroup = '49+ Months' THEN 5
        ELSE 6
    END;


------------------------------------------------------------
-- 5. Churn by Payment Method
------------------------------------------------------------

SELECT
    PaymentMethod,
    COUNT(DISTINCT customerID) AS Customers,
    SUM(ChurnFlag) AS ChurnedCustomers,
    CAST(SUM(ChurnFlag) AS FLOAT) / COUNT(DISTINCT customerID) AS ChurnRate,
    SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges ELSE 0 END) AS MonthlyRevenueAtRisk,
    SUM(CASE WHEN ChurnFlag = 1 THEN EstimatedAnnualRevenue ELSE 0 END) AS EstimatedAnnualRevenueAtRisk
FROM telco_customer_churn_cleaned
GROUP BY PaymentMethod
ORDER BY ChurnRate DESC;


------------------------------------------------------------
-- 6. Churn by Internet Service
------------------------------------------------------------

SELECT
    InternetService,
    COUNT(DISTINCT customerID) AS Customers,
    SUM(ChurnFlag) AS ChurnedCustomers,
    CAST(SUM(ChurnFlag) AS FLOAT) / COUNT(DISTINCT customerID) AS ChurnRate,
    SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges ELSE 0 END) AS MonthlyRevenueAtRisk,
    SUM(CASE WHEN ChurnFlag = 1 THEN EstimatedAnnualRevenue ELSE 0 END) AS EstimatedAnnualRevenueAtRisk
FROM telco_customer_churn_cleaned
GROUP BY InternetService
ORDER BY ChurnRate DESC;


------------------------------------------------------------
-- 7. Churn by Monthly Charge Band
------------------------------------------------------------

SELECT
    MonthlyChargeBand,
    COUNT(DISTINCT customerID) AS Customers,
    SUM(ChurnFlag) AS ChurnedCustomers,
    CAST(SUM(ChurnFlag) AS FLOAT) / COUNT(DISTINCT customerID) AS ChurnRate,
    SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges ELSE 0 END) AS MonthlyRevenueAtRisk,
    SUM(CASE WHEN ChurnFlag = 1 THEN EstimatedAnnualRevenue ELSE 0 END) AS EstimatedAnnualRevenueAtRisk
FROM telco_customer_churn_cleaned
GROUP BY MonthlyChargeBand
ORDER BY
    CASE
        WHEN MonthlyChargeBand = 'Low Value' THEN 1
        WHEN MonthlyChargeBand = 'Mid-Low Value' THEN 2
        WHEN MonthlyChargeBand = 'Mid-High Value' THEN 3
        WHEN MonthlyChargeBand = 'High Value' THEN 4
        ELSE 5
    END;


------------------------------------------------------------
-- 8. Combined High-Risk Segment Analysis
------------------------------------------------------------

SELECT
    Contract,
    TenureGroup,
    InternetService,
    PaymentMethod,
    COUNT(DISTINCT customerID) AS Customers,
    SUM(ChurnFlag) AS ChurnedCustomers,
    CAST(SUM(ChurnFlag) AS FLOAT) / COUNT(DISTINCT customerID) AS ChurnRate,
    SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges ELSE 0 END) AS MonthlyRevenueAtRisk,
    SUM(CASE WHEN ChurnFlag = 1 THEN EstimatedAnnualRevenue ELSE 0 END) AS EstimatedAnnualRevenueAtRisk
FROM telco_customer_churn_cleaned
GROUP BY
    Contract,
    TenureGroup,
    InternetService,
    PaymentMethod
HAVING COUNT(DISTINCT customerID) >= 30
ORDER BY
    ChurnRate DESC,
    EstimatedAnnualRevenueAtRisk DESC;


------------------------------------------------------------
-- 9. Retention Priority Ranking
-- Combines churn rate and annual revenue exposure
------------------------------------------------------------

WITH SegmentSummary AS (
    SELECT
        Contract,
        TenureGroup,
        InternetService,
        PaymentMethod,
        COUNT(DISTINCT customerID) AS Customers,
        SUM(ChurnFlag) AS ChurnedCustomers,
        CAST(SUM(ChurnFlag) AS FLOAT) / COUNT(DISTINCT customerID) AS ChurnRate,
        SUM(CASE WHEN ChurnFlag = 1 THEN EstimatedAnnualRevenue ELSE 0 END) AS EstimatedAnnualRevenueAtRisk
    FROM telco_customer_churn_cleaned
    GROUP BY
        Contract,
        TenureGroup,
        InternetService,
        PaymentMethod
    HAVING COUNT(DISTINCT customerID) >= 30
),

RankedSegments AS (
    SELECT
        *,
        DENSE_RANK() OVER (ORDER BY EstimatedAnnualRevenueAtRisk DESC) AS RevenueRiskRank,
        DENSE_RANK() OVER (ORDER BY ChurnRate DESC) AS ChurnRateRank
    FROM SegmentSummary
)

SELECT
    Contract,
    TenureGroup,
    InternetService,
    PaymentMethod,
    Customers,
    ChurnedCustomers,
    ChurnRate,
    EstimatedAnnualRevenueAtRisk,
    RevenueRiskRank,
    ChurnRateRank,
    RevenueRiskRank + ChurnRateRank AS RetentionPriorityScore
FROM RankedSegments
ORDER BY RetentionPriorityScore ASC;
