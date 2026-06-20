-- ================================================
-- LOCAL FOOD WASTAGE MANAGEMENT SYSTEM
-- Master SQL File
-- Author: Soham
-- Database: SQLite
-- ================================================


-- ================================================
-- SECTION 1: CREATE TABLES (SCHEMA)
-- ================================================

DROP TABLE IF EXISTS claims;
DROP TABLE IF EXISTS food_listings;
DROP TABLE IF EXISTS receivers;
DROP TABLE IF EXISTS providers;

-- Table 1: Providers
CREATE TABLE providers (
    Provider_ID INTEGER PRIMARY KEY,
    Name        TEXT,
    Type        TEXT,
    Address     TEXT,
    City        TEXT,
    Contact     TEXT
);

-- Table 2: Receivers
CREATE TABLE receivers (
    Receiver_ID INTEGER PRIMARY KEY,
    Name        TEXT,
    Type        TEXT,
    City        TEXT,
    Contact     TEXT
);

-- Table 3: Food Listings
-- References providers via Provider_ID (Foreign Key)
CREATE TABLE food_listings (
    Food_ID       INTEGER PRIMARY KEY,
    Food_Name     TEXT,
    Quantity      INTEGER,
    Expiry_Date   TEXT,
    Provider_ID   INTEGER,
    Provider_Type TEXT,
    Location      TEXT,
    Food_Type     TEXT,
    Meal_Type     TEXT,
    FOREIGN KEY (Provider_ID) REFERENCES providers(Provider_ID)
);

-- Table 4: Claims
-- References both food_listings and receivers (Foreign Keys)
CREATE TABLE claims (
    Claim_ID    INTEGER PRIMARY KEY,
    Food_ID     INTEGER,
    Receiver_ID INTEGER,
    Status      TEXT,
    Timestamp   TEXT,
    FOREIGN KEY (Food_ID) REFERENCES food_listings(Food_ID),
    FOREIGN KEY (Receiver_ID) REFERENCES receivers(Receiver_ID)
);


-- ================================================
-- SECTION 2: SAMPLE INSERT STATEMENTS
-- ================================================

-- Sample Provider
INSERT INTO providers (Provider_ID, Name, Type, Address, City, Contact)
VALUES (1, 'Green Bites Restaurant', 'Restaurant', '12 MG Road', 'Mumbai', '9876543210');

-- Sample Receiver
INSERT INTO receivers (Receiver_ID, Name, Type, City, Contact)
VALUES (1, 'Hope NGO', 'NGO', 'Mumbai', '9123456780');

