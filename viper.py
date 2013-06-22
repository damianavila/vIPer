#!/usr/bin/env python

#ver_1.0

import sys
import subprocess
import os
import signal
from PyQt4 import QtGui, QtCore, QtWebKit
from nbconvert_viper import NbConvertApp


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.tabs = QtGui.QTabWidget(self,
            tabsClosable=True,
            movable=True,
            elideMode=QtCore.Qt.ElideRight,
            currentChanged=self.currentTabChanged,
            tabCloseRequested=self.closeTabRequested)
        self.bottom = QtWebKit.QWebView(self)
        self.setWindowTitle("vIPer")
        self.splitter = QtGui.QSplitter(self)
        self.setCentralWidget(self.splitter)
        self.splitter.addWidget(self.tabs)
        self.splitter.addWidget(self.bottom)
        self.bottom.setVisible(False)
        self.tabWidgets = []
        self.titleHistory = []
        self.path = QtCore.QDir.currentPath()
        self.newtab = QtGui.QAction(QtGui.QIcon.fromTheme("document-new"),
            "New Tab",
            self,
            triggered=self.newTabTriggered,
            shortcut="Ctrl+t")
        self.htmler = QtGui.QAction(QtGui.QIcon.fromTheme("go-down"),
            "Htmler",
            self,
            triggered=self.screenHtmled,
            shortcut="Ctrl+j")
        self.slider = QtGui.QAction(QtGui.QIcon.fromTheme("go-jump"),
            "Slider",
            self,
            triggered=self.screenSlided,
            shortcut="Ctrl+k")
        self.splitterV = QtGui.QAction(QtGui.QIcon.fromTheme(
                "object-flip-vertical"),
            "Split vertically",
            self,
            triggered=self.screenSplittedVhtml,
            shortcut="F9")
        self.splitterV.setMenu(QtGui.QMenu())
        self.splitterV.menu().addAction(QtGui.QAction('HTML',
            self,
            triggered=self.screenSplittedVhtml))
        self.splitterV.menu().addAction(QtGui.QAction('SLIDE',
            self,
            triggered=self.screenSplittedVslide))
        self.splitterH = QtGui.QAction(QtGui.QIcon.fromTheme(
                "object-flip-horizontal"),
            "Split horizontally",
            self,
            triggered=self.screenSplittedHhtml,
            shortcut="F10")
        self.splitterH.setMenu(QtGui.QMenu())
        self.splitterH.menu().addAction(QtGui.QAction('HTML',
            self,
            triggered=self.screenSplittedHhtml))
        self.splitterH.menu().addAction(QtGui.QAction('SLIDE',
            self,
            triggered=self.screenSplittedHslide))
        self.recorder = QtGui.QAction(QtGui.QIcon.fromTheme(
                "media-playback-start"),
            "Record",
            self,
            triggered=self.screenRecorded,
            shortcut="Ctrl+r")
        self.stopper = QtGui.QAction(QtGui.QIcon.fromTheme(
                "media-playback-stop"),
            "Stop",
            self,
            triggered=self.screenStopped,
            shortcut="Ctrl+Alt+s")
        self.addAction(QtGui.QAction("Split Screen",
            self,
            checkable=True,
            toggled=self.splitToggled,
            shortcut="F11"))
        self.addAction(QtGui.QAction("Full Screen",
            self,
            checkable=True,
            toggled=self.screenToggled,
            shortcut="F12"))
        self.helper = QtGui.QAction(QtGui.QIcon.fromTheme("help-faq"),
            "Help",
            self,
            triggered=self.newHelpTabTriggered,
            shortcut="Ctrl+h")
        self.full = "full_html"
        self.html = '.html'
        self.rev = "reveal"
        self.rev_html = '.reveal.html'
        self.horizontal = QtCore.Qt.Horizontal
        self.vertical = QtCore.Qt.Vertical
        self.addTab(QtCore.QUrl('http://127.0.0.1:8888/'))

    def addTab(self, url=QtCore.QUrl("")):
        self.tabs.setCurrentIndex(self.tabs.addTab(Tab(url, self), ""))
        return self.tabs.currentWidget()

    def newTabTriggered(self):
        self.addTab(QtCore.QUrl('http://ipython.org/'))
        l = 'If you want to surf the web, get an address bar pressing Ctrl + A'
        self.statusBar().showMessage(l, 5000)

    def newHelpTabTriggered(self):
        localH = 'Help_page' + '.html'
        self.addTab(QtCore.QUrl.fromLocalFile(self.path + '/' + localH))

    def currentTabChanged(self, idx):
        wb = self.tabs.widget(idx)
        self.addToTitleHistory(unicode(wb.title()))
        if wb is None:
            return self.close()
        for w in self.tabWidgets:
            w.hide()
        self.tabWidgets = [wb.tb, wb.pbar, wb.lineUrl, wb.search]
        self.addToolBar(wb.tb)
        for w in self.tabWidgets[:-3]:
            w.show()

    def addToTitleHistory(self, title):
        self.titleHistory.append(title)

    def closeTabRequested(self, idx):
        self.tabs.widget(idx).deleteLater()

    def nbConverter(self, exporter):
        self.nbconverted = NbConvertApp.instance()
        self.nbconverted.start(["nbconvert.py",
                                    "--NbConvertApp.write=True",
                                    exporter,
                                    self.titleHistory[-1] + '.ipynb'])

    def screenHtmled(self):
        self.screenOS = ScreenMainer(self.full, self.html, self)

    def screenSlided(self):
        self.screenOS = ScreenMainer(self.rev, self.rev_html, self)

    def screenSplittedVhtml(self):
        self.screenV = ScreenSplitter(self.vertical, 1.0,
            self.full, self.html, self)

    def screenSplittedHhtml(self):
        self.screenH = ScreenSplitter(self.horizontal, 1.0,
            self.full, self.html, self)

    def screenSplittedVslide(self):
        self.screenV = ScreenSplitter(self.vertical, 1.0,
            self.rev, self.rev_html, self)

    def screenSplittedHslide(self):
        self.screenH = ScreenSplitter(self.horizontal, 1.0,
            self.rev, self.rev_html, self)

    def screenRecorded(self):
        l = 'Recording audio and video...'
        self.statusBar().showMessage(l, 5000)
        self.cmd = 'recordmydesktop -o ' + self.titleHistory[-1] + '.ogv'
        self.recordMachinary = subprocess.Popen(self.cmd,
                            stdout=subprocess.PIPE,
#                            stderr=subprocess.PIPE,
                            shell=True,
                            preexec_fn=os.setsid)
