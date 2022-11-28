from bs4 import BeautifulSoup
import aiohttp
import asyncio


class Analyze:
    def __init__(self, product_name: str):
        self.__product_name = product_name.lower()

    async def __parse_21_vek(self):
        async with aiohttp.ClientSession() as session:
            # 21vek.by
            vek21 = await session.get("https://www.21vek.by/search/?sa=&term=" + self.__product_name)
            data = await vek21.text()
            soup = BeautifulSoup(data, 'html.parser')
            names = soup.find_all('span', class_='result__name')
            prices = soup.find_all('span', class_='g-item-data')
            links = soup.find_all('a', class_='result__link', href=True)
            element = 0
            link_num = 0
            try:
                lower_price = await self.__normal_price(prices[0])
            except:
                return {'21vek.by': False}
            for i in prices:
                if self.__product_name in names[element].text.lower():
                    iter_price = await self.__normal_price(i)
                    if iter_price <= lower_price:
                        lower_price = iter_price
                        link_num = element
                element += 1
            return {
                '21vek.by': [lower_price, links[link_num]['href']]
            }

    @staticmethod
    async def __normal_price(price):
        if '–' in price.text:
            price = price.text.split('–')[0].replace(' ', '').replace(',', '.')
        else:
            price = price.text.replace(' ', '').replace(',', '.')
        return float(price)

    async def __parse_shop_by(self):
        # shop.by
        async with aiohttp.ClientSession() as client:
            response = await client.get(f"https://shop.by/find/?findtext={self.__product_name.lower()}"
                                        f"&sort=price--number")
            html_site = await response.text()
            soup = BeautifulSoup(html_site, 'html.parser')
            price_with_salt = soup.find_all('span', class_='PriceBlock__PriceValue')
            names_with_salt = soup.find_all('div', class_='ModelList__NameBlock')
            link_with_salt = soup.find_all('a', class_='ModelList__LinkModel', href=True)
            try:
                name = names_with_salt[0].findChildren()[1].text
            except:
                return {'shop.by': False}
            print(price_with_salt[0])
            try:
                price = await self.__normal_price(price_with_salt[0].findChildren()[1])
            except:
                price = await self.__normal_price(price_with_salt[0].findChildren()[0])
            return {
                'shop.by':
                [
                    price,
                    'https://shop.by' + link_with_salt[0]['href']
                ]
            }

    async def __parse_1k_by(self):
        # 1k.by
        async with aiohttp.ClientSession() as client:
            response = await client.get(f"https://1k.by/products/search?s_keywords={self.__product_name}"
                                        "&searchFor=products&s_categoryid=0")
            html_data = await response.text()
            soup = BeautifulSoup(html_data, 'html.parser')
            try:
                price = soup.find_all('span', class_='money__val')[0]
            except:
                return {'1k.by': False}
            link = soup.find_all('a', class_='prod__link', href=True)
            return {
                '1k.by':
                [
                    await self.__normal_price(price),
                    link[0]['href']
                ]
            }

    async def get_analysis_data(self):
        output = {}
        output.update(
            await self.__parse_shop_by()
        )
        output.update(
            await self.__parse_21_vek()
        )
        output.update(
            await self.__parse_1k_by()
        )

        return output
