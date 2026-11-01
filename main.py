#-----------------------------------------------------------------------
# IMPORTS
#-----------------------------------------------------------------------
from graphics import Canvas
from time import sleep
import random

CANVAS_WIDTH = 697
CANVAS_HEIGHT = 420


#------------------------------------------------------------------------
# CONSTANTS
#------------------------------------------------------------------------

#---| OBJECT DICTIONARY |---
# key = object name, value = (obj_x, obj_y, obj_w, obj_h, target_x, target_y)
objects = {
    "table1": (35, 277, 180, 140, 180, 220),
    "table2": (301, 284, 195, 128, 232, 220),
    "bar":    (455, 206, 230, 174, 420, 200)
}


#---| JELLY'S STARTING POSITION (top-left coordinates) |---
JELLY_START_X = 420
JELLY_START_Y = 200


#---| TABLE1 ORDERING & DELIVERING CLOCHE |---
# Jelly's target position when delivering the cloche to table1 (both rounds)
TABLE1_DELIVERY_X = 134
TABLE1_DELIVERY_Y = 251
CLOCHE_LAND_X = 91
CLOCHE_LAND_Y = 258


#---| TABLE2 ORDERING & DELIVERING CLOCHE |---
# Jelly's target position when taking table2's order in round 1 (slug)
TABLE2_ORDER_X   = 232
TABLE2_ORDER_Y   = 220

# Round 2 (Karel): Jelly walks east to the waypoint, then turns west to the final target
KAREL_WAYPOINT_X = 416
KAREL_WAYPOINT_Y = 220
KAREL_ORDER_X = 424
KAREL_ORDER_Y = 234

# Jelly's target position when delivering the cloche to table2
TABLE2_DELIVERY_X = 410
TABLE2_DELIVERY_Y = 259
CLOCHE2_LAND_X = 361
CLOCHE2_LAND_Y = 261


#---| MENU ITEM FLOATS & BUTTONS |---

# Images that float above customers' heads when they order
MENU_ITEMS = [
    "Pizza_Float.png",
    "burger_float.png",
    "fries_float.png",
    "soup_float.png",
    "doughnut_float.png",
    "icecream_float.png",
    "cookie_float.png",
    "pancake_float.png",
    "cake_float.png",
    "spaghetti_float.png",
    "green_drink_float.png",
    "redYellowDrink_float.png",
    "blue_drink_float.png",
    "rainbow_drink_float.png",
    "blue_purple_drink_float.png"
]

# Maps each floating item image to its button on the menu overlay (used to mark the player's order)
FLOAT_TO_BUTTON = {
    "burger_float.png":            "burger_button",
    "fries_float.png":             "fries_button",
    "Pizza_Float.png":             "pizza_button",
    "spaghetti_float.png":         "spaghetti_button",
    "soup_float.png":              "soup_button",
    "icecream_float.png":          "icecream_button",
    "doughnut_float.png":          "doughnut_button",
    "pancake_float.png":           "pancakes_button",
    "cake_float.png":              "cake_button",
    "cookie_float.png":            "cookie_button",
    "rainbow_drink_float.png":     "rainbowDrink_button",
    "blue_drink_float.png":        "blueDrink_button",
    "redYellowDrink_float.png":    "redYellowDrink_button",
    "green_drink_float.png":       "greenDrink_button",
    "blue_purple_drink_float.png": "bluePurpleDrink_button",
}

# (button_name, unselected_x, unselected_y, selected_x, selected_y)
MENU_BUTTONS = [
    ("burger_button",           106, 82,  106, 82),
    ("fries_button",            206, 80,  207, 82),
    ("pizza_button",            308, 79,  309, 80),
    ("spaghetti_button",        410, 78,  410, 80),
    ("soup_button",             511, 81,  511, 79),
    ("icecream_button",         105, 176, 104, 175),
    ("doughnut_button",         206, 175, 207, 174),
    ("pancakes_button",         309, 176, 309, 175),
    ("cake_button",             409, 174, 410, 175),
    ("cookie_button",           512, 176, 511, 176),
    ("rainbowDrink_button",     105, 270, 105, 270),
    ("blueDrink_button",        207, 271, 207, 271),
    ("redYellowDrink_button",   309, 272, 309, 272),
    ("greenDrink_button",       410, 271, 410, 271),
    ("bluePurpleDrink_button",  512, 271, 512, 270),
]

SUBMIT_BUTTON_X = 263
SUBMIT_BUTTON_Y = 368

# How long each ordered item floats above the customer (~3 seconds)
FRAMES_PER_ITEM = 100

# Position of floating menu items and result icons above each table
FLOAT_X_TABLE1 = 78
FLOAT_Y_TABLE1 = 75
FLOAT_X_TABLE2 = 340
FLOAT_Y_TABLE2 = 75


# The game runs at ~33 frames per second (matches sleep(0.03) in the main loop)
FRAMES_PER_SECOND = int(1 / 0.03)


#---| MENU OVERLAY |---
MENU_OVERLAY_SECONDS = 1000
MENU_OVERLAY_FRAMES = MENU_OVERLAY_SECONDS * FRAMES_PER_SECOND


#--- | RESULT FLOATS |---
# ~2.7 seconds to show tick/cross above table
RESULT_DISPLAY_FRAMES = 90


#--- | FLASHING HALOS & SELECT HALOS |---
FLASH_TOGGLE_FRAMES = 8     # 2 flashes per second at 33fps
SELECT_HALO_FRAMES = 16     # 0.5 seconds at 33fps


#--- | ROUND OVERLAYS |---
ROUND_OVERLAY_FRAMES = 66   # 2 seconds at 33fps


#--- | SUMMARY RESULT ICONS |---
# Positions of each customer's result icon on the ending overlay
SUMMARY_ICON_POSITIONS = {
    "warthog": (36,  128),
    "slug":    (36,  240),
    "octopus": (571, 128),
    "karel":   (571, 240),
}


#---| SPLASH SCREEN |---
SPLASH_FRAMES = 99     # ~3 seconds at 33fps

