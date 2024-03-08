# Ultralytics YOLO 🚀, AGPL-3.0 license

from collections import defaultdict

import cv2
import numpy as np

from ultralytics.utils.checks import check_imshow, check_requirements
from ultralytics.utils.plotting import Annotator

check_requirements('shapely>=2.0.0')

from shapely.geometry import Polygon
from shapely.geometry.point import Point


class Heatmap:
    """A class to draw heatmaps in real-time video stream based on their tracks."""

    def __init__(self):
        """Initializes the heatmap class with default values for Visual, Image, track, count and heatmap parameters."""

        # Visual information
        self.annotator = None
        self.view_img = False

        # Image information
        self.imw = None
        self.imh = None
        self.im0 = None

        # Heatmap colormap and heatmap np array
        self.colormap = None
        self.heatmap = None
        self.heatmap_alpha = 0.5

        # Predict/track information
        self.boxes = None
        self.track_ids = None
        self.clss = None
        self.track_history = None

        # Counting info
        self.count_reg_pts = None
        self.count_region = None
        self.in_counts = 0
        self.out_counts = 0
        self.count_list = []
        self.count_txt_thickness = 0
        self.count_reg_color = (0, 255, 0)
        self.region_thickness = 5

        # Check if environment support imshow
        self.env_check = check_imshow(warn=True)

    def set_args(self,
                 imw,
                 imh,
                 colormap=cv2.COLORMAP_JET,
                 heatmap_alpha=0.5,
                 view_img=False,
                 count_reg_pts=None,
                 count_txt_thickness=2,
                 count_reg_color=(255, 0, 255),
                 region_thickness=5):
        """
        Configures the heatmap colormap, width, height and display parameters.

        Args:
            colormap (cv2.COLORMAP): The colormap to be set.
            imw (int): The width of the frame.
            imh (int): The height of the frame.
            heatmap_alpha (float): alpha value for heatmap display
            view_img (bool): Flag indicating frame display
            count_reg_pts (list): Object counting region points
            count_txt_thickness (int): Text thickness for object counting display
            count_reg_color (RGB color): Color of object counting region
            region_thickness (int): Object counting Region thickness
        """
        self.imw = imw
        self.imh = imh
        self.colormap = colormap
        self.heatmap_alpha = heatmap_alpha
        self.view_img = view_img

        self.heatmap = np.zeros((int(self.imw), int(self.imh)), dtype=np.float32)  # Heatmap new frame

        if count_reg_pts is not None:
            self.track_history = defaultdict(list)
            self.count_reg_pts = count_reg_pts
            self.count_region = Polygon(self.count_reg_pts)

        self.count_txt_thickness = count_txt_thickness  # Counting text thickness
        self.count_reg_color = count_reg_color
        self.region_thickness = region_thickness

    def extract_results(self, tracks):
        """
        Extracts results from the provided data.

        Args:
            tracks (list): List of tracks obtained from the object tracking process.
        """
        self.boxes = tracks[0].boxes.xyxy.cpu()
        self.clss = tracks[0].boxes.cls.cpu().tolist()
        self.track_ids = tracks[0].boxes.id.int().cpu().tolist()

    def generate_heatmap(self, im0, tracks):
        """
        Generate heatmap based on tracking data.

        Args:
            im0 (nd array): Image
            tracks (list): List of tracks obtained from the object tracking process.
        """
        self.im0 = im0
        if tracks[0].boxes.id is None:
            return self.im0

        self.extract_results(tracks)
        self.annotator = Annotator(self.im0, self.count_txt_thickness, None)

        if self.count_reg_pts is not None:
            # Draw counting region
            self.annotator.draw_region(reg_pts=self.count_reg_pts,
                                       color=self.count_reg_color,
                                       thickness=self.region_thickness)

            for box, cls, track_id in zip(self.boxes, self.clss, self.track_ids):
                self.heatmap[int(box[1]):int(box[3]), int(box[0]):int(box[2])] += 1

                # Store tracking hist
                track_line = self.track_history[track_id]
                track_line.append((float((box[0] + box[2]) / 2), float((box[1] + box[3]) / 2)))
                if len(track_line) > 30:
                    track_line.pop(0)

                # Count objects
                if self.count_region.contains(Point(track_line[-1])):
                    if track_id not in self.count_list:
                        self.count_list.append(track_id)
                        if box[0] < self.count_region.centroid.x:
                            self.out_counts += 1
                        else:
                            self.in_counts += 1
        else:
            for box, cls in zip(self.boxes, self.clss):
                self.heatmap[int(box[1]):int(box[3]), int(box[0]):int(box[2])] += 1

        # Normalize, apply colormap to heatmap and combine with original image
        heatmap_normalized = cv2.normalize(self.heatmap, None, 0, 255, cv2.NORM_MINMAX)
        heatmap_colored = cv2.applyColorMap(heatmap_normalized.astype(np.uint8), self.colormap)

        if self.count_reg_pts is not None:
            incount_label = 'InCount : ' + f'{self.in_counts}'
            outcount_label = 'OutCount : ' + f'{self.out_counts}'
            self.annotator.count_labels(in_count=incount_label, out_count=outcount_label)

        im0_with_heatmap = cv2.addWeighted(self.im0, 1 - self.heatmap_alpha, heatmap_colored, self.heatmap_alpha, 0)

        if self.env_check and self.view_img:
            self.display_frames(im0_with_heatmap)

        return im0_with_heatmap

    @staticmethod
    def display_frames(im0_with_heatmap):
        """
        Display heatmap.

        Args:
            im0_with_heatmap (nd array): Original Image with heatmap
        """
        cv2.imshow('Ultralytics Heatmap', im0_with_heatmap)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            return


if __name__ == '__main__':
    Heatmap()
