from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pymongo import MongoClient


ITEM_OF_ONE_PAGE = 10
PAGE_PRE_RANGE = 3
PAGE_NEXT_RANGE = 3
db_client = MongoClient()


@login_required
def index(request):
    return render_to_response('index.html', locals())


@login_required
def non_evaluate_article(request):
    url = r'https://forum.u-car.com.tw/forum/thread/'
    # myquery = {"evaluate": {"$ne": None}}
    myquery = {"evaluate": None}
    article_list = db_client.data_car['ucar_article'].find(myquery)
    return render_to_response('evaluate_article.html', locals())


@login_required
def non_evaluate_reply(request, offset):
    url = r'https://forum.u-car.com.tw/forum/thread/'
    page_symbol = '/?page='
    myquery = {"parent_article": str(offset), "evaluate": None}
    reply_list = db_client.data_car['ucar_reply'].find(myquery)

    return render_to_response('evaluate_reply.html', locals())


@login_required
def all_evaluate_article(request):
    url = r'https://forum.u-car.com.tw/forum/thread/'
    article_list = db_client.data_car['ucar_article'].find()
    return render_to_response('evaluate_article.html', locals())


@login_required
def all_evaluate_reply(request, offset=None):
    url = r'https://forum.u-car.com.tw/forum/thread/'
    page_symbol = '/?page='
    reply_list = db_client.data_car['ucar_reply'].find()

    return render_to_response('evaluate_reply.html', locals())


@login_required
def all_no_evaluate_reply(request, offset=None):
    url = r'https://forum.u-car.com.tw/forum/thread/'
    page_symbol = '/?page='
    myquery = {"evaluate": None}
    reply_list = db_client.data_car['ucar_reply'].find(myquery)

    return render_to_response('evaluate_reply.html', locals())


def page_segmented(model_obj, current_page, item_num_of_one_page):
    pages = Paginator(model_obj, item_num_of_one_page)  # get all page
    tmp_page_range = []

    try:
        # get current page
        one_page_data = pages.page(current_page)
    except PageNotAnInteger:
        # if page number format incorrect, show page 1
        one_page_data = pages.page(1)
    except EmptyPage:
        # if page number is empty page, show last page
        one_page_data = pages.page(pages.num_pages)

    if pages.num_pages >= PAGE_PRE_RANGE + PAGE_NEXT_RANGE:
        # count page range
        pre_range_start = one_page_data.number - PAGE_PRE_RANGE
        next_range_end = one_page_data.number + PAGE_NEXT_RANGE

        if pre_range_start < 1:
            next_range_end += abs(pre_range_start)
            pre_range_start = 1
        elif next_range_end > pages.num_pages:
            pre_range_start -= next_range_end - pages.num_pages
            next_range_end = pages.num_pages

        # page range store into list
        for i in range(pre_range_start, next_range_end + 1):
            tmp_page_range.append(i)
    else:
        tmp_page_range = pages.page_range

    return one_page_data, tuple(tmp_page_range), pages


