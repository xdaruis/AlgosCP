import subprocess
import os

RETURN_CODE_TIMEOUT = 124

def test_submission_script(inputs, correct_outputs, problem_id, code, base_path, number_of_testcases, time_limit):
    try:
        cpp_path = f"{base_path}/{problem_id}.cpp"
        with open(cpp_path, 'wb') as cpp_file:
            cpp_file.write(code.encode('utf-8'))
        compile_program = f"g++ {cpp_path} -o {base_path}/{problem_id}.exe"
        subprocess.run(compile_program, shell=True, check=True)
        results = []
        right_answers = 0
        time_limit_exceeded = False
        for act_test in (1, number_of_testcases + 1):
            tests_path = f"{base_path}/{problem_id}/{act_test}"
            with open(cpp_path, 'wb') as cpp_file:
                cpp_file.write(inputs[act_test - 1])
            try:
                execute_program = f"timeout {time_limit} {base_path}/{problem_id}.exe < {cpp_path} > {base_path}/{problem_id}.out"
                subprocess.run(execute_program, shell=True, check=True)
                with open(f"{base_path}/{problem_id}.out", 'r') as output_file:
                    program_output = output_file.read().strip()
                # with open(f"{tests_path}.out", 'r') as output_file:
                #     correct_output = output_file.read().strip()
                print(correct_outputs[act_test - 1])
                if program_output == correct_outputs[act_test - 1]:
                    right_answers += 1
                    results.append(f"{act_test}.Correct Solution!")
                else:
                    print(f"test#{act_test}")
                    print(f"correct: {correct_outputs[act_test - 1]}")
                    print(f"actOutput: {program_output}")
                    results.append(f"{act_test}.Wrong Answer")
            except subprocess.CalledProcessError as e:
                if e.returncode == RETURN_CODE_TIMEOUT:
                    time_limit_exceeded = True
                    results.append(f"{act_test}.Time Limit Exceeded")
                else:
                    results.append("Failed Compilation")
        remove_generated_files(base_path, problem_id)
        if right_answers == number_of_testcases:
            results.append("Correct Solution!")
        elif time_limit_exceeded:
            results.append("Time Limit Exceeded!")
        else:
            results.append("Wrong Answers!")
        return results
    except subprocess.CalledProcessError as e:
        os.remove(f"{base_path}/{problem_id}.cpp")
        return ["Failed Compilation!"]

def remove_generated_files(base_path, problem_id):
    try:
        os.remove(f"{base_path}/{problem_id}.cpp")
        os.remove(f"{base_path}/{problem_id}.exe")
        os.remove(f"{base_path}/{problem_id}.out")
    except:
        pass
