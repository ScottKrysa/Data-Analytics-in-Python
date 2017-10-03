"""
This program will scrape sector results, return the sector that was 
the biggest mover, and then return the biggest winner and loser in that sector.
"""

def get_sector_level_data(link_biggest_mover):
    import requests
    from bs4 import BeautifulSoup

    base_url = link_biggest_mover

    response = requests.get(base_url)

    try:
        results_page = BeautifulSoup(response.content,'lxml')
        comp_perf_table = results_page.find('table', class_='topmovers')
        mover_list_names = list()
        mover_list_perf = list()
        for a_tag in comp_perf_table.find_all('a'):
            company_name = a_tag.get_text()
            mover_list_names.append(company_name)
        for span_tag in comp_perf_table.find_all('span'):
            company_perf = span_tag.get_text()
            mover_list_perf.append(company_perf)

        results_tuple = [(mover_list_names[0], mover_list_perf[1].strip('()')), (mover_list_names[10], mover_list_perf[11].strip('()'))]

        return results_tuple
    except:
        return None

def get_all_sector_data():
    import requests
    from bs4 import BeautifulSoup

    base_url = "https://finance.google.com/finance"
    response = requests.get(base_url)

    try:
        results_page = BeautifulSoup(response.content,'lxml')
        secperf_table = results_page.find('div', id='secperf')
        sector_list_names = list()
        sector_list_links = list()
        sector_list_perf = list()
        for a_tag in secperf_table.find_all('a'):
            sector_name = a_tag.get_text()
            sector_link = "https://finance.google.com" + a_tag.get('href')
            sector_list_names.append(sector_name)
            sector_list_links.append(sector_link)
        for span_tag in secperf_table.find_all('span'):
            sector_perf = span_tag.get_text()
            sector_list_perf.append(sector_perf)

        perf_float_abs_values = [float(y.strip('+%-')) for y in sector_list_perf]

        index_biggest_mover = perf_float_abs_values.index(max(perf_float_abs_values))

        link_biggest_mover = sector_list_links[index_biggest_mover]
        sector_level_tuple = get_sector_level_data(link_biggest_mover)

        biggest_mover = sector_list_names[index_biggest_mover]
        biggest_mover_perf = sector_list_perf[index_biggest_mover].strip('+')

        result = str("The sector with the biggest move is %s with a move \
of %s\nThe top gainer in this sector is %s with a move of \
%s\nThe top loser in this sector is %s with a move of %s") % \
(biggest_mover, biggest_mover_perf, sector_level_tuple[0][0], \
sector_level_tuple[0][1], sector_level_tuple[1][0], sector_level_tuple[1][1])
        
        return result
    except:
        return None

print(get_all_sector_data())