import pygame
import pygame_gui
import os


def draw_line_chart(surface):
    # Funktion zum Zeichnen des Liniendiagramms
    container_width, container_height = surface.get_size()

    # Setze den Hintergrund auf Weiß
    surface.fill((255, 255, 255))

    # Zeichne das Rechteck
    pygame.draw.rect(surface, (200, 200, 200), (50, 50, container_width - 100, container_height - 100))

    # Zeichne die Linie
    pygame.draw.line(surface, (0, 0, 0), (60, 60), (container_width - 60, container_height - 60), 2)
    # Hier kann weiterer Code zum Zeichnen der Datenlinie hinzugefügt werden

def draw_bar_chart(surface):
    # Funktion zum Zeichnen des Balkendiagramms
    container_width, container_height = surface.get_size()

    # Setze den Hintergrund auf Weiß
    surface.fill((255, 255, 255))

    # Beispiel-Daten für das Balkendiagramm (höhen von Balken)
    bar_data = [0.3, 0.5, 0.8, 0.4]  # Beispielwerte, die die Balkenhöhen repräsentieren

    # Balkendiagramm zeichnen
    bar_width = 50
    gap = 10
    start_x = 50
    max_height = container_height - 100

    for i, height_ratio in enumerate(bar_data):
        bar_height = int(max_height * height_ratio)
        bar_x = start_x + (bar_width + gap) * i
        bar_y = container_height - bar_height - 50  # Startpunkt der Balken (y-Koordinate)

        pygame.draw.rect(surface, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height))

def hide_dropdown_menus(menus):
    for menu in menus:
        if menu:
            menu.disable()
            menu.hide()

