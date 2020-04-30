with smap2016vzinfo_angstdep_hoog_avg as(
SELECT id, Gemeente, AVG(Hoogrisicoopangstofdepressie_percentage) AS avg_Hoogrisicoopangstofdepressie_percentage
FROM `your_project_name.volksgezondheidenzorg.smap2016vzinfo_angstdep_hoog`
GROUP BY id, Gemeente
),

smap2016vzinfo_angstdep_matig_avg as(
SELECT id, Gemeente, AVG(Matigofhoogrisicoopangstofdepressie_percentage) AS avg_Matigofhoogrisicoopangstofdepressie_percentage
FROM `your_project_name.volksgezondheidenzorg.smap2016vzinfo_angstdep_matig`
GROUP BY id, Gemeente
),

smap2016vzinfo_beb_mobiel_avg as(
SELECT id, Gemeente, AVG(Beperkingeninbewegen_percentage) AS avg_Beperkingeninbewegen_percentage
FROM `your_project_name.volksgezondheidenzorg.smap2016vzinfo_beb_mobiel`
GROUP BY id, Gemeente
),

smap2016vzinfo_bep_gehoor_avg as(
SELECT id, Gemeente, AVG(Gehoorbeperkingen_percentage) AS avg_Gehoorbeperkingen_percentage
FROM `your_project_name.volksgezondheidenzorg.smap2016vzinfo_bep_gehoor`
GROUP BY id, Gemeente
),

smap2016vzinfo_bep_gezicht_avg as(
SELECT id, Gemeente, AVG(Gezichtsbeperkingen_percentage) AS avg_Gezichtsbeperkingen_percentage
FROM `your_project_name.volksgezondheidenzorg.smap2016vzinfo_bep_gezicht`
GROUP BY id, Gemeente
),

smap2016vzinfo_bep_minst_een_avg as(
SELECT id, Gemeente, AVG(Eenofmeerbeperkingen_percentage) AS avg_Eenofmeerbeperkingen_percentage
FROM `your_project_name.volksgezondheidenzorg.smap2016vzinfo_bep_minst_een`
GROUP BY id, Gemeente
),

smap2016vzinfo_eenzaam_avg as(
SELECT id, Gemeente, AVG(Eenzaamheid_percentage) AS avg_Eenzaamheid_percentage
FROM `your_project_name.volksgezondheidenzorg.smap2016vzinfo_eenzaam`
GROUP BY id, Gemeente
),

smap2016vzinfo_eenzaam_ernstig_avg as(
SELECT id, Gemeente, AVG(Ernstigeeenzaamheid_percentage) AS avg_Ernstigeeenzaamheid_percentage
FROM `your_project_name.volksgezondheidenzorg.smap2016vzinfo_eenzaam_ernstig`
GROUP BY id, Gemeente
),

smap2016vzinfo_ervgez_goed_avg as(
SELECT id, Gemeente, AVG(Goedervarengezondheid_percentage) AS avg_Goedervarengezondheid_percentage
FROM `your_project_name.volksgezondheidenzorg.smap2016vzinfo_ervgez_goed`
GROUP BY id, Gemeente
),

smap2016vzinfo_mantelzorger_avg as(
SELECT id, Gemeente, AVG(Mantelzorgers_percentage) AS avg_Mantelzorgers_percentage
FROM `your_project_name.volksgezondheidenzorg.smap2016vzinfo_mantelzorger`
GROUP BY id, Gemeente
),

smap2016vzinfo_obesitas_avg as(
SELECT idID as id, Gemeente, AVG(Ernstigovergewicht_percentage) AS avg_Ernstigovergewicht_percentage
FROM `your_project_name.volksgezondheidenzorg.smap2016vzinfo_obesitas`
GROUP BY idID, Gemeente
),

smap2016vzinfo_ontvmz_nu_65p_avg as(
SELECT id, Gemeente, AVG(Mantelzorgontvangers_percentage) AS avg_Mantelzorgontvangers_percentage
FROM `your_project_name.volksgezondheidenzorg.smap2016vzinfo_ontvmz_nu_65p`
GROUP BY id, Gemeente
),

smap2016vzinfo_overgewicht_avg as(
SELECT id, Gemeente, AVG(Overgewicht_percentage) AS avg_Overgewicht_percentage
FROM `your_project_name.volksgezondheidenzorg.smap2016vzinfo_overgewicht`
GROUP BY id, Gemeente
),

smap2016vzinfo_regie_leven_matig_avg as(
SELECT id, Gemeente, AVG(Regieeigenleven_percentage) AS avg_Regieeigenleven_percentage
FROM `your_project_name.volksgezondheidenzorg.smap2016vzinfo_regie_leven_matig`
GROUP BY id, Gemeente
),

smap2016vzinfo_richtlijn_alcohol_avg as(
SELECT id, Gemeente, AVG(Alcoholrichtlijn_percentage) AS avg_Alcoholrichtlijn_percentage
FROM `your_project_name.volksgezondheidenzorg.smap2016vzinfo_richtlijn_alcohol`
GROUP BY id, Gemeente
)

select beweegem.id,beweegem.Gemeente,beweegem.Sportenbewegen,beweegem.Percentage as Sportenbewegen_Percentage,

