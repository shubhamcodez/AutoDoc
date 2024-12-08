import os

def scan_and_document_modules(modules_dir="Modules", documentation_dir="Documentation"):
    """
    Scans all module directories in the default 'Modules' directory and documents
    Python scripts in 'Documentation/Module_Name'.

    Parameters:
        modules_dir (str): Path to the root directory containing module directories.
        documentation_dir (str): Root directory for storing documentation files.
    """
    try:
        # Check if the modules directory exists
        if not os.path.isdir(modules_dir):
            print(f"The specified directory '{modules_dir}' does not exist.")
            return
        
        # Create the documentation root directory
        os.makedirs(documentation_dir, exist_ok=True)

        # Get a list of subdirectories (modules) in the modules directory
        module_names = [name for name in os.listdir(modules_dir) if os.path.isdir(os.path.join(modules_dir, name))]
        
        for module_name in module_names:
            module_path = os.path.join(modules_dir, module_name)
            doc_path = os.path.join(documentation_dir, module_name)
            
            # Create documentation directory for the module
            os.makedirs(doc_path, exist_ok=True)

            # Scan the module directory for Python scripts
            submodules = []
            for root, _, files in os.walk(module_path):
                for file in files:
                    if file.endswith(".py") and not file.startswith("__"):
                        relative_path = os.path.relpath(os.path.join(root, file), module_path)
                        submodules.append(relative_path)

            # Save the list of submodules to a text file
            submodules_file = os.path.join(doc_path, "submodules.txt")
            with open(submodules_file, "w") as f:
                f.write("\n".join(submodules))
            print(f"Submodules for '{module_name}' saved in '{submodules_file}'.")

            # Convert scripts to .txt files
            for submodule in submodules:
                full_script_path = os.path.join(module_path, submodule)
                if not os.path.isfile(full_script_path):
                    print(f"File not found: {full_script_path}")
                    continue

                with open(full_script_path, "r") as script_file:
                    content = script_file.read()

                txt_file_name = os.path.splitext(os.path.basename(submodule))[0] + ".txt"
                output_txt_path = os.path.join(doc_path, txt_file_name)

                with open(output_txt_path, "w") as txt_file:
                    txt_file.write(content)

                print(f"Converted '{submodule}' to '{output_txt_path}'.")

        print("All modules have been captured.")
    
    except Exception as e:
        print(f"An error occurred: {e}")


# Execution
if __name__ == "__main__":
    scan_and_document_modules()
