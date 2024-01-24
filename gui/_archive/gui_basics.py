import pygame
from pygame.locals import *


def draw_chart(surface):
    # Funktion zum Zeichnen des Liniendiagramms
    container_width, container_height = surface.get_size()

    # Setze den Hintergrund auf Weiß
    surface.fill((255, 255, 255))

    # Zeichne das Rechteck
    pygame.draw.rect(surface, (200, 200, 200), (50, 50, container_width - 100, container_height - 100))

    # Zeichne die Linie
    pygame.draw.line(surface, (0, 0, 0), (60, 60), (container_width - 60, container_height - 60), 2)
    # Hier kann weiterer Code zum Zeichnen der Datenlinie hinzugefügt werden


def create_gui():
    # Pygame initialisieren
    pygame.init()

    # Bildschirm erstellen
    screen_size = (800, 600)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Einfache GUI")

    # Clock-Objekt für die Framerate-Steuerung
    clock = pygame.time.Clock()

    # Metabar-Konfiguration
    metabar_height = 50
    metabar_bg_color = (0, 0, 0)
    metabar_logo = pygame.image.load("../REMonitor_Logo.png")
    metabar_logo = pygame.transform.scale(metabar_logo, (200, metabar_height))

    # Navigationsbereich-Konfiguration
    navigation_width = 200
    navigation_bg_color = (0, 0, 0)

    # Hauptfenster-Konfiguration
    main_width = screen_size[0] - navigation_width
    main_height = screen_size[1] - metabar_height
    main_bg_color = (255, 255, 255)

    # Filterbereich-Konfiguration
    filter_width = 200
    filter_height = main_height - 50
    filter_bg_color = (255, 255, 255)

    # Liste der Filterpunkte
    filter_labels = ["Region", "Preisart", "Filter", "Zeitraum"]
    dropdown_height = 40
    dropdown_font = pygame.font.Font(None, 24)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Bildschirm zeichnen
        screen.fill((255, 255, 255))  # Weißer Hintergrund für das Hauptfenster

        # Metabar zeichnen
        pygame.draw.rect(screen, metabar_bg_color, (0, 0, screen_size[0], metabar_height))
        screen.blit(metabar_logo, (0, 0))

        # Navigationsbereich zeichnen
        pygame.draw.rect(screen, navigation_bg_color, (0, metabar_height, navigation_width, main_height))

        # Klickbare Menüpunkte im Navigationsbereich
        menu_labels = ["Stadtplan", "Preisvergleich", "Regionsanalyse"]
        font = pygame.font.Font(None, 36)
        for i, label in enumerate(menu_labels):
            text = font.render(label, True, (255, 255, 255))
            text_rect = text.get_rect(center=(navigation_width // 2, metabar_height + (i + 1) * 100))
            screen.blit(text, text_rect)

        # Hauptfenster zeichnen
        pygame.draw.rect(screen, main_bg_color, (navigation_width, metabar_height, main_width, main_height))

        # Filterbereich zeichnen
        pygame.draw.rect(screen, filter_bg_color,
                         (navigation_width + 25, metabar_height + 25, filter_width, filter_height))

        # Filterpunkte im Filterbereich zeichnen
        for i, label in enumerate(filter_labels):
            dropdown_rect = pygame.Rect(navigation_width + 30, metabar_height + 30 + i * (dropdown_height + 10),
                                        filter_width - 40, dropdown_height)

            # Zeichne den hellgrauen Hintergrund für jeden Filterpunkt
            pygame.draw.rect(screen, (200, 200, 200), dropdown_rect)

            # Zeichne den Rahmen für jeden Filterpunkt
            pygame.draw.rect(screen, (0, 0, 0), dropdown_rect, 2)

            text = dropdown_font.render(label, True, (0, 0, 0))
            text_rect = text.get_rect(center=dropdown_rect.center)
            screen.blit(text, text_rect)

        # Liniendiagramm zeichnen
        chart_surface = pygame.Surface((main_width - 200, main_height - 50))
        draw_chart(chart_surface)
        screen.blit(chart_surface, (navigation_width + 200, metabar_height))



        # Aktualisiere den Bildschirm
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


# Starten Sie die GUI-Anwendung
create_gui()
