'''
Created on 3 Aug 2011

@author: Dave Wilson
'''

import wx

class HeaderPanel(wx.Panel):
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
        """ Creates the Minimize button"""
        sizer.AddStretchSpacer(1)
        ctrl = wx.Button(self, label="0", size=(19, 19))
        ctrl.SetFont(self._button_font)
        ctrl.SetToolTipString("Minimize")
        sizer.Add(ctrl, 0, wx.ALIGN_RIGHT)
        self.btn_minimize = ctrl

    def _create_maximize(self, sizer):
        """ Creates the Maximize button"""
        ctrl = wx.Button(self, label="1", size=(19, 19))
        ctrl.SetFont(self._button_font)
        ctrl.SetToolTipString("Maximize")
        sizer.Add(ctrl, 0, wx.ALIGN_RIGHT)
        self.btn_maximize = ctrl
        # restore = 2

    def _create_close(self, sizer):
        """ Creates the Close button"""
        ctrl = wx.Button(self, label="r", size=(19, 19))
        ctrl.SetFont(self._button_font)
        ctrl.SetToolTipString("Close")
        sizer.Add(ctrl, 0, wx.ALIGN_RIGHT)
        self.btn_close = ctrl

        
class HeaderedPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        """ Creates a panel for displaying text """
        super(HeaderedPanel, self).__init__(*args, **kwargs)
        self._create_variables()
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self._create_header_panel()
        self.SetSizer(self.sizer)
        self.Layout()
         
    def _create_variables(self):
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
        parent = self.GetParent()
        parent.Layout()
        parent.Update()
        parent.Refresh()
        self.Layout()
        
    def _set_restore_state(self):
        self.header_panel.btn_maximize.SetLabel("2")
        
    def _set_after_restore(self):
        self.header_panel.btn_maximize.SetLabel("1")
        
    def _get_items_sizer(self, item):
        sizer = item.GetContainingSizer()
        return sizer.GetItem(self)
    
    def _set_own_proportion(self, proportion):
        self._get_items_sizer(self).SetProportion(proportion)
        

    
    def show(self, show=True):
        self.Show(show)
        self._update_layout()
        
    def show_child(self, show=True):
        self.child_panel.Show(show)
        
    def _set_no_child_state(self):
        self.header_panel.btn_maximize.SetLabel("2")
        self._set_own_proportion(0)
        self._update_layout()
        self._minimized = True
        
    def minimized_state(self):
        if not self.child_panel:
            return
        self.show_child(False)
        self.header_panel.btn_maximize.SetLabel("2")
        self.header_panel.btn_maximize.SetToolTipString("Restore")
        
        self._set_own_proportion(0)
        self._update_layout()
        self._minimized = True
        
    def restore_state(self):
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
        if not self.child_panel:
            return
        self.show(False)
        
    def _move_child_to_a_frame(self):
        self.sizer.Detach(self.child_panel)
        self.show(False)
        self._parent_frame = ParentFrame(self, title=self._get_caption())
        self._parent_frame.add_child(self.child_panel, self)
        

    def set_caption(self, text):
        self.header_panel.header_caption.SetLabel(" %s" % (text))
        
    def _get_caption(self):
        return self.header_panel.header_caption.GetLabel()
        

    
class HeaderedPanelEvents(object):
    def __init__(self, view, model=""):
        self.view = view
        self.model = model
        self._create_variables()
        self._create_binds()
        
    def _create_variables(self):
        header_panel = self.view.header_panel
        self.btn_minimize = header_panel.btn_minimize
        self.btn_maximize = header_panel.btn_maximize
        self.btn_close = header_panel.btn_close
#        self.header_panel= self.view.header_panel
        
    def _create_binds(self):
        self.btn_minimize.Bind(wx.EVT_BUTTON, self._on_btn_minimize)
        self.btn_maximize.Bind(wx.EVT_BUTTON, self._on_btn_maximize)
        self.btn_close.Bind(wx.EVT_BUTTON, self._on_btn_close)
        
    def _on_btn_minimize(self, event):
        self.view.minimized_state()
        
    def _on_btn_maximize(self, event):
        self.view.restore_state()
    
    def _on_btn_close(self, event):
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
        self._child_panel = child_panel
        self._parent_window = parent_window
        child_panel.Reparent(self)
        self.sizer.Add(child_panel, 1, wx.EXPAND)
        self.Layout()
        self.Show()
#        self.Maximize()
        
    def _move_child_back(self):
        self.sizer.Detach(self._child_panel)
        self._child_panel.Reparent(self._parent_window)
        self._parent_window.sizer.Add(self._child_panel, 1, wx.EXPAND | wx.ALL, 0)
        self._parent_window.show(True)
        self._parent_window._parent_frame = None
        
        
    def _on_close(self, event):
        self._move_child_back()
        event.Skip()
        
       
             
class TestTextPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        """ Creates a panel for with a TextCtrl """
        super(TestTextPanel, self).__init__(*args, **kwargs)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self._create_textctrl()

        
        self.SetSizer(self.sizer)
        self.Layout()
        
    def _create_textctrl(self):     
        ctrl = wx.TextCtrl(self,
                          size=(-1, 300)
                          )
        self.sizer.Add(ctrl, 1, wx.EXPAND | wx.ALL, 1)
        
        
if __name__ == '__main__':
    from ide_simple_frame import SimpleFrame, SimplePanel
    app = wx.App(None)
    frame = SimpleFrame(None, title="Test frame")
    
    s_panel = SimplePanel(frame)
    frame.sizer.Add(s_panel, 1, wx.EXPAND)
    
    parent = s_panel
    
    panel = HeaderedPanel(parent, style=wx.BORDER_THEME)
    HeaderedPanelEvents(panel)
    parent.sizer.Add(panel, 0, wx.EXPAND)
    panel.add_panel_ctrl(TestTextPanel, "Panel1", 1)
    panel.minimized_state()
    panel.set_caption("Panel1 has proportion 1 and set minimized")
    
    panel = HeaderedPanel(parent, style=wx.BORDER_THEME)
    HeaderedPanelEvents(panel)
    parent.sizer.Add(panel, 1, wx.EXPAND)
    panel.add_panel_ctrl(TestTextPanel, "Panel2", 2)
    panel.set_caption("Panel1 has proportion 2")
    
    panel = HeaderedPanel(parent, style=wx.BORDER_THEME)
    HeaderedPanelEvents(panel)
    parent.sizer.Add(panel, 1, wx.EXPAND)
    panel.add_panel_ctrl(TestTextPanel, "Panel3", 3)
    panel.set_caption("Panel1 has proportion 3")
    

    frame.Layout()
    app.MainLoop()
