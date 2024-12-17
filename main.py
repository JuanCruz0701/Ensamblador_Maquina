import flet as ft
from flet_route import Routing, path
from Vista import compiler_view
from Ejemplo import Ejemplos

def main(page: ft.Page):
    # Configuración de las rutas
    app_routes = [
        path(url="/", clear=True, view=compiler_view),
        path(url="/ejemplos", clear=True, view=Ejemplos)
    ]

    Routing(page=page, app_routes=app_routes)
    page.go(page.route)

ft.app(target=main)
