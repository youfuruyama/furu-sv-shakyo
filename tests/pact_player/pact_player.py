import json
import pathlib

class PactPlayer:
    def __init__(self, path):
        path = pathlib.Path('tests', 'pact_file') / path
        with path.open(encoding='utf8') as f:
            self.data = json.load(f)
    def run(self, test_case, api, state_notifier=None):
        for intr in self.data['interactions']:
            # Provider Stateを通知する
            if state_notifier is not None:
                state_notifier(intr.get('providerState', ''))

            # インタラクションごとにサブテストを作る
            with test_case.subTest(intr['description']):
                req = intr['request']
                url = req['path']
                query = req.get('query')
                if query is not None:
                    url += '?' + query

                # リクエストを送出する。返り値は、requests.Responseオブジェクト
                resp = api.requests.request(
                    method=req['method'],
                    url=url,
                    headers=req.get('headers'),
                    json=req.get('body'),
                )

                # 期待レスポンス
                e_resp = intr['response']

                # ステータスコードを照合する
                test_case.assertEqual(resp.status_code, e_resp['status'])

                # レスポンスヘッダを照合する
                for k, v in e_resp.get('headers', {}).items():
                    test_case.assertEqual(resp.headers.get(k), v)

                # レスポンスボディを照合する
                resp_body = e_resp.get('body')
                if resp_body is not None:
                    test_case.assertEqual(resp.json(), resp_body)