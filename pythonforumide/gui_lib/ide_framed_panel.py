"""
Created on 31 Jul 2011

@author: D.W.
"""

import wx

class FramedPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        """ Creates a panel for displaying text """
        super(FramedPanel, self).__init__(*args, **kwargs)
        self._create_variables()

        sizer= wx.BoxSizer(wx.VERTICAL)

        self._create_header(sizer)
        self._create_textctrl(sizer)
        self.SetSizer(sizer)
        self.Layout()

    def _create_variables(self):
        self._parent= self.GetParent()
        self._parents_child_state= {}
       
        self._minimum_size= 26
        self._current_size= (-1, 50)
        self._maximized= False
        self._minimized= False
        
        self._drag_vertical= True
        self._sensitivity= 0.2
        self._header_pos= 0

    def _create_header(self, sizer):
##        header_sizer= wx.BoxSizer(wx.VERTICAL)
##        sizer.Add(header_sizer, 0, wx.EXPAND|wx.ALL, 2)

        ctrl= HeaderPanel(self, style= wx.BORDER_THEME|wx.TAB_TRAVERSAL)
        sizer.Add(ctrl, 0, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER, 2)
        self._header_panel= ctrl

    def _create_textctrl(self, sizer):
        ctrl= wx.TextCtrl(self, value= "Some text", style=wx.TE_MULTILINE|wx.TE_READONLY)
        sizer.Add(ctrl, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 2)
        self.textctrl= ctrl

    def set_text(self, text):
        self.textctrl.SetValue(text)

    def set_caption(self, text):
        self._header_panel._header_caption.SetLabel(" %s" % (text))

    def show(self, is_shown= True):
        self.Show(is_shown)
        self._parent.Layout()
        
    def get_parent_client_size(self):
        return self._parent.GetClientSize()
    
    def send_parent_size_evet(self):
        self._parent.SendSizeEvent()
    
    def get_own_client_size_tuple(self):
        return self.GetClientSizeTuple()
    
    def get_sizer_item(self):
        sizer= self.GetContainingSizer()
        return sizer.GetItem(self)
    
    def set_sizer_item_proportion(self, proportion):
        self.get_sizer_item().SetProportion(proportion)
        
    def set_size(self, width, height):
        sizer_item= self.get_sizer_item()
        sizer_item.SetMinSize((width, height))
        self.send_parent_size_evet()
        self._parent.Layout()
        self._parent.Update()
        self._parent.Refresh()
        
    def get_parents_children(self):
        return self._parent.GetChildren()
        
        
    def set_parents_childrens_state(self):
        for child_panel in self.get_parents_children():
            if child_panel != self:
                self._parents_child_state[child_panel]= child_panel.IsShown()
                
    def minimize(self):
        if self._maximized:
            self.restore()
        self.set_size(-1, self._minimum_size)
        self._minimized= True

    def maximize(self):
        self.set_parents_childrens_state()
        self._current_size= self.get_own_client_size_tuple()
        for child_panel, state in self._parents_child_state.iteritems():
            child_panel.Show(False) 
        self.set_sizer_item_proportion(1)
        self.set_size(-1, self.get_parent_client_size()[1])
        self._maximized= True
        self._minimized= False
        self._header_panel._btn_maximize.SetLabel("2")
        
    def restore(self):
        self.set_sizer_item_proportion(0)
        for child_panel, state in self._parents_child_state.iteritems():
            child_panel.Show(state)
        self.set_size(-1, self._current_size[1])
        self._maximized= False
        self._minimized= False
        self._header_panel._btn_maximize.SetLabel("1")

        
    
        




class FramedPanelEvents(object):
    """ Creates the events for framed panel"""
    def __init__(self, view, model = ""):
        """ Sets the view and model if one s required"""
        self.view = view
        self.model = model
        self._create_binds()
        
    def _create_binds(self):
        """ Creates the binds"""
##        self._header_panel.Bind(wx.EVT_MOUSE_EVENTS, self._on_mouse)

##        self._dragbar_top.Bind(wx.EVT_MOUSE_EVENTS, self._on_mouse)
##        self._dragbar_bottom.Bind(wx.EVT_MOUSE_EVENTS, self._on_mouse)
        header_panel= self.view._header_panel
        header_panel._btn_minimize.Bind(wx.EVT_BUTTON, self._on_btn_minimize)
        header_panel._btn_maximize.Bind(wx.EVT_BUTTON, self._on_btn_maximize)
        header_panel._btn_close.Bind(wx.EVT_BUTTON, self._on_btn_close)

#        self.timer = wx.Timer(self)
#        self.Bind(wx.EVT_TIMER, self._update_title)
#        self.timer.Start(40)  # in miliseconds
        
    def _on_mouse(self, event):
##        print "Mouse event"
        if event.LeftDown():
##            print "mouse event left down"
            if self._drag_vertical:
                self._header_pos= event.GetPosition()[1]
            else:
                self._header_pos= event.GetPosition()[0]
        elif event.Dragging():
##            print "Mouse dragging"
            x, y = self.ScreenToClient(self._header_panel.ClientToScreen(event.GetPosition()))
            if self._drag_vertical:
                change=  ((y- self._header_pos)*-1)*self._sensitivity
            else:
                change=  ((x- self._header_pos))*self._sensitivity
            newsize= self.GetSize()[1]+change
            if newsize> self._minimum_size:
                self.SetSizeHints(-1, newsize)
                self._parent.SendSizeEvent()
                self._current_size= newsize
