import sys
import os
import random
from datetime import datetime, timedelta

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from app.core.database import SessionLocal, engine
from app.models.database import (
    SalesData,
    CostData,
    MarketingData,
    CustomerData,
)
from app.crud import crud_kpi
from app.schemas.kpi import KPICreate


# =====================================================
# KPI MASTER DATA
# =====================================================
def create_sample_kpis(db):
    kpis = [
        {
            "name": "Total Revenue",
            "description": "Total revenue generated in the given period",
            "unit": "USD",
        },
        {
            "name": "Profit",
            "description": "Profit calculated as revenue minus costs",
            "unit": "USD",
        },
        {
            "name": "Customer Acquisition Cost",
            "description": "Cost to acquire a new customer",
            "unit": "USD",
        },
        {
            "name": "Customer Retention Rate",
            "description": "Percentage of customers retained over a period",
            "unit": "%",
        },
    ]

    for kpi_data in kpis:
        kpi_create = KPICreate(**kpi_data)
        crud_kpi.create(db, obj_in=kpi_create)

    print(f"Created {len(kpis)} sample KPIs")


# =====================================================
# SALES DATA
# =====================================================
def create_sample_sales_data(db):
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 3, 31)
    current_date = start_date

    count = 0

    while current_date <= end_date:
        for _ in range(random.randint(1, 6)):
            db.add(
                SalesData(
                    date=current_date,
                    amount=round(random.uniform(50, 500), 2),
                    product_id=f"PROD{random.randint(1,100):03d}",
                    customer_id=random.randint(1, 1000),
                    region=random.choice(["North", "South", "East", "West"]),
                )
            )
            count += 1

        current_date += timedelta(days=1)

    print(f"Created {count} sample sales records")


# =====================================================
# COST DATA
# =====================================================
def create_sample_cost_data(db):
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 3, 31)
    current_date = start_date

    count = 0

    while current_date <= end_date:
        for _ in range(random.randint(1, 4)):
            db.add(
                CostData(
                    date=current_date,
                    amount=round(random.uniform(20, 200), 2),
                    cost_category=random.choice(
                        ["Operations", "Marketing", "Admin", "R&D"]
                    ),
                    department=random.choice(
                        ["IT", "Sales", "HR", "Finance"]
                    ),
                    description=f"Sample cost for {current_date.date()}",
                )
            )
            count += 1

        current_date += timedelta(days=1)

    print(f"Created {count} sample cost records")


# =====================================================
# MARKETING DATA
# =====================================================
def create_sample_marketing_data(db):
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 3, 31)
    current_date = start_date

    count = 0

    while current_date <= end_date:
        if random.random() > 0.7:
            for _ in range(random.randint(1, 3)):
                db.add(
                    MarketingData(
                        date=current_date,
                        amount=round(random.uniform(100, 1000), 2),
                        campaign_type=random.choice(
                            ["Online", "Print", "TV", "Radio"]
                        ),
                        campaign_name=f"Campaign {random.randint(1,100)}",
                        channel=random.choice(
                            ["Google", "Facebook", "LinkedIn", "Twitter"]
                        ),
                    )
                )
                count += 1

        current_date += timedelta(days=1)

    print(f"Created {count} sample marketing records")


# =====================================================
# CUSTOMER DATA
# =====================================================
def create_sample_customer_data(db):
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 3, 31)
    current_date = start_date

    customer_id = 1
    count = 0

    while current_date <= end_date:
        for _ in range(random.randint(0, 4)):
            signup_date = current_date
            last_activity = signup_date + timedelta(days=random.randint(0, 90))

            db.add(
                CustomerData(
                    customer_id=customer_id,
                    name=f"Customer {customer_id}",
                    email=f"customer{customer_id}@example.com",
                    signup_date=signup_date,
                    last_activity_date=last_activity,
                    total_purchases=round(random.uniform(0, 1000), 2),
                    total_value=round(random.uniform(50, 5000), 2),
                    region=random.choice(["North", "South", "East", "West"]),
                )
            )

            customer_id += 1
            count += 1

        current_date += timedelta(days=1)

    print(f"Created {count} sample customer records")


# =====================================================
# MAIN
# =====================================================
def main():
    print("Creating sample data...")
    print("🌱 SEED DATABASE URL:", engine.url)

    db = SessionLocal()
    try:
        create_sample_kpis(db)
        create_sample_sales_data(db)
        create_sample_cost_data(db)
        create_sample_marketing_data(db)
        create_sample_customer_data(db)
        db.commit()
        print("✅ Sample data created successfully!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating sample data: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
