select B.ID, B.Gemeentenaam_1, B.SoortRegio_2, B.Codering_3, B.GeluidVanTreinverkeer_4, B.GeluidVanWegverkeer_5, B.Bevolking_6,
(select title
from your_project_name.statline_rivm.metadata_blootstelling_aan_geluid_van_weg
where col_name = 'WijkenEnBuurten' and key = B.WijkenEnBuurten) AS WijkenEnBuurten,
(select title
from your_project_name.statline_rivm.metadata_blootstelling_aan_geluid_van_weg
where col_name = 'Geluidblootstelling' and key = B.Geluidblootstelling) AS Geluidblootstelling,

from your_project_name.statline_rivm.blootstelling_aan_geluid_van_weg B
