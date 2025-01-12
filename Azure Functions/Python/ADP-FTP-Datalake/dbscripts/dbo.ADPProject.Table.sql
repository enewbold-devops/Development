/****** Object:  Table [dbo].[ADPProject]    Script Date: 9/23/2024 1:41:39 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ADPProject](
	[recordIdentity] [int] IDENTITY(1,1) NOT NULL,
	[recordID] [uniqueidentifier] NULL,
	[ADP Project] [nvarchar](255) NULL,
	[Category] [nvarchar](255) NULL,
	[Project Group 1] [nvarchar](255) NULL,
	[Project Group 2] [nvarchar](255) NULL,
	[Project Duration Group] [nvarchar](255) NULL,
	[Project Group 3] [nvarchar](255) NULL,
	[Practice Group] [nvarchar](255) NULL,
	[Modified] [date] NULL,
	[Created] [date] NULL,
	[Created By] [nvarchar](255) NULL,
	[Modified By] [nvarchar](255) NULL,
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
ALTER TABLE [dbo].[ADPProject] ADD  DEFAULT (newid()) FOR [recordID]
GO
ALTER TABLE [dbo].[ADPProject] ADD  DEFAULT ((1)) FOR [IsActive]
GO
ALTER TABLE [dbo].[ADPProject] ADD  DEFAULT ((0)) FOR [IsDemoData]
GO
ALTER TABLE [dbo].[ADPProject] ADD  DEFAULT (getdate()) FOR [CreatedOn]
GO
ALTER TABLE [dbo].[ADPProject] ADD  DEFAULT ('system') FOR [CreatedBy]
GO
ALTER TABLE [dbo].[ADPProject] ADD  DEFAULT (getdate()) FOR [ModifiedOn]
GO
ALTER TABLE [dbo].[ADPProject] ADD  DEFAULT ('system') FOR [ModifiedBy]
GO
