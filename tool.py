import httpx
import structlog
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from config.settings import settings
from .models import ToolResult
from tenacity import retry, stop_after_attempt, wait_exponential

logger = structlog.get_logger()

class BaseTool:
    def __init__(self, name: str):
        self.name = name
        self.client = httpx.AsyncClient(timeout=settings.request_timeout)
    
    async def execute(self, **kwargs) -> ToolResult:
        raise NotImplementedError
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

class AvailabilityTool(BaseTool):
    def __init__(self):
        super().__init__("get_availability")
        self.api_url = settings.availability_api_url
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def execute(self, service_type: str, location: Optional[str] = None, 
                     preferred_date: Optional[str] = None, **kwargs) -> ToolResult:
        try:
            headers = {
                "Authorization": f"Bearer {settings.internal_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "service_type": service_type,
                "location": location,
                "preferred_date": preferred_date,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("Calling availability API", payload=payload)
            
            # Mock response for development - Replace with actual API call
            # response = await self.client.post(self.api_url, json=payload, headers=headers)
            # response.raise_for_status()
            # result = response.json()
            
            # Mock data - Remove when integrating with real API
            result = {
                "available_slots": [
                    {"date": "2025-07-29", "time": "09:00", "technician": "John D."},
                    {"date": "2025-07-29", "time": "14:00", "technician": "Sarah M."},
                    {"date": "2025-07-30", "time": "10:00", "technician": "Mike R."},
                ],
                "service_type": service_type,
                "location": location or "Default service area",
                "earliest_available": "2025-07-29 09:00"
            }
            
            return ToolResult(
                tool_name=self.name,
                result=result,
                success=True
            )
            
        except Exception as e:
            logger.error("Availability API call failed", error=str(e))
            return ToolResult(
                tool_name=self.name,
                result={},
                success=False,
                error_message=str(e)
            )

class PricingTool(BaseTool):
    def __init__(self):
        super().__init__("get_pricing")
        self.api_url = settings.pricing_api_url
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def execute(self, services: List[str], location: Optional[str] = None, 
                     service_complexity: str = "standard", **kwargs) -> ToolResult:
        try:
            headers = {
                "Authorization": f"Bearer {settings.internal_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "services": services,
                "location": location,
                "service_complexity": service_complexity,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("Calling pricing API", payload=payload)
            
            # Mock response for development - Replace with actual API call
            # response = await self.client.post(self.api_url, json=payload, headers=headers)
            # response.raise_for_status()
            # result = response.json()
            
            # Mock data - Remove when integrating with real API
            base_prices = {
                "ac_repair": 150,
                "ac_installation": 800,
                "thermostat_installation": 200,
                "hvac_maintenance": 120,
                "heating_repair": 180
            }
            
            total_cost = 0
            service_breakdown = []
            
            for service in services:
                cost = base_prices.get(service.lower().replace(" ", "_"), 100)
                service_breakdown.append({
                    "service": service,
                    "cost": cost,
                    "description": f"Professional {service} service"
                })
                total_cost += cost
            
            # Apply location and complexity modifiers
            if service_complexity == "complex":
                total_cost *= 1.3
            
            result = {
                "total_cost": round(total_cost, 2),
                "service_breakdown": service_breakdown,
                "location": location or "Standard service area",
                "estimated_duration": f"{len(services) * 2}-{len(services) * 3} hours",
                "warranty": "1 year parts and labor"
            }
            
            return ToolResult(
                tool_name=self.name,
                result=result,
                success=True
            )
            
        except Exception as e:
            logger.error("Pricing API call failed", error=str(e))
            return ToolResult(
                tool_name=self.name,
                result={},
                success=False,
                error_message=str(e)
            )

class ToolRegistry:
    def __init__(self):
        self.tools = {
            "get_availability": AvailabilityTool(),
            "get_pricing": PricingTool()
        }
    
    def get_tool(self, tool_name: str) -> Optional[BaseTool]:
        return self.tools.get(tool_name)
    
    def get_available_tools(self) -> List[str]:
        return list(self.tools.keys())
    
    def get_tool_descriptions(self) -> Dict[str, str]:
        return {
            "get_availability": "Check available appointment slots for services. Parameters: service_type (required), location (optional), preferred_date (optional)",
            "get_pricing": "Get pricing information for services. Parameters: services (required list), location (optional), service_complexity (optional: standard/complex)"
        }

# Global tool registry instance
tool_registry = ToolRegistry()
