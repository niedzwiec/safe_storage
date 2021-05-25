class SafeUserAgentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.user.last_user_agent = request.META.get('HTTP_USER_AGENT', 'no user agent')
            request.user.save()
        response = self.get_response(request)
        return response
