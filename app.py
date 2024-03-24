import pathlib

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

import pandas as pd
import ast
import folium
from datetime import datetime

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "الطوارئ البيئية - المركز الوطني للرقابة على الالتزام البيئي" 
server = app.server
app.config["suppress_callback_exceptions"] = True

APP_PATH = str(pathlib.Path(__file__).parent.resolve())


today=datetime.today().strftime('%d %b, %Y')




# Your Folium map generation code
initial_map=folium.Map([24.717, 44.293], zoom_start=5)
initial_map.save("maps/map.html")

tasks_data=pd.read_excel('data/tasks.xlsx')
tasks_data['Details'] = tasks_data['Details'].apply(ast.literal_eval)
notes=pd.read_excel('data/notes.xlsx')


def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-logo",
                children=[
                    html.A(
                        html.Img(id="logo", src=app.get_asset_url("NCEC_LOGO_W.png")),
                        href="https://ncec.gov.sa/",
                    ),
                ],
            ),
            html.Div(
                id="banner-text",
                children=[
                    html.H5("الطوارئ البيئية"),
                    html.H6(today+" :التاريخ "),
                ],
            ),
            
        ],
    )
 
def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab2",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Specs-tab",
                        label="التقرير",
                        value="tab3",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Map-tab",
                        label="الخريطة التفاعلية",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Control-chart-tab",
                        label="لوحة بيانات",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )




def build_tab_1():
    return [
        dcc.Loading(
        children=[
        # Manually select metrics
            html.Div(
                id="set-specs-intro-container",
                # className='twelve columns',
                children=html.Div([html.Iframe(srcDoc=open('maps/map.html', 'r', encoding='utf-8').read(), width='100%', height=650)]),
                    ),
                 ],      
        )
    ]




def build_top_panel_tab3():


    return html.Div(
        id="top-section-container",
        className="row",
        children=[
            # incident summary MOE
            html.Div(
                id="metric-summary-session",
                className="six columns",
                children=[
                    generate_section_banner("عنوان 2"),
                   
                ]
            ),
            # incident summary NCEC
            html.Div(
                id="ooc-piechart-outer",
                className="six columns",
                children=[
                    generate_section_banner("عنوان 1"),
                    html.Div(id="monthly-incidents",children=[]
                    
                             ),
                ]
            ),
        ],
    )

def convert_to_completed_tasks(data,month):
    data=data[data['Month']==month]
    completed_tasks = []
    data.reset_index(inplace=True)
    for i in range(len(data['Task'])):
        task_dict = {
            'task': data['Task'][i],
            'details': data['Details'][i]
        }
        completed_tasks.append(task_dict)
    return completed_tasks

def update_tasks(month):
    task_dt=convert_to_completed_tasks(tasks_data,month)
    return (html.Div(id="monthly-tasks",children=[
                html.Details([
                html.Summary(task['task'], dir="rtl",style={"font-size": "20px"}),
                html.Ul([html.Li(sub_detail, style={"list-style-type": "circle","direction": "rtl","text-align":"right","font-size": "15px"})for sub_detail in task['details'] ])
                            ]) for task in task_dt
                                                ]))

def update_notes(month):
    monthly_notes=notes[notes["Month"]==month]
    return(html.Div(id="monthly-notes",children= 
                    html.Ul([
                    html.Li(sub_detail, style={"padding-right":"-20px","list-style-type": "circle","direction": "rtl","text-align":"right","font-size": "20px"}) 
                        for sub_detail in monthly_notes['rnn']
                            ])                   
                    ))

def build_bot_panel_tab3():
    return html.Div(
        id="bot-section-container",
        className="row",
        children=[
            # incident summary MOE
            html.Div(
                id="metric-summary-session",
                className="eight columns",
                children=[
                    generate_section_banner("عنوان 4"),
                        html.Div(id="task-rows",children=
                        update_tasks("September"),style={"padding": "10px"})
                ]
            ),
            # notes and recommendations
            html.Div(
                id="ooc-piechart-outer",
                className="four columns",
                children=[
                    generate_section_banner("عنوان 3"),
                        html.Div(id="task-rows",children=
                        update_notes("September"),style={"padding": "10px"})                              
                              
                ]
            ),
        ],
    )
def build_tab_3():
    return (
        html.Div(
            id="status-container",
            children=[
                
                html.Div(
                    id="report-container",
                    children=[html.Div([
                           
                            
                        ],style={"padding":"1rem 2rem","border-bottom":"#1E2130 solid 0.8rem"})
                        ,build_top_panel_tab3(),  
                        build_bot_panel_tab3()  
                        ],
                ),
            ],
        )
    )
    

