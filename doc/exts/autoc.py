
import os.path
import re

import sphinx.ext.autodoc as autodoc

file_doc_re = re.compile(
    r'''\A[^\n]*\n?     # Optional ignored first line
        /\*\*[^\n]*\n   # Start of comment, first line not part of docstring.
        (.*?)           # reST docs.
        \*/             # End docs.
     ''', re.VERBOSE | re.DOTALL)

class CFileDocumenter(autodoc.Documenter):
    """Documenter for C files.

    Extracts a single multiline comment starting in the first two lines of the
    file.  The comment should look like this:

        /**
         *
         * reST contents here.
         *
         */

    The first line (which starts with "/**") is ignored.  You can leave it
    empty or put the filename there if you wish.

    """

    objtype = 'cfile'

    def generate(self, more_content=None, real_modname=None,
                 check_module=False, all_members=False):

        # Read file
        filename = os.path.abspath(os.path.join(self.env.config.autoc_base_path,
                                                self.name))
        if not os.path.exists(filename):
            self.directive.warn('File not found: "%s".' % filename)
            return
        f = open(filename)
        file_contents = f.read()
        f.close()

        if file_contents.startswith('\n'):
            start_line = 1
        else:
            start_line = 0

        # Extract doc string
        match = file_doc_re.search(file_contents)
        if not match:
            self.directive.warn('No docstring found in file "%s".' % filename)
            return
        doc = match.group(1)

        # Format and output
        self.add_line(u'', '')
        for i, line in enumerate(doc.split('\n')):
            line = line.lstrip(' \t')
            if line.startswith('*'):
                line = line[1:]
            if line.startswith(' '):
                line = line[1:]
            self.add_line(line, filename, i+start_line)

        # Add file dependancy
        self.directive.filename_set.add(filename)

        self.add_content(more_content)


def setup(app):
    app.add_config_value('autoc_base_path', False, True)

    autodoc.add_documenter(CFileDocumenter)
    # add_directive_to_domain was added in Sphinx 1.0, use add_directive instead.
    #app.add_directive_to_domain('c', 'autofile', autodoc.AutoDirective)
    app.add_directive('autocfile', autodoc.AutoDirective)
