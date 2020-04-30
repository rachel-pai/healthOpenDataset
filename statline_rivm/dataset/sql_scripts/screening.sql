select B.* EXCEPT(Perioden),
(select title
from your_project_name.statline_rivm.metadata_screening
where col_name = 'Perioden' and key = B.Perioden) AS Perioden,

from your_project_name.statline_rivm.screening B
