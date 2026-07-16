{{ config(
    materialized='table'
) }}

with weather as (

    select *

    from (

        select
            *,
            row_number() over (
                partition by household_id, timestamp
                order by timestamp desc
            ) as rn

        from {{ ref('int_energy_weather') }}

    )

    where rn = 1

),

tariff as (

    select *

    from (

        select
            *,
            row_number() over (
                partition by household_id, timestamp
                order by timestamp desc
            ) as rn

        from {{ ref('int_energy_tariff') }}

    )

    where rn = 1

)

select

    w.household_id,

    cast(w.timestamp as date) as usage_date,

    w.timestamp,

    w.region_name,

    w.city_name,

    t.tariff_plan_type,

    t.utility_provider,

    w.energy_usage_kwh,

    w.daily_consumption_kwh,

    w.peak_demand_kw,

    w.load_factor,

    w.temperature_celsius,

    w.humidity_percent,

    w.rainfall_mm,

    w.wind_speed_kmh,

    w.condition_type,

    t.unit_rate,

    t.peak_rate,

    t.offpeak_rate,

    t.monthly_bill,

    t.billing_units,

    current_timestamp() as created_date

from weather w

inner join tariff t

on w.household_id = t.household_id
and w.timestamp = t.timestamp