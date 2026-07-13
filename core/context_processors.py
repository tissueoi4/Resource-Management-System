def user_roles(request):
    is_admin = False
    if request.user.is_authenticated:
        # roleフィールドで判定するように統一！
        is_admin = request.user.is_superuser or request.user.role == 'ADMIN'
    
    return {
        'is_admin': is_admin,
    }