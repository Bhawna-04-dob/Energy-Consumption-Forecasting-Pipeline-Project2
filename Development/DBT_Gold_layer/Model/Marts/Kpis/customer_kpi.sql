{{ config(
    materialized='table'
) }}

select

    region_name,

    count(distinct household_id) as customer_count,

    avg(monthly_bill) as average_bill,

    sum(energy_usage_kwh) as total_energy_usage,

    current_timestamp() as created_date

from {{ ref('fact_energy_usage') }}

group by region_name