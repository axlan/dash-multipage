# -*- coding: utf-8 -*-

""" Logic for App2

"""
from typing import Dict

import dash_core_components as dcc
import dash_html_components as html

from dash_multipage import URLArgs
from dash_multipage import ControllerBase
from dash_multipage import LinkInfo
from dash_multipage import Input, Output


class App2(ControllerBase):

    def __init__(self, host_path):
        id_namespace = self.get_link_info().page_link_id
        full_page_path = host_path + self.get_link_info().page_path
        self.url_args = URLArgs(id_namespace, full_page_path)

        self.drop = dcc.Dropdown(
            id=id_namespace + 'dropdown',
            options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']]
        )
        self.url_args.register_component(self.drop, default='LA')
        self.display = html.Div(id=id_namespace + '/display-value')

    def layout(self, args: Dict):
        self.url_args.initialize_components(args)
        link_box = self.url_args.generate_link_box()
        return html.Div([
            html.H2('Page 2'),
            link_box,
            self.drop,
            self.display,
        ])

    @staticmethod
    def get_link_info() -> LinkInfo:
        return LinkInfo('App2', '/app2', 'app2')

    def register_callbacks(self, app):

        self.url_args.register_callbacks(app)

        @app.callback(Output(self.display, 'children'),
                      [Input(self.drop, 'value')])
        def _display_value(value):
            print('display_value')
            return 'You have selected "{}"'.format(value)
