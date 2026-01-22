"""
Data loading and management utilities
"""

import json
import streamlit as st
from pathlib import Path
from typing import Dict, List, Optional


@st.cache_data
def load_stacking_data(data_path: str = "data/stacking_data.json") -> Dict:
    """
    Load stacking data from JSON file (cached)

    Args:
        data_path: Path to the JSON file

    Returns:
        Dictionary with stacking data
    """
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


class StackingDataLoader:
    """Load and manage revenue stacking data"""

    def __init__(self, data_path: str = "data/stacking_data.json"):
        self.data_path = Path(data_path)
        self._data = None

    def load_data(self) -> Dict:
        """Load the stacking data from JSON file (uses cached function)"""
        if self._data is None:
            self._data = load_stacking_data(str(self.data_path))
        return self._data

    @property
    def data(self) -> Dict:
        """Get loaded data, loading if necessary"""
        if self._data is None:
            self.load_data()
        return self._data

    def get_services(self) -> List[str]:
        """Get list of all services"""
        return self.data.get('services', [])

    def get_service_abbreviations(self) -> Dict[str, str]:
        """Get service abbreviations mapping"""
        return self.data.get('service_abbreviations', {})

    def get_compatibility(self, service1: str, service2: str, mode: str) -> Dict:
        """
        Get compatibility between two services for a specific mode

        Args:
            service1: First service name
            service2: Second service name
            mode: 'codelivery', 'splitting', or 'jumping'

        Returns:
            Dictionary with 'value' and 'color' keys
        """
        matrix = self.data.get('compatibility', {}).get(mode, {})
        if service1 in matrix and service2 in matrix[service1]:
            return matrix[service1][service2]
        return {'value': None, 'color': None}

    def get_technical_requirements(self, service_name: str) -> Dict:
        """
        Get technical requirements for a service

        Args:
            service_name: Service name (may need mapping)

        Returns:
            Dictionary of technical requirements
        """
        # Try to map service name using service_name_mapping
        tech_key = self._get_tech_requirements_key(service_name)
        return self.data.get('technical_requirements', {}).get(tech_key, {})

    def _get_tech_requirements_key(self, service_name: str) -> str:
        """Convert service name to technical requirements key"""
        mapping = self.data.get('service_name_mapping', {})
        if service_name in mapping:
            return mapping[service_name]
        # Fallback to service name as-is
        return service_name

    def check_multi_compatibility(self, services: List[str]) -> Dict:
        """
        Check compatibility among multiple services

        Args:
            services: List of service names

        Returns:
            Dictionary with compatibility results for all pairs
        """
        results = {}

        for i, service1 in enumerate(services):
            for service2 in services[i+1:]:
                pair_key = f"{service1}|{service2}"
                results[pair_key] = {
                    'codelivery': self.get_compatibility(service1, service2, 'codelivery'),
                    'splitting': self.get_compatibility(service1, service2, 'splitting'),
                    'jumping': self.get_compatibility(service1, service2, 'jumping')
                }

        return results

    def get_metadata(self) -> Dict:
        """Get metadata about the dataset"""
        return self.data.get('metadata', {})
