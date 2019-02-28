# -*- coding: utf-8 -*-

""" Logic for App1

"""
from typing import Dict

import dash_core_components as dcc
import dash_html_components as html

from dash_multipage import URLArgs
from dash_multipage import ControllerBase
from dash_multipage import LinkInfo
from dash_multipage import Input, Output, State


class App1(ControllerBase):
    """ Implement ControllerBase for app1"""

    def __init__(self, host_path):
        """ Initialize the components in app1"""
        id_namespace = self.get_link_info().page_link_id
        full_page_path = host_path + self.get_link_info().page_path
        # initialize a URLArgs to track state of input1 and input1
        self.url_args = URLArgs(id_namespace, full_page_path)

        self.input1 = dcc.Input(
            id=id_namespace +
            '/input-1-state',
            type='text',
            value='Montreal')
        self.url_args.register_component(self.input1)
        self.input2 = dcc.Input(
            id=id_namespace +
            '/input-2-state',
            type='text',
            value='Canada')
        self.url_args.register_component(self.input2)
        self.button = html.Button(
            id=id_namespace +
            '/submit-button',
            n_clicks=0,
            children='Submit')
        self.output = html.Div(id=id_namespace + '/output-state')

    def layout(self, args: Dict):
        """ layout the components in app1"""
        self.url_args.initialize_components(args)
        link_box = self.url_args.generate_link_box()
        return html.Div([
            html.H2('Page 1'),
            link_box,
            self.input1,
            self.input2,
            self.button,
            self.output,
        ])

    @staticmethod
    def get_link_info() -> LinkInfo:
        """ Link information """
        return LinkInfo('App1', '/', 'app1')

    def register_callbacks(self, app):
        """ Register callbacks """

        self.url_args.register_callbacks(app)

        @app.callback(Output(self.output, 'children'),
                      [Input(self.button, 'n_clicks')],
                      [State(self.input1, 'value'), State(self.input2, 'value')])
        def _update_output(n_clicks, input1, input2):
            return ('The Button has been pressed {} times,'
                    'Input 1 is "{}",'
                    'and Input 2 is "{}"').format(n_clicks, input1, input2)
