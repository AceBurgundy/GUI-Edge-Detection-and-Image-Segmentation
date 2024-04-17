from filters import GrayscaleConverter, BoxBlurFilter, SobelEdgeDetector, CannyEdgeDetector, GlobalSegmentation, KMeansSegmentation
from typing import Optional, Type, TypeAlias

IMAGE_FILTER_TYPES: TypeAlias =  Optional[Type[GrayscaleConverter]|Type[BoxBlurFilter]|Type[SobelEdgeDetector]|Type[CannyEdgeDetector]|Type[GlobalSegmentation]|Type[KMeansSegmentation]]
IMAGE_FILTERS: TypeAlias = GrayscaleConverter|BoxBlurFilter|SobelEdgeDetector|CannyEdgeDetector|GlobalSegmentation|KMeansSegmentation
