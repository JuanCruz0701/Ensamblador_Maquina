import flet as ft
from flet_route import Params, Basket
from vistas.EaM import Compiler  # Importamos el compilador ensamblador

def compiler_view(page: ft.Page, params: Params, basket: Basket):
    # Configuración de la ventana
    page.window_width = 490
    page.window_height = 710
    page.window_center()
    # Instancia del compilador
    compiler = Compiler()
    # Estilos de texto
    texto_estilo = ft.TextStyle(
        color=ft.colors.BLACK,
        font_family="Arial",
        letter_spacing=1.5,
    )
    texto_estilo_titulo = ft.TextStyle(
        color=ft.colors.WHITE,
        font_family="Arial",
        letter_spacing=1.5,
    )

    # Componentes de la interfaz
    textoEnsam = ft.Container(
        content=ft.Container(
            ft.Text(
                value="CODIGO EN ENSAMBLADOR",
                style=texto_estilo_titulo
            )
        ),
        margin=ft.margin.only(top=40, bottom=70),
        alignment=ft.alignment.top_center,
        expand=True
    )
    input_code = ft.TextField(
        bgcolor=ft.colors.WHITE,
        text_style=texto_estilo,
        min_lines=8,
        max_lines=512,
        multiline=True,
        width=400,
        height=200,
        hint_text="addi $t2, $0, 1\naddi $t3, $0, $5\nadd $t4, $t2, $t3",
        value=""
    )

    entrada = ft.Container(
        content=ft.Container(input_code),
        margin=ft.margin.only(top=50, bottom=70),
        width=450,
        height=260,
        padding=ft.padding.all(10),
        alignment=ft.alignment.top_center,
        expand=True
    )

    textoMaqui = ft.Container(
        content=ft.Container(
            ft.Text(
                value="CODIGO MAQUINA",
                style=texto_estilo_titulo
            )
        ),
        margin=ft.margin.only(top=330, bottom=70),
        alignment=ft.alignment.top_center
    )

    output_code = ft.TextField(
        bgcolor=ft.colors.WHITE,
        text_style=texto_estilo,
        min_lines=8,
        max_lines=512,
        multiline=True,
        width=400,
        height=200,
        read_only=True,
        hint_text="ACÁ SE MOSTRARÁ EL RESULTADO DE LA CONVERSION",
        value=""
    )
    error_message = ft.Text(value="", color=ft.colors.RED)

    salida = ft.Container(
        content=ft.Container(output_code),
        margin=ft.margin.only(top=340, bottom=70),
        width=450,
        height=260,
        padding=ft.padding.all(10),
        alignment=ft.alignment.top_center,
        expand=True
    )

    # Función para manejar el evento del botón
    def convert_to_machine_code(event):
        try:
            machine_code = compiler.assemble_to_machine_code(input_code.value)
            output_code.value = machine_code
            error_message.value = ""
        except Exception as e:
            error_message.value = f"Error: {e}"

        page.update()

    # Función para copiar el código al portapapeles
    def copy_to_clipboard(event):
        page.set_clipboard(output_code.value)
        page.snack_bar = ft.SnackBar(ft.Text("¡Texto copiado al portapapeles!"), open=True)
        page.update()

    # Función para guardar el archivo
    def save_file_result(e: ft.FilePickerResultEvent):
        if e.path:
            with open(e.path, "w") as file:
                file.write(output_code.value)
            page.snack_bar = ft.SnackBar(ft.Text("¡Archivo guardado correctamente!"), open=True)
        page.update()

    # Crear FilePicker para guardar archivo
    save_file_dialog = ft.FilePicker(on_result=save_file_result)
    page.overlay.append(save_file_dialog)

    # Botón para convertir el código
    convertir = ft.ElevatedButton(
        text="Convertir a Código Máquina",
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLACK,
            overlay_color=ft.colors.GREEN
        ),
        on_click=convert_to_machine_code,
    )

    # Botón para copiar el código máquina
    copiar = ft.ElevatedButton(
        text="Copiar código",
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLACK,
            overlay_color=ft.colors.GREEN
        ),
        on_click=copy_to_clipboard,
    )

    # Botón para guardar en archivo
    guardar = ft.ElevatedButton(
        text="Guardar en archivo",
        icon=ft.icons.SAVE,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLACK,
            overlay_color=ft.colors.GREEN
        ),
        on_click=lambda _: save_file_dialog.save_file(),
    )

    botonConvertir = ft.Container(
        content=ft.Row(
            controls=[convertir],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        margin=ft.margin.only(top=270, bottom=70),
        width=450,
        height=200,
        padding=ft.padding.all(10),
        alignment=ft.alignment.top_center,
        expand=True
    )

    botonCopiar = ft.Container(
        content=ft.Row(
            controls=[copiar],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        margin=ft.margin.only(top=550, bottom=70,left=250),
        width=450,
        height=200,
        padding=ft.padding.all(10),
        alignment=ft.alignment.top_center,
        expand=True
    )

    botonGuardar = ft.Container(
        content=ft.Row(
            controls=[guardar],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        margin=ft.margin.only(top=550, bottom=70,right=150),
        width=450,
        height=200,
        padding=ft.padding.all(10),
        alignment=ft.alignment.top_center,
        expand=True
    )

    stackInicio = ft.Stack([
        ft.Container(ft.Text("COMPILADOR DE ENSAMBLADOR A MAQUINA",
                              color=ft.colors.WHITE,
                              size=16,
                              weight=ft.FontWeight.BOLD,
                              text_align=ft.TextAlign.CENTER,
                              style=ft.TextStyle(
                                  font_family="Arial",
                                  letter_spacing=1.5,
                              )), margin=ft.margin.only(top=0, bottom=600),
                    padding=ft.padding.all(10),
                    width=450, height=600, bgcolor=ft.colors.GREY_800,
                    alignment=ft.alignment.top_center), textoEnsam, entrada, textoMaqui, salida, botonConvertir, botonCopiar, botonGuardar
    ])

    # Layout de la vista
    return ft.View(
        "/",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.IconButton(icon=ft.icons.AD_UNITS_SHARP, icon_color=ft.colors.BLUE,
                                      tooltip="EJEMPLOS", on_click=lambda _: page.go(f"/ejemplos"))

                    ],
                ),
                width=450,
                height=40,
                bgcolor=ft.colors.GREY_900,
                alignment=ft.alignment.top_left
            ), stackInicio
        ]
    )
