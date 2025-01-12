/****** Object:  View [dbo].[vw_jts_PayrollSchedule]    Script Date: 9/23/2024 1:41:39 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE View [dbo].[vw_jts_PayrollSchedule] as
SELECT 
	[recordID] as [PayPeriodID]
	,cast(DATEADD(day, -14, [Period End]) as nvarchar) + '_' + cast([Period End] as nvarchar) as [PayPeriod]
      ,[Week]
      ,[In Date]
      ,[Out Date]
      ,[Pay Date]
	  ,DATEADD(day, -14, [Period End]) as [Period Start]
      ,[Period End]
      ,[Year]
      ,[Quarter]
  FROM [dbo].[ADPPayrollSchedule]
GO
