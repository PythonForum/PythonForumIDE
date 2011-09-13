"""
Created on 3 Aug 2011

@author: Dave Wilson, David
"""

import wx

class HeaderPanel(wx.Panel):
    """Header Panel Class, with events and GUI creation"""

    def __init__(self, *args, **kwargs):
        """ Creates headered panel with Minimize/Maximize & Close buttons """
        super(HeaderPanel, self).__init__(*args, **kwargs)
        self._create_variables()
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self._create_statictxt(sizer)
        self._create_minimize(sizer)
        self._create_maximize(sizer)
        self._create_close(sizer)
        self.SetSizer(sizer)
        self.Layout()

    def _create_variables(self):
        """ Creates variables for internal use only"""
        self._button_font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
                                    u'Webdings')

    def _create_statictxt(self, sizer):
        """ Create header label"""
        ctrl = wx.StaticText(self, label=" Console")
        font = ctrl.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        ctrl.SetFont(font)
        sizer.Add(ctrl, 0, flag=wx.ALIGN_CENTER_VERTICAL)
        self.header_caption = ctrl

    def _create_minimize(self, sizer):
        """Creates the Minimize button"""
        sizer.AddStretchSpacer(1)
        ctrl = wx.Button(self, label="0", size=(19, 19))
        ctrl.SetFont(self._button_font)
        ctrl.SetToolTipString("Minimize")
        sizer.Add(ctrl, 0, wx.ALIGN_RIGHT)
        self.btn_minimize = ctrl

    def _create_maximize(self, sizer):
        """Creates the Maximize button"""
        ctrl = wx.Button(self, label="1", size=(19, 19))
        ctrl.SetFont(self._button_font)
        ctrl.SetToolTipString("Maximize")
        sizer.Add(ctrl, 0, wx.ALIGN_RIGHT)
        self.btn_maximize = ctrl
        # restore = 2

    def _create_close(self, sizer):
        """Creates the Close button"""
        ctrl = wx.Button(self, label="r", size=(19, 19))
        ctrl.SetFont(self._button_font)
        ctrl.SetToolTipString("Close")
        sizer.Add(ctrl, 0, wx.ALIGN_RIGHT)
        self.btn_close = ctrl

class HeaderedPanel(wx.Panel):
    """Headered Panel class"""

    def __init__(self, *args, **kwargs):
        """ Creates a panel for displaying text """
        super(HeaderedPanel, self).__init__(*args, **kwargs)
        self._create_variables()
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self._create_header_panel()
        self.SetSizer(self.sizer)
        self.Layout()

    def _create_variables(self):
        """Creates GUI variables for components"""
        self.child_panel = None
        self._proportion = None
        self._minimized = False
        self._parent_frame = None

    def _create_header_panel(self):
        """ Creates the header panel"""
        ctrl = HeaderPanel(self, style=wx.BORDER_THEME)
        self.sizer.Add(ctrl, 0, wx.EXPAND | wx.ALL, 1)
        self.header_panel = ctrl

    def add_panel_ctrl(self, panel_class, caption="", proportion=1):
        """Adds a panel to the GUI"""
        self.Freeze()
        ctrl = panel_class(self)
        self.sizer.Add(ctrl, 1, wx.EXPAND | wx.ALL, 0)
        self._update_layout()
        self.child_panel = ctrl
        self._proportion = proportion
        self._set_own_proportion(proportion)
        self.set_caption(caption)
        self.Thaw()
        return ctrl

    def _update_layout(self):
        """Refresh/Update layout of the IDE"""
        parent = self.GetParent()
        parent.Layout()
        parent.Update()
        parent.Refresh()
        self.Layout()

    def _set_restore_state(self):
        """Defines the restore state"""
        self.header_panel.btn_maximize.SetLabel("2")

    def _set_after_restore(self):
        """Defines state after restore"""
        self.header_panel.btn_maximize.SetLabel("1")

    def _get_items_sizer(self, item):
        """Gets the items in a sizer"""
        sizer = item.GetContainingSizer()
        return sizer.GetItem(self)

    def _set_own_proportion(self, proportion):
        """Defines the proportion of a sizer"""
        self._get_items_sizer(self).SetProportion(proportion)

    def show(self, show=True):
        """Shows a component"""
        self.Show(show)
        self._update_layout()

    def show_child(self, show=True):
        """Show a child component"""
        self.child_panel.Show(show)

    def _set_no_child_state(self):
        """Sets a no_child_state to a component"""
        self.header_panel.btn_maximize.SetLabel("2")
        self._set_own_proportion(0)
        self._update_layout()
        self._minimized = True

    def minimized_state(self):
        """Checks the minimized state"""
        if not self.child_panel:
            return
        self.show_child(False)
        self.header_panel.btn_maximize.SetLabel("2")
        self.header_panel.btn_maximize.SetToolTipString("Restore")

        self._set_own_proportion(0)
        self._update_layout()
        self._minimized = True

    def restore_state(self):
        """Restores state of component"""
        if not self.child_panel:
            return
        if self._minimized:
            self.show_child(True)
            self.header_panel.btn_maximize.SetLabel("1")
            self.header_panel.btn_maximize.SetToolTipString("Maximize")
            self._set_own_proportion(self._proportion)
            self._update_layout()
            self._minimized = False
        else:
            self._move_child_to_a_frame()

    def close(self):
        """Closes a component"""
        if not self.child_panel:
            return
        self.show(False)

    def _move_child_to_a_frame(self):
        """Move a child component to a frame"""
        self.sizer.Detach(self.child_panel)
        self.show(False)
        self._parent_frame = ParentFrame(self, title=self._get_caption())
        self._parent_frame.add_child(self.child_panel, self)

    def set_caption(self, text):
        """Define the caption of a component"""
        self.header_panel.header_caption.SetLabel(" %s" % (text))

    def _get_caption(self):
        """Get caption of a component"""
        return self.header_panel.header_caption.GetLabel()

