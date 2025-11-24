from manim import *

class BohrModel(Scene):
    def construct(self):
        # --- 0. Title --- 
        title = Text("Niels Bohr's Atomic Model", font_size=50).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # --- 1. Setup: Nucleus and Orbits --- 
        # Nucleus: a VGroup containing a Circle shape and a centered Text label
        nucleus_shape = Circle(radius=0.4, color=RED, fill_opacity=0.8)
        nucleus_label = Text("N", font_size=30, color=WHITE).move_to(nucleus_shape.get_center())
        nucleus = VGroup(nucleus_shape, nucleus_label)
        self.play(Create(nucleus))
        self.wait(0.5)

        # Define orbit radii for visual distinction (not strictly n^2 * a_0 for all)
        r1 = 1.5
        r2 = r1 * 2.5  
        r3 = r1 * 4.0

        orbit1 = Circle(radius=r1, color=GRAY)
        orbit2 = Circle(radius=r2, color=GRAY)
        orbit3 = Circle(radius=r3, color=GRAY)

        orbits = VGroup(orbit1, orbit2, orbit3)
        self.play(Create(orbits))
        self.wait(0.5)

        # Energy level labels, positioned relative to their respective orbits
        label_n1 = Text("n=1", font_size=24).next_to(orbit1, RIGHT, buff=0.2)
        label_n2 = Text("n=2", font_size=24).next_to(orbit2, RIGHT, buff=0.2)
        label_n3 = Text("n=3", font_size=24).next_to(orbit3, RIGHT, buff=0.2)
        
        energy_labels = VGroup(label_n1, label_n2, label_n3)
        self.play(FadeIn(energy_labels))
        self.wait(1)

        # Electron: a VGroup containing a Circle shape and a centered Text label
        electron_shape = Circle(radius=0.15, color=BLUE, fill_opacity=0.8)
        electron_label = Text("e-", font_size=18, color=WHITE).move_to(electron_shape.get_center())
        electron = VGroup(electron_shape, electron_label)
        
        # Initial position for electron on the n=1 orbit
        electron.move_to(orbit1.point_at_angle(PI/2))
        self.play(FadeIn(electron))
        self.wait(1)

        # --- 2. Postulate 1: Quantized Orbits --- 
        postulate1_text = Text("1. Electrons orbit in stable, discrete energy levels.", font_size=30).to_edge(DOWN).shift(UP*0.5)
        self.play(Write(postulate1_text))
        self.wait(1)

        # Animate electron moving between orbits (entire VGroup moves)
        self.play(
            electron.animate.move_to(orbit2.point_at_angle(PI/2)),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(
            electron.animate.move_to(orbit3.point_at_angle(PI/2)),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(
            electron.animate.move_to(orbit1.point_at_angle(PI/2)),
            run_time=1.5
        )
        self.wait(2)
        self.play(FadeOut(postulate1_text))

        # --- 3. Postulate 2: Stable Orbits --- 
        postulate2_text = Text("2. Electrons do not radiate energy while in these orbits.", font_size=30).to_edge(DOWN).shift(UP*0.5)
        self.play(Write(postulate2_text))
        self.wait(2)
        self.play(FadeOut(postulate2_text))

        # --- 4. Postulate 3: Energy Transitions (Absorption & Emission) --- 
        postulate3_text = Text("3. Electrons jump between orbits by absorbing or emitting energy.", font_size=30).to_edge(DOWN).shift(UP*0.5)
        self.play(Write(postulate3_text))
        self.wait(1)

        # Absorption animation
        absorption_text = Text("Absorption", font_size=28, color=YELLOW).next_to(postulate3_text, UP, buff=0.5)
        self.play(FadeIn(absorption_text))
        self.wait(0.5)

        # Photon: a VGroup containing a Dot shape and a centered Text label
        photon_in_shape = Dot(radius=0.1, color=YELLOW)
        photon_in_label = Text("hv", font_size=20, color=YELLOW).move_to(photon_in_shape.get_center())
        photon_in = VGroup(photon_in_shape, photon_in_label)
        photon_in.move_to(LEFT * 4 + UP * 1) # Position photon off-screen to the left

        self.play(FadeIn(photon_in))
        self.play(
            photon_in.animate.move_to(electron.get_center()), # Photon moves towards electron
            run_time=1
        )
        self.play(
            electron.animate.move_to(orbit2.point_at_angle(PI/2)), # Electron jumps to higher orbit
            FadeOut(photon_in), # Photon disappears upon absorption
            run_time=1.5
        )
        self.wait(1)

        # Emission animation
        emission_text = Text("Emission", font_size=28, color=GREEN).next_to(postulate3_text, UP, buff=0.5)
        self.play(Transform(absorption_text, emission_text)) # Transform the label text
        self.wait(0.5)

        # Photon: a VGroup containing a Dot shape and a centered Text label
        photon_out_shape = Dot(radius=0.1, color=GREEN)
        photon_out_label = Text("hv", font_size=20, color=GREEN).move_to(photon_out_shape.get_center())
        photon_out = VGroup(photon_out_shape, photon_out_label)
        photon_out.move_to(electron.get_center()) # Start photon from electron's current position

        self.play(
            electron.animate.move_to(orbit1.point_at_angle(PI/2)), # Electron jumps to lower orbit
            FadeIn(photon_out.animate.move_to(RIGHT * 4 + UP * 1)), # Photon moves off-screen to the right
            run_time=1.5
        )
        self.wait(1)
        self.play(FadeOut(photon_out))
        self.wait(1)

        self.play(FadeOut(absorption_text), FadeOut(postulate3_text)) 

        # --- 5. Postulate 4: Quantized Angular Momentum (Brief Mention) --- 
        postulate4_text = Text("4. Angular momentum is quantized: mvr = nħ", font_size=30).to_edge(DOWN).shift(UP*0.5)
        self.play(Write(postulate4_text))
        self.wait(3)
        self.play(FadeOut(postulate4_text))

        # --- 6. Significance & Limitations --- 
        significance_title = Text("Significance & Limitations", font_size=40).to_edge(DOWN).shift(UP*0.5)
        self.play(Write(significance_title))
        self.wait(1)

        # Significance point 1
        spectrum_text = Text("• Explained the Hydrogen atomic spectrum.", font_size=28).next_to(significance_title, UP, buff=0.5)
        self.play(FadeIn(spectrum_text))
        self.wait(2)

        # Limitation point 1
        limitation1_text = Text("• Only works for hydrogen-like atoms.", font_size=28).next_to(spectrum_text, UP, buff=0.5)
        self.play(FadeIn(limitation1_text))
        self.wait(2)

        # Limitation point 2
        limitation2_text = Text("• Couldn't explain fine structure or Zeeman effect.", font_size=28).next_to(limitation1_text, UP, buff=0.5)
        self.play(FadeIn(limitation2_text))
        self.wait(2)

        # Paved way for Quantum Mechanics
        quantum_mechanics_text = Text("• Paved the way for modern Quantum Mechanics.", font_size=30, color=YELLOW).next_to(significance_title, DOWN, buff=0.5)
        self.play(FadeIn(quantum_mechanics_text))
        self.wait(3)

        # --- 7. Scene Cleanup --- 
        self.play(
            FadeOut(title),
            FadeOut(nucleus),
            FadeOut(orbits),
            FadeOut(energy_labels),
            FadeOut(electron),
            FadeOut(significance_title),
            FadeOut(spectrum_text),
            FadeOut(limitation1_text),
            FadeOut(limitation2_text),
            FadeOut(quantum_mechanics_text)
        )
        self.wait(1)

        final_text = Text("End of Bohr Model Explanation", font_size=40)
        self.play(Write(final_text))
        self.wait(2)
        self.play(FadeOut(final_text))
