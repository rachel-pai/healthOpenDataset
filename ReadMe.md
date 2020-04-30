# Collecting dutch healthcare related opendataset & analyzing important factors for NL coronovirus infected number

The overall result is published on [public_healthcare_dataset_NL.ipynb](public_healthcare_dataset_NL.ipynb).

## Overall steps:
1. Web crawlling/downloading open-dataset from different websites
2. Inserting data into bigquery
3. Combining all collected data to find important factors for NL coronovirus infected number

## File structure:
- [about_nl](about_nl):
  - dutch cities info
- [accuweather](accuweather):
  - ducth city weather info
- [bq_public_dataset](bq_public_dataset):
  - [openstreet](bq_public_dataset/openstreet):
    - dutch map node in openstreet
  - [other_dataset](bq_public_dataset/other_dataset):
    - other dutch info extracted from google public dataset
- [coronvirus_NL](coronvirus_NL):
  - coronorivus info in NL.
- [nivel](nivel):
  - open dataset collected from nivel
- [statline_rivm](statline_rivm):
  - open dataset collected from nivel
- [vetkis](vetkis):
  - open dataset collected from nivel
- [volksgezondheidenzorg](volksgezondheidenzorg):
  - open dataset collected from nivel
- [zorgkaartnederland](zorgkaartnederland):
  - open dataset collected from nivel
- [public_healthcare_dataset_NL.ipynb](public_healthcare_dataset_NL.ipynb): the overall analysis of this opendatset.

<span style="color:red"> N.B.</span> Remeber to replace 'your bq credential json path' in python files and your_project_name in sql query files.
