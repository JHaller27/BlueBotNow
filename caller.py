from utils.logging import Logger
from utils.tools import read_env

import requests

from picarto.models.channelDetails import ChannelDetails


class CallerError(RuntimeError):
    def __init__(self, response: requests.models.Response, *args: object) -> None:
        super().__init__(str(response))
        self._response = response

    @property
    def status_code(self) -> int:
        return self._response.status_code

    @property
    def text(self) -> str:
        return self._response.text

    @property
    def ux_message(self) -> str:
        return f"Failed call: {self.status_code}"

    @property
    def full_message(self) -> str:
        text = 'Requires capta' if 'meta name="captcha-bypass"' in self.text else self.text

        return f"Failed call with code: {self.status_code}.\n" + text


def get_channel_data(channel_name: str, logger: Logger) -> ChannelDetails:
    host = read_env('PICARTO_HOST', 'https://api.picarto.tv/api/v1', logger=logger)

    uri = f"{host}/channel/name/{channel_name}"
    headers = {
        "User-Agent": "PTV-BOT-BlueBotNow"
    }

    response = requests.get(uri, headers=headers)

    if response.status_code != 200:
        raise CallerError(response)

    data = response.json()
    details = ChannelDetails.parse_obj(data)

    return details
