import sys

def preview_entries(file_path, lines=10):
    with open(file_path, "r") as file:
        all_lines = file.readlines()
    
    preview = all_lines[-lines:]
    for line in preview:
        print(line, end="")

if __name__ == "__main__":
    file_path = sys.argv[1]
    lines = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    preview_entries(file_path, lines)