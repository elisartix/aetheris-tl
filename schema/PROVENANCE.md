# TL generation provenance

Source: https://github.com/tdlib/td
Revision: c15d3f5a5de6e3ba5839822c451152e5e18bb700
Layer: 230, from `td/telegram/Version.h` (`MTPROTO_LAYER`).
Schema: `td/generate/scheme/telegram_api.tl` (included verbatim here).

Generator: Telethon `telethon_generator`, revision dab6bc4d4fc0c7815f6f19c6f643d9f75d2d930c.
Generator input adapts the primitive preamble to Telethon's parser and adds a
`// LAYER 230` annotation read from Version.h. Explicit schema constructor IDs
are authoritative; legacy renamed declarations can fail inferred-CRC assertions.
Every generated constructor ID must be checked against the original TDLib schema.

Generated files: aetheris_tl/tl/{functions,types,alltlobjects.py}.
Do not replace the fork's runtime, tl/custom, tl/patched or tl/tlobject.py.
Do not install until runtime/button/markup/security tests pass.
