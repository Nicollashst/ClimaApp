import flet as ft
import requests
from datetime import datetime
import pytz

def main(page: ft.Page):
    page.title = "WorkNet"
    page.window_width = 400
    page.window_height = 700
    page.padding = 20
    page.bgcolor = ft.colors.BLACK
    page.scroll = "auto"

    # Widgets
    cidade_input = ft.TextField(
        label="Digite a cidade",
        width=290,
        filled=True,
        bgcolor=ft.colors.BLUE_GREY_800,
        color=ft.colors.WHITE,
        border_radius=20,
    )

    cidade_label = ft.Text(size=28, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
    data_label = ft.Text(size=18, color=ft.colors.WHITE70)
    temperatura_label = ft.Text(size=50, weight=ft.FontWeight.BOLD, color=ft.colors.LIGHT_BLUE_ACCENT)
    temperatura_simbolo_label = ft.Text("°C", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.LIGHT_BLUE_ACCENT)
    umidade_label = ft.Text(size=50, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_ACCENT)
    umidade_simbolo_label = ft.Text("%", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_ACCENT)
    umidade_nome_label = ft.Text("Umidade", size=14, color=ft.colors.WHITE70)
    pressao_label = ft.Text(size=16, color=ft.colors.WHITE70)
    velocidade_label = ft.Text(size=16, color=ft.colors.WHITE70)
    descricao_label = ft.Text(size=18, color=ft.colors.LIGHT_BLUE_ACCENT)
    icon_image = ft.Image(width=100, height=100)
    coordenadas_label = ft.Text(size=16, color=ft.colors.WHITE70)
    temp = ft.Text("Temperatura", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.LIGHT_BLUE_ACCENT)
    umi = ft.Text("Umidade", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_ACCENT)

    def obter_clima(e):
        cidade = cidade_input.value
        if not cidade:
            return

        weather_key = '841824f2fcf9610b810d97e88b4f00b3'
        api_link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={weather_key}&lang=pt&units=metric"

        try:
            r = requests.get(api_link)
            data = r.json()

            pais_codigo = data["sys"]["country"]
            zona_fuso = pytz.country_timezones[pais_codigo]
            pais = pytz.country_names[pais_codigo]
            zona = pytz.timezone(zona_fuso[0])
            zona_horas = datetime.now(zona).strftime("%d/%m/%Y | %H:%M:%S")
            temperatura = data["main"]["temp"]
            pressao = data["main"]["pressure"]
            umidade = data["main"]["humidity"]
            velocidade = data["wind"]["speed"]
            descricao = data["weather"][0]["description"]
            coordenadas = data["coord"]

            # Atualizando dados
            cidade_label.value = f"{cidade} - {pais}"
            data_label.value = zona_horas
            temperatura_label.value = f"{temperatura:.1f}"
            umidade_label.value = f"{umidade}"
            pressao_label.value = f"Pressão: {pressao} hPa"
            velocidade_label.value = f"Vento: {velocidade} m/s"
            descricao_label.value = descricao.capitalize()
            coordenadas_label.value = f"Coordenadas: {coordenadas}"

            # Atualiza imagem e cor de fundo
            hora = int(datetime.now(zona).strftime("%H"))
            if hora <= 5 or hora > 18:
                icon_image.src = "imagens/noite.png"
                page.bgcolor = ft.colors.BLUE_GREY_900
            else:
                icon_image.src = "imagens/sol_dia.png"
                page.bgcolor = ft.colors.LIGHT_BLUE_200

            # Altera cor da temperatura
            temperatura_label.color = ft.colors.RED if temperatura >= 30 else ft.colors.LIGHT_BLUE_ACCENT

            page.update()

        except Exception:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Cidade não encontrada, digite novamente!", color=ft.colors.WHITE),
                bgcolor=ft.colors.RED_800,
            )
            page.snack_bar.open = True
            page.update()

    ver_clima_button = ft.ElevatedButton(
        text="Ver clima",
        width=290,
        bgcolor=ft.colors.BLUE_700,
        color=ft.colors.WHITE,
        on_click=obter_clima
    )

    # Layout
    page.add(
        ft.Column(
            [
                ft.Text("🌍 Previsão do Tempo", size=28, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
                cidade_input,
                ver_clima_button,
                ft.Container(height=20),
                ft.Container(
                    content=ft.Column(
                        [
                            cidade_label,
                            data_label,
                            ft.Row([temp, temperatura_label, temperatura_simbolo_label], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Row([umi, umidade_label, umidade_simbolo_label], alignment=ft.MainAxisAlignment.CENTER),
                            umidade_nome_label,
                            pressao_label,
                            velocidade_label,
                            descricao_label,
                            coordenadas_label,
                            icon_image,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    border_radius=16,
                    padding=25,
                    bgcolor=ft.colors.BLUE_GREY_800,
                    width=320,
                    shadow=ft.BoxShadow(blur_radius=12, spread_radius=5, color=ft.colors.BLACK26)
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
