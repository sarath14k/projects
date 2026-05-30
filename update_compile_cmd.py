import os

base_dir = "/home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete"

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".cpp"):
            filepath = os.path.join(root, file)
            basename = file
            no_ext = os.path.splitext(basename)[0]
            
            # The new command with cd prepended
            compile_cmd = f"// To compile and run: cd {root} && g++ -std=c++17 {basename} -o {no_ext} && ./{no_ext}\n"
            
            with open(filepath, "r") as f:
                lines = f.readlines()
                
            # Check if the first line is our previous comment
            if lines and lines[0].startswith("// To compile and run:"):
                lines[0] = compile_cmd
                with open(filepath, "w") as f:
                    f.writelines(lines)
                print(f"Updated compile command in {basename}")
