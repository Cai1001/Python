from AutoComments.mymiddlewares import resource

p = resource.CookiesMiddleware()

print(p.get_ip())