-- Sample Food Listing
INSERT INTO food_listings (Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
VALUES (1, 'Rice and Dal', 50, '2025-12-31', 1, 'Restaurant', 'Mumbai', 'Vegetarian', 'Lunch');

-- Sample Claim
INSERT INTO claims (Claim_ID, Food_ID, Receiver_ID, Status, Timestamp)
VALUES (1, 1, 1, 'Completed', '2025-12-01 10:00:00');


-- ================================================
-- SECTION 3: CRUD OPERATIONS
-- ================================================

-- CREATE: Add a new food listing
INSERT INTO food_listings (Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
VALUES (2, 'Bread and Butter', 30, '2025-12-15', 1, 'Restaurant', 'Delhi', 'Vegetarian', 'Breakfast');

-- READ: View all food listings
SELECT * FROM food_listings;

-- UPDATE: Update quantity of a food listing
UPDATE food_listings
SET Quantity = 40
WHERE Food_ID = 2;

-- DELETE: Remove a food listing
DELETE FROM food_listings
WHERE Food_ID = 2;


-- ================================================
-- SECTION 4: 15 SQL ANALYSIS QUERIES
-- ================================================

-- Query 1: How many providers and receivers are there in each city?
-- Uses UNION ALL to combine providers and receivers, then groups by city
SELECT City,
       SUM(is_provider) AS Total_Providers,
       SUM(is_receiver) AS Total_Receivers
FROM (
    SELECT City, 1 AS is_provider, 0 AS is_receiver FROM providers
    UNION ALL
    SELECT City, 0, 1 FROM receivers
)
GROUP BY City
ORDER BY City;

-- Query 2: Which provider type contributes the most food?
-- Uses SUM with GROUP BY to find total quantity per provider type
SELECT Provider_Type, SUM(Quantity) AS Total_Quantity
FROM food_listings
GROUP BY Provider_Type
ORDER BY Total_Quantity DESC;

-- Query 3: Which receivers have claimed the most food?
-- Uses JOIN between claims and receivers, COUNT to find total claims
SELECT r.Name, COUNT(c.Claim_ID) AS Total_Claims
FROM claims c
JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
GROUP BY r.Receiver_ID, r.Name
ORDER BY Total_Claims DESC;

-- Query 4: What is the total quantity of food available?
-- Uses SUM aggregate function
SELECT SUM(Quantity) AS Total_Available_Quantity
FROM food_listings;

-- Query 5: Which city has the highest number of food listings?
-- Uses COUNT with GROUP BY on Location
SELECT Location, COUNT(*) AS Total_Listings
FROM food_listings
GROUP BY Location
ORDER BY Total_Listings DESC;

-- Query 6: What are the most commonly available food types?
-- Uses COUNT with GROUP BY on Food_Type
SELECT Food_Type, COUNT(*) AS Count
FROM food_listings
GROUP BY Food_Type
ORDER BY Count DESC;

-- Query 7: How many claims have been made per food item?
-- Uses JOIN between claims and food_listings
SELECT f.Food_Name, COUNT(c.Claim_ID) AS Total_Claims
FROM claims c
JOIN food_listings f ON c.Food_ID = f.Food_ID
GROUP BY f.Food_ID, f.Food_Name
ORDER BY Total_Claims DESC;

-- Query 8: Which provider has had the most successful claims?
-- Uses multiple JOINs across claims, food_listings and providers
-- Filters only Completed claims using WHERE
SELECT p.Name, COUNT(c.Claim_ID) AS Successful_Claims
FROM claims c
JOIN food_listings f ON c.Food_ID = f.Food_ID
JOIN providers p ON f.Provider_ID = p.Provider_ID
WHERE c.Status = 'Completed'
GROUP BY p.Provider_ID, p.Name
ORDER BY Successful_Claims DESC;

-- Query 9: What percentage of claims are completed vs pending vs cancelled?
-- Uses subquery to calculate total claims for percentage
SELECT Status,
       COUNT(*) AS Count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS Percentage
FROM claims
GROUP BY Status;

-- Query 10: What is the average quantity of food claimed per receiver?
-- Uses AVG aggregate with JOIN across 3 tables
SELECT r.Name, ROUND(AVG(f.Quantity), 2) AS Avg_Quantity_Claimed
FROM claims c
JOIN food_listings f ON c.Food_ID = f.Food_ID
JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
GROUP BY r.Receiver_ID, r.Name
ORDER BY Avg_Quantity_Claimed DESC;

-- Query 11: Which meal type is claimed the most?
-- Uses JOIN between claims and food_listings, groups by Meal_Type
SELECT f.Meal_Type, COUNT(c.Claim_ID) AS Total_Claims
FROM claims c
JOIN food_listings f ON c.Food_ID = f.Food_ID
GROUP BY f.Meal_Type
ORDER BY Total_Claims DESC;

-- Query 12: Total quantity of food donated by each provider
-- Uses SUM with JOIN between food_listings and providers
SELECT p.Name, SUM(f.Quantity) AS Total_Donated
FROM food_listings f
JOIN providers p ON f.Provider_ID = p.Provider_ID
GROUP BY p.Provider_ID, p.Name
ORDER BY Total_Donated DESC;

-- Query 13: Food items expiring within the next 7 days
-- Uses DATE functions to filter by expiry date range
SELECT Food_Name, Quantity, Expiry_Date, Location
FROM food_listings
WHERE DATE(Expiry_Date) BETWEEN DATE('now') AND DATE('now', '+7 days')
ORDER BY Expiry_Date;

-- Query 14: Top providers by number of listings
-- Uses COUNT with JOIN between food_listings and providers
SELECT p.Name, COUNT(f.Food_ID) AS Number_of_Listings
FROM food_listings f
JOIN providers p ON f.Provider_ID = p.Provider_ID
GROUP BY p.Provider_ID, p.Name
ORDER BY Number_of_Listings DESC;

-- Query 15: Receivers and their city distribution
-- Uses COUNT with GROUP BY on City
SELECT City, COUNT(*) AS Total_Receivers
FROM receivers
GROUP BY City
ORDER BY Total_Receivers DESC;


-- ================================================
-- SECTION 5: ADDITIONAL USEFUL QUERIES
-- ================================================

-- Contact info of providers in a specific city
SELECT Name, Type, Address, Contact
FROM providers
WHERE City = 'Mumbai';

-- Food listings filtered by food type
SELECT Food_Name, Quantity, Expiry_Date, Location
FROM food_listings
WHERE Food_Type = 'Vegetarian'
ORDER BY Expiry_Date;

-- All pending claims with food and receiver details
SELECT c.Claim_ID, f.Food_Name, r.Name AS Receiver, c.Status, c.Timestamp
FROM claims c
JOIN food_listings f ON c.Food_ID = f.Food_ID
JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
WHERE c.Status = 'Pending'
ORDER BY c.Timestamp;