import pytest
from PIL import Image
from cv_handler import CVInspectionHandler


@pytest.fixture
def sample_image(tmp_path):
    img_path = tmp_path / "test_site.jpg"
    img = Image.new("RGB", (320, 240), color=(100, 150, 200))
    img.save(img_path)
    return str(img_path)


def test_cv_analysis(sample_image):
    cv = CVInspectionHandler()
    res = cv.analyze_image(sample_image)
    assert "completeness_score" in res
    assert "structural_risk_score" in res
    assert "cv_site_delay_factor" in res
    assert isinstance(res["detected_anomalies"], list)
