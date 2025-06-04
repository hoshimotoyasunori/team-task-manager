from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    オブジェクトの作成者または管理者のみ編集・削除を許可
    """
    def has_object_permission(self, request, view, obj):
        # 管理者は常に許可
        if request.user and request.user.is_staff:
            return True
        # 作成者のみ許可
        return obj.creator == request.user 