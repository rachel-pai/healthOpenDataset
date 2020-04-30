select B.* EXCEPT(Vaccinaties,Regio,Perioden),
(select title
from your_project_name.statline_rivm.metadata_rijksvaccinatieprogramma
where col_name = 'Vaccinaties' and key = B.Vaccinaties) AS Vaccinaties,
(select title
from your_project_name.statline_rivm.metadata_rijksvaccinatieprogramma
where col_name = 'Regio' and key = B.Regio) AS Regio,
(select title
from your_project_name.statline_rivm.metadata_rijksvaccinatieprogramma
where col_name = 'Perioden' and key = B.Perioden) AS Perioden

from your_project_name.statline_rivm.rijksvaccinatieprogramma B
