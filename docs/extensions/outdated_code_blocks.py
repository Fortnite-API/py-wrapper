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

from typing import ClassVar

from docutils.nodes import Element, Node, TextElement
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.directives import optional_int
from sphinx.directives.code import CodeBlock
from sphinx.util.typing import OptionSpec
from sphinx.writers.html5 import HTML5Translator


class OutdatedCodeBlockNode(Element):
    # The parent node, holds the code block and the warning.
    pass


# Visits the outdated code block node
def visit_outdated_code_block_node(self: HTML5Translator, node: OutdatedCodeBlockNode) -> None:
    # Returns the opening div tag for the outdated code block
    self.body.append(self.starttag(node, 'div', CLASS='outdated-code-block'))


def depart_outdated_code_block_node(self: HTML5Translator, node: OutdatedCodeBlockNode) -> None:
    # Returns the closing div tag for the outdated code block
    self.body.append('</div>')


class OutdatedCodeBlockWarning(Element):
    # Holds the warning at the bottom of the code block.
    ...


def visit_outdated_code_block_warning(self: HTML5Translator, node: OutdatedCodeBlockWarning) -> None:
    # Returns the div that actually holds the warning
    # Create some attributes so that the background is dc2626
    self.body.append(self.starttag(node, 'div', CLASS='outdated-code-block-warning'))


def depart_outdated_code_block_warning(self: HTML5Translator, node: OutdatedCodeBlockWarning) -> None:
    # Returns the closing div tag for the warning
    self.body.append('</div>')


class OutdatedCodeBlockWarningText(TextElement):
    # Holds the warning text.
    ...


def visit_outdated_code_block_warning_text(self: HTML5Translator, node: OutdatedCodeBlockWarningText) -> None:
    # Returns the opening p tag for the warning text
    self.body.append(self.starttag(node, 'div', CLASS='outdated-code-block-warning-text'))


def depart_outdated_code_block_warning_text(self: HTML5Translator, node: OutdatedCodeBlockWarningText) -> None:
    # Returns the closing p tag for the warning text
    self.body.append('</div>')


class OutdatedCodeBlock(CodeBlock):
    """A custom Sphinx directive that aims to add a warning to code blocks
    that to not work with the latest version of the library.

    .. outdated-code-block:: <language>
        :since: <version> # The version where the code block was last working

        <code block>

    Generates the following HTML:

    <div class="outdated-code-block"> # Holds the entire outdated warning
        <pre class="literal-block /> # Holds the actual code block
        <div class="outdated-code-block-warning"> # Holds the Warning
            <p>[Warning Text]</p> # The text of the warning. Notifies *when* the code block was last working.
        </div>
    </div>
    """

    has_content = True
    required_arguments = 1
    optional_arguments = 1

    option_spec: ClassVar[OptionSpec] = {
        'since': directives.unchanged_required,
        'force': directives.flag,
        'linenos': directives.flag,
        'dedent': optional_int,
        'lineno-start': int,
        'emphasize-lines': directives.unchanged_required,
        'caption': directives.unchanged_required,
        'class': directives.class_option,
        'name': directives.unchanged,
    }

    def run(self) -> list[Node]:

        # Create the main node that holds the code block and warning
        root = OutdatedCodeBlockNode()

        code_block: list[Node] = super().run()
        root += code_block

        # Create the underlying warning node
        warning = OutdatedCodeBlockWarning()
        root.append(warning)

        # The underlying warning text
        warning_text_raw = (
            f'This code block is from version {self.options["since"]}. It will not work with the latest version.'
        )
        warning_text = OutdatedCodeBlockWarningText(warning_text_raw, warning_text_raw)
        warning.append(warning_text)

        return [root]


# The setup function for the extension
def setup(app: Sphinx):
    app.add_node(OutdatedCodeBlockNode, html=(visit_outdated_code_block_node, depart_outdated_code_block_node))  # type: ignore
    app.add_node(OutdatedCodeBlockWarning, html=(visit_outdated_code_block_warning, depart_outdated_code_block_warning))  # type: ignore
    app.add_node(  # type: ignore
        OutdatedCodeBlockWarningText, html=(visit_outdated_code_block_warning_text, depart_outdated_code_block_warning_text)
    )

    app.add_directive('outdated-code-block', OutdatedCodeBlock)

    # Tell sphinx that it is okay for the exception hierarchy to be used in parallel
    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
