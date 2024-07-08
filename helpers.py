from dataclasses import dataclass
import pygame

from globals import DISPLAY_SIZE
import globals


def quit_app() -> None:
    """
    Quits the application.
    """
    globals.running = False


def line_intersection(p1, p2, p3, p4) -> None | pygame.Vector2:
    """
    return None or Vector2 of intersect
    """
    x1, y1, x2, y2 = *p1, *p2
    x3, y3, x4, y4 = *p3, *p4
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if den == 0:
        return

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    u = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / den
    if 0 < t < 1 and 0 < u < 1:
        return pygame.Vector2(x1 + t * (x2 - x1),
                              y1 + t * (y2 - y1))


def clamp(var: pygame.Vector2, bounds: tuple[tuple]):
    for i in range(len(var)):
        var[i] = max(bounds[i][0], min(var[i], bounds[i][1]))
    return var


def pygame_to_standard(pos: tuple[float, float]) -> tuple[float, float]:
    unit = min(DISPLAY_SIZE)
    return (pos[0] / unit, pos[1] / unit)


def standard_to_pygame(pos: tuple[float, float]) -> tuple[float, float]:
    unit = min(DISPLAY_SIZE)
    return (pos[0] * unit, pos[1] * unit)
