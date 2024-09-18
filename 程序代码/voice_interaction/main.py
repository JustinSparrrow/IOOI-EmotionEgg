from main_agents.main_agents import open_agents
from main_function import audio
import time


def main():
    open_agents()
    while True:
        audio()
        open_agents()


if __name__ == '__main__':
    start_time = time.time()  # 开始计时
    main()

    end_time = time.time()  # 结束计时
    execution_time = end_time - start_time  # 计算执行时间

    print(f"执行时间: {execution_time:.2f} 秒")
