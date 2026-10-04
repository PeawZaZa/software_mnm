# test_deployment.py
# Smoke Tests + การตั้งค่าผ่าน Environment (สัปดาห์ที่ 13 — Deployment Readiness)
# ════════════════════════════════════════
# รันเฉพาะ smoke (เร็ว < 1 วินาที — ใช้ตรวจหลังติดตั้งบนเครื่องใหม่):
#     pytest -m smoke -v
# รันทั้งหมด:
#     pytest -v

import builtins
import json
import os
from pathlib import Path

import pytest

import app_v2
from app_v2 import (
    ConsoleUI,
    InventoryRepository,
    InventoryService,
    Settings,
    load_env_file,
)


@pytest.fixture
def clean_env(monkeypatch):
    """ล้างตัวแปรของระบบออกก่อน เพื่อไม่ให้ค่าบนเครื่องผู้รันปนเข้ามา"""
    for key in ("INVENTORY_DB_PATH", "REPORT_EXPORT_DIR"):
        monkeypatch.delenv(key, raising=False)
    return monkeypatch


def run_main(monkeypatch, keys):
    """เรียก main() จริง โดยป้อนปุ่มแทนคีย์บอร์ด และเก็บข้อความที่พิมพ์ออกหน้าจอ"""
    queue, screen = list(keys), []
    monkeypatch.setattr(builtins, "input", lambda prompt="": queue.pop(0))
    monkeypatch.setattr(builtins, "print", lambda *a, **k: screen.append(" ".join(map(str, a))))
    app_v2.main()
    return "\n".join(screen)


# ══════════════════════════════════════════════════
# Smoke Tests — "ระบบเปิดติดไหม ข้อมูลโหลดขึ้นไหม หน้าจอหลักไม่ crash ใช่ไหม"
# ══════════════════════════════════════════════════

@pytest.mark.smoke
def test_system_boots_and_loads_database(tmp_path):
    """ระบบเริ่มต้นและอ่านไฟล์ข้อมูลได้โดยไม่ crash"""
    db_file = tmp_path / "smoke_db.json"
    db_file.write_text(json.dumps({"P01": {"n": "Milk", "q": 10, "p": 20.0, "c": "Dairy"}}))
    service = InventoryService(InventoryRepository(db_file))
    assert service.inventory is not None
    assert "P01" in service.inventory
    assert service.inventory["P01"].name == "Milk"


@pytest.mark.smoke
def test_main_menu_opens_and_exits(tmp_path, clean_env):
    clean_env.chdir(tmp_path)
    screen = run_main(clean_env, ["5"])
    assert "=== INVENTORY SYSTEM v2.0 ===" in screen
    assert "7. Export CSV" in screen
    assert "Bye" in screen


@pytest.mark.smoke
def test_new_features_work_after_install(tmp_path, clean_env):
    """Sanity check ฟีเจอร์ที่เพิ่งบำรุงรักษา: Barcode · Reorder alert · CSV ลงโฟลเดอร์ exports/"""
    clean_env.chdir(tmp_path)
    clean_env.setenv("REPORT_EXPORT_DIR", "exports")
    screen = run_main(clean_env, [
        "2", "P1", "Milk", "10", "20", "Dairy", "885123456789", "5",
        "3", "P1", "6",
        "7", "smoke.csv",
        "5",
    ])
    assert "REORDER POINT REACHED" in screen
    assert (tmp_path / "exports" / "smoke.csv").is_file()


# ══════════════════════════════════════════════════
# Config Externalization — .env และ Settings
# ══════════════════════════════════════════════════

class TestLoadEnvFile:

    def test_missing_file_is_fine(self, tmp_path):
        assert load_env_file(tmp_path / "nope.env") == {}

    def test_reads_values_and_skips_comments(self, tmp_path, clean_env):
        env = tmp_path / ".env"
        env.write_text('# comment\n\nINVENTORY_DB_PATH="data/inv.json"\nNOT A PAIR\n'
                       "REPORT_EXPORT_DIR = exports/\n", encoding="utf-8")
        loaded = load_env_file(env)
        assert loaded == {"INVENTORY_DB_PATH": "data/inv.json", "REPORT_EXPORT_DIR": "exports/"}
        assert os.environ["INVENTORY_DB_PATH"] == "data/inv.json"

    def test_does_not_override_existing_environment(self, tmp_path, clean_env):
        clean_env.setenv("INVENTORY_DB_PATH", "from-shell.json")
        env = tmp_path / ".env"
        env.write_text("INVENTORY_DB_PATH=from-file.json\n", encoding="utf-8")
        assert load_env_file(env) == {}
        assert os.environ["INVENTORY_DB_PATH"] == "from-shell.json"


class TestSettings:

    def test_defaults_keep_v2_behaviour(self):
        """ไม่ตั้งค่าอะไรเลย = ทำงานแบบเดิมทุกประการ (data.json ในโฟลเดอร์ที่สั่งรัน)"""
        settings = Settings.from_env({})
        assert settings.db_path == Path("data.json")
        assert settings.export_dir is None

    def test_reads_environment(self):
        settings = Settings.from_env({"INVENTORY_DB_PATH": "data/inv.json",
                                      "REPORT_EXPORT_DIR": "exports"})
        assert settings.db_path == Path("data/inv.json")
        assert settings.export_dir == Path("exports")

    def test_prepare_directories_creates_missing_folders(self, tmp_path):
        settings = Settings(tmp_path / "data" / "inv.json", tmp_path / "exports")
        settings.prepare_directories()
        assert (tmp_path / "data").is_dir()
        assert (tmp_path / "exports").is_dir()

    def test_main_uses_env_file_in_working_directory(self, tmp_path, clean_env):
        clean_env.chdir(tmp_path)
        (tmp_path / ".env").write_text("INVENTORY_DB_PATH=data/inventory_db.json\n",
                                       encoding="utf-8")
        run_main(clean_env, ["2", "P9", "Tea", "3", "5", "Drink", "", "0", "5"])
        saved = json.loads((tmp_path / "data" / "inventory_db.json").read_text(encoding="utf-8"))
        assert "P9" in saved


class TestExportPath:

    @pytest.fixture
    def service(self, tmp_path):
        return InventoryService(InventoryRepository(tmp_path / "db.json"))

    def test_bare_filename_goes_to_export_dir(self, service, tmp_path):
        ui = ConsoleUI(service, export_dir=tmp_path / "exports")
        assert ui.export_path("report.csv") == tmp_path / "exports" / "report.csv"

    def test_path_with_folder_is_used_as_typed(self, service, tmp_path):
        ui = ConsoleUI(service, export_dir=tmp_path / "exports")
        typed = str(tmp_path / "elsewhere" / "r.csv")
        assert ui.export_path(typed) == Path(typed)

    def test_without_export_dir_behaves_like_v2(self, service):
        assert ConsoleUI(service).export_path("report.csv") == Path("report.csv")
