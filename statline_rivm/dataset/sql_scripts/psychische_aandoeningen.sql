select B.* EXCEPT(Geslacht,Persoonskenmerken,PsychiatrischeAandoeningen,Perioden),
(select title
from your_project_name.statline_rivm.metadata_psychische_aandoeningen
where col_name = 'Geslacht' and key = B.Geslacht) AS Geslacht,
(select title
from your_project_name.statline_rivm.metadata_psychische_aandoeningen
where col_name = 'Persoonskenmerken' and key = B.Persoonskenmerken) AS Persoonskenmerken,
(select title
from your_project_name.statline_rivm.metadata_psychische_aandoeningen
where col_name = 'PsychiatrischeAandoeningen' and key = B.PsychiatrischeAandoeningen) AS PsychiatrischeAandoeningen,
(select title
from your_project_name.statline_rivm.metadata_psychische_aandoeningen
where col_name = 'Perioden' and key = B.Perioden) AS Perioden,

from your_project_name.statline_rivm.psychische_aandoeningen B
