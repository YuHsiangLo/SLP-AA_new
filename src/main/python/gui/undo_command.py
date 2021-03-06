#from PyQt5.QtCore import ()
from PyQt5.QtWidgets import (
    QUndoCommand
)
#from PyQt5.QtGui import ()


class TranscriptionUndoCommand(QUndoCommand):
    def __init__(self, slot, old_prop, new_prop, **kwargs):
        super().__init__(**kwargs)

        self.slot = slot
        self.old_prop = old_prop
        self.new_prop = new_prop

    def redo(self):
        self.slot.set_value_from_dict(self.new_prop)

    def undo(self):
        self.slot.set_value_from_dict(self.old_prop)


class PredefinedUndoCommand(QUndoCommand):
    def __init__(self, transcription, transcription_list, **kwargs):
        super().__init__(**kwargs)

        self.transcription = transcription
        self.old_trans = transcription.get_hand_transcription()
        self.new_trans = transcription_list
        self.hand = transcription.selected_hand_group.checkedId()

    def redo(self):
        self.transcription.set_predefined(self.new_trans, hand=self.hand)

    def undo(self):
        self.transcription.set_predefined(self.old_trans, hand=self.hand)


class LexicalUndoCommand(QUndoCommand):
    def __init__(self, lexical_field, **kwargs):
        super().__init__(**kwargs)

        self.lexical_field = lexical_field

    def redo(self):
        self.lexical_field.redo()

    def undo(self):
        self.lexical_field.undo()
