"""
Main bot implementation for the translation bot.
"""
import argostranslate.package
import argostranslate.translate
from lxmfy import LXMFBot
from lxmfy.attachments import IconAppearance, pack_icon_appearance_field

class TranslateBot:
    """
    A translation bot that uses Argos Translate for offline translations.
    """
    def __init__(self):
        """Initialize the translation bot."""
        # Initialize Argos Translate packages
        argostranslate.package.update_package_index()
        self.available_packages = argostranslate.package.get_available_packages()
        
        # Create LXMFy bot instance
        self.bot = LXMFBot(
            name="TranslateBot",
            command_prefix="",
            storage_path="translate_data",
            permissions_enabled=True
        )
        
        # Set up bot icon
        icon_data = IconAppearance(
            icon_name="translate",
            fg_color=b'\x00\xFF\x00',
            bg_color=b'\x33\x33\x33'
        )
        self.bot_icon_field = pack_icon_appearance_field(icon_data)
        
        # Register commands
        self.register_commands()
    
    def register_commands(self):
        """Register all bot commands."""
        @self.bot.command(name="translate", description="Translate text between languages")
        def translate_command(ctx):
            """
            Translate text between languages.
            Usage: translate <source_lang> <target_lang> <text>
            Example: translate en es Hello world
            """
            if len(ctx.args) < 3:
                ctx.reply(
                    "Please provide source language, target language, and text to translate.\n"
                    "Example: translate en es Hello world",
                    lxmf_fields=self.bot_icon_field
                )
                return
            
            source_lang = ctx.args[0].lower()
            target_lang = ctx.args[1].lower()
            text = " ".join(ctx.args[2:])
            
            try:
                package = next(
                    (p for p in self.available_packages 
                     if p.from_code == source_lang and p.to_code == target_lang),
                    None
                )
                
                if package:
                    argostranslate.package.install_from_path(package.download())
                    translated = argostranslate.translate.translate(text, source_lang, target_lang)
                    ctx.reply(
                        f"Translation ({source_lang} → {target_lang}):\n{translated}",
                        lxmf_fields=self.bot_icon_field
                    )
                else:
                    ctx.reply(
                        f"Sorry, translation from {source_lang} to {target_lang} is not available.",
                        lxmf_fields=self.bot_icon_field
                    )
            except Exception as e:
                ctx.reply(
                    f"Error during translation: {str(e)}",
                    lxmf_fields=self.bot_icon_field
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
                lxmf_fields=self.bot_icon_field
            )
    
    def run(self):
        """Run the translation bot."""
        print(f"Starting TranslateBot: {self.bot.config.name}")
        print(f"Bot LXMF Address: {self.bot.local.hash}")
        self.bot.run()

def main():
    """Main entry point for the bot."""
    bot = TranslateBot()
    bot.run()

if __name__ == "__main__":
    main() 