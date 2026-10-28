-- Customer Churn and Revenue Retention Analysis
-- Database and Table Setup Script

CREATE DATABASE CustomerChurnRetentionAnalysis;
GO

USE CustomerChurnRetentionAnalysis;
GO

CREATE TABLE telco_customer_churn_cleaned (
    customerID VARCHAR(20) PRIMARY KEY,
    gender VARCHAR(10),
    SeniorCitizen INT,
    Partner VARCHAR(5),
    Dependents VARCHAR(5),
    tenure INT,
    PhoneService VARCHAR(5),
    MultipleLines VARCHAR(20),
    InternetService VARCHAR(20),
    OnlineSecurity VARCHAR(25),
    OnlineBackup VARCHAR(25),
    DeviceProtection VARCHAR(25),
    TechSupport VARCHAR(25),
    StreamingTV VARCHAR(25),
    StreamingMovies VARCHAR(25),
    Contract VARCHAR(20),
    PaperlessBilling VARCHAR(5),
    PaymentMethod VARCHAR(50),
    MonthlyCharges DECIMAL(10,2),
    TotalCharges DECIMAL(10,2),
    Churn VARCHAR(5),
    ChurnFlag INT,
    SeniorCitizenLabel VARCHAR(20),
    EstimatedAnnualRevenue DECIMAL(10,2),
    AverageMonthlyValue DECIMAL(10,2),
    TenureGroup VARCHAR(20),
    MonthlyChargeBand VARCHAR(20)
);
GO