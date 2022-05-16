import numpy as np
import pandas as pd
import plotly
import plotly.express as px

import plotly.io as pio

# import chart-studio as py
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, Dash
from dash import html
from dash.dependencies import Input, Output

# import the data
revenue_topten = pd.read_csv("csv/cleaned_df/revenue_topten.csv")
print(revenue_topten.info())

total_sales_gb_month = \
    pd.read_csv("csv/cleaned_df/total_sales_gb_month.csv")

categories = pd.read_csv("csv/cleaned_df/categories.csv", index_col=0)

major_categories_log = pd.read_csv("csv/cleaned_df/major_category_log.csv", index_col=0)

print('total_sales_gb_month')
print(total_sales_gb_month.info())



# build the plotly plots
# and make those available for Dash through functions
def get_bar_chart():
    fig_sales_gb_month = \
        px.bar(data_frame=total_sales_gb_month, x='Year-Month', y='Total_Sales ($)',
               color_discrete_sequence=["magenta"], width=700, height=600)

    fig_sales_gb_month.update_traces(marker_line_width=2, marker_line_color='black')
    fig_sales_gb_month.update_layout({'plot_bgcolor': 'black', 'paper_bgcolor': 'black',
                                      'font': {'color': 'white', 'size': 13},
                                      'margin': {'l': 50, 'r': 50, 'b': 20, 't': 20},
                                      'title': {'text': 'Total sales over month', 'x': 0.5, 'y': 0.98,
                                                'xanchor': 'center', 'yanchor': 'top',
                                                'font': {'size': 25}},
                                      })

    fig_sales_gb_month.update_traces(marker_line_width=2, marker_line_color="white")

    fig_sales_gb_month.update_xaxes(tickangle=90)

    # Setting the margins and thereby cutting the paper bg,
    # makes it easier to set the margins within the Dash app below

    # fig_sales_gb_month.show(fig_sales_gb_month)

    fig_sales_gb_month = dcc.Graph(figure=fig_sales_gb_month, style={'display': 'inline-block',
                                                                     'margin-top': 50, 'margin-left': 60,
                                                                     'margin-right': 50})

    return fig_sales_gb_month

def get_multiple_line_chart():

            top_ten_revenue_fig = \
            px.line(data_frame=revenue_topten, x='year_month', y='revenue',
                    color='Country', width=700, height=600,
                    title='Top ten countries by revenue without UK')

            top_ten_revenue_fig.update_layout({"paper_bgcolor": "black", "plot_bgcolor": 'black',
                                               "font": {'color': 'white', 'size': 13},
                                               'margin': {'l': 50, 'r': 50, 'b': 20, 't': 20},
                                               'title': {'text': 'Top ten revenue countries without UK', 'x': 0.5, 'y': 0.99,
                                                         'xanchor': 'center', 'yanchor': 'top',
                                                         'font': {'size': 23}, 'pad_b': 0.1
                                                     }})

            top_ten_revenue_fig = dcc.Graph(figure=top_ten_revenue_fig, style={'display': 'inline-block',
                                                                               'margin-top': 50, 'margin-left': 60,
                                                                               'margin-right': 50})

            return top_ten_revenue_fig



def get_horizontal_bar_chart():
            categories_fig = \
            px.bar(categories, x='Total_Orders', y='Minor_Category',
                   color='Major_Category',
                   color_discrete_sequence=["orange", "red", "green", "blue"],
                   width=700, height=600)

            categories_fig.update_layout({'yaxis': {'dtick': 1, 'categoryorder': 'total ascending'},
                                          'plot_bgcolor': 'black', 'paper_bgcolor': 'black',
                                          'font': {'color': 'white', 'size': 12},
                                          'margin': {'l': 50, 'r': 50, 'b': 20, 't': 20},
                                          'title': {'text': 'Minor categories of products', 'x': 0.5, 'y': 0.99,
                                                    'xanchor': 'center', 'yanchor': 'top',
                                                    'font': {'size': 20}, 'pad': {'b': 0, 't': 0.01}}})

            categories_fig.update_traces(marker_line_width=1, marker_line_color="white")

            categories_fig = dcc.Graph(figure=categories_fig, style={'display': 'inline-block',
                                                                     'margin-top': 80, 'margin-left': 60,
                                                                     'margin-right': 40})

            return categories_fig


def get_pie_chart():
            major_categories_fig = \
            px.pie(major_categories_log,
                   names='Major_Category', values='Total_Orders',
                   color_discrete_sequence=px.colors.qualitative.Prism,
                   width=700, height=600)

            major_categories_fig.update_layout({'plot_bgcolor': 'black', 'paper_bgcolor': 'black',
                                                'font': {'size': 12, 'color':'white'},
                                                'margin': {'l': 50, 'r': 50, 'b': 20, 't': 20},
                                                'title': {'text': 'Major categories of products', 'x': 0.5, 'y': 0.99,
                                                          'xanchor': 'center', 'yanchor': 'top',
                                                          'font': {'size': 25}
                                                          }})

            major_categories_fig.update_traces(marker_line_color='white', marker_line_width=2)

            major_categories_fig = dcc.Graph(figure=major_categories_fig, style={'display': 'inline-block',
                                                                                 'margin-top': 80, 'margin-left': 60,
                                                                                 'margin-right': 50})

            return major_categories_fig



app = dash.Dash(__name__)
server = app.server
# ======================== App Layout
app.layout = html.Div([

    html.H1('Ecommerce Sales Dashboard', style={'text-align': 'center', 'background-color': 'black', 'font-size': 30,
                                                'font_color': 'white'}),
    html.Div(children=[get_bar_chart(), get_multiple_line_chart()]),
    html.Div(children=[get_horizontal_bar_chart(), get_pie_chart()])


], style={'text-align': 'center',
          'font-size': 20,
          'font-family': 'Arial',
          'color': 'white',
          'paper_bgcolor': 'black',
          'background-color': 'black',
          'border': '4px solid red'})
if __name__ == '__main__':
    app.run_server(port=8066)
