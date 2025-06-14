CREATE DATABASE pepper;
GO
USE pepper;

CREATE TABLE items (
    item_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    item_text NVARCHAR(MAX),
    closed BIT DEFAULT 0,
    created DATETIME DEFAULT CURRENT_TIMESTAMP
);