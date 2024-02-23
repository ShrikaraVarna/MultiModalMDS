import json
import sys
import matplotlib.pyplot as plt

if __name__ == '__main__':
    MODE = sys.argv[1]
    with open(f"../../../../data/tir/projects/tir4/users/svarna/A2Summ/data/BLiSS/annotation/{MODE}.json", "r") as file:
        data = json.load(file)
    video_id = {}
    overall = {}
    for l, i in enumerate(data):
        idx = data[i]['video_id']
        label = data[i]['video_label']
        if idx not in video_id.keys():
            video_id[idx] = {}
        count = 0
        for j in range(300):
            if label[j] == 1:
                count += 1
            else:
                if count != 0:
                    video_id[idx][count] = video_id[idx].get(count, 0) + 1
                    overall[count] = overall.get(count, 0) + 1
                count = 0
        if count != 0:
            video_id[idx][count] = video_id[idx].get(count, 0) + 1
            overall[count] = overall.get(count, 0) + 1

    x_axis = overall.keys()
    y_axis = overall.values()
    y_axis = [item / len(video_id.keys()) for item in y_axis]
    print(y_axis)
    
    plt.scatter(x_axis, y_axis, label=MODE)
    plt.xlabel('Average # of Consequent Key-Frames')
    plt.ylabel('Count')
    plt.title(f'{MODE} Dataset Analysis')
    plt.savefig(f'Average_{MODE}.png')

        
    
