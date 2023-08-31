import subprocess
import os
import random
import string

RETURN_CODE_TIMEOUT = 124

def test_submission_script(inputs, correct_outputs, code, number_of_testcases, time_limit):
    try:
        base_path = "/home/daruis/test-environment/"
        characters = string.ascii_letters + string.digits
        random_name = ''.join(random.choices(characters, k=5))
        file_path = f"{base_path}/{random_name}.cpp"
        with open(file_path, 'wb') as cpp_file:
            cpp_file.write(code.encode('utf-8'))
        compile_program = f"g++ {file_path} -o {base_path}/{random_name}.exe"
        subprocess.run(compile_program, shell=True, check=True)
        results = []
        right_answers = 0
        time_limit_exceeded = False
        for act_test in range(number_of_testcases):
            with open(file_path, 'w') as input_file:
                input_file.write(inputs[act_test])
            try:
                execute_program = f"timeout {time_limit} {base_path}/{random_name}.exe < {file_path} > {base_path}/{random_name}.out"
                subprocess.run(execute_program, shell=True, check=True)
                with open(f"{base_path}/{random_name}.out", 'r') as output_file:
                    program_output = output_file.read().strip()
                    results.append(program_output)
                if program_output == correct_outputs[act_test]:
                    right_answers += 1
                    results.append(f"{act_test + 1}.Correct Solution!")
                else:
                    results.append(f"{act_test + 1}.Wrong Answer")
            except subprocess.CalledProcessError as e:
                if e.returncode == RETURN_CODE_TIMEOUT:
                    time_limit_exceeded = True
                    results.append(f"{act_test + 1}.Time Limit Exceeded")
                else:
                    results.append("Failed Compilation")
        # remove_generated_files(base_path, random_name)
        if right_answers == number_of_testcases:
            results.append("Correct Solution!")
        elif time_limit_exceeded:
            results.append("Time Limit Exceeded!")
        else:
            results.append("Wrong Answers!")
        return results
    except subprocess.CalledProcessError as e:
        os.remove(f"{base_path}/{random_name}.cpp")
        return ["Failed Compilation!"]

def remove_generated_files(base_path, random_name):
    try:
        os.remove(f"{base_path}/{random_name}.cpp")
        os.remove(f"{base_path}/{random_name}.exe")
        os.remove(f"{base_path}/{random_name}.out")
    except:
        pass
