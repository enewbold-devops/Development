/****** Object:  View [dbo].[vw_jts_PayrollHours]    Script Date: 9/23/2024 1:41:39 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO


CREATE View [dbo].[vw_jts_PayrollHours] as
SELECT 
		  a.[Department]
		  ,a.[Client]
		  ,a.[Project]
		  ,a.[Employee] as [ADPEmployee]
		  ,a.[ID_Number]
		  ,d.[DisplayName]
		  ,lower(d.[UserPrincipalName]) as [UserPrincipalName]
		  ,cast(a.[Date] as Date) as [Date]
		  --,cast(c.recordID as nvarchar(255)) as [PayPeriodID]
		  --,c.[Week]
		  --,c.[Year]
		  --,c.[Quarter]
		  --,DATEADD(day, -14, c.[Period End]) as [Period Start]
		  --,c.[Period End]
		  ,SUM(a.[Hours]) AS [Hours]
  FROM [dbo].[ADPHoursArchive] a
  left join [dbo].[ADPPayrollSchedule] c
	ON
		a.[Date] between DATEADD(day, -14, c.[Period End]) and c.[Period End]
  left join [dbo].[JTSADUsers] d
	ON
		a.[ID_Number] = d.ADP_ID_Number

	WHERE
		a.[Date] is not null
		and
		len(Trim(a.[Client])) > 1
			and
		Trim(a.[Client]) <> 'JTS-Corp'
			and
		len(Trim(a.[Project])) > 1
			and
		a.[Hours] is not null

GROUP BY 
	a.[Department]
	,a.[Client]
	,a.[Project]
	,a.[Employee]
	,a.[ID_Number]
	,d.[DisplayName]
	,d.[UserPrincipalName]
	,cast(a.[Date] as Date)
	--,cast(c.recordID as nvarchar(255))
	--,c.[Week]
	--,c.[Year]
	--,c.[Quarter]
	--,DATEADD(day, -14, c.[Period End])
	--,c.[Period End]
		

GO
