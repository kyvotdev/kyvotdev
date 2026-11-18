from pathlib import Path
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1]

def badge(label,logo=None,light=False):
    params='style=for-the-badge'
    if logo:
        params+=f'&logo={logo}&logoColor={"000000" if light else "FFFFFF"}'
    return f'![{label}](https://img.shields.io/badge/{quote(label.replace("-","--").replace("_","__"),safe="")}-{"FFFFFF" if light else "111111"}?{params})'

stack=[
('LANGUAGES',[('Python','python'),('C++','cplusplus'),('Rust','rust')]),
('BACKEND / API / BOTS',[('FastAPI','fastapi'),('Litestar',None),('Django','django'),('Django Ninja',None),('aiogram',None),('REST API',None)]),
('DATABASES / ORM',[('PostgreSQL · PRIMARY','postgresql',True),('MariaDB','mariadb'),('MongoDB','mongodb'),('SQLAlchemy','sqlalchemy'),('Django ORM','django')]),
('FRONTEND',[('Next.js','nextdotjs'),('Nuxt.js','nuxt')]),
('AUTOMATION / TESTING',[('Playwright',None),('Selenium','selenium'),('PyScraper',None),('Custom scripts',None)]),
('SYSTEM / VERSION CONTROL',[('Linux','linux',True),('Git','git',True),('Shell','gnubash'),('SSH',None),('systemd','systemd')]),
]
stack_md='\n\n'.join('<samp>'+name+'</samp>\n\n'+'\n'.join(badge(*entry) for entry in items) for name,items in stack)

