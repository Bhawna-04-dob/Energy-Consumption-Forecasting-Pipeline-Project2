{{ config(
    materialized='table'
) }}

with grid as (

    select *

    from (

        select
            *,
            row_number() over (
                partition by household_id, timestamp
                order by timestamp desc
            ) as rn

        from {{ ref('int_energy_grid') }}

    )

    where rn = 1

)

select

    household_id,

    cast(timestamp as date) as usage_date,

    timestamp,

    region_name,

    grid_region,

    substation_name,

    feeder_line,

    energy_usage_kwh,

    load_factor,

    grid_load_kw,

    transformer_load,

    line_loss_percent,

    reserve_margin,

    current_timestamp() as created_date

from grid