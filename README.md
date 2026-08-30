# IKEA Floor Planner — Andrée Geulen

A Render-ready, touch-friendly floor planner using the supplied flat plan. Paste an IKEA Belgium product URL, import the product footprint, and position/rotate it at calibrated scale.

## Deploy on Render

1. Create a new empty GitHub repository and upload every file/folder in this package.
2. In Render, choose **New > Blueprint** and connect that repository.
3. Render detects `render.yaml`; click **Apply**. No API key or database is required.

## First use

1. Paste an IKEA Belgium product URL and click **Find**. If IKEA blocks or changes its page format, type the width/depth manually.
2. Add, drag and rotate the item. Layouts save in the current browser.

## Important limitations

- No calibration is required. The built-in scale (48 pixels per metre) was estimated by comparing the drawn shapes of the 33 m² salon, 27 m² main bedroom and 21 m² bedroom against their stated areas. The source plan itself says dimensions are approximate, so furniture placement is an informed estimate rather than a construction measurement.
- IKEA occasionally changes its public page markup or blocks automated requests. Manual dimensions remain available by design.
- Storage is browser-local, so layouts are not shared between devices. This keeps the deployment free and removes the need for login/database infrastructure.
