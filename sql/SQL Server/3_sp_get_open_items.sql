USE [pepper];
GO

CREATE PROCEDURE sp_get_open_items
AS
BEGIN
    SELECT item_id, item_text, user_message, created
    FROM items
    WHERE closed = 0
    ORDER BY created DESC;
END
GO