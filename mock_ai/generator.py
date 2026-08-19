from typing import Dict, Any

class APIMockGenerator:
    def generate_mock_for_schema(self, schema_name: str) -> Dict[str, Any]:
        return {
            "schema": schema_name,
            "mock_data": {
                "id": "usr_9981",
                "name": "Sarah Connor",
                "email": "sarah.connor@cyberdyne.io",
                "active_subscriptions": ["Pro_Plan_2026"]
            }
        }
