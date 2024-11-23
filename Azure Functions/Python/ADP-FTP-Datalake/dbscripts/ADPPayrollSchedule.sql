CREATE TABLE [dbo].[ADPPayrollSchedule](
	[recordIdentity] [int] IDENTITY(1,1) NOT NULL,
	[recordID] [uniqueidentifier] NULL,
	[Week] [int] NULL,
	[In Date] [date] NULL,
	[Out Date] [date] NULL,
	[Pay Date] [date] NULL,
	[Period End] [date] NULL,
	[Year] [int] NULL,
	[Quarter] [nvarchar](255) NULL,
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

ALTER TABLE [dbo].[ADPPayrollSchedule] ADD  DEFAULT (newid()) FOR [recordID]
GO

ALTER TABLE [dbo].[ADPPayrollSchedule] ADD  DEFAULT ((1)) FOR [IsActive]
GO

ALTER TABLE [dbo].[ADPPayrollSchedule] ADD  DEFAULT ((0)) FOR [IsDemoData]
GO

ALTER TABLE [dbo].[ADPPayrollSchedule] ADD  DEFAULT (getdate()) FOR [CreatedOn]
GO

ALTER TABLE [dbo].[ADPPayrollSchedule] ADD  DEFAULT ('azfn_system') FOR [CreatedBy]
GO

ALTER TABLE [dbo].[ADPPayrollSchedule] ADD  DEFAULT (getdate()) FOR [ModifiedOn]
GO

ALTER TABLE [dbo].[ADPPayrollSchedule] ADD  DEFAULT ('azfn_system') FOR [ModifiedBy]
GO