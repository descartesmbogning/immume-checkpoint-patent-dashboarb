# Import required libraries
from components import Navbar, Footer
from dash import dcc, html, Input, Output, dash_table, callback, State, callback_context, no_update
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate
import numpy as np
from dash.dash_table.Format import Format, Scheme

# Load your data
df = pd.read_csv('./data/applicant_table.csv')
df_trend = pd.read_csv('./data/applicant_year_table.csv')

# Drop 'Unnamed: 0' column if it exists
if 'Unnamed: 0' in df.columns:
    df = df.drop(columns=['Unnamed: 0'])

## Define helper functions for dynamic content (Placeholder content for now)
def get_total_applicant():
    return str(df['Applicant'].count())

layout = dbc.Container([
    Navbar(),  # Include navbar at the top
    dbc.Row(dbc.Col(html.H1("Applicants"), width={'size': 6, 'offset': 3}, className="text-center mt-1 mb-2")),
    dbc.Row([
        dbc.Col(html.P("Applicant: The applicant is the organization or individual that files the patent application. This could be the original inventor, or it could be the assignee."), width={'size': 10, 'offset': 0}, className="d-flex justify-content-center"),
        dbc.Col(html.P("Explore the contributions of key applicants in the field of immune checkpoint therapy."), width={'size': 10, 'offset': 0}, className="d-flex justify-content-center"),
        dbc.Col(html.P("Use the table below to sort, filter, and understand the landscape of patent contributions."), width={'size': 10, 'offset': 0}, className="d-flex justify-content-center")
        ], className="mb-2 d-flex justify-content-center"
    ),    
     # Key Metrics in Cards
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total Applicants", className="card-title"),
                html.P(get_total_applicant(), className="card-text")
            ])
        ]), className="text-center mt-1 mb-1", width=4),
        # dbc.Col(dbc.Card([
        #     dbc.CardBody([
        #         html.H5("Top Inventor", className="card-title"),
        #         html.P(get_top_inventor(), className="card-text")
        #     ])
        # ]), width=4),
        # # ... Add more cards as needed ...
    ], className="mb-2 d-flex justify-content-center"),


    # Buttons for downloading data
    dbc.Row([
        dbc.Col(html.Button("Download Full Data", id="btn_download_full_applicant"), width={'size': 2, 'offset': 0}),
        dbc.Col(html.Button("Download Selected Data", id="btn_download_selected_applicant"), width=2),
    ], justify="start", className="mb-0"),
    
    # Data Table
    dash_table.DataTable(
        id='applicant-datatable-interactivity',
        columns=[
            {
                "name": f"{i} (use: >, <, =)" if df[i].dtype in [np.float64, np.int64] else i,
                "id": i,
                "type": "numeric",
                "format": Format(precision=4, scheme=Scheme.decimal_or_exponent) if df[i].dtype in [np.float64, np.int64] else None
            } for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        page_action="native",
        page_current= 0,
        page_size= 10,
        style_table={'height': '400px', 'overflowY': 'auto'},
        style_cell={
            'height': 'auto',
            'minWidth': '80px', 'width': '120px', 'maxWidth': '180px',
            'whiteSpace': 'normal'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        }
    ),
    
    # Place the metric dropdown right above the Data Table
    dbc.Row(
        [
            dbc.Col(html.Label("Select Metric:"), width=2),
            dbc.Col(
                dcc.Dropdown(
                    id='applicant-metric-dropdown',
                    options=[
                        {'label': 'Patent Count', 'value': 'Patent Count'},
                        {'label': 'Total Citations', 'value': 'Total Citations'},
                        {'label': 'Degree Centrality', 'value': 'Degree Centrality'},
                        {'label': 'Betweenness Centrality', 'value': 'Betweenness Centrality'},
                        {'label': 'Duration (Years)', 'value': 'Duration (Years)'}
                    ],
                    value='Patent Count'  # default value
                ),
                width=3
            ),
        ],
        className="mb-0  d-flex justify-content-center"
    ),
    
    # Placeholder for Bar Chart
    dbc.Row(dbc.Col(dcc.Graph(id='applicant-bar-chart'), width=12)),
################### update on 30/03/2024
    # Add a Row for the Google search link
    dbc.Row(
        dbc.Col(
            html.A(
                id='google-search-link-applicant', 
                children='Click on an applicant to search', 
                href='', 
                target='_blank',
                style={'display': 'block', 'margin': '20px 0', 'textAlign': 'center'}
            ), 
            width={"size": 6, "offset": 3}
        )
    ),

    # Add a Row for the Google patent search link
    dbc.Row(
        dbc.Col(
            html.A(
                id='google-search-link-applicant-patent', 
                children='Click on an applicant to search patents', 
                href='', 
                target='_blank',
                style={'display': 'block', 'margin': '20px 0', 'textAlign': 'center'}
            ), 
            width={"size": 6, "offset": 3}
        )
    ),

#     # Add a Row for the espacenet patent search link
#     dbc.Row(
#         dbc.Col(
#             html.A(
#                 id='google-search-link-applicant-patent-espacenet', 
#                 children='Click on an applicant to search espacenet patents', 
#                 href='', 
#                 target='_blank',
#                 style={'display': 'block', 'margin': '20px 0', 'textAlign': 'center'}
#             ), 
#             width={"size": 6, "offset": 3}
#         )
#     ),
# ##################
    # Placeholder for Line Chart
    dbc.Row(dbc.Col(dcc.Graph(id='applicant-line-chart'), width=12)),

    dbc.Row([
        dbc.Col(dcc.Link(
            html.Div([
                html.Img(src='/assets/applicant_VOSviewer-screenshot.png', style={'max-width': '100%', 'max-height': '600px', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'}),
                # html.P("Inventors")
            ]),
            target='_blank',  # Opens the link in a new tab
            href='http://tinyurl.com/263xb4pv'
        ), width={"size": 8, "offset": 1}, className="d-flex justify-content-center mt-5 mb-5"),  
    ], className="mb-2 d-flex justify-content-center"),

    # dbc.Row(
    #     dbc.Col(
    #         html.Iframe(
    #             src="http://tinyurl.com/263xb4pv",
    #             style={
    #                 "border": "1px solid #ddd",
    #                 "width": "100%",  # Adjust width as needed
    #                 "height": "500px",  # Adjust height as needed
    #                 "display": "block",
    #                 "margin-left": "auto",
    #                 "margin-right": "auto"
    #             },
    #             allow="fullscreen",  # This enables fullscreen mode
    #         ),
    #         width=12,  # Adjust the column width as needed
    #     )
    # ),

    # Hidden Div for storing JSON-serialized data (full and selected)
    html.Div(id='applicant-data-storage-full', style={'display': 'none'}),
    html.Div(id='applicant-data-storage-selected', style={'display': 'none'}),
    # html.Div([
    # dcc.Location(id='url', refresh=False),
    # # Your layout components here
    # ]),
    # Hidden element for triggering downloads
    dcc.Download(id="applicant-download-dataframe-csv"),
    Footer()  # Include footer at the bottom


], fluid=True)

# # Callbacks for the Applicant page
# @callback(
#     Output('applicant-bar-chart', 'figure'),
#     [Input('applicant-datatable-interactivity', 'selected_rows'),
#      Input('applicant-metric-dropdown', 'value')]  # Input from the dropdown
# )
# def update_applicant_bar_chart(selected_rows, selected_metric):
#     if selected_rows is None or len(selected_rows) == 0:
#         # Sort the DataFrame by the selected metric and take the top 20
#         filtered_df = df.sort_values(selected_metric, ascending=False).head(20)
#         title = f'Top 20 Applicants by {selected_metric}'
#     else:
#         filtered_df = df.iloc[selected_rows]
#         # Even when specific applicants are selected, sort them by the selected metric
#         filtered_df = filtered_df.sort_values(selected_metric, ascending=False)
#         title = f'Selected Applicants by {selected_metric}'

#     # Plotting the bar chart
#     fig = px.bar(filtered_df, x="Applicant", y=selected_metric, color="2023 Classification", barmode="group",
#                  category_orders={"Applicant": filtered_df["Applicant"]})  # Ensure consistent ordering
#     fig.update_layout(title=title)
#     return fig
####
# Callbacks for the Applicant page
@callback(
    Output('applicant-bar-chart', 'figure'),
    [Input('applicant-datatable-interactivity', 'derived_virtual_data'),
     Input('applicant-datatable-interactivity', 'derived_virtual_selected_rows'),
     Input('applicant-metric-dropdown', 'value')]  # Input from the dropdown
)
def update_applicant_bar_chart(rows, derived_virtual_selected_rows, selected_metric):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    # When the table is first loaded and there's no filtering or sorting, use original data
    dff = pd.DataFrame(rows) if rows is not None else df

    if len(derived_virtual_selected_rows) == 0:
        # Sort the DataFrame by the selected metric and take the top 20
        filtered_df = dff.sort_values(selected_metric, ascending=False).head(20)
        title = f'Top 20 Applicants by {selected_metric}'
    else:
        filtered_df = dff.iloc[derived_virtual_selected_rows]
        # Even when specific applicants are selected, sort them by the selected metric
        filtered_df = filtered_df.sort_values(selected_metric, ascending=False)
        title = f'Selected Applicants by {selected_metric}'

    # Plotting the bar chart
    # fig = px.bar(filtered_df, x="Applicant", y=selected_metric, color="2023 Classification", barmode="group",
    #              category_orders={"Applicant": filtered_df["Applicant"].tolist()})  # Ensure consistent ordering
    # fig.update_layout(title=title)
    fig = px.bar(filtered_df, x="Applicant", y=selected_metric, color="2023 Classification",
             hover_data=[selected_metric, 'First Year', 'Last Year','Mean Patents/Year'],
             barmode="group",
             category_orders={"Applicant": filtered_df["Applicant"].tolist()})  # Ensure consistent ordering
             
    fig.update_traces(hovertemplate="Applicant: %{x}<br>" + selected_metric + ": %{y}<br>First Year: %{customdata[0]}<br>Last Year: %{customdata[1]}<br>Mean Patents/Year: %{customdata[2]}")
    fig.update_layout(title=title)
    return fig

# ... (other callbacks)
################### update on 30/03/2024
from urllib.parse import quote_plus  # For URL encoding

@callback(
    Output('google-search-link-applicant', 'href'),  # Update the link's href
    Output('google-search-link-applicant', 'children'),  # Optionally update the link text to make it clear
    Input('applicant-bar-chart', 'clickData'),  # Listen to clicks on the bar chart
    prevent_initial_call=True
)
def update_google_search_link(clickData):
    if clickData is None:
        # If no bar is clicked, don't update the link
        return no_update, no_update
    applicant_name = clickData['points'][0]['x']
    search_query = f"{applicant_name} immune checkpoint"
    search_url = f"https://www.google.com/search?q={quote_plus(search_query)}"
    link_text = f"Search for {applicant_name} in immune checkpoint"
    return search_url, link_text
######################""
######################""
from urllib.parse import quote_plus  # For URL encoding

@callback(
    Output('google-search-link-applicant-patent', 'href'),
    Output('google-search-link-applicant-patent', 'children'),
    Input('applicant-bar-chart', 'clickData'),
    prevent_initial_call=True
)
def update_patent_search_link(clickData):
    if clickData is None:
        return no_update, no_update
    applicant_name = clickData['points'][0]['x']
    # Constructing the query
    search_query = f"assignee:\"{applicant_name}\" AND TAC=('checkpoint inhibitor' OR 'Immune Checkpoint' OR 'anti-pd' OR 'PD-L1')"
    # For Google Patents
    search_url = f"https://patents.google.com/?q={quote_plus(search_query)}"
    link_text = f"Search patents for {applicant_name} with 'immune checkpoint'"
    return search_url, link_text

# # Espacenet search query
# from urllib.parse import quote_plus  # For URL encoding

# @callback(
#     Output('google-search-link-applicant-patent-espacenet', 'href'),  # Assuming this is the ID of your link element
#     Output('google-search-link-applicant-patent-espacenet', 'children'),
#     Input('applicant-bar-chart', 'clickData'),
#     prevent_initial_call=True
# )
# def update_patent_search_link(clickData):
#     if clickData is None:
#         return no_update, no_update
#     applicant_name = clickData['points'][0]['x']
#     # Constructing the Espacenet search query
#     search_keywords = "'checkpoint inhibitor' OR 'Immune Checkpoint' OR 'anti-pd' OR 'PD-L1'"
#     search_query = f"pa any \"{applicant_name}\" AND ctxt all \"{search_keywords}\""
#     # Encoding the query for URL
#     encoded_search_query = quote_plus(search_query)
#     # Constructing the URL for Espacenet
#     search_url = f"https://worldwide.espacenet.com/patent/search?q={encoded_search_query}&queryLang=en"
#     link_text = f"Search Espacenet patents for {applicant_name} with 'immune checkpoint'"
#     return search_url, link_text

####
@callback(
    Output('applicant-line-chart', 'figure'),
    [Input('applicant-datatable-interactivity', 'derived_virtual_data'),  # Get the filtered data from the table
     Input('applicant-datatable-interactivity', 'derived_virtual_selected_rows'),  # Get the selected rows from the table
     Input('applicant-bar-chart', 'clickData')]  # Get the click data from the bar chart
)
def update_applicant_line_chart(all_rows_data, slctd_row_indices, clickData):
    # Process the data from the table
    dff = pd.DataFrame(all_rows_data) if all_rows_data is not None else pd.DataFrame()
    selected_applicants = dff.iloc[slctd_row_indices]['Applicant'].tolist() if slctd_row_indices else []

    # Process the click data from the bar chart
    if clickData:
        clicked_applicant = clickData['points'][0]['x']
        if clicked_applicant not in selected_applicants:
            selected_applicants.append(clicked_applicant)

    # Aggregate data: count patents per year for each applicant
    applicant_yearly_counts = df_trend.groupby(['Application Year', 'Applicant']).size().reset_index(name='Patent Count')

    # Create the line chart
    if selected_applicants:
        filtered_df = applicant_yearly_counts[applicant_yearly_counts['Applicant'].isin(selected_applicants)]
        fig = px.line(filtered_df, x='Application Year', y='Patent Count', color='Applicant',markers=True)
        fig.update_layout(title='Contribution Trends of Selected Applicants Over Years')
    else:
        # When no applicants are selected, show the global trend
        df_trend2 = df_trend[['Lens ID','Application Year']].drop_duplicates()
        global_yearly_counts = df_trend2.groupby(['Application Year']).size().reset_index(name='Total Patents')
        fig = px.line(global_yearly_counts, x='Application Year', y='Total Patents',markers=True)
        fig.update_layout(title='Global Trend of Patent Contributions Over Years')
    
    return fig

# ... The rest of the callbacks remain similar to those in inventor_page.py, just change IDs and variables to match the context of applicants ...
from dash import Input, Output, callback

# Assuming you have already set up your Dash app and layout

# @callback(
#     [Output('nav-home', 'className'), Output('nav-inventors', 'className'),
#      Output('nav-applicants', 'className'), Output('nav-applicant-countries', 'className'),
#      Output('nav-jurisdictions', 'className')],
#     [Input('url', 'pathname')]
# )
# def update_nav_active(pathname):
#     if pathname == '/':
#         return 'nav-link active', 'nav-link', 'nav-link', 'nav-link', 'nav-link'
#     elif pathname == '/inventor':
#         return 'nav-link', 'nav-link active', 'nav-link', 'nav-link', 'nav-link'
#     elif pathname == '/applicants':
#         return 'nav-link', 'nav-link', 'nav-link active', 'nav-link', 'nav-link'
#     elif pathname == '/applicants_countries':
#         return 'nav-link', 'nav-link', 'nav-link', 'nav-link active', 'nav-link'
#     elif pathname == '/jurisdiction':
#         return 'nav-link', 'nav-link', 'nav-link', 'nav-link', 'nav-link active'
#     # Add more elif blocks as needed for additional pages
#     else:
#         # Default case if no path matches
#         return 'nav-link', 'nav-link', 'nav-link', 'nav-link', 'nav-link'

@callback(
    [Output('applicant-data-storage-full', 'children'),
     Output('applicant-data-storage-selected', 'children')],
    [Input('applicant-datatable-interactivity', 'derived_virtual_data'),
     Input('applicant-datatable-interactivity', 'derived_virtual_selected_rows')]
)
def store_applicant_data(all_rows_data, slctd_row_indices):
    if all_rows_data is None:
        raise PreventUpdate
    
    # Store full data
    full_data_str = pd.DataFrame(all_rows_data).to_json(date_format='iso', orient='split')

    # Store selected data
    if slctd_row_indices is None or len(slctd_row_indices) == 0:
        selected_data_str = None
    else:
        selected_data_str = pd.DataFrame([all_rows_data[i] for i in slctd_row_indices]).to_json(date_format='iso', orient='split')
    
    return full_data_str, selected_data_str

@callback(
    Output("applicant-download-dataframe-csv", "data"),
    [Input("btn_download_full_applicant", "n_clicks"),
     Input("btn_download_selected_applicant", "n_clicks"),
     Input('applicant-data-storage-full', 'children'),
     Input('applicant-data-storage-selected', 'children')],
    prevent_initial_call=True,
)
def download_applicant_csv(btn_full, btn_selected, full_data_str, selected_data_str):
    ctx = callback_context

    if not ctx.triggered:
        return dash.no_update
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == "btn_download_full_applicant":
        df = pd.read_json(full_data_str, orient='split')
        return dcc.send_data_frame(df.to_csv, filename="full_data_applicant.csv")
    elif button_id == "btn_download_selected_applicant":
        if selected_data_str:
            df = pd.read_json(selected_data_str, orient='split')
            return dcc.send_data_frame(df.to_csv, filename="selected_data_applicant.csv")
    return no_update

if __name__ == '__main__':
    app.run_server(debug=True)
