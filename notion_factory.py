from notion.client import NotionClient
from notion.collection import NotionDate


class NotionFactory:

    TOKEN = '61a87702b8c4f7d402a7b31366d3fa68b22b9a74a8e31340faa327e7ced68a04ad665eba77cad3be5af7bef31a1ac9f96c99' \
            'deecabf91b6e28685852c083d7469ad217f3a485451936ac2c0dd1c3'
    NOTION = 'https://www.notion.so/e0bcfe544d5d4ef29c2cf2d17227a87e?v=b7b5f9220e32456ba27a9809922b5e7d'

    def __init__(self):
        self.client = NotionClient(token_v2=self.TOKEN)
        self.database = self.client.get_collection_view(self.NOTION)

    def push_request(self, request):
        if not request.is_valid:
            raise TypeError('Request is invalid')
        print(self.database.parent.views)
        row = self.database.collection.add_row()
        row.title = request.phone
        row.data = NotionDate(request.date)
        row.tsena = request.price
        row.ot_kogo = request.partner
        row.kol_vo = request.amount
        row.tip = request.request_type
        row.prishli = request.came
        if request.prepaid != 0:
            row.predoplata = request.prepaid
