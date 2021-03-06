#from PyQt5.QtCore import ()
from PyQt5.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QTabWidget,
    QSpinBox,
    QCheckBox,
    QMessageBox,
    QDialogButtonBox,
    QLineEdit,
    QLabel
)
#from PyQt5.QtGui import ()


class DisplayTab(QWidget):
    def __init__(self, settings, **kwargs):
        super().__init__(**kwargs)

        self.settings = settings

        main_layout = QFormLayout()
        self.setLayout(main_layout)

        self.decimal_place = QSpinBox(parent=self)
        self.decimal_place.setMinimum(0)
        self.decimal_place.setMaximum(10)
        self.decimal_place.setValue(settings['display']['sig_figs'])
        main_layout.addRow(QLabel('Number of displayed decimal places:'), self.decimal_place)

        self.coder_name = QLineEdit(settings['metadata']['coder'], parent=self)
        main_layout.addRow(QLabel('Preferred coder name:'), self.coder_name)

        self.show_tooltip = QCheckBox(parent=self)
        self.show_tooltip.setChecked(settings['display']['tooltips'])
        main_layout.addRow(QLabel('Show tooltip:'), self.show_tooltip)

    def save_settings(self):
        self.settings['display']['sig_figs'] = int(self.decimal_place.value())
        self.settings['display']['tooltips'] = self.show_tooltip.isChecked()
        self.settings['metadata']['coder'] = str(self.coder_name.text())


class ReminderTab(QWidget):
    def __init__(self, settings, **kwargs):
        super().__init__(**kwargs)
        self.settings = settings

        main_layout = QFormLayout()
        self.setLayout(main_layout)

        self.overwrite_reminder = QCheckBox(parent=self)
        self.overwrite_reminder.setChecked(settings['reminder']['overwrite'])
        main_layout.addRow(QLabel('Always ask before overwriting a sign:'), self.overwrite_reminder)

    def save_settings(self):
        self.settings['reminder']['overwrite'] = self.overwrite_reminder.isChecked()


class PreferenceDialog(QDialog):
    def __init__(self, settings, **kwargs):
        super().__init__(**kwargs)

        self.settings = settings

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        tabs = QTabWidget(parent=self)
        main_layout.addWidget(tabs)

        self.display_tab = DisplayTab(settings, parent=self)
        tabs.addTab(self.display_tab, 'Display')

        self.reminder_tab = ReminderTab(settings, parent=self)
        tabs.addTab(self.reminder_tab, 'Reminder')

        buttons = QDialogButtonBox.Save | QDialogButtonBox.Cancel
        self.button_box = QDialogButtonBox(buttons, parent=self)
        main_layout.addWidget(self.button_box)

        # Ref: https://programtalk.com/vs2/python/654/enki/enki/core/workspace.py/
        self.button_box.clicked.connect(self.handle_button_click)

    def handle_button_click(self, button):
        standard = self.button_box.standardButton(button)
        if standard == QDialogButtonBox.Cancel:
            self.reject()
        elif standard == QDialogButtonBox.Save:
            self.display_tab.save_settings()
            self.reminder_tab.save_settings()

            QMessageBox.information(self, 'Preferences Saved', 'New preferences saved!')
            self.accept()
