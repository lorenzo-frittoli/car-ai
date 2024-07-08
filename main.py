import pygame

from globals import DISPLAY_SIZE, NET_SIZE, FPS, MAP_FILE, GameState, Game, MapMaker
import globals
from helpers import quit_app
from map_handler.map_handler import MapHandler
from car import Car


def main() -> None:
    pygame.init()
    display = pygame.display.set_mode(DISPLAY_SIZE)
    pygame.display.set_caption("Car AI")
    clock = pygame.time.Clock()

    globals.game_state = GameState(Game())
    map_handler = MapHandler()
    map_handler.load_map(MAP_FILE)
    car = Car(NET_SIZE, pygame.Vector2(100.0, 100.0))
    car.acceleration = pygame.Vector2(5.0, 5.0)

    globals.running = True
    delta_time = 0.0
    while globals.running:
        # print(globals.game_state)
        match globals.game_state.state:
            case Game():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit_app()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            map_handler.reset_map()
                            globals.game_state.state = MapMaker()

                map_handler.display_map(display)
                car.update(delta_time)
                car.display(display)
                car.raycast_(map_handler, display)

            case MapMaker():
                map_handler.run_map_maker(display)

        # End of frame updates
        pygame.display.flip()
        delta_time = clock.tick(FPS) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()
