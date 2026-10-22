"""Make the participant page index.html from the team's dev.html.

dev.html is the page we edit: every slide link, plus a "development copy" banner and noindex.
index.html is what participants see: only the slide PDFs listed in PUBLIC and the lab notebooks listed in PUBLIC_NOTEBOOKS;
every other slide link becomes "Slides soon", and every other lab's links (Colab and Docker version) become "Notebook soon".
The pre-work readiness check is not in the schedule table, so it always stays. Usage: python3 publish.py, then commit and push both pages.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
PUBLIC = [  # files in slides/ (PDF or PPTX, without extension) participants can see; add one when it is settled
    'D1-1a_What_Is_a_Language_Model', 'D1-1b_Neural_Language_Models', 'D1-1c_Attention_and_Transformers',
    'D1-1d_BERT_and_GPT', 'D1-1e_From_GPT_to_ChatGPT', 'D1-4_RAG',
    'D2-0_Capstone_Brief', 'D2-0b_Capstone_Design_Template', 'D2-1_Agents_I',
]
PUBLIC_NOTEBOOKS = [  # notebooks in notebooks/ (without .ipynb) participants can open from the schedule
    'day1_chatgpt_lab', 'day1_rag_lab', 'day2_agents1_lab_cheese_quiz',
]

s = open(os.path.join(HERE, 'dev.html')).read()
s = re.sub(r'<meta name="robots"[^>]*><!--DEV-->\n', '', s)                      # participant page may be indexed
s = re.sub(r'<div[^>]*><!--DEV-->.*?<!--/DEV-->\n', '', s, flags=re.S)           # drop the banner


def materials(m):  # one Materials cell: keep public slides and notebooks, replace the rest by "Slides soon" / "Notebook soon"
    cell = m.group(0)
    notebooks = re.findall(r'notebooks/([^"/]+)\.ipynb"', cell)
    if any(n not in PUBLIC_NOTEBOOKS for n in notebooks):  # a lab that is not public yet: hide all its links
        return '<td class="mat"><span class="soon">Notebook soon</span></td>'
    hidden = [n for n in re.findall(r'<a href="slides/([^"]+)\.(?:pdf|pptx)">', cell) if n not in PUBLIC]
    if not hidden: return cell
    for n in hidden: cell = re.sub(rf'<a href="slides/{re.escape(n)}\.(?:pdf|pptx)">.*?</a>', '', cell)
    if not re.search(r'<a |<span', cell[len('<td class="mat">'):]):
        cell = cell.replace('<td class="mat">', '<td class="mat"><span class="soon">Slides soon</span>', 1)
    return cell


s = re.sub(r'<td class="mat">.*?</td>', materials, s, flags=re.S)
assert '<!--DEV-->' not in s
open(os.path.join(HERE, 'index.html'), 'w').write(s)
shown = sorted(set(re.findall(r'href="slides/([^"]+)\.(?:pdf|pptx)"', s)))
nbs = sorted(set(re.findall(r'<td class="mat">[^<]*<a href="[^"]*notebooks/([^"/]+)\.ipynb"', s)))
print(f'index.html: {len(shown)} slide PDFs shown — ' + ', '.join(shown))
print(f'index.html: {len(nbs)} lab notebooks shown' + (' — ' + ', '.join(nbs) if nbs else ''))
