SELECT f.*,
b.* EXCEPT (year,country_code,country_name),
a.country_area,
m.midyear_population AS midyear_population_all,
mas.* EXCEPT (year,country_code,country_name),
mle.* EXCEPT (year,country_code,country_name),
FROM `bigquery-public-data.census_bureau_international.age_specific_fertility_rates` f
INNER JOIN `bigquery-public-data.census_bureau_international.birth_death_growth_rates` b ON b.year = f.year AND f.country_code ='NL' AND b.country_code = 'NL'
INNER JOIN `bigquery-public-data.census_bureau_international.country_names_area` a ON a.country_code = f.country_code AND f.country_code ='NL'
INNER JOIN `bigquery-public-data.census_bureau_international.midyear_population` m ON m.year = f.year AND f.country_code ='NL' AND m.country_code = 'NL'
INNER JOIN `bigquery-public-data.census_bureau_international.midyear_population_age_sex` mas ON mas.year = f.year AND f.country_code ='NL' AND mas.country_code = 'NL'
INNER JOIN `bigquery-public-data.census_bureau_international.mortality_life_expectancy` mle ON mle.year = f.year AND f.country_code ='NL' AND mle.country_code = 'NL'
