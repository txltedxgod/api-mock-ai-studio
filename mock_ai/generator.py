from __future__ import annotations

import hashlib
import random
from typing import Any


class APIMockGenerator:
    """Deterministic API payload mock generator parameterized by schema name."""

    def generate_mock_for_schema(
        self,
        schema_name: str,
        count: int = 1,
        seed: int | None = None,
    ) -> dict[str, Any]:
        cleaned = schema_name.strip()
        if not cleaned:
            raise ValueError("schema_name must not be empty")
        if count < 1 or count > 50:
            raise ValueError("count must be between 1 and 50")

        effective_seed = (
            seed
            if seed is not None
            else int(hashlib.sha256(cleaned.encode("utf-8")).hexdigest()[:8], 16)
        )
        rng = random.Random(effective_seed)
        records = [self._build_record(cleaned, idx, rng) for idx in range(count)]

        result: dict[str, Any] = {
            "schema": cleaned,
            "mock_data": records[0],
        }
        if count > 1:
            result["items"] = records
        return result

    def _build_record(
        self, schema_name: str, index: int, rng: random.Random
    ) -> dict[str, Any]:
        lowered = schema_name.lower()
        prefix = lowered[:3] if len(lowered) >= 3 else "obj"
        uid = f"{prefix}_{rng.randint(1000, 9999)}_{index + 1}"

        if "order" in lowered:
            return {
                "id": uid,
                "status": rng.choice(["pending", "paid", "shipped"]),
                "amount_cents": rng.randint(500, 50000),
                "currency": "USD",
            }
        if "product" in lowered or "item" in lowered:
            return {
                "id": uid,
                "sku": f"SKU-{rng.randint(100, 999)}",
                "in_stock": rng.choice([True, False]),
                "price_cents": rng.randint(199, 19900),
            }
        return {
            "id": uid,
            "name": f"{schema_name} Sample {index + 1}",
            "email": f"{lowered}.{index + 1}@example.test",
            "active_subscriptions": ["Pro_Plan_2026"],
        }
