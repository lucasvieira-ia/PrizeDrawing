import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "create_site.py"


def load_module(monkeypatch, tmp_path):
    csv_file = tmp_path / "lotofacil.csv"
    csv_file.write_text(
        "Concurso,Data Sorteio,Bola1,Bola2,Bola3,Bola4,Bola5,Bola6,Bola7,Bola8,Bola9,Bola10,Bola11,Bola12,Bola13,Bola14,Bola15\n"
        "101,10/01/2025,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15\n"
        "102,20/02/2026,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    spec = importlib.util.spec_from_file_location("create_site_test_module", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_process_total_data_filters_only_2026_rows(monkeypatch, tmp_path):
    module = load_module(monkeypatch, tmp_path)

    payload = json.loads(module.process_total_data())

    assert len(payload) == 1
    assert payload[0]["id"] == 102
    assert payload[0]["date"] == "20/02/2026"
    assert payload[0]["numbers"] == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    assert payload[0]["evens"] == 7
    assert payload[0]["odds"] == 8
