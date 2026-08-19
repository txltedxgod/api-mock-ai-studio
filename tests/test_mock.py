from mock_ai.generator import APIMockGenerator

def test_mock_gen():
    g = APIMockGenerator()
    res = g.generate_mock_for_schema("UserProfile")
    assert "mock_data" in res
