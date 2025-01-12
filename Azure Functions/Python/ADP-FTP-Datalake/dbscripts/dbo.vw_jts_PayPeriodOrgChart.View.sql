/****** Object:  View [dbo].[vw_jts_PayPeriodOrgChart]    Script Date: 9/23/2024 1:41:39 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO


Create View [dbo].[vw_jts_PayPeriodOrgChart] as
SELECT 
       [AssociateID]
      ,[LastName] + ', ' + [FirstName] as [Employee]
      ,[ReportsTo AssociateID] as [ManagerAssocID]
      ,[ReportsTo LastName] + ', ' + [ReportsTo FirstName] as [Manager]
      ,[Supervisor Name]  as [Supervisor]
  FROM [dbo].[ADPPayrollOrgChart]
  where [Position Status] = 'Active' 


GO
