import scrapy

class MilAnuncios_Spider(scrapy.Spider):
    name = 'milan'
    start_urls = ['https://www.milanuncios.com/alquiler-de-pisos/']

    #Extract
    def parse(self, response):
        for piso in response.css('.aditem.ProfesionalCardTestABClass'):
            try:
                yield {
                    'name': piso.css('.aditem-detail-title::text').get(),
                    'location': piso.css('.list-location-region::text').get(),
                    'link': piso.css('.aditem-detail-title').attrib['href'],
                    'precio': piso.css('.aditem-price::text').get().replace('.', ''),
                    'metros_cuadrados': piso.css('.m2.tag-mobile::text').get(),
                    'n_dormitorios': piso.css('.dor.tag-mobile::text').get(),
                    'n_baños': piso.css('.ban.tag-mobile::text').get(),
                }
            except:
                print('Error al extraer info')

        next_page = response.css('.adlist-paginator-pagelink.adlist-paginator-pageselected a')[1].attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)