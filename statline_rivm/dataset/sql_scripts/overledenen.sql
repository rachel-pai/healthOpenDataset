select B.* EXCEPT(Leeftijd,Geslacht,Doodsoorzaken,Perioden),
(select title
from your_project_name.statline_rivm.metadata_overledenen
where col_name = 'Leeftijd' and key = CAST(B.Leeftijd AS STRING)) AS Leeftijd,
(select title
from your_project_name.statline_rivm.metadata_overledenen
where col_name = 'Geslacht' and key = B.Geslacht) AS Geslacht,
(select title
from your_project_name.statline_rivm.metadata_overledenen
where col_name = 'Doodsoorzaken' and key = B.Doodsoorzaken) AS Doodsoorzaken,
(select title
from your_project_name.statline_rivm.metadata_overledenen
where col_name = 'Perioden' and key = B.Perioden) AS Perioden

from your_project_name.statline_rivm.overledenen B
