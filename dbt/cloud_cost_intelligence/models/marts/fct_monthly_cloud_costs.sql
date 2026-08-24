select
    billing_month,
    provider,
    team,
    project,
    service_name,
    environment,
    allocation_status,

    sum(cost_amount) as total_cost,
    sum(usage_quantity) as total_usage,
    count(*) as usage_records,
    count(distinct resource_id) as resource_count

from {{ ref('stg_cloud_costs') }}

group by
    billing_month,
    provider,
    team,
    project,
    service_name,
    environment,
    allocation_status