SELECT t.[Id]
      ,[Location]
      ,t.[Name]
      ,[FullName]
      ,d.[Name] as Division
	  ,c.[Name] as Conference
  FROM [NflProjections].[dbo].[Teams] t
  JOIN Divisions d on d.Id = t.DivisionId
  JOIN Conferences c on c.Id = d.ConferenceId