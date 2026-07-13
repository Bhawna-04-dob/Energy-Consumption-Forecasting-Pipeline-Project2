{{ config(
    materialized='table'
) }}

select

    grid_region,

    avg(grid_load_kw) as average_grid_load,

    avg(transformer_load) as average_transformer_load,

    avg(line_loss_percent) as average_line_loss,

    avg(reserve_margin) as average_reserve_margin,

    current_timestamp() as created_date

from {{ ref('fact_grid_load') }}

group by grid_region