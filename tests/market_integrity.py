"""驗證全市場歸戶、市占、年度與產品分布的一致性。"""
import json
from pathlib import Path
from collections import Counter
p=Path(__file__).resolve().parents[1]
d=json.loads((p/'public/data/202608.json').read_text())
funds=d['funds']; banks=d['banks']; totals=d['totals']
assert totals['funds']==1097 and totals['classes']==4427
assert len({f['id'] for f in funds})==len(funds)==totals['funds']
assert sum(b['n'] for b in banks)==totals['funds']
assert abs(sum(b['aum'] for b in banks)-totals['aum'])<1
assert abs(sum(b['fee'] for b in banks)-totals['fee'])<=len(banks)
for bank in banks:
 rows=[f for f in funds if f['bank']==bank['bank']]
 assert len(rows)==bank['n']
 assert len({f['co'] for f in rows})==bank['clients']
 assert bank['n_rank']==1+sum(b['n']>bank['n'] for b in banks)
 assert bank['n_share']==round(bank['n']/totals['funds']*100,1)
for year in d['years']:
 rows=[f for f in funds if f['est'].startswith(str(year['year']))]
 assert len(rows)==year['total']==sum(b['n'] for b in year['banks'])
window=d['meta']['window']
rows=[f for f in funds if window['start']<=f['est']<=window['end']]
assert len(rows)==totals['newfunds_window']==sum(t['n'] for t in d['newfund_types'])
assert Counter(f['group'] for f in rows)==Counter({t['group']:t['n'] for t in d['newfund_types']})
assert 'highlight' not in d['meta'] and all('hl' not in t for t in d['newfund_types'])
assert all(c['status']=='pass' for c in d['checks'])
print('全市場資料一致性檢查通過：23 家保管行、1,097 檔基金')
