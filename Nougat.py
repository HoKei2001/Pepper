import subprocess

# 脚本路径变量
default_path = "C:\\Users\Administrator\Desktop\Future.pdf"

# script_path = "files\\IECONfinal.pdf"

def pre_read(script_path):
    # 定义虚拟环境名称
    virtualenv_name = "pytorch"

    # 定义要运行的命令
    command_to_execute = f"nougat {script_path} -o files"  # 替换为你的实际命令

    # 构建激活虚拟环境的命令
    activate_command = f"conda activate {virtualenv_name}"

    # 使用 subprocess 执行激活命令
    subprocess.Popen(activate_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()

    # 构建完整的命令，包括在虚拟环境中运行
    full_command = f"conda run -n {virtualenv_name} {command_to_execute}"

    # 打开命令行并执行完整的命令
    execute_command = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 逐行读取并实时显示输出
    for line in execute_command.stdout:
        print(line, end='')

    # 等待命令执行完成
    execute_command.wait()

    # 输出返回的命令退出码
    print("Command Exit Code:", execute_command.returncode)

    # 退出虚拟环境
    deactivate_command = "conda deactivate"
    subprocess.Popen(deactivate_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()


if __name__ == "__main__":
    pre_read(default_path)