import subprocess
def run_script(script_name):
    """Execute a Python script and wait for it to finish."""
    result = subprocess.run(["python", script_name], check=True)
    return result.returncode == 0

def main():
    scripts_to_run = [
        "GUINonQuotesCSV.py",
        "GUIQuotesCSV.py",
        "create_book_csv.py",
        "book_display_and_generate_with_preview.py",
        "book_display_and_combine_gui.py"
    ]

    for script in scripts_to_run:
        print(f"Running {script} ...")
        success = run_script(script)
        if not success:
            print(f"Error encountered while running {script}. Stopping execution.")
            break
        print(f"{script} completed.")

if __name__ == "__main__":
    main()

