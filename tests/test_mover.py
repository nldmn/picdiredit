import tempfile
from pathlib import Path
from picdiredit.mover import move_files_from_csv


def test_move_files(tmp_path):
    # create source files
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    f1 = src_dir / "a.txt"
    f2 = src_dir / "b.txt"
    f1.write_text("one")
    f2.write_text("two")

    # write csv
    csv_file = tmp_path / "files.csv"
    csv_file.write_text(f"{f1}\n{f2}\n")

    dest = tmp_path / "dest"

    moved, errors = move_files_from_csv(str(csv_file), str(dest))
    assert moved == 2
    assert not errors
    assert not f1.exists()
    assert not f2.exists()
    assert (dest / "a.txt").exists()
    assert (dest / "b.txt").exists()


def test_dry_run(tmp_path):
    src_dir = tmp_path / "src2"
    src_dir.mkdir()
    f1 = src_dir / "c.txt"
    f1.write_text("c")
    csv_file = tmp_path / "files2.csv"
    csv_file.write_text(f"{f1}\n")
    dest = tmp_path / "dest2"
    moved, errors = move_files_from_csv(str(csv_file), str(dest), dry_run=True)
    assert moved == 1
    assert not errors
    assert f1.exists()
    assert not dest.exists()
