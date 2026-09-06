import os
import sys
import asyncio

backend_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(backend_dir)
sys.path.insert(0, backend_dir)
sys.path.insert(0, project_dir)

import database
from services.alert_service import alert_service


async def main():
    database.init_pool()
    database.init_schema()

    print("Step 1: Running live ML risk predictions across all 37 NER locations...")
    sync_res = await alert_service.sync_live_alerts_from_ml()
    print("Sync Summary:", sync_res)

    print("\nStep 2: Fetching regional dashboard summary...")
    summary = await alert_service.get_regional_dashboard_summary()
    print("Monitored Stations:", summary["statistics"]["monitoredLocations"])
    print("Active Alerts:", summary["statistics"]["activeAlerts"])
    print("Risk Distribution:", summary["riskDistribution"])

    print("\nStep 3: Fetching risk map zones...")
    zones = await alert_service.get_all_risk_zones()
    print("Total Map Zones:", len(zones))
    for z in zones[:5]:
        p = z["probability"] * 100
        print(f"  * {z['name']}: {z['riskLevel']} ({p:.1f}%)")


if __name__ == "__main__":
    asyncio.run(main())
