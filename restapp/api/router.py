from rest_framework.routers import DefaultRouter
from restapp.api.views import restappViewSet

router_posts = DefaultRouter()

#viewset, _ = router_posts.routes[0].mapping.items()
#print('hola routes')
#print(viewset)

router_posts.register(prefix = 'restapp', basename = 'restapp', viewset=restappViewSet)
