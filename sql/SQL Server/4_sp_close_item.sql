USE [pepper];
GO

CREATE PROCEDURE sp_close_item
    @item_id UNIQUEIDENTIFIER
AS
BEGIN
    UPDATE items
    SET closed = 1
    WHERE item_id = @item_id;
END
GO