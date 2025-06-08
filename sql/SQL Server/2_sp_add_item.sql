USE [pepper];
GO

CREATE PROCEDURE sp_add_item
    @item_text NVARCHAR(MAX)
AS
BEGIN
    INSERT INTO items (item_text)
    VALUES (@item_text);
END
GO