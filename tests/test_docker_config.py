import os
import pytest

def test_docker_compose_structure():
    compose_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docker-compose.yml"))
    assert os.path.exists(compose_path)
    with open(compose_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "services:" in content
        assert "db:" in content
        assert "backend:" in content
        assert "frontend:" in content
        assert "redis:" in content

def test_dockerfiles_exist():
    backend_df = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docker", "Dockerfile.backend"))
    frontend_df = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docker", "Dockerfile.frontend"))
    assert os.path.exists(backend_df)
    assert os.path.exists(frontend_df)

def test_env_example_template():
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env.example"))
    assert os.path.exists(env_path)
    with open(env_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "POSTGRES_DB=" in content
        assert "SECRET_KEY=" in content
