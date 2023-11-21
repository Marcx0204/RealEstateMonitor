import pygame
import pygame_gui
import os


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
    info = pygame.display.Info()  # Informationen über den Bildschirm erhalten
    screen_size = (info.current_w * 0.9, info.current_h * 0.9)  # Bildschirmgröße verwenden
    screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)  # RESIZABLE macht das Fenster anpassbar
    pygame.display.set_caption("Einfache GUI")
    manager = pygame_gui.UIManager(screen_size)

    # Clock-Objekt für die Framerate-Steuerung
    clock = pygame.time.Clock()

    # Metabar-Konfiguration
    metabar_height = int(screen_size[1] * 0.08)  # Höhe der Metabar als Prozentsatz der Bildschirmhöhe
    metabar_bg_color = (0, 0, 0)
    metabar_logo = pygame.image.load("REMonitor_Logo.png")
    metabar_logo = pygame.transform.scale(metabar_logo, (int(screen_size[0] * 0.15), metabar_height))

    # Navigationsbereich-Konfiguration
    navigation_width = int(screen_size[0] * 0.15)
    navigation_bg_color = (0, 0, 0)

    # Hauptfenster-Konfiguration
    main_width = screen_size[0] - navigation_width
    main_height = screen_size[1] - metabar_height
    main_bg_color = (255, 255, 255)

    # Filterbereich-Konfiguration
    filter_width = int(screen_size[0] * 0.2)
    filter_height = main_height - int(metabar_height * 0.5)
    filter_bg_color = (255, 255, 255)

    # DropDown-Menü für "Bezirk" hinzufügen
    manager = pygame_gui.UIManager(screen.get_size())
    dropdown_bezirk_rect = pygame.Rect(navigation_width + 30, metabar_height + 30, filter_width - 40, 40)
    dropdown_bezirk_menu = pygame_gui.elements.UIDropDownMenu(['Bezirk auswählen', '1. Bezirk', '2. Bezirk', '3. Bezirk'],
                                                       'Bezirk auswählen', dropdown_bezirk_rect, manager)

    # DropDown-Menüs für "Preis" hinzufügen
    dropdown_preis_rect = pygame.Rect(navigation_width + 30, metabar_height + 90, filter_width - 40, 40)
    dropdown_preis_menu = pygame_gui.elements.UIDropDownMenu(['Preis auswählen', 'absolut', 'relativ'],
                                                             'Preis auswählen', dropdown_preis_rect, manager)

    # DropDown-Menüs für "Filter" hinzufügen
    dropdown_filter_rect = pygame.Rect(navigation_width + 30, metabar_height + 150, filter_width - 40, 40)
    dropdown_filter_menu = pygame_gui.elements.UIDropDownMenu(['Filter auswählen', 'Widmung', 'Bauklasse'],
                                                              'Filter auswählen', dropdown_filter_rect, manager)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            manager.process_events(event)

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

        # Liniendiagramm zeichnen
        chart_surface = pygame.Surface((main_width - filter_width - 50, main_height - 50))
        draw_chart(chart_surface)
        screen.blit(chart_surface, (navigation_width + filter_width + 50, metabar_height))

        manager.update(clock.tick(30) / 1000.0)
        manager.draw_ui(screen)

        # Aktualisiere den Bildschirm
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


# Starten Sie die GUI-Anwendung
create_gui()
