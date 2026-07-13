{{ config(
    materialized='view'
) }}

select

    household_id,
    tariff_region,
    tariff_city,
    tariff_plan_type,
    billing_cycle,
    utility_provider,

    unit_rate,
    peak_rate,
    offpeak_rate,
    fixed_charge,
    tax_amount,
    subsidy_amount,
    monthly_bill,
    billing_units,
    late_fee,
    adjustment_amount,

    ingestion_timestamp,

    tariff_sk,
    effective_from,
    effective_to,
    is_current

from {{ source('silver','silver_tariff_metrics') }}