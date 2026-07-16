{{ config(
    materialized='table'
) }}

select distinct

    household_id,

    device_category,

    device_brand,

    device_model,

    maintenance_status,

    installation_region,

    current_timestamp() as created_date

from {{ ref('stg_device_metrics') }}