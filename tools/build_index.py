from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {'.git', '.github', '_data', '_includes', '_layouts', '_site', '_templates', 'assets', 'tools'}

CRYPTOHACK_ORDER = {
    'Elliptic Curves': [
        ('Background', ['Background Reading']),
        ('Starter', ['Point Negation', 'Point Addition', 'Scalar Multiplication', 'Curves and Logs', 'Efficient Exchange']),
        ('Parameter Choice', ['Smooth Criminal', 'Exceptional Curves', 'Micro Transmissions', 'Elliptic Nodes', 'Moving Problems']),
        ('Parameter Choice 2', ['A Twisted Mind', 'An Exceptional Twisted Mind', 'Checkpoint', 'An Evil Twisted Mind', 'Real Curve Crypto']),
        ('Signatures', ['Digestive', 'Curveball', 'ProSign 3', 'No Random, No Bias']),
        ('Edwards Curves', ['Edwards Goes Degenerate']),
        ('Side Channels', ['Montgomerys Ladder', 'Double and Broken']),
    ]
}


def enc_path(parts):
    return '/' + '/'.join(quote(p, safe='') for p in parts) + '/'


def yq(s):
    return '"' + str(s).replace('\\', '\\\\').replace('"', '\\"') + '"'


def sort_challenges(category_name, challenges):
    by_name = {c.name: c for c in challenges}
    ordered = []
    used = set()
    for _, names in CRYPTOHACK_ORDER.get(category_name, []):
        for name in names:
            if name in by_name:
                ordered.append(by_name[name])
                used.add(name)
    ordered.extend(c for c in sorted(challenges, key=lambda x: x.name.lower()) if c.name not in used)
    return ordered


def challenge_group(category_name, challenge_name):
    for group, names in CRYPTOHACK_ORDER.get(category_name, []):
        if challenge_name in names:
            return group
    return 'Unsorted'


def grouped_challenges(category_name, challenges):
    ordered = sort_challenges(category_name, challenges)
    groups = []
    for chal in ordered:
        group = challenge_group(category_name, chal.name)
        if not groups or groups[-1][0] != group:
            groups.append((group, []))
        groups[-1][1].append(chal)
    return groups


def list_categories():
    cats = []
    for p in sorted(ROOT.iterdir(), key=lambda x: x.name.lower()):
        if not p.is_dir() or p.name in SKIP_DIRS or p.name.startswith('.'):
            continue
        challenges = [c for c in p.iterdir() if c.is_dir() and (c / 'original.md').exists()]
        if challenges:
            cats.append((p, sort_challenges(p.name, challenges)))
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
            has_attachments = (chal / 'attachments.md').exists()
            group = challenge_group(cat.name, chal.name)
            ch_yaml.append(f'    - title: {yq(chal.name)}\n      url: {yq(enc_path([cat.name, chal.name]))}\n      group: {yq(group)}\n      has_wp: {str(has_wp).lower()}\n      has_attachments: {str(has_attachments).lower()}\n')
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
        total = len(challenges)
        done = sum(1 for chal in challenges if (chal / 'WP.md').exists())
        todo = total - done
        percent = round(done * 100 / total) if total else 0
        sections = []
        running_index = 1
        for group, group_challenges in grouped_challenges(cat.name, challenges):
            items = []
            for chal in group_challenges:
                has_wp = (chal / 'WP.md').exists()
                status = '<span class="pill pill-done">已写 WP</span>' if has_wp else '<span class="pill pill-todo">待写 WP</span>'
                items.append(f'''    <a class="challenge-card" href="{quote(chal.name, safe='')}/">
      <div class="challenge-card-main">
        <span class="challenge-number">{running_index:02d}</span>
        <div>
          <h3>{chal.name}</h3>
          <p>英语题面固定展示；中文精翻和个人解答在单题页内展开阅读。</p>
        </div>
      </div>
      <div class="challenge-card-foot">
        {status}
        <span class="enter-link">进入题目 →</span>
      </div>
    </a>''')
                running_index += 1
            sections.append(f'''  <section class="challenge-group">
    <div class="challenge-group-head">
      <h3>{group}</h3>
      <span>{len(group_challenges)} challenges</span>
    </div>
    <div class="challenge-grid">
{chr(10).join(items)}
    </div>
  </section>''')
        page = f'''---
layout: default
title: {cat.name}
---

<section class="collection-hero collection-hero-compact">
  <div class="breadcrumb"><a href="{{{{ '/' | relative_url }}}}">首页</a><span>/</span><span>{cat.name}</span></div>
  <p class="eyebrow">Challenge Set</p>
  <h1>{cat.name}</h1>
  <p class="lead">这一页按照 CryptoHack 原站顺序排版。先看题目列表，进入单题后再看固定英文题面、展开中文精翻或展开我的解答。</p>
</section>

<section class="collection-overview" aria-label="题目集概览">
  <div class="overview-card overview-main">
    <h2>阅读顺序</h2>
    <ol>
      <li>按照 CryptoHack 原站分组和顺序从上到下阅读。</li>
      <li>默认先读英文题面，保持原题语境。</li>
      <li>需要时展开中文精翻，对照理解细节。</li>
      <li>最后展开我的解答，按思路复盘。</li>
    </ol>
  </div>
  <div class="overview-card progress-card">
    <h2>整理进度</h2>
    <div class="progress-number">{done}<span>/ {total}</span></div>
    <div class="progress-track"><span style="width: {percent}%"></span></div>
    <p>{done} 道已写 WP，{todo} 道待补题解。</p>
  </div>
</section>

<div class="challenge-section-head">
  <h2>题目列表</h2>
  <span>CryptoHack order · {total} challenges</span>
</div>
<div class="challenge-groups">
{chr(10).join(sections)}
</div>
'''
        (cat / 'index.md').write_text(page, encoding='utf-8')
        (cat / 'README.md').write_text(page, encoding='utf-8')


def markdownified_include(filename):
    var = filename.replace('.', '_').replace('-', '_') + '_content'
    return f'''{{% capture {var} %}}{{% include_relative {filename} %}}{{% endcapture %}}
{{{{ {var} | markdownify }}}}'''


def write_challenge_pages(cats):
    for cat, challenges in cats:
        for chal in challenges:
            has_wp = (chal / 'WP.md').exists()
            has_attachments = (chal / 'attachments.md').exists()
            wp_block = markdownified_include('WP.md') if has_wp else '<p class="muted-note">这里先留空。等我写完题解后，再让 Codex 按我的语气和语义润色。</p>'
            attachments_block = ''
            if has_attachments:
                attachments_block = f'''
<details class="fold-card attachment-card markdown-body">
  <summary><h2>题目附件 / Challenge Files</h2></summary>

{markdownified_include('attachments.md')}
</details>
'''
            py_link = ''
            if (chal / 'WP.py').exists():
                py_link = '\n\n<p class="download-row"><a class="download-link" href="./WP.py" download>下载解题代码（WP.py）</a></p>'
            page = f'''---
layout: challenge
title: {chal.name}
category_title: {cat.name}
category_url: {enc_path([cat.name])}
has_wp: {str(has_wp).lower()}
---

<section class="content-card markdown-body">
  <h2>English Problem</h2>

{markdownified_include('original.md')}
</section>

<details class="fold-card markdown-body">
  <summary><h2>中文题面 / 精翻</h2></summary>

{markdownified_include('translation.md')}
</details>

{attachments_block}<details class="fold-card markdown-body">
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
