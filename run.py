#!/usr/bin/env python

import resource
import pty
import select
import os
import signal
from copy import copy

import wx


class AppRunnerFrame(wx.Frame):

    def __init__(self, parent, id, title, size):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, size)

        self.app_panels = []
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.sizer = wx.GridSizer(1, 1, 0, 0)
        self.SetSizer(self.sizer)

        self.main_split = wx.SplitterWindow(self, -1)
        self.main_split.SetMinimumPaneSize(120)

        self.panel_left = wx.Panel(self.main_split, -1)
        self.panel_left_sizer = wx.GridSizer(1, 1, 0, 0)
        self.panel_left.SetSizer(self.panel_left_sizer)

        self.panel_right = wx.Panel(self.main_split, -1)
        self.panel_right_sizer = wx.GridSizer(1, 1, 0, 0)
        self.panel_right.SetSizer(self.panel_right_sizer)

        self.current_app_panel = None
        self.app_tree = wx.TreeCtrl(self.panel_left, -1, wx.DefaultPosition, (-1, -1), wx.TR_FULL_ROW_HIGHLIGHT | wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT)
        self.read_apps()
        self.app_tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_app_select, id=self.app_tree.GetId())
        self.app_tree.SetFocus()
        self.app_tree.SelectItem(self.app_tree.GetFirstVisibleItem())
        self.panel_left_sizer.Add(self.app_tree, 1, wx.EXPAND)

        self.main_split.SplitVertically(self.panel_left, self.panel_right, 250)
        self.sizer.Add(self.main_split, 1, wx.EXPAND)

        # Timer to update stdout display of the current app
        self.timer = wx.PyTimer(lambda: self.update())
        self.timer.Start(200)

    def update(self):
        for app in self.app_panels:
            app.update()

    def read_apps(self):
        '''Populates the application tree.'''
        applications = {
            "Communication": {
                "Hub": AppPanel(self.panel_right, ["seawolf-hub", "-c", "../conf/hub.conf"], "db/"),
                "Serial App": AppPanel(self.panel_right, ["./bin/serialapp"], "serial/"),
                "SVR": AppPanel(self.panel_right, ["svrd"], ""),
                "SVR Record": AppPanel(self.panel_right, ["python", "vision/svr_record_all.py", "vision/capture/"], ""),
            },
            "Debugging": {
                "Simulator": AppPanel(self.panel_right, ["python", "run.py"], "utils/simulator/", options=[
                    CheckBoxOption("--svr-source", "", "SVR Source", False),
                ]),
                "SVR Watch": AppPanel(self.panel_right, ["python", "vision/svr_watch_all.py"], ""),
                "HUD": AppPanel(self.panel_right, ["python", "HUD.py"], "utils/HUD/"),
                "Vision": AppPanel(self.panel_right, ["python", "run.py"], "vision/", options=[
                    TextOption("Entity: ", ignore_empty=False),
                    CheckBoxOption("-s", None, "Single Process", False),
                    CheckBoxOption(None, "-G", "Debug", True),
                    TextOption("Delay: ", "10", "-d"),
                    VisionCameraOption()]
                ),
            },
            "PID": {
                "Depth PID": AppPanel(self.panel_right, ["./bin/depthpidpy"], "applications/"),
                "Roll PID": AppPanel(self.panel_right, ["./bin/rollpidpy"], "applications/"),
                "Pitch PID": AppPanel(self.panel_right, ["./bin/pitchpidpy"], "applications/"),
                "Yaw PID": AppPanel(self.panel_right, ["./bin/yawpidpy"], "applications/"),
                "Mixer": AppPanel(self.panel_right, ["./bin/mixer"], "applications/"),
            },
            "Control": {
                "Joystick Controller": AppPanel(self.panel_right, ["./bin/joystick_controller"], "applications/"),
                "Steering Wheel Controller": AppPanel(self.panel_right, ["./bin/steering_controller"], "applications/"),
                "Zero Thrusters": AppPanel(self.panel_right, ["./bin/zerothrusters"], "applications/"),
            },
            "Missions (Simulator)": {
                "Run All Missions": AppPanel(self.panel_right, ["python", "run.py", "-s"], "mission_control/"),

            },
        }
        tree_root = self.app_tree.AddRoot("Applications")
        for group_name, app_dict in applications.iteritems():
            group_root = self.app_tree.AppendItem(tree_root, group_name)
            for app_name, panel in app_dict.iteritems():

                # Add the app
                app_item = self.app_tree.AppendItem(group_root, app_name)
                self.app_tree.SetPyData(app_item, panel)
                self.app_tree.Bind(wx.EVT_TREE_ITEM_MIDDLE_CLICK, self.on_app_middle_click)
                self.app_tree.Bind(wx.EVT_TREE_KEY_DOWN, self.on_app_key_press)
                panel.Show(False)
                panel.register(self.app_tree, app_item)
                self.app_panels.append(panel)

            self.app_tree.ExpandAll()

    def on_app_key_press(self, event):
        key_event = event.GetKeyEvent()
        key = key_event.GetKeyCode()
        if key == wx.WXK_NUMPAD_ENTER or key == wx.WXK_RETURN:
            selected_app = self.app_tree.GetSelection()
            app_panel = self.app_tree.GetPyData(selected_app)
            if app_panel:
                app_panel.on_run_toggle(None)
        else:
            event.Skip()  # Continue to default key handler

    def on_app_middle_click(self, event):
        app_panel = self.app_tree.GetPyData(event.GetItem())
        app_panel.on_run_toggle(None)

    def on_app_select(self, event):
        '''Called when an app is selected from the app tree.'''
        app_panel = self.app_tree.GetPyData(event.GetItem())
        self.display_app(app_panel)

    def display_app(self, app_panel):
        '''Displays the given panel in the right frame.'''
        if self.current_app_panel:
            self.current_app_panel.Show(False)
        self.panel_right_sizer.Clear(False)
        if app_panel:
            self.panel_right_sizer.Add(app_panel, 1, wx.EXPAND)
            app_panel.Show(True)
            app_panel.Layout()
        self.panel_right_sizer.Layout()
        self.current_app_panel = app_panel

    def on_close(self, event):
        for app in self.app_panels:
            app.stop()
        self.Destroy()


