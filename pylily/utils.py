import yaml
import rospy
import ros_numpy
import os
from sensor_msgs.msg import PointCloud2
import numpy as np
from pypcd import pypcd


def parse_config(config_path):
    config = {}
    with open(config_path, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    # check config
    # - load_way
    if "load_way" not in config:
        raise ValueError("load_way should be in config")
    else:
        load_way = config["load_way"]
        if load_way not in ["topic", "file"]:
            raise ValueError("load_way should be topic or file")

    # - result_config
    if "result_config" not in config:
        raise ValueError("result_config should be in config")
    else:
        result_config = config["result_config"]
        # format and path check
        if "format" not in result_config:
            raise ValueError("format should be in result_config")
        else:
            format = result_config["format"]  # common or yczx
            if format not in ["common", "yczx"]:
                raise ValueError("format should be common or yczx")
        if "path" not in result_config:
            raise ValueError("path should be in result_config")

    return config


def collect_data(config):
    load_way = config["load_way"]  # topic or file

    # need to return
    data_dict = {}
    topic_to_frame_id_dict = {}
    frame_id_to_topic_dict = {}

    subscribers = {}

    def collect_data_callback(data, topic):
        print(f"Received data from topic: {topic}")
        frame_id = topic_to_frame_id_dict[topic]

        # convert data to numpy array
        pc = pypcd.PointCloud.from_msg(data)
        array = pc.to_np_array()

        # array = ros_numpy.numpify(data)
        data_dict[frame_id] = array

    # iter config["data"] get frame_id and topic map
    for i in range(len(config["data"])):
        frame_id = config["data"][i]["frame_id"]
        topic = config["data"][i]["topic"]
        data_dict[frame_id] = None
        topic_to_frame_id_dict[topic] = frame_id
        frame_id_to_topic_dict[frame_id] = topic

    # iter config["data"] get all frame_id and data
    if load_way == "topic":
        # ros node init
        rospy.init_node("pylily", anonymous=True)
    for i in range(len(config["data"])):
        frame_id = config["data"][i]["frame_id"]
        topic = config["data"][i]["topic"]
        file = config["data"][i]["file"]

        if load_way == "topic":
            # create subscriber
            subscribers[topic] = rospy.Subscriber(
                topic,
                PointCloud2,
                lambda data: collect_data_callback(data, topic),
            )
        elif load_way == "file":
            # load file
            # check if path exist
            if not os.path.exists(file):
                raise ValueError(f"file {file} not exist")
            pc = pypcd.PointCloud.from_path(file)
            array = pc.to_np_array()
            data_dict[frame_id] = array

    # check data
    if load_way == "topic":
        # loop until all data is collected in 2 seconds
        water_time = 2
        start_time = rospy.Time.now()
        rate = rospy.Rate(10)
        while not check_data(data_dict):
            if (rospy.Time.now() - start_time).to_sec() > water_time:
                raise ValueError("collect data timeout")
            rate.sleep()
        # shutdown all subscribers
        for topic in subscribers:
            subscribers[topic].unregister()
    elif load_way == "file":
        if not check_data(data_dict):
            raise ValueError("collect data failed")

    # return
    return data_dict, topic_to_frame_id_dict, frame_id_to_topic_dict


def check_data(data_dict):
    for frame_id in data_dict:
        if data_dict[frame_id] is None:
            return False
    return True
