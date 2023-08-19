import os, uuid, shutil
from pathlib import Path

threads = 4
last_output_dir = ""


def build_command(input_file: str, output_dir: str, i: int) -> str:
    global threads

    if i == 0:
        return f'-i "{input_file}" -c:a aac -c:v h264 -b:v 32k -b:a 8k -ar 8000 "{os.path.join(output_dir, "crunch0.mp4")}" -y -threads {threads}'
    else:
        return f"-i \"{os.path.join(output_dir, f'crunch{i - 1}.mp4')}\" -c:a aac -c:v h264 -b:v 32k -b:a 8k -ar 8000 \"{os.path.join(output_dir, f'crunch{i}.mp4')}\" -y -threads {threads}"


def main():
    global last_output_dir

    output_dir = f"TEMP_{uuid.uuid4().hex}"
    input_file = input("Input File: ")

    last_output_dir = output_dir

    if not os.path.isfile(input_file):
        print("E: Could not find input file")
        exit(1)

    print(f"->Path: {os.path.abspath(input_file)}")

    iterations = input("Compression Iterations: ")

    try:
        iterations = int(iterations)

    except ValueError:
        print("E: Invalid Iterations")
        exit(1)

    # Create temporary directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(0, iterations):
        command = build_command(input_file, output_dir, i)
        os.system(f"ffmpeg {command}")

    # Move last output
    last_iteration_file = os.path.join(output_dir, f"crunch{iterations - 1}.mp4")
    final_filename = f"{Path(input_file).stem}_compressed.mp4"
    os.replace(last_iteration_file, final_filename)

    # Delete temporary files
    shutil.rmtree(output_dir)

    print(f"-> {Path.absolute(Path(final_filename))}")


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\nE: Operation aborted")

        # Removes last output dir when aborting
        if os.path.exists(last_output_dir):
            shutil.rmtree(last_output_dir)
