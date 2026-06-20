QUERIES = {
    "1. Providers and receivers count per city": "SELECT City, SUM(is_provider) AS Total_Providers, SUM(is_receiver) AS Total_Receivers FROM (SELECT City, 1 AS is_provider, 0 AS is_receiver FROM providers UNION ALL SELECT City, 0, 1 FROM receivers) GROUP BY City ORDER BY City",
    "2. Which provider type contributes the most food": "SELECT Provider_Type, SUM(Quantity) AS Total_Quantity FROM food_listings GROUP BY Provider_Type ORDER BY Total_Quantity DESC",
    "3. Receivers who have claimed the most food": "SELECT r.Name, COUNT(c.Claim_ID) AS Total_Claims FROM claims c JOIN receivers r ON c.Receiver_ID = r.Receiver_ID GROUP BY r.Receiver_ID, r.Name ORDER BY Total_Claims DESC",
    "4. Total quantity of food available": "SELECT SUM(Quantity) AS Total_Available_Quantity FROM food_listings",
    "5. City with the highest number of food listings": "SELECT Location, COUNT(*) AS Total_Listings FROM food_listings GROUP BY Location ORDER BY Total_Listings DESC",
    "6. Most commonly available food types": "SELECT Food_Type, COUNT(*) AS Count FROM food_listings GROUP BY Food_Type ORDER BY Count DESC",
    "7. Number of claims made per food item": "SELECT f.Food_Name, COUNT(c.Claim_ID) AS Total_Claims FROM claims c JOIN food_listings f ON c.Food_ID = f.Food_ID GROUP BY f.Food_ID, f.Food_Name ORDER BY Total_Claims DESC",
    "8. Provider with the most successful claims": "SELECT p.Name, COUNT(c.Claim_ID) AS Successful_Claims FROM claims c JOIN food_listings f ON c.Food_ID = f.Food_ID JOIN providers p ON f.Provider_ID = p.Provider_ID WHERE c.Status = 'Completed' GROUP BY p.Provider_ID, p.Name ORDER BY Successful_Claims DESC",
    "9. Percentage of claims by status": "SELECT Status, COUNT(*) AS Count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS Percentage FROM claims GROUP BY Status",
    "10. Average quantity of food claimed per receiver": "SELECT r.Name, ROUND(AVG(f.Quantity), 2) AS Avg_Quantity_Claimed FROM claims c JOIN food_listings f ON c.Food_ID = f.Food_ID JOIN receivers r ON c.Receiver_ID = r.Receiver_ID GROUP BY r.Receiver_ID, r.Name ORDER BY Avg_Quantity_Claimed DESC",
    "11. Which meal type is claimed the most": "SELECT f.Meal_Type, COUNT(c.Claim_ID) AS Total_Claims FROM claims c JOIN food_listings f ON c.Food_ID = f.Food_ID GROUP BY f.Meal_Type ORDER BY Total_Claims DESC",
    "12. Total quantity of food donated by each provider": "SELECT p.Name, SUM(f.Quantity) AS Total_Donated FROM food_listings f JOIN providers p ON f.Provider_ID = p.Provider_ID GROUP BY p.Provider_ID, p.Name ORDER BY Total_Donated DESC",
    "13. Food items expiring within the next 7 days": "SELECT Food_Name, Quantity, Expiry_Date, Location FROM food_listings WHERE DATE(Expiry_Date) BETWEEN DATE('now') AND DATE('now', '+7 days') ORDER BY Expiry_Date",
    "14. Top providers by number of listings": "SELECT p.Name, COUNT(f.Food_ID) AS Number_of_Listings FROM food_listings f JOIN providers p ON f.Provider_ID = p.Provider_ID GROUP BY p.Provider_ID, p.Name ORDER BY Number_of_Listings DESC",
    "15. Receivers and their city distribution": "SELECT City, COUNT(*) AS Total_Receivers FROM receivers GROUP BY City ORDER BY Total_Receivers DESC",
}

PROVIDER_CONTACTS_BY_CITY = "SELECT Name, Type, Address, Contact FROM providers WHERE City = :city"
