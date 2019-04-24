# -*- coding: utf-8 -*-
""" Code for managing page state through the URL
"""

from typing import Dict, Union, List, Tuple, Any, NamedTuple
from urllib import parse
from enum import Enum, auto
import json

from dash import Dash
from dash.development.base_component import Component
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html


class ValueTypes(Enum):
    """ Types of values that can be read from url
    """
    STR = auto()
    STR_LIST = auto()
    INT = auto()
    FLOAT = auto()
    DICT = auto()


class ComponentInfo(NamedTuple):
    """ Tracks info on how to initialize a component from URL args
    """
    component: Component
    value_name: str
    value_type: ValueTypes
    default: Any


class URLArgs:
    """ Class for managing loading values from URL, and generating a link box
        that gives a URL with the page's current state

        Parameters
        ----------
        id_namespace : str
            the name space for ids on the page.
            ie. MY_PAGE/input1 would have the namespace MY_PAGE
        page_path : str
            the base URL for the app ie. http://localhost:8080

    """

    def __init__(self, id_namespace: str, page_path: str):
        self.page_path = page_path
        self.id_namespace = id_namespace
        self.link_id = id_namespace + '/quick-link-box'
        self.link_id_workaround = self.link_id + '-workaround'
        self.linked_components: List[ComponentInfo] = []

    def register_component(
            self,
            component: Component,
            value='value',
            default=None,
            value_type=ValueTypes.STR) -> None:
        """ Register a component to have it's value associated with a url argument

        Parameters
        ----------
        component : dash component to register
        value : the attribute of the component to track
        default : default value of component if none specified in URL
        value_type : how to interpret url argument
        """
        self.linked_components.append(
            ComponentInfo(
                component,
                value,
                value_type,
                default))

    @staticmethod
    def _get_key(component_id: Component) -> str:
        return component_id.split('/')[-1]

    def generate_link_box(self) -> html.Div:
        """ Get layout of the link box for this page
        """
        return html.Div([
            dcc.Input(
                id=self.link_id,
                type='text',
                readOnly=True,
                value='',),
            html.Div(id=self.link_id_workaround, style={'display': 'none'}),
        ])

    def _generate_url(self, kwargs: Dict[str, Union[str, List[str]]]) -> str:
        """Generates a page URL with state arguments

        Parameters
        ----------
        kwargs: key value pairs with page state. Values can be a string or list of strings

        Returns
        ----------
        str, fully formatted URL
        """
        tuples: Tuple = ()
        for k, vals in kwargs.items():
            if vals is None:
                continue
            if not isinstance(vals, list):
                vals = [vals]
            for val in vals:
                tuples = tuples + ((k, val),)
        arg_str = parse.urlencode(tuples)
        return '{}?{}'.format(self.page_path, arg_str)

    def initialize_components(self, args_dict: Dict[str, List[str]]) -> None:
        """ Update components with the values from the Dict

            Should be called after all components are registered
        """
        for component_info in self.linked_components:
            component = component_info.component
            value_name = component_info.value_name
            key = self._get_key(component.id)
            value = component_info.default
            try:
                str_list = args_dict[key]
                if component_info.value_type == ValueTypes.STR_LIST:
                    value = str_list
                else:
                    str_val = str_list[-1]
                    if component_info.value_type == ValueTypes.STR:
                        value = str_val
                    else:
                        try:
                            if component_info.value_type == ValueTypes.INT:
                                value = float(str_val)
                            elif component_info.value_type == ValueTypes.FLOAT:
                                value = float(str_val)
                            elif component_info.value_type == ValueTypes.DICT:
                                value = json.loads(str_val.replace("'", '"'))
                        except (ValueError, json.JSONDecodeError):
                            pass
            except KeyError:
                pass
            setattr(component, value_name, value)

    def register_callbacks(self, app: Dash) -> None:
        """ Add the callbacks for the components and link box to the app
            Should only be called after all the components are registered
        """
        # Workaround for
        # https://github.com/plotly/dash-core-components/issues/430
        @app.callback(Output(self.link_id_workaround, 'children'),
                      [Input(self.link_id, 'value')])
        def _update_div(input_value) -> str:  # pylint: disable=unused-argument
            return ''
        # Add callback to update link box when one of the monitored components
        # changes

        @app.callback(
            Output(
                self.link_id, 'value'), [
                    Input(info.component.id, info.value_name) for info in self.linked_components])
        def _update_link_box(*args) -> str:
            """Materializes a copyable, read-only URL to the current page view.

            """
            kwargs = {
                self._get_key(
                    info.component.id): arg for info, arg in zip(
                        self.linked_components, args)}
            return self._generate_url(kwargs)


def parse_href(href: str) -> Tuple[str, Dict[str, List[str]]]:
    """Parses a href from Dash.

    The expected format is /PAGE_NAME?arg1=val1&arg2=val2.

    Also repeated keys are treated as entries in a list. arg1=val1&arg1=val2
    would be treated as arg1: [val1, val2]. See:
    https://docs.python.org/2/library/urlparse.html#urlparse.parse_qs

    Parameters
    ----------
    href : str
      URL path name as passed from Dash

    Returns
    ----------
    (str, dict), server route and query parameters

    """
    if not href:
        return ('', {})
    result = parse.urlparse(href)
    url_args = parse.parse_qs(result.query)
    return result.path, url_args
