{{ config(
    materialized='table'
) }}

with household_data as (

    select
        household_id,
        customer_category,
        meter_type,
        city_name,
        region_name,
        grid_zone,

        row_number() over(
            partition by household_id
            order by timestamp desc
        ) as rn

    from {{ ref('stg_energy_usage') }}

)

select

    household_id,
    customer_category,
    meter_type,
    city_name,
    region_name,
    grid_zone,

    current_timestamp() as created_date

from household_data

where rn = 1