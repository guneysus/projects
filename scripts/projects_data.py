# -*- coding: utf-8 -*-
"""
Project metadata for the guneysus.github.io-projects index.

Each entry:
  name          : repository/project name (folder name in the archive)
  description   : short description (from GitHub/GitLab metadata)
  visibility    : public | private
  fork          : True if it is a fork
  last_activity : last activity date (YYYY-MM-DD)
  archived      : True if archived in the monorepo
  source        : "github" | "gitlab"  (original hosting platform)
  owner         : original owner/namespace
  original_url  : link to the original repository
  archive_path  : path inside the archive monorepo (relative to archive root)
  archive_repo  : which archive monorepo holds it
"""

# ---------------------------------------------------------------------------
# Archive monorepos (origins)
# ---------------------------------------------------------------------------
ARCHIVES = {
    "gitlab-archive": {
        "label": "GitLab Archive",
        "local_path": r"X:\git\gitlab.com\guneysu\gitlab-archive",
        "origins": [
            "git@github.com:guneysus/archive.git",
            "git@gitlab.com:guneysu/gitlab-archive.git",
        ],
    },
    "github-guneysus-archive": {
        "label": "GitHub Archive",
        "local_path": r"X:\git\gitlab.com\guneysu\github-guneysus-archive",
        "origins": [
            "git@gitlab.com:guneysu/github-guneysus-archive.git",
            "gitea@192.168.1.19:guneysu.dev/github-guneysus-archive.git",
        ],
    },
}

# ---------------------------------------------------------------------------
# Projects from gitlab-archive  (repos/guneysu + repos/guneysu.dev)
# ---------------------------------------------------------------------------
GITLAB_ARCHIVE_PROJECTS = [
    # --- guneysu namespace ---
    dict(name="backstage", description="", visibility="private", fork=False,
         last_activity="2026-08-02", archived=True, source="gitlab",
         owner="guneysu", archive_path="repos/guneysu/backstage"),
    dict(name="docker-apps", description="", visibility="private", fork=False,
         last_activity="2026-08-02", archived=True, source="gitlab",
         owner="guneysu", archive_path="repos/guneysu/docker-apps"),
    dict(name="dotnet-extension-methods", description="", visibility="private", fork=False,
         last_activity="2026-08-02", archived=True, source="gitlab",
         owner="guneysu", archive_path="repos/guneysu/dotnet-extension-methods"),
    dict(name="fullstack-dotnet-template", description="", visibility="private", fork=False,
         last_activity="2026-08-02", archived=True, source="gitlab",
         owner="guneysu", archive_path="repos/guneysu/fullstack-dotnet-template"),
    dict(name="gitops-config", description="k8s manifests files for continious deployment",
         visibility="private", fork=False, last_activity="2026-08-02", archived=True,
         source="gitlab", owner="guneysu", archive_path="repos/guneysu/gitops-config"),
    dict(name="homelab-caddy-config", description="", visibility="private", fork=False,
         last_activity="2026-08-02", archived=True, source="gitlab",
         owner="guneysu", archive_path="repos/guneysu/homelab-caddy-config"),
    dict(name="latex-docs", description="", visibility="private", fork=False,
         last_activity="2026-08-02", archived=True, source="gitlab",
         owner="guneysu", archive_path="repos/guneysu/latex-docs"),
    dict(name="parsers", description="", visibility="private", fork=False,
         last_activity="2026-08-02", archived=True, source="gitlab",
         owner="guneysu", archive_path="repos/guneysu/parsers"),
    dict(name="project-incubation", description="", visibility="private", fork=False,
         last_activity="2026-08-02", archived=True, source="gitlab",
         owner="guneysu", archive_path="repos/guneysu/project-incubation"),
    dict(name="prompt-library", description="LLM Prompts", visibility="private", fork=False,
         last_activity="2026-08-02", archived=True, source="gitlab",
         owner="guneysu", archive_path="repos/guneysu/prompt-library"),
    dict(name="surmene", description="", visibility="private", fork=False,
         last_activity="2026-08-02", archived=True, source="gitlab",
         owner="guneysu", archive_path="repos/guneysu/surmene"),
    dict(name="templates", description="", visibility="private", fork=False,
         last_activity="2026-08-02", archived=True, source="gitlab",
         owner="guneysu", archive_path="repos/guneysu/templates"),
    dict(name="torque-collector", description="", visibility="private", fork=False,
         last_activity="2026-08-02", archived=True, source="gitlab",
         owner="guneysu", archive_path="repos/guneysu/torque-collector"),
    # --- guneysu.dev namespace ---
    dict(name="acme-welcome-dotnet", description="", visibility="private", fork=False,
         last_activity="2026-08-02", archived=True, source="gitlab",
         owner="guneysu.dev", archive_path="repos/guneysu.dev/acme-welcome-dotnet"),
    dict(name="cloudflare-worker-get-user", description="", visibility="private", fork=False,
         last_activity="2026-08-02", archived=True, source="gitlab",
         owner="guneysu.dev", archive_path="repos/guneysu.dev/cloudflare-worker-get-user"),
    dict(name="form-flow", description="", visibility="private", fork=False,
         last_activity="2026-08-02", archived=True, source="gitlab",
         owner="guneysu.dev", archive_path="repos/guneysu.dev/form-flow"),
    dict(name="skaf", description="", visibility="private", fork=False,
         last_activity="2026-08-02", archived=True, source="gitlab",
         owner="guneysu.dev", archive_path="repos/guneysu.dev/skaf"),
]

