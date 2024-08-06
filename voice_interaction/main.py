from main_agents.main_agents import open_agents
from main_function import audio


def main():
    open_agents()
    while True:
        audio()
        open_agents()


if __name__ == '__main__':
    main()
