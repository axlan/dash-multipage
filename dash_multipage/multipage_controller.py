# -*- coding: utf-8 -*-
""" Class for generating a multipage dash app

    This class turns a list of controllers into a multi-page website
"""

from typing import List
import logging
import os

import dash_html_components as html
import dash_core_components as dcc
from dash import Dash
from dash.dependencies import Input, Output
import flask

from dash_multipage.controller_base import ControllerBase
from dash_multipage.url_arg_manager import parse_href

URL_ID = 'url'

class MultiPageDashController():
    """ Class for generating a multipage dash app.

        Creating an instance of this class will register the list of controllers
        with the dash app so that the pages will be displayed at their specified
        paths, and their callbacks will be added.

        Parameters:
            app - the dash app that will be serving the page and handling callbacks
            ctrls - a list of controllers that implement the abstract
                ControllerBase class. These provide the rendering and logic for
                the pages that make up this app.
            error_404 - rendering for 404 error page
            footer - common rendering to put at the bottom of all pages
    """

    def __init__(self, app: Dash, ctrls: List[ControllerBase],
                 error_404: html.Div, footer=html.Div()):
        self.ctrls = ctrls
        self.app = app
        self.error_404 = error_404
        self.logger = logging.getLogger(os.path.basename(__file__))

        nav_tab_html = [
            html.Li(
                dcc.Link(
                    ctrls.get_link_info().link_text,
                    href=ctrls.get_link_info().page_path,
                    className='nav-link',
                    id=ctrls.get_link_info().page_link_id, ),
                className='nav-item') for ctrls in self.ctrls
        ]
        self.top_layout = html.Div(children=[
            html.H4(),
            html.Ul(
                className='nav nav-tabs',
                children=nav_tab_html,
                id='nav-bar'),
            dcc.Location(id=URL_ID, refresh=False),
            html.Br(),
            html.Div(id='page-content', children=[]),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            footer,
            html.Br(),
        ], className='container', )
        app.layout = self._serve_layout
        self._register_callbacks()

    def _serve_layout(self) -> html.Div:
        # See "Dynamically Create a Layout for Multi-Page App Validation"
        # in https://dash.plot.ly/urls
        if flask.has_request_context():
            # Normal operation
            return self.top_layout
        # Only returned for initial callback validation
        return html.Div([self.top_layout] + [ctrl.layout({})
                                             for ctrl in self.ctrls])

    def _register_callbacks(self) -> None:
        def generate_navlink_update(url: str, id_str: str):
            """Create a dash callback function to update a nav-link element class based
            on the current selected page

            Parameters
            ----------
            url : str
            url of nav-link href
            id_str : str
            id of nav-link element

            Returns
            ----------
            function:
            callback function

            """

            @self.app.callback(Output(id_str, 'className'), [
                Input(URL_ID, 'pathname'),
            ])
            def _update_navlink(pathname):
                if pathname == url:
                    return 'nav-link active'
                return 'nav-link'

        for ctrl in self.ctrls:
            generate_navlink_update(ctrl.get_link_info().page_path,
                                    ctrl.get_link_info().page_link_id)
            ctrl.register_callbacks(self.app)

        @self.app.callback(
            Output('page-content', 'children'), [
                Input(URL_ID, 'href'),
            ])
        def _display_page(href: str):
            """Handle URL changes for whole app
            """
            self.logger.info("Loading path: %s", href)
            # The framework can occasionally pass in 'None' while loading.
            if href is None:
                return 'Loading.....'
            try:
                route, args = parse_href(href)
            except BaseException:  # pylint: disable=bare-except
                return self.error_404
            for ctrls in self.ctrls:
                if route == ctrls.get_link_info().page_path:
                    return ctrls.layout(args)
            return self.error_404
