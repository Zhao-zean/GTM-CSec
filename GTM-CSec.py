import numpy as np
import pandas as pd
import time
import schedule
import matplotlib.pyplot as plt
import random
import sys
import os
import shutil
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

global count, x_axis, defender, attacker, seconds, generated_values, selected_case, image_files


mue = list(np.arange(0.5, 1.00, 0.01))  # values from 0.5 to 0.99
alpha = mue.copy()
gamma = mue.copy()

Bds = [-5, 0, 5]
Gat = Bds.copy()

Eds = list(np.arange(0, 1.00, 0.01))
Hhp = Eds.copy()
Rat = Hhp.copy()
Vass = list(range(1, 5, 1))  # [1, 2, 3, 4]

# 初始化数据框
df = pd.DataFrame(columns=[
    'signature',  # u
    'anomaly',  # a
    'honeypot',  # y
    'gain_detection',  # B
    'gain_attack',  # G
    'ids_energy',  # E
    'ids_honeypot',  # H
    'resource',  # R
    'asset_value'  # V
])

# 初始化 generated_values 字典
generated_values = {
    'a': 0,
    'u': 0,
    'y': 0,
    'B': 0,
    'G': 0,
    'R': 0,
    'V': 0,
    'E': 0,
    'H': 0
}

# 初始化 image_files 列表以跟踪已保存的图像
image_files = []


def check_constraint(time, a, u, y, B, G, R, V, E, H):
    global generated_values
    # 示例约束
    if generated_values['E'] < E or generated_values['H'] < H or generated_values['R'] < R:
        return True
    else:
        return False


def get_user_input():
    global seconds, selected_case
    # 提示用户输入编号
    while True:
        try:
            selected_case = int(input("请输入案例编号（2 到 7）："))
            if selected_case < 2 or selected_case > 7:
                print("请输入 2 到 7 之间的有效案例编号。")
                continue
            break
        except ValueError:
            print("输入无效。请输入 2 到 7 之间的整数。")

    # 提示用户输入运行时间（以秒为单位）
    while True:
        try:
            seconds = int(input("请输入运行时间（秒）："))
            if seconds <= 0:
                print("请输入一个正整数作为运行时间。")
                continue
            break
        except ValueError:
            print("输入无效。请输入一个正整数作为运行时间。")


def generate():
    global count, defender, attacker, x_axis, generated_values, selected_case, stop_simulation, image_files

    # 检查是否超出模拟时间
    if count > seconds:
        print("模拟完成。")
        stop_simulation = True  # 设置标志以停止调度
        return

    a, u, y, B, G, R, V, E, H = get_random_value()

    # 根据选择的案例编号计算收益
    if selected_case == 2:
        Ud = case_2_get_pay_off_defender(a, u, y, B, G, R, V, E, H)
        Ua = case_2_get_pay_off_attacker(a, u, y, B, G, R, V, E, H)
    elif selected_case == 3:
        Ud = case_3_get_pay_off_defender(a, u, y, B, G, R, V, E, H)
        Ua = case_3_get_pay_off_attacker(a, u, y, B, G, R, V, E, H)
    elif selected_case == 4:
        Ud = case_4_get_pay_off_defender(a, u, y, B, G, R, V, E, H)
        Ua = case_4_get_pay_off_attacker(a, u, y, B, G, R, V, E, H)
    elif selected_case == 5:
        Ud = case_5_get_pay_off_defender(a, u, y, B, G, R, V, E, H)
        Ua = case_5_get_pay_off_attacker(a, u, y, B, G, R, V, E, H)
    elif selected_case == 6:
        Ud = case_6_get_pay_off_defender(a, u, y, B, G, R, V, E, H)
        Ua = case_6_get_pay_off_attacker(a, u, y, B, G, R, V, E, H)
    elif selected_case == 7:
        Ud = case_7_get_pay_off_defender(a, u, y, B, G, R, V, E, H)
        Ua = case_7_get_pay_off_attacker(a, u, y, B, G, R, V, E, H)
    else:
        print(f"不支持的案例编号: {selected_case}")
        Ud, Ua = 0, 0

    # 检查约束条件
    if check_constraint(count, a, u, y, B, G, R, V, E, H):
        # 更新 x 轴数据
        x_axis.append(count)

        # 更新防御者和攻击者收益
        defender.append(Ud)
        attacker.append(Ua)

        # 更新绘图
        plt.figure(figsize=(8, 6))
        plt.xlabel('时间（秒）')
        plt.ylabel('收益')
        plt.title(f'案例 {selected_case} 的收益随时间变化')
        plt.plot(x_axis, defender, label='Defender')
        plt.plot(x_axis, attacker, label='Attacker')
        plt.legend()

        # 创建 'outputs' 目录
        output_dir = 'outputs'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 保存图像
        image_filename = f'output_{count}.png'
        image_path = os.path.join(output_dir, image_filename)
        plt.savefig(image_path)
        image_files.append(image_path)

        plt.close()  # 使用 plt.close() 而不是 plt.clf() 关闭绘图

    count += 1


