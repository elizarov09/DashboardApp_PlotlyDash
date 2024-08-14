# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("/Users/olegelizarov/Documents/GitHub/DashboardApp_PlotlyDash/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # ЗАДАЧА 1: Добавить раскрывающийся список для выбора стартовой площадки
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                 ],
                 value='ALL',
                 placeholder="Select a Launch Site",
                 searchable=True
                 ),
    html.Br(),

    # ЗАДАЧА 2: Добавить круговую диаграмму для отображения успешных запусков
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # ЗАДАЧА 3: Добавить ползунок для выбора диапазона полезной нагрузки
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0', 10000: '10000'},
                    value=[min_payload, max_payload]),

    # ЗАДАЧА 4: Добавить диаграмму рассеяния для отображения корреляции между полезной нагрузкой и успешными запусками
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])


# ЗАДАЧА 2: Добавляем функцию обратного вызова для круговой диаграммы
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Фильтр по всем сайтам и создание круговой диаграммы
        fig = px.pie(spacex_df, values='class',
                     names='Launch Site',
                     title='Total Success Launches By Site')
    else:
        # Фильтр по выбранному сайту и создание круговой диаграммы успехов/неудач
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df,
                     names='class',
                     title=f'Total Success Launches for site {selected_site}')

    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# ЗАДАЧА 4: Добавляем функцию обратного вызова для диаграммы рассеяния
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
        ]

    if selected_site == 'ALL':
        # Если выбраны все сайты, то отображаем все данные в пределах выбранного диапазона полезной нагрузки
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title='Correlation between Payload and Success for all Sites')
    else:
        # Если выбран конкретный сайт, то фильтруем данные по этому сайту
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title=f'Correlation between Payload and Success for site {selected_site}')

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(port=8051)
