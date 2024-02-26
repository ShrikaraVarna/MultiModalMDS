import os
import random
import torch
import h5py
import numpy as np
import json
import math
from tqdm import tqdm

from helpers.bbox_helper import get_loc_label, get_ctr_label
from helpers.vsumm_helper import get_keyshot_summ

class BLiSSDataset(object):
    def __init__(self, mode='train', args=None):
        self.gt = json.load(open('{}/{}/annotation/updated_{}.json'.format(args.data_root, args.dataset, mode)))
        self.indx = json.load(open('{}/{}/annotation/index_{}.json'.format(args.data_root, args.dataset, mode)))
        self.clip_id_list = list(self.gt.keys())

        video_feature_path = '{}/{}/feature/video_clip_{}.npy'.format(args.data_root, args.dataset, mode)
        text_feature_path = '{}/{}/feature/text_roberta_{}.npy'.format(args.data_root, args.dataset, mode)
        video_summ_feature_path = '{}/{}/feature/video_summ_clip_{}.npy'.format(args.data_root, args.dataset, mode)
        video_feature_dict = np.load(video_feature_path, allow_pickle=True).item()
        text_feature_dict = np.load(text_feature_path, allow_pickle=True).item()
        video_summ_feature_dict = np.load(video_summ_feature_path, allow_pickle=True).item()

        self.video_dict = {}
        self.video_summ_dict = {}
        self.text_dict = {}
        for clip_id in tqdm(self.clip_id_list):
            self.video_dict[clip_id] = torch.tensor(video_feature_dict[clip_id]).to(torch.float32)
            self.text_dict[clip_id] = torch.tensor(text_feature_dict[clip_id]).to(torch.float32)
            self.video_summ_dict[clip_id] = torch.tensor(video_summ_feature_dict[clip_id]).to(torch.float32)
            
    def __len__(self):
        return len(self.clip_id_list)
    
    def __getitem__(self, index):
        clip_id = self.clip_id_list[index]
        video_id = self.gt[clip_id]['video_id']

        video = self.video_dict[clip_id] # [T, 512]
        video_summ = self.video_summ_dict[clip_id] # [N, 512]
        text = self.text_dict[clip_id] # [T, 768]

        video_label = torch.tensor(self.gt[clip_id]['video_label'], dtype=torch.long)
        text_label = torch.tensor(self.gt[clip_id]['text_label'], dtype=torch.long)

        num_frame = self.gt[clip_id]['num_frame']
        num_keyframe = self.gt[clip_id]['num_keyframe']
        num_sentence = self.gt[clip_id]['num_sentence']

        assert torch.sum(video_label) == num_keyframe
            
        sentence = self.gt[clip_id]['sentence']
        highlight = self.gt[clip_id]['highlight']
        time_index = self.gt[clip_id]['sentence_time']
        
        video_to_text_mask = torch.zeros((num_frame, num_sentence), dtype=torch.long)
        text_to_video_mask = torch.zeros((num_sentence, num_frame), dtype=torch.long)
        for j in range(num_sentence):
            start_frame, end_frame = time_index[j]
            video_to_text_mask[start_frame: end_frame, j] = 1
            text_to_video_mask[j, start_frame: end_frame] = 1
        
        mask_video = torch.ones(num_frame, dtype=torch.long)
        mask_video_summ = torch.ones(num_keyframe, dtype=torch.long)
        mask_text = torch.ones(num_sentence, dtype=torch.long)

        return video, video_summ, text, mask_video, mask_video_summ, mask_text, video_label, text_label, sentence, highlight, video_to_text_mask, text_to_video_mask

def worker_init_fn(worker_id):
    """
    Re-seed each worker process to preserve reproducibility
    """
    worker_seed = torch.initial_seed() % 2**32
    np.random.seed(worker_seed)
    random.seed(worker_seed)
    return

def my_collate_fn(batch):
    batched_output_list = []
    for i in range(len(batch[0])):
        batched_output = [item[i] for item in batch]
        batched_output_list.append(batched_output)
    return batched_output_list