#        html, stderr = proc.communicate()
#        if stderr:
#            raise IOError(stderr)

    def screenStopped(self):
        l = 'Stopping audio and video recording...'
        self.statusBar().showMessage(l, 3000)
        os.killpg(self.recordMachinary.pid, signal.SIGTERM)

    def splitToggled(self, v):
        self.bottom.setVisible(False) if v else self.bottom.setVisible(True)

    def screenToggled(self, v):
        self.showFullScreen() if v else self.showNormal()


class Converter:
    def __init__(self, exporter, container):
        self.container = container
        self.exporter = exporter

        self.container.nbConverter(self.exporter)


class ScreenMainer:
    def __init__(self, exporter, extension, container):
        self.container = container
        self.extension = extension
        self.exporter = exporter

        localO = self.container.titleHistory[-1] + self.extension
#        try:
        l = 'Building a view from the IPython notebook, please wait...'
        self.container.statusBar().showMessage(l, 3000)
        self.container.screenOS = Converter(self.exporter, self.container)
        self.container.addTab(QtCore.QUrl.fromLocalFile(
            self.container.path + '/' + localO))
        #except IOError:
            #l = 'This tab is not an IPython notebook'
            #self.statusBar().showMessage(l, 3000)


class ScreenSplitter:
    def __init__(self, orientation, zoom, exporter, extension, container):
        self.container = container
        self.extension = extension
        self.exporter = exporter
        self.zoom = zoom
        self.orientation = orientation

        localO = self.container.titleHistory[-1] + self.extension
        self.container.splitter.setOrientation(self.orientation)
        #try:
        l = 'Building the splitted view, please wait...'
        self.container.statusBar().showMessage(l, 3000)
        self.container.screenHtmler = Converter(exporter, self.container)
        self.container.bottom.load(QtCore.QUrl.fromLocalFile(
            self.container.path + '/' + localO))
        self.container.bottom.setVisible(True)
        self.container.bottom.setZoomFactor(self.zoom)
        #except IOError:
            #l = 'This tab is not an IPython notebook'
            #self.container.statusBar().showMessage(l, 3000)


