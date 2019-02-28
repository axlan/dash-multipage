"""Content not found (404) error pages
"""

import dash_html_components as html

CATS = 'http://thecatapi.com/api/images/get?format=src&type=gif'


def render_404():
    """
    Returns
    ----------
    dash_html_components.Div of a 404 page
    """
    return html.Div(
        children=[
            html.Img(
                id='sbpla_cats',
                src=CATS,
                width='100%',
                style={'marginTop': '10px',
                       'marginBottom': '20px'}),
            html.Br(),
            html.H3('404 - No Content Available.'),
        ],
        style={'text-align': 'center'})