#---| LIFT CONSTANTS |---
LIFT_LEFT_DOOR_X  = 261
LIFT_LEFT_DOOR_Y  = 157
LIFT_RIGHT_DOOR_X = 286
LIFT_RIGHT_DOOR_Y = 158


#---------------------------------------------------------------------------
# THE STATE DICTIONARY
#---------------------------------------------------------------------------

state = {
    "x": JELLY_START_X, "y": JELLY_START_Y,
    "target_x": 444, "target_y": 218,
    "moving": False,
    "speed": 5,                 # pixels per frame
    "selected": None,           # which object Jelly is walking to
    "score": 0,

    "round": 1,                 # 1 or 2
    "current_customer": 1,      # 1 = table1 customer, 2 = table2 customer

    # Ordering sequence
    "ordering": False,
    "order_items": [],
    "order_index": 0,           # which item of the order is currently floating
    "order_timer": 0,
    "order_complete": False,
    "current_order": [],

    # Menu overlay (shown at chef/bar)
    "menu_open": False,
    "menu_timer": 0,
    # A set because order doesn't matter and duplicates aren't allowed
    "player_selection": set(),
    "order_prepared": False,

    # Tick or cross above the table
    "showing_result": False,
    "result_timer": 0,
    "result_correct": False,

    # Player results per customer, used by the ending overlay
    "order_results": {
        "warthog": None,
        "slug":    None,
        "octopus": None,
        "karel":   None,
    },

    # Flashing halo
    "active_flash": None,
    "flash_timer": 0,
    "flash_visible": False,

    # Select halo (acknowledges a click)
    "showing_select": False,
    "select_object": None,
    "select_timer": 0,

    # "west" = Jelly facing tables (default), "east" = Jelly facing bar
    "jelly_facing": "west",

    # Cloche arc animation (table1)
    "cloche_animating": False,
    "cloche_t": 0.0,
    "cloche_start_x": 0,
    "cloche_start_y": 0,

    # Cloche arc animation (table2)
    "cloche2_animating": False,
    "cloche2_t": 0.0,
    "cloche2_start_x": 0,
    "cloche2_start_y": 0,

    "cloche1_placed": False,

    # Waypoint: Jelly walks to the waypoint first, then the final target
    "waypoint_x": None,
    "waypoint_y": None,
    "waypoint_direction": None,
    "final_target_x": None,
    "final_target_y": None,
    "final_direction": None,

    "showing_round_overlay": True,
    "round_overlay_timer": 0,

    # Float image currently visible (so it can be hidden when switching)
    "current_float_shown": None,

    "game_over": False,

    # "splash" -> "instructions" -> "game"
    "phase": "splash",
    "splash_timer": 0,
}


# ---------------------------------------------------------------------------
# FLASHING & SELECT HALO HELPER FUNCTIONS
# ---------------------------------------------------------------------------

# Hides all halos, then sets which object ("table1", "table2", "bar" or None) flashes next
def set_active_flash(canvas, flash_imgs, select_imgs, new_target):
    for key in flash_imgs:
        canvas.set_hidden(flash_imgs[key], True)
    for key in select_imgs:
        canvas.set_hidden(select_imgs[key], True)

    state["active_flash"] = new_target
    state["flash_timer"] = 0
    state["flash_visible"] = False
    state["showing_select"] = False
    state["select_object"] = None
    state["select_timer"] = 0

# Hides the flash halo and briefly shows the select (acknowledgement) halo
def trigger_select_halo(canvas, flash_imgs, select_imgs, obj_name):
    canvas.set_hidden(flash_imgs[obj_name], True)
    state["active_flash"] = None
    state["flash_visible"] = False

    canvas.set_hidden(select_imgs[obj_name], False)
    state["showing_select"] = True
    state["select_object"] = obj_name
    state["select_timer"] = 0


# Called every frame to handle flashing and select-halo timing
def update_flash(canvas, flash_imgs, select_imgs):
    if state["showing_select"]:
        state["select_timer"] += 1
        if state["select_timer"] >= SELECT_HALO_FRAMES:
            obj = state["select_object"]
            canvas.set_hidden(select_imgs[obj], True)
            state["showing_select"] = False
            state["select_object"] = None
        return

    if state["active_flash"] is None:
        return

    state["flash_timer"] += 1
    if state["flash_timer"] >= FLASH_TOGGLE_FRAMES:
        state["flash_timer"] = 0
        state["flash_visible"] = not state["flash_visible"]
        obj = state["active_flash"]
        canvas.set_hidden(flash_imgs[obj], not state["flash_visible"])


# ---------------------------------------------------------------------------
# JELLY SPRITE HELPER FUNCTIONS
# ---------------------------------------------------------------------------

# Shows the correct Jelly sprite for the direction of travel
def set_jelly_direction(canvas, player, player_east, direction):
    if direction == state["jelly_facing"]:
        return
    state["jelly_facing"] = direction
    if direction == "east":
        canvas.set_hidden(player, True)
        canvas.set_hidden(player_east, False)
    else:
        canvas.set_hidden(player_east, True)
        canvas.set_hidden(player, False)


# ---------------------------------------------------------------------------
# CLOCHE ARC ANIMATION (TABLE1)
# ---------------------------------------------------------------------------

# Animates the cloche in an arc as Jelly puts it on table1
def update_cloche(canvas, cloche):
    if not state["cloche_animating"]:
        return

    state["cloche_t"] += 0.05
    t  = state["cloche_t"]
    sx = state["cloche_start_x"]
    sy = state["cloche_start_y"]
    ex = CLOCHE_LAND_X
    ey = CLOCHE_LAND_Y

    # Control point: midway in x, 40 pixels above the higher endpoint (makes the arc high)
    cx = (sx + ex) / 2
    cy = min(sy, ey) - 40

    # Quadratic Bézier curve
    x = (1 - t)**2 * sx  +  2 * (1 - t) * t * cx  +  t**2 * ex
    y = (1 - t)**2 * sy  +  2 * (1 - t) * t * cy  +  t**2 * ey

    canvas.moveto(cloche, x, y)

    if state["cloche_t"] >= 1.0:
        state["cloche_animating"] = False
        canvas.moveto(cloche, ex, ey)


