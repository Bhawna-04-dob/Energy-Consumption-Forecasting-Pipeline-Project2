{{ config(
    materialized='table'
) }}

select

    e.household_id,
    e.timestamp,

    e.region_name,
    e.city_name,

    e.energy_usage_kwh,
    e.daily_consumption_kwh,
    e.peak_demand_kw,
    e.load_factor,

    w.temperature_celsius,
    w.humidity_percent,
    w.rainfall_mm,
    w.wind_speed_kmh,
    w.condition_type

from {{ ref('stg_energy_usage') }} e

left join {{ ref('stg_weather') }} w

on e.household_id = w.household_id
and date(e.timestamp)=date(w.timestamp)