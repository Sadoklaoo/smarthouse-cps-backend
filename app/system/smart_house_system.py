from app.services.monitor_service import MonitorService
from app.services.reactor_service import ReactorService
import asyncio


class SmartHouseSystem:
    def __init__(self):
        self.monitor_service = MonitorService()
        self.reactor_service = ReactorService()

    async def start(self):
        # Start monitoring and processing events in parallel
        monitor_task = asyncio.create_task(self.monitor_service.monitor_house())
        reactor_task = asyncio.create_task(self.reactor_service.process_events())
        await asyncio.gather(monitor_task, reactor_task)


# Run the system if the script is executed
if __name__ == "__main__":
    system = SmartHouseSystem()
    asyncio.run(system.start())
