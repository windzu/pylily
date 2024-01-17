from .utils import parse_config, collect_data
import rospy
import ros_numpy
from sensor_msgs.msg import PointCloud2


class ManualCalibrator:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = parse_config(config_path)

    def run(self):
        print("manual calibrator")
        print(self.config)

        self.data_dict = {}
        self.topic_and_frame_id_dict = {}
        self.subscribers = {}

        (
            self.data_dict,
            self.topic_to_frame_id_dict,
            self.frame_id_to_topic_dict,
        ) = collect_data(self.config)
