# -*- coding: utf-8 -*-
####################################################
##                                                ##
##           Image Occlusion Enhanced             ##
##                                                ##
##        Copyright (c) Glutanimate 2016          ##
##       (https://github.com/Glutanimate)         ##
##                                                ##
##     Original Image Occlusion 2.0 add-on is     ##
##         Copyright (c) 2012-2015 tmbb           ##
##           (https://github.com/tmbb)            ##
##                                                ##
####################################################

from PyQt4 import QtCore, QtGui
from aqt.qt import *

from aqt import mw, webview, deckchooser, tagedit
from aqt.utils import saveGeom, restoreGeom

from config import *

class ImgOccEdit(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, parent=None)
        self.mode = mw.ImgOccAdd.mode
        self.setupUi()
        restoreGeom(self, "imageOccEditor")

    def closeEvent(self, event):
        if mw.pm.profile is not None:
            saveGeom(self, "imageOccEditor")
        QWidget.closeEvent(self, event)

    def setupUi(self):
        self.svg_edit = webview.AnkiWebView()
        self.svg_edit.setCanFocus(True) # focus necessary for hotkeys

        editing_text = "<b>Instructions for editing</b>:\
            Each mask shape represents a card.\
            Removing any of the existing shapes will remove the corresponding card.\
            New shapes will generate new cards. You can change the occlusion type\
            by using the dropdown box on the left. If you click on the <i>Add new \
            cards</i> button a completely new batch of cards will be generated, \
            leaving your originals untouched."

        self.edit_label = QLabel(editing_text)
        self.edit_label.setWordWrap(True)

        self.header_edit = QPlainTextEdit()
        self.header_label = QLabel(IO_FLDS["header"])
        header_hbox = QHBoxLayout()
        header_hbox.addWidget(self.header_label)
        header_hbox.addWidget(self.header_edit)

        self.footer_edit = QPlainTextEdit()
        self.footer_label = QLabel(IO_FLDS["footer"])
        footer_hbox = QHBoxLayout()
        footer_hbox.addWidget(self.footer_label)
        footer_hbox.addWidget(self.footer_edit)

        self.remarks_edit = QPlainTextEdit()
        self.remarks_label = QLabel(IO_FLDS["remarks"])
        remarks_hbox = QHBoxLayout()
        remarks_hbox.addWidget(self.remarks_label)
        remarks_hbox.addWidget(self.remarks_edit)

        self.sources_edit = QPlainTextEdit()
        self.sources_label = QLabel(IO_FLDS["sources"])
        sources_hbox = QHBoxLayout()
        sources_hbox.addWidget(self.sources_label)
        sources_hbox.addWidget(self.sources_edit)

        self.extra1_edit = QPlainTextEdit()
        self.extra1_label = QLabel(IO_FLDS["extra1"])
        extra1_hbox = QHBoxLayout()
        extra1_hbox.addWidget(self.extra1_label)
        extra1_hbox.addWidget(self.extra1_edit)

        self.extra2_edit = QPlainTextEdit()
        self.extra2_label = QLabel(IO_FLDS["extra2"])
        extra2_hbox = QHBoxLayout()
        extra2_hbox.addWidget(self.extra2_label)
        extra2_hbox.addWidget(self.extra2_edit)

        self.tags_edit = tagedit.TagEdit(self)
        self.tags_label = QLabel("Tags")
        tags_hbox = QHBoxLayout()
        tags_hbox.addWidget(self.tags_label)
        tags_hbox.addWidget(self.tags_edit)

        deck_container = QGroupBox()
        self.deckChooser = deckchooser.DeckChooser(mw, deck_container,
                                                   label=True) 

        for i in [self.header_edit, self.footer_edit, self.remarks_edit, 
            self.sources_edit, self.extra1_edit, self.extra2_edit]:
            i.setTabChangesFocus(True)

        for i in [self.header_label, self.footer_label, self.remarks_label, 
            self.sources_label, self.extra1_label, self.extra2_label, self.tags_label]:
            i.setFixedWidth(70)        

        # Create buttons

        self.bottom_label = QLabel()
        button_box = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal, self)
        button_box.setCenterButtons(False)

        self.occl_tp_select = QComboBox()
        self.occl_tp_select.addItems(["Don't change", "All Hidden, One Revealed",
            "All Hidden, All Revealed", "One Hidden, All Revealed"])

        self.edit_btn = button_box.addButton("&Edit cards",
                QDialogButtonBox.ActionRole)
        self.new_btn = button_box.addButton("&Add new cards",
                QDialogButtonBox.ActionRole)
        self.ao_btn = button_box.addButton(u"All Hidden, &One Revealed",
                QDialogButtonBox.ActionRole)
        self.aa_btn = button_box.addButton(u"All Hidde&n, All Revealed",
                QDialogButtonBox.ActionRole)
        self.oa_btn = button_box.addButton(u"One Hidden, &All Revealed",
                QDialogButtonBox.ActionRole)
        self.close_button = button_box.addButton("&Close", 
                QDialogButtonBox.RejectRole)

        dc_tt = "Preserve existing occlusion type"
        edit_tt = "Edit all cards using current mask shapes and field entries"
        new_tt = "Create new batch of cards without editing existing ones"
        ao_tt = "Formerly known as nonoverlapping.<br>\
            Generate cards where all labels are hidden and just one is revealed<br>\
            on the back"
        aa_tt = "A step between nonoverlapping and overlapping.<br>\
            Generate cards where all labels are hidden on the front, but all \
            revealed on the back"
        oa_tt = "Formerly known as overlapping.<br>\
            Generate cards where just one label is hidden on the front and all\
            revealed on the back"
        close_tt = "Close Image Occlusion Editor without generating cards"

        self.edit_btn.setToolTip(edit_tt)
        self.new_btn.setToolTip(new_tt)
        self.ao_btn.setToolTip(ao_tt)
        self.aa_btn.setToolTip(aa_tt)
        self.oa_btn.setToolTip(oa_tt)
        self.close_button.setToolTip(close_tt)
        self.occl_tp_select.setItemData(0, dc_tt, Qt.ToolTipRole)
        self.occl_tp_select.setItemData(1, ao_tt, Qt.ToolTipRole)
        self.occl_tp_select.setItemData(2, aa_tt, Qt.ToolTipRole)
        self.occl_tp_select.setItemData(3, oa_tt, Qt.ToolTipRole)

        self.connect(self.edit_btn, SIGNAL("clicked()"), self.edit_all)
        self.connect(self.new_btn, SIGNAL("clicked()"), self.new)
        self.connect(self.ao_btn, SIGNAL("clicked()"), self.add_ao)
        self.connect(self.aa_btn, SIGNAL("clicked()"), self.add_aa)
        self.connect(self.oa_btn, SIGNAL("clicked()"), self.add_oa)
        self.connect(self.close_button, SIGNAL("clicked()"), self.close)

        bottom_hbox = QHBoxLayout()
        bottom_hbox.addWidget(self.bottom_label)
        bottom_hbox.addWidget(self.occl_tp_select)
        bottom_hbox.addWidget(button_box)

        # Set layout up

        ## Tab 1
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.svg_edit, stretch=1)
        vbox1.addWidget(self.edit_label)

        ## Tab 2
        vbox2 = QVBoxLayout()
        vbox2.addLayout(header_hbox)
        vbox2.addLayout(footer_hbox)
        vbox2.addLayout(remarks_hbox)
        vbox2.addLayout(sources_hbox)
        vbox2.addLayout(extra1_hbox)
        vbox2.addLayout(extra2_hbox)
        vbox2.addLayout(tags_hbox)
        vbox2.addWidget(deck_container)

        # Create tabs, set their layout, add them to the QTabWidget
        tab1 = QWidget()
        tab2 = QWidget()
        tab1.setLayout(vbox1)
        tab2.setLayout(vbox2)
        self.tab_widget = QtGui.QTabWidget() 
        self.tab_widget.addTab(tab1,"&Masks Editor")
        self.tab_widget.addTab(tab2,"&Fields")
        self.tab_widget.setTabToolTip(1, "Include additional information (optional)")
        self.tab_widget.setTabToolTip(0, "Create image occlusion masks (required)")

        # Add all widgets to main window
        vbox_main = QtGui.QVBoxLayout()
        vbox_main.setMargin(5);
        vbox_main.addWidget(self.tab_widget)
        vbox_main.addLayout(bottom_hbox)
        self.setLayout(vbox_main)

        # Define and connect key bindings
        self.connect(QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Tab"), self), 
            QtCore.SIGNAL('activated()'), self.switch_tabs)
        self.connect(QtGui.QShortcut(QtGui.QKeySequence("Ctrl+r"), self), 
            QtCore.SIGNAL('activated()'), self.reset_main_fields)
        self.connect(QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Shift+r"), self), 
            QtCore.SIGNAL('activated()'), self.reset_all_fields)
        self.connect(QtGui.QShortcut(QtGui.QKeySequence("Ctrl+1"), self), 
            QtCore.SIGNAL('activated()'), lambda:self.focus_field(self.header_edit))
        self.connect(QtGui.QShortcut(QtGui.QKeySequence("Ctrl+2"), self), 
            QtCore.SIGNAL('activated()'), lambda:self.focus_field(self.footer_edit))
        self.connect(QtGui.QShortcut(QtGui.QKeySequence("Ctrl+3"), self), 
            QtCore.SIGNAL('activated()'), lambda:self.focus_field(self.remarks_edit))
        self.connect(QtGui.QShortcut(QtGui.QKeySequence("Ctrl+4"), self), 
            QtCore.SIGNAL('activated()'), lambda:self.focus_field(self.sources_edit))
        self.connect(QtGui.QShortcut(QtGui.QKeySequence("Ctrl+5"), self), 
            QtCore.SIGNAL('activated()'), lambda:self.focus_field(self.extra1_edit))
        self.connect(QtGui.QShortcut(QtGui.QKeySequence("Ctrl+6"), self), 
            QtCore.SIGNAL('activated()'), lambda:self.focus_field(self.extra2_edit))
        self.connect(QtGui.QShortcut(QtGui.QKeySequence("Ctrl+d"), self), 
            QtCore.SIGNAL('activated()'), deck_container.setFocus)
        self.connect(QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Shift+t"), self), 
            QtCore.SIGNAL('activated()'), lambda:self.focus_field(self.tags_edit))
        self.connect(QtGui.QShortcut(QtGui.QKeySequence("Ctrl+i"), self), 
            QtCore.SIGNAL('activated()'), self.svg_edit.setFocus)
        self.connect(QtGui.QShortcut(QtGui.QKeySequence("Ctrl+f"), self), 
            QtCore.SIGNAL('activated()'), self.fit_image_canvas)

        # Set Focus
        self.tab_widget.setCurrentIndex(0)
        self.svg_edit.setFocus()

    # Note actions
    def add_ao(self): 
        mw.ImgOccAdd.onAddNotesButton("ao")
    def add_aa(self): 
        mw.ImgOccAdd.onAddNotesButton("aa")
    def add_oa(self): 
        mw.ImgOccAdd.onAddNotesButton("oa")
    def new(self):
        choice = self.occl_tp_select.currentText()
        mw.ImgOccAdd.onAddNotesButton(choice)
    def edit_all(self):
        choice = self.occl_tp_select.currentText()
        mw.ImgOccAdd.onAddNotesButton(choice, True)
        print "btnpress"

    # Modes
    def switch_to_mode(self, mode):
        hide_on_add = [self.edit_label, self.occl_tp_select, 
                        self.edit_btn, self.new_btn]
        hide_on_edit = [self.ao_btn, self.aa_btn, self.oa_btn]
        if mode == "add":
            for i in hide_on_add:
                i.hide()
            for i in hide_on_edit:
                i.show()
            dl_txt = "Deck"
            ttl = "Image Occlusion Enhanced - Add mode"
            bl_txt = "Add card type:"
        else:
            for i in hide_on_add:
                i.show()
            for i in hide_on_edit:
                i.hide()
            dl_txt = "Deck for <i>Add new cards</i>"
            ttl = "Image Occlusion Enhanced - Editing mode"
            bl_txt = "Choose card type:"
        self.deckChooser.deckLabel.setText(dl_txt)
        self.setWindowTitle(ttl)
        self.bottom_label.setText(bl_txt)

    # Other actions
    def reset_window(self):
        self.reset_all_fields()
        self.tab_widget.setCurrentIndex(0)
        self.occl_tp_select.setCurrentIndex(0)
        self.header_edit.setFocus()
        self.svg_edit.setFocus()

    def switch_tabs(self):
        currentTab = self.tab_widget.currentIndex()
        if currentTab == 0:
          self.tab_widget.setCurrentIndex(1)
          if isinstance(QApplication.focusWidget(), QPushButton):
              self.header_edit.setFocus()
        else:
          self.tab_widget.setCurrentIndex(0)

    def focus_field(self, target_field):
        self.tab_widget.setCurrentIndex(1)
        target_field.setFocus()

    def reset_main_fields(self):
        for i in [self.header_edit, self.footer_edit, self.remarks_edit, 
          self.extra1_edit, self.extra2_edit]:
            i.setPlainText("")

    def reset_all_fields(self):
        self.reset_main_fields()
        self.sources_edit.setPlainText("")

    def fit_image_canvas(self):
        command = "svgCanvas.zoomChanged('', 'canvas');"
        self.svg_edit.eval(command)

