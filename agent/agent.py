"""
OBSAgent - Core agent loop
Uses Claude with tool use to control OBS Studio
"""

import anthropic
from obs_client import OBSClient
from image_gen import ImageGenerator
from tools import get_all_tools, execute_tool


class OBSAgent:
    def __init__(self, config: dict):
        self.config = config
        self.client = anthropic.Anthropic(api_key=config['anthropic_api_key'])
        self.obs_client = OBSClient(config['obs_websocket'])
        self.image_gen = None
        if config.get('openai_api_key'):
            self.image_gen = ImageGenerator(api_key=config['openai_api_key'])
        self.model = config.get('agent', {}).get('model', 'claude-opus-4-6')
        self.max_tokens = config.get('agent', {}).get('max_tokens', 4096)
        self.max_iterations = config.get('agent', {}).get('max_iterations', 20)
        self.tools = get_all_tools()
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        return """You are OBSAgent, an AI assistant embedded inside OBS Studio.

You have direct control over OBS through a set of tools. When the user asks you to do something, use the tools to do it — don't just describe what to do.

You can:
- Create, switch, and manage scenes
- Add, position, configure, and remove sources (screen capture, webcam, images, text, browser, audio)
- Generate images with AI (backgrounds, overlays, logos, thumbnails) and add them to scenes
- Control audio: volume, mute, filters (compressor, noise suppression, EQ, limiter, gain)
- Manage filters on any source
- Start/stop recording, streaming, and virtual camera
- Read the current state of OBS (what scenes exist, what sources are active, current settings)

Image workflow: use generate_image to create an image, then add_source with image_source kind and settings {"file": "<path>"} to place it in a scene. Use get_input_kind_list to discover the exact image source kind name.

Guidelines:
- When given a setup task, figure out the full picture before acting. Read existing state first.
- Be efficient: batch related operations where possible.
- If a request is ambiguous, make a reasonable choice and tell the user what you did.
- If something fails, explain why clearly.
- Keep responses concise — the user is in the middle of production work.
- After executing a task, briefly confirm what you did.

You're running locally. All data stays on the user's machine. No cloud calls except to Anthropic for reasoning and OpenAI for image generation."""

    def run(self, message: str, history: list = None) -> dict:
        """Run the agent loop for a single user message"""
        if history is None:
            history = []

        messages = list(history) + [{"role": "user", "content": message}]
        tool_calls_log = []
        iterations = 0

        while iterations < self.max_iterations:
            iterations += 1

            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=self.system_prompt,
                tools=self.tools,
                messages=messages
            )

            # Collect text and tool use from response
            text_parts = []
            tool_uses = []

            for block in response.content:
                if block.type == 'text':
                    text_parts.append(block.text)
                elif block.type == 'tool_use':
                    tool_uses.append(block)

            # If no tool calls, we're done
            if not tool_uses or response.stop_reason == 'end_turn':
                return {
                    'text': '\n'.join(text_parts) or 'Done.',
                    'tool_calls': tool_calls_log
                }

            # Add assistant response to messages
            messages.append({"role": "assistant", "content": response.content})

            # Execute tools and collect results
            tool_results = []
            for tool_use in tool_uses:
                tool_name = tool_use.name
                tool_input = tool_use.input

                try:
                    result = execute_tool(self.obs_client, tool_name, tool_input, image_gen=self.image_gen)
                    tool_calls_log.append({
                        'tool': tool_name,
                        'input': tool_input,
                        'result': result,
                        'success': True
                    })
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": str(result)
                    })
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    tool_calls_log.append({
                        'tool': tool_name,
                        'input': tool_input,
                        'error': error_msg,
                        'success': False
                    })
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": error_msg,
                        "is_error": True
                    })

            messages.append({"role": "user", "content": tool_results})

        return {
            'text': 'Max iterations reached. Some tasks may be incomplete.',
            'tool_calls': tool_calls_log
        }
