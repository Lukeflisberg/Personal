import csv
from models.block import Block
from PyQt5.QtWidgets import QFileDialog

def load_csv(filepath):
    """ Load blocks from a CSV file. """
    blocks = []
    
    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            block = Block(
                start_time=row['Start Time'],
                group=row['Group'],
                duration=row['Duration'],
                header=row['Header'],
                description=row['Description'],
                before_t=row['Before T'],
                after_t=row['After T']
            )
            blocks.append(block)

    return blocks

def import_blocks_from_csv(parent=None):
    """ Import blocks from multiple CSV files using a file dialog. """
    filepaths, _ = QFileDialog.getOpenFileNames(parent, "Open CSV Files", "", "CSV Files (*.csv)")
    if not filepaths:
        return []
    blocks = []
    for filepath in filepaths:
        with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                block = Block(
                    start_time=row['Start Time'],
                    group=row['Group'],
                    duration=row['Duration'],
                    header=row['Header'],
                    description=row['Description'],
                    before_t=row['Before T'],
                    after_t=row['After T']
                )
                blocks.append(block)
    return blocks

def save_to_csv(filepath, blocks):
    """ Save blocks to a CSV file. """
    with open(filepath, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Start Time', 'Group', 'Duration', 'Header', 'Description', 'Before T', 'After T']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for block in blocks:
            writer.writerow({
                'Start Time': block.start_time,
                'Group': block.group,
                'Duration': block.duration,
                'Header': block.header,
                'Description': block.description,
                'Before T': block.before_t,
                'After T': block.after_t
            })