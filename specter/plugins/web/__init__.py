from __future__ import annotations

from specter.plugins.web.headers import SecurityHeadersPlugin
from specter.plugins.web.js_endpoints import JavaScriptEndpointsPlugin
from specter.plugins.web.jwt import JWTClaimsPlugin

BUILTIN_WEB_PLUGINS = (
    SecurityHeadersPlugin,
    JWTClaimsPlugin,
    JavaScriptEndpointsPlugin,
)


__all__ = [
    "BUILTIN_WEB_PLUGINS",
    "JWTClaimsPlugin",
    "JavaScriptEndpointsPlugin",
    "SecurityHeadersPlugin",
]
