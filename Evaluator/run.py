import subprocess

def test_solution():
    try:
        move_file_from_downloads = "mv /home/daruis/Downloads/solution.cpp /home/daruis/PersProject/AlgosCP/Evaluator"
        subprocess.run(move_file_from_downloads, shell=True, check=True)
        base_path = "/home/daruis/PersProject/AlgosCP/Evaluator"
        compile_program = f"g++ {base_path}/solution.cpp -o {base_path}/solution"
        subprocess.run(compile_program, shell=True, check=True)
        execute_program = f"{base_path}/solution > {base_path}/solution.out"
        subprocess.run(execute_program, shell=True, check=True)
        compare_results = f"diff {base_path}/correct_solution.txt {base_path}/solution.out > {base_path}/errors.txt"
        try:
            subprocess.run(compare_results, shell=True, check=True)
        except:
            print("WRONG ANSWER")
        cleanup_files = f"rm {base_path}/solution {base_path}/solution.cpp {base_path}/solution.out"
        subprocess.run(cleanup_files, shell=True, check=True)
    except:
        print("Failed Compilation")

if __name__ == '__main__': 
    test_solution()
