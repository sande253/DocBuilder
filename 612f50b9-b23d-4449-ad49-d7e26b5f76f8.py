from manim import *

class BohrModel(Scene):
    def construct(self):
        # --- Configuration --- 
        nucleus_radius = 0.5
        electron_radius = 0.15
        # Radii for n=1, n=2, n=3 orbits
        orbit_radii = [2, 3.5, 5] 
        orbit_colors = [BLUE_A, GREEN_A, RED_A]
        electron_color = YELLOW
        nucleus_color = RED_E

        # --- Create Elements --- 
        # Nucleus: A VGroup of a Circle and its centered Text label
        nucleus_shape = Circle(radius=nucleus_radius, color=nucleus_color, fill_opacity=0.8)
        nucleus_label = Text("NUCLEUS", font_size=24, color=WHITE).move_to(nucleus_shape.get_center())
        nucleus = VGroup(nucleus_shape, nucleus_label)

        # Orbits: VGroup of concentric circles. Labels are separate as they are not centered within the circles.
        orbits = VGroup()
        orbit_labels = VGroup()
        for i, r in enumerate(orbit_radii):
            orbit_circle = Circle(radius=r, color=orbit_colors[i], stroke_width=2)
            orbit_text = Text(f"n={i+1}", font_size=20, color=orbit_colors[i])
            # Position label slightly outside the orbit, relative to its top-right point
            orbit_text.move_to(orbit_circle.point_at_angle(PI/4) + 0.5 * (UP + RIGHT))
            orbits.add(orbit_circle)
            orbit_labels.add(orbit_text)
        
        # Electron: A VGroup of a Circle and its centered Text label
        # Initial position at the top of the n=1 orbit
        initial_electron_pos = orbits[0].point_at_angle(PI/2) 
        electron_shape = Circle(radius=electron_radius, color=electron_color, fill_opacity=1)
        electron_label = Text("e-", font_size=18, color=BLACK).move_to(electron_shape.get_center())
        electron = VGroup(electron_shape, electron_label).move_to(initial_electron_pos)

        # --- Introduction --- 
        title = Text("The Niels Bohr Atomic Model", font_size=48).to_edge(UP)
        self.play(FadeIn(title))
        self.wait(0.5)

        # Animate creation of nucleus, orbits, and electron
        self.play(Create(nucleus), FadeIn(nucleus_label))
        self.play(Create(orbits), FadeIn(orbit_labels))
        self.play(Create(electron))
        self.wait(1)

        intro_text = Text("A central nucleus with electrons orbiting in specific energy levels.", font_size=28).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(intro_text))
        self.wait(2)
        self.play(FadeOut(intro_text))

        # --- Postulate 1: Stable Orbits --- 
        postulate1_title = Text("Postulate 1: Stable Orbits", font_size=36).next_to(title, DOWN, buff=0.0).to_edge(UP).shift(DOWN*0.8)
        postulate1_text = Text("Electrons orbit in specific, stable energy levels (orbits) without radiating energy.", font_size=28).next_to(postulate1_title, DOWN, buff=0.5)
        
        # Transform the main title to the postulate title
        self.play(Transform(title, postulate1_title))
        self.play(FadeIn(postulate1_text))
        self.wait(1)

        # Animate electron orbiting in the n=1 orbit
        orbit_path_n1 = orbits[0]
        self.play(MoveAlongPath(electron, orbit_path_n1, run_time=3, rate_func=linear))
        self.wait(1)
        self.play(FadeOut(postulate1_text))

        # --- Postulate 2: Energy Transitions --- 
        postulate2_title = Text("Postulate 2: Energy Transitions", font_size=36).next_to(title, DOWN, buff=0.0).to_edge(UP).shift(DOWN*0.8)
        postulate2_text_absorb = Text("Electrons absorb specific quanta of energy to jump to higher orbits.", font_size=28).next_to(postulate2_title, DOWN, buff=0.5)
        postulate2_text_emit = Text("Electrons emit specific quanta of energy to jump to lower orbits.", font_size=28).next_to(postulate2_title, DOWN, buff=0.5)

        self.play(Transform(title, postulate2_title))
        self.wait(1)

        # Absorption (n=1 to n=2)
        self.play(FadeIn(postulate2_text_absorb))
        # Photon incoming from left
        photon_in = Arrow(start=LEFT * 6, end=orbits[0].point_at_angle(PI/2) + LEFT * 0.5, color=ORANGE, buff=0)
        photon_label_in = Text("Energy (Photon)", font_size=20, color=ORANGE).next_to(photon_in, LEFT)
        
        self.play(Create(photon_in), FadeIn(photon_label_in))
        # Electron jumps from n=1 to n=2, photon fades out (absorbed)
        self.play(
            electron.animate.move_to(orbits[1].point_at_angle(PI/2)), # Move electron to n=2
            FadeOut(photon_in, shift=RIGHT*0.5), # Photon "absorbed"
            FadeOut(photon_label_in),
            run_time=1.5
        )
        self.wait(1)
        self.play(FadeOut(postulate2_text_absorb))

        # Emission (n=2 to n=1)
        self.play(FadeIn(postulate2_text_emit))
        # Photon outgoing to right
        photon_out = Arrow(start=orbits[1].point_at_angle(PI/2) + RIGHT * 0.5, end=RIGHT * 6, color=PURPLE, buff=0)
        photon_label_out = Text("Energy (Photon)", font_size=20, color=PURPLE).next_to(photon_out, RIGHT)

        # Electron jumps from n=2 back to n=1, photon fades in (emitted)
        self.play(
            electron.animate.move_to(orbits[0].point_at_angle(PI/2)), # Move electron back to n=1
            Create(photon_out), # Photon "emitted"
            FadeIn(photon_label_out),
            run_time=1.5
        )
        self.wait(1)
        self.play(FadeOut(postulate2_text_emit), FadeOut(photon_out), FadeOut(photon_label_out))

        # --- Significance: Atomic Spectra --- 
        significance_title = Text("Significance: Explaining Atomic Spectra", font_size=36).next_to(title, DOWN, buff=0.0).to_edge(UP).shift(DOWN*0.8)
        significance_text = Text("These discrete energy transitions explain the unique emission and absorption spectra of elements.", font_size=28).next_to(significance_title, DOWN, buff=0.5)

        self.play(Transform(title, significance_title))
        self.play(FadeIn(significance_text))
        self.wait(1)

        # Show multiple transitions to illustrate different spectral lines
        electron_n1_pos = orbits[0].point_at_angle(PI/2)
        electron_n2_pos = orbits[1].point_at_angle(PI/2)
        electron_n3_pos = orbits[2].point_at_angle(PI/2)

        # Reset electron to n=1 for new transitions
        self.play(electron.animate.move_to(electron_n1_pos))

        # n=1 to n=3 absorption (higher energy photon)
        photon_in_long = Arrow(start=LEFT * 6, end=electron_n1_pos + LEFT * 0.5, color=YELLOW_A, buff=0)
        photon_label_in_long = Text("High Energy", font_size=20, color=YELLOW_A).next_to(photon_in_long, LEFT)
        self.play(Create(photon_in_long), FadeIn(photon_label_in_long))
        self.play(
            electron.animate.move_to(electron_n3_pos),
            FadeOut(photon_in_long, shift=RIGHT*0.5),
            FadeOut(photon_label_in_long),
            run_time=1
        )
        self.wait(0.5)

        # n=3 to n=2 emission (medium energy photon)
        photon_out_mid = Arrow(start=electron_n3_pos + RIGHT * 0.5, end=RIGHT * 6, color=GREEN_B, buff=0)
        photon_label_out_mid = Text("Medium Energy", font_size=20, color=GREEN_B).next_to(photon_out_mid, RIGHT)
        self.play(
            electron.animate.move_to(electron_n2_pos),
            Create(photon_out_mid),
            FadeIn(photon_label_out_mid),
            run_time=1
        )
        self.wait(0.5)
        self.play(FadeOut(photon_out_mid), FadeOut(photon_label_out_mid))

        # n=2 to n=1 emission (lower energy photon)
        photon_out_short = Arrow(start=electron_n2_pos + RIGHT * 0.5, end=RIGHT * 6, color=BLUE_B, buff=0)
        photon_label_out_short = Text("Low Energy", font_size=20, color=BLUE_B).next_to(photon_out_short, RIGHT)
        self.play(
            electron.animate.move_to(electron_n1_pos),
            Create(photon_out_short),
            FadeIn(photon_label_out_short),
            run_time=1
        )
        self.wait(0.5)
        self.play(FadeOut(photon_out_short), FadeOut(photon_label_out_short))

        self.wait(2)
        self.play(FadeOut(significance_text))

        # --- Conclusion --- 
        conclusion_text = Text("The Bohr Model: A foundational step in understanding quantum mechanics.", font_size=36).next_to(title, DOWN, buff=0.0).to_edge(UP).shift(DOWN*0.8)
        self.play(Transform(title, conclusion_text))
        self.wait(3)

        # Clear all mobjects from the scene
        self.play(FadeOut(VGroup(*self.mobjects)))
