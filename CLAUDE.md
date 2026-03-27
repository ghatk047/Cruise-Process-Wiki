# Cruise Process Wiki — Claude Instructions

## Context
This is an auto-generated process wiki for Royal Caribbean Group operations.
Scripts in `scripts/` generate L1→L4 wiki pages using Qwen via Ollama.

## Hard Constraints
1. **Mermaid**: `%%{init}%%` ONLY. Never `---config---` YAML. No blank lines before `flowchart`.
2. **Diagrams**: PNG via mmdc (`-w 1920 -H 1080 --scale 2`). `<img src="assets/img/pid.png">` in HTML.
3. **Node IDs**: Start with letter. Never `1.1`. Use `S1_1` style.
4. **Arrows**: `-->` only. Never `--gt`.
5. **Sidebar**: Static HTML per page. NOT pushed after every process.
6. **Index pages**: Pushed ONCE at end of run via `push_all_index_pages()`.
7. **Home counter**: Updated after every process.
8. **Deploy marker**: `.deploy` pushed as final commit.
9. **Wiki verify**: 90s wait + HTTP 200 + content check before writing link to Excel.

## Reference
Royal Caribbean International — Icon of the Seas (250,800 GT)
Systems: Oracle SPMS, RES, MICROS, Royal App, Starlink, SAP S/4HANA, Workday, Salesforce, IDEMIA MFACE, SeaPass

## Repo
https://github.com/ghatk047/Cruise-Process-Wiki
