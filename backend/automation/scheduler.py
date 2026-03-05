from apscheduler.schedulers.blocking import BlockingScheduler
from backend.connectors.sync_manager import run_sync


scheduler = BlockingScheduler()

scheduler.add_job(
    run_sync,
    "interval",
    hours=6
)

print("Sync scheduler started...")

scheduler.start()