from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate_queryset(queryset, page, items_per_page=10):
    """
    Разбивает queryset на страницы.

    :param queryset: QuerySet - данные, которые нужно разделить на страницы
    :param page: int - текущая страница
    :param items_per_page: int - количество элементов на странице
    :return: tuple (page_object, paginator)
    """
    paginator = Paginator(queryset, items_per_page)
    try:
        page_object = paginator.page(page)
    except PageNotAnInteger:
        # Если номер страницы не целое число, показываем первую страницу
        page_object = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше, чем общее количество страниц, показываем последнюю
        page_object = paginator.page(paginator.num_pages)

    return page_object, paginator
