with G AS (
SELECT *
FROM
  `your_project_name.statline_rivm.kosten_van_ziekten2017_rivm*`
WHERE
  _TABLE_SUFFIX BETWEEN '1'
  AND '33'
)

select G.* except (Leeftijd,Geslacht,Diagnose,Zorgsector,Zorgfunctie,Financieringsvorm),

(select title
from your_project_name.statline_rivm.metadata_kosten_van_ziekten2017_rivm
where col_name = 'Leeftijd' and key = CAST(G.Leeftijd AS STRING)) AS Leeftijd,

(select title
from your_project_name.statline_rivm.metadata_kosten_van_ziekten2017_rivm
where col_name = 'Geslacht' and key =G.Geslacht) AS Geslacht,

(select title
from your_project_name.statline_rivm.metadata_kosten_van_ziekten2017_rivm
where col_name = 'Diagnose' and key =G.Diagnose) AS Diagnose,

(select title
from your_project_name.statline_rivm.metadata_kosten_van_ziekten2017_rivm
where col_name = 'Zorgsector' and key =G.Zorgsector) AS Zorgsector,

(select title
from your_project_name.statline_rivm.metadata_kosten_van_ziekten2017_rivm
where col_name = 'Zorgfunctie' and key =G.Zorgfunctie) AS Zorgfunctie,

(select title
from your_project_name.statline_rivm.metadata_kosten_van_ziekten2017_rivm
where col_name = 'Financieringsvorm' and key = CAST(G.Financieringsvorm AS STRING)) AS Financieringsvorm

from  G
