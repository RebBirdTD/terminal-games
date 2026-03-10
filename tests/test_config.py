from terminal_garden.config import PLANT_TYPES, Stage

def test_plant_types_exist():
    assert "grass" in PLANT_TYPES
    assert "rose" in PLANT_TYPES
    assert "tulip" in PLANT_TYPES
    assert "sunflower" in PLANT_TYPES
    assert "tree" in PLANT_TYPES

def test_plant_has_required_fields():
    for name, pt in PLANT_TYPES.items():
        assert "stages" in pt, f"{name} missing stages"
        assert "colors" in pt, f"{name} missing colors"
        assert len(pt["stages"]) == 4, f"{name} should have 4 stages"

def test_stages_enum():
    assert Stage.SEED.value == 0
    assert Stage.SPROUT.value == 1
    assert Stage.BLOOM.value == 2
    assert Stage.WILT.value == 3

def test_stage_has_template_and_duration():
    for name, pt in PLANT_TYPES.items():
        for stage_info in pt["stages"]:
            assert "template" in stage_info, f"{name} stage missing template"
            assert "duration" in stage_info, f"{name} stage missing duration"
            assert isinstance(stage_info["template"], list), f"{name} template should be list of strings"
