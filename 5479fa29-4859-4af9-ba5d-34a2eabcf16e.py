from manim import *

class BohrModel(Scene):
    def construct(self):
        # --- Configuration ---
        num_shells = 3
        base_radius = 1.5
        shell_radii = [base_radius * (i + 1) for i in range(num_shells)]
        electron_dot_radius = 0.1
        nucleus_radius = 0.5

        # --- Create Nucleus ---
        nucleus_circle = Circle(radius=nucleus_radius, color=RED_E, fill_opacity=0.8)
        nucleus_text = Text("Nucleus", font_size=24).move_to(nucleus_circle.get_center())
        nucleus = VGroup(nucleus_circle, nucleus_text)

        # --- Create Electron Shells ---
        shells = VGroup()
        for i, r in enumerate(shell_radii):
            shell_circle = Circle(radius=r, color=BLUE_D, stroke_width=2)
            # Position label relative to a point on the shell's circumference
            shell_label = Text(f"n={i+1}", font_size=20, color=BLUE_A).next_to(shell_circle.point_at_angle(PI/4), UP + RIGHT, buff=0.1)
            shells.add(VGroup(shell_circle, shell_label))

        # --- Create Electrons ---
        # Helper function to create an electron VGroup (dot + label)
        def create_electron_vgroup(position):
            electron_dot = Dot(point=position, radius=electron_dot_radius, color=YELLOW_E)
            electron_label = Text("e-", font_size=18, color=YELLOW_A).move_to(electron_dot.get_center())
            return VGroup(electron_dot, electron_label)

        # Initial positions for electrons on their respective shells
        electron1 = create_electron_vgroup(shells[0][0].point_at_angle(0)) # n=1 shell
        electron2 = create_electron_vgroup(shells[1][0].point_at_angle(PI)) # n=2 shell
        electron3 = create_electron_vgroup(shells[1][0].point_at_angle(PI/2)) # n=2 shell
        electron4 = create_electron_vgroup(shells[2][0].point_at_angle(3*PI/2)) # n=3 shell

        electrons = VGroup(electron1, electron2, electron3, electron4)

        # --- Introduction ---
        title = Text("Niels Bohr's Atomic Model", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Animate creation of nucleus, shells, and electrons
        self.play(Create(nucleus))
        self.play(LaggedStart(*[Create(shell) for shell in shells], lag_ratio=0.5))
        self.play(LaggedStart(*[FadeIn(electron) for electron in electrons], lag_ratio=0.3))
        self.wait(1)

        # --- Absorption Animation ---
        absorption_text = Text("Absorption: Electron gains energy and jumps to a higher shell.", font_size=30).to_edge(DOWN)
        self.play(Write(absorption_text))
        self.wait(0.5)

        # Highlight electron1 (currently on n=1 shell)
        self.play(electron1.animate.set_color(GREEN_E), run_time=0.5)

        # Store electron's position before the jump for photon target
        electron_pre_jump_pos_abs = electron1.get_center()

        # Create incoming photon VGroup
        # Define a generic arrow and label, then position the VGroup off-screen
        photon_arrow_abs = Arrow(start=ORIGIN, end=RIGHT * 1.5, color=PURPLE_A, buff=0.1)
        photon_label_abs = Text("Photon", font_size=20, color=PURPLE_A).next_to(photon_arrow_abs, UP)
        photon_vgroup_in = VGroup(photon_arrow_abs, photon_label_abs).move_to(LEFT * 5) # Initial position off-screen

        # Electron jumps from n=1 to n=3 shell
        target_pos_e1_absorption = shells[2][0].point_at_angle(PI/4) # New position on n=3 shell
        
        # Animate photon appearing off-screen, moving towards electron's initial position, and electron jumping
        self.play(
            FadeIn(photon_vgroup_in), # Photon appears off-screen
            photon_vgroup_in.animate.move_to(electron_pre_jump_pos_abs), # Photon moves to electron's initial position
            electron1.animate.move_to(target_pos_e1_absorption),
            run_time=2
        )
        self.play(FadeOut(photon_vgroup_in)) # Photon is absorbed
        self.play(electron1.animate.set_color(YELLOW_E), run_time=0.5) # Electron returns to original color
        self.wait(1)
        self.play(FadeOut(absorption_text))

        # --- Emission Animation ---
        emission_text = Text("Emission: Electron loses energy and jumps to a lower shell, emitting a photon.", font_size=30).to_edge(DOWN)
        self.play(Write(emission_text))
        self.wait(0.5)

        # Highlight electron1 (now on n=3 shell)
        self.play(electron1.animate.set_color(GREEN_E), run_time=0.5)

        # Electron jumps from n=3 back to n=1 shell
        target_pos_e1_emission = shells[0][0].point_at_angle(0) # Back to n=1 shell
        
        # Store electron's position before the jump for photon emission origin
        electron_pre_jump_pos_emit = electron1.get_center()

        # Create outgoing photon VGroup
        # It should appear at electron_pre_jump_pos_emit and move outwards.
        photon_arrow_emit = Arrow(start=ORIGIN, end=RIGHT * 1.5, color=PURPLE_A, buff=0.1)
        photon_label_emit = Text("Photon", font_size=20, color=PURPLE_A).next_to(photon_arrow_emit, UP)
        photon_vgroup_out = VGroup(photon_arrow_emit, photon_label_emit).move_to(electron_pre_jump_pos_emit) # Start at electron's position

        # Animate electron jumping and photon being emitted simultaneously
        self.play(
            electron1.animate.move_to(target_pos_e1_emission),
            FadeIn(photon_vgroup_out), # Photon appears at the electron's initial position
            photon_vgroup_out.animate.shift(RIGHT * 3), # And moves outwards
            run_time=2
        )
        self.play(FadeOut(photon_vgroup_out)) # Photon moves away and fades
        self.play(electron1.animate.set_color(YELLOW_E), run_time=0.5) # Electron returns to original color
        self.wait(1)
        self.play(FadeOut(emission_text))

        # --- Conclusion ---
        conclusion_text = Text("Electrons exist in discrete energy levels (shells).", font_size=36).to_edge(DOWN)
        self.play(Write(conclusion_text))
        self.wait(2)
        self.play(FadeOut(conclusion_text, title, nucleus, shells, electrons))
        self.wait(1)
