"""Rebuild both playbook PDFs into docs/playbooks/."""
import writing, editing
from common import render

render("ai-video-writing-playbook", writing.HTML)
render("ai-video-editing-playbook", editing.HTML)
