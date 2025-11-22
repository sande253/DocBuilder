from manim import *

# Manim Community v0.19+

class ExplainEMC2(Scene):
    """An animation explaining the components and meaning of E=mc^2."""

    def construct(self):
        # Helper function to create a VGroup with a shape and centered text
        def create_labeled_box(text_string, color):
            text = Text(text_string, font_size=32)
            box = Rectangle(
                width=text.width + 0.8,
                height=text.height + 0.5,
                color=color,
                fill_color=color,
                fill_opacity=0.2
            ).round_corners(0.1)
            text.move_to(box.get_center())
            return VGroup(box, text)

        # 1. Introduce the equation
        equation = MathTex("E", "=", "m", "c", "^2").scale(3)
        self.play(Write(equation))
        self.wait(1)

        # 2. Define the components
        e_label = create_labeled_box("Energy", YELLOW)
        m_label = create_labeled_box("Mass", BLUE)
        c_label = create_labeled_box("Speed of Light", RED)

        # Position labels below the equation parts
        e_label.next_to(equation[0], DOWN, buff=0.7)
        m_label.next_to(equation[2], DOWN, buff=0.7)
        c_label.next_to(equation[3], DOWN, buff=0.7)

        labels = VGroup(e_label, m_label, c_label)
        self.play(FadeIn(labels, shift=UP))
        self.wait(2)

        # 3. Explain each component individually
        # Group equation and labels for easier manipulation
        full_equation_group = VGroup(equation, labels)
        self.play(full_equation_group.animate.to_edge(UP))
        self.wait(1)

        # Explain 'E' for Energy
        explanation_e = Text("Energy is the capacity to do work.", font_size=36).next_to(full_equation_group, DOWN, buff=1)
        self.play(Indicate(e_label, color=YELLOW))
        self.play(Write(explanation_e))
        self.wait(2)
        self.play(FadeOut(explanation_e))

        # Explain 'm' for Mass
        explanation_m = Text("Mass is the amount of 'stuff' in an object.", font_size=36).next_to(full_equation_group, DOWN, buff=1)
        self.play(Indicate(m_label, color=BLUE))
        self.play(Write(explanation_m))
        self.wait(2)
        self.play(FadeOut(explanation_m))

        # Explain 'c' for Speed of Light
        explanation_c1 = Text("The speed of light in a vacuum.", font_size=36)
        explanation_c2 = MathTex("c \approx 300,000,000 \text{ m/s}", font_size=48)
        explanation_c_group = VGroup(explanation_c1, explanation_c2).arrange(DOWN, buff=0.4).next_to(full_equation_group, DOWN, buff=1)
        self.play(Indicate(c_label, color=RED))
        self.play(Write(explanation_c_group))
        self.wait(2)
        self.play(FadeOut(explanation_c_group))

        # 4. Explain the 'c^2' part
        c_squared_part = VGroup(equation[3], equation[4])
        explanation_c_squared1 = Text("c-squared is a massive number.", font_size=36)
        explanation_c_squared2 = MathTex("c^2 \approx 90,000,000,000,000,000", font_size=48)
        explanation_c_squared_group = VGroup(explanation_c_squared1, explanation_c_squared2).arrange(DOWN, buff=0.4).next_to(full_equation_group, DOWN, buff=1)
        
        self.play(Indicate(c_squared_part, color=RED))
        self.play(Write(explanation_c_squared_group))
        self.wait(3)
        self.play(FadeOut(explanation_c_squared_group))
        self.play(FadeOut(labels))
        self.play(equation.animate.move_to(ORIGIN).scale(1/3 * 2)) # Center and resize equation
        self.wait(1)

        # 5. Demonstrate the core concept: mass-energy equivalence
        core_concept = Text("A tiny amount of mass can be converted into...", font_size=36).to_edge(UP)
        self.play(Write(core_concept))
        self.wait(1)

        # Create a small dot representing mass
        mass_dot = Dot(point=LEFT * 3, radius=0.1, color=BLUE)
        mass_text = Text("Mass", font_size=24).next_to(mass_dot, DOWN)
        mass_vgroup = VGroup(mass_dot, mass_text)

        # Create a large glowing circle representing energy
        energy_burst = Circle(radius=2, color=YELLOW, fill_color=YELLOW, fill_opacity=0.5).move_to(RIGHT * 3)
        energy_text = Text("A VAST amount of Energy", font_size=36).next_to(energy_burst, DOWN)
        energy_vgroup = VGroup(energy_burst, energy_text)

        # Show the initial mass
        self.play(FadeIn(mass_vgroup))
        self.wait(1)

        # Animate the transformation
        arrow = Arrow(mass_dot.get_right(), energy_burst.get_left(), buff=0.2)
        self.play(GrowArrow(arrow))
        self.play(Transform(mass_dot.copy(), energy_burst), FadeIn(energy_vgroup))
        self.wait(3)

        # 6. Conclusion
        # Fade out the demonstration elements
        self.play(
            FadeOut(core_concept),
            FadeOut(mass_vgroup),
            FadeOut(energy_vgroup),
            FadeOut(arrow)
        )

        # Display final message
        final_text = Text(
            "This is the principle behind nuclear power and the stars.",
            font_size=36
        ).next_to(equation, DOWN, buff=1)

        self.play(Write(final_text))
        self.wait(4)

        # Fade out the entire scene
        self.play(FadeOut(equation), FadeOut(final_text))
        self.wait(1)
