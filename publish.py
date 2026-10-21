"""Make the participant page index.html from the team's dev.html.

dev.html is the page we edit: every slide link, plus a "development copy" banner and noindex.
index.html is what participants see: only the slide PDFs listed in PUBLIC; every other slide link becomes "Slides soon".
Notebooks and every other link are unchanged. Usage: python3 publish.py, then commit and push both pages.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
PUBLIC = [  # slide PDFs participants can see; add a deck here when it is settled
    'D1-1a_What_Is_a_Language_Model', 'D1-1b_Neural_Language_Models', 'D1-1c_Attention_and_Transformers',
    'D1-1d_BERT_and_GPT', 'D1-1e_From_GPT_to_ChatGPT',
]

s = open(os.path.join(HERE, 'dev.html')).read()
s = re.sub(r'<meta name="robots"[^>]*><!--DEV-->\n', '', s)                      # participant page may be indexed
s = re.sub(r'<div[^>]*><!--DEV-->.*?<!--/DEV-->\n', '', s, flags=re.S)           # drop the banner


def materials(m):  # one Materials cell: keep public slide links, replace the rest by a single "Slides soon"
    cell = m.group(0)
    links = re.findall(r'<a href="slides/([^"]+)\.pdf">.*?</a>', cell)
    hidden = [n for n in links if n not in PUBLIC]
    if not hidden: return cell
    for n in hidden: cell = re.sub(rf'<a href="slides/{re.escape(n)}\.pdf">.*?</a>', '', cell)
    if not re.search(r'<a |<span', cell[len('<td class="mat">'):]):
        cell = cell.replace('<td class="mat">', '<td class="mat"><span class="soon">Slides soon</span>', 1)
    return cell

s = re.sub(r'<td class="mat">.*?</td>', materials, s, flags=re.S)
assert '<!--DEV-->' not in s
open(os.path.join(HERE, 'index.html'), 'w').write(s)
shown = sorted(set(re.findall(r'href="slides/([^"]+)\.pdf"', s)))
print(f'index.html: {len(shown)} slide PDFs shown — ' + ', '.join(shown))
