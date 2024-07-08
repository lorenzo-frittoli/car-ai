from copy import deepcopy
import pygame
import json
import json_fix
import os

from globals import BACKGROUND_COLOR, MAP_FILE, Game
import globals
from helpers import quit_app, standard_to_pygame
from map_handler.map import Map


class MapHandler:
    """
    Class that handles loading and making maps.
    """

    def __init__(self) -> None:
        self.map: Map = Map()
        self.point_radius = 5
        self.line_width = 3
        self.point_color = "black"
        self.line_color = "black"

    def reset_map(self) -> None:
        self.map = Map()

    def display_map(self, display) -> None:
        """
        Displays the map.
        !TODO:  do rendering to img to improve compute times
                for no reason other than being cool.
                In alternative add an array to avoid
                calling `standard_to_pygame` every time
                there is a unit conversion.
        """
        display.fill(BACKGROUND_COLOR)
        for i, chain in enumerate(self.map.chains):
            if not chain.points:
                continue

            points = list(map(standard_to_pygame, chain.points))
            if i == len(self.map.chains)-1:
                points.append(pygame.mouse.get_pos())

            for point in points:
                pygame.draw.circle(display, self.point_color,
                                   point, self.point_radius)

            if len(points) > 1:
                pygame.draw.lines(display, self.line_color,
                                  chain.closed, points, self.line_width)

    def run_map_maker(self, display) -> None:
        """
        Runs the map maker in the main loop.
        """
        for event in pygame.event.get():
            # Close window -> quit
            if event.type == pygame.QUIT:
                quit_app()

            # Keypress
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_g:
                        self.load_map(MAP_FILE)
                        globals.game_state.state = Game()
                    case pygame.K_s:
                        self.save_map(MAP_FILE)

            # Mouse click
            if event.type == pygame.MOUSEBUTTONUP:
                # Left click -> add node
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    self.map.add_point(pos)

                # Right click -> close chain & make new
                if event.button == 3:
                    # Right click + Shift -> make new without closing chain
                    if not pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        self.map.close_chain()
                    self.map.add_chain()

        self.display_map(display)

    def load_map(self, filename: str) -> None:
        """
        Loads a mapfile(json).
        """
        if not os.path.isfile(filename):
            self.map = Map()
        with open(filename, 'r') as f:
            self.map = Map.from_json(f)

    def save_map(self, filename: str) -> None:
        """
        Saves a mapfile.
        """
        cp = deepcopy(self.map)
        with open(filename, 'w') as f:
            f.write(json.dumps(cp, indent=4))
