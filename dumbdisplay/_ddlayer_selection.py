from ._ddlayer import DDLayer, _DD_INT_ARG, _DD_FLOAT_ARG
from ._ddlayer import _DD_BOOL_ARG
from ._ddlayer import _DD_COLOR_ARG

class DDLayerSelection(DDLayer):
    '''Selection'''
    def __init__(self, dd,
                 col_count: int = 16, row_count: int = 2,
                 hori_selection_count: int = 1, vert_selection_count: int = 1,
                 char_height: int = 0, font_name: str = "",
                 can_draw_dots: bool = True, selection_border_size_char_height_factor: float = 0.3):
        layer_id = dd._createLayer("selection", _DD_INT_ARG(col_count), _DD_INT_ARG(row_count),
                                   _DD_INT_ARG(hori_selection_count), _DD_INT_ARG(vert_selection_count),
                                   _DD_INT_ARG(char_height), font_name,
                                   _DD_BOOL_ARG(can_draw_dots), _DD_FLOAT_ARG(selection_border_size_char_height_factor))
        super().__init__(dd, layer_id)
    def text(self, text: str, y: int = 0, hori_selection_idx: int = 0, vert_selection_idx: int = 0, align: str = "L"):
        '''
        set a "selection" unit text (of y-th row)
        :param align 'L', 'C', or 'R'
        '''
        self.dd._sendCommand(self.layer_id, "text", _DD_INT_ARG(y), _DD_INT_ARG(hori_selection_idx), _DD_INT_ARG(vert_selection_idx), align, text)
    def textCentered(self, text: str, y: int = 0, hori_selection_idx: int = 0, vert_selection_idx: int = 0):
        '''
        set a "selection" unit centered text (of y-th row)
        '''
        self.dd._sendCommand(self.layer_id, "text", _DD_INT_ARG(y), _DD_INT_ARG(hori_selection_idx), _DD_INT_ARG(vert_selection_idx), "C", text)
    def textRightAligned(self, text: str, y: int = 0, hori_selection_idx: int = 0, vert_selection_idx: int = 0):
        '''
        set a "selection" unit right-aligned text (of y-th row)
        '''
        self.dd._sendCommand(self.layer_id, "text", _DD_INT_ARG(y), _DD_INT_ARG(hori_selection_idx), _DD_INT_ARG(vert_selection_idx), "R", text)
    def unselectedText(self, text: str, y: int = 0, hori_selection_idx: int = 0, vert_selection_idx: int = 0, align: str = "L"):
        '''
        set a "selection" unit text (of y-th row) when unselected (it defaults to the same text as selected)
        :param align 'L', 'C', or 'R'
        '''
        self.dd._sendCommand(self.layer_id, "unselectedtext", _DD_INT_ARG(y), _DD_INT_ARG(hori_selection_idx), _DD_INT_ARG(vert_selection_idx), align, text)
    def unselectedTextCentered(self, text: str, y: int = 0, hori_selection_idx: int = 0, vert_selection_idx: int = 0):
        '''
        set a "selection" unit centered text (of y-th row) when unselected (it defaults to the same text as selected)
        '''
        self.dd._sendCommand(self.layer_id, "unselectedtext", _DD_INT_ARG(y), _DD_INT_ARG(hori_selection_idx), _DD_INT_ARG(vert_selection_idx), "C", text)
    def unselectedTextRightAligned(self, text: str, y: int = 0, hori_selection_idx: int = 0, vert_selection_idx: int = 0):
        '''
        set a "selection" unit right-aligned text (of y-th row) when unselected (it defaults to the same text as selected)
        '''
        self.dd._sendCommand(self.layer_id, "unselectedtext", _DD_INT_ARG(y), _DD_INT_ARG(hori_selection_idx), _DD_INT_ARG(vert_selection_idx), "R", text)
    def select(self, hori_selection_idx: int = 0, vert_selection_idx: int = 0, deselect_the_others: bool = True):
        '''
        select a "selection" unit
        :param deselect_the_others: if True, deselect the others
        '''
        self.dd._sendCommand(self.layer_id, "select", _DD_INT_ARG(hori_selection_idx), _DD_INT_ARG(vert_selection_idx), _DD_BOOL_ARG(deselect_the_others))
    def deselect(self, hori_selection_idx: int = 0, vert_selection_idx: int = 0, select_the_others: bool = False):
        '''
        deselect a "selection" unit
        :param select_the_others: if True, select the others
        '''
        self.dd._sendCommand(self.layer_id, "deselect", _DD_INT_ARG(hori_selection_idx), _DD_INT_ARG(vert_selection_idx), _DD_BOOL_ARG(select_the_others))
    def selected(self, selected: bool, hori_selection_idx: int = 0, vert_selection_idx: int = 0, reverse_the_others: bool = False):
        '''
        set a "selection" unit selected or not (combination of select() and deselect())
        :param reverse_the_others: if True, reverse the others
        '''
        if selected:
            self.dd._sendCommand(self.layer_id, "select", _DD_INT_ARG(hori_selection_idx), _DD_INT_ARG(vert_selection_idx), _DD_BOOL_ARG(reverse_the_others))
        else:
            self.dd._sendCommand(self.layer_id, "deselect", _DD_INT_ARG(hori_selection_idx), _DD_INT_ARG(vert_selection_idx), _DD_BOOL_ARG(reverse_the_others))



