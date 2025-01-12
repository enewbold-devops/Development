create table dbo.CLIENTS(
	ID VARCHAR(20) NOT NULL PRIMARY KEY,
	[NAME] VARCHAR(255) NOT NULL,
	[START_DATE] DATE,
	[END_DATE] DATE,
	ACTIVE INT NOT NULL DEFAULT 1
);

create table dbo.PROJECTS(
	ID VARCHAR(50) NOT NULL PRIMARY KEY,
	CLIENT_ID VARCHAR(20) NOT NULL,
	[NAME] VARCHAR(255) NOT NULL,
	[START_DATE] DATE,
	[END_DATE] DATE,
	ACTIVE INT NOT NULL DEFAULT 1
);

create table dbo.SUBPROJECTS(
	ID VARCHAR(100) NOT NULL,
	PROJECT_ID VARCHAR(50) NOT NULL,
	CLIENT_ID VARCHAR(20) NOT NULL,
	[NAME] VARCHAR(255) NOT NULL,
	[START_DATE] DATE,
	[END_DATE] DATE,
	ACTIVE INT NOT NULL DEFAULT 1
);
