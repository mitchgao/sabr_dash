# SABR Dash

A small Dash web application for viewing SABR-related visualisations (smile, surface, graphs).

**Quick Start**

- **Python version:** 3.8+
- **Tested with:** Dash, dash-bootstrap-components

1. (Optional) Create a virtual environment and activate it (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
pip install --upgrade pip
```

2. Install runtime dependencies:

```powershell
pip install dash dash-bootstrap-components
```

3. Run the app (from the project root):

```powershell
python .\app.py
```

Open http://127.0.0.1:5050 in your browser.

**Project Layout**

- `app.py` — main Dash app, layout and routing.
- `pages/` — folder containing page modules. Each page module should expose a variable with the page layout (for example `landing_page`, `smile_page`, `surface_page`).
  - `pages/landing.py`
  - `pages/smile.py`
  - `pages/surface.py`

**Adding a new page**

1. Create a new file in `pages/`, e.g. `pages/newpage.py`.
2. Define a page layout variable (match naming convention used in `app.py`), for example:

```python
from dash import html

newpage = html.Div([html.H3("New Page"), html.P("Content here")])
```

3. Import the variable in `app.py`, add a `dbc.NavLink` for navigation, and add a branch in `render_page_content` to return the page for the desired pathname.

**Notes & Tips**

- The app uses `suppress_callback_exceptions=True` in case pages register callbacks dynamically. Keep callbacks defined in the page modules or in a central place as needed.
- If you plan to add more dependencies, add a `requirements.txt` file and install with `pip install -r requirements.txt`.

**Contributing**

Feel free to open issues or submit PRs. For small changes (adding pages, updating styles), follow the existing code style and keep changes focused.

**License**

This repository currently has no license specified — add one if you intend to open-source the code.

---

If you'd like, I can:
- create a `requirements.txt` for you, or
- flesh out `pages/surface.py` with a richer layout and example callbacks.
