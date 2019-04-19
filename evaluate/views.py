from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pymongo import MongoClient
from datetime import datetime

ITEM_OF_ONE_PAGE = 10
PAGE_PRE_RANGE = 3
PAGE_NEXT_RANGE = 3
db_client = MongoClient()

redirect_url = ""

@login_required
def index(request):
    return render(request, 'index.html', locals())


@login_required
def evaluate_article(request):
    global redirect_url
    if request.method == 'POST' and 'renew_all_item' in request.POST:
        count = 1
        while count <= int(request.POST['len_of_count']):
            evaluate_val = request.POST.get(str('evaluate_%s' % count))
            article_id = request.POST.get(str('article_id_%s' % count))
            username = request.user.username
            article_db = db_client.data_car['ucar_article']

            if evaluate_val:
                article_db.update({"article_id": article_id},
                                  {"$set": {"evaluate": int(evaluate_val),
                                            "evaluate_date": datetime.utcnow(),
                                            "evaluate_author": username}})
            count += 1
        return HttpResponseRedirect('/evaluate_article/?redirect_offset=%s' % redirect_url)
    else:
        url = r'https://forum.u-car.com.tw/forum/thread/'
        myquery = {}
        if request.method == 'GET' and 'redirect_offset' in request.GET:
            redirect_url = request.GET['redirect_offset']
            if redirect_url == 'non_evaluate_article':
                myquery = {"evaluate": None}

        article_list = db_client.data_car['ucar_article'].find(myquery)

        # pages
        current_page = request.GET.get("page", 1)
        current_page_data, page_range, pages_h = page_segmented(article_list, current_page, ITEM_OF_ONE_PAGE)

        return render(request, 'evaluate_article.html', locals())


@login_required
def evaluate_reply(request, offset):
    # global redirect_url
    if request.method == 'POST' and 'renew_all_item' in request.POST:
        count = 1
        while count <= int(request.POST['len_of_count']):
            evaluate_val = request.POST.get(str('evaluate_%s' % count))
            reply_id = request.POST.get(str('reply_id_%s' % count))
            username = request.user.username
            reply_db = db_client.data_car['ucar_reply']

            if evaluate_val:
                reply_db.update({"reply_id": reply_id},
                                  {"$set": {"evaluate": int(evaluate_val),
                                            "evaluate_date": datetime.utcnow(),
                                            "evaluate_author": username}})
            count += 1
        return HttpResponseRedirect(request.get_full_path())
    else:
        url = r'https://forum.u-car.com.tw/forum/thread/'
        page_symbol = '/?page='
        myquery = {"parent_article": str(offset)}

        reply_list = db_client.data_car['ucar_reply'].find(myquery)
        # pages
        current_page = request.GET.get("page", 1)
        current_page_data, page_range, pages_h = page_segmented(reply_list, current_page, ITEM_OF_ONE_PAGE)

        return render(request, 'evaluate_reply.html', locals())


def all_evaluate_reply(request):
    global redirect_url
    if request.method == 'POST' and 'renew_all_item' in request.POST:
        count = 1
        while count <= int(request.POST['len_of_count']):
            evaluate_val = request.POST.get(str('evaluate_%s' % count))
            reply_id = request.POST.get(str('reply_id_%s' % count))
            username = request.user.username
            reply_db = db_client.data_car['ucar_reply']

            if evaluate_val:
                reply_db.update({"reply_id": reply_id},
                                  {"$set": {"evaluate": int(evaluate_val),
                                            "evaluate_date": datetime.utcnow(),
                                            "evaluate_author": username}})
            count += 1
        return HttpResponseRedirect(request.get_full_path())
    else:
        url = r'https://forum.u-car.com.tw/forum/thread/'
        page_symbol = '/?page='
        myquery = {}

        if request.method == 'GET' and 'redirect_offset' in request.GET:
            redirect_url = request.GET['redirect_offset']
            if redirect_url == 'non_evaluate_reply':
                myquery = {"evaluate": None}

        reply_list = db_client.data_car['ucar_reply'].find(myquery)
        # pages
        current_page = request.GET.get("page", 1)
        current_page_data, page_range, pages_h = page_segmented(reply_list, current_page, ITEM_OF_ONE_PAGE)

        return render(request, 'evaluate_reply.html', locals())

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

#
# @login_required
# def non_evaluate_article(request):
#     url = r'https://forum.u-car.com.tw/forum/thread/'
#     # myquery = {"evaluate": {"$ne": None}}
#     myquery = {"evaluate": None}
#     article_list = db_client.data_car['ucar_article'].find(myquery)
#     return render(request, 'evaluate_article.html', locals())
#

# @login_required
# def non_evaluate_reply(request, offset):
#     url = r'https://forum.u-car.com.tw/forum/thread/'
#     page_symbol = '/?page='
#     myquery = {"parent_article": str(offset), "evaluate": None}
#     reply_list = db_client.data_car['ucar_reply'].find(myquery)
#
#     return render(request, 'evaluate_reply.html', locals())
#
#
# @login_required
# def all_evaluate_article(request):
#     url = r'https://forum.u-car.com.tw/forum/thread/'
#     article_list = db_client.data_car['ucar_article'].find()
#     return render(request, 'evaluate_article.html', locals())
#
#
# @login_required
# def all_evaluate_reply(request, offset=None):
#     url = r'https://forum.u-car.com.tw/forum/thread/'
#     page_symbol = '/?page='
#     reply_list = db_client.data_car['ucar_reply'].find()
#
#     return render(request, 'evaluate_reply.html', locals())
#
#
# @login_required
# def all_no_evaluate_reply(request, offset=None):
#     url = r'https://forum.u-car.com.tw/forum/thread/'
#     page_symbol = '/?page='
#     myquery = {"evaluate": None}
#     reply_list = db_client.data_car['ucar_reply'].find(myquery)
#
#     return render(request, 'evaluate_reply.html', locals())
