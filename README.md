# PLATO RealLog Agent

Real-World Scene Logger for reallog.ai. Camera events → PLATO → persistent spatial memory.

## Quick Start

```python
from reallog_agent import RealLogAgent

agent = RealLogAgent(camera_id="security_cam_1")
agent.log_scene("front_door", "person approaching at 14:32", motion=True)
agent.log_scene("back_yard", "bird detected", motion=False)
print(agent.ask("who came to the front door?"))
```

## Architecture

- Camera frames → described text → PLATO tiles
- Agent reads PLATO → answers visual questions
- "Don the shell" → view from another camera's perspective

## Related

- [reallog.ai](https://reallog.ai) — Live site
- [reallog-ai-pages](https://github.com/SuperInstance/reallog-ai-pages) — GitHub Pages source
