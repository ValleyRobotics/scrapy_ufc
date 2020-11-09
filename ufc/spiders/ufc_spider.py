from scrapy import Spider, Request
from ufc.items import UfcItem


def split_it(lst):
    ret = lst.split(' ')
    return [ret[0], ret[-1]]


class UfcSpider(Spider):
    name = 'ufc_spider'
    allowed_domains = ['ufcstats.com']
    start_urls = ['http://www.ufcstats.com/statistics/events/completed?page=all']


    def parse(self, response):
        event_urls = response.css('a::attr(href)').getall()
        for url in event_urls:#[95:125]: # here #
            if len(url) == 54:
                print(url)
                yield Request(url=url, callback=self.parse_results_page)


    def parse_results_page(self, response):
        print("z" * 100)
        event_date = response.xpath('//li[@class="b-list__box-list-item"]//text()').getall()
        fight_urls = response.css('a::attr(href)').getall()
        event_loc = (event_date[5].strip().replace('\n', ''))
        event_date = (event_date[2].strip().replace('\n', ''))
        for fight in fight_urls:
            if len(fight) == 54:
                print(fight)
                print((event_date))
                print('XX'*50)
                yield Request(url=fight, callback=self.parse_fight_details,
                              meta={'event_date': event_date, 'event_loc': event_loc})


    def parse_fight_details(self, response):
        event = response.xpath('//a[@class="b-link"]/text()').extract_first().strip().replace('\n', '')
        fight_class = response.xpath('//i[@class="b-fight-details__fight-title"]/text()').extract()
        res_detail = response.xpath('//p[@class="b-fight-details__text"]//text()').extract()
        fight_result = response.xpath('//div[@class="b-fight-details__person"]//text()').getall()
        x = '-'
        result = []
        res_det = []

        item = UfcItem()
        item['event_name'] = event
        result_out = []
        for line in fight_result:
            line_out = line.strip().replace('\n', '')
            if len(line_out) > 0:
                result_out.append(line_out)
        item['f1_res'] =result_out[0]
        if result_out[0]=='W':
            item['f2_res'] = 'L'
        elif result_out[0] == 'L':
            item['f2_res'] = 'W'
        else:
            item['f2_res'] = result_out[0]

        item['fight_result'] = result_out

        if len(fight_class)>1:
            fight_class=fight_class[1].strip().replace('\n', '')
        else:
            fight_class=fight_class[0].strip().replace('\n', '')
        item['fight_class'] = fight_class
        for i, line in enumerate(res_detail):
            res_det.append(line.strip().replace('\n', ''))
        item['method'] = res_det[4]
        item['round'] = res_det[9]
        item['time'] = res_det[13]
        item['time_format'] = res_det[17]
        item['referee'] = res_det[22]
        item['event_loc'] = response.meta['event_loc']
        item['event_date'] = response.meta['event_date']
        if len(res_det[29])<5:
            #x = x.join(res_det[29:])
            item['details']= 'Judge'
            item['judge_1'] = x.join(res_det[31:33])
            item['judge_2'] = x.join(res_det[35:37])
            item['judge_3'] = x.join(res_det[39:41])
        else:
            item['details'] = res_det[29]
        fight_details = response.selector.xpath('//p[@class ="b-fight-details__table-text"]//text()').extract()
        for i, line in enumerate(fight_details):
            line_out = line.strip().replace('\n', '')
            result.append(line_out)
            # debug
            #y.append(str(i))
            #y.append(line_out)
        item['fighter_name_1'] = result[1]
        item['fighter_name_2'] = result[4]
        item['kd_1'] = result[6]
        item['kd_2'] = result[7]
        item['sig_str_1'] = split_it(result[8])
        item['sig_str_2'] = split_it(result[9])
        item['sig_strP_1'] = result[10]
        item['sig_strP_2'] = result[11]
        item['tot_str_1'] = split_it(result[12])
        item['tot_str_2'] = split_it(result[13])
        item['TD_1'] = split_it(result[14])
        item['TD_2'] = split_it(result[15])
        item['TDP_1'] = result[16]
        item['TDP_2'] = result[17]
        item['sub_att_1'] = result[18]
        item['sub_att_2'] = result[19]
        item['rev_1'] = result[20]
        item['rev_2'] = result[21]
        item['ctrl_1'] = result[22]
        item['ctrl_2'] = result[23]
        item['r1_sig_str_1'] = split_it(result[32])
        item['r1_sig_str_2'] = split_it(result[33])
        item['r1_sig_strP_1'] = result[34]
        item['r1_sig_strP_2'] = result[35]
        item['r1_tot_str_1'] = split_it(result[36])
        item['r1_tot_str_2'] = split_it(result[37])
        item['r1_TD_1'] = split_it(result[38])
        item['r1_TD_2'] = split_it(result[39])
        item['r1_TDP_1'] = result[40]
        item['r1_TDP_2'] = result[41]
        item['r1_sub_att_1'] = result[42]
        item['r1_sub_att_2'] = result[43]
        item['r1_rev_1'] = result[44]
        item['r1_rev_2'] = result[45]
        item['r1_ctrl_1'] = result[46]
        item['r1_ctrl_2'] = result[47]
        # base + 24 per round is the starting place for tot columns #
        base = 34 + (int(res_det[9])*24)
        item['tot_head_1'] = split_it(result[base])
        item['tot_head_2'] = split_it(result[base + 1])
        item['tot_body_1'] = split_it(result[base + 2])
        item['tot_body_2'] = split_it(result[base + 3])
        item['tot_leg_1'] = split_it(result[base + 4])
        item['tot_leg_2'] = split_it(result[base + 5])
        item['tot_dist_1'] = split_it(result[base + 6])
        item['tot_dist_2'] = split_it( result[base + 7])
        item['tot_clinch_1'] = split_it(result[base + 8])
        item['tot_clinch_2'] = split_it(result[base + 9])
        item['tot_ground_1'] = split_it(result[base + 10])
        item['tot_ground_2'] = split_it(result[base + 11])

        yield item