class Tab(QtWebKit.QWebView):
    def __init__(self, url, container):
        self.container = container
        self.pbar = QtGui.QProgressBar(maximumWidth=120, visible=False)
        self.tab = QtWebKit.QWebView.__init__(self,
            loadProgress=lambda v: (self.pbar.show(), self.pbar.setValue(v)),
            loadFinished=self.pbar.hide,
            loadStarted=lambda: self.pbar.show(),
            titleChanged=self.titleTabChanged)

        self.tb = QtGui.QToolBar("Main Toolbar")
        for a, sc in [[QtWebKit.QWebPage.Back, "Alt+Left"],
                      [QtWebKit.QWebPage.Forward, "Alt+Right"],
                      [QtWebKit.QWebPage.Reload, "Ctrl+r"]
                      ]:
            self.tb.addAction(self.pageAction(a))
            self.pageAction(a).setShortcut(sc)
        self.tb.addAction(container.newtab)
        self.tb.addAction(container.htmler)
        self.tb.addAction(container.slider)
        self.tb.addAction(container.splitterV)
        self.tb.addAction(container.splitterH)
        self.tb.addAction(container.recorder)
        self.tb.addAction(container.stopper)
        self.tb.addAction(container.helper)

        self.titleChanged.connect(lambda t:
            container.addToTitleHistory(unicode(t)))

        self.lineUrl = QtGui.QLineEdit(visible=False,
            returnPressed=lambda:
            self.setUrl(QtCore.QUrl.fromUserInput(self.lineUrl.text())))
        self.showAddress = QtGui.QShortcut("Ctrl+a",
            self,
            activated=lambda:
                self.lineUrl.show() or self.lineUrl.setFocus())
        self.hideAddress = QtGui.QShortcut("Ctrl+d",
            self,
            activated=lambda:
                (self.lineUrl.hide(), self.setFocus()))

        self.search = QtGui.QLineEdit(visible=False,
            returnPressed=lambda:
                self.findText(self.search.text()))
        self.addAction(QtGui.QAction("Search",
            self,
            checkable=True,
            toggled=self.searchToggled,
            shortcut="Ctrl+f"))

        self.do_close = QtGui.QShortcut("Ctrl+w",
            self,
            activated=lambda:
                container.tabs.removeTab(container.tabs.indexOf(self)))
        self.do_quit = QtGui.QShortcut("Ctrl+q",
            self,
            activated=lambda: container.close())

        self.zoomIn = QtGui.QShortcut("Ctrl++",
            self,
            activated=lambda:
                self.setZoomFactor(self.zoomFactor() + 0.2))
        self.zoomOut = QtGui.QShortcut("Ctrl+-",
            self,
            activated=lambda:
                self.setZoomFactor(self.zoomFactor() - 0.2))
        self.zoomOne = QtGui.QShortcut("Ctrl+0",
            self,
            activated=lambda:
                self.setZoomFactor(1))

        self.urlFocus = QtGui.QShortcut("Ctrl+l",
            self,
            activated=self.lineUrl.setFocus)

        self.printLater()

        container.statusBar().addPermanentWidget(self.pbar)
        container.statusBar().addPermanentWidget(self.lineUrl)
        container.statusBar().addPermanentWidget(self.search)

        self.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled,
            True)
        self.load(url)

    def titleTabChanged(self, t):
        if self.amCurrent():
            self.container.tabs.setTabText(
                self.container.tabs.indexOf(self), t)

    def lineUrlToggled(self, v):
        if v is True:
            self.lineUrl.show() or self.lineUrl.setFocus()
        else:
            (self.lineUrl.hide(), self.setFocus())

    def searchToggled(self, v):
        if v is True:
            self.search.show() or self.search.setFocus()
        else:
            (self.search.hide(), self.setFocus())

    def printLater(self):
        self.previewer = QtGui.QPrintPreviewDialog(paintRequested=self.print_)
        self.do_print = self.tb.addAction(QtGui.QAction(
            QtGui.QIcon.fromTheme("document-print"),
            "Print",
            self,
            triggered=self.previewer.exec_,
            shortcut="Ctrl+p"))

    amCurrent = lambda self: self.container.tabs.currentWidget() == self

    def createWindow(self, windowType):
        return self.container.addTab()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    wb = MainWindow()
    wb.showMaximized()
    sys.exit(app.exec_())
