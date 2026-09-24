# -*- coding: utf-8 -*-
"""把四个技能的所有 markdown 打成单文件 HTML 阅读版（侧边栏导航 + 全文搜索）。"""
import os, re, json, html, pathlib

SKILLS = ["skill-authoring", "skill-crafting", "skill-refining", "skill-distribution",
          "skill-evaluating", "skill-governance", "skill-orchestration", "skill-selection",
          "skill-patterns"]
TITLES = {
    "skill-authoring": "写：从零创建",
    "skill-crafting": "构：正文构件",
    "skill-refining": "优：瘦身与拆分",
    "skill-distribution": "发：发布与推广",
    "skill-evaluating": "评：有没有用",
    "skill-governance": "管：安全与合规",
    "skill-orchestration": "编：多技能编排",
    "skill-selection": "选：该不该做",
    "skill-patterns": "范式：按任务类型",
    "skill-domain-eng": "域·软件：代码与开发"
    ,"skill-domain-infra": "域·基础设施：运维与数据",
    "skill-domain-biz": "域·业务：11 类实例",
}


def esc(t):
    return html.escape(t, quote=False)


def md2html(text):
    """够用的 md→html：标题/表格/代码块/列表/粗体/行内码/引用/分隔线/链接。"""
    lines = text.split("\n")
    out, i = [], 0
    n = len(lines)

    def inline(s):
        # 行内代码先占位
        codes = []
        def stash(m):
            codes.append(m.group(1))
            return f"\x00{len(codes)-1}\x00"
        s = re.sub(r"`([^`]+)`", stash, s)
        s = esc(s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
        s = re.sub(r"\[([^\]]*)\]\(([^)]*)\)", r'<a href="\2" target="_blank">\1</a>', s)
        def restore(m):
            return f"<code>{esc(codes[int(m.group(1))])}</code>"
        s = re.sub(r"\x00(\d+)\x00", restore, s)
        return s

    while i < n:
        ln = lines[i]
        # 代码块
        if ln.strip().startswith("```"):
            lang = ln.strip()[3:].strip()
            buf, i = [], i + 1
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1
            out.append(f'<pre><code class="lang-{esc(lang)}">{esc(chr(10).join(buf))}</code></pre>')
            continue
        # 表格
        if ln.strip().startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            header = [c.strip() for c in ln.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            h = "".join(f"<th>{inline(c)}</th>" for c in header)
            body = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) for r in rows)
            out.append(f"<table><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table>")
            continue
        # 标题
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m:
            lvl = len(m.group(1))
            out.append(f'<h{lvl}>{inline(m.group(2))}</h{lvl}>')
            i += 1
            continue
        # 分隔线
        if re.match(r"^\s*---+\s*$", ln):
            out.append("<hr>"); i += 1; continue
        # 引用
        if ln.strip().startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip()); i += 1
            out.append(f"<blockquote>{inline(' '.join(buf))}</blockquote>")
            continue
        # 列表
        if re.match(r"^\s*([-*+]|\d+\.)\s+", ln):
            buf, i2 = [], i
            while i2 < n and re.match(r"^\s*([-*+]|\d+\.)\s+", lines[i2]):
                buf.append(re.sub(r"^\s*([-*+]|\d+\.)\s+", "", lines[i2])); i2 += 1
            tag = "ol" if re.match(r"^\s*\d+\.", ln) else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(b)}</li>" for b in buf) + f"</{tag}>")
            i = i2
            continue
        if ln.strip() == "":
            i += 1; continue
        out.append(f"<p>{inline(ln)}</p>")
        i += 1
    return "\n".join(out)


def strip_fm(text):
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[2].lstrip("\n"), parts[1]
    return text, ""


def main():
    docs, nav = [], []
    for sk in SKILLS:
        items = []
        # SKILL.md
        p = pathlib.Path(sk) / "SKILL.md"
        body, fm = strip_fm(p.read_text(encoding="utf-8"))
        docs.append({"id": f"{sk}::SKILL", "skill": sk, "title": "SKILL.md（路由层）",
                     "html": md2html(body), "raw": body})
        items.append({"id": f"{sk}::SKILL", "title": "SKILL.md（路由层）"})
        # references
        rdir = pathlib.Path(sk) / "references"
        for f in sorted(rdir.glob("*.md")):
            body, _ = strip_fm(f.read_text(encoding="utf-8"))
            first = next((l.lstrip("# ").strip() for l in body.split("\n") if l.startswith("# ")), f.stem)
            docs.append({"id": f"{sk}::{f.name}", "skill": sk, "title": f"{f.stem}",
                         "html": md2html(body), "raw": body})
            items.append({"id": f"{sk}::{f.name}", "title": first or f.stem})
        nav.append({"skill": sk, "label": TITLES.get(sk, sk), "items": items})

    payload = json.dumps([{"id": d["id"], "skill": d["skill"], "title": d["title"],
                           "html": d["html"], "raw": d["raw"][:6000]} for d in docs],
                          ensure_ascii=False)

    nav_html = []
    for g in nav:
        lis = "".join(
            f'<li><a href="#" data-id="{it["id"]}" onclick="go(\'{it["id"]}\');return false;">'
            f'{esc(it["title"])}</a></li>' for it in g["items"])
        nav_html.append(
            f'<div class="grp"><div class="grp-t">{esc(g["skill"])}'
            f'<span class="grp-s">{esc(g["label"])} · {len(g["items"])} 份</span></div><ul>{lis}</ul></div>')
    nav_html = "\n".join(nav_html)

    tpl = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Agent Skills 技能套件 · 阅读版</title>
