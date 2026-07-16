{{ config(
    materialized='table'
) }}

select distinct

    cast(timestamp as date) as date,

    year(timestamp) as year,

    month(timestamp) as month,

    day(timestamp) as day,

    quarter(timestamp) as quarter,

    weekofyear(timestamp) as week_no,

    date_format(timestamp,'EEEE') as day_name,

    current_timestamp() as created_date

from {{ ref('stg_energy_usage') }}