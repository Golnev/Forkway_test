from fastapi import FastAPI

from routers.shop import shop
from routers.admin import admin

tags_metadata = [
    {
        'name': 'Shop',
        'description': 'Operations with shop'
    },
    {
        'name': 'Admin',
        'description': 'Operations with admin panel'
    }
]

app = FastAPI(
    title='Forkway Test',
    openapi_tags=tags_metadata,
    version='0.0.1',
    contact={
        'name': 'Eugene Golnev',
        'url': 'https://www.linkedin.com/in/eugene-golnev-2b2518234/',
        'email': 'eugenegolnev1993@gmail.com'
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


# Shop router
app.include_router(router=shop.router)

# Admin router
app.include_router(router=admin.router)