<style>
*{box-sizing:border-box}
body{margin:0;font:15px/1.75 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;color:#1a1a1a;background:#fff}
#side{position:fixed;left:0;top:0;bottom:0;width:300px;overflow-y:auto;background:#fafafa;border-right:1px solid #e5e5e5;padding:14px 0}
#side h1{font-size:15px;margin:0 16px 12px;letter-spacing:.3px}
#q{width:calc(100% - 32px);margin:0 16px 12px;padding:8px 10px;border:1px solid #ddd;border-radius:6px;font-size:13px}
.grp{margin:0 0 6px}
.grp-t{padding:8px 16px 4px;font-size:12px;font-weight:700;color:#555;font-family:ui-monospace,Menlo,monospace}
.grp-s{display:block;font-weight:400;color:#999;margin-top:2px;font-family:inherit}
.grp ul{list-style:none;margin:0;padding:0 8px 4px}
.grp li a{display:block;padding:4px 8px;border-radius:5px;color:#333;text-decoration:none;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.grp li a:hover{background:#eee}
.grp li a.on{background:#2563eb;color:#fff}
#res{margin:0 8px 8px;font-size:12px;color:#666}
#res div{padding:4px 8px;border-radius:5px;cursor:pointer}
#res div:hover{background:#eee}
main{margin-left:300px;padding:28px 40px;max-width:920px}
main h1{font-size:26px;border-bottom:2px solid #eee;padding-bottom:10px;margin-top:0}
main h2{font-size:20px;margin-top:32px;border-bottom:1px solid #f0f0f0;padding-bottom:6px}
main h3{font-size:16px;margin-top:24px;color:#2563eb}
main h4{font-size:14px;margin-top:18px}
table{border-collapse:collapse;width:100%;margin:14px 0;font-size:13.5px;display:block;overflow-x:auto}
th,td{border:1px solid #e3e3e3;padding:7px 10px;text-align:left;vertical-align:top}
th{background:#f6f8fa;font-weight:600}
tr:nth-child(even) td{background:#fcfcfc}
pre{background:#f6f8fa;border:1px solid #e5e5e5;border-radius:6px;padding:12px 14px;overflow-x:auto;font-size:12.5px;line-height:1.6}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;background:#f2f4f6;padding:1px 5px;border-radius:3px;font-size:.9em}
pre code{background:none;padding:0}
blockquote{border-left:3px solid #2563eb;background:#f8faff;margin:14px 0;padding:8px 14px;color:#334}
blockquote p{margin:4px 0}
hr{border:0;border-top:1px solid #eee;margin:24px 0}
.tag{display:inline-block;font-size:11px;color:#888;background:#f0f0f0;border-radius:4px;padding:2px 7px;margin-bottom:14px;font-family:ui-monospace,monospace}
mark{background:#ffe9a8}
.hint{color:#999;font-size:13px;margin:8px 0 0}
</style></head><body>
<aside id="side">
  <h1>Agent Skills 套件 · 阅读版</h1>
  <input id="q" placeholder="搜索全文（回车 / 输入即筛）">
  <div id="res"></div>
  __NAV__
</aside>
<main id="main"><p class="hint">← 从左侧选一份开始。共 __N__ 份文档。</p></main>
<script>
const DOCS=__DATA__;
const nav=document.getElementById('side'), main=document.getElementById('main'), res=document.getElementById('res');
let cur=null;
function go(id){
  const d=DOCS.find(x=>x.id===id); if(!d) return;
  cur=id;
  document.querySelectorAll('.grp li a').forEach(a=>a.classList.toggle('on',a.dataset.id===id));
  main.innerHTML='<div class="tag">'+d.skill+' / '+d.title+'</div>'+d.html;
  main.scrollTop=0; window.scrollTo(0,0);
  location.hash=id;
}
const q=document.getElementById('q');
q.addEventListener('input',()=>{
  const s=q.value.trim().toLowerCase();
  res.innerHTML='';
  if(!s){nav.querySelectorAll('.grp').forEach(g=>g.style.display='');return;}
  nav.querySelectorAll('.grp').forEach(g=>g.style.display='none');
  const hits=DOCS.filter(d=>(d.raw+' '+d.title).toLowerCase().includes(s)).slice(0,40);
  if(!hits.length){res.innerHTML='<div style="color:#b00">无匹配</div>';return;}
  hits.forEach(d=>{
    const el=document.createElement('div');
    el.textContent=d.skill.replace('skill-','')+' · '+d.title;
    el.onclick=()=>go(d.id);
    res.appendChild(el);
  });
});
window.addEventListener('load',()=>{ if(location.hash) go(decodeURIComponent(location.hash.slice(1))); });
</script></body></html>"""

    out = (tpl.replace("__NAV__", nav_html)
              .replace("__DATA__", payload)
              .replace("__N__", str(len(docs))))
    pathlib.Path("skills-suite-reader.html").write_text(out, encoding="utf-8")
    print(f"生成 skills-suite-reader.html：{len(docs)} 份文档，{len(out)/1024:.0f} KB")


if __name__ == "__main__":
    main()
