# Get some sample data from the whole DOTA dataset
# Save sample images and labels to train_split_1024_sample/images(labels) and val_split_1024_sample/images(labels) and test_split_1024_sample/images(labels)
import os

train_dir = "/home/lingjie/git-repos/DynamicDet/DOTA/train_split_1024"
val_dir = "/home/lingjie/git-repos/DynamicDet/DOTA/val_split_1024"
test_dir = "/home/lingjie/git-repos/DynamicDet/DOTA/test_split_1024"

train_img_dir = train_dir + "/images"
train_label_dir = train_dir + "/labels"

val_img_dir = val_dir + "/images"
val_label_dir = val_dir + "/labels"

test_img_dir = test_dir + "/images"

train_img_list = os.listdir(train_img_dir)
train_label_list = os.listdir(train_label_dir)

val_img_list = os.listdir(val_img_dir)
val_label_list = os.listdir(val_label_dir)

test_img_list = os.listdir(test_img_dir)

train_img_list.sort()
train_label_list.sort()

val_img_list.sort()
val_label_list.sort()

test_img_list.sort()

train_img_list = train_img_list[:500]
train_label_list = train_label_list[:500]

val_img_list = val_img_list[:100]
val_label_list = val_label_list[:100]
test_img_list = test_img_list[:100]

print(train_img_list)
print(val_img_list)
print(test_img_list)

# Save sample images and labels
import shutil

for img in train_img_list:
    shutil.copy(train_img_dir + "/" + img, train_dir + "_sample/images")

for label in train_label_list:
    shutil.copy(train_label_dir + "/" + label, train_dir + "_sample/labels")

for img in val_img_list:
    shutil.copy(val_img_dir + "/" + img, val_dir + "_sample/images")

for label in val_label_list:
    shutil.copy(val_label_dir + "/" + label, val_dir + "_sample/labels")

for img in test_img_list:
    shutil.copy(test_img_dir + "/" + img, test_dir + "_sample/images")



