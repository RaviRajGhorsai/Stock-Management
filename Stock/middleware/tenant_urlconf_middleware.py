from django.conf import settings

class TenantURLConfMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("\n*** TENANT DEBUG MIDDLEWARE LOADED ***\n")
    def __call__(self, request):
        print("\n" + "="*70)
        print("REQUEST RECEIVED")
        print("="*70)
        print(f"HTTP_HOST: {request.META.get('HTTP_HOST', 'NOT SET')}")
        print(f"Path: {request.path}")
        print(f"Method: {request.method}")
        
        if hasattr(request, 'tenant'):
            print(f"\n✓ TENANT FOUND:")
            print(f"  Schema: {request.tenant.schema_name}")
            print(f"  Name: {request.tenant.name}")
            
            # Check which URLconf is being used
            if request.tenant.schema_name == 'public':
                expected_urlconf = settings.PUBLIC_SCHEMA_URLCONF
                print(f"  Expected URLconf: {expected_urlconf} (PUBLIC)")
            else:
                expected_urlconf = settings.TENANT_URLCONF
                print(f"  Expected URLconf: {expected_urlconf} (TENANT)")
            
            # Check what URLconf is actually set
            actual_urlconf = getattr(request, 'urlconf', None)
            print(f"  Actual URLconf on request: {actual_urlconf}")
            
            if actual_urlconf != expected_urlconf:
                print(f"  ⚠⚠⚠ URLconf MISMATCH! ⚠⚠⚠")
                print(f"  Forcing correct URLconf...")
                request.urlconf = expected_urlconf
        else:
            print(f"\n✗ NO TENANT!")
        
        print("="*70 + "\n")
        
        response = self.get_response(request)
        
        if response.status_code == 404:
            print("⚠ 404 NOT FOUND\n")
        
        return response

# Stock/middleware.py
# This version will print even at module load time

# from django.conf import settings

# print("\n" + "!"*70)
# print("!!! MIDDLEWARE MODULE IS BEING LOADED !!!")
# print("!"*70 + "\n")

# class TenantDebugMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         print("\n*** TENANT DEBUG MIDDLEWARE __init__ CALLED ***")
#         print("*** This should only print ONCE when server starts ***\n")
    
#     def __call__(self, request):
#         # This MUST print for EVERY request
#         host = request.META.get('HTTP_HOST', 'NO_HOST')
#         path = request.path
        
#         print(f"\n{'='*70}")
#         print(f"MIDDLEWARE CALLED: {host} {path}")
#         print(f"{'='*70}")
        
#         # Check tenant
#         if hasattr(request, 'tenant'):
#             print(f"✓ Tenant: {request.tenant.schema_name}")
            
#             # Force URLconf
#             if request.tenant.schema_name == 'public':
#                 request.urlconf = settings.PUBLIC_SCHEMA_URLCONF
#             else:
#                 request.urlconf = settings.TENANT_URLCONF
#                 print(f"  Set URLconf to: {request.urlconf}")
#         else:
#             print(f"✗ NO TENANT ATTRIBUTE!")
#             print(f"  TenantMainMiddleware did not set request.tenant")
        
#         print(f"{'='*70}\n")
        
#         response = self.get_response(request)
        
#         print(f"→ Status: {response.status_code} for {host}{path}\n")
        
#         return response