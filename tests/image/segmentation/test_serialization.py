import pytest
import torch

from flash.core.data.data_source import DefaultDataKeys
from flash.core.utilities.imports import _FIFTYONE_AVAILABLE
from flash.image.segmentation.serialization import FiftyOneSegmentationLabels, SegmentationLabels


class TestSemanticSegmentationLabels:

    def test_smoke(self):
        serial = SegmentationLabels()
        assert serial is not None
        assert serial.labels_map is None
        assert serial.visualize is False

    def test_exception(self):
        serial = SegmentationLabels()

        with pytest.raises(Exception):
            sample = torch.zeros(1, 5, 2, 3)
            serial.serialize(sample)

        with pytest.raises(Exception):
            sample = torch.zeros(2, 3)
            serial.serialize(sample)

    def test_serialize(self):
        serial = SegmentationLabels()

        sample = torch.zeros(5, 2, 3)
        sample[1, 1, 2] = 1  # add peak in class 2
        sample[3, 0, 1] = 1  # add peak in class 4

        classes = serial.serialize({DefaultDataKeys.PREDS: sample})
        assert classes[1, 2] == 1
        assert classes[0, 1] == 3

    @pytest.mark.skipif(not _FIFTYONE_AVAILABLE, reason="fiftyone is not installed for testing")
    def test_serialize_fiftyone(self):
        serial = FiftyOneSegmentationLabels()

        sample = torch.zeros(5, 2, 3)
        sample[1, 1, 2] = 1  # add peak in class 2
        sample[3, 0, 1] = 1  # add peak in class 4

        segmentation = serial.serialize({DefaultDataKeys.PREDS: sample})
        assert segmentation.mask[1, 2] == 1
        assert segmentation.mask[0, 1] == 3

    # TODO: implement me
    def test_create_random_labels(self):
        pass

    # TODO: implement me
    def test_labels_to_image(self):
        pass
