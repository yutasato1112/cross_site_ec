from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from ..process import serch
# Create your views here.

class serchView(TemplateView):
    template_name = "serch.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return render(self.request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        word = request.POST["serch_word"]
        serch_website = request.POST["select_range"]
        
        if serch_website == 'all':
            context = serch.all_serch(word)
            a_item_name_list = context['item_name']
            a_item_pic_list = context['item_pic']
            a_item_price_list = context['item_price']
            a_item_link_list = context['item_link']
            a_item_time_list = context['item_time']
            a_item_origin_list = context['origin']

            result = []
            for i in range(len(a_item_name_list)):
                tmp = {'item_name' : a_item_name_list[i],
                       'item_pic' : a_item_pic_list[i],
                       'item_price' : a_item_price_list[i],
                       'item_link' : a_item_link_list[i],
                       'item_time' : a_item_time_list[i],
                       'item_origin' : a_item_origin_list[i]
                       }
                result.append(tmp)
            context = {'word' : word,
                       'serch' : 'all',
                       'item_num' : len(result),
                       'result' : result
                       }

        elif serch_website == 'mercari':
            context = serch.mercari_serch(word)
            m_item_name_list = context['item_name']
            m_item_pic_list = context['item_pic']
            m_item_price_list = context['item_price']
            m_item_link_list = context['item_link']

            result = []
            for i in range(len(m_item_name_list)):
                tmp = {'item_name' : m_item_name_list[i],
                       'item_pic' : m_item_pic_list[i],
                       'item_price' : m_item_price_list[i],
                       'item_link' : m_item_link_list[i],
                       'item_time' : None,
                       'item_origin' : 'mercari'
                       }
                result.append(tmp)
            context = {'word' : word,
                       'serch' : 'mercari',
                       'item_num' : len(result),
                       'result' : result
                       }

        elif serch_website == 'yahoo':
            context = serch.yahoo_serch(word)
            y_item_name_list = context['item_name']
            y_item_pic_list = context['item_pic']
            y_item_price_list = context['item_price']
            y_item_link_list = context['item_link']
            y_item_time_list = context['item_time']

            result = []
            for i in range(len(y_item_name_list)):
                tmp = {'item_name' : y_item_name_list[i],
                       'item_pic' : y_item_pic_list[i],
                       'item_price' : y_item_price_list[i],
                       'item_link' : y_item_link_list[i],
                       'item_time' : y_item_time_list[i],
                       'item_origin' : 'yahoo'
                       }
                result.append(tmp)
            context = {'word' : word,
                       'serch' : 'yahoo',
                       'item_num' : len(result),
                       'result' : result
                       }

        return render(self.request, self.template_name, context)
    
    
