from backend.app.memory.service import MemoryService


def test_store_replaces_same_key_and_retrieves() -> None:
    service = MemoryService()
    service.store("s1", "name", "Sweekar")
    service.store("s1", "name", "Sweekar M")

    records = service.retrieve("s1", "name")

    assert len(records) == 1
    assert records[0].value == "Sweekar M"


def test_sessions_are_isolated() -> None:
    service = MemoryService()
    service.store("s1", "project", "SoulOS")

    assert service.retrieve("s2", "project") == []


def test_clear_removes_session_memory() -> None:
    service = MemoryService()
    service.store("s1", "x", "value")
    service.clear("s1")

    assert service.retrieve("s1", "x") == []
