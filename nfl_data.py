import nfl_data_py as nfl
from dash import Dash, html, dash_table, dcc, callback, Output, Input


nfl_draft = nfl.import_combine_data(
    [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]).drop(
    ['season', 'pfr_id', 'cfb_id', 'ht', 'wt', 'forty', 'bench', 'vertical', 'broad_jump', 'cone', 'shuttle'], axis=1)
combine_data = nfl.import_combine_data(
    [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]).drop(
    ['season', 'pfr_id', 'cfb_id'], axis=1)

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1('NFL DRAFT AND COMBINE RESULTS')
    ], style={'textAlign': 'center', 'margin': 'auto'}),
    html.Div([
        html.P('Explore NFL Draft and Combine insights from the years 2010 to 2023'),
        html.P('Select a draft year and round to view a detailed chart of draft and combine results for players. '
               'Information includes key performance metrics from the combine, team selections, physical attributes '
               'and more.')
    ]),
    html.Br(),
    html.Div([
        html.Button("Draft Info", id='draft-info-ctx',
                    style={'width': '140px', 'height': '35px', 'border-radius': '5px', 'margin-right': '10px'}),
        html.Button("Combine Results", id='combine-results-ctx',
                    style={'width': '140px', 'height': '35px', 'border-radius': '5px', 'margin-bottom': '10px'}),
        html.Br(),
        dcc.Dropdown(options=[
            {'label': 2010, 'value': 2010},
            {'label': 2011, 'value': 2011},
            {'label': 2012, 'value': 2012},
            {'label': 2013, 'value': 2013},
            {'label': 2014, 'value': 2014},
            {'label': 2015, 'value': 2015},
            {'label': 2016, 'value': 2016},
            {'label': 2017, 'value': 2017},
            {'label': 2018, 'value': 2018},
            {'label': 2019, 'value': 2019},
            {'label': 2020, 'value': 2020},
            {'label': 2021, 'value': 2021},
            {'label': 2022, 'value': 2022},
            {'label': 2023, 'value': 2023}
        ], placeholder='Select Year', id='year-selection', style={'width': '65%'}),
        dcc.Dropdown(options=[
            {'label': 'Round 1', 'value': 1},
            {'label': 'Round 2', 'value': 2},
            {'label': 'Round 3', 'value': 3},
            {'label': 'Round 4', 'value': 4},
            {'label': 'Round 5', 'value': 5},
            {'label': 'Round 6', 'value': 6},
            {'label': 'Round 7', 'value': 7},
        ], id='round-selection', style={'width': '65%'}, placeholder='Select Round')
    ]),
    html.Br(),
    html.Div([
        dash_table.DataTable(
            data=[], id='create-table', page_size=20,
            style_header={'fontWeight': 'bold', 'textAlign': 'center', 'padding': '5px'},
            style_data={'textAlign': 'center'},
            style_table={'width': '90%', 'margin': 'auto'}
        )
    ])
], style={'fontFamily': 'Monospace'})


@callback(
    Output(component_id='create-table', component_property='data', allow_duplicate=True),
    Input(component_id='draft-info-ctx', component_property='n_clicks'),
    Input(component_id='year-selection', component_property='value'),
    Input(component_id='round-selection', component_property='value'),
    config_prevent_initial_callbacks=True)
def update_table_draft_info(draft_btn, year, round):
    column_names = {'player_name': 'Player Name', 'pos': 'Position', 'draft_ovr': 'Overall', 'draft_team': 'Team',
                    'school': 'School'}
    players = nfl_draft[(nfl_draft['draft_year'] == year) & (nfl_draft['draft_round'] == round)].sort_values(
        by=['draft_ovr'])
    format_players = players[['draft_ovr', 'player_name', 'pos', 'draft_team', 'school']].rename(columns=column_names)
    table = format_players.to_dict('records')
    return table


@callback(
    Output(component_id='create-table', component_property='data', allow_duplicate=True),
    Input(component_id='combine-results-ctx', component_property='n_clicks'),
    Input(component_id='year-selection', component_property='value'),
    Input(component_id='round-selection', component_property='value'),
    config_prevent_initial_callbacks=True)
def update_table_combine_results(combine_btn, year, round):
    column_names = {'player_name': 'Player Name', 'pos': 'Position', 'ht': 'Height', 'wt': 'Weight', 'forty': 'Forty',
                    'bench': 'Bench', 'vertical': 'Vertical', 'broad_jump': 'Broad Jump', 'cone': 'Cone',
                    'shuttle': 'Shuttle'}
    players = combine_data[(combine_data['draft_year'] == year) & (combine_data['draft_round'] == round)].sort_values(
        by=['draft_ovr'])
    format_players = players[
        ['player_name', 'pos', 'ht', 'wt', 'forty', 'bench', 'vertical', 'broad_jump', 'cone', 'shuttle']].rename(
        columns=column_names).fillna("--")
    table = format_players.to_dict('records')
    return table


if __name__ == '__main__':
    app.run_server(debug=True)