class ImgOccOpts(QDialog):
    # Main IO Options dialog
    def __init__(self, mw):
        QDialog.__init__(self, parent=mw)
        self.setupUi()

    def getNewMaskColor(self):
        # Remove the # sign from QColor.name():
        choose_color_dialog = QColorDialog()
        color = choose_color_dialog.getColor()
        if color.isValid():
            color_ = color.name()[1:]
            mw.col.conf['imgocc']['qfill'] = color_
            # notify db of modification
            mw.col.setMod()
            self.changeButtonColor(self.mask_color_button, color_)

    def getNewOfillColor(self):
        # Remove the # sign from QColor.name():
        choose_color_dialog = QColorDialog()
        color = choose_color_dialog.getColor()
        if color.isValid():
            color_ = color.name()[1:]
            mw.col.conf['imgocc']['ofill'] = color_
            # notify db of modification
            mw.col.setMod()
            self.changeButtonColor(self.ofill_button, color_)

    def changeButtonColor(self, button, color):
        pixmap = QPixmap(128,18)
        qcolour = QtGui.QColor(0, 0, 0)
        qcolour.setNamedColor("#" + color)
        pixmap.fill(qcolour)
        button.setIcon(QIcon(pixmap))
        button.setIconSize(QSize(128, 18))

    def setupUi(self):
        # load preferences
        load_prefs(self)

        ### shape color for questions:
        qfill_label = QLabel('<b>Question</b> shape color')
        self.mask_color_button = QPushButton()
        self.mask_color_button.connect(self.mask_color_button,
                                  SIGNAL("clicked()"),
                                  self.getNewMaskColor)
        ### initial shape color:
        ofill_label = QLabel('<b>Initial</b> shape color')
        self.ofill_button = QPushButton()
        self.ofill_button.connect(self.ofill_button,
                                SIGNAL("clicked()"),
                                self.getNewOfillColor)

        ### set colors
        ofill = mw.col.conf['imgocc']['ofill']
        qfill = mw.col.conf['imgocc']['qfill']
        self.changeButtonColor(self.ofill_button, ofill)
        self.changeButtonColor(self.mask_color_button, qfill)

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        # 1st row:
        grid.addWidget(qfill_label, 0, 0)
        grid.addWidget(self.mask_color_button, 0, 1)
        # 2nd row:
        grid.addWidget(ofill_label, 1, 0)
        grid.addWidget(self.ofill_button, 1, 1)

        self.setLayout(grid)
        self.setMinimumWidth(400)
        self.setWindowTitle('Image Occlusion Enhanced Options')