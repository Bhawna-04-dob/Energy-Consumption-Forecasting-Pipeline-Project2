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

    t.tariff_plan_type,
    t.utility_provider,

    t.unit_rate,
    t.peak_rate,
    t.offpeak_rate,

    t.monthly_bill,
    t.billing_units

from {{ ref('stg_energy_usage') }} e

left join {{ ref('stg_tariff_metrics') }} t

on e.household_id=t.household_id