# ---------------------------------------------------------------------------
# CLOCHE ARC ANIMATION (TABLE2) — same as above but for cloche2
# ---------------------------------------------------------------------------

def update_cloche2(canvas, cloche2):
    if not state["cloche2_animating"]:
        return

    state["cloche2_t"] += 0.05

    t  = state["cloche2_t"]
    sx = state["cloche2_start_x"]
    sy = state["cloche2_start_y"]
    ex = CLOCHE2_LAND_X
    ey = CLOCHE2_LAND_Y

    cx = (sx + ex) / 2
    cy = min(sy, ey) - 40

    x = (1 - t)**2 * sx  +  2 * (1 - t) * t * cx  +  t**2 * ex
    y = (1 - t)**2 * sy  +  2 * (1 - t) * t * cy  +  t**2 * ey

    canvas.moveto(cloche2, x, y)

    if state["cloche2_t"] >= 1.0:
        state["cloche2_animating"] = False
        canvas.moveto(cloche2, ex, ey)


# ---------------------------------------------------------------------------
# ROUND OVERLAY
# ---------------------------------------------------------------------------

# Shows the round overlay, then sets up the round when it finishes
def update_round_overlay(canvas, round1_overlay, round2_overlay,
                         flash_imgs, select_imgs,
                         player, player_east,
                         warthog, octopus, slug, karel,
                         cloche, cloche2):
    if not state["showing_round_overlay"]:
        return

    state["round_overlay_timer"] += 1

    if state["round_overlay_timer"] >= ROUND_OVERLAY_FRAMES:
        state["showing_round_overlay"] = False
        state["round_overlay_timer"] = 0

        if state["round"] == 1:
            canvas.set_hidden(round1_overlay, True)
            set_active_flash(canvas, flash_imgs, select_imgs, "table1")

        else:
            canvas.set_hidden(round2_overlay, True)

            # Swap table1 customer: warthog -> octopus
            canvas.set_hidden(warthog[0], True)
            canvas.set_hidden(warthog[1], True)
            canvas.set_hidden(octopus[0], False)
            canvas.set_hidden(octopus[1], True)

            # Swap table2 customer: slug -> Karel
            canvas.set_hidden(slug[0], True)
            canvas.set_hidden(slug[1], True)
            canvas.set_hidden(karel, False)

            # Move Jelly back to the starting position
            dx = JELLY_START_X - state["x"]
            dy = JELLY_START_Y - state["y"]
            canvas.move(player, dx, dy)
            canvas.move(player_east, dx, dy)

            # Force the west-facing sprite to show (jelly_facing is set to "east" so the swap isn't skipped)
            state["jelly_facing"] = "east"
            set_jelly_direction(canvas, player, player_east, "west")
            state["x"] = JELLY_START_X
            state["y"] = JELLY_START_Y

            # Reset round state
            state["current_customer"] = 1
            state["order_complete"] = False
            state["order_prepared"] = False
            state["current_order"] = []
            state["player_selection"] = set()
            state["cloche1_placed"] = False

            state["waypoint_x"] = None
            state["waypoint_y"] = None
            state["waypoint_direction"] = None
            state["final_target_x"] = None
            state["final_target_y"] = None
            state["final_direction"] = None

            # Hide both cloches and return them to Jelly's head
            canvas.set_hidden(cloche, True)
            canvas.set_hidden(cloche2, True)
            canvas.moveto(cloche,  JELLY_START_X + 28, JELLY_START_Y - 25)
            canvas.moveto(cloche2, JELLY_START_X + 28, JELLY_START_Y - 25)

            set_active_flash(canvas, flash_imgs, select_imgs, "table1")


# ---------------------------------------------------------------------------
# SPLASH SCREEN & INSTRUCTIONS HANDLING
# ---------------------------------------------------------------------------

# Returns True while still in the pre-game screens so the main loop can skip game-logic updates
def update_splash(canvas, splash_img, instructions_img,
                  start_btn_normal, start_btn_selected):
    phase = state["phase"]

    if phase == "splash":
        state["splash_timer"] += 1
        if state["splash_timer"] >= SPLASH_FRAMES:
            canvas.set_hidden(splash_img, True)
            canvas.set_hidden(instructions_img, False)
            canvas.set_hidden(start_btn_normal, False)
            state["phase"] = "instructions"

        return True

    if phase == "instructions":
        return True

    return False


# Called when the player clicks the start button on the instructions overlay
def handle_start_button(canvas, instructions_img,
                        start_btn_normal, start_btn_selected,
                        round1_overlay):
    # Show the selected button briefly before hiding the instructions
    canvas.set_hidden(start_btn_normal, True)
    canvas.set_hidden(start_btn_selected, False)
    sleep(1)

    canvas.set_hidden(start_btn_selected, True)
    canvas.set_hidden(instructions_img, True)
    canvas.set_hidden(round1_overlay, False)

    state["phase"] = "game"


# ---------------------------------------------------------------------------
# CLICK HANDLING
# ---------------------------------------------------------------------------

