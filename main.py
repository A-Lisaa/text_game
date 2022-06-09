import sys

from src import globs


def run_cli():
    from src.ui.cli.cli import CLI
    globs.ui = CLI()
    globs.ui.start()

def run_pyqt():
    #pylint: disable=no-name-in-module
    from PyQt6.QtWidgets import QApplication

    from src.ui.pyqt.pyqt6 import PyQt6
    app = QApplication(sys.argv)
    globs.ui = PyQt6()
    globs.ui.start()
    app.exec()

uis = {
    "CLI": run_cli,
    "PyQt6": run_pyqt,
}

def main():
    ui_name = "PyQt6"
    uis[ui_name]()

if __name__ == "__main__":
    main()