##        elif event.ButtonDClick():
##            new_size= self.GetClientSize()[0]
##            print "Mouse doubleclick currentsize: %s" % (self._current_size)
##            print "Actual size: %s" % (self.GetSize())
##            if not self._maximized:
##                self.SetSizeHints(-1, new_size)
##                self._maximized= True
##            else:
##                self.SetSizeHints(-1, self._current_size)
##                self._maximized= False
##            self.SendSizeEventToParent()

        event.Skip()

    def _on_btn_close(self, event):
        self.view.show(False)

    def _on_btn_minimize(self, event):
        self.view.minimize()


    def _on_btn_maximize(self, event):
        if not self.view._maximized:
            self.view.maximize()
        else:
            self.view.restore()
        
        

    def _update_title(self, event):
         pos = wx.GetMousePosition()
         csize= self.GetClientSizeTuple()
##         cpos= self.GetPositionTuple()
##         client_to_screen= self.ClientToScreen(cpos)
         client_to_screen= self.GetScreenPosition()
         panel_top = client_to_screen[1]
         panel_bottom= panel_top+csize[1]
         panel_left= client_to_screen[0]
         panel_right= panel_left+csize[0]
         in_width= pos[0]>= panel_left and pos[0]<= panel_right
         if pos[1] in xrange(panel_top-5, panel_top+5):
            toporbot= "At the top"
         elif pos[1]in xrange(panel_bottom-5, panel_bottom+5):
            toporbot= "At the Bottom"
         else:
            toporbot= "Neither"
         text = "Window client size: %s \ client to screen pos: %s \n top: %s bottom: %s left: %s Right: %s inwidth: %s toporbottom: %s" % (csize, client_to_screen, panel_top, panel_bottom, panel_left, panel_right, in_width, toporbot)
         self.set_text(text)
         self.set_caption("Your mouse is at (%s, %s)" % (pos.x, pos.y))
         cur_cursor= self.GetCursor()
         if in_width and toporbot!= "Neither":
            cursor = wx.StockCursor(wx.CURSOR_SIZENS)
         else:
            cursor= wx.StockCursor(wx.CURSOR_DEFAULT)
         if cur_cursor!= cursor:
            self.SetCursor(cursor)



class HeaderPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        """ Creates a panel for displaying text """
        super(HeaderPanel, self).__init__(*args, **kwargs)
        self._button_font= wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              u'Webdings')
        sizer= wx.BoxSizer(wx.HORIZONTAL)
        self._create_statictxt(sizer)
        self._create_minimize(sizer)
        self._create_maximize(sizer)
        self._create_close(sizer)

        self.SetSizer(sizer)
        self.Layout()

    def _create_statictxt(self, sizer):
        ctrl= wx.StaticText(self, label= " Console")
        font= ctrl.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        ctrl.SetFont(font)
        sizer.Add(ctrl, 0, flag= wx.ALIGN_CENTER_VERTICAL)
        self._header_caption= ctrl

    def _create_minimize(self, sizer):
        sizer.AddStretchSpacer(1)
        ctrl= wx.Button(self, label= "0", size= (19, 19))
        ctrl.SetFont(self._button_font)
        sizer.Add(ctrl, 0, wx.ALIGN_RIGHT)
        self._btn_minimize= ctrl

    def _create_maximize(self, sizer):
        ctrl= wx.Button(self, label= "1", size= (19, 19))
        ctrl.SetFont(self._button_font)
        sizer.Add(ctrl, 0, wx.ALIGN_RIGHT)
        self._btn_maximize= ctrl
        # restore = 2

    def _create_close(self, sizer):
        ctrl= wx.Button(self, label= "r", size= (19, 19))
        ctrl.SetFont(self._button_font)
        sizer.Add(ctrl, 0, wx.ALIGN_RIGHT)
        self._btn_close= ctrl





if __name__=='__main__':
    import ide_test_app as wx_app
    from ide_simple_frame import SimpleFrame, SimplePanel
    app = wx_app.Wx_App(False)
    frame= SimpleFrame(None, title= "Testing TextPanel without events")
    panel= SimplePanel(frame)
    frame.sizer.Add(panel, 1, wx.EXPAND)
    panel_black= wx.Panel(panel)
    panel_black.SetBackgroundColour((0, 0,0 ))
    panel.sizer.Add(panel_black, 1, wx.EXPAND)
    frame.panel_black= panel_black
    

    text_panel= FramedPanel(panel)
    FramedPanelEvents(text_panel)
    panel.sizer.Add(text_panel, 0, wx.EXPAND)
    text_panel.set_caption("New Title")

    text_panel= FramedPanel(panel)
    FramedPanelEvents(text_panel)
    panel.sizer.Add(text_panel, 0, wx.EXPAND)
    text_panel= FramedPanel(panel)
    FramedPanelEvents(text_panel)
    panel.sizer.Add(text_panel, 0, wx.EXPAND)
    text_panel= FramedPanel(panel)
    FramedPanelEvents(text_panel)
    panel.sizer.Add(text_panel, 0, wx.EXPAND)

    frame.Layout()
    
    
    app.MainLoop()
    
    