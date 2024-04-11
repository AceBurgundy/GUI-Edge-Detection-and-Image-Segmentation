from cv2 import cvtColor, COLOR_BGR2GRAY, blur, Sobel, CV_64F, magnitude, normalize, NORM_MINMAX, Canny, threshold, COLOR_GRAY2BGR, TERM_CRITERIA_EPS, TERM_CRITERIA_MAX_ITER, kmeans, KMEANS_RANDOM_CENTERS, COLOR_BGR2RGB
from numpy import ndarray, float32, uint8, clip
from typing import Literal, Tuple
from cv2.typing import MatLike
from abc import ABC

class PropertyTypeManager(ABC):
    """
    Abstract class that manages the properties and their types
    """
    def __init__(self) -> None:
        self.property_data = {}

    def add_property(self, name: str, data_type: str, min: int|float = 0, max: int|float = 200) -> None:
        """
        Adds new property data to self.property_data

        Arguments:
        ----------
            name (str): The name of the property
            data_type (str): The declared data type of the property
            min (float|int): The minimum value allowed for the property
            max (float|int): The maximum value allowed for the property
        """
        self.property_data[name] = {
            "data_type": data_type,
            "min": min,
            "max": max
        }

class GrayscaleConverter(PropertyTypeManager):
    """
    Class representing a greyscale converter
    """
    def __init__(self, level: float = 1.0):
        """
        Initializes the greyscale converter class.

        level (float): Level of greyness. A value of 1.0 maintains the original grayscale conversion,
                        while values less than 1.0 result in a darker grayscale image.
        """
        super().__init__()
        self.__level: float = level
        self.add_property("level", float.__name__, 0.0, 1.0)

    @property
    def level(self) -> float:
        """
        level (float): the level of greyness.
        """
        return self.__level

    @level.setter
    def level(self, new_level: float) -> None:
        """
        Arguments:
        ----------
            new_level (float): The new level of greyness value.
        """
        self.__level = float(new_level)

    def apply(self, image: ndarray) -> MatLike:
        """
        Apply the grayscale filter to the image.

        Arguments:
        ----------
            image (numpy.ndarray): The input image in BGR color format.

        Returns:
        --------
            MatLike: The grayscaled image.
        """
        gray_image: MatLike = cvtColor(image, COLOR_BGR2GRAY)
        adjusted_gray: ndarray = gray_image.astype(float) * self.__level
        adjusted_gray: ndarray = clip(adjusted_gray, 0, 255).astype(uint8)  # Clip values and convert back to uint8
        return cvtColor(adjusted_gray, COLOR_GRAY2BGR)

class BoxBlurFilter(PropertyTypeManager):
    """
    Class for applying a box blur filter to images.

    Attributes:
        matrix_x (int): The matrix x size of the blur filter.
        matrix_y (int): The matrix y size of the blur filter.
    """
    def __init__(self, matrix_x: int = 50, matrix_y: int = 50):
        """
        Initializes the BoxBlurFilter class.

        Args:
            kluster_matrix (Tuple[int, int], optional): The matrix size of the blur filter. Defaults to (50, 50).
        """
        super().__init__()
        self.__matrix_x: int = matrix_x
        self.__matrix_y: int = matrix_y
        self.add_property("matrix_x", int.__name__, 25, 100)
        self.add_property("matrix_y", int.__name__, 25, 100)

    @property
    def matrix_x(self):
        """
        matrix_x (int): the matrix_x for the kluster matrix.
        """
        return self.__matrix_x

    @matrix_x.setter
    def matrix_x(self, matrix_x: int):
        """
        Arguments:
        ----------
            matrix_x (int): The new matrix_x of the kluster matrix (x, y).
        """
        self.__matrix_x = int(matrix_x)

    @property
    def matrix_y(self):
        """
        matrix_y (int): the matrix_y for the kluster matrix.
        """
        return self.__matrix_y

    @matrix_y.setter
    def matrix_y(self, matrix_y: int):
        """
        Arguments:
        ----------
            matrix_y (int): The new matrix_y of the kluster matrix (x, y).
        """
        self.__matrix_y = int(matrix_y)

    def apply(self, image: ndarray) -> MatLike:
        """
        Applies a box blur filter to the given image.

        Args:
            image (numpy.ndarray): The input image.

        Returns:
            MatLike: The image with box blur applied.
        """
        image_rgb: MatLike = cvtColor(image, COLOR_BGR2RGB)
        blurred_image: MatLike = blur(image_rgb, (self.matrix_x, self.matrix_y))
        return blurred_image

