from datetime import datetime

from termcolor import colored


class Logger:
    @property
    def current_time(self):
        return datetime.strftime(datetime.now(), '%Y.%m.%d-%H:%M:%S')

    def debug(self, *message):
        print(repr(colored('{0} [DEBUG] {1}'.format(self.current_time, ' '.join(map(str, message))))))

    def info(self, *message):
        print(repr(colored('{0} [INFO ] {1}'.format(self.current_time, ' '.join(map(str, message))), 'cyan')))

    def warning(self, *message):
        print(repr(colored('{0} [WARN ] {1}'.format(self.current_time, ' '.join(map(str, message))), 'yellow')))

    def success(self, *message):
        print(repr(colored('{0} [OK  ] {1}'.format(self.current_time, ' '.join(map(str, message))), 'green')))

    def error(self, *message):
        print(repr(colored('{0} [ERROR] {1}'.format(self.current_time, ' '.join(map(str, message))), 'red')))


logger = Logger()

if __name__ == '__main__':
    logger.debug("debug", "second message")
    logger.info("info", "second message")
    logger.warning("warning", "second message")
    logger.success("success", "second message")
    logger.error("error", "second message")
