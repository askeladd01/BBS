from django.core.paginator import Paginator


def MyPaginator(request, article_list, per_count):
    paginator = Paginator(article_list, per_count)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    is_paginated = True if paginator.num_pages > 1 else False
    page_range = paginator.get_elided_page_range(page_obj.number, on_each_side=2)

    content = {'page_obj': page_obj, 'page_range': page_range, 'is_paginated': is_paginated}
    return content
