"""Main bot implementation for the translation bot.
"""
import argparse
import time

import argostranslate.package
import argostranslate.translate
from lxmfy import LXMFBot
from lxmfy.attachments import IconAppearance, pack_icon_appearance_field


class TranslateBot:
    """A translation bot that uses Argos Translate for offline translations.
    """

    def __init__(self):
        """Initialize the translation bot."""
        # Initialize Argos Translate packages
        argostranslate.package.update_package_index()
        self.available_packages = argostranslate.package.get_available_packages()

        # Initialize statistics tracking
        self.start_time = time.time()
        self.translations_completed = 0
        self.total_translation_time = 0.0
        self.translation_times = []  # Keep last 100 translation times for avg calculation

        # Create LXMFy bot instance
        self.bot = LXMFBot(
            name="LXMFy Translate Bot",
            command_prefix="",
            storage_path="translate_data",
            permissions_enabled=True,
        )

        # Set up bot icon
        icon_data = IconAppearance(
            icon_name="translate",
            fg_color=b"\x00\xFF\x00",
            bg_color=b"\x33\x33\x33",
        )
        self.bot_icon_field = pack_icon_appearance_field(icon_data)

        # Register commands
        self.register_commands()

    def register_commands(self):
        """Register all bot commands."""
        @self.bot.command(name="translate", description="Translate text between languages")
        def translate_command(ctx):
            """Translate text between languages.
            Usage: translate <source_lang> <target_lang> <text>
            Example: translate en es Hello world
            """
            if len(ctx.args) < 3:
                ctx.reply(
                    "Please provide source language, target language, and text to translate.\n"
                    "Example: translate en es Hello world",
                    lxmf_fields=self.bot_icon_field,
                )
                return

            source_lang = ctx.args[0].lower()
            target_lang = ctx.args[1].lower()
            text = " ".join(ctx.args[2:])

            try:
                package = next(
                    (p for p in self.available_packages
                     if p.from_code == source_lang and p.to_code == target_lang),
                    None,
                )

                if package:
                    # Track translation start time
                    translation_start = time.time()

                    argostranslate.package.install_from_path(package.download())
                    translated = argostranslate.translate.translate(text, source_lang, target_lang)

                    # Track translation completion time
                    translation_time = time.time() - translation_start
                    self.translations_completed += 1
                    self.total_translation_time += translation_time
                    self.translation_times.append(translation_time)

                    # Keep only last 100 translation times for average calculation
                    if len(self.translation_times) > 100:
                        self.translation_times.pop(0)

                    ctx.reply(
                        f"Translation ({source_lang} → {target_lang}):\n{translated}",
                        lxmf_fields=self.bot_icon_field,
                    )
                else:
                    ctx.reply(
                        f"Sorry, translation from {source_lang} to {target_lang} is not available.",
                        lxmf_fields=self.bot_icon_field,
                    )
            except Exception as e:
                ctx.reply(
                    f"Error during translation: {e!s}",
                    lxmf_fields=self.bot_icon_field,
                )

        @self.bot.command(name="languages", description="List available languages")
        def languages_command(ctx):
            """List all available languages for translation."""
            languages = set()
            for package in self.available_packages:
                languages.add(package.from_code)
                languages.add(package.to_code)

            lang_list = "\n".join(sorted(languages))
            ctx.reply(
                f"Available languages:\n{lang_list}",
                lxmf_fields=self.bot_icon_field,
            )

        @self.bot.command(name="help", description="Show detailed help and usage information")
        def help_command(ctx):
            """Show comprehensive help for all bot commands."""
            help_text = """**LXMFy Translate Bot Help**

**Available Commands:**

**translate** `<source_lang> <target_lang> <text>`
   Translate text between languages
   • Example: `translate en es Hello world`
   • Example: `translate fr en Bonjour le monde`
   • Note: Language codes are 2-letter (en, es, fr, de, it, pt, etc.)

**languages**
   Show all available language codes for translation
   • Example: `languages`
   • Returns a list of supported language codes

**stats**
   Show bot statistics and performance metrics
   • Example: `stats`
   • Shows uptime, translations completed, average response time, and model status

**help**
   Show this help message
   • Example: `help`

**Language Code Examples:**
• en = English    • es = Spanish    • fr = French
• de = German     • it = Italian    • pt = Portuguese
• ru = Russian    • zh = Chinese    • ja = Japanese
• ar = Arabic     • hi = Hindi      • ko = Korean

**Tips:**
• All commands work offline once models are downloaded
• First translation of a language pair downloads the model automatically
• Use `download` command to pre-load models for better performance
• Invalid language pairs will show an error message

**Need more languages?** Use `languages` to see what's available!"""

            ctx.reply(help_text, lxmf_fields=self.bot_icon_field)

        @self.bot.command(name="stats", description="Show bot statistics and performance metrics")
        def stats_command(ctx):
            """Show comprehensive bot statistics."""
            # Calculate uptime
            uptime_seconds = time.time() - self.start_time
            uptime_str = self.format_uptime(uptime_seconds)

            # Get installed packages
            installed_packages = argostranslate.package.get_installed_packages()
            installed_count = len(installed_packages)
            total_available = len(self.available_packages)

            # Calculate translation statistics
            avg_translation_time = 0.0
            if self.translation_times:
                avg_translation_time = sum(self.translation_times) / len(self.translation_times)

            # Format stats message
            stats_text = f"""**Bot Statistics**

**Uptime:** {uptime_str}
**Translations Completed:** {self.translations_completed}
**Average Translation Time:** {avg_translation_time:.2f} seconds
**Total Translation Time:** {self.total_translation_time:.2f} seconds

**Translation Models:**
• Downloaded: {installed_count} packages
• Available: {total_available} packages
• Coverage: {installed_count}/{total_available} ({installed_count/total_available*100:.1f}%)"""

            if installed_packages:
                # Show some example installed packages
                package_list = []
                for pkg in installed_packages[:5]:  # Show first 5
                    package_list.append(f"• {pkg.from_code} → {pkg.to_code}")

                if len(installed_packages) > 5:
                    package_list.append(f"• ... and {len(installed_packages) - 5} more")

                stats_text += "\n\n**Installed Packages:**\n" + "\n".join(package_list)

            ctx.reply(stats_text, lxmf_fields=self.bot_icon_field)

    def download_all_packages(self):
        """Download all available translation packages."""
        print("Downloading all available translation packages...")
        success_count = 0
        fail_count = 0

        for package in self.available_packages:
            try:
                print(f"Downloading {package.from_code} → {package.to_code}...")
                argostranslate.package.install_from_path(package.download())
                success_count += 1
            except Exception as e:
                print(f"Failed to download {package.from_code} → {package.to_code}: {e}")
                fail_count += 1

        print(f"Download complete! {success_count} successful, {fail_count} failed.")
        return success_count, fail_count

    def format_uptime(self, seconds):
        """Format seconds into a human-readable uptime string."""
        days, remainder = divmod(int(seconds), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        if seconds > 0 or not parts:  # Always show seconds if no other parts
            parts.append(f"{seconds}s")

        return " ".join(parts)

    def run(self):
        """Run the translation bot."""
        print(f"Starting TranslateBot: {self.bot.config.name}")
        print(f"Bot LXMF Address: {self.bot.local.hash.hex()}")
        self.bot.run()

def main():
    """Main entry point for the bot."""
    parser = argparse.ArgumentParser(description="LXMFy Translate Bot")
    parser.add_argument(
        "--download-all",
        action="store_true",
        help="Download all available translation models before starting the bot",
    )
    parser.add_argument(
        "--download",
        nargs="+",
        help="Download specific language pairs before starting (format: lang1-lang2 lang3-lang4)",
    )

    args = parser.parse_args()

    # Create bot instance
    bot = TranslateBot()

    # Handle downloads if requested
    if args.download_all:
        print("Downloading all translation models...")
        success_count, fail_count = bot.download_all_packages()
        print(f"Pre-download complete: {success_count} successful, {fail_count} failed.")
        if fail_count > 0:
            print("Some downloads failed. The bot will still work but may download missing models on-demand.")

    elif args.download:
        # Parse language pairs
        pairs = []
        for arg in args.download:
            if "-" in arg and len(arg.split("-")) == 2:
                from_lang, to_lang = arg.split("-")
                pairs.append((from_lang.lower(), to_lang.lower()))
            else:
                print(f"Invalid language pair format: {arg}. Use format like 'en-es'")
                return

        if pairs:
            print(f"Downloading {len(pairs)} specific language pair(s)...")
            success_count, fail_count = bot.download_specific_packages(pairs)
            print(f"Pre-download complete: {success_count} successful, {fail_count} failed.")

    # Start the bot
    bot.run()

if __name__ == "__main__":
    main()
