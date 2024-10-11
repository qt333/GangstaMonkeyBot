from contextlib import suppress

from bot.utils.launcher import start_threads


def main():
    start_threads()


if __name__ == '__main__':
    # with suppress(KeyboardInterrupt, RuntimeError, RuntimeWarning):
        main()