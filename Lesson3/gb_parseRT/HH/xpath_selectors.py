PAGINATION = {
    "selector": '//div[@data-qa="pager-block"]//a[@data-qa="pager-page"]/@href',
    "callback": 'parse',
}

VACANCY = {
    "selector": "???",
    "callback": "vacancy_parse",
}

VACANCY_DATA = {
    "title": {"xpath": '//h1[@data-qa="vacancy-title"]/text()'},
    "salary": {"xpath": '//h1[@class="vacancy-salary"]/span/text()'},
    "description": {"xpath": '//h1[@data-qa="vacancy-description"]//text()'},
    "skills": {"xpath": 'div[@class="bloko-tag-list"]//'
               'div[contains(@data-qa, "skills-element")]'
               'span[@data-qa="bloko-tag__text"]/text()'},
    "author": {"xpath": '//h1[@data-qa="vacancy-company_name"]/text()'}
}

COMPANY_VACANCIES = {
    "selector": "//div[contains(@data-qa, 'vacancy-serp__vacancy')]//",
    "callback": "vacancy_parse",
}

COMPANY_DATA = {
    "company_name": {"xpath": "//div[@class='company_header']//h1/span[@data-qa='company-header-title-name"},
    "company_site": {"xpath": "//a[@data-qa='sidebar-company-site']/@href"},
    "sphere_activities": {"xpath": "//div[contains(text(), 'Сферы деятельности')]/../p//text()"}
}