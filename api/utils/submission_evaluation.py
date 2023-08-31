import subprocess
import os
import tempfile
import secrets
import shutil
import stat

RETURN_CODE_TIMEOUT = 124

def test_submission_script(inputs, code, number_of_testcases, time_limit):
    base_path = create_temporary_directory()
    random_name = secrets.token_hex(16)
    file_path = f"{base_path}/{random_name}.cpp"
    with open(file_path, 'wb') as cpp_file:
        cpp_file.write(code.encode('utf-8'))
    try:
        results = []
        compile_program = f"g++ {file_path} -o {base_path}/{random_name}.exe"
        subprocess.run(compile_program, shell=True, check=True)
        for act_test in range(number_of_testcases):
            with open(file_path, 'w') as input_file:
                input_file.write(inputs[act_test])
            try:
                execute_program = f"timeout {time_limit} {base_path}/{random_name}.exe < {file_path} > {base_path}/{random_name}.out"
                subprocess.run(execute_program, shell=True, check=True)
                with open(f"{base_path}/{random_name}.out", 'r') as output_file:
                    program_output = output_file.read().strip()
                    results.append(program_output)
            except subprocess.CalledProcessError as e:
                if e.returncode == RETURN_CODE_TIMEOUT:
                    results.append(f"{act_test + 1}.Time Limit Exceeded")
                else:
                    results.append("Internal Server Error!")
    except subprocess.CalledProcessError as e:
        results = ['Failed Compilation!']
    remove_directory(base_path)
    return results

def create_temporary_directory():
    try:
        random_hex_name = secrets.token_hex(16)
        temp_directory_path = os.path.join(tempfile.gettempdir(), random_hex_name)
        os.makedirs(temp_directory_path)
        os.chmod(temp_directory_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        return temp_directory_path
    except:
        return None

def remove_directory(path):
    try:
        shutil.rmtree(path)
    except:
        pass
