# IKEA Floor Planner — Andrée Geulen

A Render-ready, touch-friendly floor planner using the supplied flat plan. Paste an IKEA Belgium product URL, import the product footprint, and position/rotate it at calibrated scale.

## Deploy on Render

1. Create a new empty GitHub repository and upload every file/folder in this package.
2. In Render, choose **New > Blueprint** and connect that repository.
3. Render detects `render.yaml`; click **Apply**. No API key or database is required.

## First use

1. Click **Calibrate from a wall**.
2. Click the two ends of a wall whose real length you have measured.
3. Enter that length in centimetres.
4. Paste an IKEA Belgium product URL and click **Find**. If IKEA blocks or changes its page format, type the width/depth manually.
5. Add, drag and rotate the item. Layouts save in the current browser.

## Important limitations

- The source plan says dimensions are approximate and contains room areas, but no linear measurements. A real wall measurement is required for reliable scale.
- IKEA occasionally changes its public page markup or blocks automated requests. Manual dimensions remain available by design.
- Storage is browser-local, so layouts are not shared between devices. This keeps the deployment free and removes the need for login/database infrastructure.
