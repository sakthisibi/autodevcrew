"""
AutoDevCrew Core Module

This module contains core functionality for privacy management,
lightweight mode optimization, and cloud deployment.
"""

from .privacy_manager import PrivacyManager, PrivacyLevel, DataRetentionPolicy
from .lightweight_mode import LightweightMode, HardwareProfile, QuantizationLevel
from .cloud_deployer import CloudDeployer, DeploymentConfig

__all__ = [
    'PrivacyManager',
    'PrivacyLevel',
    'DataRetentionPolicy',
    'LightweightMode',
    'HardwareProfile',
    'QuantizationLevel',
    'CloudDeployer',
    'DeploymentConfig'
]
