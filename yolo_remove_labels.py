import os

def process_txt_files(directory_path):
    # List all files in the directory
    files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]

    for idx, file_name in enumerate(files, start=1):
        file_path = os.path.join(directory_path, file_name)

        # Read the contents of the file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Filter out lines starting with [1, 2, 3, 4, 5, 6]
        lines = [line for line in lines if not line.strip().startswith(('0','1', '2', '3', '5'))]

        # Write the modified content back to the file
        with open(file_path, 'w') as file:
            file.writelines(lines)

        # Print file number every 500 files
        if idx % 500 == 0:
            print(f"Processed {idx} files.")

if __name__ == "__main__":
    # Specify the directory path where your text files are located
    directory_path = 'aerial_050124\id\labels'

    # Call the function to process the text files
    process_txt_files(directory_path)
