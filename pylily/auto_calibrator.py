from .utils import parse_config
import rospy
import ros_numpy
from sensor_msgs.msg import PointCloud2


class AutoCalibrator:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = parse_config(config_path)

    def run(self):
        print("auto calibrator")

        print(self.config)

    def collect_data(self):
        load_way = self.config["load_way"]  # topic or file
        self.data_dict = {}
        self.topic_and_frame_id_dict = {}
        self.subscribers = {}

        # iter self.config["data"] get frame_id and topic map
        for i in range(len(self.config["data"])):
            frame_id = self.config["data"][i]["frame_id"]
            topic = self.config["data"][i]["topic"]
            self.topic_and_frame_id_dict[topic] = frame_id

        # iter self.config["data"] get all frame_id and data
        for i in range(len(self.config["data"])):
            frame_id = self.config["data"][i]["frame_id"]
            topic = self.config["data"][i]["topic"]
            file = self.config["data"][i]["file"]

            if load_way == "topic":
                # create subscriber
                self.subscribers[topic] = rospy.Subscriber(
                    topic, PointCloud2, lambda data: self.collect_data_callback(data, topic)
                )

    def collect_data_callback(self, data, topic):
        print(f"Received data from topic: {topic}")
        frame_id = self.topic_and_frame_id_dict[topic]

        # convert data to numpy array
        array = ros_numpy.numpify(data)
        self.data_dict[frame_id] = array
