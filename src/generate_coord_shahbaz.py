#put file in pose-tensorflow/demo and run from pose-tensorflow (deepercut implementation)
#time python demo/generate_coord.py ../size_normed_images/multiplied/train ../size_normed_images/csvs/ | tr -d "'[]" > joints.csv
import os
import sys
import numpy as np
import glob
sys.path.append(os.path.dirname(__file__) + "/../")
from scipy.misc import imread
from config import load_config
from nnet import predict
from util import visualize
from dataset.pose_dataset import data_to_input

if(len(sys.argv)< 2):
        print("python generate_coord.py input_dir output_dir")
        sys.exit(0)

cfg = load_config("demo/pose_cfg.yaml")
#{'all_joints': [[0, 5], [1, 4], [2, 3], [6, 11], [7, 10], [8, 9], [12], [13]],
#'video': False, 'log_dir': 'log', 'weigh_part_predictions': False, 'weight_decay': 0.0001, 'locref_stdev': 7.2801, 'intermediate_supervision': False, 'regularize': False, 'num_joints': 14, 'crop_pad': 0, 'locref_huber_loss': True, 'locref_loss_weight': 1.0, 'weigh_only_present_joints': False, 'global_scale': 1.0, 'optimizer': 'sgd', 'location_refinement': True, 'mean_pixel': [123.68, 116.779, 103.939], 'shuffle': True, 'video_batch': False, 'fg_fraction': 0.25, 'net_type': 'resnet_101', 'snapshot_prefix': 'snapshot', 'crop': False, 'weigh_negatives': False, 'batch_size': 1,
#'all_joints_names': ['ankle', 'knee', 'hip', 'wrist', 'elbow', 'shoulder', 'chin', 'forehead'],
#'intermediate_supervision_layer': 12, 'init_weights': 'models/mpii/mpii-single-resnet-101', 'stride': 8.0, 'scoremap_dir': 'test', 'mirror': False, 'dataset_type': 'mpii', 'use_gt_segm': False}
#r-ankle-x	r-ankle-y	r-knee-x	r-knee-y	r-hip-x	r-hip-y	l-hip-x	l-hip-y	l-knee-x	l-knee-y	l-ankle-x	l-ankle-y	pelvis-x	pelvis-y	thorax-x	thorax-y	upper-neck-x	upper-neck-y	head-top-x	head-top-y	r-wrist-x	r-wrist-y	r-elbow-x	r-elbow-y	r-shoulder-x	r-shoulder-y	l-shoulder-x	l-shoulder-y	l-elbow-x	l-elbow-y	l-wrist-x	l-wrist-y
#process config file

dirs = ["adho_mukha_svanasana",  "pasasana", "salamba_sirsasana", "virabhadrasana_ii",
"bharadvajasana", "salamba_sarvangasana", "virabhadrasana_i",  "virabhadrasana_iii"]

# Load and setup CNN part detector
sess, inputs, outputs = predict.setup_pose_prediction(cfg)

# Read image from file
# TODO write for loop to consume all images in data folder and run the algo once for each image, append coordinates to pose_coordinates.csv and repeat
# file_name = "demo/image.png"
file_name = sys.argv[1]
#===============================================================
input_dirs = sys.argv[1]
output_dirs = sys.argv[2]
for dir in dirs:
    curr_input_dir = os.path.join(input_dirs, dir)
    curr_output_dir = os.path.join(output_dirs, dir)
    #print(curr_input_dir)
    #print(curr_output_dir)
    for file_name in glob.glob(curr_input_dir + "/*.png"):
        image = imread(file_name, mode='RGB')

        image_batch = data_to_input(image)

        # Compute prediction with the CNN
        outputs_np = sess.run(outputs, feed_dict={inputs: image_batch})
        scmap, locref, _ = predict.extract_cnn_output(outputs_np, cfg)

        # Extract maximum scoring location from the heatmap, assume 1 person
        pose = predict.argmax_pose_predict(scmap, locref, cfg.stride)
        #reorganize Numpy array into a single row
        pose_csv = np.reshape(pose,42)
        pose_csv = np.append(pose_csv,file_name)
        pose_csv = np.append(pose_csv,dir)
        pose_csv = pose_csv[None]
        with open(os.path.join(curr_output_dir, os.path.basename(file_name) + ".csv"),'ab') as fhandle:
             	 np.savetxt(fhandle,pose_csv,delimiter=',',fmt='%s')
        fhandle.close()
        #o = ','.join(pose_csv.tolist())
        o = pose_csv.tolist()
        print(o)

sys.exit(0)
#===============================================================
image = imread(file_name, mode='RGB')

image_batch = data_to_input(image)

# Compute prediction with the CNN
outputs_np = sess.run(outputs, feed_dict={inputs: image_batch})
scmap, locref, _ = predict.extract_cnn_output(outputs_np, cfg)
#test = predict.extract_cnn_output(outputs_np, cfg)
#print(type(test))
#print(len(test))

# Extract maximum scoring location from the heatmap, assume 1 person
pose = predict.argmax_pose_predict(scmap, locref, cfg.stride)
#reorganize Numpy array into a single row
pose_csv = np.reshape(pose,42)
pose_csv = np.append(pose_csv,file_name)
pose_csv = pose_csv[None]
with open(sys.argv[2],'ab') as fhandle:
     	 np.savetxt(fhandle,pose_csv,delimiter=',',fmt='%s')
fhandle.close()
#===============================================================
