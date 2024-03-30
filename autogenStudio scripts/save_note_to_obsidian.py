# A skill to store markdown content to our second brain obsidian

import os

def store_note_to_obsidian(filename, content):
    """
    Store markdown content to our second brain in a local Obsidian vault
    :param filename: str, filename of the note
    :param content: str, content of the note as markdown
    """

    # Path to Obsidian vault
    obsidian_dir = r'C:/1600/2nd_brain/1600_agent_swarm/'

    # Add .md suffix if not present
    if not filename.endswith('.md'):
        filename += '.md'

    # full path prefix obsidian_dir to filename
    full_path = os.path.join(obsidian_dir, filename)

    # Write content to file
    with open(full_path, 'w') as file:
        file.write(content)


## To test the skill
#if __name__ == '__main__':
#    store_note_to_obsidian("Test", "This is a **test** ==markdown== note!")