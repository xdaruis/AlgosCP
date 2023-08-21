import subprocess
import re

def test_solution():
    problem_id = '1'
    base_path = "/home/daruis/PersProject/AlgosCP/Evaluator"
    try:
        move_file_from_downloads = f"mv /home/daruis/Downloads/{problem_id}.cpp /home/daruis/PersProject/AlgosCP/Evaluator"
        subprocess.run(move_file_from_downloads, shell=True, check=True)
        add_testcases_loop(problem_id)
    except:
        print("Files Missing! Internal server error")
        return
    try:
        compile_program = f"g++ {base_path}/{problem_id}.cpp -o {base_path}/{problem_id}"
        subprocess.run(compile_program, shell=True, check=True)
        execute_program = f"timeout 5 {base_path}/{problem_id} > {base_path}/{problem_id}.out"
        subprocess.run(execute_program, shell=True, check=True)
        compare_results = f"diff {base_path}/DesiredOutputs/{problem_id}.out {base_path}/{problem_id}.out > {base_path}/errors.txt"
        try:
            subprocess.run(compare_results, shell=True, check=True)
        except:
            print("WRONG ANSWER!")
    except subprocess.CalledProcessError as e:
        if e.returncode == 124:
            print("Time limit exceeded!")
        else:
            print("Failed Compilation!")
    # cleanup_files = f"rm {base_path}/{problem_id} {base_path}/{problem_id}.cpp {base_path}/{problem_id}.out"
    # subprocess.run(cleanup_files, shell=True, check=True)

def add_testcases_loop(problem_id):
    cpp_filename = f"{problem_id}.cpp"
    start_testing = f'freopen("Inputs/{problem_id}.in", "r", stdin); int __tests; cin >> __tests; while(__tests--) {{'
    end_testing = ' cout << " "; }'
    with open(cpp_filename, 'r') as cpp_file:
        cpp_content = cpp_file.read()
    modified_content = re.sub(r'(int\s+main\s*\(\s*\)\s*{)', rf'\1\n    {start_testing}\n', cpp_content, count=1)
    modified_content = re.sub(r'(\s*return\s+0\s*;)', rf'    {end_testing}\n\1', modified_content)
    with open(cpp_filename, 'w') as cpp_file:
        cpp_file.write(modified_content)

if __name__ == '__main__':
    test_solution()
