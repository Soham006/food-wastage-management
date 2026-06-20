DROP TABLE IF EXISTS claims;
DROP TABLE IF EXISTS food_listings;
DROP TABLE IF EXISTS receivers;
DROP TABLE IF EXISTS providers;

CREATE TABLE providers (
    Provider_ID INTEGER PRIMARY KEY,
    Name        TEXT,
    Type        TEXT,
    Address     TEXT,
    City        TEXT,
    Contact     TEXT
);

CREATE TABLE receivers (
    Receiver_ID INTEGER PRIMARY KEY,
    Name        TEXT,
    Type        TEXT,
    City        TEXT,
    Contact     TEXT
);

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

CREATE TABLE claims (
    Claim_ID    INTEGER PRIMARY KEY,
    Food_ID     INTEGER,
    Receiver_ID INTEGER,
    Status      TEXT,
    Timestamp   TEXT,
    FOREIGN KEY (Food_ID) REFERENCES food_listings(Food_ID),
    FOREIGN KEY (Receiver_ID) REFERENCES receivers(Receiver_ID)
);
