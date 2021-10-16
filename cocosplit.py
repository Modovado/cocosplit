"""
Originated from:
https://github.com/akarazniewicz/cocosplit/blob/master/cocosplit.py
"""

import json
import argparse
from sklearn.model_selection import train_test_split

parser = argparse.ArgumentParser(description='Splits COCO annotations file into training and test sets.')

parser.add_argument('annotations', metavar='coco_annotations', type=str, help='Path to COCO annotations file (*.json)')
parser.add_argument('train', type=str, help='Where to store COCO train annotations (*.json)')
parser.add_argument('test', type=str, help='Where to store COCO val/test annotations (*.json)')
parser.add_argument('--classname', type=str, help='Path to COCO class name file (*.txt)')
parser.add_argument('--split', default=0.8, type=float, help="A percentage of a split; a number in (0, 1)")

args = parser.parse_args()

def save_coco(file, images, annotations, categories):
    with open(file, 'wt', encoding='UTF-8') as coco:
        json.dump({'images': images, 'annotations': annotations, 'categories': categories}, coco, indent=2)


def flatten(x):  # make list of lists to list
    # https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-a-list-of-lists
    return [item for sublist in x for item in sublist]

def main(args):
    with open(args.annotations, 'rt', encoding='UTF-8') as annotations:

        # make a list to save sorted output
        annotations_list = []

        coco = json.load(annotations)
        images = coco['images']
        annotations = coco['annotations']
        categories = coco['categories']

# annotations
    # sort annotations by image
    for i in range(len(images)):
        print(f'processing : {i + 1}...')
        # if annotation's image_id is matching to image's id
        annotations_list.append([annotation for annotation in annotations if annotation['image_id'] == images[i]['id']])

    # assert when lens are not matching
    assert len(images) == len(
        annotations_list), f'`num_images`({len(images)}) not match `num_annotations_list`({len(annotations_list)})'
    img_x, img_y, anno_x, anno_y = train_test_split(images, annotations_list, train_size=args.split, shuffle=True)

    print(f'before flatten: x:{len(anno_x)},y:{len(anno_y)}')

    anno_x = flatten(anno_x)
    anno_y = flatten(anno_y)

    print(f'after flatten: x:{len(anno_x)},y:{len(anno_y)}')

# categories
    if args.classname is not None:
    # load txt readlines but replace out the \n in line
        txt = [line.replace('\n', '') for line in open(args.classname, 'r').readlines()]

        # assert when lens are not matching
        assert len(categories) == len(txt), f'`num_categories`({len(categories)}) not match `num_classname`({len(txt)})'

        # change categories' name
        for i in range(len(txt)):
            categories[i]['name'] = txt[i]
            # print(categories[i]['name'])

    save_coco(args.train, img_x, anno_x, categories)
    save_coco(args.test, img_y, anno_y, categories)

    print("Saved {} entries in {} and {} in {}".format(len(img_x), args.train, len(img_y), args.test))

if __name__ == "__main__":
    main(args)
