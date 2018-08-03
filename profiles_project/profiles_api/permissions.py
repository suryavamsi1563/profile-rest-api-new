from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit or load profiles"""
    def has_object_permission(self,request,view,obj):
        """Check users trying to edit thier own profile"""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id

class PostOwnStatus(permissions.BasePermission):
    """Allows users to update thier own status"""
    def has_object_permission(self,request,view,obj):
        """Check users trying to edit thier own profile"""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile.id == request.user.id