{{ config(
    materialized='table'
) }}

select

    usage_date,

    count(distinct household_id) as total_households,

    sum(energy_usage_kwh) as total_energy_usage,

    sum(daily_consumption_kwh) as total_daily_consumption,

    avg(load_factor) as avg_load_factor,

    sum(monthly_bill) as total_revenue,

    current_timestamp() as created_date

from {{ ref('fact_energy_usage') }}

group by usage_date