class SobelEdgeDetector(PropertyTypeManager):
    """
    Class for applying Sobel edge detection to images.

    Attributes:
        k_size (int): Aperture size for the Sobel kernel.
        scale (int): Optional scale factor for the computed derivative values.
        delta (int): Optional delta value that is added to the results prior to storing them.
    """
    def __init__(self, k_size: int = 3, scale: int = 1):
        """
        Initializes the SobelEdgeDetector class.

        Args:
            k_size (int, optional): Aperture size for the Sobel kernel. Defaults to 3.
            scale (int, optional): Optional scale factor for the computed derivative values. Defaults to 1.
        """
        super().__init__()
        self.__k_size: int = k_size
        self.__scale: int = scale
        self.add_property("k_size", int.__name__, 1, 3)
        self.add_property("scale", int.__name__, 1, 3)

    @property
    def k_size(self) -> int:
        """
        k_size (int): Aperture size for the Sobel kernel.
        """
        return self.__k_size

    @k_size.setter
    def k_size(self, new_k_size: int) -> None:
        """
        Arguments:
        ----------
            new_k_size (int): The new apperture size for the Sobel kernel.
        """
        self.__k_size = int(new_k_size)

    @property
    def scale(self) -> int:
        """
        scale (int): Scale factor for the computed derivative values.
        """
        return self.__scale

    @scale.setter
    def scale(self, new_scale: int) -> None:
        """
        Arguments:
        ----------
            new_scale (int): The new scale value.
        """
        self.__scale = int(new_scale)

    def apply(self, image: ndarray) -> MatLike:
        """
        Applies Sobel edge detection to the given image.

        Args:
            image (numpy.ndarray): The input image.

        Returns:
            MatLike: The image with Sobel edge detection applied.
        """
        gray: ndarray = cvtColor(image, COLOR_BGR2GRAY)
        sobel_x: ndarray = Sobel(gray, CV_64F, 1, 0, ksize=self.k_size, scale=self.scale, delta=0) # type: ignore
        sobel_y: ndarray = Sobel(gray, CV_64F, 0, 1, ksize=self.k_size, scale=self.scale, delta=0) # type: ignore
        magnitude_image: ndarray = magnitude(sobel_x, sobel_y).astype('uint8')
        magnitude_image = normalize(magnitude_image, None, 0, 255, NORM_MINMAX).astype('uint8') # type: ignore
        return cvtColor(magnitude_image, COLOR_GRAY2BGR)

