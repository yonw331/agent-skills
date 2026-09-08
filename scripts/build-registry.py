#!/usr/bin/env python3
"""从 SKILL.md 自动构建 registry.json"""

import json, os
from datetime import datetime, timezone
from skill_metadata import read_skill, skill_entrypoints

def scan_skills(base_dir, namespace):
    skills = []
    for md_path in skill_entrypoints(base_dir):
        d = os.path.dirname(md_path)
        name = os.path.basename(d)
        desc = " ".join(read_skill(md_path)["description"].split())
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
