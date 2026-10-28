from rest_framework import permissions
from .services import MembershipService
from .models import SecurityLog


class IsProjectAdminOrReadOnly(
    permissions.BasePermission
):
    """
    Cualquier miembro puede leer.
    Solo un admin puede modificar.
    """

    def has_object_permission(
        self,
        request,
        view,
        obj
    ):
        project = (
            obj.project
            if hasattr(obj, "project")
            else obj
        )

        if request.method in permissions.SAFE_METHODS:
            return MembershipService.is_member(
                request.user,
                project
            )

        is_admin = MembershipService.is_admin(
            request.user,
            project
        )

        if not is_admin:
            SecurityLog.objects.create(
                user=request.user,
                action="permission_denied",
                detail=f"Intentó modificar proyecto {project.id}",
            )

        return is_admin