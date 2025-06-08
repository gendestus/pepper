USE [pepper];
GO

CREATE PROCEDURE sp_add_item
    @item_text NVARCHAR(MAX),
    @user_message NVARCHAR(MAX) = NULL
AS
BEGIN
    INSERT INTO items (item_text, user_message)
    VALUES (@item_text, @user_message);
END
GO