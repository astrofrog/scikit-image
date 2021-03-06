import itertools as it
import warnings
import numpy as np
from numpy.testing import assert_equal, assert_array_equal
from skimage.segmentation import slic


def test_color_2d():
    rnd = np.random.RandomState(0)
    img = np.zeros((20, 21, 3))
    img[:10, :10, 0] = 1
    img[10:, :10, 1] = 1
    img[10:, 10:, 2] = 1
    img += 0.01 * rnd.normal(size=img.shape)
    img[img > 1] = 1
    img[img < 0] = 0
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        seg = slic(img, n_segments=4, sigma=0)

    # we expect 4 segments
    assert_equal(len(np.unique(seg)), 4)
    assert_equal(seg.shape, img.shape[:-1])
    assert_array_equal(seg[:10, :10], 0)
    assert_array_equal(seg[10:, :10], 2)
    assert_array_equal(seg[:10, 10:], 1)
    assert_array_equal(seg[10:, 10:], 3)


def test_gray_2d():
    rnd = np.random.RandomState(0)
    img = np.zeros((20, 21))
    img[:10, :10] = 0.33
    img[10:, :10] = 0.67
    img[10:, 10:] = 1.00
    img += 0.0033 * rnd.normal(size=img.shape)
    img[img > 1] = 1
    img[img < 0] = 0
    seg = slic(img, sigma=0, n_segments=4, compactness=1,
               multichannel=False, convert2lab=False)

    assert_equal(len(np.unique(seg)), 4)
    assert_equal(seg.shape, img.shape)
    assert_array_equal(seg[:10, :10], 0)
    assert_array_equal(seg[10:, :10], 2)
    assert_array_equal(seg[:10, 10:], 1)
    assert_array_equal(seg[10:, 10:], 3)


def test_color_3d():
    rnd = np.random.RandomState(0)
    img = np.zeros((20, 21, 22, 3))
    slices = []
    for dim_size in img.shape[:-1]:
        midpoint = dim_size // 2
        slices.append((slice(None, midpoint), slice(midpoint, None)))
    slices = list(it.product(*slices))
    colors = list(it.product(*(([0, 1],) * 3)))
    for s, c in zip(slices, colors):
        img[s] = c
    img += 0.01 * rnd.normal(size=img.shape)
    img[img > 1] = 1
    img[img < 0] = 0
    seg = slic(img, sigma=0, n_segments=8)

    assert_equal(len(np.unique(seg)), 8)
    for s, c in zip(slices, range(8)):
        assert_array_equal(seg[s], c)


def test_gray_3d():
    rnd = np.random.RandomState(0)
    img = np.zeros((20, 21, 22))
    slices = []
    for dim_size in img.shape:
        midpoint = dim_size // 2
        slices.append((slice(None, midpoint), slice(midpoint, None)))
    slices = list(it.product(*slices))
    shades = np.arange(0, 1.000001, 1.0/7)
    for s, sh in zip(slices, shades):
        img[s] = sh
    img += 0.001 * rnd.normal(size=img.shape)
    img[img > 1] = 1
    img[img < 0] = 0
    seg = slic(img, sigma=0, n_segments=8, compactness=1,
               multichannel=False, convert2lab=False)

    assert_equal(len(np.unique(seg)), 8)
    for s, c in zip(slices, range(8)):
        assert_array_equal(seg[s], c)


def test_list_sigma():
    rnd = np.random.RandomState(0)
    img = np.array([[1, 1, 1, 0, 0, 0],
                    [0, 0, 0, 1, 1, 1]], np.float)
    img += 0.1 * rnd.normal(size=img.shape)
    result_sigma = np.array([[0, 0, 0, 1, 1, 1],
                             [0, 0, 0, 1, 1, 1]], np.int)
    seg_sigma = slic(img, n_segments=2, sigma=[1, 50, 1], multichannel=False)
    assert_equal(seg_sigma, result_sigma)


def test_spacing():
    rnd = np.random.RandomState(0)
    img = np.array([[1, 1, 1, 0, 0],
                    [1, 1, 0, 0, 0]], np.float)
    result_non_spaced = np.array([[0, 0, 0, 1, 1],
                                  [0, 0, 1, 1, 1]], np.int)
    result_spaced = np.array([[0, 0, 0, 0, 0],
                              [1, 1, 1, 1, 1]], np.int)
    img += 0.1 * rnd.normal(size=img.shape)
    seg_non_spaced = slic(img, n_segments=2, sigma=0, multichannel=False,
                          compactness=1.0)
    seg_spaced = slic(img, n_segments=2, sigma=0, spacing=[1, 500, 1],
                      compactness=1.0, multichannel=False)
    assert_equal(seg_non_spaced, result_non_spaced)
    assert_equal(seg_spaced, result_spaced)



if __name__ == '__main__':
    from numpy import testing
    testing.run_module_suite()
