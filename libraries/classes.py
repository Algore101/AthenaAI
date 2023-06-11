import discord
from discord.ui import View, Button


class TriviaView(View):
    def __init__(self, question, correct_answer, player):
        super().__init__()
        self.question = question
        self.correct_answer = correct_answer
        self.response = None
        self.player = player

    # Button 1
    @discord.ui.button(label='A', style=discord.ButtonStyle.primary)
    async def answer_a(self, interaction: discord.Interaction, button: Button):
        # Check if it's the user who started the game answered the question
        if interaction.user == self.player:
            self.response = 'A'
            await interaction.response.defer()
            self.stop()
            # Disable the buttons after question has been answered
            for item in self.children:
                item.disabled = True
            await interaction.edit_original_response(view=self)
        else:
            # Message if it isn't the user who started the game that answered
            await interaction.response.send_message('This isn\'t your game...Make your own!')

    # Button 2
    @discord.ui.button(label='B', style=discord.ButtonStyle.primary)
    async def answer_b(self, interaction: discord.Interaction, button: Button):
        # Check if it's the user who started the game answered the question
        if interaction.user == self.player:
            self.response = 'B'
            await interaction.response.defer()
            self.stop()
            # Disable the buttons after question has been answered
            for item in self.children:
                item.disabled = True
            await interaction.edit_original_response(view=self)
        else:
            # Message if it isn't the user who started the game that answered
            await interaction.response.send_message('This isn\'t your game...Make your own!')

    # Button 3
    @discord.ui.button(label='C', style=discord.ButtonStyle.primary)
    async def answer_c(self, interaction: discord.Interaction, button: Button):
        # Check if it's the user who started the game answered the question
        if interaction.user == self.player:
            self.response = 'C'
            await interaction.response.defer()
            self.stop()
            # Disable the buttons after question has been answered
            for item in self.children:
                item.disabled = True
            await interaction.edit_original_response(view=self)
        else:
            # Message if it isn't the user who started the game that answered
            await interaction.response.send_message('This isn\'t your game...Make your own!')

    # Button 4
    @discord.ui.button(label='D', style=discord.ButtonStyle.primary)
    async def answer_d(self, interaction: discord.Interaction, button: Button):
        # Check if it's the user who started the game answered the question
        if interaction.user == self.player:
            self.response = 'D'
            await interaction.response.defer()
            self.stop()
            # Disable the buttons after question has been answered
            for item in self.children:
                item.disabled = True
            await interaction.edit_original_response(view=self)
        else:
            # Message if it isn't the user who started the game that answered
            await interaction.response.send_message('This isn\'t your game...Make your own!')
