# dash-multipage
A framework to simplify some of the challenges in setting up multipage dash pages

This can be used as is to reduce the boilerplate for a multipage app, or used as a template.

The basic structure is to create an instance of dash_multipage.MultiPageDashController.

This adds the layout and callbacks to the dash app passed in as an argument. It provides the
nav buttons on top, and handles selecting the page based on the URL.

Each page is an implementation of dash_multipage.ControllerBase. The implementation gives the
link information, layout and callbacks.

To handle loading a page with specific selections, the from dash_multipage.URLArgs provides
a way to generate links with the current input, dropdown, etc. selection preserved. This is
not required, and you can generate a multipage app without this functionality.

As a minor note, there is also a set of classes that override dash's Input, Output, and State.
These are merely a convenience wrapper to allow them to be initialized directly from the
components.

#Example
An example app is found in example/

To run with flask:
FLASK_DEBUG=1 FLASK_APP=example/multipage_app.py:SERVER flask run