fiet2017.Indicator as fietsgebruik2017klik,fiet2017.Percentage as fietsgebruik2017klik_Percentage,
kindmethandicap_2015.Indicator as kindmethandicap_2015,kindmethandicap_2015.Percentage as kindmethandicap_2015_Percentage,
smap2016vzinfo_angstdep_hoog_avg.avg_Hoogrisicoopangstofdepressie_percentage,
smap2016vzinfo_angstdep_matig_avg.avg_Matigofhoogrisicoopangstofdepressie_percentage,
smap2016vzinfo_beb_mobiel_avg.avg_Beperkingeninbewegen_percentage,
smap2016vzinfo_bep_gehoor_avg.avg_Gehoorbeperkingen_percentage,
smap2016vzinfo_bep_gezicht_avg.avg_Gezichtsbeperkingen_percentage,
smap2016vzinfo_bep_minst_een_avg.avg_Eenofmeerbeperkingen_percentage,
smap2016vzinfo_eenzaam_avg.avg_Eenzaamheid_percentage,
smap2016vzinfo_eenzaam_ernstig_avg.avg_Ernstigeeenzaamheid_percentage,
smap2016vzinfo_ervgez_goed_avg.avg_Goedervarengezondheid_percentage,
smap2016vzinfo_mantelzorger_avg.avg_Mantelzorgers_percentage,
smap2016vzinfo_obesitas_avg.avg_Ernstigovergewicht_percentage,
smap2016vzinfo_ontvmz_nu_65p_avg.avg_Mantelzorgontvangers_percentage,
smap2016vzinfo_overgewicht_avg.avg_Overgewicht_percentage,
smap2016vzinfo_regie_leven_matig_avg.avg_Regieeigenleven_percentage,
smap2016vzinfo_richtlijn_alcohol_avg.avg_Alcoholrichtlijn_percentage

from `your_project_name.volksgezondheidenzorg.beweegrichtlijn_gem` as beweegem
inner join `your_project_name.volksgezondheidenzorg.fietsgebruik2017klik` as fiet2017
on beweegem.Gemeente = fiet2017.Gemeente and beweegem.ID = fiet2017.ID

inner join `your_project_name.volksgezondheidenzorg.kindmethandicap_2015` as kindmethandicap_2015
on beweegem.Gemeente = kindmethandicap_2015.Gemeente and beweegem.ID = kindmethandicap_2015.ID

inner join smap2016vzinfo_angstdep_hoog_avg
on beweegem.Gemeente = smap2016vzinfo_angstdep_hoog_avg.Gemeente and beweegem.ID = smap2016vzinfo_angstdep_hoog_avg.ID

inner join smap2016vzinfo_angstdep_matig_avg
on beweegem.Gemeente = smap2016vzinfo_angstdep_matig_avg.Gemeente and beweegem.ID = smap2016vzinfo_angstdep_matig_avg.ID

inner join smap2016vzinfo_beb_mobiel_avg
on beweegem.Gemeente = smap2016vzinfo_beb_mobiel_avg.Gemeente and beweegem.ID = smap2016vzinfo_beb_mobiel_avg.ID

inner join smap2016vzinfo_bep_gehoor_avg
on beweegem.Gemeente = smap2016vzinfo_bep_gehoor_avg.Gemeente and beweegem.ID = smap2016vzinfo_bep_gehoor_avg.ID

inner join smap2016vzinfo_bep_gezicht_avg
on beweegem.Gemeente = smap2016vzinfo_bep_gezicht_avg.Gemeente and beweegem.ID = smap2016vzinfo_bep_gezicht_avg.ID

inner join smap2016vzinfo_bep_minst_een_avg
on beweegem.Gemeente = smap2016vzinfo_bep_minst_een_avg.Gemeente and beweegem.ID = smap2016vzinfo_bep_minst_een_avg.ID

inner join smap2016vzinfo_eenzaam_avg
on beweegem.Gemeente = smap2016vzinfo_eenzaam_avg.Gemeente and beweegem.ID = smap2016vzinfo_eenzaam_avg.ID

inner join smap2016vzinfo_eenzaam_ernstig_avg
on beweegem.Gemeente = smap2016vzinfo_eenzaam_ernstig_avg.Gemeente and beweegem.ID = smap2016vzinfo_eenzaam_ernstig_avg.ID

inner join smap2016vzinfo_ervgez_goed_avg
on beweegem.Gemeente = smap2016vzinfo_ervgez_goed_avg.Gemeente and beweegem.ID = smap2016vzinfo_ervgez_goed_avg.ID

inner join smap2016vzinfo_mantelzorger_avg
on beweegem.Gemeente = smap2016vzinfo_mantelzorger_avg.Gemeente and beweegem.ID = smap2016vzinfo_mantelzorger_avg.ID

inner join smap2016vzinfo_obesitas_avg
on beweegem.Gemeente = smap2016vzinfo_obesitas_avg.Gemeente and beweegem.ID = smap2016vzinfo_obesitas_avg.ID

inner join smap2016vzinfo_ontvmz_nu_65p_avg
on beweegem.Gemeente = smap2016vzinfo_ontvmz_nu_65p_avg.Gemeente and beweegem.ID = smap2016vzinfo_ontvmz_nu_65p_avg.ID

inner join smap2016vzinfo_overgewicht_avg
on beweegem.Gemeente = smap2016vzinfo_overgewicht_avg.Gemeente and beweegem.ID = smap2016vzinfo_overgewicht_avg.ID

inner join smap2016vzinfo_regie_leven_matig_avg
on beweegem.Gemeente = smap2016vzinfo_regie_leven_matig_avg.Gemeente and beweegem.ID = smap2016vzinfo_regie_leven_matig_avg.ID

inner join smap2016vzinfo_richtlijn_alcohol_avg
on beweegem.Gemeente = smap2016vzinfo_richtlijn_alcohol_avg.Gemeente and beweegem.ID = smap2016vzinfo_richtlijn_alcohol_avg.ID
