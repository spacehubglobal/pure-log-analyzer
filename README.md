# Semantic Log Analyzer for Telecom Core Networks (pure Python)

No pip installs, no compiled packages - standard library only (Python 3.8+).

## Run
    python server.py          # opens http://127.0.0.1:8000 in your browser
    python server.py 9000     # optional custom port

Drag a log file onto the page (or click "Load sample log").

## Files
- server.py   - tiny local web server (http.server)
- analyzer.py - regex parsing + aggregation
- catalog.py  - error-code knowledge base (add your own codes here)
- index.html  - dashboard UI (HTML/CSS/JS, no external libraries or CDNs)
- make_sample.py - regenerates sample_logs/This_Is_A_Sample.log

Everything runs on 127.0.0.1; uploaded logs never leave your machine.