# Decides what happens when the player clicks, depending on the game phase and state
def handle_click(canvas, x, y,
                 flash_imgs, select_imgs, menu_ui, cloche, cloche2, slug,
                 splash_img, instructions_img,
                 start_btn_normal, start_btn_selected,
                 round1_overlay):

    # Pre-game screens
    if state["phase"] == "splash":
        return
    if state["phase"] == "instructions":
        if 523 <= x <= 523 + 130 and 364 <= y <= 364 + 50:   # start button hit area
            handle_start_button(canvas, instructions_img,
                                start_btn_normal, start_btn_selected,
                                round1_overlay)
        return

    # Game phase: ignore clicks while a round overlay is showing or the game is over
    if state["showing_round_overlay"] or state["game_over"]:
        return

    if state["menu_open"]:
        handle_menu_click(canvas, x, y, flash_imgs, select_imgs, menu_ui, cloche, cloche2)
        return

    # Ignore clicks while the tick/cross is showing
    if state["showing_result"]:
        return

    t1_ox, t1_oy, t1_w, t1_h, t1_tx, t1_ty = objects["table1"]
    t2_ox, t2_oy, t2_w, t2_h, t2_tx, t2_ty = objects["table2"]
    bar_ox, bar_oy, bar_w, bar_h, bar_tx, bar_ty = objects["bar"]

    # TABLE 1 click (customer 1 flow)
    if state["current_customer"] == 1:
        # Table1 must be flashing (take order) or the order must be prepared (deliver it)
        if state["active_flash"] == "table1" or (state["order_prepared"] and not state["showing_select"]):
            if t1_ox <= x <= t1_ox + t1_w and t1_oy <= y <= t1_oy + t1_h:
                if state["active_flash"] == "table1" and not state["ordering"]:
                    trigger_select_halo(canvas, flash_imgs, select_imgs, "table1")
                    if state["order_prepared"]:
                        # Deliver the cloche
                        state["target_x"] = TABLE1_DELIVERY_X
                        state["target_y"] = TABLE1_DELIVERY_Y
                    else:
                        # Take the customer's order
                        state["target_x"] = t1_tx
                        state["target_y"] = t1_ty
                    state["moving"] = True
                    state["selected"] = "table1"
                return

    # TABLE 2 click (customer 2 flow)
    if state["current_customer"] == 2:
        if state["active_flash"] == "table2" or (state["order_prepared"] and not state["showing_select"]):
            if t2_ox <= x <= t2_ox + t2_w and t2_oy <= y <= t2_oy + t2_h:
                if state["active_flash"] == "table2" and not state["ordering"]:
                    trigger_select_halo(canvas, flash_imgs, select_imgs, "table2")
                    if state["order_prepared"]:
                        # Deliver the cloche
                        state["target_x"] = TABLE2_DELIVERY_X
                        state["target_y"] = TABLE2_DELIVERY_Y
                    else:
                        if state["round"] == 2:
                            # Karel: walk east to the waypoint first, then west to the table
                            state["target_x"] = KAREL_WAYPOINT_X
                            state["target_y"] = KAREL_WAYPOINT_Y
                            state["waypoint_x"] = KAREL_WAYPOINT_X
                            state["waypoint_y"] = KAREL_WAYPOINT_Y
                            state["waypoint_direction"] = "east"
                            state["final_target_x"] = KAREL_ORDER_X
                            state["final_target_y"] = KAREL_ORDER_Y
                            state["final_direction"] = "west"
                        else:
                            state["target_x"] = TABLE2_ORDER_X
                            state["target_y"] = TABLE2_ORDER_Y
                            state["waypoint_x"] = None
                    state["moving"] = True
                    state["selected"] = "table2"
                return

    # BAR click: the bar counter, bar background and chef are all clickable
    bar_bg_x1, bar_bg_y1, bar_bg_x2, bar_bg_y2 = 458, 0, CANVAS_WIDTH, CANVAS_HEIGHT
    chef_x1, chef_y1, chef_x2, chef_y2 = 500, 115, 650, 300

    clicked_bar_area = (
        (bar_ox <= x <= bar_ox + bar_w and bar_oy <= y <= bar_oy + bar_h) or
        (bar_bg_x1 <= x <= bar_bg_x2 and bar_bg_y1 <= y <= bar_bg_y2) or
        (chef_x1 <= x <= chef_x2 and chef_y1 <= y <= chef_y2)
    )

    if clicked_bar_area:
        if state["active_flash"] == "bar" and state["order_complete"] and not state["menu_open"]:
            trigger_select_halo(canvas, flash_imgs, select_imgs, "bar")
            state["target_x"] = bar_tx
            state["target_y"] = bar_ty
            state["moving"] = True
            state["selected"] = "bar"
        return

# Only runs while the menu overlay is open
def handle_menu_click(canvas, x, y, flash_imgs, select_imgs, menu_ui, cloche, cloche2):
    overlay, buttons, submit_imgs = menu_ui

    if 263 <= x <= 437 and 369 <= y <= 405:               # submit button hit area
        canvas.set_hidden(submit_imgs["normal"], True)
        canvas.set_hidden(submit_imgs["selected"], False)
        sleep(1)                                          # lets the selected button be seen before the menu closes
        close_menu(canvas, flash_imgs, select_imgs, menu_ui, cloche, cloche2)
        return

    for name, nx, ny, sx, sy in MENU_BUTTONS:
        if nx <= x <= nx + 80 and ny <= y <= ny + 80:     # every button is 80x80
            toggle_button(canvas, name, buttons)
            return

# Toggles a menu button between selected and unselected
def toggle_button(canvas, name, buttons):
    if name in state["player_selection"]:
        state["player_selection"].discard(name)
        canvas.set_hidden(buttons[name]["selected"], True)
        canvas.set_hidden(buttons[name]["normal"], False)
    else:
        state["player_selection"].add(name)
        canvas.set_hidden(buttons[name]["normal"], True)
        canvas.set_hidden(buttons[name]["selected"], False)


# ---------------------------------------------------------------------------
# PLAYER MOVEMENT
# ---------------------------------------------------------------------------