class CannyEdgeDetector(PropertyTypeManager):
    """
    Class for applying Canny edge detection to images.

    Attributes:
        threshold_one (int): The first threshold for the hysteresis procedure in Canny.
        threshold_two (int): The second threshold for the hysteresis procedure in Canny.
    """
    def __init__(self, threshold_one: int = 50, threshold_two: int = 150):
        """
        Initializes the CannyEdgeDetector class.

        Args:
            threshold_one (int, optional): The first threshold for the hysteresis procedure in Canny. Defaults to 50.
            threshold_two (int, optional): The second threshold for the hysteresis procedure in Canny. Defaults to 150.
        """
        super().__init__()
        self.__threshold_one: int|Literal[50] = threshold_one
        self.__threshold_two: int|Literal[150] = threshold_two
        self.add_property("threshold_one", int.__name__, 0, 200)
        self.add_property("threshold_two", int.__name__, 0, 200)

    @property
    def threshold_one(self) -> int:
        """
        threshold_one (int): The first threshold for the hysteresis procedure in Canny.
        """
        return self.__threshold_one

    @threshold_one.setter
    def threshold_one(self, new_threshold_one: int) -> None:
        """
        Arguments:
        ----------
            new_threshold_one (int): A new value for the first threshold for the hysteresis procedure in Canny.
        """
        self.__threshold_one = int(new_threshold_one)

    @property
    def threshold_two(self) -> int:
        """
        threshold_one (int): The second threshold for the hysteresis procedure in Canny.
        """
        return self.__threshold_two

    @threshold_two.setter
    def threshold_two(self, new_threshold_two: int) -> None:
        """
        Arguments:
        ----------
            new_threshold_two (int): A new value for the second threshold for the hysteresis procedure in Canny.
        """
        self.__threshold_two = int(new_threshold_two)

    def apply(self, image: ndarray) -> MatLike:
        """
        Applies Canny edge detection to the given image.

        Args:
            image (numpy.ndarray): The input image.

        Returns:
            MatLike: The image with Canny edge detection applied.
        """
        gray: MatLike = cvtColor(image, COLOR_BGR2GRAY)
        return Canny(gray, self.__threshold_one, self.__threshold_two)

class GlobalSegmentation(PropertyTypeManager):
    """
    Class for performing global segmentation on images.

    Attributes:
        thresh (int): The threshold value for segmentation.
    """
    def __init__(self, thresh: int = 127):
        """
        Initializes the GlobalSegmentation class.

        Args:
            thresh (int, optional): The threshold value for segmentation. Defaults to 127.
        """
        super().__init__()
        self.__thresh = thresh
        self.add_property("thresh", int.__name__, 0, 150)

    @property
    def thresh(self) -> int:
        """
        thresh (int): The threshold value for segmentation.
        """
        return self.__thresh

    @thresh.setter
    def thresh(self, new_threshold: int) -> None:
        """
        Arguments:
        ----------
            new_threshold (int): The new threshold value for segmentation.
        """
        self.__thresh = int(new_threshold)

    def apply(self, image: ndarray) -> MatLike:
        """
        Performs global segmentation on the given image.

        Args:
            image (numpy.ndarray): The input image.

        Returns:
            MatLike: The segmented image.
        """
        gray: MatLike = cvtColor(image, COLOR_BGR2GRAY)
        _, segmented_image = threshold(gray, self.__thresh, 255, 0)
        return cvtColor(segmented_image, COLOR_GRAY2BGR)

class KMeansSegmentation(PropertyTypeManager):
    """
    Class for performing segmentation using K-means clustering on images.

    Attributes:
        kluster_count (int): The number of clusters for K-means clustering.
    """
    def __init__(self, kluster_count: int = 2):
        """
        Initializes the KMeansSegmentation class.

        Args:
            kluster_count (int, optional): The number of clusters for K-means clustering. Defaults to 2.
        """
        super().__init__()
        self.__kluster_count: int = kluster_count
        self.add_property("kluster_count", int.__name__, 0, 10)

    @property
    def kluster_count(self) -> int:
        """
        kluster_count (int): The number of clusters for K-means clustering.
        """
        return self.__kluster_count

    @kluster_count.setter
    def kluster_count(self, new_kluster_count: int) -> None:
        """
        Arguments:
        ----------
            new_kluster_count (int): The new number of clusters for K-means clustering.
        """
        self.__kluster_count = int(new_kluster_count)

    def apply(self, image: ndarray) -> ndarray:
        """
        Performs segmentation using K-means clustering on the given image.

        Args:
            image (numpy.ndarray): The input image.

        Returns:
            numpy.ndarray: The segmented image.
        """
        z: ndarray = image.reshape((-1, 3)).astype(float32)
        criteria: Tuple[float, int, float] = (TERM_CRITERIA_EPS + TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, labels, (centers) = kmeans(z, 2 if self.__kluster_count > 5 else self.__kluster_count, None, criteria, 10, KMEANS_RANDOM_CENTERS) # type: ignore

        centers = uint8(centers)
        segmented_image = centers[labels.flatten()] # type: ignore
        return segmented_image.reshape((image.shape))
