select B.* EXCEPT(Populatie,Persoonskenmerken,Marges,Perioden),
(select title
from your_project_name.statline_rivm.metadata_participatie
where col_name = 'Populatie' and key = B.Populatie) AS Populatie,
(select title
from your_project_name.statline_rivm.metadata_participatie
where col_name = 'Persoonskenmerken' and key = B.Persoonskenmerken) AS Persoonskenmerken,
(select title
from your_project_name.statline_rivm.metadata_participatie
where col_name = 'Marges' and key = B.Marges) AS Marges,
(select title
from your_project_name.statline_rivm.metadata_participatie
where col_name = 'Perioden' and key = B.Perioden) AS Perioden

from your_project_name.statline_rivm.participatie B
