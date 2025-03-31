from PySide6.QtWidgets import QWizard, QMessageBox, QWizardPage, QLabel, QVBoxLayout, QCheckBox, QApplication


class Wizard(QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addPage(IntroPage())
        self.addPage(ConclusionPage())
        self.setWindowTitle("Wizard")

    def accept(self):
        QMessageBox.information(None, "Wizard", "Wizard is accepted")
        super(Wizard, self).accept()


class IntroPage(QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Introduction")
        label = QLabel("Hello!")
        layout = QVBoxLayout(self)
        layout.addWidget(label)


class ConclusionPage(QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Conclusion")
        launch_check_box = QCheckBox("Launch")
        layout = QVBoxLayout(self)
        layout.addWidget(launch_check_box)


if __name__ == '__main__':
    app = QApplication([])
    wizard = Wizard()
    wizard.show()
    app.exec()
