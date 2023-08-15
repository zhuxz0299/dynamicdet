from PIL import Image
import os

# Convert DOTA dataset  to COCO format
classes = [ 'plane', 'ship', 'storage-tank', 'baseball-diamond', 
            'tennis-court','basketball-court', 'ground-track-field', 'harbor', 
            'bridge', 'large-vehicle', 'small-vehicle', 'helicopter', 
            'roundabout', 'soccer-ball-field', 'swimming-pool', 'container-crane']

# Read dota files

# img_path = "/home/lingjie/git-repos/DynamicDet/DOTA/train/images/P0000.png"
# file_path = "/home/lingjie/git-repos/DynamicDet/DOTA/train/original_labels/P0000.txt"

# Input and output directories
input_img_dir = "/home/lingjie/git-repos/DynamicDet/DOTA/train_split_128/images/"
input_label_dir = "/home/lingjie/git-repos/DynamicDet/DOTA/train_split_128/original_labels/"
output_label_dir = "/home/lingjie/git-repos/DynamicDet/DOTA/train_split_128/labels/"


def convert(name):
    img_path = input_img_dir + name + ".png"
    input_label_path = input_label_dir + name + ".txt"
    output_label_path = output_label_dir + name + ".txt"

    write_lines = []
    img = Image.open(img_path)
    img_w, img_h = img.size

    with open(input_label_path, 'r') as f:
        lines = f.readlines()
        if (lines and "imagesource" in lines[0]):
            lines = lines[2:]
        for line in lines:
            line = line.strip().split(' ')[8:9] + line.strip().split(' ')[:8]
            line[0] = str(classes.index(line[0]))
            for x_index in range(1, 9, 2):
                line[x_index] = str(round(float(line[x_index])/img_w, 6))
            for y_index in range(2, 9, 2):
                line[y_index] = str(round(float(line[y_index])/img_h, 6))
            write_lines.append(line)

    # Write lines to coco files
    with open(output_label_path , 'w') as f:
        for line in write_lines:
            f.write(" ".join(line) + '\n')


if __name__ == "__main__":
    for img_name in os.listdir(input_img_dir):
        name = img_name.split('.')[0]
        convert(name)