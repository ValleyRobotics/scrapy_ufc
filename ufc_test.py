





scrapy shell -s USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15"

http://www.ufcstats.com/statistics/events/completed?page=all

response.xpath('//span/[class="b-statistics__date"]').extract()





<span class="b-statistics__date">
                          August 29, 2020
                        </span>


for p in divs.xpath('.//p'):  # extracts all <p> inside
    print(p.get())


>>> for p in divs.xpath('p'):
...     print(p.get())


for p in divs.xpath('.//@class="b-statistics__date"'):
    ...:     print(p.getall())

    response.xpath('//a[contains(@href, "image")]/text()').re_first(r'Name:\s*(.*)')

    url = response.css('a::attr(href)').getall()
    returns 552

    < td


    class ="b-statistics__table-col b-statistics__table-col_style_big-top-padding" >


    Las
    Vegas, Nevada, USA
< / td >

    body > section > div > div
<span class="b-statistics__date">
                          August 22, 2020
                        </span>

response.selector.xpath('//span[@class="b-statistics__date"]/text()‌​').extract()

http://www.ufcstats.com/statistics/events/completed?page=all
#this works
date = response.selector.xpath('//span[@class="b-statistics__date"]/text()').extract()
event_url = response.css('a::attr(href)').getall()
location = response.selector.xpath('//td[@class="b-statistics__table-col b-statistics__table-col_style_big-top-padding"]/text()').extract()

http://www.ufcstats.com/event-details/e29cf523ebd155c5
fighter_name = response.selector.xpath('//a[@class="b-link b-link_style_black"]//text()').extract()
response.xpath('//p[@class="b-fight-details__table-text"]//text()').extract()
response.xpath('//p[@class="b-fight-details__table-text"]//text()').extract()




<p class="b-fight-details__table-text">

<a class="b-link b-link_style_black" href="http://www.ufcstats.com/fighter-details/333b9e5c723ac873">
              Aleksandar Rakic
            </a>

body > section > div > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > p:nth-child(1) > a

body > section > div > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > p:nth-child(1)

class="b-fight-details__table-text"


for line in d2:
    line_out = line.strip().replace('\n', '')
    print(line_out)



urls = response.xpath('//tr[@class="b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click"]//data-link/text()').get()
class="b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click"


body > section > div > h2 > a
d2 = response.xpath('//a[@class="b-link"]/text()').extract_first()
response.xpath('//p[@class="b-fight-details__table-text"]//text()').extract()

# result = []
         for line in d2:
             line_out = line.strip().replace('\n', '')
             if len(line_out) > 0:
                 result.append(line_out)
