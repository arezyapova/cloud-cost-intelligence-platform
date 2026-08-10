| Field                | Purpose                                            |
| -------------------- | -------------------------------------------------- |
| `billing_date`       | Date associated with the cost                      |
| `provider`           | AWS, Azure or GCP                                  |
| `billing_account_id` | Billing account or subscription                    |
| `resource_id`        | Individual cloud resource                          |
| `service_name`       | Compute, Storage, Database, Networking, etc.       |
| `usage_type`         | Type of billable usage                             |
| `region`             | Cloud region                                       |
| `team`               | Team responsible for the cost                      |
| `project`            | Internal project or product                        |
| `environment`        | Production, Development, Test                      |
| `usage_quantity`     | Amount of resource usage                           |
| `usage_unit`         | Hours, GB, requests, etc.                          |
| `cost_amount`        | Cost before or after discounts—define consistently |
| `currency`           | For example, EUR                                   |
| `tags_present`       | Whether allocation tags are available              |

- `cost_amount` must be numeric and non-negative unless credit records are
  deliberately included.
- `billing_date`, `service_name` and `cost_amount` are mandatory.
- Missing `team` or `project` values will be classified as `Unallocated`
  rather than deleted.

## Sample dataset

The project currently uses reproducible synthetic
multi-cloud billing data.

Period: January–June 2026

Approximate volume: 2,500 billing records

Cloud providers:
- AWS
- Azure
- GCP

Currency: EUR

The raw dataset intentionally contains several
data-quality issues:

- missing team allocations
- missing project allocations
- inconsistent environment labels
- duplicate records

These issues will be handled in the Silver layer.