class AppPanel(wx.Panel):

    '''A self contained panel that represents a subprocess.

    :param parent_window:
    :param command:
    :param directory:
    :param default_args: TODO
    :param help_text: TODO
    :param single: TODO

    '''

    def __init__(self, parent_window, command, directory="", default_args="",
                 options=[], help_text=""):
        '''Initialize the panel and its children in this hierarchy:

        AppPanel
          |
          +- horizontal_box
              |
              +- vertical_box
                   |
                   +- control_box
                   |    |
                   |    +- run_button
                   |    |
                   |    +- argument_box
                   |    |
                   |    +- [other controls]
                   |
                   +- output_box

        '''
        wx.Panel.__init__(self, parent_window, -1)

        self.command = command
        self.option_controls = options
        self.pid = None
        self.stdout = None

        self.short_directory = directory
        head, tail = os.path.split(__file__)
        self.directory = os.path.abspath(os.path.join(head, directory))

        # control_box
        # Contains run_button and any other controls
        self.control_box = wx.BoxSizer(wx.HORIZONTAL)
        self.run_button = wx.ToggleButton(self, -1, "Run")
        self.run_button.Bind(wx.EVT_TOGGLEBUTTON, self.on_run_toggle)
        self.control_box.Add(self.run_button, 0, wx.ALIGN_LEFT)
        for i, control in enumerate(self.option_controls):
            control.register(self)
            if i is not 0:
                self.control_box.AddSpacer(10)
            self.control_box.Add(control, 0, wx.ALIGN_LEFT)

        # output_box to display app's stdout
        self.output_box = wx.TextCtrl(self, -1, '', style=
                                      wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH |
                                      wx.TE_NOHIDESEL | wx.TE_LEFT)
        self.output_box.SetDefaultStyle(
            wx.TextAttr("black", "white", wx.Font(8, wx.FONTFAMILY_TELETYPE,
                                                  wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL), False)
        )
        self.output_box.Fit()

        self.vertical_box = wx.BoxSizer(wx.VERTICAL)
        self.horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
        self.horizontal_box.Add(self.vertical_box, 1, wx.EXPAND)
        self.SetSizer(self.horizontal_box)

        self.vertical_box.Add(self.output_box, 1, wx.EXPAND)
        self.vertical_box.Add(self.control_box, 0, wx.SHRINK)

    def register(self, app_tree, tree_item):
        self.app_tree = app_tree
        self.tree_item = tree_item

    def on_run_toggle(self, event):
        if self.pid is None:
            self.run()
        else:
            self.stop()

    def run(self):

        command = copy(self.command)
        for control in self.option_controls:
            command += control.get_options()

        # Start Process
        self.pid, self.stdout = pty.fork()

        if self.pid == 0:  # Child

            # Close open file descriptors
            # This tidbit taken from pexpect
            max_fd = resource.getrlimit(resource.RLIMIT_NOFILE)[0]
            for i in xrange(3, max_fd):
                try:
                    os.close(i)
                except OSError:
                    pass

            os.chdir(self.directory)
            os.execvp(command[0], command)
            raise OSError("os.exec failed!")

        self.app_tree.SetItemBold(self.tree_item, True)
        self.run_button.SetLabel("Stop")
        self.output_box.SetValue(self.short_directory + " $ " + command_to_string(command) + "\n")

    def stop(self):
        if self.pid:
            try:
                os.kill(self.pid, signal.SIGINT)
            except OSError:  # Process doesn't exist
                pass

    def update(self):

        if self.pid:

            # Get stdout
            text = None
            if select.select([self.stdout], [], [], 0)[0]:
                try:
                    text = os.read(self.stdout, 65535)

                except OSError:
                    # Process exited
                    self.pid = None
                    self.stdout = None
                    self.app_tree.SetItemBold(self.tree_item, False)
                    self.run_button.SetValue(False)
                    self.run_button.SetLabel("Run")

                if text:
                    self.output_box.AppendText(text)


