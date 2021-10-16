#### Modified version of  `akarazniewicz/cocosplit` for a niche case  

Simple tool to split coco annotations (json) into train and test sets.

## Installation

``cocosplit`` requires python 3 and dependencies:

```
pip install -r requirements
```

## Usage

```
Splits COCO annotations file into training and test sets.

positional arguments:

  annotations           Path to COCO annotations file (*.json)
  train                 Where to store COCO train annotations (*.json)
  test                  Where to store COCO val/test annotations (*.json)
  
optional arguments:

  --classname           Path to COCO class name file (*.txt)
  --split               A percentage of a split; a number in (0, 1), default : 0.8
  
```

## Running

```
$ python cocosplit.py /path/to/your/coco_annotations.json train.json test.json
```

will split ``coco_annotation.json`` into ``train.json`` and ``test.json`` with ratio 80 20 respectively
