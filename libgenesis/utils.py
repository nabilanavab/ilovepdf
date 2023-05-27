import re
from urllib.parse import unquote_plus


class Util:
    @staticmethod
    async def get_filename(con_disp: str) -> str:

        fname = re.findall("filename\*=([^;]+)", con_disp, flags=re.IGNORECASE)
        if not fname:
            fname = re.findall(
                "filename=([^;]+)", con_disp, flags=re.IGNORECASE)
        if "utf-8''" in fname[0].lower():
            fname = re.sub("utf-8''", '', fname[0], flags=re.IGNORECASE)
            fname = unquote_plus(fname)
        else:
            fname = fname[0]
        return fname.strip().strip('"')

    @staticmethod
    async def filter_result(result: dict,
                            filters: dict) -> bool:

        outcome = True
        for key in filters:
            if not filters[key] in result[key]:
                outcome = False
        return outcome

    @staticmethod
    async def raise_error(status_code: int,
                          resp: str) -> None:

        raise ConnectionError(
            f'{status_code}: {resp}')
