import time
import sys
import os
from typing import Optional

class AgentSeaLogo:
    def __init__(self, animate: bool = False, style: str = 'default'):
        self.animate = animate
        self.style = style
        
        # ANSI color codes
        self.BLUE = '\033[34m'
        self.BRIGHT_BLUE = '\033[94m'
        self.CYAN = '\033[36m'
        self.BOLD = '\033[1m'
        self.RESET = '\033[0m'
        
        self.logos = {
            'detailed': f"""
{self.BLUE}┌────────────────────────────────────────┐
│                                        │
│         ○───●      ╭─────────╮        │
│            │       │{self.RESET} •••     {self.BLUE}│        │
│            │       ╰─────────╯        │
│       ┌────┴────┐                     │
│       │ ╭─────╮ │     ╭─────────╮    │
│       │ │{self.RESET} ••• {self.BLUE}│ │     │{self.RESET} •••     {self.BLUE}│    │
│       │ ╰─────╯ │     ╰─────────╯    │
│       └─────────┘                     │
│                                        │
│            {self.BOLD}{self.CYAN}AgentSea{self.RESET}{self.BLUE}                  │
│                                        │
└────────────────────────────────────────┘{self.RESET}""",

            'minimal': f"""
{self.BLUE}╭────────────────────────────╮
│        ○─●    ╭───╮        │
│         │     │{self.RESET}•••{self.BLUE}│        │
│     ╭───┴───╮ ╰───╯        │
│     │ {self.RESET}•••{self.BLUE} │   ╭───╮      │
│     ╰───────╯   │{self.RESET}•••{self.BLUE}│      │
│                 ╰───╯      │
│      {self.BOLD}{self.CYAN}AgentSea{self.RESET}{self.BLUE}            │
╰────────────────────────────╯{self.RESET}""",

            'ascii': """
+--------------------------------+
|          o-*    .---.          |
|           |     |...|          |
|      .----+-.   '---'          |
|      | ... |                   |
|      '-----'    .---.          |
|                 |...|          |
|        AgentSea '---'          |
+--------------------------------+"""
        }

        self.animation_frames = [
            ('•••', '   '),
            ('•• ', '•  '),
            ('•  ', '•• '),
            ('   ', '•••'),
        ]

    def _supports_unicode(self) -> bool:
        return sys.stdout.encoding.lower().startswith('utf')

    def _supports_ansi(self) -> bool:
        return 'TERM' in os.environ and os.environ.get('TERM', '') != 'dumb'

    def _clear_screen(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def _animate_frame(self, content: str, dots1: str, dots2: str) -> str:
        return (content
                .replace('•••', dots1)
                .replace('...', dots2))

    def display(self, duration: Optional[float] = None) -> None:
        """Display the logo with optional animation."""
        try:
            if self._supports_ansi() and self._supports_unicode():
                base_logo = self.logos['detailed' if self.style == 'default' else self.style]
            elif self._supports_unicode():
                base_logo = self.logos['minimal'].replace(self.BLUE, '').replace(self.CYAN, '').replace(self.BOLD, '').replace(self.RESET, '')
            else:
                base_logo = self.logos['ascii']

            if self.animate:
                start_time = time.time()
                while duration is None or time.time() - start_time < duration:
                    for dots1, dots2 in self.animation_frames:
                        self._clear_screen()
                        print(self._animate_frame(base_logo, dots1, dots2))
                        time.sleep(0.2)
            else:
                print(base_logo)

        except (UnicodeEncodeError, IOError):
            print(self.logos['ascii'])

def main():
    """Example usage with different styles and animation."""
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Display AgentSea Logo')
    parser.add_argument('--animate', action='store_true', help='Enable animation')
    parser.add_argument('--style', choices=['default', 'minimal', 'ascii'], 
                       default='default', help='Logo style')
    parser.add_argument('--duration', type=float, help='Animation duration in seconds')
    args = parser.parse_args()

    # Create and display logo
    logo = AgentSeaLogo(animate=args.animate, style=args.style)
    logo.display(duration=args.duration)

if __name__ == "__main__":
    main()