def build_value_setter_line(line_num, label, value, col3):
    return html.Div(
        id=line_num,
        children=[
            html.Label(label, className="four columns"),
            html.Label(value, className="four columns"),
            html.Div(col3, className="four columns"),
        ],
        className="row",
    )



def build_quick_stats_panel():
    return html.Div(
        id="quick-stats",
        className="row",
        children=[
           
        ],
    )


def generate_section_banner(title):
    return html.Div(className="section-banner", children=title)


def build_top_panel(stopped_interval):
    return html.Div(
        id="top-section-container",
        className="row",
        children=[
            # Metrics summary
            html.Div(
                id="metric-summary-session",
                className="eight columns",
                children=[
                    generate_section_banner("عنوان 2"),
                    html.Div(
                        id="metric-div",
                        children=[
                            
                         
                        ],
                    ),
                ],
            ),
            # Piechart
            html.Div(
                id="ooc-piechart-outer",
                className="four columns",
                children=[
                    generate_section_banner("عنوان 1"),
                   
                ]
            ),
        ],
    )

    




# Build header
def generate_metric_list_header():
    return generate_metric_row(
        "metric_header",
        {"height": "3rem", "margin": "1rem 0", "textAlign": "center"},
        {"id": "m_header_1", "children": html.Div("المنطقة")},
        {"id": "m_header_2", "children": html.Div("العدد")},
        {"id": "m_header_3", "children": html.Div("البلاغات\شهر")},
        {"id": "m_header_4", "children": html.Div("%")},
        {"id": "m_header_5", "children": html.Div("نسبة التزام الفرع بالاجراءات")},
        {"id": "m_header_6", "children": "Pass/Fail"},
    )


def generate_metric_row(id, style, col1, col2, col3, col4, col5, col6):
    if style is None:
        style = {"height": "8rem", "width": "100%"}

    return html.Div(
        id=id,
        className="row metric-row",
        style=style,
        children=[
            html.Div(
                id=col6["id"],
                style={"display": "flex", "justifyContent": "center"},
                className="one column",
                children=col6["children"],
            ),
            html.Div(
                id=col5["id"],
                style={"height": "100%", "margin-top": "5rem"},
                className="three columns",
                children=col5["children"],
            ),
            html.Div(
                id=col4["id"],
                style={},
                className="one column",
                children=col4["children"],
            ),
            html.Div(
                id=col3["id"],
                style={"height": "100%"},
                className="four columns",
                children=col3["children"],
            ),
            html.Div(
                id=col2["id"],
                style={"textAlign": "right"},
                className="one column",
                children=col2["children"],
            ),
            html.Div(
                id=col1["id"],
                className="one column",
                style={"margin-left": "2.5rem", "minWidth": "50px","textAlign": "right"},
                children=col1["children"],
            ),
            
            
            
            
        ],
    )


def build_chart_panel():
    return html.Div(
        id="control-chart-container",
        className="twelve columns",
        children=[
            generate_section_banner("عنوان 3"),
            
        ],
    )







app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        dcc.Interval(
            id="interval-component",
            interval=2 * 1000,  # in milliseconds
            n_intervals=50,  # start at batch 50
            disabled=True,
        ),
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
        dcc.Store(id="n-interval-stage", data=50),
    ],
)


@app.callback(
    [Output("app-content", "children"), Output("interval-component", "n_intervals")],
    [Input("app-tabs", "value")],
    [State("n-interval-stage", "data")],
)
def render_tab_content(tab_switch, stopped_interval):
    if tab_switch == "tab1":
        return build_tab_1(), stopped_interval
    if tab_switch == "tab3":
        return build_tab_3(), stopped_interval
    return (
        html.Div(
            id="status-container",
            children=[
                html.Div(
                    id="graphs-container",
                    children=[build_top_panel(stopped_interval), build_chart_panel(),   ],
                ),build_quick_stats_panel(),
                
            ],
        ),
        stopped_interval,
    )


# Update interval
@app.callback(
    Output("n-interval-stage", "data"),
    [Input("app-tabs", "value")],
    [
        State("interval-component", "n_intervals"),
        State("interval-component", "disabled"),
        State("n-interval-stage", "data"),
    ],
)
def update_interval_state(tab_switch, cur_interval, disabled, cur_stage):
    if disabled:
        return cur_interval

    if tab_switch == "tab1":
        return cur_interval
    if tab_switch == "tab3":
        return cur_interval
    
    return cur_stage














# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, port=8050)

