import shutil
import tempfile
from pathlib import Path

import app as app_module
from reportlab.pdfgen import canvas
from werkzeug.security import generate_password_hash


def main() -> None:
    test_dir = Path(tempfile.mkdtemp(prefix="firma_smoke_"))
    (test_dir / "uploads").mkdir(parents=True)
    (test_dir / "signed").mkdir(parents=True)

    app_module.DATA_DIR = test_dir
    app_module.UPLOAD_DIR = test_dir / "uploads"
    app_module.SIGNED_DIR = test_dir / "signed"
    app_module.DB_PATH = test_dir / "firma_digital.sqlite3"
    app_module.init_db()

    pdf_path = test_dir / "sample.pdf"
    c = canvas.Canvas(str(pdf_path))
    c.drawString(72, 720, "Documento de prueba")
    c.save()

    flask_app = app_module.app
    flask_app.config["TESTING"] = True
    client = flask_app.test_client()

    with flask_app.app_context():
        conn = app_module.db()
        role_id = conn.execute("SELECT id FROM roles WHERE name = 'Director'").fetchone()["id"]
        conn.execute(
            """
            INSERT INTO users(name, rut, recovery_email, internal_code, password_hash, role_id, can_download, can_print, created_at)
            VALUES (?, ?, ?, ?, ?, ?, 1, 1, ?)
            """,
            ("Director Prueba", "11111111-1", "director@example.com", "DIRTEST", generate_password_hash("Clave123!"), role_id, app_module.now()),
        )
        role_id = conn.execute("SELECT id FROM roles WHERE name = 'Secretario'").fetchone()["id"]
        conn.execute(
            """
            INSERT INTO users(name, rut, recovery_email, internal_code, password_hash, role_id, can_download, can_print, created_at)
            VALUES (?, ?, ?, ?, ?, ?, 1, 1, ?)
            """,
            ("Secretario Prueba", "22222222-2", "secretario@example.com", "SECTEST", generate_password_hash("Clave123!"), role_id, app_module.now()),
        )
        conn.commit()

    assert client.post("/login", data={"rut": app_module.DEFAULT_ADMIN_RUT, "password": app_module.DEFAULT_PASSWORD}).status_code in (302, 303)
    with pdf_path.open("rb") as fh:
        response = client.post(
            "/admin/upload",
            data={
                "title": "Acta smoke",
                "document_type_id": "1",
                "signers": ["2", "3"],
                "pdf": (fh, "sample.pdf"),
            },
            content_type="multipart/form-data",
            follow_redirects=False,
        )
    assert response.status_code in (302, 303)

    client.get("/logout")
    assert client.post("/login", data={"rut": "11111111-1", "password": "Clave123!"}).status_code in (302, 303)
    assert client.post("/documents/1/sign", data={"password": "Clave123!"}).status_code in (302, 303)
    client.get("/logout")
    assert client.post("/login", data={"rut": "22222222-2", "password": "Clave123!"}).status_code in (302, 303)
    assert client.post("/documents/1/sign", data={"password": "Clave123!"}).status_code in (302, 303)

    with flask_app.app_context():
        doc = app_module.db().execute("SELECT status, signed_path FROM documents WHERE id = 1").fetchone()
        assert doc["status"] == "pending"
        assert doc["signed_path"] is None

    client.get("/logout")
    assert client.post("/login", data={"rut": app_module.DEFAULT_ADMIN_RUT, "password": app_module.DEFAULT_PASSWORD}).status_code in (302, 303)
    assert client.post("/admin/documents/1/close").status_code in (302, 303)

    with flask_app.app_context():
        doc = app_module.db().execute("SELECT status, signed_path FROM documents WHERE id = 1").fetchone()
        assert doc["status"] == "closed"
        assert Path(doc["signed_path"]).exists()

    print("smoke test ok")
    shutil.rmtree(test_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
