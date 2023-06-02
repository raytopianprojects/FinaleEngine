from entity import Entity
from window import window
from direct.gui.DirectGui import DirectButton, DirectEntry, DirectFrame, DirectLabel, DirectDialog, DirectSlider, \
    DirectWaitBar, DirectScrollBar, DirectEntryScroll, DirectScrolledFrame, DirectScrolledList, DirectScrolledListItem, \
    DirectCheckButton, DirectRadioButton, DirectOptionMenu


class Button(Entity):
    def __init__(self, name="Button"):
        super().__init__(name)
        self.reparent_to(window.render2d.aspect2d)
        self._button = DirectButton(parent=self)
