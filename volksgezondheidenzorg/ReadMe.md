# Collecting data from [volksgezondheidenzorg](https://www.volksgezondheidenzorg.info/)
Steps:
1. Run insertBQ.py
2. [summarize_gemeentenaam.py](summarize_gemeentenaam.py):
    - summarize all tables and connnect them by 'Gemeente'
    - pivot 'beweegrichtlijn_gem' table
    - insert summarize table into BQ