class AppOption(wx.Control):

    '''A user configurable option for an application.

    Instances will be displayed in their application panel.  The user can then
    change the value of an option and get_options is called when the app is
    run.
    '''

    def get_options(self):
        '''Return a list of command line options.'''
        raise NotImplementedError("This must be implemented by a subclass!")

    def register(self, panel):
        '''Called after the AppOption is passed to the AppPanel.

        This is nessesary because AppOptions are initialized before the
        AppPanel, even though the AppPanel needs to be given to the wx.Control
        superclass as the parent window.

        '''
        raise NotImplementedError("This must be implemented by a subclass!")


class CheckBoxOption(AppOption, wx.CheckBox):

    def __init__(self, on_value, off_value, text, default=False):
        '''

        :param on_value:
            The argument that will be included when running the program if the
            checkbox is checked.  No argument will be included if this
            evaluates to False.

        :param off_value:
            The argument that will be included when running the program if the
            checkbox is unchecked.  No argument will be included if this
            evaluates to False.

        :param text:
            The text displayed to the user next to the checkbox.

        :param default:
            If False (default), the checkbox will start unchecked.  If True, it
            will start checked.

        '''
        self.on_value = on_value
        self.off_value = off_value
        self.text = text
        self.default = default

    def register(self, panel):
        wx.CheckBox.__init__(self, panel, -1, self.text)
        self.SetValue(self.default)

    def get_options(self):

        if self.GetValue():
            value = self.on_value
        else:
            value = self.off_value

        if value:
            return [value]
        else:
            return []


class TextOption(AppOption, wx.Panel):

    def __init__(self, text, default="", option=None, ignore_empty=True):
        '''
        An AppOption that provides these options to the application:
            [option] <textbox value>

        :param text:
            The text displayed to the user next to the text box.

        :param default:
            The value of the text box before it is changed by the user.

        :param option:
            The option that will precede the textbox value.  If this evaluates
            to False, it will not be included.

        :param allow_empty:
            If True, an empty value will yield no arguments.  If False, an
            empty value will yield one empty argument.

        '''
        self.text = text
        self.default = default
        self.option = option
        self.ignore_empty = ignore_empty

    def register(self, panel):
        wx.Panel.__init__(self, panel, -1)
        self.text = wx.StaticText(self, -1, self.text)
        self.textbox = wx.TextCtrl(self, -1, self.default)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.text)
        self.sizer.Add(self.textbox)
        self.SetSizer(self.sizer)

    def get_options(self):
        value = self.textbox.GetValue()
        if value or not self.ignore_empty:
            if self.option:
                return [self.option, value]
            else:
                return [value]
        else:
            return []


class VisionCameraOption(AppOption, wx.Panel):

    def __init__(self):
        pass  # wx.Panel.__init__ will be called in self.register()

    def register(self, panel):
        wx.Panel.__init__(self, panel, -1)
        self.checkbox = wx.CheckBox(self, -1, "SVR")
        self.text = wx.StaticText(self, -1, "Camera:")
        self.textbox = wx.TextCtrl(self, -1, "")

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.checkbox)
        self.sizer.Add(self.text)
        self.sizer.AddSpacer(10)
        self.sizer.Add(self.textbox)
        self.SetSizer(self.sizer)

    def get_options(self):
        if self.checkbox.GetValue():  # Use SVR
            return [self.textbox.GetValue()]
        else:  # No SVR
            return ["camera", "-c", "camera", self.textbox.GetValue()]


class ConstantOption(AppOption):

    def __init__(self, option):
        self.option = option

    def register(self, panel):
        pass

    def get_options(self):
        return [option]


def command_to_string(command):
    result = []
    for arg in command:
        if " " in arg or not arg:
            arg = '"%s"' % arg
        result.append(arg)
    return " ".join(result)

if __name__ == "__main__":
    app = wx.App(0)
    frame = AppRunnerFrame(None, -1, "Application Runner", size=wx.Size(1000, 400))
    frame.Show(True)
    app.SetTopWindow(frame)
    app.MainLoop()
