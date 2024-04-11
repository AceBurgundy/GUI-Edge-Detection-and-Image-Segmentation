from cv2 import cvtColor, COLOR_BGR2GRAY, blur, Sobel, CV_64F, magnitude, normalize, NORM_MINMAX, Canny, threshold, COLOR_GRAY2BGR, TERM_CRITERIA_EPS, TERM_CRITERIA_MAX_ITER, kmeans, KMEANS_RANDOM_CENTERS, COLOR_BGR2RGB
from numpy import ndarray, float32, uint8, clip
from cv2.typing import MatLike
from typing import Tuple

def grayscale(image: ndarray, level: float = 1.0) -> MatLike:
    """
    Converts the given image to grayscale.

    Arguments:
    ----------
        image (numpy.ndarray): The input image in BGR color format.
        level (float): Level of greyness. A value of 1.0 maintains the original grayscale conversion,
                       while values less than 1.0 result in a darker grayscale image.

    Returns:
    --------
        numpy.ndarray: The grayscaled image.
    """
    gray_image: MatLike = cvtColor(image, COLOR_BGR2GRAY)
    adjusted_gray: ndarray = gray_image.astype(float) * level
    adjusted_gray: ndarray = clip(adjusted_gray, 0, 255).astype(uint8)  # Clip values and convert back to uint8
    return cvtColor(adjusted_gray, COLOR_GRAY2BGR)

def box_blur(image: ndarray, kluster_matrix: Tuple[int, int] = (50, 50)) -> MatLike:
    """
    Applies a box blur filter to the given image.

    Arguments:
    ----------
        image (numpy.ndarray): The input image.

    Returns:
    --------
        numpy.ndarray: The image with box blur applied.
    """
    image_rgb: MatLike = cvtColor(image, COLOR_BGR2RGB)
    blurred_image: MatLike = blur(image_rgb, kluster_matrix)

    return blurred_image

def sobel_edge_detection(image: ndarray, ksize: int = 3, scale: int = 1, delta: int = 0) -> ndarray:
    """
    Applies Sobel edge detection to the given image.

    Arguments:
    ----------
        image (numpy.ndarray): The input image.
        ksize (int): Aperture size for the Sobel kernel. Default is 3.
        scale (int): Optional scale factor for the computed derivative values. Default is 1.
        delta (int): Optional delta value that is added to the results prior to storing them. Default is 0.

    Returns:
    --------
        numpy.ndarray: The image with Sobel edge detection applied.
    """
    gray: ndarray = cvtColor(image, COLOR_BGR2GRAY)
    sobel_x: ndarray = Sobel(gray, CV_64F, 1, 0, ksize=ksize, scale=scale, delta=delta)
    sobel_y: ndarray = Sobel(gray, CV_64F, 0, 1, ksize=ksize, scale=scale, delta=delta)
    magnitude_image: ndarray = magnitude(sobel_x, sobel_y)
    magnitude_image = normalize(magnitude_image, None, 0, 255, NORM_MINMAX).astype('uint8') # type: ignore
    return cvtColor(magnitude_image, COLOR_GRAY2BGR)

def canny_edge_detection(image: ndarray, threshold_one: int = 50, threshold_two: int = 150) -> ndarray:
    """
    Applies Canny edge detection to the given image.

    Arguments:
    ----------
        image (numpy.ndarray): The input image.
        threshold_one (int): The first threshold for the hysteresis procedure in Canny. Default is 50.
        threshold_two (int): The second threshold for the hysteresis procedure in Canny. Default is 150.

    Returns:
    --------
        numpy.ndarray: The image with Canny edge detection applied.
    """
    gray: ndarray = cvtColor(image, COLOR_BGR2GRAY)
    return Canny(gray, threshold_one, threshold_two)

def global_segmentation(image: ndarray, thresh: int = 127) -> MatLike:
    """
    Performs global segmentation on the given image.

    Arguments:
    ----------
        image (numpy.ndarray): The input image.

    Returns:
    --------
        numpy.ndarray: The segmented image.
    """
    gray: MatLike = cvtColor(image, COLOR_BGR2GRAY)
    _, segmented_image = threshold(gray, thresh, 255, 0)
    return cvtColor(segmented_image, COLOR_GRAY2BGR)

def kmeans_segmentation(image: ndarray, kluster_count: int = 2) -> ndarray:
    """
    Performs segmentation using K-means clustering on the given image.

    Arguments:
    ----------
        image (numpy.ndarray): The input image.

    Returns:
    --------
        numpy.ndarray: The segmented image.
    """
    z: ndarray = image.reshape((-1, 3)).astype(float32)
    criteria: Tuple[float, int, float] = (TERM_CRITERIA_EPS + TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, (centers) = kmeans(z, 2 if kluster_count > 5 else kluster_count, None, criteria, 10, KMEANS_RANDOM_CENTERS) # type: ignore

    centers = uint8(centers)
    segmented_image = centers[labels.flatten()] # type: ignore
    return segmented_image.reshape((image.shape))
