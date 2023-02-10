# fileName: plugins/dm/callBack/inline_query/__init__.py
# copyright ©️ 2021 nabilanavab
fileName = "plugins/dm/callBack/inline_query/__init__.py"

in_work = list()
# all users will be added to in_work on_chosen_inline_result and
# It stops all new requests from that user else inline_data changes

inline_data = dict()

"""
inline_data = {
    "from_user.id" : {
        "id" : "file_id",
        "href" : "file_link",
        "span" : "additional_info",
        "thumb" : "thumbnail",
        "title" : "book_name"
    }
}
"""