def create_gui():

    #********** BASIS CODE ****************

    # Pygame initialisieren
    pygame.init()

    # Bildschirm erstellen
    info = pygame.display.Info()  # Informationen über den Bildschirm erhalten
    screen_size = (info.current_w * 0.9, info.current_h * 0.9)  # Bildschirmgröße verwenden
    screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)  # RESIZABLE macht das Fenster anpassbar
    pygame.display.set_caption("Einfache GUI")
    manager = pygame_gui.UIManager(screen.get_size())

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

    running = True
    current_view = "Preisvergleich"  # Current view

    # Create buttons for Stadtplan, Preisvergleich, and Regionsanalyse
    button_height = 60
    stadtplan_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(10, metabar_height + 10, navigation_width - 20, button_height),
        text="Stadtplan",
        manager=manager
    )
    preisvergleich_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(10, metabar_height + 10 + button_height + 10, navigation_width - 20, button_height),
        text="Preisvergleich",
        manager=manager
    )
    regionsanalyse_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(10, metabar_height + 10 + 2 * (button_height + 10), navigation_width - 20,
                                  button_height),
        text="Regionsanalyse",
        manager=manager
    )

    # Initialisierung des Dropdown-Menüs für "Bezirk" außerhalb der Haupt-Schleife
    bezirke_liste = ['Bezirk auswählen'] + [f'{i}. Bezirk' for i in range(1, 24)]
    selected_bezirk = 'Bezirk auswählen'
    dropdown_bezirk_menu = None
    dropdown_preis_menu = None
    dropdown_filter_menu = None



    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Check button clicks
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == stadtplan_button:
                        current_view = "Stadtplan"
                        hide_dropdown_menus([dropdown_preis_menu, dropdown_filter_menu, dropdown_bezirk_menu])
                        print("Wechsel zur Stadtplan-Ansicht")
                        dropdown_bezirk_rect = pygame.Rect(navigation_width + 30, metabar_height + 30,
                                                           filter_width - 40, 40)
                        dropdown_bezirk_menu = pygame_gui.elements.UIDropDownMenu(
                            bezirke_liste, selected_bezirk, dropdown_bezirk_rect, manager)

                        # DropDown-Menüs für "Preis" hinzufügen
                        dropdown_preis_rect = pygame.Rect(navigation_width + 30, metabar_height + 90, filter_width - 40,
                                                          40)
                        dropdown_preis_menu = pygame_gui.elements.UIDropDownMenu(
                            ['Preis auswählen', 'absolut', 'relativ'],
                            'Preis auswählen', dropdown_preis_rect, manager)

                        # DropDown-Menüs für "Filter" hinzufügen
                        dropdown_filter_rect = pygame.Rect(navigation_width + 30, metabar_height + 150,
                                                           filter_width - 40, 40)
                        dropdown_filter_menu = pygame_gui.elements.UIDropDownMenu(
                            ['Zuordnung auswählen', 'Ein-, Zweifamilienhaus', 'Betriebsobjekt', 'Kleingarten'],
                            'Zuordnung auswählen', dropdown_filter_rect, manager)
                    elif event.ui_element == preisvergleich_button:
                        current_view = "Preisvergleich"
                        hide_dropdown_menus([dropdown_preis_menu, dropdown_filter_menu, dropdown_bezirk_menu])
                        print("Wechsel zur Preisvergleich-Ansicht")
                        dropdown_bezirk_rect = pygame.Rect(navigation_width + 30, metabar_height + 30,
                                                           filter_width - 40, 40)
                        dropdown_bezirk_menu = pygame_gui.elements.UIDropDownMenu(
                            bezirke_liste, selected_bezirk, dropdown_bezirk_rect, manager)

                        # DropDown-Menüs für "Preis" hinzufügen
                        dropdown_preis_rect = pygame.Rect(navigation_width + 30, metabar_height + 90, filter_width - 40,
                                                          40)
                        dropdown_preis_menu = pygame_gui.elements.UIDropDownMenu(
                            ['Preis auswählen', 'absolut', 'relativ'],
                            'Preis auswählen', dropdown_preis_rect, manager)

                        # DropDown-Menüs für "Filter" hinzufügen
                        dropdown_filter_rect = pygame.Rect(navigation_width + 30, metabar_height + 150,
                                                           filter_width - 40, 40)
                        dropdown_filter_menu = pygame_gui.elements.UIDropDownMenu(
                            ['Zuordnung auswählen', 'Ein-, Zweifamilienhaus', 'Betriebsobjekt', 'Kleingarten'],
                            'Zuordnung auswählen', dropdown_filter_rect, manager)
                    elif event.ui_element == regionsanalyse_button:
                        current_view = "Regionsanalyse"
                        hide_dropdown_menus([dropdown_preis_menu, dropdown_filter_menu, dropdown_bezirk_menu])
                        print("Wechsel zur Regionsanalyse-Ansicht")

                        dropdown_bezirk_rect = pygame.Rect(navigation_width + 30, metabar_height + 30,
                                                           filter_width - 40, 40)
                        dropdown_bezirk_menu = pygame_gui.elements.UIDropDownMenu(
                            bezirke_liste, selected_bezirk, dropdown_bezirk_rect, manager)

                        # DropDown-Menüs für "Filter" hinzufügen
                        dropdown_filter_rect = pygame.Rect(navigation_width + 30, metabar_height + 150,
                                                           filter_width - 40, 40)
                        dropdown_filter_menu = pygame_gui.elements.UIDropDownMenu(
                            ['Zuordnung auswählen', 'Ein-, Zweifamilienhaus', 'Betriebsobjekt', 'Kleingarten'],
                            'Zuordnung auswählen', dropdown_filter_rect, manager)

            manager.process_events(event)

        # Bildschirm zeichnen
        screen.fill((255, 255, 255))  # Weißer Hintergrund für das Hauptfenster

        # Metabar zeichnen
        pygame.draw.rect(screen, metabar_bg_color, (0, 0, screen_size[0], metabar_height))
        screen.blit(metabar_logo, (0, 0))

        # Navigationsbereich zeichnen
        pygame.draw.rect(screen, navigation_bg_color, (0, metabar_height, navigation_width, main_height))

        # Hauptfenster zeichnen
        pygame.draw.rect(screen, main_bg_color, (navigation_width, metabar_height, main_width, main_height))

        # Filterbereich zeichnen
        pygame.draw.rect(screen, filter_bg_color,
                         (navigation_width + 25, metabar_height + 25, filter_width, filter_height))

        # Diagrammbereich zeichnen
        chart_surface = pygame.Surface((main_width - filter_width - 50, main_height - 50))

        # ********** CODE JE NACH MENÜPUNKT ****************


        if current_view == "Stadtplan":

            pass

        elif current_view == "Preisvergleich":

            pass

        elif current_view == "Regionsanalyse":

            pass

        manager.update(clock.tick(30) / 1000.0)
        manager.draw_ui(screen)

        # Aktualisiere den Bildschirm
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


# Starten Sie die GUI-Anwendung
create_gui()
