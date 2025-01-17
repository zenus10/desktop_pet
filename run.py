# run.py

import sys
from PyQt5.QtWidgets import QApplication
from core.app import PetApp

def main():
    app = QApplication(sys.argv)

    pet_app = PetApp()
    pet_app.initialize_pets(num=2)  # 比如默认生成2只宠物

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