def create_plot():
    global count, image_files
    plt.xlabel('时间（秒）')
    plt.ylabel('收益')
    plt.title(f'案例 {selected_case} 的收益随时间变化')
    plt.plot(x_axis, defender, label='防守者')
    plt.plot(x_axis, attacker, label='攻击者')
    plt.legend()
    plt.pause(1e-3)


    output_dir = 'outputs'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    image_filename = f'output_{count}.png'
    image_path = os.path.join(output_dir, image_filename)
    plt.savefig(image_path)
    image_files.append(image_path)  # Keep track of the saved images

    plt.clf()



def case_2_get_pay_off_defender(a, u, y, B, G, R, V, E, H):
    p = u / (u + a - y)
    q = (u - y - 2 * a) / (u - y - a) - (V) / ((u - y - a) * (B + V)) - (H) / ((u - y - a) * (B + V))
    return (p * q * u * B) + (p * q * u * V) + (p * V) + (q * y * B) + (q * y * V) - (p * q * y * B) - (
            p * q * y * V) - (p * a * B) - (p * a * V) + (p * H) - (q * a * B) - (q * a * V) + (p * q * a * B) + (
            p * q * a * V)


def case_2_get_pay_off_attacker(a, u, y, B, G, R, V, E, H):
    p = u / (u + a - y)
    q = (u - y - 2 * a) / (u - y - a) - (V) / ((u - y - a) * (B + V)) - (H) / ((u - y - a) * (B + V))
    return (4 * G) - (p * u * G) + (p * a * G) - (2 * p * G) - (q * y * G) + (q * a * G) - (p * q * u * G) + (
            p * q * y * G) - (p * q * a * G) - (a * G) - (2 * R)


def case_3_get_pay_off_defender(a, u, y, B, G, R, V, E, H):
    p = a / (a + u + y)
    q = (u + y) / (u + a + y) + V / ((u + a + y) * (B + V)) + H / ((u + y + a) * (B + V))
    return (p * a * B) - (p * V) + (p * a * V) - (p * q * a * B) - (p * q * a * V) + (p * u * B) - (2 * q * V) - (
            q * y * B) + (q * y * V) - (q * H) - (p * q * u * B) - (p * q * u * V) - (p * q * y * B) - (
            p * q * y * V) + (p * H) + (q * E) + (2 * q * V) + (q * H)


def case_3_get_pay_off_attacker(a, u, y, B, G, R, V, E, H):
    p = a / (a + u + y)
    q = (u + y) / (u + a + y) + V / ((u + a + y) * (B + V)) + H / ((u + y + a) * (B + V))
    return (p * G) - (p * a * G) - (p * R) + (p * q * a * G) - (u * q * G) - (q * a * G) + (p * q * u * G) + (
            p * q * y * G) + (2 * G) - (2 * R) - (2 * p * G) + (2 * p * R)


def case_4_get_pay_off_defender(a, u, y, B, G, R, V, E, H):
    p = y / (y + a - u)
    q = (y - u - 2 * a) / (y - u - a) + V / ((y - u - a) * (B + V)) + H / ((y - u - a) * (B + V)) - (2 * E) / (
            (y - u - a) * (B + V))
    return (p * q * y * B) + (p * q * y * V) - (p * H) - (p * V) - (p * q * u * B) - (p * q * u * V) - (p * a * B) + (
            2 * p * V) - (p * a * V) + (2 * p * E) + (p * q * a * B) + (p * q * a * V)


