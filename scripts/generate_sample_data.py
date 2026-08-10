"""
Generate synthetic multi-cloud billing data for the
Cloud Cost Intelligence Data Platform.

Grain:
One row represents cloud resource/service usage
for one billing date.
"""
import csv
import random
from datetime import date, timedelta
from pathlib import Path


random.seed(42)

OUTPUT_PATH = Path("data/sample/cloud_costs.csv")
NUMBER_OF_ROWS = 2500


providers = {
    "AWS": {
        "accounts": ["aws-1001", "aws-1002"],
        "regions": ["eu-west-1", "eu-central-1"],
    },
    "Azure": {
        "accounts": ["az-2001", "az-2002"],
        "regions": ["westeurope", "northeurope"],
    },
    "GCP": {
        "accounts": ["gcp-3001"],
        "regions": ["europe-west1", "europe-north1"],
    },
}


services = {
    "Compute": {
        "usage_types": ["Instance Hours", "CPU Hours"],
        "unit": "hours",
        "rate": 0.18,
    },
    "Storage": {
        "usage_types": ["Object Storage", "Disk Storage"],
        "unit": "GB",
        "rate": 0.03,
    },
    "Database": {
        "usage_types": ["Database Hours", "Read Operations"],
        "unit": "hours",
        "rate": 0.35,
    },
    "Networking": {
        "usage_types": ["Data Transfer", "Public IP"],
        "unit": "GB",
        "rate": 0.08,
    },
}


team_projects = {
    "Data Platform": [
        "Analytics Platform",
        "Data Governance",
    ],
    "Customer Product": [
        "Customer Portal",
        "Mobile Application",
    ],
    "Infrastructure": [
        "Cloud Migration",
        "Shared Services",
    ],
    "Security": [
        "Identity Platform",
        "Threat Monitoring",
    ],
}


environments = [
    "Production",
    "prod",
    "Development",
    "DEV",
    "Test",
    "test",
]


start_date = date(2026, 1, 1)
end_date = date(2026, 6, 30)

number_of_days = (end_date - start_date).days

rows = []


for row_number in range(NUMBER_OF_ROWS):

    provider = random.choice(list(providers))
    provider_info = providers[provider]

    service = random.choice(list(services))
    service_info = services[service]

    team = random.choice(list(team_projects))
    project = random.choice(team_projects[team])

    # Intentionally create some missing allocation data
    if random.random() < 0.08:
        team = ""

    if random.random() < 0.10:
        project = ""

    environment = random.choice(environments)

    usage_quantity = round(
        random.uniform(5, 500),
        2,
    )

    # Production tends to cost more
    environment_multiplier = (
        1.8
        if environment.lower() in ["production", "prod"]
        else 1.0
    )

    cost_amount = round(
        usage_quantity
        * service_info["rate"]
        * environment_multiplier
        * random.uniform(0.85, 1.15),
        2,
    )

    billing_date = start_date + timedelta(
        days=random.randint(0, number_of_days)
    )

    row = {
        "billing_date": billing_date.isoformat(),
        "provider": provider,
        "billing_account_id": random.choice(
            provider_info["accounts"]
        ),
        "resource_id":
            f"{provider.lower()}-resource-{row_number + 1:05d}",
        "service_name": service,
        "usage_type": random.choice(
            service_info["usage_types"]
        ),
        "region": random.choice(
            provider_info["regions"]
        ),
        "team": team,
        "project": project,
        "environment": environment,
        "usage_quantity": usage_quantity,
        "usage_unit": service_info["unit"],
        "cost_amount": cost_amount,
        "currency": "EUR",
    }

    rows.append(row)


# Add deliberate duplicate records
rows.extend(rows[:10])


OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)


with OUTPUT_PATH.open(
    "w",
    newline="",
    encoding="utf-8",
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=rows[0].keys(),
    )

    writer.writeheader()
    writer.writerows(rows)


print(
    f"Created {len(rows)} records "
    f"at {OUTPUT_PATH}"
)