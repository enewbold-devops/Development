CREATE TABLE [dbo].[ADPPayrollOrgChart](
	[recordIdentity] [int] IDENTITY(1,1) NOT NULL,
	[recordID] [uniqueidentifier] NULL,
	[AssociateID] [nvarchar](255) NULL,
	[FirstName] [nvarchar](255) NULL,
	[LastName] [nvarchar](255) NULL,
	[MiddleName] [nvarchar](255) NULL,
	[Position Status] [nvarchar](255) NULL,
	[ReportsTo AssociateID] [nvarchar](255) NULL,
	[ReportsTo FirstName] [nvarchar](255) NULL,
	[ReportsTo LastName] [nvarchar](255) NULL,
	[Supervisor Name] [nvarchar](255) NULL,
	[ReportsTo EffectiveDate] [date] NULL,
	[IsActive] [bit] NULL,
	[IsDemoData] [bit] NULL,
	[CreatedOn] [date] NULL,
	[CreatedBy] [nvarchar](255) NULL,
	[ModifiedOn] [date] NULL,
	[ModifiedBy] [nvarchar](255) NULL,
PRIMARY KEY CLUSTERED 
(
	[recordIdentity] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[ADPPayrollOrgChart] ADD  DEFAULT (newid()) FOR [recordID]
GO

ALTER TABLE [dbo].[ADPPayrollOrgChart] ADD  DEFAULT ((1)) FOR [IsActive]
GO

ALTER TABLE [dbo].[ADPPayrollOrgChart] ADD  DEFAULT ((0)) FOR [IsDemoData]
GO

ALTER TABLE [dbo].[ADPPayrollOrgChart] ADD  DEFAULT (getdate()) FOR [CreatedOn]
GO

ALTER TABLE [dbo].[ADPPayrollOrgChart] ADD  DEFAULT ('azfn_system') FOR [CreatedBy]
GO

ALTER TABLE [dbo].[ADPPayrollOrgChart] ADD  DEFAULT (getdate()) FOR [ModifiedOn]
GO