def update_player(canvas, player, player_east, flash_imgs, select_imgs, menu_ui,
                  warthog, octopus, cloche, cloche2, slug, karel):
    if not state["moving"]:
        return

    if state["showing_select"]:
        return

    # Direction: a waypoint direction takes priority while walking to the waypoint,
    # otherwise use the standard rules for each destination
    if state["waypoint_direction"] is not None:
        set_jelly_direction(canvas, player, player_east, state["waypoint_direction"])
    elif state["selected"] == "bar":
        set_jelly_direction(canvas, player, player_east, "east")
    elif state["selected"] == "table2" and not state["order_prepared"] and state["round"] == 1:
        set_jelly_direction(canvas, player, player_east, "east")
    else:
        set_jelly_direction(canvas, player, player_east, "west")

    dx = state["target_x"] - state["x"]
    dy = state["target_y"] - state["y"]
    speed = state["speed"]

    # Move by `speed` toward the target or by the remaining distance if closer than that
    move_x = speed if dx > speed else (-speed if dx < -speed else dx)
    move_y = speed if dy > speed else (-speed if dy < -speed else dy)

    state["x"] += move_x
    state["y"] += move_y
    canvas.move(player, move_x, move_y)
    canvas.move(player_east, move_x, move_y)

    # Move whichever cloche Jelly is currently carrying
    if state["current_customer"] == 1 and not state["cloche1_placed"]:
        canvas.move(cloche, move_x, move_y)
    elif state["current_customer"] == 2 and state["order_prepared"]:
        canvas.move(cloche2, move_x, move_y)

    # Jelly has reached her target
    if state["x"] == state["target_x"] and state["y"] == state["target_y"]:

        # Waypoint reached: switch direction and continue to the final target
        if (state["waypoint_x"] is not None and
                state["x"] == state["waypoint_x"] and
                state["y"] == state["waypoint_y"] and
                state["final_target_x"] is not None):
            set_jelly_direction(canvas, player, player_east, state["final_direction"])
            state["waypoint_direction"] = None
            state["waypoint_x"] = None
            state["waypoint_y"] = None
            state["target_x"] = state["final_target_x"]
            state["target_y"] = state["final_target_y"]
            state["final_target_x"] = None
            state["final_target_y"] = None
            state["final_direction"] = None

            return   # return before "moving" is set to False so Jelly doesn't stop at the waypoint

        state["moving"] = False

        # Customer 1 (table1) arrivals
        if state["selected"] == "table1" and not state["order_complete"] and state["current_customer"] == 1:
            if state["round"] == 1:
                start_ordering(canvas, warthog)
            else:
                start_ordering_octopus(canvas, octopus)

        elif state["selected"] == "bar" and state["order_complete"] and not state["menu_open"]:
            open_menu(canvas, menu_ui)

        elif state["selected"] == "table1" and state["order_prepared"] and state["current_customer"] == 1:
            # Cloche starts its arc from just above Jelly's head
            state["cloche_start_x"] = state["x"] + 28
            state["cloche_start_y"] = state["y"] - 25
            state["cloche_t"] = 0.0
            state["cloche_animating"] = True
            evaluate_order(canvas, flash_imgs, select_imgs, menu_ui)

        # Customer 2 (table2) arrivals
        elif state["selected"] == "table2" and not state["order_complete"] and state["current_customer"] == 2:
            if state["round"] == 1:
                start_ordering_slug(canvas, slug)
            else:
                start_ordering_karel(canvas, karel)

        elif state["selected"] == "table2" and state["order_prepared"] and state["current_customer"] == 2:
            state["cloche2_start_x"] = state["x"] + 28
            state["cloche2_start_y"] = state["y"] - 25
            state["cloche2_t"] = 0.0
            state["cloche2_animating"] = True
            evaluate_order(canvas, flash_imgs, select_imgs, menu_ui)

        state["selected"] = None


# ---------------------------------------------------------------------------
# ORDERING SEQUENCES
# ---------------------------------------------------------------------------
# Each customer picks random items (random.sample so there are no repeats)
# and starts floating them above their head one at a time.

# Customer 1, round 1: warthog at table1 (3 items)
def start_ordering(canvas, warthog):
    num_items = random.randint(3, 3)    # fixed for now, but kept as randint in case it varies later
    state["order_items"] = random.sample(MENU_ITEMS, num_items)
    state["order_index"] = 0
    state["order_timer"] = 0
    state["ordering"] = True
    state["current_order"] = list(state["order_items"])   # copy, so the order survives after order_items is used up
    canvas.set_hidden(warthog[0], True)     # swap waiting pose for ordering pose
    canvas.set_hidden(warthog[1], False)


# Customer 1, round 2: octopus at table1 (5 items)
def start_ordering_octopus(canvas, octopus):
    num_items = random.randint(5, 5)
    state["order_items"] = random.sample(MENU_ITEMS, num_items)
    state["order_index"] = 0
    state["order_timer"] = 0
    state["ordering"] = True
    state["current_order"] = list(state["order_items"])
    canvas.set_hidden(octopus[0], True)
    canvas.set_hidden(octopus[1], False)


# Customer 2, round 1: slug at table2 (4 items)
def start_ordering_slug(canvas, slug):
    num_items = random.randint(4, 4)
    state["order_items"] = random.sample(MENU_ITEMS, num_items)
    state["order_index"] = 0
    state["order_timer"] = 0
    state["ordering"] = True
    state["current_order"] = list(state["order_items"])
    canvas.set_hidden(slug[0], True)    # slug_waiting
    canvas.set_hidden(slug[1], False)   # slug_facing_jelly


# Customer 2, round 2: Karel at table2 (6 items)
def start_ordering_karel(canvas, karel):
    num_items = random.randint(6, 6)
    state["order_items"] = random.sample(MENU_ITEMS, num_items)
    state["order_index"] = 0
    state["order_timer"] = 0
    state["ordering"] = True
    state["current_order"] = list(state["order_items"])
    # Karel only has one sprite (already facing Jelly), so nothing to swap


# ---------------------------------------------------------------------------
# ORDERING UPDATE
# ---------------------------------------------------------------------------

# Called every frame during ordering. Float images are pre-loaded at startup,
# so this only moves, shows and hides them rather than creating/deleting images.
def update_ordering(canvas, float_images, flash_imgs, select_imgs,
                    warthog, octopus, slug, karel):
    if not state["ordering"]:
        return

    state["order_timer"] += 1

    # First frame of a new item: show it above the correct table
    if state["order_timer"] == 1:
        if state["current_float_shown"] is not None:
            canvas.set_hidden(float_images[state["current_float_shown"]], True)

        if state["current_customer"] == 1:
            fx, fy = FLOAT_X_TABLE1, FLOAT_Y_TABLE1
        else:
            fx, fy = FLOAT_X_TABLE2, FLOAT_Y_TABLE2

        new_image = state["order_items"][state["order_index"]]

        canvas.moveto(float_images[new_image], fx, fy)
        canvas.set_hidden(float_images[new_image], False)
        state["current_float_shown"] = new_image

    # Item has been shown long enough: hide it and move to the next one
    if state["order_timer"] >= FRAMES_PER_ITEM:
        if state["current_float_shown"] is not None:
            canvas.set_hidden(float_images[state["current_float_shown"]], True)
            state["current_float_shown"] = None

        state["order_timer"] = 0
        state["order_index"] += 1

        # Whole order shown
        if state["order_index"] >= len(state["order_items"]):
            state["ordering"] = False
            state["order_complete"] = True

            # Customer returns to their waiting pose
            if state["current_customer"] == 1:
                if state["round"] == 1:
                    canvas.set_hidden(warthog[1], True)
                    canvas.set_hidden(warthog[0], False)
                else:
                    canvas.set_hidden(octopus[1], True)
                    canvas.set_hidden(octopus[0], False)
            else:
                if state["round"] == 1:
                    canvas.set_hidden(slug[1], True)
                    canvas.set_hidden(slug[0], False)
                # Karel has no alternate pose to revert to

            # Order done, so flash the bar
            set_active_flash(canvas, flash_imgs, select_imgs, "bar")


