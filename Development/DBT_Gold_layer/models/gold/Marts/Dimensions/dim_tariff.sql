{{ config(
    materialized='table'
) }}

select distinct

    tariff_plan_type,

    utility_provider,

    unit_rate,

    peak_rate,

    offpeak_rate,

    current_timestamp() as created_date

from {{ ref('int_energy_tariff') }}