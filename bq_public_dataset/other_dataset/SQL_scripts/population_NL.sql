WITH country_summary as (
  select *
  from `bigquery-public-data.world_bank_health_population.country_summary`
--   where short_name IN ('Netherlands','Europe & Central Asia','European Union')
  where short_name = 'Netherlands'
),

country_series_def as (
  select series_code, description AS series_code_description, csd.country_code, country_summary.* EXCEPT(country_code)
  from `bigquery-public-data.world_bank_health_population.country_series_definitions` csd
  inner join country_summary
  on csd.country_code = country_summary.country_code
),

health_nut_pop as (
  select indicator_name, indicator_code AS series_code, value AS health_nutrition_population_value , year AS health_nutrition_population_year, country_series_def.* EXCEPT (country_code, series_code)
  from `bigquery-public-data.world_bank_health_population.health_nutrition_population` hnp
  inner join country_series_def
  on hnp.country_code= country_series_def.country_code AND hnp.indicator_code= country_series_def.series_code
),

series_sum as (
select ss.*
from `bigquery-public-data.world_bank_health_population.series_summary` ss
inner join country_series_def csd
on csd.series_code = ss.series_code
)

select hnp.*,ss.* EXCEPT (series_code,indicator_name)
from health_nut_pop hnp
join series_sum ss
on ss.series_code = hnp.series_code
AND ss.indicator_name = hnp.indicator_name

-- SELECT hnp.*, ss.* EXCEPT (indicator_name,series_code), cs.*
-- FROM health_nut_pop hnp
-- join series_sum
-- on series_sum.series_code = hnp.series_code AND ss.indicator_name = hnp.indicator_name
-- inner join country_series_def csd
-- on csd.series_code = hnp.series_code AND csd.series_code = ss.series_code
-- inner join country_summary cs
-- on cs.country_code = csd.country_code

