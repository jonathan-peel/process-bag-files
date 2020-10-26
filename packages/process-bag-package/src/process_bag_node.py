#!/usr/bin/env python3

print("Script running! Please ensure that the bag to be processed (BAG_NAME) \
is in your ~/Documents folder.")

import os
import rosbag
import numpy as np
import cv2
from cv_bridge import CvBridge

""" 
    This program extracts is for exercise 20. It processes the image messages
    from any bag specified by BAG_NAME. This must be in the ~/Documents 
    directory of the machine running this code. The code extracts the images,
    and then pastes the timestamp of the image on each image's bottom-left 
    corner. These new images are written into a new bagfile with their topic 
    and timestamp. The new bag file is called processed_bag.bag and can be 
    found in the mounted ~/Documents directory.
"""

# Extract the bag name from the mounted volume using the runtime environment 
# variable
bag_name = os.environ["BAG_NAME"]
bag = rosbag.Bag("mounted-vol/{}".format(bag_name))

# Find the topic name for the image msg using a versatile search
topics_list = bag.get_type_and_topic_info()[1].keys()
image_topic = [topic for topic in topics_list if 'image' in topic][0]

with rosbag.Bag("mounted-vol/processed_bag.bag", "w") as processed_bag:
    for topic, image_msg, timestamp in bag.read_messages(image_topic):
        # Extract the timestamp and image from the message

        # Convert the image to OpenCV image
        bridge = CvBridge()
        image_cv = bridge.compressed_imgmsg_to_cv2(image_msg)

        # Draw the timestamp on the image
        org =  (4, image_cv.shape[0] - 8) # Position text in bottom-left corner
        font_face = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        text_color = 0 # Black text
        thickness = 2
        image_timestamped_cv = cv2.putText(image_cv, str(timestamp), org, font_face, font_scale, text_color, thickness)

        # Convert image back to ros image msg
        img_timestamped_msg = bridge.cv2_to_compressed_imgmsg(image_timestamped_cv)

        # Write timestamped image to the new bag file
        processed_bag.write(topic, img_timestamped_msg, timestamp)

bag.close()
print("Bag processed sucessfully! Please check your ~/Documents directory for \
processed_bag.bag.")