# ---------------------------------------------------------------------------
# MENU OVERLAY (open_menu, update_menu, close_menu)
# ---------------------------------------------------------------------------

# Called when Jelly reaches the chef after taking an order
def open_menu(canvas, menu_ui):
    overlay, buttons, submit_imgs = menu_ui
    state["menu_open"] = True               # clicks now go to the menu instead of moving Jelly
    state["menu_timer"] = 0
    state["player_selection"] = set()

    canvas.set_hidden(overlay, False)

    for name, nx, ny, sx, sy in MENU_BUTTONS:
        canvas.set_hidden(buttons[name]["normal"], False)
        canvas.set_hidden(buttons[name]["selected"], True)

    canvas.set_hidden(submit_imgs["normal"], False)
    canvas.set_hidden(submit_imgs["selected"], True)

# Closes the menu automatically if it's been open too long
def update_menu(canvas, flash_imgs, select_imgs, menu_ui, cloche, cloche2):
    if not state["menu_open"]:
        return

    state["menu_timer"] += 1

    if state["menu_timer"] >= MENU_OVERLAY_FRAMES:
        close_menu(canvas, flash_imgs, select_imgs, menu_ui, cloche, cloche2)


def close_menu(canvas, flash_imgs, select_imgs, menu_ui, cloche, cloche2):
    overlay, buttons, submit_imgs = menu_ui
    state["menu_open"] = False

    canvas.set_hidden(overlay, True)

    for name, nx, ny, sx, sy in MENU_BUTTONS:
        canvas.set_hidden(buttons[name]["normal"], True)
        canvas.set_hidden(buttons[name]["selected"], True)

    canvas.set_hidden(submit_imgs["normal"], True)
    canvas.set_hidden(submit_imgs["selected"], True)

    state["order_prepared"] = True

    # Show the cloche on Jelly's head and flash the table to deliver to
    if state["current_customer"] == 1:
        canvas.set_hidden(cloche, False)
        set_active_flash(canvas, flash_imgs, select_imgs, "table1")
    else:
        canvas.set_hidden(cloche2, False)
        set_active_flash(canvas, flash_imgs, select_imgs, "table2")


# ---------------------------------------------------------------------------
# ORDER EVALUATION
# ---------------------------------------------------------------------------

# Compares what the player selected to what the customer ordered
def evaluate_order(canvas, flash_imgs, select_imgs, menu_ui):
    # The customer orders in float files but the player selects buttons, so convert to compare
    correct_buttons = set()
    for float_file in state["current_order"]:
        btn = FLOAT_TO_BUTTON.get(float_file)
        if btn:
            correct_buttons.add(btn)

    player_set = state["player_selection"]
    # Symmetric difference = items in one set but not the other (missed items + extra items)
    wrong_count = len(player_set.symmetric_difference(correct_buttons))
    state["score"] -= wrong_count

    is_correct = (wrong_count == 0)
    state["result_correct"] = is_correct

    # Record the per-customer result for the ending summary
    if state["round"] == 1:
        customer_key = "warthog" if state["current_customer"] == 1 else "slug"
    else:
        customer_key = "octopus" if state["current_customer"] == 1 else "karel"
    state["order_results"][customer_key] = is_correct

    state["showing_result"] = True
    state["result_timer"] = 0

    set_active_flash(canvas, flash_imgs, select_imgs, None)

# Shows the tick or cross above the table, then advances to the next customer/round
def update_result(canvas, result_imgs_t1, result_imgs_t2, flash_imgs, select_imgs,
                  cloche, cloche2, round1_overlay, round2_overlay,
                  player, player_east, warthog, octopus, slug, karel,
                  ending_ui):
    if not state["showing_result"]:
        return

    if state["current_customer"] == 1:
        correct_img, wrong_img = result_imgs_t1
    else:
        correct_img, wrong_img = result_imgs_t2

    if state["result_timer"] == 0:
        if state["result_correct"]:
            canvas.set_hidden(correct_img, False)
            canvas.set_hidden(wrong_img, True)
        else:
            canvas.set_hidden(wrong_img, False)
            canvas.set_hidden(correct_img, True)

    state["result_timer"] += 1

    if state["result_timer"] >= RESULT_DISPLAY_FRAMES:
        canvas.set_hidden(correct_img, True)
        canvas.set_hidden(wrong_img, True)
        state["showing_result"] = False

        if state["current_customer"] == 1:
            # Move on to the table2 customer (cloche1 stays on table1)
            state["cloche1_placed"] = True
            state["current_customer"] = 2
            state["order_complete"] = False
            state["order_prepared"] = False
            state["current_order"] = []
            state["player_selection"] = set()
            state["cloche_animating"] = False

            set_active_flash(canvas, flash_imgs, select_imgs, "table2")

        else:
            state["cloche2_animating"] = False
            canvas.set_hidden(cloche2, True)
            state["order_complete"] = False
            state["order_prepared"] = False
            state["current_order"] = []
            state["player_selection"] = set()

            if state["round"] == 1:
                state["round"] = 2
                state["showing_round_overlay"] = True
                state["round_overlay_timer"] = 0
                canvas.set_hidden(round2_overlay, False)
                set_active_flash(canvas, flash_imgs, select_imgs, None)

            else:
                show_ending(canvas, ending_ui,
                            flash_imgs, select_imgs,
                            cloche, cloche2,
                            warthog, octopus, slug, karel,
                            player, player_east)


