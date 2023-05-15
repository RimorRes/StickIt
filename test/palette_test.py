from stickit.palettize import hex_to_rgb


def test_hex_to_rgb():

        with open('./res/palettes/nes_hex', 'r') as hex_file:
            hex_colors = [l.strip() for l in hex_file.readlines()]
        with open('./res/palettes/nes_rgb', 'r') as rgb_file:
            rgb_colors = [l.strip() for l in rgb_file.readlines()]

        for i in range(len(hex_colors)):
            assert str(hex_to_rgb(hex_colors[i])) == rgb_colors[i]
