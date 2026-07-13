{{ config(
    materialized='view'
) }}

select

    household_id,
    region_name,
    city_name,
    grid_zone,
    meter_type,
    customer_category,

    voltage_reading,
    current_reading,
    active_power_kw,
    reactive_power_kvar,

    energy_usage_kwh,
    frequency_hz,
    load_factor,
    peak_demand_kw,
    offpeak_demand_kw,
    daily_consumption_kwh,

    timestamp,

    energy_sk,
    effective_from,
    effective_to,
    is_current

from {{ source('silver','silver_energy_usage') }}