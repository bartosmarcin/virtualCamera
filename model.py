__author__ = 'marcin'
import numpy as np
import math
import copy
class Color:
    red = (255, 0, 0)
    green = (0,255,0)
    blue = (0,0,255)
    black = (0,0,0)
    white = (255,255,255)

class Object3D:
    def __init__(self, color, lines):
        self.lines = lines
        self.color = color

class ObjectBuilder:

    @staticmethod
    def build_cuboid(center, width, height, depth):
        w = width / 2
        h = height / 2
        d = depth / 2
        lines = [
            [np.matrix([[center[0] - w], [center[1] - h], [center[2] - d], [1]]),
             np.matrix([[center[0] + w], [center[1] - h], [center[2] - d], [1]])],
            [np.matrix([[center[0] + w], [center[1] - h], [center[2] - d], [1]]),
             np.matrix([[center[0] + w], [center[1] + h], [center[2] - d], [1]])],
            [np.matrix([[center[0] + w], [center[1] + h], [center[2] - d], [1]]),
             np.matrix([[center[0] - w], [center[1] + h], [center[2] - d], [1]])],
            [np.matrix([[center[0] - w], [center[1] + h], [center[2] - d], [1]]),
             np.matrix([[center[0] - w], [center[1] - h], [center[2] - d], [1]])],

            [np.matrix([[center[0] - w], [center[1] - h], [center[2] + d], [1]]),
             np.matrix([[center[0] + w], [center[1] - h], [center[2] + d], [1]])],
            [np.matrix([[center[0] + w], [center[1] - h], [center[2] + d], [1]]),
             np.matrix([[center[0] + w], [center[1] + h], [center[2] + d], [1]])],
            [np.matrix([[center[0] + w], [center[1] + h], [center[2] + d], [1]]),
             np.matrix([[center[0] - w], [center[1] + h], [center[2] + d], [1]])],
            [np.matrix([[center[0] - w], [center[1] + h], [center[2] + d], [1]]),
             np.matrix([[center[0] - w], [center[1] - h], [center[2] + d], [1]])],

            [np.matrix([[center[0] - w], [center[1] - h], [center[2] - d], [1]]),
             np.matrix([[center[0] - w], [center[1] - h], [center[2] + d], [1]])],
            [np.matrix([[center[0] - w], [center[1] + h], [center[2] - d], [1]]),
             np.matrix([[center[0] - w], [center[1] + h], [center[2] + d], [1]])],
            [np.matrix([[center[0] + w], [center[1] + h], [center[2] - d], [1]]),
             np.matrix([[center[0] + w], [center[1] + h], [center[2] + d], [1]])],
            [np.matrix([[center[0] + w], [center[1] - h], [center[2] - d], [1]]),
             np.matrix([[center[0] + w], [center[1] - h], [center[2] + d], [1]])],
        ]
        return lines

class VirtualCamera:
    def __init__(self):
        self.focalLen = 0.1
        self.x = 0
        self.y = 0
        self.z = -1000
        self.ang_x = 0
        self.ang_y = 0
        self.ang_z = 0

    def get2Dcast(self, lines):
        lines = self.translate(lines)
        lines = self.rotate(lines)
        lines = self.projectToCameraPlain(lines)
        return lines

    def translate(self, lines):
        return [self.translateLine(line) for line in lines]

    def translateLine(self, line):
        return [self.translatePoint(point) for point in line]

    def translatePoint(self, point):
            point_c = copy.copy(point)
            point_c[0][0]-=self.x
            point_c[1][0]-=self.y
            point_c[2][0]-=self.z
            return point_c

    def rotate(self, lines):
        lines = self.rotate_horizontal(lines)
        lines = self.rotate_vertical(lines)
        return lines

    def _get_x_rotation_matrix(self, ang_x):
        return np.matrix([
            [math.cos(math.radians(ang_x)), 0.0, math.sin(math.radians(ang_x)), 0.0],
            [0.0, 1, 0.0, 0.0],
            [-math.sin(math.radians(ang_x)), 0.0, math.cos(math.radians(ang_x)), 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
    def rotate_horizontal(self, lines):
        #print self.ang_x
        rotMat = self._get_x_rotation_matrix(self.ang_x)
        return [self.rotateLine(rotMat, line) for line in lines]

    def _get_y_rotation_matrix(self, ang_y):
        return np.matrix([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, math.cos(math.radians(ang_y)), -math.sin(math.radians(ang_y)), 0.0],
            [0.0, math.sin(math.radians(ang_y)),  math.cos(math.radians(ang_y)), 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])

    def rotate_vertical(self, lines):
#        print self.ang_y
        rotMat = self._get_y_rotation_matrix(self.ang_y)
        return [self.rotateLine(rotMat, line) for line in lines]

    def rotateLine(self,rotationMat, line):
        return [self.rotatePoint(rotationMat, point) for point in line]

    def rotatePoint(self, rotationMat, point):
        return rotationMat * point

    def setFocalLen(self, len):
        self.focalLen = len



    def projectToCameraPlain(self, lines):
        v = -1.0/self.focalLen
        castMat = np.matrix([[1.0, 0.0, 0.0, 0.0],
                            [0.0, 1.0, 0.0, 0.0],
                            [0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, v, 0.0]])
        return [self.projectLine(castMat, line) for line in lines if self.is_projectabel(line)]

    def projectLine(self, castMat, line):
        return [self.projectPoint(castMat, point) for point in line]

    def projectPoint(self, castMat, point):
        if point[2][0] < 0:
            return None
        point = castMat*point
        point /= point[3][0]
        return point

    def is_projectabel(self, line):
        return line[0][2][0]>0 and line[1][2][0]>0

    def move_camera(self, forward, right, up):
        move_vector = np.matrix([[right], [up], [forward], [1]])
        x_rot_mat = self._get_x_rotation_matrix(-self.ang_x)
        y_rot_mat = self._get_y_rotation_matrix(-self.ang_y)
        move_vector = self.rotatePoint(x_rot_mat, move_vector)
        move_vector = self.rotatePoint(y_rot_mat, move_vector)
        self.x-= move_vector[0][0]
        self.y-= move_vector[1][0]
        self.z-= move_vector[2][0]
