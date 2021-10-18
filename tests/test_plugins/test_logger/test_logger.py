import pytest
from loguru._defaults import LOGURU_FORMAT

from asyncbox.plugins.logger.plugin import LoguruPlugin as Plugin
from asyncbox.settings import BaseAppSettings


@pytest.mark.asyncio
async def test_custom_formatter():
    plugin = Plugin(BaseAppSettings(), None, None)
    await plugin.on_startup()
    record_dict = {"extra": {}}
    assert plugin.format_record(record_dict) == LOGURU_FORMAT + "{exception}\n"

    record_dict = {"extra": {"payload": {}}}
    assert "extra[payload]" in plugin.format_record(record_dict)

    incoming_request = {
        "method": "POST",
        "url": "https://cts.ccsteam.ru/api/v3/botx/command/callback",
        "headers": {
            "Content-Type": "application/json",
            "Authorization": "Bearer token",
        },
        "query_params": {},
        "request_data": '{"sync_id": "uuid", "recipients": "all", "command_result": {"status": "ok", "body": "", "metadata": {}, "keyboard": [], "bubble": [], "mentions": []}, "file": {"file_name": "d.txt", "data": "data:text/plain;base64, foobar'
        '="}, "opts": {"stealth_mode": false, "notification_opts": {"send": true, "force_dnd": false}}}'.replace(
            "foobar", "foobar" * plugin.max_file_length * 2
        ),
    }
    plugin.format_botx_client_payload(incoming_request)
    file_data = incoming_request["request_data"]["file"]["data"]
    assert file_data.rfind("foobar" * plugin.max_file_length) == file_data.find(
        "foobar" * plugin.max_file_length
    )
    await plugin.on_shutdown()
