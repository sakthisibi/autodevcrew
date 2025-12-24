"""
AutoDevCrew Integrations Module

This module contains integrations with external platforms like
GitHub, GitLab, Bitbucket, and CI/CD systems.
"""

from .github_integration import GitHubIntegration

__all__ = [
    'GitHubIntegration'
]
