# from django.utils.deprecation import MiddlewareMixin

# class ContentSecurityPolicyMiddleware(MiddlewareMixin):
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
#         response['Content-Security-Policy'] = "default-src 'self'"
#         return response
