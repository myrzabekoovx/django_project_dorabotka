def user_context(request):
    return {
        'current_user': request.user
    }