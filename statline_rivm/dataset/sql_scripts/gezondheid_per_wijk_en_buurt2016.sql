with G AS (
SELECT *
FROM
  `your_project_name.statline_rivm.gezondheid_per_wijk_en_buurt2016_*`
WHERE
  _TABLE_SUFFIX BETWEEN '1'
  AND '3'
)

select G.* except (Leeftijd,WijkenEnBuurten),
(select title
from your_project_name.statline_rivm.metadata_gezondheid_per_wijk_en_buurt2016
where col_name = 'WijkenEnBuurten' and key = G.WijkenEnBuurten) AS WijkenEnBuurten,
(select title
from your_project_name.statline_rivm.metadata_gezondheid_per_wijk_en_buurt2016
where col_name = 'Leeftijd' and key =CAST(G.Leeftijd AS STRING)) AS Leeftijd
from  G
