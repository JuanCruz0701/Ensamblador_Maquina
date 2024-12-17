import flet as ft
from flet_route import Params, Basket

def Ejemplos(page: ft.Page, params: Params, basket: Basket):

    texto_estilo = ft.TextStyle(
                color=ft.colors.BLACK,
                font_family="Arial",
                letter_spacing=1.5,
                ) 

    textoEjemplos = ft.Text(
        value="     EJEMPLOS DE USO\n              ",
        style=texto_estilo
    )

    EjemplosImagen = ft.Image(
        src="assets/imagenes/ejemplo1.jpg",
        width=356,
        height=253,
        fit=ft.ImageFit.CONTAIN,
    )
    EjemplosImagenSalida = ft.Image(
        src="assets/imagenes/salida1.png",
        width=356,
        height=253,
        fit=ft.ImageFit.CONTAIN,
    )
    
    return ft.View(
        "/ejemplos",
        controls=[
            ft.Container(
                content=ft.Row(
                    [        
                        ft.IconButton(
                            icon=ft.icons.HOME,
                            icon_color=ft.colors.BLUE,
                            tooltip="INICIO",
                            on_click=lambda _: page.go("/")
                        ),                                  
                    ]
                ),
                width=450,
                height=40,
                bgcolor=ft.colors.GREY_900,
                alignment=ft.alignment.center,
                
            ),
             ft.Container(
                content=ft.Column(
                    [
                        textoEjemplos,
                        EjemplosImagen,
                        EjemplosImagenSalida  
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                margin=ft.margin.only(top=0, bottom=70),
                padding=ft.padding.all(10), 
                width=450, 
                height=600, 
                bgcolor=ft.colors.GREY_800, 
                alignment=ft.alignment.top_center,  
                
            )
            
        ]
    )