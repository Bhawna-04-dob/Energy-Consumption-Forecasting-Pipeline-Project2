{{ config(
    materialized='table'
) }}

select

    count(distinct household_id) as total_households,

    sum(energy_usage_kwh) as total_energy_usage,

    sum(monthly_bill) as total_revenue,

    avg(load_factor) as average_load_factor,

    avg(unit_rate) as average_tariff,

    avg(monthly_bill) as average_monthly_bill,

    current_timestamp() as created_date

from {{ ref('fact_energy_usage') }}