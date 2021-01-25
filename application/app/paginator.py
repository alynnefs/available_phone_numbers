from math import ceil

def paginate(query, page, per_page):
    """
    This method paginates the response
    Returns:
        json: page attributes
    """
    total = query.count()
    per_page = min(per_page, total) if total > 0 and per_page > 0 else 50
    total_pages = ceil(total / per_page)
    prev_page = page - 1 if page > 1 else page
    next_page = page + 1 if page < total_pages else total_pages

    page_items = query.paginate(page=page, per_page=per_page)

    items = [
        {
            'id': item.id,
            'value': item.value,
            'monthyPrice': str(item.monthyPrice),
            'setupPrice': str(item.setupPrice),
            'currency': item.currency
        }
        for item in page_items.items]

    return {
        "page": page,
        "total": total,
        "per_page": per_page,
        "total_pages": total_pages,
        "prev_page": prev_page,
        "next_page": next_page,
        "items": items
    }
