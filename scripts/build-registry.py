#!/usr/bin/env python3
"""从 SKILL.md 自动构建 registry.json"""

import json, os, re, glob
from datetime import datetime, timezone

def extract_description(content):
    """从 SKILL.md frontmatter 提取 description"""
    # 先试多行 literal block: description: |\n  内容
    m2 = re.search(r'^description:\s*(\|)\s*$(.+?)^---', content, re.MULTILINE | re.DOTALL)
    if m2:
        lines = [l.strip() for l in m2.group(2).split('\n') if l.strip()]
        return ' '.join(lines)
    # 单行: description: 拆分prd
    m1 = re.search(r'^description:\s*(\S.*?)$', content, re.MULTILINE)
    if m1:
        return m1.group(1).strip().strip('"').strip("'")
    return ''

def skill_entrypoints(base_dir):
    for directory in sorted(glob.glob(os.path.join(base_dir, '*'))):
        if not os.path.isdir(directory):
            continue
        direct_entrypoint = os.path.join(directory, 'SKILL.md')
        if os.path.isfile(direct_entrypoint):
            yield direct_entrypoint
            continue
        for child in sorted(glob.glob(os.path.join(directory, '*'))):
            entrypoint = os.path.join(child, 'SKILL.md')
            if os.path.isdir(child) and os.path.isfile(entrypoint):
                yield entrypoint

def scan_skills(base_dir, namespace):
    skills = []
    for md_path in skill_entrypoints(base_dir):
        d = os.path.dirname(md_path)
        name = os.path.basename(d)
        with open(md_path) as f:
            desc = extract_description(f.read())
        skills.append({
            'name': name,
            'namespace': namespace,
            'description': desc[:300],
            'path': os.path.relpath(d, '.').replace(os.sep, '/') + '/'
        })
    return skills

def write_skills_index(skills):
    """Keep the human-readable index derived from the same source as registry.json."""
    labels = {'curated': '精选技能 (curated/)', 'community': '社区技能 (community/)'}
    lines = ['# Skills 清单', '', '> 仓库内所有技能的快速索引。', '']
    for namespace in ('curated', 'community'):
        lines.extend([f'## {labels[namespace]}', '', '| 技能 | 说明 |', '|------|------|'])
        for skill in (s for s in skills if s['namespace'] == namespace):
            description = skill['description'].replace('|', '\\|').replace('\n', ' ')
            relative_path = skill['path'].removeprefix(f"{namespace}/").rstrip('/')
            label = relative_path if '/' in relative_path else skill['name']
            lines.append(f"| {label} | {description or '—'} |")
        lines.append('')
    with open('SKILLS.md', 'w') as f:
        f.write('\n'.join(lines))

def main():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(repo_dir)

    skills = []
    skills += scan_skills('curated', 'curated')
    skills += scan_skills('community', 'community')

    registry = {
        'version': 1,
        'description': 'agent-skills 技能注册表 — 机器可读索引',
        'updated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'skills': skills
    }

    with open('registry.json', 'w') as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)

    write_skills_index(skills)

    print(f'✅ registry.json and SKILLS.md updated — {len(skills)} skills')
    for s in skills:
        print(f'  {s["namespace"]:>10}/{s["name"]:<30} {s["description"][:50]}')

if __name__ == '__main__':
    main()