for lang in ['ru','en']:
    ru=lang=='ru'
    nav='**Русский** &nbsp; / &nbsp; [English](./README.en.md)' if ru else '[Русский](./README.md) &nbsp; / &nbsp; **English**'
    intro=('Пишу код на разных языках и работаю с разными технологиями. Мой фокус — **backend, API, безопасные сайты и автоматизация**. Разрабатываю frontend, Telegram-ботов и инструменты для тестирования на проникновение. Использую **Python, C++ и Rust**; стек выбираю под задачу.' if ru else 'I write code in multiple languages and work across technologies. My focus is **backend development, APIs, secure websites and automation**. I also build frontends, Telegram bots and penetration testing tools. I use **Python, C++ and Rust**, choosing the stack to fit the problem.')
    focus=('''| Направление | Что делаю |
| :--- | :--- |
| **Backend & API** | Проектирую и разрабатываю API, интегрирую внешние сервисы, реализую бизнес-логику и аутентификацию. FastAPI, Litestar, Django, Django Ninja. |
| **Bots** | Создаю Telegram-ботов на aiogram: обработчики, сценарии взаимодействия, интеграции с API и базами данных. |
| **Data** | **PostgreSQL — основная БД.** Также работаю с MariaDB и MongoDB; использую SQLAlchemy и Django ORM, проектирую схемы, запросы и миграции. |
| **Frontend** | Разрабатываю сайты и интерфейсы на Next.js и Nuxt.js, соединяю frontend с backend через API. |
| **Automation** | Пишу скрипты, автоматизирую браузерные сценарии, сбор и обработку данных. Playwright, Selenium, PyScraper. |
| **Security** | Создаю сайты с учётом безопасности, провожу проверки веб-приложений и пишу собственные скрипты для пентеста. |''' if ru else '''| Area | What I do |
| :--- | :--- |
| **Backend & API** | Design and build APIs, integrate external services, implement business logic and authentication. FastAPI, Litestar, Django, Django Ninja. |
| **Bots** | Build Telegram bots with aiogram: handlers, interaction flows, API integrations and databases. |
| **Data** | **PostgreSQL is my primary database.** Also work with MariaDB and MongoDB; use SQLAlchemy and Django ORM for schemas, queries and migrations. |
| **Frontend** | Build websites and interfaces with Next.js and Nuxt.js, connecting frontends to backends through APIs. |
| **Automation** | Write scripts and automate browser workflows, data collection and processing with Playwright, Selenium and PyScraper. |
| **Security** | Build websites with security in mind, assess web applications and write custom penetration testing scripts. |''')
    linux=('''**Linux — полноценная рабочая среда.** Работаю из терминала: shell-скрипты, SSH, пользователи и права доступа, процессы и службы, systemd, пакеты, логи, сеть и настройка окружения. Разворачиваю приложения, разбираюсь с неполадками, автоматизирую обслуживание и уделяю внимание защите сервера.

**Git — ежедневный рабочий инструмент.** Работаю с ветками и удалёнными репозиториями, использую merge, rebase и cherry-pick, разрешаю конфликты, разбираюсь в истории изменений и восстанавливаю нужные состояния через reflog. Поддерживаю понятную историю коммитов и работаю через pull requests.''' if ru else '''**Linux is my full working environment.** I work in the terminal with shell scripts, SSH, users and permissions, processes and services, systemd, packages, logs, networking and environment configuration. I deploy applications, troubleshoot issues, automate maintenance and pay attention to server hardening.

**Git is part of my daily workflow.** I work with branches and remotes, use merge, rebase and cherry-pick, resolve conflicts, investigate history and recover states with reflog. I keep commit history understandable and collaborate through pull requests.''')
    security=('''Безопасность учитываю при разработке: аутентификация и авторизация, проверка входных данных, работа с секретами, настройки доступа и защита данных.

Могу протестировать сайт на безопасность: проверить API, сессии, права доступа и конфигурацию, найти слабые места и предложить исправления. Для тестирования на проникновение и повторяемых проверок пишу собственные скрипты и автоматизацию.

**Приватность и анонимность в сети** — отдельная область интереса: минимизация цифрового следа, защита личных данных, изоляция окружений и понимание того, какую информацию раскрывают приложения и сетевые сервисы.''' if ru else '''I account for security during development: authentication and authorization, input validation, secret management, access configuration and data protection.

I can assess a website's security by examining APIs, sessions, access controls and configuration, identifying weaknesses and suggesting fixes. I write custom scripts and automation for penetration testing and repeatable checks.

**Online privacy and anonymity** are another area of interest: reducing digital footprints, protecting personal data, isolating environments and understanding what applications and network services reveal.''')
    oss=('''Ценю **open source**: открытый код, прозрачные решения и обмен знаниями. Создаю инструменты, которые можно изучать, дорабатывать и использовать повторно. Мне интересно разбирать чужие реализации и делиться своими находками.''' if ru else '''I value **open source**: accessible code, transparent solutions and shared knowledge. I build tools that can be studied, extended and reused. I enjoy exploring other implementations and sharing what I learn.''')
    note=('Статистика обновляется автоматически. Диаграмма языков показывает объём кода в публичных собственных репозиториях без форков, а не уровень владения технологиями.' if ru else 'Statistics update automatically. Language distribution reflects code size in public, owned, non-fork repositories, rather than proficiency.')
    body=f'''<!-- Replace kyvotdev and yupirut@protonmail.com. Setup: see SETUP.md. -->
<div align="center">

{nav}

<br />
<br />

<img src="./assets/hero.gif" width="100%" alt="BUILD. BREAK. UNDERSTAND. — animated terminal" />

<br />
<br />

<samp>BACKEND / FRONTEND / SECURITY / AUTOMATION</samp>

<br />
<br />

<img src="./assets/pulse.gif" width="100%" alt="" />

<br />
<br />

[![GitHub](https://img.shields.io/badge/GITHUB-111111?style=for-the-badge&logo=github&logoColor=FFFFFF)](https://github.com/kyvotdev)
[![Contact](https://img.shields.io/badge/CONTACT-FFFFFF?style=for-the-badge&logo=protonmail&logoColor=000000)](mailto:yupirut@protonmail.com)

</div>

<br />

## `01` / {'Обо мне' if ru else 'About me'}

{intro}

> {'От интерфейса до базы данных. От работающего кода до понимания его уязвимостей.' if ru else 'From the interface to the database. From working code to understanding its weaknesses.'}

<br />

## `02` / {'Что я делаю' if ru else 'What I do'}

{focus}

<br />

## `03` / {'Мой стек' if ru else 'My stack'}

{stack_md}

<br />

## `04` / Linux & Git

{linux}

<br />

## `05` / {'Безопасность и приватность' if ru else 'Security & privacy'}

{security}

<br />

## `06` / Open source

{oss}

<br />

## `07` / {'Активность на GitHub' if ru else 'GitHub activity'}

<img src="./assets/stats.svg" width="100%" alt="GitHub statistics" />

<br />

<img src="./assets/activity.svg" width="100%" alt="Contribution calendar — last 12 months" />

<br />

<img src="./assets/languages.svg" width="100%" alt="Public repository language distribution" />

<sub>{note}</sub>

<br />
<br />

---

<div align="center">

<br />

<samp>BUILD WITH PURPOSE. QUESTION EVERY ASSUMPTION.</samp>

<br />
<br />

{nav}

<br />

</div>
'''
    (ROOT/('README.md' if ru else 'README.en.md')).write_text(body,encoding='utf-8')
