{{ config(
    materialized='view'
) }}

select

    household_id,
    weather_region,
    weather_city,
    weather_station,
    climate_zone,
    condition_type,

    temperature_celsius,
    humidity_percent,
    wind_speed_kmh,
    rainfall_mm,
    pressure_hpa,
    solar_radiation,
    dew_point,
    uv_index,
    visibility_km,
    cloud_cover_percent,

    timestamp,

    weather_sk,
    effective_from,
    effective_to,
    is_current

from {{ source('silver','silver_weather') }}