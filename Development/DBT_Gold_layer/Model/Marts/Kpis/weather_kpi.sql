{{ config(
    materialized='table'
) }}

select

    condition_type,

    avg(temperature_celsius) as average_temperature,

    avg(humidity_percent) as average_humidity,

    avg(rainfall_mm) as average_rainfall,

    avg(energy_usage_kwh) as average_energy_usage,

    current_timestamp() as created_date

from {{ ref('fact_energy_usage') }}

group by condition_type