""" Example Multipage App"""

import dash

from dash_multipage import MultiPageDashController

from app1 import App1
from app2 import App2
from footer import render_footer
from error_404 import render_404

# Bootstrap CSS for pretty navigation tabs
APP = dash.Dash(__name__, external_stylesheets=[
    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css'])

# Pull flask app into namespace so it can be found for FLASK_APP
SERVER = APP.server

APP.title = "Multipage Dash Example"

# This is how the URLS to initialize the app page states will start
HOST_PATH = 'http://localhost:5000'

# List of controllers for the app pages
VIEW_CTRLS = [App1(HOST_PATH), App2(HOST_PATH)]

# Initialize the multipage App
PAGE_CTRL = MultiPageDashController(
    APP, VIEW_CTRLS, render_404(), render_footer())

if __name__ == '__main__':
    APP.run_server(debug=True)
