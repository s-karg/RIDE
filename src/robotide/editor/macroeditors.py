#  Copyright 2008-2011 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import wx
from robotide.usages.UsageRunner import Usages
from robotide.editor.kweditor import KeywordEditor
from robotide.editor.editors import _RobotTableEditor, WithFindUsages
from robotide.publish.messages import RideItemNameChanged
from robotide.widgets.button import ButtonWithHandler
from robotide.widgets.sizers import HorizontalSizer


class TestCaseEditor(_RobotTableEditor):
    _settings_open_id = 'test case settings open'

    def _populate(self):
        self.header = self._create_header(self.controller.name)
        self.sizer.Add(self.header, 0, wx.EXPAND|wx.ALL, 5)
        self._add_settings()
        self.sizer.Add((0,10))
        self._create_kweditor()
        self.plugin.subscribe(self._name_changed, RideItemNameChanged)

    def _create_kweditor(self):
        self.kweditor = KeywordEditor(self, self.controller, self._tree)
        self.sizer.Add(self.kweditor, 1, wx.EXPAND|wx.ALL, 2)
        self._editors.append(self.kweditor)

    def _name_changed(self, data):
        if data.item == self.controller:
            self.header.SetLabel(data.item.name)

    def close(self):
        for editor in self._editors:
            editor.close()
        _RobotTableEditor.close(self)
        self.kweditor.close()
        self.plugin.unsubscribe(self._name_changed, RideItemNameChanged)

    def save(self):
        self.kweditor.save()

    def undo(self):
        self.kweditor.OnUndo()

    def redo(self):
        self.kweditor.OnRedo()

    def cut(self):
        self.kweditor.OnCut()

    def copy(self):
        self.kweditor.OnCopy()

    def paste(self):
        self.kweditor.OnPaste()

    def insert(self):
        self.kweditor.OnInsert()

    def insert_rows(self):
        self.kweditor.OnInsertRows()

    def delete_rows(self):
        self.kweditor.OnDeleteRows()

    def delete(self):
        self.kweditor.OnDelete()

    def comment(self):
        self.kweditor.OnCommentRows()

    def uncomment(self):
        self.kweditor.OnUncommentRows()

    def show_content_assist(self):
        self.kweditor.show_content_assist()

    def view(self):
        _RobotTableEditor.view(self)
        self.kweditor.SetFocus()


class UserKeywordHeader(HorizontalSizer):

    def __init__(self):
        HorizontalSizer.__init__(self)

    def SetLabel(self, label):
        self._header.SetLabel(label)

    def add_header(self, header):
        self._header = header
        self.add_expanding(self._header)


class UserKeywordEditor(TestCaseEditor, WithFindUsages):
    _settings_open_id = 'user keyword settings open'

    def _create_header(self, name):
        return self._usage_button_header(_RobotTableEditor._create_header(self, name), Usages)
