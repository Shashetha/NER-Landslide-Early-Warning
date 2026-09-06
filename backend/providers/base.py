"""
Base interface for environmental data providers.

Each provider must implement get() and return a float or None.
None means "data unavailable" — the model imputer will handle it.

To add a real provider:
1. Create a subclass in this directory (e.g. open_meteo_provider.py)
2. Implement get()
3. Register it in prediction_service.py

Never hard-code API keys here. Use environment variables.
"""

from abc import ABC, abstractmethod
from typing import Optional


class RainfallProvider(ABC):
    @abstractmethod
    async def get(
        self,
        latitude: float,
        longitude: float,
    ) -> dict:
        """
        Return dict with keys: rainfall_1d, rainfall_3d, rainfall_7d (all mm).
        Return None values for any unavailable field.
        """


class TerrainProvider(ABC):
    @abstractmethod
    async def get(
        self,
        latitude: float,
        longitude: float,
    ) -> dict:
        """
        Return dict with keys: elevation_m (m), slope_degrees (°).
        Return None values for any unavailable field.
        """


class SoilMoistureProvider(ABC):
    @abstractmethod
    async def get(
        self,
        latitude: float,
        longitude: float,
    ) -> Optional[float]:
        """
        Return soil moisture as a FRACTION (0–1, volumetric m³/m³).
        Return None if unavailable.
        """
