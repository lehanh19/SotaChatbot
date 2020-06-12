import re

import lxml.html as lh
import requests
from cachetools import cached, TTLCache
from googletrans import Translator
from date_helpers import to_date
#import actions

translator = Translator()

def get_data():
    msg = ""
    #msg = actions.ActionAskPaper()
    print('hello world')
    return msg

def handle_data(intent):
    try:
        intent_map = {
            'ask_paper': 'paper',
            'ask_trending1': 'trend1',
            'ask_trending2': 'trend2',
            'ask_trending3': 'trend3',
            'ask_competition': 'competition',
            'ask_conference': 'conference',
            'fallback': 'fallback'
        }
        if intent_map[intent] == 'paper':
            return get_data()
        # When fallback
        return "Xin lỗi, em chưa được training để trả lời câu hỏi này ạ :(("
    except:
        return "Đã có lỗi xảy ra trong khi cập nhật dữ liệu. Anh (chị) vui lòng thử lại sau ạ."

print(handle_data('ask_paper'))