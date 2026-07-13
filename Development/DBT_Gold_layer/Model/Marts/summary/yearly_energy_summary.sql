{{ config(
    materialized='table'
) }}

select

    year(usage_date) as year,

    count(distinct household_id) as total_households,

    sum(energy_usage_kwh) as total_energy_usage,

    sum(monthly_bill) as total_revenue,

    avg(load_factor) as avg_load_factor,

    current_timestamp() as created_date

from {{ ref('fact_energy_usage') }}

group by year(usage_date)