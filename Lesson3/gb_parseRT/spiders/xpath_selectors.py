BRANDS = {
    'selector': '//div[contains(@class, "TransportMainFilters_brandsList")]//a[@data-target="brand"]/@href',
    'callback': 'brand_parse',
}

PAGINATION = {
    'selector': '//div[contains(@class, "Paginator_block")]/a[@data-target="buttom-link"]',
    'callback': 'brand_parse',
}

CARS = {
    'selector': '//article[@data-target="serp-snippet"]//a[@data-target="serp-snippet-title"]',
    'callback': 'car_parse',
}

CAR_DATA = {
    'title': {"xpath": '//div[@data-target="advert-title"]/text()'},
    'price': {"xpath": '//div[@data-target="advert-price"]/text()'},
    'photos': {"xpath": '//figure[contains(@class, "PhotoGallery")]/picture/img[contains(@class, "photoImage")]/@src'},
    'characteristics': {"xpath": '//div[contains(@class, "AdvertCard_specs")]//div[contains(@class, "AdvertSpecs_row")]'},
    'description': {"xpath": '//div[@data-target="advert-info-descriptionFull"]/text()'},
    'author': {"xpath": '//div[contains(text(), "window.transitState = decoderURIComponent")]',
               're': r"youlaId%22%2C%22([a-za-z|\d]+)%22%2C%22avatar"},
}

