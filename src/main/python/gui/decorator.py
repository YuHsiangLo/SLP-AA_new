import os
import functools
from datetime import date
from PyQt5.QtWidgets import (
    QMessageBox,
    QFileDialog
)


def check_unsaved_change(func):
    @functools.wraps(func)
    def wrapper_check_unsaved_change(self, event, *args, **kwargs):
        if not self.undostack.isClean():
            response = QMessageBox.question(self, 'Unsaved Changes', 'You have unsaved changes. Are you sure you want to close the app?')
            if response == QMessageBox.No:
                return event.ignore()
        func(self, event, *args, **kwargs)
    return wrapper_check_unsaved_change


def check_date_format(func):
    @functools.wraps(func)
    def wrapper_check_date_format(self, *args, **kwargs):
        if len(self.update_edit.text().split(sep='-')) != 3:
            QMessageBox.critical(self, 'Date Format Error',
                                 'Please make sure your date follows the format of YYYY-MM-DD.')
            return
        try:
            year, month, day = self.update_edit.text().split(sep='-')
            date(int(year), int(month), int(day))
        except ValueError as error:
            QMessageBox.critical(self, 'Date Format Error', str(error))
            return
        else:
            return func(self, *args, **kwargs)
    return wrapper_check_date_format


def check_empty_gloss(func):
    @functools.wraps(func)
    def wrapper_check_empty_gloss(self, *args, **kwargs):
        if not self.gloss_edit.text():
            QMessageBox.critical(self, 'Empty Gloss', 'Gloss cannot be empty.')
            return
        else:
            return func(self, *args, **kwargs)
    return wrapper_check_empty_gloss


def check_duplicated_gloss(func):
    @functools.wraps(func)
    def wrapper_duplicated_gloss(self, *args, **kwargs):
        lexical_info = self.lexical_scroll.get_value()
        if lexical_info is None:
            return
        else:
            if self.current_sign:
                if lexical_info['gloss'] == self.current_sign.lexical_information.gloss or lexical_info['gloss'] not in self.corpus.get_sign_glosses():
                    return func(self, *args, **kwargs)

            if lexical_info['gloss'] in self.corpus.get_sign_glosses():
                QMessageBox.critical(self, 'Duplicated Gloss',
                                     'Please use a different gloss. Duplicated glosses are not allowed.')
                return
            else:
                return func(self, *args, **kwargs)
    return wrapper_duplicated_gloss


def check_unsaved_corpus(func):
    @functools.wraps(func)
    def wrapper_check_unsaved_corpus(self, *args, **kwargs):
        if self.corpus.path is None:
            file_name, _ = QFileDialog.getSaveFileName(self,
                                                       self.tr('Save Corpus'),
                                                       os.path.join(self.app_settings['storage']['recent_folder'],
                                                                    'corpus.slpaa'),
                                                       self.tr('SLAP-AA Corpus (*.slpaa)'))
            if file_name:
                self.corpus.path = file_name
                folder, _ = os.path.split(file_name)
                if folder:
                    self.app_settings['storage']['recent_folder'] = folder
        return func(self, *args, **kwargs)

    return wrapper_check_unsaved_corpus
