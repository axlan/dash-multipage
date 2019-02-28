"""Example Footer layout"""
import dash_html_components as html


def render_footer():
    """Generate footer HTML added to every page
    """
    return html.Footer(
        html.Div(
            id='footer-copyright',
            className='container-fluid text-center',
            children=[
                html.Span(
                    'Copyright © 2019 Jonathan Diamond',
                    className='text-muted'),
                html.H5(),
            ]),
        className='page-footer',
        style={
            'textAlign': 'center',
            'position': 'absolute',
            'bottom': 0,
            'width': '100%',
            'padding': '60px 15px 0',
        }, )
