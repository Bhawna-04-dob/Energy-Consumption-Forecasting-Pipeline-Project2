{{ config(
    materialized='table'
) }}

select

    device_category,

    count(distinct household_id) as total_households,

    sum(energy_draw_kwh) as total_energy_consumption,

    avg(runtime_hours) as avg_runtime_hours,

    avg(device_power_kw) as avg_device_power_kw,

    current_timestamp() as created_date

from {{ ref('stg_device_metrics') }}

group by device_category