CREATE TABLE [dbo].[ADPHoursArchive](
	[recordIdentity] [int] IDENTITY(1,1) NOT NULL,
	[recordID] [uniqueidentifier] NULL,
	[Department] [nvarchar](50) NULL,
	[Client] [nvarchar](50) NULL,
	[Project] [nvarchar](50) NULL,
	[Sub_Project] [nvarchar](50) NULL,
	[Employee] [nvarchar](50) NULL,
	[ID_Number] [nvarchar](50) NULL,
	[Date] [nvarchar](50) NULL,
	[Hours] [float] NULL,
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

ALTER TABLE [dbo].[ADPHoursArchive] ADD  DEFAULT (newid()) FOR [recordID]
GO

ALTER TABLE [dbo].[ADPHoursArchive] ADD  DEFAULT ((1)) FOR [IsActive]
GO

ALTER TABLE [dbo].[ADPHoursArchive] ADD  DEFAULT ((0)) FOR [IsDemoData]
GO

ALTER TABLE [dbo].[ADPHoursArchive] ADD  DEFAULT (getdate()) FOR [CreatedOn]
GO

ALTER TABLE [dbo].[ADPHoursArchive] ADD  DEFAULT ('azfn_system') FOR [CreatedBy]
GO

ALTER TABLE [dbo].[ADPHoursArchive] ADD  DEFAULT (getdate()) FOR [ModifiedOn]
GO

ALTER TABLE [dbo].[ADPHoursArchive] ADD  DEFAULT ('azfn_system') FOR [ModifiedBy]
GO
