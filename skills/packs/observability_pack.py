"""
Observability Skill Pack
------------------------
Gives an agent deep observability expertise for production systems:
  • OpenTelemetry (OTel) — unified traces, metrics, and logs
  • Prometheus — metrics collection, PromQL, recording rules, alerting
  • Grafana — dashboards, alerting, Loki, Tempo data sources
  • Jaeger / Tempo — distributed tracing backend
  • Structured logging best practices (JSON, correlation IDs, log levels)

Best for: Cloud DevOps Specialist, Solution Architect, Senior Developer
"""
from crewai_tools import ScrapeWebsiteTool

from skills.packs import SkillPack


def _observability_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://opentelemetry.io/docs/"),
        ScrapeWebsiteTool(website_url="https://opentelemetry.io/docs/instrumentation/python/"),
        ScrapeWebsiteTool(website_url="https://prometheus.io/docs/"),
        ScrapeWebsiteTool(website_url="https://grafana.com/docs/grafana/latest/"),
        ScrapeWebsiteTool(website_url="https://grafana.com/docs/loki/latest/"),
        ScrapeWebsiteTool(website_url="https://www.jaegertracing.io/docs/"),
        ScrapeWebsiteTool(website_url="https://opentelemetry.io/docs/collector/"),
    ]


OBSERVABILITY = SkillPack(
    name="observability",
    description=(
        "OpenTelemetry traces/metrics/logs, Prometheus PromQL, Grafana dashboards, "
        "Jaeger distributed tracing, structured logging."
    ),
    tools_factory=_observability_tools,
    backstory_addendum=(
        "You are an observability engineer who operates by the three pillars: "
        "metrics, traces, and logs. You instrument applications with OpenTelemetry "
        "SDKs, propagate trace context across service boundaries, and export spans "
        "to Jaeger or Grafana Tempo. You write PromQL queries for RED (Rate, Errors, "
        "Duration) and USE (Utilisation, Saturation, Errors) methodologies and "
        "define SLOs with Prometheus recording rules. You design Grafana dashboards "
        "that surface SLO burn rates and error budgets. You deploy the OTel Collector "
        "as a daemonset or sidecar for unified pipeline management. You enforce "
        "structured JSON logging with mandatory fields: timestamp, level, service, "
        "trace_id, span_id, and message. You set up alerting with Alertmanager or "
        "Grafana Alerting, write runbook links into every alert annotation, and "
        "classify alerts by severity (critical, warning, info)."
    ),
    goal_addendum=(
        "Instrument code with OpenTelemetry, expose Prometheus /metrics endpoints, "
        "produce Grafana dashboard JSON, and apply RED/USE alert rules."
    ),
)
