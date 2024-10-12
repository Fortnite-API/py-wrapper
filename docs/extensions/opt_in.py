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

from docutils import nodes
from docutils.parsers import rst
from typing import TYPE_CHECKING, Any, Sequence
from sphinx.addnodes import pending_xref

# from sphinx.roles import XRefRole

if TYPE_CHECKING:
    from sphinx.application import Sphinx


class OptInDirective(rst.Directive):
    """Denotes a directive that notes a feature is opt-in.

    This directive is used to denote that a feature is opt-in, meaning that it is not enabled by default
    and must be enabled using a flag. This is a shorthand for the following:

    .. code-block:: rst

        .. danger::

            This is opt-in. For this parameter to be available, you must enable the
            <user-set-flag-link> flag on the client.

        .. seealso::

            See the :ref:`response flags documentation <response_flags>` for more information on
            what response flags are and how to use them.
    """

    required_arguments = 1
    optional_arguments = 0
    has_content = False

    def run(self) -> Sequence[nodes.Node]:
        # (1) Grab the argument from the directive which denotes the flag that must be set.
        flag_name = self.arguments[0]

        # (2) Create the important node that denotes the feature is opt-in.
        important_node = nodes.important(
            '',
            nodes.paragraph(
                '',
                '',
                nodes.Text("This attribute is opt-in, meaning it will be unavailable by default. You must enable the "),
                self._create_pending_xref('attr', f'fortnite_api.ResponseFlags.{flag_name}', flag_name),
                nodes.Text(" flag on the client to have access to this attribute."),
            ),
            nodes.paragraph(
                '',
                '',
                nodes.Text('See the '),
                self._create_pending_xref(
                    'ref', 'response_flags', 'response flags documentation', refdomain='std', refexplicit=True
                ),
                nodes.Text(" for more information on what response flags are and how to use them."),
            ),
        )

        return [important_node]

    def _create_pending_xref(
        self, reftype: str, target: str, text: str, refdomain: str = 'py', **kwargs: Any
    ) -> pending_xref:
        refnode = pending_xref(
            '', refdomain=refdomain, reftype=reftype, reftarget=target, modname=None, classname=None, **kwargs
        )
        refnode += nodes.Text(text)
        return refnode


def setup(app: Sphinx):
    app.add_directive('opt-in', OptInDirective)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
