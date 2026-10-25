#!/bin/sh
# Rebuild every Phase 2 generated output, in dependency order. Run from the repository root.
# CI runs this and then requires a clean working tree: committed outputs must equal a fresh build.
set -e
python phase2/tools/extract_adopted_cip.py --write
python phase2/tools/network_condition.py --write
python phase2/tools/street_plan_conditions.py --write
python phase2/tools/street_funding.py --write
python phase2/tools/pci_model.py --emit
python phase2/tools/build_answers.py --write
python phase2/tools/build_dashboard_data.py
python phase2/tools/build_review_checklist.py
