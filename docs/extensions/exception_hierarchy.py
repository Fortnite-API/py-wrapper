"""
MIT License

Copyright (c) 2019-present Luc1412

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sphinx.application
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.locale import _

if TYPE_CHECKING:
    from sphinx.writers.html5 import HTML5Translator


class exception_hierarchy(nodes.General, nodes.Element):
    pass


def visit_exception_hierarchy_node(self: HTML5Translator, node: exception_hierarchy):
    self.body.append(self.starttag(node, 'div', CLASS='exception-hierarchy-content'))


def depart_exception_hierarchy_node(self: HTML5Translator, node: exception_hierarchy):
    self.body.append('</div>\n')


class ExceptionHierarchyDirective(Directive):
    # Essentials creates a new directive titled "exception_hierarchy" that can be used in the .rst files
    # for displaying an exception hierarchy.
    has_content = True

    def run(self):
        self.assert_has_content()
        node = exception_hierarchy('\n'.join(self.content))
        self.state.nested_parse(self.content, self.content_offset, node)  # type: ignore
        return [node]


def setup(app: sphinx.application.Sphinx):
    app.add_node(  # type: ignore
        exception_hierarchy,
        html=(visit_exception_hierarchy_node, depart_exception_hierarchy_node),
    )

    app.add_directive('exception_hierarchy', ExceptionHierarchyDirective)

    # Tell sphinx that it is okay for the exception hierarchy to be used in parallel
    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
