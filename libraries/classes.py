import discord
from discord.ui import View, Button


class TriviaView(View):
    def __init__(self, question, correct_answer):
        super().__init__()
        self.question = question
        self.correct_answer = correct_answer
        self.response = None

    @discord.ui.button(label='A', style=discord.ButtonStyle.primary)
    async def answer_a(self, interaction: discord.Interaction, button: Button):
        self.response = 'A'
        await interaction.response.defer()
        self.stop()

    @discord.ui.button(label='B', style=discord.ButtonStyle.primary)
    async def answer_b(self, interaction: discord.Interaction, button: Button):
        self.response = 'B'
        await interaction.response.defer()
        self.stop()

    @discord.ui.button(label='C', style=discord.ButtonStyle.primary)
    async def answer_c(self, interaction: discord.Interaction, button: Button):
        self.response = 'C'
        await interaction.response.defer()
        self.stop()

    @discord.ui.button(label='D', style=discord.ButtonStyle.primary)
    async def answer_d(self, interaction: discord.Interaction, button: Button):
        self.response = 'D'
        await interaction.response.defer()
        self.stop()