# ---------------------------------------------------------------------------
# Projects from github-guneysus-archive  (repos/github.com/guneysus-archieve)
# ---------------------------------------------------------------------------
GITHUB_ARCHIVE_PROJECTS = [
    dict(name=".cli-template_dotnet", description=".NET CLI Tool Template", visibility="private", fork=False, last_activity="2024-12-11", archived=False, source="github", owner="guneysus"),
    dict(name="aes", description="AES-256 block cipher", visibility="public", fork=True, last_activity="2023-01-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="aes_dust", description="Unlicensed tiny / small portable implementation of 128/256-bit AES encryption in C, x86, AMD64, ARM32 and ARM64 assembly", visibility="public", fork=True, last_activity="2021-02-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="ai", description="", visibility="public", fork=False, last_activity="2026-06-29", archived=False, source="github", owner="guneysus"),
    dict(name="algoritms", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="analyzers", description="C# code analyzers", visibility="private", fork=False, last_activity="2026-07-31", archived=False, source="github", owner="guneysus"),
    dict(name="app.namazvaktim", description="https://guneysus.github.io/app.namazvaktim/", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="asm", description="Learning assembly for linux-x64", visibility="public", fork=True, last_activity="2023-01-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="asp-net-sample-apps", description="", visibility="private", fork=False, last_activity="2026-07-31", archived=False, source="github", owner="guneysus"),
    dict(name="aspcore-sample-apps", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="aspnet-core-streaming", description="ASP.Net Streaming to the Client", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="aws_list_all", description="List all your AWS resources, all regions, all services.", visibility="public", fork=True, last_activity="2021-02-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="bginfz", description="", visibility="private", fork=False, last_activity="2026-07-31", archived=False, source="github", owner="guneysus"),
    dict(name="bin", description="", visibility="public", fork=True, last_activity="2023-01-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="blog-from-scratch", description="", visibility="private", fork=False, last_activity="2026-07-31", archived=False, source="github", owner="guneysus"),
    dict(name="blog-v1", description="blog sources", visibility="private", fork=False, last_activity="2025-09-06", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="blog-v2", description="", visibility="private", fork=False, last_activity="2025-10-11", archived=False, source="github", owner="guneysus"),
    dict(name="blog-v3", description="", visibility="private", fork=False, last_activity="2026-07-31", archived=False, source="github", owner="guneysus"),
    dict(name="blog-v3-theme", description="", visibility="private", fork=False, last_activity="2025-06-05", archived=False, source="github", owner="guneysus"),
    dict(name="boilerplate", description="Boilerplate file templates to be used by copier", visibility="public", fork=False, last_activity="2025-10-03", archived=False, source="github", owner="guneysus"),
    dict(name="browser-pick", description="Android like selecting application for specific URLs, protocols etc. [WIP]", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="bug.report-docker-3106", description="", visibility="public", fork=False, last_activity="2023-01-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="calc.asm", description="Minimal arithmetic calculator in x86 assembly", visibility="public", fork=True, last_activity="2023-01-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="calcx", description="Calcx", visibility="public", fork=False, last_activity="2026-07-31", archived=False, source="github", owner="guneysus"),
    dict(name="chess.js", description="A brand new OOP Chess modeling with ES6", visibility="public", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="coding-interview-university", description="A complete computer science study plan to become a software engineer.", visibility="public", fork=True, last_activity="2021-05-08", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="configs", description="", visibility="private", fork=False, last_activity="2026-07-31", archived=False, source="github", owner="guneysus"),
    dict(name="CoreHook", description="A library that simplifies intercepting application function calls using managed code and the .NET Core runtime", visibility="public", fork=True, last_activity="2022-10-13", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="Craig-s-Utility-Library", description="Main repo for Craig's Utility Library", visibility="public", fork=True, last_activity="2023-01-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="crem", description="Crud Made Easy for .asp net core", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="CSharpExpressionTreesInTheRealWorld", description="Slides plus links for my talk, C# Expression Trees in the Real World", visibility="public", fork=True, last_activity="2023-01-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="cv", description="my cv", visibility="private", fork=False, last_activity="2026-05-17", archived=False, source="github", owner="guneysus"),
    dict(name="de4dot", description=".NET deobfuscator and unpacker.", visibility="public", fork=True, last_activity="2023-04-05", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="deployement-templates", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="Design-Patterns", description="You can find here bunch of useful design patterns to help your project", visibility="public", fork=True, last_activity="2021-02-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="Devup", description="YAML based, docker-compose like tools, helping to start development environments. The idea @ybrs's project-switcher, reimplemented with .NET.", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="dingil", description="Generate POCO class and assembly by only defining an YAML file", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="dinq", description="Dynamic Query Tool", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="dlr", description="Dynamic Language Runtime", visibility="public", fork=True, last_activity="2021-01-03", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="do-not-reinvent", description="My technical memo", visibility="public", fork=True, last_activity="2023-01-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="docker-apps", description="", visibility="private", fork=False, last_activity="2026-07-31", archived=False, source="github", owner="guneysus"),
    dict(name="docker-baseimage-rdesktop", description="base image for xrdp containers", visibility="public", fork=True, last_activity="2022-02-26", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="docker-baseimage-rdesktop-web", description="Custom all in one container for running GUI apps from a web browser", visibility="public", fork=True, last_activity="2025-01-15", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="docker-images", description="docker images that updated regulary by TravisCI", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="docker-rdesktop", description="", visibility="public", fork=True, last_activity="2022-02-26", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="DoH-IP-blocklists", description="This repo contains the domain names and the IPv4/IPv6 addresses of public DoH server", visibility="public", fork=True, last_activity="2026-08-01", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="dotfiles", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="dotnet-core-plugins", description=".NET core plugging architechture", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="dotnet-dynamic-assembly-loading", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="dotnet-expression-trees", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="dotnet-how-to-debug-source-generator-vs2022", description="Step by step guide on how to debug a C# SourceGenerator in Visual Studio 2022", visibility="private", fork=False, last_activity="2026-07-31", archived=False, source="github", owner="guneysus"),
    dict(name="dotnet-html-gen", description="Generate HTML with fluent API", visibility="public", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="dotnet-mock-server", description="declarative mock server with fake data generation capabilities for .NET Core 2.1+", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="dotnet-reversing", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="dotnet-sandbox", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="dotnet-sandbox-2", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="dotnetcore-imageserver", description="aspnet core image resizing web app with upload, delete support via REST interface", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="DotNetHooking", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="DotNextMoscow2019", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="git-ctf", description="Hey! Git gurus, capture the flag from this repository 🐱‍👤 🏴", visibility="public", fork=False, last_activity="2026-05-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="git-presentation", description='This repo (will) contain the presentation "Git & Github Guide"', visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="har-spec", description="The HTTP Archive Spec", visibility="public", fork=True, last_activity="2023-01-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="heceleme", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="Heijden.Dns", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="humanizer-tr", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="ildasm", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="ILProgramming", description="Coding close to the .NET Runtime using ILProj, ildasm, ilasm", visibility="public", fork=True, last_activity="2023-02-18", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="ILProj", description="", visibility="public", fork=True, last_activity="2023-01-24", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="interview-downtime-alerter-service", description="Downtime Alert Service with ASP.Net Core", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="interview-project-mars-rover-tdd", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="kvb-iot-demo", description="", visibility="public", fork=False, last_activity="2023-01-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="LightQuery", description="Lightweight solution for sorting and paging Asp.Net Core API results", visibility="public", fork=True, last_activity="2021-04-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="loadlibrary", description="Porting Windows Dynamic Link Libraries to Linux", visibility="public", fork=True, last_activity="2021-02-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="managed-x86", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="MethodRedirect", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="minsk", description="This repo contains Minsk, a handwritten compiler in C#. It illustrates basic concepts of compiler construction and how one can tool the language inside of an IDE by exposing APIs for parsing and type checking.", visibility="public", fork=True, last_activity="2023-01-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="mssql-TableTruncate", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="mssql-tools", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="mssqlfs", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="musahid", description="", visibility="public", fork=False, last_activity="2023-01-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="nemerle", description="Nemerle language. Main repository.", visibility="public", fork=True, last_activity="2022-12-22", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="NGINX-Demos", description="NGINX and NGINX Plus demos", visibility="public", fork=True, last_activity="2021-04-04", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="NRules", description="Rules engine for .NET, based on the Rete matching algorithm, with internal DSL in C#.", visibility="public", fork=True, last_activity="2021-11-03", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="ntpserver", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="Object-Initialization-in-CSharp", description="A C# Pill that highlights the order in which the fields, properties and constructors, both static and instance, are initialized in C#.", visibility="public", fork=True, last_activity="2022-12-19", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="openresty-gateway-waf", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="openresty-twitter-clone", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="Parallel-Evolution", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="perfect-presentation", description="This project contains all steps which you need to make a perfect presentation. You creating a wonderful presentation is our role and our priority.", visibility="public", fork=True, last_activity="2021-02-25", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="performance-optimization", description="Guidance on how to observe, measure, and correct common issues in a cloud-based system.", visibility="public", fork=True, last_activity="2023-01-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="peview", description="Web based HEX viewer. The goal was developing a Web based PE Viewer.", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="PiOBDII", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="playbook", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="pose", description="Replace any .NET method (including static and non-virtual) with a delegate", visibility="public", fork=True, last_activity="2023-01-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="prayer-times-android", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="prayer-times-api", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="predicate-builder", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="project-switcher", description="hassle free project switching", visibility="public", fork=True, last_activity="2023-01-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="pw", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="python-sqlite-json-explorer", description="", visibility="public", fork=False, last_activity="2023-01-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="pytotube", description="Simple 1D Thermal problem solver", visibility="public", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="Random-Problems", description="What actually happens when we use a Random instance from multiple threads? Can we do something to make it thread-safe?", visibility="public", fork=True, last_activity="2021-12-16", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="sandbox-net", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="selenium-webdriver-winappdriver-example", description="An example of selenium-webdriver and winappdriver integration", visibility="public", fork=True, last_activity="2022-01-04", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="sensorfusion-gps-process", description="", visibility="public", fork=False, last_activity="2023-01-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="sid", description="Simple Declarative Web Apps", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="side-projects", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="sitemap-parser", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="snake", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="snow-flakes-js", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="speedcrunch.net", description="Parser based expression evaluator", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="sql-injection", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="sscli20_20060311", description="Version: 2.0 Date Published: 3/23/2006. The Shared Source CLI is a compressed archive of the source code to a working implementation of the ECMA CLI and the ECMA C# language specification. This implementation builds and runs on Windows XP.", visibility="public", fork=True, last_activity="2023-01-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="symreader-converter", description="Converts between Windows PDB and Portable PDB formats.", visibility="public", fork=True, last_activity="2021-02-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="testere", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="Todos", description="Various todo list backend API implementations", visibility="public", fork=True, last_activity="2021-02-26", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="underscore-net-docs", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="underscore.net", description="Simple, Handy Toolkits for .NET Core projects with high test coverage.", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="understanding-csrf", description="What are CSRF tokens and how do they work?", visibility="public", fork=True, last_activity="2023-01-28", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="unicode_tr", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="uxplay", description="", visibility="public", fork=True, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="Virtual-in-Constructor", description="This pill demonstrates why it is not a good idea to call abstract or virtual methods from the constructor.", visibility="public", fork=True, last_activity="2022-12-19", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="vulnerable-api", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="web-layouts", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="wox-prayer-times-plugin", description="wox prayer times plugin", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="wxdatcom-2", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
]

# Projects present in the archive folder but NOT in the README table (extra)
GITHUB_ARCHIVE_EXTRA = [
    ".template-powershell-core-binary-module", "Antlr4.Extension", "ascii_b64",
    "asprofiled", "bin_b64", "calcpaper", "clr-profiling", "csharp-connected-disconnected",
    "csharp.dotnet.custom-config-generator", "csharp.generic.db.view",
    "csharp.hw.northwind.sepet", "csharp.mvc.blog.hw", "csharp.mvc.nw.intro",
    "csharp.oop.uygulama", "csharp.winforms.autocomplete", "des", "Disposable-Pattern",
    "dot",
]

# Full metadata for the extra projects found in the archive folder
GITHUB_ARCHIVE_EXTRA_PROJECTS = [
    dict(name=".template-powershell-core-binary-module", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="Antlr4.Extension", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="ascii_b64", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="asprofiled", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="bin_b64", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="calcpaper", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="clr-profiling", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="csharp-connected-disconnected", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="csharp.dotnet.custom-config-generator", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="csharp.generic.db.view", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="csharp.hw.northwind.sepet", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="csharp.mvc.blog.hw", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="csharp.mvc.nw.intro", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="csharp.oop.uygulama", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="csharp.winforms.autocomplete", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="des", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="Disposable-Pattern", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
    dict(name="dot", description="", visibility="private", fork=False, last_activity="2024-10-14", archived=True, source="github", owner="guneysus-archieve"),
]

# ---------------------------------------------------------------------------
# Duplicates are detected automatically by the generator: any project name
# that appears in more than one archive monorepo is flagged as a duplicate.
# The same project may have multiple origins and possibly different commit
# histories across archives, so each copy is kept as its own entry.
# ---------------------------------------------------------------------------