from aetheris_tl.client.buttons import ButtonMethods
from aetheris_tl.tl import types
from aetheris_tl.tl.custom.button import Button
from aetheris_tl.tl.custom.messagebutton import MessageButton


def test_callback_button_uses_layer230_wire_constructors_and_roundtrips():
    button = Button.inline("go", b"payload")
    markup = ButtonMethods.build_reply_markup(button)

    assert isinstance(button, types.KeyboardInlineButton)
    assert isinstance(button.type, types.InlineButtonTypeCallback)
    assert isinstance(markup.rows[0], types.KeyboardInlineButtonRow)
    raw = bytes(markup)
    assert raw[:4] == bytes.fromhex("7057b1b2")
    assert bytes(button)[:4] == bytes.fromhex("22a3c111")

    # Decode using the generated reader and registry, not just object fields.
    from aetheris_tl.extensions import BinaryReader
    decoded = types.ReplyInlineMarkup.from_reader(BinaryReader(raw[4:]))
    decoded_button = decoded.rows[0].buttons[0]
    assert decoded_button.text == "go"
    assert decoded_button.type.data == b"payload"


def test_message_button_reads_callback_data_from_layer230_shape():
    button = types.KeyboardInlineButton("go", types.InlineButtonTypeCallback(b"x"))
    wrapped = MessageButton(None, button, None, None, 1)
    assert wrapped.data == b"x"


def test_build_reply_markup_rejects_mixed_button_families():
    normal = Button.text("normal")
    inline = Button.inline("inline", b"x")
    try:
        ButtonMethods.build_reply_markup([normal, inline])
    except ValueError as exc:
        assert "mix inline" in str(exc)
    else:
        raise AssertionError("mixed button families must be rejected")
