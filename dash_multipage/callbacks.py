""" Convenience wrappers to allow Components to be directly used to initialize
    dependencies. This avoids linting issues if "id" is seen as an attribute
"""

from dash import dependencies
from dash.development.base_component import Component

# pylint: disable=too-few-public-methods
class Output(dependencies.Output):
    """Output of a callback."""

    def __init__(self, component: Component, component_property='value'):
        super().__init__(component.id, component_property)


# pylint: disable=too-few-public-methods
class Input(dependencies.Input):
    """Input of callback trigger an update when it is updated."""

    def __init__(self, component: Component, component_property='value'):
        super().__init__(component.id, component_property)


# pylint: disable=too-few-public-methods
class State(dependencies.State):
    """Use the value of a state in a callback but don't trigger updates."""

    def __init__(self, component: Component, component_property='value'):
        super().__init__(component.id, component_property)
