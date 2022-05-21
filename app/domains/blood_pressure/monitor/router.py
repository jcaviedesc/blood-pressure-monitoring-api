from fastapi import APIRouter
from loguru import logger
import requests
from fastapi.responses import JSONResponse
from bs4 import BeautifulSoup
from starlette import status

router = APIRouter(prefix="/monitors", tags=["Blood pressure"])


@router.get("", status_code=status.HTTP_200_OK)
async def search_blood_pressure_monitor(q: str = '', lang: str = 'es'):
    base_url = "https://www.stridebp.org"
    #TODO implementar los otros filtros
    end_point = f'{base_url}/{lang}/index.php?option=com_content&view=category&layout=monitors&id=8&Itemid=103&ajax=true&limit=20&search={q}'

    monitors_result = []
    try:
        r = requests.post(end_point)

        soup = BeautifulSoup(r.content, "html.parser")
        monitors_html = soup.find_all("div", class_="dev-item", itemprop=True)

        for monitor_html in monitors_html:
            title_element = monitor_html.find("div", class_="dev-info")

            brand = title_element.find("h2").text.strip()
            model = title_element.find("div", class_="model").text.strip()

            [location, use] = [item.text.strip()
                               for item in monitor_html.select(".field_title > .item")]

            validation_study = monitor_html.select(
                ".field_title > .devBtn")[0].text.strip()
            img = monitor_html.select(".dev-img .img-responsive")
            if img != None and len(img) > 0:
                img = "{}{}".format(base_url, img[0]['src'])
            else:
                img = None

            # metodo
            method = monitor_html.select(".method .item")[0].text.strip()
            # adicional
            additional = monitor_html.select(".additional .item")
            if additional != None and len(additional) > 0:
                additional = additional[0].text.strip()
            else:
                additional = None

            monitor = {
                'brand': brand,
                'model': model,
                'measurement_site ': location,
                'use': use,
                'validation_study': validation_study,
                'img': img,
                'measurement_method': method,
                'additional': additional
            }
            monitors_result.append(monitor)
    #TODO determinar la exepcion precisa
    except Exception as err:
        logger.error(err)
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content=monitors_result)

    return JSONResponse(status_code=status.HTTP_200_OK, content=monitors_result)
