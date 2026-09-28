from backend.app.conversations.service import ConversationService


def test_conversation_append_and_clear() -> None:
    service = ConversationService()
    service.append("session-1", "user", "hello")
    service.append("session-1", "assistant", "hi")

    conversation = service.get("session-1")
    assert [message.role for message in conversation.messages] == ["user", "assistant"]
    assert conversation.messages[0].content == "hello"

    service.clear("session-1")
    assert service.get("session-1").messages == []
