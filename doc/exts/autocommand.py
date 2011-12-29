
from subprocess import Popen, PIPE
import os.path

from docutils import nodes
import docutils.parsers.rst.directives as directives
from sphinx.util.compat import Directive

def command_to_string(command):
    result = []
    for arg in command:
        if " " in arg or not arg:
            arg = '"%s"' % arg
        result.append(arg)
    return " ".join(result)

class CommandDirective(Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = float('inf')
    option_spec = {
        'dir': directives.unchanged,
        'show_command': directives.flag
    }

    def run(self):
        env = self.state.document.settings.env

        # Determine dir to run in
        run_path = env.config.autocommand_base_path
        if not run_path:
            #TODO: Proper error reporting
            raise ValueError("autocommand_base_path configuration option is required")
        if 'dir' in self.options:
            run_path = os.path.abspath(os.path.join(run_path, self.options['dir']))
        #TODO: Proper error reporting
        if not os.path.exists(run_path):
            raise ValueError("Directory does not exist: %s" % run_path)
        if not os.path.isdir(run_path):
            raise ValueError("Path is not a directory: %s" % run_path)

        if 'show_command' in self.options:
            command_text = "$ %s\n" % command_to_string(self.arguments)
        else:
            command_text = ''

        # Run program and get stdout
        process = Popen(self.arguments, stdout=PIPE, cwd=run_path)
        stdout, stderr = process.communicate()

        text = command_text + stdout
        textnode = nodes.literal_block(text, text)
        return [textnode]

def setup(app):
    app.add_directive('autocommand', CommandDirective)
    app.add_config_value('autocommand_base_path', False, True)
