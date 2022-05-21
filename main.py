import logging

from PyQt5.QtWidgets import QApplication


from views import UI_Window

logging.basicConfig(handlers=(logging.FileHandler('logs/log.txt'), logging.StreamHandler()),
                    format=u'%(asctime)s %(filename)s [LINE:%(lineno)d] #%(levelname)-15s %(message)s',
                    level=logging.INFO,
                    )

if __name__ == '__main__':
    logging.log(logging.INFO, "Приложение запущено")
    app = QApplication([])

    start_window = UI_Window()
    start_window.show()

    app.exit(app.exec_())


