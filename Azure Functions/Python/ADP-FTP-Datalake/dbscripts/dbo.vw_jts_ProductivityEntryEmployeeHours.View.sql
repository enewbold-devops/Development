/****** Object:  View [dbo].[vw_jts_ProductivityEntryEmployeeHours]    Script Date: 9/23/2024 1:41:39 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO


CREATE View [dbo].[vw_jts_ProductivityEntryEmployeeHours] AS
SELECT
		c.[Account Id]
		,c.[Account Status]
		,c.[Client]
		,d.[Project Alias] as [Project]
		,c.[Project code] as [ProjectCode]
		,c.[CreatedBy]
		,c.[CreatedOn]
		,c.[Count_Charts]
		,b.[UserPrincipalName]
		,b.[Date] 
		,b.[Hours]

FROM (
	SELECT
		 a.[Account Id]
		,a.[Account Status]
		,a.[Client]
		--,a.[Project]
		,a.[Project code]
		,a.[CreatedBy]
		,a.[CreatedOn]
		,count(a.recordID) as [Count_Charts]
		,Sum(cast(a.[Balance] as money)) as [Balance]
	  FROM [dbo].[HIMAccountTracker] a
	  GROUP BY
		 a.[Account Id]
		,a.[Account Status]
		,a.[Client]
		--,a.[Project]
		,a.[Project code]
		,a.[CreatedOn]
		,a.[CreatedBy] 
) as c
 LEFT JOIN [dbo].[ProjectList] d
	ON
		c.Client = d.Client
		and
		c.[Project code] = d.[Project Code]

 LEFT JOIN [dbo].[vw_jts_PayrollHours] b
	ON
		c.[CreatedBy] = b.[DisplayName]
		and
		c.CreatedOn = b.[Date]
		and
		c.Client = b.Client
		and
		d.[Project Alias] = b.Project
GO
