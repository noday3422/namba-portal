import chainer
import chainer.links as L
import chainer.functions as F

class CNN(chainer.Chain):

    def __init__(self, n_mid=200, n_out=2):
        super().__init__()
        with self.init_scope():
            self.conv1 = L.Convolution2D(in_channels=3, out_channels=32, ksize=3, stride=1,pad=1)
            self.conv2 = L.Convolution2D(in_channels=32, out_channels=64, ksize=3, stride=1,pad=1)
            self.fc1 = L.Linear(None, n_mid)
            self.fc2 = L.Linear(None, n_out)
            self.bn = L.BatchNormalization(3)

    def __call__(self, x):
        h = self.bn(x)
        h = F.relu(self.conv1(h))
        h = F.relu(self.conv2(h))
        h = F.max_pooling_2d(h, ksize=3, stride=3)
        h = F.relu(self.fc1(h))
        h = self.fc2(h)
        return h
