"""
InsightBI AI — Role-Based Access Control (RBAC) Module (backend/app/core/rbac.py)
Enforces granular role permissions (Admin, Executive, Analyst, Viewer).
"""

from typing import List, Dict, Set
from fastapi import Depends, HTTPException, status
from backend.app.core.security import get_current_user

# Role-to-Permissions Mapping Matrix
ROLE_PERMISSIONS: Dict[str, Set[str]] = {
    "Admin": {
        "read:kpis", "read:trends", "read:products", "read:customers", "read:forecast",
        "export:pdf", "export:csv", "execute:copilot", "manage:users", "admin:write"
    },
    "Executive": {
        "read:kpis", "read:trends", "read:products", "read:customers", "read:forecast",
        "export:pdf", "export:csv", "execute:copilot"
    },
    "Analyst": {
        "read:kpis", "read:trends", "read:products", "read:customers", "read:forecast",
        "export:csv", "execute:copilot"
    },
    "Viewer": {
        "read:kpis", "read:trends"
    }
}

class PermissionChecker:
    def __init__(self, required_permission: str):
        self.required_permission = required_permission

    def __call__(self, current_user: dict = Depends(get_current_user)) -> dict:
        user_role = current_user.get("role", "Viewer")
        user_permissions = ROLE_PERMISSIONS.get(user_role, set())

        if self.required_permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access Denied: Role '{user_role}' lacks required permission '{self.required_permission}'"
            )
        return current_user

def require_permission(permission: str):
    return PermissionChecker(permission)
