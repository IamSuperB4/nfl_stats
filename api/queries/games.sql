SELECT g.[Id]
      ,[SeasonId]
      ,[Week]
      ,[StartTime]
      ,t_away.[FullName] as AwayTeam
      ,t_home.[FullName] as HomeTeam
  FROM [NflProjections].[dbo].[Games] g
  JOIN Teams t_away on t_away.Id = g.AwayTeamId
  JOIN Teams t_home on t_home.Id = g.HomeTeamId