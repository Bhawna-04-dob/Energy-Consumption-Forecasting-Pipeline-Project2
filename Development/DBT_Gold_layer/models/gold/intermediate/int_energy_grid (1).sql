{{ config(
    materialized='table'
) }}

select

    e.household_id,
    e.timestamp,

    e.region_name,

    e.energy_usage_kwh,
    e.load_factor,

    g.grid_region,
    g.substation_name,
    g.feeder_line,

    g.grid_load_kw,
    g.transformer_load,
    g.line_loss_percent,
    g.reserve_margin

from {{ ref('stg_energy_usage') }} e

left join {{ ref('stg_grid_load') }} g

on e.household_id=g.household_id