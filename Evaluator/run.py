import subprocess

def test_solution():
    base_path = "/home/daruis/PersProject/AlgosCP/Evaluator"
    try:
        move_file_from_downloads = "mv /home/daruis/Downloads/solution.cpp /home/daruis/PersProject/AlgosCP/Evaluator"
        subprocess.run(move_file_from_downloads, shell=True, check=True)
    except:
        print("Files Missing! Internal server error")
        return
    try:
        compile_program = f"g++ {base_path}/solution.cpp -o {base_path}/solution"
        subprocess.run(compile_program, shell=True, check=True)
        # memory = 1024 * 256
        # memory_limit = f"ulimit -v {memory}"
        execute_program = f"timeout 5 {base_path}/solution > {base_path}/solution.out"
        subprocess.run(execute_program, shell=True, check=True)
        compare_results = f"diff {base_path}/correct_solution.txt {base_path}/solution.out > {base_path}/errors.txt"
        try:
            subprocess.run(compare_results, shell=True, check=True)
        except:
            print("WRONG ANSWER")
    except subprocess.CalledProcessError as e:
        if e.returncode == 124:
            print("Time limit exceeded!")
        else:
            print("Failed Compilation")
    cleanup_files = f"rm {base_path}/solution {base_path}/solution.cpp {base_path}/solution.out"
    subprocess.run(cleanup_files, shell=True, check=True)

if __name__ == '__main__': 
    test_solution()
