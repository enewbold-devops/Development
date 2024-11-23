CREATE PROCEDURE [dbo].[RemoveADPCurrentPayperiodHours]
    @StartDate DATE,
    @EndDate DATE
AS
BEGIN

    -- Ensure proper error handling
	SET NOCOUNT ON

    BEGIN TRY
        BEGIN TRANSACTION

        -- Delete records between the provided dates
        DELETE FROM dbo.ADPHoursArchive
        WHERE Cast([Date] as date) >= @StartDate AND Cast([Date] as date) <= @EndDate;

        -- Commit the transaction if everything is successful
        COMMIT TRANSACTION
    END TRY
    BEGIN CATCH
        -- Rollback the transaction if there is an error
        ROLLBACK TRANSACTION;

        -- Raise the error to the caller
        THROW;
    END CATCH
END;