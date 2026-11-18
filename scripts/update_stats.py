"""Generate monochrome profile statistics from GitHub. Python standard library only."""
import datetime as dt
import html
import json
import math
import os
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
WIDTH = 1200

def esc(s):
    return html.escape(str(s), quote=True)

def svg(height, body, label):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-label="{esc(label)}">
<title>{esc(label)}</title><style>text{{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}}.label{{fill:#999;font-size:14px}}.value{{fill:#fff;font-size:38px;font-weight:700}}</style>
<rect x="1" y="1" width="1198" height="{height-2}" rx="18" fill="#090909" stroke="#303030"/>{body}</svg>'''

def write(name, height, body, label):
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / name).write_text(svg(height, body, label), encoding='utf-8')

def placeholder():
    for name, title in [('stats.svg', 'GITHUB / LIVE STATISTICS'), ('activity.svg', 'CONTRIBUTIONS / ACTIVITY MAP'), ('languages.svg', 'PUBLIC CODE / LANGUAGE DISTRIBUTION')]:
        write(name, 170, f'<text x="32" y="48" fill="#fff" font-size="18">{title}</text><text x="32" y="92" class="label">Waiting for the first GitHub Actions run.</text><text x="32" y="122" class="label">Real account data will appear here automatically.</text>', title)

QUERY = '''query($login: String!, $after: String) {
 user(login: $login) {
  login
  contributionsCollection {
   totalCommitContributions totalPullRequestContributions
   contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
  }
  repositories(first:100, after:$after, ownerAffiliations:OWNER, privacy:PUBLIC, orderBy:{field:NAME,direction:ASC}) {
   totalCount pageInfo { hasNextPage endCursor }
   nodes { isFork stargazerCount languages(first:100,orderBy:{field:SIZE,direction:DESC}) { edges { size node { name } } } }
  }
 }
}'''

def get_data(login, token):
    after = None
    repos = []
    while True:
        req = urllib.request.Request('https://api.github.com/graphql',
            data=json.dumps({'query':QUERY, 'variables':{'login':login, 'after':after}}).encode(),
            headers={'Authorization':f'Bearer {token}', 'Content-Type':'application/json', 'User-Agent':'monochrome-profile-stats'})
        with urllib.request.urlopen(req, timeout=45) as res:
            payload = json.load(res)
        if payload.get('errors'):
            raise RuntimeError(json.dumps(payload['errors']))
        user = payload['data']['user']
        if user is None:
            raise RuntimeError('GitHub user not found')
        connection = user['repositories']
        repos.extend(connection['nodes'])
        if not connection['pageInfo']['hasNextPage']:
            return user, repos
        after = connection['pageInfo']['endCursor']

def render(user, repos):
    collection = user['contributionsCollection']
    calendar = collection['contributionCalendar']
    own = [r for r in repos if not r['isFork']]
    metrics = [('PUBLIC REPOS',len(repos)),('STARS / NON-FORK REPOS',sum(r['stargazerCount'] for r in own)),('COMMITS / LAST YEAR',collection['totalCommitContributions']),('CONTRIBUTIONS / LAST YEAR',calendar['totalContributions'])]
    body = '<text x="32" y="38" class="label">GITHUB / LIVE STATISTICS</text>'
    for i,(label,value) in enumerate(metrics):
        x = 32+i*294
        if i:
            body += f'<path d="M{x-16} 65v88" stroke="#292929"/>'
        body += f'<text x="{x}" y="108" class="value">{value:,}</text><text x="{x}" y="143" class="label" style="font-size:12px">{label}</text>'
    body += f'<text x="32" y="187" class="label" style="font-size:11px">@{esc(user["login"])} / updated {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M UTC}</text>'
    write('stats.svg',210,body,'GitHub profile statistics')
    weeks = calendar['weeks']
    high = max((day['contributionCount'] for w in weeks for day in w['contributionDays']), default=0)
    shades = ['#161616','#454545','#777777','#b5b5b5','#ffffff']
    body = '<text x="32" y="38" fill="#fff" font-size="17">CONSISTENCY / CONTRIBUTION MAP</text>'
    size, gap = 15, 5
    for x, week in enumerate(weeks):
        for day in week['contributionDays']:
            date = dt.date.fromisoformat(day['date'])
            y = (date.weekday()+1)%7
            count = day['contributionCount']
            level = 0 if count == 0 else max(1,min(4,math.ceil(count/max(1,high)*4)))
            body += f'<rect x="{65+x*(size+gap)}" y="{67+y*(size+gap)}" width="{size}" height="{size}" rx="3" fill="{shades[level]}"><title>{date}: {count} contributions</title></rect>'
    body += '<text x="32" y="247" class="label" style="font-size:12px">LAST 12 MONTHS / GitHub contribution calendar</text>'
    for i,color in enumerate(shades):
        body += f'<rect x="{1020+i*22}" y="234" width="15" height="15" rx="3" fill="{color}"/>'
    write('activity.svg',275,body,'GitHub contribution calendar for the last year')
    languages = {}
    for repo in own:
        for edge in repo['languages']['edges']:
            name = edge['node']['name']
            languages[name] = languages.get(name,0)+edge['size']
    ranked = sorted(languages.items(), key=lambda pair:pair[1], reverse=True)
    selected = ranked[:5]
    if len(ranked)>5:
        selected.append(('Other',sum(v for _,v in ranked[5:])))
    total = sum(languages.values())
    body = '<text x="32" y="40" fill="#fff" font-size="17">PUBLIC CODE / LANGUAGE DISTRIBUTION</text>'
    palette = ['#ffffff','#cccccc','#999999','#777777','#555555','#353535']
    radius=85
    circ=2*math.pi*radius
    body += '<circle cx="165" cy="174" r="85" fill="none" stroke="#202020" stroke-width="23"/>'
    offset=0
    for i,(name,count) in enumerate(selected):
        fraction=count/total
        body += f'<circle cx="165" cy="174" r="85" fill="none" stroke="{palette[i]}" stroke-width="23" stroke-dasharray="{fraction*circ:.3f} {circ:.3f}" stroke-dashoffset="{-offset:.3f}" transform="rotate(-90 165 174)"/>'
        offset += fraction*circ
        col, row = i//3, i%3
        x,y = 330+col*405,108+row*62
        body += f'<rect x="{x}" y="{y-12}" width="12" height="12" rx="3" fill="{palette[i]}"/><text x="{x+25}" y="{y}" fill="#eee" font-size="17">{esc(name)}</text><text x="{x+310}" y="{y}" fill="#aaa" font-size="16">{fraction*100:.1f}%</text>'
    body += f'<text x="165" y="169" text-anchor="middle" fill="#fff" font-size="30">{len(languages)}</text><text x="165" y="193" text-anchor="middle" class="label" style="font-size:11px">LANGUAGES</text>'
    if not total:
        body += '<text x="330" y="130" class="label">No public language data yet.</text>'
    body += '<text x="32" y="302" class="label" style="font-size:12px">By code size in public, owned, non-fork repositories. Not a skill rating.</text>'
    write('languages.svg',330,body,'Language distribution by public source code size')

if __name__ == '__main__':
    if os.environ.get('PROFILE_PREVIEW') == '1':
        placeholder()
    else:
        render(*get_data(os.environ['GITHUB_REPOSITORY_OWNER'],os.environ['GITHUB_TOKEN']))
