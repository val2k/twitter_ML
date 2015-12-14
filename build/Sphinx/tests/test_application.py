# -*- coding: utf-8 -*-
"""
    test_application
    ~~~~~~~~~~~~~~~~

    Test the Sphinx class.

    :copyright: Copyright 2007-2015 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from docutils import nodes

from sphinx.application import ExtensionError
from sphinx.domains import Domain

from util import with_app, raises_msg


@with_app()
def test_events(app, status, warning):
    def empty():
        pass
    raises_msg(ExtensionError, "Unknown event name: invalid",
               app.connect, "invalid", empty)

    app.add_event("my_event")
    raises_msg(ExtensionError, "Event 'my_event' already present",
               app.add_event, "my_event")

    def mock_callback(a_app, *args):
        assert a_app is app
        assert emit_args == args
        return "ret"
    emit_args = (1, 3, "string")
    listener_id = app.connect("my_event", mock_callback)
    assert app.emit("my_event", *emit_args) == ["ret"], "Callback not called"

    app.disconnect(listener_id)
    assert app.emit("my_event", *emit_args) == [], \
        "Callback called when disconnected"


@with_app()
def test_emit_with_nonascii_name_node(app, status, warning):
    node = nodes.section(names=[u'\u65e5\u672c\u8a9e'])
    app.emit('my_event', node)


@with_app()
def test_output(app, status, warning):
    status.truncate(0)  # __init__ writes to status
    status.seek(0)
    app.info("Nothing here...")
    assert status.getvalue() == "Nothing here...\n"
    status.truncate(0)
    status.seek(0)
    app.info("Nothing here...", True)
    assert status.getvalue() == "Nothing here..."

    old_count = app._warncount
    app.warn("Bad news!")
    assert warning.getvalue() == "WARNING: Bad news!\n"
    assert app._warncount == old_count + 1


@with_app()
def test_extensions(app, status, warning):
    app.setup_extension('shutil')
    assert warning.getvalue().startswith("WARNING: extension 'shutil'")


@with_app()
def test_domain_override(app, status, warning):
    class A(Domain):
        name = 'foo'

    class B(A):
        name = 'foo'

    class C(Domain):
        name = 'foo'

    # No domain know named foo.
    raises_msg(ExtensionError, 'domain foo not yet registered',
               app.override_domain, A)
    assert app.add_domain(A) is None
    assert app.override_domain(B) is None
    raises_msg(ExtensionError, 'new domain not a subclass of registered '
               'foo domain', app.override_domain, C)