# ---------------------------------------------------------------------------
# ENDING OVERLAY
# ---------------------------------------------------------------------------

# Tallies results, shows the hired/fired overlay and places each customer's summary icon
def show_ending(canvas, ending_ui,
                flash_imgs, select_imgs,
                cloche, cloche2,
                warthog, octopus, slug, karel,
                player, player_east):
    hired_overlay, fired_overlay, summary_icons = ending_ui

    results = state["order_results"]
    correct_count = sum(1 for v in results.values() if v is True)
    player_wins = correct_count >= 3    # need at least 3 of 4 orders correct

    canvas.set_hidden(hired_overlay, not player_wins)
    canvas.set_hidden(fired_overlay, player_wins)

    for customer_key, (ix, iy) in SUMMARY_ICON_POSITIONS.items():
        correct_icon, wrong_icon = summary_icons[customer_key]
        was_correct = results.get(customer_key)
        canvas.moveto(correct_icon, ix, iy)
        canvas.moveto(wrong_icon,   ix, iy)
        if was_correct:
            canvas.set_hidden(correct_icon, False)
            canvas.set_hidden(wrong_icon,   True)
        else:
            canvas.set_hidden(wrong_icon,   False)
            canvas.set_hidden(correct_icon, True)

    state["game_over"] = True
    set_active_flash(canvas, flash_imgs, select_imgs, None)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

