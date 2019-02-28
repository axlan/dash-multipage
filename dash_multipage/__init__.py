"""
    dash_multipage
    ~~~~~~~~~
    A framework to handle some of the boilerplate for creating a multipage
    dash application
"""

from .version import __version__

from .controller_base import ControllerBase, LinkInfo
from .multipage_controller import MultiPageDashController
from .url_arg_manager import URLArgs
from .callbacks import Input, Output, State
