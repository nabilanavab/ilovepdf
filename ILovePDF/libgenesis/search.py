import re
import logging
import requests
from .utils import Util
from pathlib import Path
from .download import LibgenDownload
from bs4 import BeautifulSoup as bsoup
from typing import Awaitable, Callable, Optional

logg = logging.getLogger(__name__)


class Libgen:
    def __init__(
        self, sort: str = "def", sort_mode: str = "DESC", result_limit: int = 25
    ) -> None:
        """This class contains an async method to search Library Genesis and return a dictionary of search
        results using the results id as the dictinary key.

        Args:

            sort (str):  It is used to sort the results based on the following allowed column values (based on libgen) - id, author, title, publisher, year, pages, language, size, extension.
                Default value = 'def'

            sort_mode (str):  It is used to sort the results in ascending or descending order based on the the column chosen with sort parameter.
                Default vaule = 'DESC'

            result_limit (int):  It is used to limit the returned values. Allowed values (based on libgen) are 25, 50, 100. If other than the allowed number in given it will return 25 results.
                Default vaule = 25

        Methods:
            search -> dict

        Retrun:
            An object with a search and download method.

        """

        if sort.lower() in [
            "def",
            "id",
            "author",
            "title",
            "publisher",
            "year",
            "pages",
            "language",
            "size",
            "extension",
        ]:
            self.sort = sort.lower()
        else:
            raise ValueError(
                f"sort parameter invalid. Allowed value is one of these (def, id, author, title, publisher, year, pages, language, size, extension)"
            )
        if sort_mode in ["ASC", "DESC"]:
            self.sort_mode = sort_mode.upper()
        else:
            raise ValueError(
                f"sort_mode parameter invalid. Allowed vaule is one of these (ASC, DESC)"
            )
        self.result_limit = result_limit
        self.__fields = [
            "def",
            "title",
            "author",
            "series",
            "publisher",
            "year",
            "identifier",
            "language",
            "md5",
            "tags",
            "extension",
        ]
        self.__libgen_url = "http://libgen.is"
        self.__json_url = f"{self.__libgen_url}/json.php?"
        self.__search_url = f"{self.__libgen_url}/search.php?"

        self.__ses = requests.Session()
        self.__ses.cookies.set("lg_topic", "libgen", domain="libgen.rs", expires=None)
        self.__ses.headers.update(
            {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/86.0.4240.198 Safari/537.36"
            }
        )

    async def search(
        self,
        query: str,
        search_field: str = "def",
        filters: dict = {},
        return_fields: list = [],
    ) -> dict:
        """A method used to search libgen.rs with diffrent filter and search fields.

        Args:

            query (str): The text to be searched

            search_field (str, optional): The colomun to search the query from, allowed columns to search are,

                'def' = default search according to relevance
                'title' = search the query from the title column of the books
                'author' = search the query from the author column of the books
                'series' = search the query from the series column of the books
                'publisher' = search the query from the publisher column of the books
                'year' = search the query from the year column of the books
                'identifier' = search the query from the identifier column of the books
                'language' = search the query from the language column of the books
                'md5' = search the query from the md5 column of the books
                'tags' = search the query from the tags column of the books
                'extension' = search the query from the extention column of the books

            filters (dict, optional): filter the results based on a given criterial. Works on every returned fields. Becareful when using this, it might decrese the limit of the returned results

                Example;
                    {
                        'year': '2009'
                        'extention': 'pdf'
                    }

            return_fields (list, optional): limit the reurned fields to a given fields in the list. Can pick from aviliable return fields.

                Example;
                    [
                        'id'
                        'title'
                        'md5'
                    ]

        Raises:

            ValueError: if query is empty.
            ValueError: if the query is less than 2 characters.
            ValueError: if search_field parameter is not from the allowed columns

        Returns:

            dict: returns a dictionary of dictionaries where the 'id' of the book is the key to the detailed result dictionary

        """

        if query:
            if len(query.strip()) < 2:
                raise ValueError(f'The query "{query}" is less than 2 characters.')
            req = "req=" + "+".join(query.strip().split(" "))
        else:
            raise ValueError(f"Query not set.")

        if search_field.lower() in self.__fields:
            column = "column=" + search_field.lower()
        else:
            raise ValueError(
                f'search_field invalid. Allowed fields are {",".join(self.__fields)}'
            )

        sort = "sort=" + self.sort
        sort_mode = "sortmode=" + self.sort_mode
        res = "res=" + str(self.result_limit)

        url = "&".join([self.__search_url, req, res, column, sort, sort_mode])

        return await self.__search(url, filters, return_fields)

    async def __search(self, url: str, filters: dict, return_fields: list) -> dict:

        ids_list = await self.__get_ids(url=url)
        data = {}
        if ids_list:
            data = await self.__get_json(
                ids_list=ids_list, return_fields=return_fields, filters=filters
            )
        return data

    async def __get_ids(self, url: str) -> list:

        r = self.__ses.get(url=url, allow_redirects=True)
        logg.debug(f"Requesting IDs page resulted in code: {r.status_code}")
        if r.status_code != 200:
            await Util().raise_error(
                r.status_code,
                str(r.reason) + " - " + str(bsoup(r.text, "lxml").get_text()),
            )

        soup = bsoup(r.content, "lxml")
        for s in soup.findAll("script"):
            s.decompose()
        table = soup.find("table", attrs={"rules": "rows"})

        ids = []
        for tr in table.findAll("tr")[1:]:
            ids.append(tr.td.get_text(strip=True))
        return ids

    async def __get_json(
        self, ids_list: list, return_fields: list, filters: dict
    ) -> dict:

        ids = "ids=" + ",".join(ids_list)
        fields = "fields=" + (
            "id," if return_fields and "id" not in return_fields else ""
        )
        if return_fields and "mirrors" in return_fields:
            fields += f'md5,sha1,filesize,edonkey,aich,tth,extension{"," if len(return_fields) > 1 else ""}'

        fields += (
            ",".join([fld for fld in return_fields if fld != "mirrors"])
            if return_fields
            else "*"
        )

        url = "&".join([self.__json_url, ids, fields])
        r = self.__ses.get(url, allow_redirects=True)
        logg.debug(f"Requesting JSON data from resulted in code: {r.status_code}")
        if r.status_code != 200:
            await Util().raise_error(
                r.status_code,
                str(r.reason) + " - " + str(bsoup(r.text, "lxml").get_text()),
            )

        raw_data = r.json()
        return await self.__format_json(
            raw_data=raw_data,
            ids_list=ids_list,
            filters=filters,
            return_fields=return_fields,
        )

    async def __format_json(
        self, raw_data: list, ids_list: list, filters: dict, return_fields: list
    ) -> dict:

        data = {}
        if raw_data:
            for res in ids_list:
                data[str(res)] = next(
                    item for item in raw_data if item["id"] == str(res)
                )
            if data:
                removed = []
                for res_id in data:
                    if filters:
                        if not await Util().filter_result(data[str(res_id)], filters):
                            removed.append(res_id)
                            continue

                    cover_reg = re.compile(
                        r"^\d+\\?\/[a-z-0-9]+\..{1,4}$", re.IGNORECASE
                    )
                    if "coverurl" in data[res_id].keys():
                        if re.match(cover_reg, data[res_id]["coverurl"]):
                            data[res_id][
                                "coverurl"
                            ] = f'{self.__libgen_url}/covers/{data[res_id]["coverurl"]}'
                        else:
                            data[res_id][
                                "coverurl"
                            ] = "https://cdn2.iconfinder.com/data/icons/leto-blue-online-education/64/__book_mouth_education_online-512.png"
                    if not return_fields or "mirrors" in return_fields:
                        md5 = data[res_id]["md5"]
                        if return_fields and "md5" not in return_fields:
                            data[res_id].pop("md5")
                        sha1 = data[res_id]["sha1"]
                        if return_fields and "sha1" not in return_fields:
                            data[res_id].pop("sha1")
                        size = data[res_id]["filesize"]
                        if return_fields and "filesize" not in return_fields:
                            data[res_id].pop("filesize")
                        edonkey = data[res_id]["edonkey"]
                        if return_fields and "edonkey" not in return_fields:
                            data[res_id].pop("edonkey")
                        aich = data[res_id]["aich"]
                        if return_fields and "aich" not in return_fields:
                            data[res_id].pop("aich")
                        tth = data[res_id]["tth"]
                        if return_fields and "tth" not in return_fields:
                            data[res_id].pop("tth")
                        extension = data[res_id]["extension"]
                        if return_fields and "extension" not in return_fields:
                            data[res_id].pop("extension")
                        tor_number = (
                            str(res_id)[:-3] + "000" if int(res_id) >= 1000 else "000"
                        )
                        data[res_id]["mirrors"] = {}

                        data[res_id]["mirrors"][
                            "main"
                        ] = f"http://library.lol/main/{md5}"

                        data[res_id]["mirrors"][
                            "libgen.lc"
                        ] = f"http://libgen.lc/ads.php?md5={md5}"

                        data[res_id]["mirrors"][
                            "z-library"
                        ] = f"http://b-ok.cc/md5/{md5}"

                        data[res_id]["mirrors"][
                            "libgen.pw"
                        ] = f"https://libgen.pw/item?id={res_id}"

                        data[res_id]["mirrors"][
                            "bookfi"
                        ] = f"http://bookfi.net/md5/{md5}"

                        data[res_id]["mirrors"][
                            "torrent"
                        ] = f"{self.__libgen_url}/book/index.php?md5={md5}&oftorrent="

                        data[res_id]["mirrors"][
                            "torrent_1k"
                        ] = f"{self.__libgen_url}/repository_torrent/r_{tor_number}.torrent"

                        data[res_id]["mirrors"][
                            "gnutella"
                        ] = f"magnet:?xt=urn:sha1:{sha1}&xl={size}&dn={md5}.{extension}"

                        data[res_id]["mirrors"][
                            "ed2k"
                        ] = f"ed2k://|file|{md5.upper()}.{extension}|{size}|{edonkey}|h={aich}|/"

                        data[res_id]["mirrors"][
                            "dc++"
                        ] = f"magnet:?xt=urn:tree:tiger:{tth}&xl={size}&dn={md5}.{extension}"

                    if "torrent" in data[res_id].keys():
                        data[res_id].pop("torrent")
                    if "locator" in data[res_id].keys():
                        data[res_id].pop("locator")
                    data[res_id].pop("id")
                if removed:
                    for ids in removed:
                        data.pop(ids)
        logg.info(f"Finished processing {len(data)} results.")
        return data

    @staticmethod
    async def download(
        url: str,
        dest_folder: Path = None,
        progress: Optional[Callable[..., Awaitable[None]]] = None,
        progress_args: list = [],
    ) -> Path:
        """Download the book from support mirro: 'library.lol', 'libgen.lc', 'libgen.gs', 'b-ok.cc'


        Args:
            url (str): The download like retrived from search method
            dest_folder (Path, optional): A path where the book should be download. Defaults to the current working directory.
            progress (Optional[Callable[..., Awaitable[None]]]): An awaitable function for progress updates that takes at least 2 arguments -
                    current: int and total int or str and other arguments passed through progress args.
            progress_args (list): Arguments to be passed to the progress update function along with progress update


        Returns:
            Path: The full path of the download book.

        """
        return await LibgenDownload().download(
            url, dest_folder, progress, progress_args
        )