# Images are layered in creation order i.e. later images appear on top of earlier ones.
def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    #### BACKGROUND IMAGE ####
    canvas.create_image(0, 0, "images/CosmicCafeFinalBG.png")

    #### LIFT DOORS ####
    left_door  = canvas.create_image(LIFT_LEFT_DOOR_X,  LIFT_LEFT_DOOR_Y,  "images/left_lift_door.png")
    right_door = canvas.create_image(LIFT_RIGHT_DOOR_X, LIFT_RIGHT_DOOR_Y, "images/right_lift_door.png")

    #### CHEF ####
    canvas.create_image(550, 115, "images/Chef_shrunk.png")

    #### BAR BACKGROUND (clickable) ####
    canvas.create_image(458, 0, "images/bar_bg.png")

    #### BAR & FLASH HALOS ####
    flash_bar = canvas.create_image(417, 0, "images/bar_flash.png")
    canvas.set_hidden(flash_bar, True)

    select_bar = canvas.create_image(417, 0, "images/bar_flash_select.png")
    canvas.set_hidden(select_bar, True)

    canvas.create_image(455, 206, "images/bar_shrunk.png")

    #### BAR STOOLS ####
    canvas.create_image(105, 295, "images/BarStool1.png")
    canvas.create_image(375, 296, "images/BarStool2.png")

    #### WARTHOG (round 1, table1) ####
    warthog_waiting  = canvas.create_image(64, 189, "images/Warthog_waiting.png")
    warthog_ordering = canvas.create_image(64, 189, "images/warthog_facing_jelly.png")
    canvas.set_hidden(warthog_ordering, True)
    warthog = [warthog_waiting, warthog_ordering]   # [waiting, ordering]

    #### OCTOPUS (round 2, table1) — hidden until round 2 ####
    octopus_waiting  = canvas.create_image(34, 176, "images/octopus_waiting.png")
    octopus_ordering = canvas.create_image(34, 176, "images/octopus_facing_east.png")
    canvas.set_hidden(octopus_waiting,  True)
    canvas.set_hidden(octopus_ordering, True)
    octopus = [octopus_waiting, octopus_ordering]   # [waiting, ordering]

    #### JELLY ####
    player      = canvas.create_image(state["x"], state["y"], "images/Jelly_shrunk.png")       # faces west
    player_east = canvas.create_image(state["x"], state["y"], "images/Jelly_shrunk_East.png")  # faces east
    canvas.set_hidden(player_east, True)

    #### TABLE 1 & HALOS ####
    select_table1 = canvas.create_image(38,  262, "images/table1_flash_select.png")
    canvas.set_hidden(select_table1, True)

    flash_table1  = canvas.create_image(48,  263, "images/table1_flash.png")
    canvas.set_hidden(flash_table1, True)

    canvas.create_image(35,  277, "images/Table1shrunk.png")

    #### CLOCHE 1 (table1 delivery) — starts hidden on Jelly's head ####
    cloche = canvas.create_image(state["x"] + 28, state["y"] - 25, "images/cloche.png")
    canvas.set_hidden(cloche, True)

    #### SLUG (round 1, table2) ####
    slug_waiting      = canvas.create_image(355, 185, "images/slug_waiting.png")
    slug_facing_jelly = canvas.create_image(355, 185, "images/slug_facing_jelly.png")
    canvas.set_hidden(slug_facing_jelly, True)
    slug = [slug_waiting, slug_facing_jelly]        # [waiting, ordering]

    #### TABLE 2 & HALOS ####
    select_table2 = canvas.create_image(309, 262, "images/table2_flash_select.png")
    canvas.set_hidden(select_table2, True)

    flash_table2  = canvas.create_image(318, 264, "images/table2_flash.png")
    canvas.set_hidden(flash_table2, True)

    canvas.create_image(301, 284, "images/Table2shrunk.png")

    #### CLOCHE 2 (table2 delivery) — starts hidden on Jelly's head ####
    cloche2 = canvas.create_image(state["x"] + 28, state["y"] - 25, "images/cloche.png")
    canvas.set_hidden(cloche2, True)

    #### KAREL (round 2, table2) — hidden until round 2, only has one sprite ####
    karel = canvas.create_image(281, 224, "images/Karel_facing_east.png")
    canvas.set_hidden(karel, True)

    #### FLASH / SELECT HALO DICTIONARIES ####
    flash_imgs  = {"table1": flash_table1,  "table2": flash_table2,  "bar": flash_bar}
    select_imgs = {"table1": select_table1, "table2": select_table2, "bar": select_bar}

    #### SPLASH SCREEN ####
    # Visible immediately; update_splash hides it after SPLASH_FRAMES
    splash_img = canvas.create_image(0, 0, "images/splash_screen.png")

    #### PRE-LOAD ALL FLOAT IMAGES ####
    # Created once at startup and hidden until needed
    float_images = {}
    for item in MENU_ITEMS:
        img = canvas.create_image(FLOAT_X_TABLE1, FLOAT_Y_TABLE1, f"images/{item}")
        canvas.set_hidden(img, True)
        float_images[item] = img

    #### MENU OVERLAY ####
    overlay = canvas.create_image(0, 0, "images/cosmic_cafe_menu_overlay.png")
    canvas.set_hidden(overlay, True)

    # Image filenames are built from the button name: "<name>.png" and "<name>_selected.png"
    buttons = {}
    for name, nx, ny, sx, sy in MENU_BUTTONS:
        normal_img   = canvas.create_image(nx, ny, f"images/{name}.png")
        selected_img = canvas.create_image(sx, sy, f"images/{name}_selected.png")
        canvas.set_hidden(normal_img, True)
        canvas.set_hidden(selected_img, True)
        buttons[name] = {"normal": normal_img, "selected": selected_img}

    #### SUBMIT BUTTON ####
    submit_selected = canvas.create_image(SUBMIT_BUTTON_X, SUBMIT_BUTTON_Y, "images/submit_button_selected.png")
    submit_normal   = canvas.create_image(SUBMIT_BUTTON_X, SUBMIT_BUTTON_Y, "images/submit_button.png")
    canvas.set_hidden(submit_normal, True)
    canvas.set_hidden(submit_selected, True)
    submit_imgs = {"normal": submit_normal, "selected": submit_selected}

    menu_ui = (overlay, buttons, submit_imgs)

    #### ROUND OVERLAYS — hidden until needed ####
    round1_overlay = canvas.create_image(0, 0, "images/Round1_overlay.png")
    canvas.set_hidden(round1_overlay, True)
    round2_overlay = canvas.create_image(0, 0, "images/Round2_overlay.png")
    canvas.set_hidden(round2_overlay, True)

    #### ENDING OVERLAYS ####
    hired_overlay = canvas.create_image(0, 0, "images/hired_overlay.png")
    canvas.set_hidden(hired_overlay, True)

    fired_overlay = canvas.create_image(0, 0, "images/fired_overlay.png")
    canvas.set_hidden(fired_overlay, True)

    summary_icons = {}
    for customer_key, (ix, iy) in SUMMARY_ICON_POSITIONS.items():
        c_icon = canvas.create_image(ix, iy, "images/correct_order_icon.png")
        w_icon = canvas.create_image(ix, iy, "images/wrong_order_icon.png")
        canvas.set_hidden(c_icon, True)
        canvas.set_hidden(w_icon, True)
        summary_icons[customer_key] = (c_icon, w_icon)

    ending_ui = (hired_overlay, fired_overlay, summary_icons)

    #### RESULT ICONS (tick/cross above each table) ####
    correct_img_t1 = canvas.create_image(FLOAT_X_TABLE1, FLOAT_Y_TABLE1, "images/correct_order_icon.png")
    wrong_img_t1   = canvas.create_image(FLOAT_X_TABLE1, FLOAT_Y_TABLE1, "images/wrong_order_icon.png")
    canvas.set_hidden(correct_img_t1, True)
    canvas.set_hidden(wrong_img_t1,   True)
    result_imgs_t1 = (correct_img_t1, wrong_img_t1)

    correct_img_t2 = canvas.create_image(FLOAT_X_TABLE2, FLOAT_Y_TABLE2, "images/correct_order_icon.png")
    wrong_img_t2   = canvas.create_image(FLOAT_X_TABLE2, FLOAT_Y_TABLE2, "images/wrong_order_icon.png")
    canvas.set_hidden(correct_img_t2, True)
    canvas.set_hidden(wrong_img_t2,   True)
    result_imgs_t2 = (correct_img_t2, wrong_img_t2)

    #### INSTRUCTIONS OVERLAY — on top of everything ####
    start_btn_normal    = canvas.create_image(523, 364, "images/start_button.png")
    instructions_img    = canvas.create_image(0, 0, "images/instructions.png")
    start_btn_selected  = canvas.create_image(523, 364, "images/start_button_select.png")

    # Hidden until the splash screen finishes
    canvas.set_hidden(instructions_img,   True)
    canvas.set_hidden(start_btn_normal,   True)
    canvas.set_hidden(start_btn_selected, True)


    # -------------------------------------------------------------------------
    # MAIN LOOP
    # -------------------------------------------------------------------------
    while True:
        click = canvas.get_last_click()     # None if no click, otherwise (x, y)

        # True while on the splash/instructions screens
        pre_game = update_splash(canvas, splash_img, instructions_img,
                                 start_btn_normal, start_btn_selected)

        if click is not None:
            handle_click(canvas, click[0], click[1],
                         flash_imgs, select_imgs, menu_ui, cloche, cloche2, slug,
                         splash_img, instructions_img,
                         start_btn_normal, start_btn_selected,
                         round1_overlay)

        # Game-logic updates only run during the game phase.
        # Each update function returns immediately unless its feature is active.
        if not pre_game:
            update_player(canvas, player, player_east,
                          flash_imgs, select_imgs, menu_ui,
                          warthog, octopus, cloche, cloche2, slug, karel)
            update_ordering(canvas, float_images, flash_imgs, select_imgs,
                            warthog, octopus, slug, karel)
            update_menu(canvas, flash_imgs, select_imgs, menu_ui, cloche, cloche2)
            update_cloche(canvas, cloche)
            update_cloche2(canvas, cloche2)
            update_result(canvas, result_imgs_t1, result_imgs_t2, flash_imgs, select_imgs,
                          cloche, cloche2, round1_overlay, round2_overlay,
                          player, player_east, warthog, octopus, slug, karel,
                          ending_ui)
            update_round_overlay(canvas, round1_overlay, round2_overlay,
                                 flash_imgs, select_imgs,
                                 player, player_east,
                                 warthog, octopus, slug, karel,
                                 cloche, cloche2)
            update_flash(canvas, flash_imgs, select_imgs)

        sleep(0.03)     # caps the loop at ~33 frames per second


if __name__ == '__main__':
    main()