class HeaderedPanelEvents(object):
    """Headered Panel Events class, handles events"""

    def __init__(self, view, model=''):
        """Initiates the panel, calls event binding functions"""
        self.view = view
        self.model = model
        self._create_variables()
        self._create_binds()

    def _create_variables(self):
        """Creates GUI_related variables"""
        header_panel = self.view.header_panel
        self.btn_minimize = header_panel.btn_minimize
        self.btn_maximize = header_panel.btn_maximize
        self.btn_close = header_panel.btn_close
#       self.header_panel= self.view.header_panel

    def _create_binds(self):
        """Defines binds"""
        self.btn_minimize.Bind(wx.EVT_BUTTON, self._on_btn_minimize)
        self.btn_maximize.Bind(wx.EVT_BUTTON, self._on_btn_maximize)
        self.btn_close.Bind(wx.EVT_BUTTON, self._on_btn_close)

    def _on_btn_minimize(self, event):
        """Handles minimize button"""
        self.view.minimized_state()

    def _on_btn_maximize(self, event):
        """Handles maximizing button"""
        self.view.restore_state()

    def _on_btn_close(self, event):
        """Handles closing event with button"""
        self.view.close()

class ParentFrame(wx.Frame):
    """Frame to use for testing"""
    def __init__(self, *args, **kwargs):
        """Initiates the frame and the GUI"""
        super(ParentFrame, self).__init__(*args, **kwargs)
        self.SetInitialSize(kwargs.get("size", (600, 600)))
        self.Center(wx.BOTH)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.Bind(wx.EVT_CLOSE, self._on_close)

    def add_child(self, child_panel, parent_window):
        """Handles child_panel to parent_window"""
        self._child_panel = child_panel
        self._parent_window = parent_window
        child_panel.Reparent(self)
        self.sizer.Add(child_panel, 1, wx.EXPAND)
        self.Layout()
        self.Show()
#       self.Maximize()

    def _move_child_back(self):
        """Removes a child_panel back"""
        self.sizer.Detach(self._child_panel)
        self._child_panel.Reparent(self._parent_window)
        self._parent_window.sizer.Add(self._child_panel, 1, wx.EXPAND | wx.ALL, 0)
        self._parent_window.show(True)
        self._parent_window._parent_frame = None

    def _on_close(self, event):
        """Handles closing event"""
        self._move_child_back()
        event.Skip()
