from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {'.git', '.github', '_data', '_includes', '_layouts', '_site', '_templates', 'assets', 'tools'}


def enc_path(parts):
    return '/' + '/'.join(quote(p, safe='') for p in parts) + '/'


def yq(s):
    return '"' + str(s).replace('\\', '\\\\').replace('"', '\\"') + '"'


def list_categories():
    cats = []
    for p in sorted(ROOT.iterdir(), key=lambda x: x.name.lower()):
        if not p.is_dir() or p.name in SKIP_DIRS or p.name.startswith('.'):
            continue
        challenges = [c for c in sorted(p.iterdir(), key=lambda x: x.name.lower()) if c.is_dir() and (c / 'original.md').exists()]
        if challenges:
            cats.append((p, challenges))
    return cats


def write_data(cats):
    data = ROOT / '_data'
    data.mkdir(exist_ok=True)
    nav = []
    ch_yaml = []
    for cat, challenges in cats:
        nav.append(f'- title: {yq(cat.name)}\n  url: {yq(enc_path([cat.name]))}\n  count: {len(challenges)}\n')
        ch_yaml.append(f'- title: {yq(cat.name)}\n  url: {yq(enc_path([cat.name]))}\n  count: {len(challenges)}\n  challenges:\n')
        for chal in challenges:
            has_wp = (chal / 'WP.md').exists()
            ch_yaml.append(f'    - title: {yq(chal.name)}\n      url: {yq(enc_path([cat.name, chal.name]))}\n      has_wp: {str(has_wp).lower()}\n')
    (data / 'navigation.yml').write_text(''.join(nav), encoding='utf-8')
    (data / 'challenges.yml').write_text(''.join(ch_yaml), encoding='utf-8')


def write_home(cats):
    total = sum(len(chals) for _, chals in cats)
    cards = []
    for cat, challenges in cats:
        cards.append(f'''  <a class="card" href="{{{{ '{enc_path([cat.name])}' | relative_url }}}}">
    <h3>{cat.name}</h3>
    <p>{len(challenges)} 道题目 · 点击进入题目集</p>
  </a>''')
    text = f'''---
layout: default
title: 首页
---

<section class="hero">
  <p class="eyebrow">CryptoHack CN</p>
  <h1>CryptoHack 题面精译与个人解答</h1>
  <p class="lead">这里按 CryptoHack 原有题目集组织内容。每道题保留固定英语题面，并提供可展开的中文精翻与个人解答，方便先读题、再对照理解、最后审阅解法。</p>
  <div class="meta-row">
    <span class="pill">{len(cats)} 个题目集</span>
    <span class="pill">{total} 道题目</span>
    <span class="pill">GitHub Pages 友好结构</span>
  </div>
</section>

<h2 class="section-title">题目集导航</h2>
<div class="grid">
{chr(10).join(cards)}
</div>
'''
    (ROOT / 'index.md').write_text(text, encoding='utf-8')


def write_category_pages(cats):
    for cat, challenges in cats:
        items = []
        for chal in challenges:
            status = '<span class="pill pill-done">已写 WP</span>' if (chal / 'WP.md').exists() else '<span class="pill pill-todo">待写 WP</span>'
            items.append(f'''  <a class="challenge-item" href="{quote(chal.name, safe='')}/">
    <span class="challenge-item-title">{chal.name}</span>
    {status}
  </a>''')
        page = f'''---
layout: default
title: {cat.name}
---

<section class="collection-hero">
  <div class="breadcrumb"><a href="{{{{ '/' | relative_url }}}}">首页</a><span>/</span><span>{cat.name}</span></div>
  <p class="eyebrow">Challenge Set</p>
  <h1>{cat.name}</h1>
  <p class="lead">本题目集共 {len(challenges)} 道题。进入单题页后，英语题面固定显示；中文题面和我的解答默认折叠，按需展开。</p>
</section>

<div class="challenge-list">
{chr(10).join(items)}
</div>
'''
        (cat / 'index.md').write_text(page, encoding='utf-8')
        (cat / 'README.md').write_text(page, encoding='utf-8')


def write_challenge_pages(cats):
    for cat, challenges in cats:
        for chal in challenges:
            has_wp = (chal / 'WP.md').exists()
            wp_block = '{% include_relative WP.md %}' if has_wp else '> 这里先留空。等我写完题解后，再让 Codex 按我的语气和语义润色。'
            py_link = ''
            if (chal / 'WP.py').exists():
                py_link = '\n\n<p><a class="pill" href="./WP.py">查看 WP 源码</a></p>'
            page = f'''---
layout: challenge
title: {chal.name}
category_title: {cat.name}
category_url: {enc_path([cat.name])}
has_wp: {str(has_wp).lower()}
---

<section class="content-card markdown-body" markdown="1">
  <h2>English Problem</h2>

{{% include_relative original.md %}}
</section>

<details class="fold-card markdown-body" markdown="1">
  <summary><h2>中文题面 / 精翻</h2></summary>

{{% include_relative translation.md %}}
</details>

<details class="fold-card markdown-body" markdown="1">
  <summary><h2>我的解答</h2></summary>

{wp_block}{py_link}
</details>
'''
            (chal / 'index.md').write_text(page, encoding='utf-8')


def main():
    cats = list_categories()
    write_data(cats)
    write_home(cats)
    write_category_pages(cats)
    write_challenge_pages(cats)
    print(f'Generated {len(cats)} categories and {sum(len(c) for _, c in cats)} challenge pages.')

if __name__ == '__main__':
    main()

