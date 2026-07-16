{{ config(
    materialized='table'
) }}

select *

from {{ ref('fact_energy_usage') }}