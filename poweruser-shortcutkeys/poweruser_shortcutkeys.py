# ------------------------------------------------------------
# MO2 Power User Shortcut Keys - Plugin for Mod Organizer 2
# Author: ferrrett33
# Version: 1.0.0
# Copyright (C) 2025 None reserved
# -------------------------------------------------------------

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QKeySequence, QShortcut
from PyQt6.QtWidgets import QMenu, QPushButton, QTabWidget

import mobase

from .key_config import (
    COLLAPSE_ALL_KEY,
    EXPAND_ALL_KEY,
    PUSH_START_BUTTON_KEY,
    PUSH_START_BUTTON_KEY2,
    OPEN_DISCORD_INVITE_KEY,
    CREATE_EMPTY_MOD_KEY,
    CREATE_SEPARATOR_KEY,
    CHECK_FOR_UPDATES_KEY,
    QUIT_MO2_KEY,
    TAB_WIDGET_NEXT_KEY,
    TAB_WIDGET_PREV_KEY,
    TOGGLE_LOG_KEY,
)

class PowerUserShortcutKeys(mobase.IPlugin):

    def name(self): return "MO2 Power User Shortcut Keys"
    def author(self): return "ferrrett33"
    def description(self): return "A plugin to add more hotkeys."
    def version(self): return mobase.VersionInfo(1, 0, 0, 0)
    def isActive(self): return True
    def settings(self): return []
    
    def __init__(self): super().__init__()

    def init(self, organizer):

        # Create list of items (actions) added directly to main window for easy reference

        keys_data = [
            [PUSH_START_BUTTON_KEY,      self.push_start_button],
            [PUSH_START_BUTTON_KEY2,     self.push_start_button],
            [OPEN_DISCORD_INVITE_KEY,    self.open_discord]
        ]

        # Method to attach to organizer.onUserInterfaceInitialized

        def hook_this(main_window):

            # we'll be adding shortcuts in these 6 places
            self.window = main_window
            self.listoptions_button = self.window.findChild(QPushButton, 'listOptionsBtn')
            self.filemenu = self.window.findChild(QMenu, 'menuFile')
            self.runmenu = self.window.findChild(QMenu, 'menuRun')
            self.viewmenu = self.window.findChild(QMenu, 'menuView')
            self.tabwidget = self.window.findChild(QTabWidget, 'tabWidget')

            # add back and forth to tabs in right pane tab widget
            self.hook_tabwidget()

            # add f-key shortcuts to Run menu, connect to aboutToShow as contents of that menu may change
            self.hook_runmenu()
            self.runmenu.aboutToShow.connect(self.hook_runmenu)

            # add exit shortcut to File menu
            for action in self.filemenu.actions():
                if action.text() == "E&xit":
                    action.setShortcut(QUIT_MO2_KEY)
                    action.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)
                    break

            # add toggle log shortcut to View menu
            for action in self.viewmenu.actions():
                if action.text() == "Log":
                    action.setShortcut(TOGGLE_LOG_KEY)
                    action.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)
                    break

            # listoptionsbutton menu is not created until first clicked, simulate click
            self.listoptions_button.click()
            self.listoptions_button.menu().hide()

            # once the menu has been created hook the shortcut keys
            self.hook_listoptionsbtn_actions()

            # then repeat the same each time button is pressed, since it keeps getting recreated
            self.listoptions_button.pressed.connect(self.hook_listoptionsbtn_actions)

            # add other items directly to main window
            for key_data in keys_data:
                action = QAction("plugin_hotkey", main_window)
                action.setShortcut(QKeySequence(key_data[0]))
                action.triggered.connect(key_data[1])
                main_window.addAction(action)

        # Return the same value to indicate if plugin loaded
        return organizer.onUserInterfaceInitialized(hook_this)

    # class methods

    def hook_tabwidget(self):

        def next_tab():
            self.tabwidget.setCurrentIndex((self.tabwidget.currentIndex() + 1) % self.tabwidget.count())

        def prev_tab():
            self.tabwidget.setCurrentIndex(
                (self.tabwidget.currentIndex() - 1 + self.tabwidget.count()) % self.tabwidget.count())

        QShortcut(TAB_WIDGET_NEXT_KEY, self.tabwidget).activated.connect(next_tab)
        QShortcut(TAB_WIDGET_PREV_KEY, self.tabwidget).activated.connect(prev_tab)


    def hook_listoptionsbtn_actions(self):

        actions = self.listoptions_button.menu().actions()

        for i in actions:
            menutext = i.text()

            match menutext:
                case "Create empty mod":
                    i.setShortcut(CREATE_EMPTY_MOD_KEY)
                case "Create separator":
                    i.setShortcut(CREATE_SEPARATOR_KEY)
                case "Collapse all":
                    i.setShortcut(COLLAPSE_ALL_KEY)
                case "Expand all":
                    i.setShortcut(EXPAND_ALL_KEY)
                case "Check for updates":
                    i.setShortcut(CHECK_FOR_UPDATES_KEY)

            i.setShortcutVisibleInContextMenu(True)
            i.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)


    def hook_runmenu(self):

        fkeys = ["F1","F3","F4","F6","F7","F8","F9","F10","F11","F12"]

        actions = self.runmenu.actions()

        count = 0
        for i in actions:
            i.setShortcut(fkeys[count])
            count+=1
            i.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)


    def push_start_button(self):

        self.window.on_startButton_clicked()


    def open_discord(self):

        self.window.discordTriggered()

