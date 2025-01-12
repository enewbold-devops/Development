/****** Object:  Table [dbo].[AccountAudit]    Script Date: 9/23/2024 1:41:39 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[AccountAudit](
	[recordIdentity] [int] IDENTITY(1,1) NOT NULL,
	[recordID] [uniqueidentifier] NULL,
	[AccountId] [nvarchar](255) NULL,
	[Soarian User] [nvarchar](255) NULL,
	[Comment] [nvarchar](max) NULL,
	[Activity Date] [nvarchar](255) NULL,
	[Timely Reason Code] [nvarchar](255) NULL,
	[Correct Act Reason Code] [nvarchar](255) NULL,
	[Proper Doc Reason Code] [nvarchar](255) NULL,
	[Reshow Reason Code] [nvarchar](255) NULL,
	[Due Date] [nvarchar](255) NULL,
	[Audit Status] [nvarchar](255) NULL,
	[Level Of Care] [nvarchar](255) NULL,
	[Balance] [nvarchar](255) NULL,
	[Supervisor] [nvarchar](255) NULL,
	[Challenge Reason Code] [nvarchar](255) NULL,
	[Auditor] [nvarchar](255) NULL,
	[Auditor Notes] [nvarchar](max) NULL,
	[Client] [nvarchar](255) NULL,
	[Auditor2] [nvarchar](255) NULL,
	[Auditor3] [nvarchar](255) NULL,
	[Auditor4] [nvarchar](255) NULL,
	[Modified] [date] NULL,
	[Created] [date] NULL,
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
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
ALTER TABLE [dbo].[AccountAudit] ADD  DEFAULT (newid()) FOR [recordID]
GO
ALTER TABLE [dbo].[AccountAudit] ADD  DEFAULT ((1)) FOR [IsActive]
GO
ALTER TABLE [dbo].[AccountAudit] ADD  DEFAULT ((0)) FOR [IsDemoData]
GO
ALTER TABLE [dbo].[AccountAudit] ADD  DEFAULT (getdate()) FOR [CreatedOn]
GO
ALTER TABLE [dbo].[AccountAudit] ADD  DEFAULT ('system') FOR [CreatedBy]
GO
ALTER TABLE [dbo].[AccountAudit] ADD  DEFAULT (getdate()) FOR [ModifiedOn]
GO
ALTER TABLE [dbo].[AccountAudit] ADD  DEFAULT ('system') FOR [ModifiedBy]
GO
