"""
{{ AgentName }} - {{ AgentPurpose }}

This agent is written to be framework-agnostic and easy to scaffold.
Replace/extend methods to implement your domain logic.
"""

# mypy: ignore-errors
from __future__ import annotations

import asyncio
from typing import List, Dict, Any, Optional

# Use logfire if available, else fall back to stdlib logging
try:
    import logfire  # type: ignore
    logfire.configure()
    LOGGER = logfire
    def span(name: str, **kw): 
        try: return LOGGER.span(name, **kw)
        except Exception: return None
except Exception:  # pragma: no cover
    import logging
    logging.basicConfig(level=logging.INFO)
    LOGGER = logging.getLogger("{{ AgentSlug }}")
    def span(name: str, **kw): 
        class _NoopCtx: 
            def __enter__(self): return None
            def __exit__(self, *a): return False
        return _NoopCtx()

from .schema import (
    TaskInput,
    TaskOutput,
    Section,
)
from .utils import load_config  # optional helper (see below); provide your own if not used


class {{ AgentClassName }}:
    """Agent responsible for {{ AgentPurpose }}."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or load_config("config.yaml")
        LOGGER.info("{{ AgentClassName }} initialized with config: %s", self.config.get("strategy", {}))

    async def run(self, input_data: TaskInput) -> TaskOutput:
        """Entry point for the agent. Override or orchestrate sub-steps here."""
        with span("{{ AgentSlug }}.run", query=input_data.query or "") or span("noop"):
            LOGGER.info("Starting {{ AgentClassName }} run() with %d items", len(input_data.items))
            items = self._rank_items(input_data.items, input_data.query or "")
            sections = self._create_sections(items, input_data)
            text = self._assemble_text(sections, self.config.get("assembly", {}).get("max_output_length", 4000))
            metrics = self._score(sections, input_data)
            return TaskOutput(
                text=text,
                sections=sections,
                status="ok",
                metrics=metrics,
                attachments=[],
            )

    # ---------- Implementation building blocks (replace as needed) ----------

    def _rank_items(self, items: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """Rank items by a naive similarity score + optional boosts.
        Expected item fields: {id, title, content, similarity_score?, tags?}
        """
        for it in items:
            it.setdefault("similarity_score", 0.0)
            base = it.get("similarity_score", 0.0)
            boost = 0.1 * sum(1 for t in (query.lower().split()) if t in it.get("title", "").lower())
            it["_score"] = min(1.0, base + boost)
        items = sorted(items, key=lambda x: x.get("_score", 0.0), reverse=True)
        threshold = self.config.get("assembly", {}).get("min_relevance_threshold", 0.3)
        return [it for it in items if it.get("_score", 0.0) >= threshold]

    def _create_sections(self, items: List[Dict[str, Any]], input_data: TaskInput) -> List[Section]:
        """Create sections from ranked items. Customize per agent type."""
        max_sections = self.config.get("assembly", {}).get("max_sections", 5)
        sections: List[Section] = []

        if items:
            overview = Section(
                title="Overview",
                content=f"{len(items)} items selected for {{ AgentName }}.",
                sources=[],
                score=1.0,
                meta={"type": "overview"},
            )
            sections.append(overview)

        for i, it in enumerate(items[:max_sections]):
            body = self._summarize_item(it)
            sections.append(
                Section(
                    title=f"Item {i+1}: {it.get('title','Untitled')[:60]}",
                    content=body,
                    sources=[it.get("id", str(i))],
                    score=it.get("_score", 0.0),
                    meta={"tags": it.get("tags", []), "source": it.get("source")},
                )
            )
        return sections

    def _summarize_item(self, it: Dict[str, Any]) -> str:
        content = (it.get("content") or "").strip()
        if len(content) > 280:
            cut = content[:280]
            dot = cut.rfind(".")
            content = (cut[: dot + 1] if dot > 120 else cut + "...")
        return f"Source: {it.get('source','n/a')}\n\n{content}\n(Score: {it.get('_score',0.0):.2f})"

    def _assemble_text(self, sections: List[Section], max_len: int) -> str:
        text = []
        cur = 0
        for s in sections:
            block = f"\n## {s.title}\n\n{s.content}\n"
            if cur + len(block) > max_len:
                remain = max_len - cur - len(f"\n## {s.title}\n\n")
                if remain > 80:
                    block = f"\n## {s.title}\n\n{s.content[:remain-3]}...\n"
                    text.append(block); break
                break
            text.append(block); cur += len(block)
        return "".join(text).strip()

    def _score(self, sections: List[Section], input_data: TaskInput) -> Dict[str, Any]:
        if not sections:
            return {"coverage": 0, "diversity": 0, "length": 0}
        avg = sum(s.score for s in sections) / len(sections)
        unique_sources = len(set().union(*[set(s.sources) for s in sections if s.sources]))
        total_len = sum(len(s.content) for s in sections)
        return {"avg_score": round(avg, 3), "unique_sources": unique_sources, "length": total_len}
