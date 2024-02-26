import json
import os
import sys

DATA_ROOT = '../../../../data/tir/projects/tir4/users/svarna/A2Summ/data/BLiSS/annotation/'

if __name__ == '__main__':
    mode = sys.argv[1]
    with open(f"{DATA_ROOT}{mode}.json", "r") as file:
        data = json.load(file)

    video_parts = {}
    updated_data = {}

    keys = ['video_label', 'text_label', 'sentence', 'sentence_time', 'num_frame', 'num_keyframe', 'num_sentence', 'highlight', 'abstractive_summary']

    for k, i in enumerate(data):
        idx = data[i]['video_id']
        if idx not in list(video_parts.keys()):
            video_parts[idx] = []
        if idx not in list(updated_data.keys()):
            updated_data[idx] = {}
            updated_data[idx]['video_label'], updated_data[idx]['text_label'] = [], []
            updated_data[idx]['sentence'], updated_data[idx]['sentence_time'] = [], []
            updated_data[idx]['num_frame'], updated_data[idx]['num_keyframe'], updated_data[idx]['num_sentence'] = 0, 0, 0
            updated_data[idx]['highlight'] = []
            updated_data[idx]['abstractive_summary'] = ''

        video_parts[idx].append(i)
        for time in data[i]['sentence_time']:
            time[0] += updated_data[idx]['num_frame']
            time[1] += updated_data[idx]['num_frame']
        for key in keys:
            updated_data[idx][key] += data[i][key]
        
    with open(f'{DATA_ROOT}updated_{mode}.json', 'w') as out_file:
        json.dump(updated_data, out_file)
    
    with open(f'{DATA_ROOT}index_{mode}.json', 'w') as ind_file:
        json.dump(video_parts, ind_file)
        
