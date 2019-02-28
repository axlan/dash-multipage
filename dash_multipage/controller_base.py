# -*- coding: utf-8 -*-
""" Abstract base class for controllers for a page in a multipage dash app
"""

from abc import ABC, abstractmethod
from typing import NamedTuple, Dict

from dash_html_components import Div


class LinkInfo(NamedTuple):
    """ The link info for a controller

        Attributes:
            link_text: Text to show in navigation tab
            page_path: The url path for the page starting with '/'
            page_link_id: unique id for the navigation link callback

        for example:
            ('Metrics Viewer', '/metrics', 'metrics_view')
            ('Run Viewer', '/', 'run_view')
    """
    link_text: str
    page_path: str
    page_link_id: str


class ControllerBase(ABC):
    """ Abstract base class for controllers for a page in a multipage dash app
    """

    @abstractmethod
    def layout(self, args: Dict) -> Div:
        """ Return this controller's layout initialized with a of optional args
        """

    @abstractmethod
    def register_callbacks(self, app) -> None:
        """ Register this controllers callbacks
            This should only be called after the top level layout has been
            added to the app

            Parameters
            ----------
            app: dash app to register callbacks with
        """

    @staticmethod
    @abstractmethod
    def get_link_info() -> LinkInfo:
        """ Return the link info for this controller see LinkInfo docstring
        """
