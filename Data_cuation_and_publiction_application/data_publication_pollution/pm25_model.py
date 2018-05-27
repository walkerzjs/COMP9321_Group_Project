from mongoengine import *
import xlrd


class AirPollution(Document):
    country = StringField(required=True, primary_key=True, max_length=100)
    ppy = DictField(required=True) # pollution per year

    def __init__(self, country, ppy, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.country = country
        self.ppy = ppy


pm25_link = 'http://api.worldbank.org/v2/en/indicator/EN.ATM.PM25.MC.M3?downloadformat=excel'
pm25_file = 'API_EN.ATM.PM25.MC.M3_DS2_en_excel_v2_9911760.xls'

connect(host='mongodb://admin:password@ds229450.mlab.com:29450/9321-ass3')
collection_created = False

_entry_check = AirPollution.objects().first()
if _entry_check is not None:
    collection_created = True


def import_ap_data():
    xl_workbook = xlrd.open_workbook(pm25_file)
    xl_sheet = xl_workbook.sheet_by_index(0)
    for row in range(4, 267):
        country = xl_sheet.cell_value(row, 0)
        # FIXME filter out country groups if needed
        ppy_data = {}
        year_count = 0
        for year in range(1960, 2017):
            if year < 1990:
                continue
            col = year - 1956
            try:
                pollution = float(xl_sheet.cell_value(row, col))
                ppy_data[str(year)] = pollution
                year_count += 1
            except ValueError:
                # No pollution data for this year
                continue
        # only add countries that have data
        if year_count > 0:
            ap = AirPollution(country, ppy_data)
            ap.save()


def get_collection():
    if not collection_created:
        import_ap_data()
    ap_set = AirPollution.objects()
    ap_list = []
    for ap in ap_set:
        ap_list.append({"Country": ap.country, "Data": ap.ppy})
    return ap_list


def get_sorted_collection():
    return sorted(get_collection(), key=lambda ap: ap['Country'])


def get_entry_by_country(country):
    if not collection_created:
        import_ap_data()
    ap = AirPollution.objects(country=country).first()
    if ap is not None:
        return {"Country": country, "Data": ap.ppy}
    return None


def get_entry_by_year(year):
    if not collection_created:
        import_ap_data()
    try:
        year_str = str(year)
        ap_set = AirPollution.objects()
        ap_dict = {}
        for ap in ap_set:
            if year_str in ap.ppy:
                ap_dict[ap.country] = ap.ppy[year_str]
        return ap_dict
    except ValueError:
        return None


def get_entry_by_filter(year, country):
    if not collection_created:
        import_ap_data()
    try:
        year_str = str(year)
        ap = AirPollution.objects(country=country).first()
        if ap is not None and year_str in ap.ppy:
            return {"Country": country, year_str: ap.ppy[year_str]}
        return None 
    except ValueError:
        return None
