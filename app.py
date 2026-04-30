from data.sql_data_collector import extract_pgres
from shiny import App, ui
from server import server

card_style = """
background-color: #f4f9fd;
padding: 20px;
border-radius: 16px;
box-shadow: 0 2px 6px rgba(0,0,0,0.08);
"""

_df = extract_pgres()
county_choices = sorted(_df["county_name"].dropna().unique())

app_ui = ui.page_fluid(
    
    ui.tags.style("""
        .app-container { max-width: 1400px; margin-left: auto; margin-right: auto; padding: 12px; }
        .card { margin-bottom: 18px; }
    """),

    # Header
    ui.div(
        ui.h3("Prison Population Dashboard", style="margin-top: 8px; margin-bottom: 12px;"),
        ui.p("Interactive dashboard for the IDOC dataset.", style="margin-top:0; color: #666;"),
        class_="app-container",
    ),

    


    # Sidebar + main layout
    ui.page_sidebar(
        # 1) Sidebar (must be a ui.sidebar(...) instance)
        ui.sidebar(
            ui.h4("Filters", style="margin-top:0;"),
            ui.input_select("year", "Year", choices=[2020, 2021, 2022], selected=2022),
            ui.input_select("sex", "Sex", choices=["All", "Male", "Female"], selected="All"),
            ui.input_slider("age", "Age", 18, 80, value=30),
            width=3,
        ),

        # 2) Main content (just put components here, no panel_main, no main=)
        ui.row(
            ui.column(
                12,
                ui.div(
                    ui.h5("Trend by Race", style="margin-top:0;"),
                    ui.output_plot("line_graph"),
                    class_="card",
                    style=card_style,
                )
            )
        ),

        ui.row(
            ui.column(
                6,
                ui.div(
                    ui.h5("By Sex", style="margin-top:0;"),
                    ui.output_plot("sex_bar"),
                    class_="card",
                    style=card_style,
                )
            ),
            ui.column(
                6,
                ui.div(
                    ui.h5("By Race", style="margin-top:0;"),
                    ui.output_plot("race_bar"),
                    class_="card",
                    style=card_style,
                )
            )
        ),

        ui.row(
            ui.column(
                12,
                ui.div(
                    ui.h5("Data (sample)", style="margin-top:0;"),
                    ui.output_ui("table"),
                    class_="card",
                    style=card_style,
                )
            )
        )
    )
)

app = App(app_ui, server)
