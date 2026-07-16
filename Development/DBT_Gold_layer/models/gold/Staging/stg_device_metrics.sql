{{ config(
    materialized='view'
) }}

select

    household_id,
    device_category,
    device_brand,
    device_model,
    maintenance_status,
    installation_region,

    runtime_hours,
    device_power_kw,
    motor_speed_rpm,
    efficiency_ratio,
    energy_draw_kwh,
    heat_output,
    cooling_load,
    device_voltage,
    device_current,
    device_temperature,

    ingestion_timestamp,

    device_sk,
    effective_from,
    effective_to,
    is_current

from {{ source('silver','silver_device_metrics') }}