def case_4_get_pay_off_attacker(a, u, y, B, G, R, V, E, H):
    p = y / (y + a - u)
    q = (y - u - 2 * a) / (y - u - a) + V / ((y - u - a) * (B + V)) + H / ((y - u - a) * (B + V)) - (2 * E) / (
            (y - u - a) * (B + V))
    return ((-p * q * y * G) + (p * G) - (p * R) - (y * u * G) + (p * q * u * G) + (2 * G) - (2 * R) - (a * G) - (
            2 * p * G) + (2 * p * R) + (p * a * G) + (y * a * G) - (p * q * a * G))


def case_5_get_pay_off_defender(a, u, y, B, G, R, V, E, H):
    p = a / (u + a)
    q = p
    return ((p * q * u * B) + (p * q * a * B) + (p * q * u * V) + (p * q * a * V) - (p * a * B) - (p * a * V) - (
            q * a * B) - (q * a * V))


def case_5_get_pay_off_attacker(a, u, y, B, G, R, V, E, H):
    p = a / (u + a)
    q = p
    return ((-p * q * u * G) + 1 - (a * G) - R + (p * a * G) + (q * a * G) - (p * q * a * G))


def case_6_get_pay_off_defender(a, u, y, B, G, R, V, E, H):
    p = y / (y - u)
    q = (E - H) / (u - y)
    return (p * q * u * B) + (p * q * u * V) + (q * y * B) + (q * y * V) - (p * q * y * B) - (p * q * y * V) - (H) - (
        V) + (p * H) - (p * E)


def case_6_get_pay_off_attacker(a, u, y, B, G, R, V, E, H):
    p = y / (y - u)
    q = (E - H) / (u - y)
    return (-p * q * u * G) - (q * y * G) - (p * q * G) + (p * q * a * G) + (p * q * R) + (G) - (R) + (p * q * G) - (
            p * q * R)


def case_7_get_pay_off_defender(a, u, y, B, G, R, V, E, H):
    p = y / (y + a)
    q = a / (a + y)
    return (q * y * B) + (q * y * V) - (p * q * y * B) - (p * q * a * V) + (p * a * B) + (p * a * V) - (
            p * q * a * B) - (p * q * a * V) - (H) - (V)


def case_7_get_pay_off_attacker(a, u, y, B, G, R, V, E, H):
    p = y / (y + a)
    q = a / (a + y)
    return (p * a * G) + (p * q * a * G) - (p * y * G) + (p * q * y * G) + (G) - (R)


def get_random_value():
    a = random.choice(alpha)
    y = random.choice(gamma)
    u = random.choice(mue)
    B = random.choice(Bds)
    G = random.choice(Gat)
    R = random.choice(Rat)
    V = random.choice(Vass)
    H = random.choice(Hhp)
    E = random.choice(Eds)
    return a, u, y, B, G, R, V, E, H


def stop_program():
    print("Stopping the simulation...")
    sys.exit()


def main():
    global count, x_axis, defender, attacker, stop_simulation, image_files

    # 获取用户输入
    get_user_input()

    # 初始化变量
    count = 1
    x_axis = []
    defender = []
    attacker = []
    stop_simulation = False

    # 生成图像
    schedule.every(1).second.do(generate)

    print(f"开始运行案例 {selected_case}，持续 {seconds} 秒...")

    # Run the scheduler
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
            if stop_simulation:
                break
    except KeyboardInterrupt:
        print("模拟被用户中断。")
    finally:
        # 确保至少生成了一张图片
        if len(image_files) >= 1:
            last_image = image_files[-1]
            results_dir = 'results'
            if not os.path.exists(results_dir):
                os.makedirs(results_dir)
            new_filename = f'case{selected_case}.png'
            new_filepath = os.path.join(results_dir, new_filename)
            shutil.copy(last_image, new_filepath)
            print(f"最后一张图片已保存为 {new_filepath}")
        else:
            print("未生成足够的图片，无法保存最后一张图片。")

        plt.show()


if __name__ == "__main__":
    main()