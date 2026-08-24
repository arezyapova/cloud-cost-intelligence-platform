select
    billing_date,
    billing_month,
    provider,
    billing_account_id,
    resource_id,
    service_name,
    usage_type,
    region,
    team,
    project,
    environment,
    allocation_status,
    usage_quantity,
    usage_unit,
    cost_amount,
    currency

from {{ source('cloud_cost_intelligence', 'silver_cloud_costs') }}