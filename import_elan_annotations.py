import os
import xml.etree.ElementTree as ElementTree
from pathlib import Path
from typing import List, Dict
from numpy import arange

import pandas as pd


def get_annotation_files(path_to_top_level_folder):
    return [p for p in Path(path_to_top_level_folder).rglob('*.eaf')]


def get_data_files(path_to_top_level_folder):
    return [p for p in Path(path_to_top_level_folder).rglob('*.csv')]


class EafParser:
    file_path: str
    root: ElementTree.Element
    timeslot_element: ElementTree.Element
    timeslots: List[int]
    time_origin: int
    annotations: pd.DataFrame = None
    top_level_path: str
    data: pd.DataFrame = None
    tier_annotations: Dict
    codes: pd.DataFrame
    time_origin: int

    def __init__(self, file_path, search_path=None, load_data=False):
        self.file_path = file_path
        self.path_to_data = None
        self.tier_annotations = {}
        self.load_eaf()
        self.parse_timeslots()
        self.parse_annotations()
        self.top_level_path = search_path
        if load_data:
            self.get_path_to_data_file()
            self.load_data()
        self.parse_time_origin()

    def load_eaf(self):
        tree = ElementTree.parse(self.file_path)
        self.root = tree.getroot()
        self.timeslot_element = self.root.find('TIME_ORDER')

    def parse_timeslots(self):
        self.timeslots = [int(ts.get('TIME_VALUE')) for ts in self.timeslot_element]

    def parse_annotations(self):
        tier_elements = self.root.findall('TIER')
        for tier in tier_elements:
            self.tier_annotations[tier.get('TIER_ID')] = self.parse_tier(tier)

    def parse_tier(self, tier_element):
        annotation_list = None
        for annotation in tier_element.findall('ANNOTATION'):
            try:
                if int(annotation[0].get('TIME_SLOT_REF2')[2:]) - 1 < len(self.timeslots):
                    idx = annotation[0].get('ANNOTATION_ID')
                    start_time = self.timeslots[int(annotation[0].get('TIME_SLOT_REF1')[2:]) - 1] / 1000
                    end_time = self.timeslots[int(annotation[0].get('TIME_SLOT_REF2')[2:]) - 1] / 1000
                    annotation_value = 'NULL'
                else:
                    continue
            except IndexError as e:
                print(str(e))
                continue
            for annotation_details in annotation:
                annotation_value = annotation_details[0].text
            if annotation_list is None:
                annotation_list = [[idx, start_time, end_time, annotation_value, (end_time - start_time)]]
            else:
                annotation_list.append([idx, start_time, end_time, annotation_value, (end_time - start_time)])

        return pd.DataFrame(annotation_list, columns=['id', 'start', 'stop', 'label', 'duration'])

    def parse_time_origin(self):
        self.time_origin = int(self.root.find('HEADER').find('MEDIA_DESCRIPTOR').get('TIME_ORIGIN'))

    def get_path_to_data_file(self):
        data_files = [f.get('LINK_URL') for f in (self.root.find('HEADER').findall('LINKED_FILE_DESCRIPTOR')) if
                      '.csv' in f.get('LINK_URL')]
        if len(data_files) > 0:
            self.path_to_data = data_files[0]
            if not os.path.isfile(self.path_to_data):
                search_path = self.top_level_path

                searchable_files = list(Path(search_path).rglob('*' + Path(self.path_to_data).name[:-4] + ".csv"))
                if len(searchable_files) > 0:
                    corrected_files = [s for s in searchable_files if 'corrected' in str(s)]
                    if len(corrected_files) == 0:
                        self.path_to_data = searchable_files[0]
                    else:
                        self.path_to_data = corrected_files[0]
                else:
                    self.path_to_data = None
            else:
                self.path_to_data = data_files[0]
        else:
            self.path_to_data = None

    def load_data(self):
        if self.path_to_data is not None:
            if not os.path.isfile(self.path_to_data):
                data_files = [p for p in get_data_files(self.top_level_path)]
                if self.path_to_data.split('/')[-1] in [d.name for d in data_files]:
                    try:
                        self.path_to_data = [d for d in data_files if d.name == self.path_to_data.split('/')[-1]][0]
                    except IndexError:
                        raise IndexError
            try:
                self.data = pd.read_csv(Path(self.path_to_data)).iloc[:, :4]
            except Exception:
                try:
                    self.data = pd.read_csv(Path(self.path_to_data[8:])).iloc[:, :4]
                except Exception:
                    self.data = None
        else:
            self.data = None

    def get_labeled_data(self) -> pd.DataFrame():
        if self.data is None:
            raise FileNotFoundError
        labeled_data = self.data.copy()
        labeled_data.columns = ['timestamp', 'x', 'y', 'z'] + list(arange(4, labeled_data.shape[1]))
        for tier in self.tier_annotations:
            labeled_data[tier] = 'NULL'
            for row, annotation in self.tier_annotations[tier].iterrows():
                labeled_data.loc[(labeled_data['timestamp'] < annotation['stop']) & (
                        labeled_data['timestamp'] >= annotation['start']), tier] = annotation['label']
                # labeled_data.loc[list(
                #     map(lambda l: annotation['stop'] > l >= annotation['start'], labeled_data['timestamp'])), tier] = \
                #     annotation['label']
        return labeled_data

    def get_annotation_durations(self) -> pd.DataFrame:
        output_df = pd.DataFrame(columns=['label', 'duration'])
        for tier in self.tier_annotations:
            for row, annotation in self.tier_annotations[tier].iterrows():
                output_df = output_df.append({'label': annotation['label'], 'duration': annotation['duration']}, ignore_index=True)
        return output_df

    def load_behavior_codes(self, path_to_behavior_codes: str = 'Q:/adp/behavior_codes.csv'):
        self.codes = pd.read_csv(path_to_behavior_codes)
