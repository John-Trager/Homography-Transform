import numpy as np
import cv2
import matplotlib.pyplot as plt
import time # measure function time

class Point:

    def __init__(self,x: int,y: int):
        self.x = x
        self.y = y

class Transform:

    def __init__(self):
        self.H = None
        self.img = None
        self.img_transform = None



    def add_points(self, p_in: list[Point], p_to: list[Point]):
        # 4 points (img 1) -> 4 transfrom points (img 2)
        # 8 points total

        a1 = p_in[0]
        a2 = p_in[1]
        a3 = p_in[2]
        a4 = p_in[3]

        b1 = p_to[0]
        b2 = p_to[1]
        b3 = p_to[2]
        b4 = p_to[3]

        # print input and outputs points
        print (a1, a2, a3, a4, b1, b2, b3, b4)

        A = np.mat([[-a1.x,-a1.y,-1,0,0,0, a1.x*b1.x, a1.y*b1.x, b1.x],
                    [0,0,0,-a1.x,-a1.y,-1, a1.x*b1.y, a1.y*b1.y, b1.y],
                    [-a2.x,-a2.y,-1,0,0,0, a2.x*b2.x, a2.y*b2.x, b2.x],
                    [0,0,0,-a2.x,-a2.y,-1, a2.x*b2.y, a2.y*b2.y, b2.y],
                    [-a3.x,-a3.y,-1,0,0,0, a3.x*b3.x, a3.y*b3.x, b3.x],
                    [0,0,0,-a3.x,-a3.y,-1, a3.x*b3.y, a3.y*b3.y, b3.y],
                    [-a4.x,-a4.y,-1,0,0,0, a4.x*b4.x, a4.y*b4.x, b4.x],
                    [0,0,0,-a4.x,-a4.y,-1, a4.x*b4.y, a4.y*b4.y, b4.y],
                    [0,0,0,0,0,0,0,0,1]
                    ])

        b = np.array([0,0,0,0,0,0,0,0,1])

        # (A^T * A)^-1
        C = np.linalg.inv(np.matmul(np.transpose(A),A))
        # (A^T * A)^-1 * A^T
        C = np.matmul(C,np.transpose(A))
        self.H = np.matmul(C,b)

        self.H = np.reshape(self.H,(3,3))
        print("Points Added")
        print("H mat calculated:\n", self.H)

    def transform_point(self,p: Point):
        if (self.H is not None):
            x = np.mat([p.x,p.y,1]).reshape((3,1))
            x = np.matmul(self.H,x)
            ret = x/x[2]
            return ret # np array size (3,1)

        else:
            print("Error: H matrix not generated")
            exit(1)

    def load_image(self,path: str):
        '''
        load image to numpy array from path
        '''
        self.img = cv2.imread(path)
        self.img = cv2.resize(self.img, (800, 800), interpolation = cv2.INTER_AREA)


    def transform_image(self,scale=4):
        # function timer
        start = time.time()

        # factor that image is downscaled for pixel compression (due to loss in transformation)
        SCALE_FACTOR = scale

        if (self.img is None):
            print("Error: img not loaded in, load first then transform")
            return
        else:
            print("Starting Transform")

        # make new image
        self.img_transform = np.zeros(self.img.shape, np.uint8)

        # do transform
        for i in range(self.img.shape[0]): # assuming i is row

            print(int((i/self.img.shape[0])*100),"%", end='\r')

            for j in range(self.img.shape[1]): # assuming i is col
                tp = self.transform_point(Point(j,i))


                if (tp[0] < 0 or tp[0] >= self.img.shape[0] or tp[1] < 0 or tp[1] >= self.img.shape[1]):
                    continue
                #print("TP: ", int(tp[0]),int(tp[1]))
                #print("I: ", i, " J:",j)

                self.img_transform[int(tp[0])//SCALE_FACTOR][int(tp[1])//SCALE_FACTOR] = self.img[i][j]

        # crop image based on scale factor diff
        self.img_transform = self.img_transform[0:self.img.shape[0]//SCALE_FACTOR, 0:self.img.shape[1]//SCALE_FACTOR]

        # remove noise

        # for every black pixel in image set to pixel above it (simple de-noise)
        for i in range(self.img_transform.shape[0]):
            for j in range(self.img_transform.shape[1]):
                if sum(self.img_transform[i][j]) == 0:
                    if i > 0:
                        self.img_transform[i][j] = self.img_transform[i-1][j]


        end = time.time()
        print("\nTransform Time:",(end-start), "seconds")



    def display_image(self):
        plt.imshow(self.img)
        plt.show()

    def display_transform(self):

        cv2.imshow('Transformed Image', self.img_transform)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def debug_H(self):
        '''
        used to test different H matrices
        '''
        self.H = np.mat([
                        [0.1,0.1,0.1],
                        [1,0.1,0.1],
                        [0.1,0.1,100]
                        ])















