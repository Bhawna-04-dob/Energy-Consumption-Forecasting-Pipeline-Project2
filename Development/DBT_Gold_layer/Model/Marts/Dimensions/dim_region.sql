{{ config(
    materialized='table'
) }}

select distinct

    region_name,

    city_name,

    grid_zone,

    current_timestamp() as created_date

from {{ ref('stg_energy_usage') }}