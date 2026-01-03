from dumbdisplay import *
from dumbdisplay_examples.tamagotchi.common import Button, Panel, StageBase
from dumbdisplay_examples.tamagotchi.sound import play_button_sound
from dumbdisplay_examples.utils import DDAppBase

# _background_menu_0_image_name = "gifMenu-0.png"
# _background_menu_1_image_name = "gifMenu-1.png"
_background_menu_image_name_prefix = "gifMenu-"
_background_menu_image_name_count = 2
_background_menu_image_name = "gifMenu-##0-1##.png"  # encoded for animation

_logika_label = Button(70, 60, 100, 100, "logika.png")
#_logika_label = Button(0, 0, 100, 100, "logika.png")
_start_btn = Button(140, 150, 200, 50, "buttonLong_brown.png", "Start")
#_start_btn = Button(750, 0, 200, 50, "buttonLong_brown.png", "Start")
_rule_btn = Button(140, 250, 200, 50, "buttonLong_brown.png", "Help")
_exit_btn = Button(140, 350, 200, 50, "buttonLong_brown.png", "Exit")

# _help_menu = Panel(25, 50, 750, 400, "panel_brown.png",
# """You have to keep
# the indicators normal.
# If at least one of them
# is equal to zero,
# you will lose.
#
# Good Luck!""")
_help_menu = Panel(400, 250, 750, 450, "panel_brown.png",
"""You have to keep
the indicators normal.
If at least one of them
is equal to zero,
you will lose.

Good Luck!""")


_menu_buttons = [_logika_label, _start_btn, _rule_btn, _exit_btn]


def get_menu_stage_image_names():
    image_names = []
    for i in range(_background_menu_image_name_count):
        image_name = f"{_background_menu_image_name_prefix}{i}.png"
        image_names.append(image_name)
    #image_names = [_background_menu_0_image_name, _background_menu_1_image_name]
    image_names += _help_menu.get_image_names()
    for menu_button in _menu_buttons:
        image_names.append(menu_button.image_name)
    return image_names

def setup_menu_stage_layer(app: DDAppBase, menu_stage_layer: LayerGraphical) -> 'MenuStage':
    _help_menu.initialize(menu_stage_layer, init_visible=False)
    for menu_button in _menu_buttons:
        menu_button.initialize(menu_stage_layer)
    menu_stage_layer.backgroundImage(_background_menu_image_name)
    menu_stage_layer.animateBackgroundImage(0.7)
    return MenuStage(app, menu_stage_layer)



class MenuStage(StageBase):
    def __init__(self, app: DDAppBase, stage_layer: LayerGraphical):
        super().__init__(app, stage_layer)

    def handle_clicked(self, pos_x: int, pos_y: int):
        if _help_menu.is_visible():
            if _help_menu.check_clicked_cross(pos_x, pos_y):
                play_button_sound()
                _help_menu.set_visible(False)
        else:
            if _logika_label.check_clicked(pos_x, pos_y):
                #print("Logika label clicked")
                pass
            elif _start_btn.check_clicked(pos_x, pos_y):
                #print("Start button clicked")
                play_button_sound()
                self.app.handleStartGame()
            elif _rule_btn.check_clicked(pos_x, pos_y):
                #print("Help button clicked")
                play_button_sound()
                _help_menu.set_visible(True)
            elif _exit_btn.check_clicked(pos_x, pos_y):
                #print("Exit button clicked")
                self.app.masterReset()
