import os

base_dir = "/home/sarath/projects/cpp/CompetitiveProgramming/C++/LLD_Complete"

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".cpp"):
            filepath = os.path.join(root, file)
            basename = file
            no_ext = os.path.splitext(basename)[0]
            
            # Using -std=c++17 to ensure modern C++ features work without issues
            compile_cmd = f"// To compile and run: g++ -std=c++17 {basename} -o {no_ext} && ./{no_ext}\n"
            
            with open(filepath, "r") as f:
                content = f.read()
                
            if "To compile and run:" not in content:
                with open(filepath, "w") as f:
                    f.write(compile_cmd + content)
                print(f"Added compile command to {basename}")
